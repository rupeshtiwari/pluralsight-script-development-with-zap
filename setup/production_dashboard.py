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


def step_html(root: Path, demo: str, step: int, block: str, command: str) -> str:
    first = block.splitlines()[0].replace("## Step ", "Step ").strip()
    title = first.split(" — ", 1)[-1]
    proof, raw = actual_paths(root, demo, step)
    available = proof.is_file()
    transcript = proof.read_text(encoding="utf-8", errors="replace") if available else ""
    raw_text = raw.read_text(encoding="utf-8", errors="replace") if raw.is_file() else ""
    focus = focused_labels(raw_text)
    rows = rows_from_terminal(transcript, raw_text)
    beats = beat_rows(block)
    if available and ("✔ PASS" not in transcript or "✘ FAIL" in transcript):
        # Never display a failed or incomplete capture as a verified success.
        verified = False
    else:
        verified = available
    summary = "<span class='ready'>REAL TERMINAL PROOF</span>" if verified else "<span class='hold'>HOLD — NO VERIFIED STEP PROOF</span>"
    problem = segment(block, "The small problem to solve") or segment(block, "The specific problem")
    screen = segment(block, "Where to go") or segment(block, "Which application and screen?")
    if not problem:
        m = re.search(r"### (?:The small problem to solve|The specific problem)\s*\n\s*([^\n]+)", block)
        problem = m.group(1) if m else "Review the approved playbook for the step's security question."
    if not screen:
        screen = "See the Recorder instructions for the exact application, source file and pane."
    fields = ("<table class='evidence-table'><thead><tr><th>Observed terminal field</th>"
              "<th>Exact displayed value</th></tr></thead><tbody>" + "".join(
                f"<tr><th scope='row'>{h(r['label'])}</th><td class='actual {'focus' if r['focus'] else ''}'>{h(r['value'])}</td></tr>" for r in rows
              ) + "</tbody></table>") if rows else ("<p class='hold'>No parsed result fields in this capture. "
                                                    "Read the untouched terminal transcript below.</p>")
    timeline = []
    stages = ["Before command · source and intent", "During result inspection · proof A", "After result · proof B and decision"]
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
    source_status = "Developer reference, not final narration. Confirm against the Recorder's same-take GUI or GitHub Actions evidence."
    proof_html = (f"<div class='statusline'>{summary} <span>Step {step}/4 · Source: {h(proof.name)}</span></div>"
                  f"<div class='columns'><section class='pane'><h3>Expected decision and screen</h3>"
                  f"<p><b>Why it matters</b> {h(problem)}</p><p><b>Where to work</b> {h(screen)}</p>"
                  f"<h3>Exact concept-named command</h3><pre class='command'>{h(command)}</pre>"
                  f"<p class='subtle'>Show the command, then press Enter once. These are the approved commands; "
                  f"no prerecorded security evidence is substituted.</p></section>"
                  f"<section class='pane'><h3>Actual result fields</h3>{fields}</section></div>"
                  f"<details class='transcript' open><summary>Exact terminal transcript · captured data</summary>"
                  f"<pre class='terminal'>{style_terminal(transcript, focus) if available else h('NO REAL PRE-FLIGHT LOG FOR THIS STEP')}</pre></details>"
                  f"<details class='transcript'><summary>Untouched raw audit evidence</summary>"
                  f"<pre class='terminal'>{h(raw.read_text(encoding='utf-8',errors='replace')) if raw.is_file() else h('No raw audit file captured; pending Mac preflight')}</pre></details>")
    return (f"<section class='step' data-step='{step}' id='{demo}-step-{step}'>"
            f"<div class='stephead'><span class='stepn'>STEP {step:02}</span><h2>{h(title)}</h2></div>"
            f"<div class='role-panel' data-role='narrator'><p class='notice'>{h(source_status)}</p>"
            f"<div class='columns'><div><h3>What the learner sees</h3>"
            f"<p>{h(screen)}</p><pre class='command'>{h(command)}</pre>"
            f"<h3>After the command</h3>{fields if verified else '<p class="hold">Real output not verified</p>'}</div>"
            f"<div><h3>Exact ElevenLabs wording · three spoken beats</h3>{''.join(timeline)}</div></div>"
            f"<details class='transcript'><summary>View exact captured terminal transcript</summary>"
            f"<pre class='terminal'>{style_terminal(transcript, focus) if available else h('Not captured')}</pre></details></div>"
            f"<div class='role-panel' data-role='recorder'><h3>Recorder · exact actions and holds</h3>"
            f"<p>Reference command: <code>{h(command)}</code></p>{role_source(block, 'RECORDER')}"
            f"<details class='transcript'><summary>Verified terminal output for the take comparison</summary>"
            f"<pre class='terminal'>{style_terminal(transcript, focus) if available else h('Not captured')}</pre></details></div>"
            f"<div class='role-panel' data-role='editor'><h3>Editor · callouts, focus and cut choreography</h3>"
            f"<p>Never cover a failed output with a recorded PASS from another take.</p>{role_source(block, 'EDITOR')}</div>"
            f"<div class='role-panel' data-role='developer'><h3>Developer · executable contract and current proof</h3>"
            f"{proof_html}</div>"
            f"<div class='role-panel' data-role='cqa'><h3>Technical CQA · approve only observable proof</h3>"
            f"<p><b>Security question:</b> {h(problem)}</p><p><b>Command:</b> <code>{h(command)}</code></p>"
            f"<p><b>Current proof status:</b> {'Terminal PASS observed; external GUI/CI unverified' if verified else 'HOLD — missing or failed preflight output'}</p>"
            f"<p>Require the actual application or ZAP result, source SHA and take ID. A terminal check is not evidence that a GUI pane or hosted runner displayed a result.</p>"
            f"<details class='transcript'><summary>Review untouched proof</summary><pre class='terminal'>{style_terminal(transcript, focus) if available else h('Not captured')}</pre></details>"
            f"</div></section>")


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
        # Backward-compatible fallback: read only actual generated step headings.
        step_file = root / demo / "steps-and-output.md"
        if step_file.is_file():
            commands = re.findall(r"^## Step [1-4] — (\./steps/[a-z0-9-]+\.sh)$", step_file.read_text(encoding="utf-8"), flags=re.M)
    steps = ''.join(step_html(root, demo, n, block, commands[n-1] if len(commands)>=n else "Not available — check batch manifest") for n, block in enumerate(blocks, 1))
    manifest = h(json.dumps(row, indent=2, ensure_ascii=False))
    reports = report_paths(root, demo)
    report_links = "".join(f'<li><a href="{h(demo + "/" + str(p.relative_to(root / demo)))}" target="_blank" rel="noopener">{h(p.relative_to(root / demo))}</a></li>' for p in reports)
    report_section = (f"<details><summary>Generated raw JSON evidence ({len(reports)})</summary><ul>{report_links}</ul></details>" if reports else "<p class='subtle'>No standalone JSON file captured in the deliverables. Raw logs remain available.</p>")
    return (f"<article class='demo' data-demo='{h(demo)}'><div class='demo-heading'>"
            f"<div><span class='eyebrow'>{h(demo.upper())} · APPROVED COURSE DEMO</span>"
            f"<h1>{h(label)}</h1><p>{h(proof)}</p></div><div class='sha'>SOURCE SHA<br><code>{h(row.get('sha') or 'NOT CAPTURED')}</code></div></div>"
            f"<div class='role-panel' data-role='developer'><div class='pill-row'>"
            f"<span class='pill'>Startup exit: {h(row.get('startup_exit'))}</span>"
            f"<span class='pill'>Preflight exit: {h(row.get('preflight_exit'))}</span>"
            f"<span class='pill'>Cleanup exit: {h(row.get('cleanup_exit'))}</span></div>"
            "<p>Batch evidence: " + " · ".join(
                f"<a href='{h(demo + '/' + name)}'>{h(label)}</a>"
                for name,label in (("steps-and-output.md","captured steps and output"),("production-guide.html","per-demo production HTML"),("narration-draft.md","narration draft"),("manifest.json","manifest"))
                if (root/demo/name).is_file()
            ) + ". Files not produced by the actual Mac run are never linked as completed.</p>"
            f"{report_section}<details><summary>Full SHA and process results</summary><pre>{manifest}</pre></details></div>"
            f"<div class='role-panel' data-role='cqa'><p class='notice'>Required release evidence: one fresh authorized app execution, actual ZAP GUI or hosted CI proof where applicable, per-step output/alert reconciliation, exact process exit, source SHA and take ID. Structural CI is separate.</p></div>"
            f"<nav class='step-nav' aria-label='Steps for {h(label)}'>" + ''.join(
                f"<button class='stepbtn' data-target-step='{i}' type='button'>Step {i}</button>" for i in range(1,5)) + "</nav>"
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
"""
JS = r"""
(() => {
  const demos = [...document.querySelectorAll('.demo')];
  const navs = [...document.querySelectorAll('.navdemo')];
  const roles = [...document.querySelectorAll('.rolebtn')];
  let currentDemo = demos[0]?.dataset.demo || '';
  let currentRole = 'narrator';
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
  document.querySelector('#copy-command').addEventListener('click',async()=>{
    const value=document.querySelector('.demo.active .step.active pre.command')?.textContent;
    if(!value||value.includes('Not available'))return;
    try{await navigator.clipboard.writeText(value.trim());document.querySelector('#copy-command').textContent='Copied'}
    catch {document.querySelector('#copy-command').textContent='Select the command to copy'}
  });
})();
"""


def render_dashboard(batch: Path, rows: list[dict], author_dir: Path) -> Path:
    """Create index.html only from captured per-demo batch outputs and author files."""
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
<body><header><span class="eyebrow">PLURALSIGHT · DEVELOPER → RECORDER → EDITOR → NARRATOR → TECHNICAL CQA</span><h1>Script Development with ZAP · Production Cockpit</h1><p>{h(header)} This page is generated locally from actual completed-branch preflight outputs. Sample/expected values are never labeled observed.</p></header>
<main><aside><h2>Six independent demonstrations</h2><nav aria-label="Demo navigation">{nav}</nav><p class="subtle">Generated after the Developer batch. One selected demo and one focus at a time.</p><p class="subtle">Serve locally using <code>./serve.sh</code> from this batch folder. Stop with Ctrl+C.</p></aside>
<div class="content"><div class="toolbar"><span id="location" class="status" role="status">Select a demo</span><input id="search" class="search" type="search" placeholder="Find a demo" aria-label="Filter demonstrations"><nav class="rolebar" aria-label="Production roles">"""+"".join(f'<button type="button" class="rolebtn" data-role="{r}">{r.title() if r!="cqa" else "Technical CQA"}</button>' for r in ["developer","recorder","editor","narrator","cqa"])+f"""</nav><button id="copy-command" type="button" class="rolebtn">Copy selected command</button></div>{content}<footer class="footer">Only authorized Globomantics training endpoints. The preflight proof does not by itself verify ZAP Script Console, GUI browser execution or GitHub Actions. Inspect raw records before audio freeze. All colors follow the supplied Pluralsight palette.</footer></div></main><script>{JS}</script></body></html>"""
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
