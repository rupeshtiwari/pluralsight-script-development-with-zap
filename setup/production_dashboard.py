#!/usr/bin/env python3
"""Generate a local, offline-first production cockpit from ACTUAL ZAP batch logs.

It does not start ZAP, synthesize evidence, edit logs, or approve narration.
It works after setup/run_all_demo_preflights.py has copied each demo's logs.
Standard-library only; every displayed observed value comes from a proof file.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import shutil
from production_plan import LAB_DIRS, LO, PLAN, REPO_URL, SCREENS, screen_action
from narration_handoff import validate_final, evidence_ready, tts_text, write_narration_handoff

DEMOS = {
    "m1-demo1": "Injection, XSS and CSRF",
    "m1-demo2": "JavaScript HTTP Sender",
    "m1-demo3": "Jython scanning and authentication",
    "m2-demo1": "Authenticated GitHub Actions",
    "m2-demo2": "ZAP API, reports and Insights",
    "m2-demo3": "Alert filtering and quality gate",
}
PALETTE = {"pink": "#FF1675", "inky": "#130F25", "blue": "#00A3FF",
           "purple": "#770EF7", "yellow": "#FFC942", "orange": "#FF7B01",
           "green": "#02E088", "stop": "#B9004B", "muted": "#585FA2"}
ANSI = re.compile(r"\x1b\[[0-9;]*m")
FIELD = re.compile(r"^\s*★\s*(?:(?:│\s*)?(.+?)\s*│\s*(.*)|(.+?):\s+(.+))$")
STEP = re.compile(r"(?=^## Step [1-4]\b)", re.M)
BEAT = re.compile(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(\d+)(?:\s+spoken\s+words)?</td>\s*</tr>", re.S | re.I)


def clean(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]*>", " ", text)).strip()


def h(text: object) -> str:
    return html.escape(str(text), quote=True)


def focused_labels(raw: str) -> set[str]:
    """Recognize the primary pink focus chosen by the real terminal formatter.

    The raw log is required; never invent an editor highlight when absent.
    """
    names = set()
    for line in raw.splitlines():
        if "\x1b[38;2;255;22;117m" not in line:
            continue
        match = FIELD.match(ANSI.sub("", line))
        if match:
            label = match.group(1) if match.group(1) is not None else match.group(3)
            names.add(label.strip().removesuffix(":"))
    return names


def rows_from_terminal(proof: str, raw: str = "") -> list[dict]:
    """Parse original or new star rows without changing any value or label."""
    focus = focused_labels(raw)
    rows = []
    for line in ANSI.sub("", proof).splitlines():
        m = FIELD.match(line)
        if not m:
            continue
        label, value = (m.group(1), m.group(2)) if m.group(1) is not None else (m.group(3), m.group(4))
        if not (label and value):
            continue
        name = label.strip().removesuffix(":")
        rows.append({"label": name, "value": value.strip(), "focus": name in focus})
    return rows


def style_terminal(text: str, focus: set[str] | None = None) -> str:
    """Mirror captured terminal text and its primary-focus semantics in HTML.

    Formatting spans are display-only; removing markup yields the identical
    normalized stdout text with line order and whitespace preserved.
    """
    focus = focus or set()
    lines = []
    table_line = re.compile(r"^(\s*★\s*│\s*)(.+?)(\s*│\s*)(.*)$")
    for line in ANSI.sub("", text).splitlines():
        escaped = h(line)
        if "✘ FAIL" in line or "SYNC MISMATCH" in line:
            escaped = f'<span class="stopline">{escaped}</span>'
        elif "✔ PASS" in line:
            escaped = f'<span class="passline">{escaped}</span>'
        elif (m := table_line.match(line)):
            label = m.group(2).strip().removesuffix(":")
            color = "focused-value" if label in focus else "ordinary-value"
            escaped = (f'<span class="field-prefix">{h(m.group(1))}</span>'
                       f'<span class="field-label">{h(m.group(2))}</span>'
                       f'<span class="field-prefix">{h(m.group(3))}</span>'
                       f'<span class="{color}">{h(m.group(4))}</span>')
        elif line.lstrip().startswith("★"):
            escaped = f'<span class="fieldline">{escaped}</span>'
        elif "WHAT:" in line or "WHY:" in line:
            escaped = f'<span class="subline">{escaped}</span>'
        lines.append(escaped)
    return "\n".join(lines)


def role_source(block: str, role: str) -> str:
    pattern = r"<details(?:\s+open)?>\s*<summary>\s*<img\b[^>]*" + re.escape(role) + r"[^>]*>.*?</summary>(.*?)</details>"
    m = re.search(pattern, block, re.I | re.S)
    if not m:
        return "<p class='hold'>Role instructions unavailable. Consult the approved playbook.</p>"
    raw = m.group(1).strip()
    raw = re.sub(r"<img\b[^>]*>", "", raw, flags=re.I)
    raw = re.sub(r"<script\b[^>]*>.*?</script>", "", raw, flags=re.I | re.S)
    raw = re.sub(r"<style\b[^>]*>.*?</style>", "", raw, flags=re.I | re.S)
    raw = re.sub(r"`([^`]+)`", lambda t: "<code>" + h(t.group(1)) + "</code>", raw)
    return raw


def beat_rows(block: str) -> list[tuple[str, str, int]]:
    source = role_source(block, "NARRATOR")
    return [(clean(a), clean(b), int(n)) for a, b, n in BEAT.findall(source)]


def segment(block: str, heading: str) -> str:
    rx = r"^### " + re.escape(heading) + r"\s*\n(.*?)(?=^### |^<details|\Z)"
    m = re.search(rx, block, re.M | re.S)
    return clean(m.group(1)) if m else ""


def actual_paths(root: Path, demo: str, index: int) -> tuple[Path, Path]:
    logs = root / demo / "logs"
    proof = logs / f"preflight-step-{index:02}.log"
    raw = logs / ".producer" / f"reference-step-{index:02}.raw.log"
    return proof, raw


def report_paths(root: Path, demo: str) -> list[Path]:
    logs = root / demo / "logs"
    if not logs.exists():
        return []
    return [p for p in sorted(logs.rglob("*.json")) if p.is_file() and p.stat().st_size < 5_000_000][:12]


def step_html(root: Path, demo: str, step: int, block: str, command: str, batch_status: str, imported_speech: dict | None = None) -> str:
    first = block.splitlines()[0].replace("## Step ", "Step ").strip()
    title = first.split(" — ", 1)[-1]
    proof, raw = actual_paths(root, demo, step)
    available = proof.is_file()
    transcript = proof.read_text(encoding="utf-8", errors="replace") if available else ""
    raw_text = raw.read_text(encoding="utf-8", errors="replace") if raw.is_file() else ""
    focus = focused_labels(raw_text)
    rows = rows_from_terminal(transcript, raw_text)
    beats = beat_rows(block)
    if imported_speech:
        beats = [(name, imported_speech.get(field, ''), len(imported_speech.get(field, '').split()))
                 for name, field in (('Before command', 'before'), ('During result', 'during'), ('After decision', 'after'))]
    speech = imported_speech or ({'step':step,'command':command,
                                    'before':beats[0][1],'during':beats[1][1],'after':beats[2][1]}
                                   if len(beats)==3 else None)
    stage_text_v2 = tts_text({'steps':[speech]},'v2') if speech else ''
    stage_text_v4 = tts_text({'steps':[speech]},'v4') if speech else ''
    if available and ("✔ PASS" not in transcript or "✘ FAIL" in transcript or not batch_status.startswith("PREFLIGHT PASSED")):
        # Never display a failed or incomplete capture as a verified success.
        verified = False
    else:
        verified = available
    summary = "<span class='ready'>REAL TERMINAL PROOF</span>" if verified else "<span class='hold'>HOLD — NO VERIFIED STEP PROOF</span>"
    problem = segment(block, "Learning Goal") or segment(block, "The small problem to solve") or segment(block, "The specific problem")
    screen = segment(block, "Demo Workspace") or segment(block, "Where to go") or segment(block, "Which application and screen?")
    if not problem:
        m = re.search(r"### (?:Learning Goal|The small problem to solve|The specific problem)\s*\n\s*([^\n]+)", block)
        problem = m.group(1) if m else "Review the approved playbook for the step's security question."
    if not screen:
        screen = "See the Recorder instructions for the exact application, source file and pane."
    lab = LAB_DIRS[demo]
    cue = screen_action(demo, step)
    cd_command = f'cd "$HOME/pluralsight-script-development-with-zap/{lab}"'
    branch_command = ('cd "$HOME/pluralsight-script-development-with-zap"' + "\n" +
                      f"git switch {demo}-before" + "\n" + cd_command)
    source_url = f"{REPO_URL}/blob/{demo}-before/{lab}/steps/{command.removeprefix('./steps/')}"
    src_path = cue['source'] if cue['source'].startswith(('runtime/','docs/','.github/')) else lab+'/'+cue['source']
    # Source files authored during a learner exercise can be absent on *-before.
    # Link to the real starter folder rather than inventing an existing file URL.
    creates_source = cue['source'].startswith(('zap-scripts/','ci/'))
    src_on_before = (f"{REPO_URL}/tree/{demo}-before/{lab}" if creates_source else
                     f"{REPO_URL}/blob/{demo}-before/{src_path}")
    source_link_caption = ('Open starter folder; create the approved source if missing'
                           if creates_source else 'Open existing starter source context')
    nav_html = (f"<section class='location-guide'><h3>Demo workspace · app, branch and terminal</h3>"
                f"<p><b>Step A · open application manually:</b> {h(cue['application'])}. "
                f"<b>Required on-screen source/pane:</b> <code>{h(cue['source'])}</code> "
                f"→ {h(cue['pane'])}.</p>"
                f"<p><b>Step B · open terminal:</b> Use VS Code → Terminal → New Terminal "
                f"when the application includes VS Code; otherwise open macOS Terminal. "
                f"No manual folder browsing. Paste the following shell command:</p>"
                f"<p><b>Off-camera branch setup:</b> Preserve local edits before switching, then paste:</p>"
                f"<pre class='nav-command'>{h(branch_command)}</pre><button type='button' class='copy-nav' data-cd='{h(branch_command)}'>Copy branch and folder commands</button>"
                f"<p><b>Already on the approved branch?</b> Use this directory command only:</p>"
                f"<pre class='nav-command'>{h(cd_command)}</pre><button type='button' class='copy-nav' data-cd='{h(cd_command)}'>Copy cd command</button>"
                f"<p><b>Step C · prepare source and perform the approved action:</b> {h(cue['preparation'])}. "
                f"Then run the concept-named command below, from <code>{h(lab)}</code>. "
                f"Use full-screen capture and 26–30-point source/terminal text.</p>"
                f"<p><b>Step D · visible proof:</b> {h(cue['proof'])}. "
                f"Only highlight values actually present in the current captured take.</p>"
                f"<p><a href='{h(src_on_before)}' target='_blank' rel='noopener'>{h(source_link_caption)}</a> · "
                f"<a href='{h(source_url)}' target='_blank' rel='noopener'>Open the named step script</a> "
                f"· <a href='{h(REPO_URL + '/blob/main/docs/course-outline.md')}' target='_blank' rel='noopener'>Approved course outline</a></p></section>")
    plan = PLAN[demo][step-1]
    region, first_key, second_key, arrow, callout = plan
    def match_row(key: str):
        return next((r for r in rows if key and (r['label'] == key or key.lower() in r['label'].lower())), None)
    primary = match_row(first_key)
    secondary = match_row(second_key)
    def claim(row, expected):
        if not row:
            return f"<span class='hold'>NOT OBSERVED: {h(expected)} — do not highlight a guessed value</span>"
        return (f"<code class='pink-label'>{h(row['label'])}</code> → "
                f"<code class='actual-value'>{h(row['value'])}</code>"
                f" <small>(from this real captured output)</small>")
    source_alert = 'VALIDATED batch terminal evidence' if verified else 'HOLD — this step did not pass the Developer batch; overlays are planning instructions only'
    editor_detail = f"""<p class='notice'><b>Overlay status:</b> {h(source_alert)}. Match every overlay to the Recorder's SAME TAKE.</p>
    <table class='editor-map'><thead><tr><th>Capture time / visual change</th><th>Precise editing action</th><th>What the learner should read</th></tr></thead><tbody>
    <tr><th>Before Enter · source and command</th><td>Cut typing/backspaces. Place a <b>single large blue region box</b> (<code>#00A3FF</code>) around the source/command. Show the whole approved command, hold ~8 s, remove the box as Enter is pressed. No competing callouts.</td><td><code>{h(command)}</code></td></tr>
    <tr><th>After output arrives · 6–8 s</th><td>Move the large blue box to the <b>entire relevant result area</b>: {h(region)}. Keep the output framed; replace the first box, do not leave it over an empty pane.</td><td>{claim(primary,first_key)}</td></tr>
    <tr><th>Within result · next 6–8 s</th><td>Inside that region, add a small <b>Transform Pink (#FF1675) label/highlight</b> directly on the FIRST evidenced value below. Only one primary value highlighted at once, with legible high-contrast text.</td><td>{claim(primary,first_key)}</td></tr>
    <tr><th>If two actual fields remain · 6–8 s</th><td>Replace the pink label or retain only the one region box. Use a slim <b>purple arrow (#770EF7)</b> when both endpoints are visible and meaningful: {h(arrow)}. If the second field was not captured, omit the arrow and mark HOLD.</td><td>{claim(secondary,second_key) if second_key else '<span class="hold">Separate GUI proof required</span>'}</td></tr>
    <tr><th>Only when same screen stays beyond 12 s</th><td>Do not leave an idle frame. Only when there is no other meaningful box/arrow/label movement, at ~12 s temporarily add a compact <b>yellow callout</b> (<code>#FFC942</code>, Inky Blue text), showing the gist below for 6–8 s. Remove before the next focus change. This is EDITOR TEXT, not a spoken narrator line.</td><td><strong>{h(callout)}</strong></td></tr>
    <tr><th>Pane change / final</th><td>Remove the previous box, arrow and label immediately as you switch. Cut scan waits, typo/backspace takes and unneeded idle frames. Allow the final result ~6–8 s and preserve 8 s raw footage around meaningful clicks.</td><td>One operator decision backed by displayed evidence</td></tr>
    </tbody></table>
    <p><b>Camtasia ordering:</b> Source → named command → run → real output → frame blue region → pink label exact value → purple arrow only where a real relationship is visible → optional short gist callout when otherwise static → operator result → remove all decorations. Match each narrated sentence, not arbitrary fixed timestamps. The terminal may require long execution time; skip waiting footage but never cut out the actual result.</p>
    <p><b>Safety:</b> The annotation cannot assert an unseen XSS execution, console emission, login session, genuine alert, or process exit. Raw JSON remains visible where the approved objective requires inspecting its structure.</p>"""
    # Audio-to-edit mapping uses only the exact lines currently being displayed.
    # A later narrator import replaces these drafts without changing step order.
    stage_targets = (
        ("Before Enter", "Source/pane + approved command; large blue square", command),
        ("After completion", "Blue output-area square; Transform Pink label only on the recorded field", primary['value'] if primary else "HOLD — primary value not observed"),
        ("After results", "Retire old callout, then conditional purple arrow to the second actual field", secondary['value'] if secondary else "HOLD — second value not observed"),
    )
    synchronized = "".join(
        "<tr><th>"+h(stage_targets[i][0])+"</th><td>"+h(stage_targets[i][1])+"</td>"
        "<td>"+h(stage_targets[i][2])+"</td><td>"+h(beat[1])+"</td></tr>"
        for i, beat in enumerate(beats[:3])
    )
    editor_detail += ("<h3>Synchronize with the narrator’s exact words</h3>"
                      "<p>Lines below are " + ("imported narration" if imported_speech else "source draft narration, NOT FINAL") + ". "
                      "Once an approved narrator returns a revised script, use the imported lines; do not reuse old overlay timecodes.</p>"
                      "<table class='editor-map'><thead><tr><th>Screen event</th><th>Action in Camtasia</th>"
                      "<th>Observed value</th><th>Exact words to align</th></tr></thead><tbody>"
                      + synchronized + "</tbody></table>")
    fields = ("<table class='evidence-table'><thead><tr><th>Observed terminal field</th>"
              "<th>Exact displayed value</th></tr></thead><tbody>" + "".join(
                f"<tr><th scope='row'>{h(r['label'])}</th><td class='actual {'focus' if r['focus'] else ''}'>{h(r['value'])}</td></tr>" for r in rows
              ) + "</tbody></table>") if rows else ("<p class='hold'>No parsed result fields in this capture. "
                                                    "Read the untouched terminal transcript below.</p>")
    timeline = []
    stages = ["BEFORE ENTER · source/command visible", "AFTER COMPLETION · actual output field visible", "AFTER RESULT · final field and operator decision"]
    for n, (shot, spoken, count) in enumerate(beats):
        actual_count = len(spoken.split())
        valid = actual_count == count and count <= 27
        timeline.append(f"<article class='beat'><div class='beat-index'>{n + 1:02}</div>"
                        f"<div><span class='eyebrow'>{h(stages[n] if n < 3 else shot)}</span>"
                        f"<p class='shot'>{h(shot)}</p><p class='speak'>{h(spoken)}</p>"
                        f"<small>{actual_count} spoken words · {'count verified' if valid else 'CHECK WORD COUNT'}</small>"
                        f"</div></article>")
    if len(timeline) != 3:
        timeline = ["<p class='hold'>The approved three-beat narration is unavailable. Do not record invented lines.</p>"]
    source_status = ("Imported narration text. CQA approval and recorded evidence are independent requirements."
                     if imported_speech else
                     "Developer reference DRAFT, not final narration. Confirm against the Recorder's same-take GUI or GitHub Actions evidence.")
    proof_html = (f"<div class='statusline'>{summary} <span>Step {step}/4 · Source: {h(proof.name)}</span></div>"
                  f"<div class='columns'><section class='pane'><h3>Expected decision and screen</h3>"
                  f"<p><b>Why it matters</b> {h(problem)}</p>{nav_html}"
                  f"<h3>Exact concept-named command</h3><pre class='command'>{h(command)}</pre>"
                  f"<p class='subtle'>Show the command, then press Enter once. These are the approved commands; "
                  f"no prerecorded security evidence is substituted.</p></section>"
                  f"<section class='pane'><h3>Actual result fields</h3>{fields}</section></div>"
                  f"<details class='transcript' open><summary>Exact terminal transcript · captured data</summary>"
                  f"<pre class='terminal'>{style_terminal(transcript, focus) if available else h('NO REAL PRE-FLIGHT LOG FOR THIS STEP')}</pre></details>"
                  f"<details class='transcript'><summary>Untouched raw audit evidence</summary>"
                  f"<pre class='terminal'>{h(raw.read_text(encoding='utf-8',errors='replace')) if raw.is_file() else h('No raw audit file captured; pending Mac preflight')}</pre></details>")
    source_textareas = (f"<textarea hidden class='step-v2' readonly>{h(stage_text_v2)}</textarea>"
                        f"<textarea hidden class='step-v4' readonly>{h(stage_text_v4)}</textarea>")
    return (f"<section class='step' data-step='{step}' id='{demo}-step-{step}'>"
            f"<div class='stephead'><span class='stepn'>STEP {step:02}</span><h2>{h(title)}</h2></div>"
            f"<div class='role-panel' data-role='narrator'><p class='notice'>{h(source_status)}</p>"
            f"<div class='columns'><div><h3>What the learner sees</h3>"
            f"<p>{h(cue['application'])}: {h(cue['pane'])}</p>{nav_html}<pre class='command'>{h(command)}</pre>"
            f"<h3>After the command</h3>{fields if verified else '<p class="hold">Real output not verified</p>'}</div>"
            f"<div><h3>Exact ElevenLabs wording · three spoken beats</h3>{''.join(timeline)}</div></div>"
            f"<details class='transcript'><summary>View exact captured terminal transcript</summary>"
            f"<pre class='terminal'>{style_terminal(transcript, focus) if available else h('Not captured')}</pre></details></div>"
            f"<div class='role-panel' data-role='recorder'><h3>Recorder · exact actions and holds</h3>"
            f"{nav_html}<p><b>Exact command to execute once:</b></p><pre class='command'>{h(command)}</pre>"
            f"<p><b>After Enter:</b> Wait for real completion. Show the actual proof pane and hold each evidenced result 6–8 seconds. If it fails, keep the failure visible and retake after fixing the cause. Never paste prior-run output.</p>{role_source(block, 'RECORDER')}"
            f"<details class='transcript'><summary>Verified terminal output for the take comparison</summary>"
            f"<pre class='terminal'>{style_terminal(transcript, focus) if available else h('Not captured')}</pre></details></div>"
            f"<div class='role-panel' data-role='editor'><h3>Editor · callouts, focus and cut choreography</h3>"
            f"{editor_detail}<details class='transcript'><summary>Original approved editor notes</summary>{role_source(block, 'EDITOR')}</details></div>"
            f"<div class='role-panel' data-role='developer'><h3>Developer · executable contract and current proof</h3>"
            f"{proof_html}</div>"
            f"<div class='role-panel' data-role='cqa'><h3>Technical CQA · approve only observable proof</h3>"
            f"<p><b>Security question:</b> {h(problem)}</p><p><b>Command:</b> <code>{h(command)}</code></p>"
            f"<p><b>Current proof status:</b> {'Terminal PASS observed; external GUI/CI unverified' if verified else 'HOLD — missing or failed preflight output'}</p>"
            f"<p>Require the actual application or ZAP result, source SHA and take ID. A terminal check is not evidence that a GUI pane or hosted runner displayed a result.</p>"
            f"<details class='transcript'><summary>Review untouched proof</summary><pre class='terminal'>{style_terminal(transcript, focus) if available else h('Not captured')}</pre></details>"
            f"</div>{source_textareas}</section>")


def render_demo(root: Path, row: dict, author_dir: Path) -> str:
    demo = row['demo']
    label = DEMOS[demo]
    proof = row.get('status', 'NOT VERIFIED')
    author_path = author_dir / f"{demo}.md"
    author = author_path.read_text(encoding='utf-8') if author_path.is_file() else ""
    blocks = STEP.split(author)[1:5]
    if len(blocks) != 4:
        blocks = [f"## Step {i} — source playbook unavailable\n" for i in range(1,5)]
    commands = row.get("step_commands") or []
    if not commands:
        step_file = root / demo / "steps-and-output.md"
        if step_file.is_file():
            commands = re.findall(r"^## Step [1-4] — (\./steps/[a-z0-9-]+\.sh)$", step_file.read_text(encoding="utf-8"), flags=re.M)
    manifest = h(json.dumps(row, indent=2, ensure_ascii=False))
    reports = report_paths(root, demo)
    report_links = "".join(f'<li><a href="{h(demo + "/" + str(p.relative_to(root / demo)))}" target="_blank" rel="noopener">{h(p.relative_to(root / demo))}</a></li>' for p in reports)
    report_section = (f"<details><summary>Captured JSON evidence ({len(reports)})</summary><ul>{report_links}</ul></details>" if reports else "<p class='subtle'>No JSON report file captured here; actual terminal and raw logs remain available.</p>")
    handoff_steps=[]
    draft_steps=[]
    for n, block in enumerate(blocks,1):
        log, raw = actual_paths(root,demo,n)
        transcript = log.read_text(encoding='utf-8',errors='replace') if log.is_file() else ''
        raw_text = raw.read_text(encoding='utf-8',errors='replace') if raw.is_file() else ''
        beats=beat_rows(block)
        cmd=commands[n-1] if len(commands)>=n else 'NOT AVAILABLE'
        handoff_steps.append({
            'step':n, 'title':block.splitlines()[0].replace('## Step ', 'Step ').strip(),
            'working_directory': LAB_DIRS[demo], 'navigate':f'cd "$HOME/pluralsight-script-development-with-zap/{LAB_DIRS[demo]}"',
            'command':cmd, 'source_file':screen_action(demo,n)['source'], 'screen_action':screen_action(demo,n),
            'screen':segment(block,'Demo Workspace') or segment(block,'Where to go') or segment(block,'Which application and screen?'),
            'draft_beats':beats,'editor_targets':dict(zip(('region','first_field','second_field','arrow','gist_callout'),PLAN[demo][n-1])),
            'observed_fields':rows_from_terminal(transcript,raw_text),
            'terminal_log':f'logs/preflight-step-{n:02}.log',
            'raw_log':f'logs/.producer/reference-step-{n:02}.raw.log',
            'observed_transcript':transcript,
            'proof_verified':proof.startswith('PREFLIGHT PASSED') and '✔ PASS' in transcript and '✘ FAIL' not in transcript
        })
        if len(beats)==3:
            draft_steps.append({'step':n,'command':cmd,'before':beats[0][1],'during':beats[1][1],'after':beats[2][1]})
    package={'schema_version':1,'demo':demo,'label':label,'source_repo':REPO_URL,
             'reference_branch':f'{demo}-after','starter_branch':f'{demo}-before',
             'reference_sha':row.get('sha',''),'learning_objectives':LO[demo],
             'status':proof,'external_gui_ci_proof':'PENDING independent matching same-take evidence',
             'recording_take_id':'NOT PROVIDED','steps':handoff_steps}
    write_narration_handoff(root/demo,package)
    final_path = root/demo/'narration-final.json'
    imported=None; import_errors=[]
    if final_path.is_file():
        try:
            incoming=json.loads(final_path.read_text(encoding='utf-8'))
            imported,import_errors=validate_final(incoming,demo,row.get('sha',''),commands)
        except (ValueError, UnicodeDecodeError) as exc:
            import_errors=[str(exc)]
    steps = ''.join(step_html(root, demo, n, block, commands[n-1] if len(commands)>=n else "Not available — check batch manifest",
                              proof, imported['steps'][n-1] if imported else None)
                    for n, block in enumerate(blocks, 1))
    approved = bool(imported and evidence_ready(imported) and proof.startswith('PREFLIGHT PASSED'))
    data = imported if imported else ({'opening':'','closing':'','steps':draft_steps} if len(draft_steps)==4 else None)
    if data:
        text_v2=tts_text(data,'v2');text_v4=tts_text(data,'v4')
    else:
        text_v2=text_v4=''
    if imported:
        status_label=('AUTHOR SIGN-OFF DECLARED — verify matching proof files before delivery'
                      if approved else 'IMPORTED FINAL DRAFT — same-take evidence and CQA still pending')
    else:
        status_label='REFERENCE DRAFT ONLY — import narration-final.json after evidence-aware narrator review'
    if import_errors:
        status_label='HOLD — invalid narration-final.json: '+ '; '.join(import_errors)
    # The provided model's pause tags are displayed ONLY in editable/copyable text areas.
    # Stage headings and production cues do not enter the ElevenLabs payload.
    narration = f"""<section class='narration-export'>
    <h2>Whole-demo ElevenLabs narration · copy only after evidence review</h2>
    <p class='notice'>{h(status_label)}. The text is generated from the existing three recorded-stage beats; it is not an invented security result.</p>
    <p><label for='model-{h(demo)}'><b>ElevenLabs speech model:</b></label>
    <select class='modelselect' id='model-{h(demo)}'><option value='v2'>Multilingual v2 / Flash v2 & v2.5 · timed SSML breaks</option>
    <option value='v4'>Eleven v3 / v4 · approximate [pause] audio tag</option></select></p>
    <p class='subtle'>Each three-beat step is BEFORE command → one-second transition → DURING visible results → one-second transition → AFTER operator decision. The first transition is after Enter and before the verified result; if a scan takes longer, the Editor cuts the wait and inserts the measured one-second gap at the completed-result edit. Eleven v3/v4 cannot guarantee exact pause duration.</p>
    <div class='copyrow'><button type='button' class='copy-demo-narration'>Copy entire demo narration ({'APPROVAL DECLARED' if approved else 'UNVERIFIED DRAFT'})</button>
    <button type='button' class='copy-narration-step'>Copy selected step</button>
    <a href='{h(demo)}/NARRATION_HANDOFF.md'>Narrator handoff instructions</a> · <a href='{h(demo)}/narration-handoff.json'>Machine-readable handoff</a>
    </div>
    <textarea class='voice-text voice-v2' spellcheck='false' readonly aria-label='ElevenLabs Multilingual v2 script'>{h(text_v2)}</textarea>
    <textarea class='voice-text voice-v4' spellcheck='false' readonly hidden aria-label='ElevenLabs v3/v4 script'>{h(text_v4)}</textarea>
    <p class='subtle'>After the narrator returns <code>narration-final.json</code> and <code>narration-final.md</code>, place both in <code>{h(demo)}/</code>, run <code>./refresh.sh</code> in the batch folder and refresh this browser. Never paste production labels or an unverified draft into a published course.</p>
    </section>"""
    lab=LAB_DIRS[demo]
    code_links=f"""<section class='links'><b>Approved code references:</b>
      <a target='_blank' rel='noopener' href='{h(REPO_URL+'/tree/'+demo+'-before/'+lab)}'>Starter · {h(demo)}-before</a> ·
      <a target='_blank' rel='noopener' href='{h(REPO_URL+'/tree/'+demo+'-after/'+lab)}'>Completed reference · {h(demo)}-after</a> ·
      <a target='_blank' rel='noopener' href='{h(REPO_URL+'/blob/main/docs/course-outline.md')}'>Approved outline</a>
      <p>Learning objectives: {h(LO[demo])}</p></section>"""
    return (f"<article class='demo' data-demo='{h(demo)}'><div class='demo-heading'>"
            f"<div><span class='eyebrow'>{h(demo.upper())} · APPROVED COURSE DEMO</span>"
            f"<h1>{h(label)}</h1><p>{h(proof)}</p></div><div class='sha'>SOURCE SHA<br><code>{h(row.get('sha') or 'NOT CAPTURED')}</code></div></div>"
            f"{code_links}"
            f"<div class='role-panel' data-role='developer'><div class='pill-row'>"
            f"<span class='pill'>Startup exit: {h(row.get('startup_exit'))}</span>"
            f"<span class='pill'>Preflight exit: {h(row.get('preflight_exit'))}</span>"
            f"<span class='pill'>Cleanup exit: {h(row.get('cleanup_exit'))}</span></div>"
            "<p>Batch evidence: " + " · ".join(
                f"<a href='{h(demo + '/' + name)}'>{h(label)}</a>"
                for name,label in (("steps-and-output.md","captured steps and output"),("production-guide.html","per-demo HTML"),("narration-draft.md","initial narration"),("manifest.json","manifest"),("NARRATION_HANDOFF.md","narration handoff"),("narration-handoff.json","handoff JSON"))
                if (root/demo/name).is_file()
            ) + ". Never treat missing evidence as generated.</p>"
            f"{report_section}<details><summary>Full SHA and process results</summary><pre>{manifest}</pre></details></div>"
            f"<div class='role-panel' data-role='cqa'><p class='notice'>Required release proof: one authorized app run, actual ZAP GUI or hosted CI evidence where relevant, output/alert reconciliation, process exit, source SHA, and take ID. Structural CI is separate.</p></div>"
            f"<nav class='step-nav' aria-label='Steps for {h(label)}'>" + ''.join(
                f"<button class='stepbtn' data-target-step='{i}' type='button'>Step {i}</button>" for i in range(1,5)) + "</nav>"
            f"<div class='role-panel' data-role='narrator'>{narration}</div>"
            f"{steps}</article>")


CSS = r"""
:root{font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#130F25;background:#EBEFF5;font-size:16px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0}button,select,input{font:inherit}a{color:#770EF7}a:focus-visible,button:focus-visible,select:focus-visible{outline:3px solid #FF1675;outline-offset:3px}
header{background:#130F25;color:#fff;padding:20px max(20px,calc((100% - 1540px)/2));border-bottom:5px solid #FF1675}header h1{font-size:clamp(1.3rem,2.2vw,2rem);margin:4px 0}header p{max-width:850px;color:#EBEFF5}header .eyebrow{color:#FFC942}
main{max-width:1600px;margin:auto;display:grid;grid-template-columns:260px minmax(0,1fr);gap:20px;padding:20px}
aside{position:sticky;top:12px;align-self:start;background:#fff;border:1px solid #cfd7e9;border-radius:14px;padding:16px;max-height:calc(100vh - 24px);overflow:auto}aside h2{font-size:1rem}aside nav{display:grid;gap:6px}
.navdemo,.rolebtn,.stepbtn{cursor:pointer;text-align:left;border:1px solid #d4dced;padding:12px 14px;border-radius:9px;background:#fff;color:#130F25;font-weight:650}.navdemo:hover,.rolebtn:hover,.stepbtn:hover{border-color:#FF1675;background:#fdf0f6}.navdemo.active,.rolebtn.active,.stepbtn.active{background:#130F25;color:#fff;border-left:5px solid #FF1675}
.content{min-width:0}.toolbar{position:sticky;top:0;z-index:5;background:#EBEFF5;padding:10px 0 16px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}.rolebar{display:flex;flex-wrap:wrap;gap:6px}.search{flex:1;min-width:160px;border:1px solid #adb9d4;border-radius:9px;padding:12px}.toolbar label{font-weight:650}
.status{font-size:.86rem;font-weight:750;background:#FFC942;color:#130F25;border-radius:8px;padding:8px 12px}.demo{display:none}.demo.active{display:block}.demo-heading{background:#fff;border-radius:14px;border:1px solid #ccd4e2;padding:22px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px}.demo-heading h1{font-size:clamp(1.5rem,2vw,2.3rem);margin:5px 0}.sha{max-width:360px;overflow-wrap:anywhere;font-size:.88rem;text-align:right}
.eyebrow{font-weight:850;letter-spacing:.06em;text-transform:uppercase;color:#770EF7;font-size:.75rem}.role-panel{display:none}.role-panel.active{display:block}.step{display:none;background:#fff;border:1px solid #cfd7e9;border-radius:14px;padding:24px;margin:16px 0;overflow:hidden}.step.active{display:block}.stephead{display:flex;align-items:center;gap:12px;margin-bottom:18px}.stephead h2{margin:0;font-size:1.3rem}.stepn{background:#FF1675;color:#fff;padding:8px;border-radius:7px;font-weight:750;white-space:nowrap}
.step-nav{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.columns{display:grid;grid-template-columns:1fr 1.05fr;gap:16px}.columns>div,.columns>.pane{min-width:0;background:#f7f8fb;border-radius:10px;padding:16px;border:1px solid #d6deed}.pane h3,.role-panel h3{margin-top:4px}.notice{padding:12px 16px;background:#fff6df;border-left:4px solid #FFC942;border-radius:7px;margin:12px 0 20px}.subtle{color:#464c70;font-size:.92rem}.hold{font-weight:700;color:#9f0041}.ready{font-weight:800;color:#166c4b}.statusline{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;padding:12px;border-bottom:1px solid #d4dcec;margin-bottom:12px}
.evidence-table{border-collapse:collapse;width:100%;font-size:.9rem;table-layout:fixed}.evidence-table th,.evidence-table td{border:1px solid #cfd9ee;padding:10px;vertical-align:top;overflow-wrap:anywhere;text-align:left}.evidence-table thead th{color:#fff;background:#130F25}.evidence-table tbody th{width:48%;background:#edeafb;color:#36225b}.evidence-table tbody .actual{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:650;color:#130F25;background:#f7f8fc}.evidence-table tbody .actual.focus{font-weight:850;color:#FF1675;background:#130F25}
pre,.terminal{max-width:100%;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;background:#130F25;color:#f6f6fa;border-radius:10px;padding:18px;font:0.89rem/1.75 ui-monospace,SFMono-Regular,Menlo,monospace}.command{font-size:1rem;font-weight:700;border-left:6px solid #FF1675;color:#FFC942}.terminal{min-height:80px}.fieldline{color:#00A3FF}.field-prefix{color:#00A3FF}.field-label{color:#b792ff}.focused-value{color:#FF1675;font-weight:800}.ordinary-value{color:#f6f6fa}.passline{color:#02E088}.stopline{background:#B9004B;color:#fff;padding:1px 3px}.subline{color:#00A3FF}
details.transcript{background:#f8f9fc;border:1px solid #d0d9e9;border-radius:10px;margin:14px 0;padding:0 14px}details.transcript summary{cursor:pointer;font-weight:750;padding:14px 0;color:#130F25}details.transcript pre{margin:0 0 14px}
.beat{border:1px solid #d6dcec;border-left:5px solid #770EF7;display:grid;grid-template-columns:40px 1fr;gap:12px;border-radius:9px;padding:12px;background:#fff;margin:10px 0}.beat-index{font-weight:850;color:#FF1675;font-size:1.2rem}.beat p{margin:.35rem 0}.shot{font-size:.86rem;color:#565d7c}.speak{font-weight:650;font-size:1.07rem;line-height:1.58}.beat small{color:#555e7a}
.role-panel table{border-collapse:collapse;width:100%;margin:12px 0}.role-panel th,.role-panel td{border:1px solid #d5dcea;padding:11px;text-align:left;vertical-align:top}.role-panel th{background:#130F25;color:#fff}.role-panel code{color:#ab0050;overflow-wrap:anywhere}.pill-row{display:flex;gap:8px;flex-wrap:wrap}.pill{border:1px solid #808abc;border-radius:18px;padding:7px 10px;font-size:.85rem}.footer{border-top:1px solid #bac5da;margin-top:22px;padding:16px;color:#434b66}
@media (max-width:950px){main{grid-template-columns:1fr}aside{position:static;max-height:none}aside nav{grid-template-columns:repeat(2,minmax(0,1fr))}.columns{grid-template-columns:1fr}.sha{text-align:left}}@media(max-width:600px){main{padding:10px}aside nav{grid-template-columns:1fr}.step{padding:13px}.toolbar{position:static}.rolebtn{padding:9px 10px}.stephead{align-items:flex-start}.stephead h2{font-size:1.08rem}}

.location-guide{padding:12px 14px;background:white;border:1px solid #b3c9ee;border-radius:10px;margin:12px 0}.location-guide p{margin:9px 0}.copy-nav{cursor:pointer;margin:4px 0 10px;padding:7px 12px;border:2px solid #00A3FF;background:#fff;color:#130F25;border-radius:8px;font-weight:750}.nav-command{background:#130F25;color:#FFC942;font-size:1.02rem;padding:14px;border-left:6px solid #00A3FF}.links{background:#fff;border:1px solid #d4dce8;border-radius:10px;padding:12px 18px;margin:14px 0}.links p{margin-bottom:0;color:#353552}
.editor-map{width:100%;border-collapse:collapse}.editor-map th,.editor-map td{padding:12px;border:1px solid #d4d9e5;text-align:left;vertical-align:top}.editor-map thead{background:#130F25;color:white}.editor-map tbody th{background:#eee9f5;width:22%;color:#130F25}.editor-map .actual-value,.pink-label{background:#130F25;color:#FF1675;padding:3px 5px;border-radius:4px;overflow-wrap:anywhere}
.narration-export{background:#fff;border:1px solid #d5dceb;padding:14px;border-radius:12px;margin:12px 0}.narration-export h2{font-size:1.12rem}.narration-export select{padding:10px 14px;border:1px solid #585FA2;border-radius:7px;max-width:100%;background:white}.voice-text{width:100%;min-height:260px;resize:vertical;padding:16px;background:#130F25;color:#f5f6fc;border-radius:10px;border:2px solid #585FA2;font:1rem/1.75 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre-wrap}.copyrow{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin:14px 0}.copyrow button{cursor:pointer;background:#FF1675;color:#fff;font-weight:750;border:2px solid #B9004B;padding:11px 17px;border-radius:8px}.copyrow button:focus-visible{outline:3px solid #130F25;outline-offset:2px}
@media(max-width:700px){.editor-map{font-size:.85rem}.editor-map th,.editor-map td{padding:7px}.links{overflow-wrap:anywhere}}
"""
JS = r"""
(() => {
  const demos = [...document.querySelectorAll('.demo')];
  const navs = [...document.querySelectorAll('.navdemo')];
  const roles = [...document.querySelectorAll('.rolebtn')];
  let currentDemo = demos[0]?.dataset.demo || '';
  let currentRole = 'recorder';
  let currentStep = 1;
  const search = document.querySelector('#search');
  function activate() {
    demos.forEach(d => {
      d.classList.toggle('active',d.dataset.demo===currentDemo);
      d.querySelectorAll('.role-panel').forEach(el => el.classList.toggle('active',el.dataset.role===currentRole));
      d.querySelectorAll('.step').forEach(el=>el.classList.toggle('active',Number(el.dataset.step)===currentStep));
      d.querySelectorAll('.stepbtn').forEach(el=>el.classList.toggle('active',Number(el.dataset.targetStep)===currentStep));
    });
    navs.forEach(n=>n.classList.toggle('active',n.dataset.demo===currentDemo));
    roles.forEach(r=>r.classList.toggle('active',r.dataset.role===currentRole));
    const name = document.querySelector('.demo.active h1')?.textContent || currentDemo;
    document.querySelector('#location').textContent = `${name} · ${currentRole.toUpperCase()} · Step ${currentStep}`;
    document.title=`${name} — Production Cockpit`;
  }
  function jump(demo,role,step,hash=true){
    if(demo && demos.some(d=>d.dataset.demo===demo))currentDemo=demo;
    if(role && roles.some(r=>r.dataset.role===role))currentRole=role;
    if(step>=1 && step<=4)currentStep=step;
    activate();
    if(hash)history.replaceState(null,'',`#${currentDemo}/${currentRole}/${currentStep}`);
  }
  navs.forEach(n=>n.addEventListener('click',()=>jump(n.dataset.demo,null,1)));
  roles.forEach(r=>r.addEventListener('click',()=>jump(null,r.dataset.role,currentStep)));
  document.querySelectorAll('.stepbtn').forEach(b=>b.addEventListener('click',()=>jump(b.closest('.demo').dataset.demo,null,Number(b.dataset.targetStep))));
  if(location.hash){const parts=location.hash.substring(1).split('/');jump(parts[0],parts[1],Number(parts[2]),false)}
  else activate();
  window.addEventListener('hashchange',()=>{const p=location.hash.slice(1).split('/');jump(p[0],p[1],Number(p[2]),false)});
  search.addEventListener('input',()=>{const q=search.value.trim().toLowerCase();navs.forEach(n=>{
    n.hidden=q!==''&&!n.textContent.toLowerCase().includes(q)
  })});

  async function copyText(value,button){
    if (!value || !value.trim()) {button.textContent='No script available';return}
    try {await navigator.clipboard.writeText(value.trim());button.textContent='Copied · choose matching model and verify evidence'}
    catch {button.textContent='Select text and press Command+C'}
  }
  document.querySelectorAll('.modelselect').forEach(select=>select.addEventListener('change',()=>{
    const demo=select.closest('.demo');const v=select.value;
    demo.querySelector('.voice-v2').hidden=v!=='v2';demo.querySelector('.voice-v4').hidden=v!=='v4';
  }));
  document.querySelectorAll('.copy-nav').forEach(b=>b.addEventListener('click',()=>copyText(b.dataset.cd,b)));
  document.querySelectorAll('.copy-demo-narration').forEach(button=>button.addEventListener('click',()=>{
    const demo=button.closest('.demo'),v=demo.querySelector('.modelselect').value;
    const box=demo.querySelector(v==='v2'?'.voice-v2':'.voice-v4');
    copyText(box.value,button);
  }));
  document.querySelectorAll('.copy-narration-step').forEach(button=>button.addEventListener('click',()=>{
    const demo=button.closest('.demo'),v=demo.querySelector('.modelselect').value;
    const step=demo.querySelector('.step.active');
    const text=step?.querySelector(v==='v2'?'.step-v2':'.step-v4')?.value || '';
    copyText(text,button);
  }));
  document.querySelector('#copy-command').addEventListener('click',async()=>{
    const value=document.querySelector('.demo.active .step.active pre.command')?.textContent;
    if(!value||value.includes('Not available'))return;
    try{await navigator.clipboard.writeText(value.trim());document.querySelector('#copy-command').textContent='Copied'}
    catch {document.querySelector('#copy-command').textContent='Select the command to copy'}
  });
})();
"""


def render_dashboard(batch: Path, rows: list[dict], author_dir: Path) -> Path:
    """Create index.html and handoff data only from real batch outputs and author files."""
    batch = Path(batch).resolve()
    author_dir = Path(author_dir).resolve()
    batch.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("Empty batch manifest: nothing to present")
    if len(rows) != len({r.get('demo') for r in rows}):
        raise ValueError("Duplicate demo IDs in batch manifest")
    for row in rows:
        if row.get('demo') not in DEMOS:
            raise ValueError("Unexpected demo identity in batch manifest")
    status_count=sum(r.get('status','').startswith('PREFLIGHT PASSED') for r in rows)
    nav="".join(f'<button class="navdemo" data-demo="{h(r["demo"])}" type="button">{h(r["demo"].upper())} · {h(DEMOS[r["demo"]])}</button>' for r in rows)
    content="".join(render_demo(batch,r,author_dir) for r in rows)
    header=f"{status_count}/{len(rows)} terminal preflights verified; ZAP GUI/hosted CI and recorded takes still need independent review."
    page=f"""<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ZAP Production Cockpit</title><style>{CSS}</style></head>
<body><header><span class="eyebrow">PLURALSIGHT · DEVELOPER → RECORDER → NARRATOR → EDITOR → TECHNICAL CQA</span><h1>Script Development with ZAP · Production Cockpit</h1><p>{h(header)} This page is generated locally from actual completed-branch preflight outputs. Sample/expected values are never labeled observed.</p></header>
<main><aside><h2>Six independent demonstrations</h2><nav aria-label="Demo navigation">{nav}</nav><p class="subtle">Generated after the Developer batch. One selected demo and one focus at a time.</p><p class="subtle"><a href="PRODUCTION_PORTAL_GUIDE.md">Full production instructions</a> · <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap" target="_blank" rel="noopener">Course GitHub</a></p><p class="subtle">Serve locally with <code>./serve.sh</code>; Ctrl+C stops it.</p></aside>
<div class="content"><div class="toolbar"><span id="location" class="status" role="status">Select a demo</span><input id="search" class="search" type="search" placeholder="Find a demo" aria-label="Filter demonstrations"><nav class="rolebar" aria-label="Production roles">"""+"".join(f'<button type="button" class="rolebtn" data-role="{r}">{r.title() if r!="cqa" else "Technical CQA"}</button>' for r in ["developer","recorder","narrator","editor","cqa"])+f"""</nav><button id="copy-command" type="button" class="rolebtn">Copy selected command</button></div>{content}<footer class="footer">Only authorized Globomantics training endpoints. The preflight proof does not by itself verify ZAP Script Console, GUI browser execution or GitHub Actions. Inspect raw records before audio freeze. All colors follow the supplied Pluralsight palette. Official ElevenLabs support differs by speech model; verify the selected voice and model before production.</footer></div></main><script>{JS}</script></body></html>"""
    path=batch/"index.html"
    path.write_text(page,encoding="utf-8")
    return path


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("batch", type=Path, help="Real Mac batch folder containing manifest.json and demo logs")
    p.add_argument("--authors", type=Path, required=True, help="Author playbook directory")
    opts=p.parse_args()
    manifest=opts.batch/"manifest.json"
    if not manifest.is_file():
        p.error("No actual manifest.json was found. Run the Mac batch preflight first")
    rows=json.loads(manifest.read_text(encoding="utf-8"))
    result=render_dashboard(opts.batch,rows,opts.authors)
    print("Local production dashboard:",result)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
