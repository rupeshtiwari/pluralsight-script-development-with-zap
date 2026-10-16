#!/usr/bin/env python3
"""Render real per-demo preflight evidence with role-specific recording instructions.

Never creates findings or PASS lines: it embeds only verified on-disk preflight
outputs. Expected-looking display samples belong to the authored runbooks, not
this evidence deliverable. No third-party dependencies.
"""
from __future__ import annotations

import html
from pathlib import Path
import re


def text_only(source: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", source)).strip()


def section_html(block: str, role: str) -> str:
    pattern = (r"<details(?:\s+open)?>\s*<summary>\s*<img\b[^>]*"
               + re.escape(role) + r"[^>]*>.*?</summary>(.*?)</details>")
    match = re.search(pattern, block, flags=re.I | re.S)
    return re.sub(r"`([^`]+)`",lambda m:"<code>"+html.escape(m.group(1))+"</code>",match.group(1).strip()) if match else (
        "<p>Proof instructions unavailable — inspect the author playbook.</p>")


def narrator_rows(block: str) -> list[tuple[str, str, str]]:
    narrator = section_html(block, "NARRATOR")
    rows = re.findall(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*"
                      r"<td>(\d+)(?:\s+spoken\s+words)?</td>\s*</tr>",
                      narrator, flags=re.I | re.S)
    return [(text_only(a), text_only(b), c) for a, b, c in rows]


def style_line(line: str) -> str:
    safe = html.escape(line.rstrip("\n"))
    if "✘ FAIL" in line or "SYNC MISMATCH" in line:
        return '<span class="stop">' + safe + "</span>"
    if "✔ PASS" in line:
        return '<span class="pass">' + safe + "</span>"
    if "★" in line:
        return '<span class="focus">' + safe + "</span>"
    return safe


def output_table(proof: str) -> str:
    """Create readable label/value rows ONLY from observed star output lines."""
    rows = []
    for line in proof.splitlines():
        match = (re.match(r"^\s*★\s*│\s*(.+?)\s*│\s*(.*)$", line)
                 or re.match(r"^\s*★\s*(.+?):\s+(.+)$", line))
        if not match:
            continue
        label, value = match.groups()
        rows.append("<tr><td><b>" + html.escape(label) +
                    "</b></td><td><code>" + html.escape(value) + "</code></td></tr>")
    if not rows:
        return "<p>No structured star fields were emitted; inspect the raw log.</p>"
    return ("<table><thead><tr><th>Actual output field</th>"
            "<th>Value captured by this preflight</th></tr></thead>"
            "<tbody>" + "".join(rows) + "</tbody></table>")


def render(demo: str, sha: str, lab: Path, destination: Path) -> Path:
    author_path = lab.parents[2] / "docs" / ".author-instructions" / (demo + ".md")
    if not author_path.is_file():
        raise FileNotFoundError("Author production playbook missing: " + str(author_path))
    parts = re.split(r"(?=^## Step [1-4]\b)", author_path.read_text(
        encoding="utf-8"), flags=re.M)
    steps = parts[1:5]
    if len(steps) != 4:
        raise ValueError("Expected four authored production steps for " + demo)
    scripts = sorted((lab / "steps").glob("0[1-4]-*.sh"))
    if len(scripts) != 4:
        raise ValueError("Expected four concept-named scripts for " + demo)
    cards = []
    for index, (step, script) in enumerate(zip(steps, scripts), start=1):
        proof_file = lab / "logs" / ("preflight-step-%02d.log" % index)
        proof = proof_file.read_text(encoding="utf-8", errors="replace")
        if "✔ PASS" not in proof or "✘ FAIL" in proof:
            raise ValueError("Step %d has no verified PASS log" % index)
        title = html.escape(step.splitlines()[0].lstrip("# ").strip())
        intro = re.search(r"### (?:Learning Goal|The small problem to solve|The specific problem)\s*\n\s*([^\n]+)",step,re.I) or re.search(r"\*\*(?:Business / operator consequence|Problem and operator consequence|Why it matters|Operator reason|Real-world problem)\s*:?\*\*\s*([^\n]+)",step,re.I)
        micro = html.escape(intro.group(1) if intro else
                            "Resolve the specific security evidence question.")
        recorder = section_html(step, "RECORDER")
        editor = section_html(step, "EDITOR")
        narration = narrator_rows(step)
        if len(narration) != 3:
            raise ValueError("Step %d missing three approved narration beats" % index)
        narration_body = "".join(
            '<tr><td>' + html.escape(shot) + '</td><td>' +
            html.escape(speech) + '</td><td>' + count + ' words</td></tr>'
            for shot, speech, count in narration
        )
        lines = "\n".join(style_line(row) for row in proof.splitlines())
        open_step = " open" if index == 1 else ""
        cards.append(
            '<details class="step"' + open_step + '><summary>Step ' + str(index)
            + ' — ' + title + '</summary><section><p><b>Micro-problem:</b> ' +
            micro + '</p><h4>Where and what to run</h4>'
            '<p>Use the integrated VS Code terminal or Mac Terminal, from this '
            'demo directory. Keep the terminal at readable zoom.</p><pre class="command">'
            './steps/' + html.escape(script.name) + '</pre>'
            '<h4>Evidence table · actual preflight values</h4>' + output_table(proof) +
            '<h4>Real output from this verified preflight</h4><pre>' + lines
            + '</pre>'
            '<details open><summary>Recorder · exact screen and holds</summary>' +
            recorder + '</details>'
            '<details><summary>Editor · highlights, arrows and cuts</summary>' +
            editor + '</details>'
            '<details><summary>Narrator · spoken words for each output reveal'
            '</summary><table><thead><tr><th>Screen</th><th>ElevenLabs'
            ' spoken line</th><th>Length</th></tr></thead><tbody>' +
            narration_body + '</tbody></table></details>'
            '<p class="gate">Record only verified values. The terminal proof '
            'comes from this SHA; separate GUI and Actions evidence remains '
            'required where applicable.</p></section></details>'
        )
    heading = html.escape(demo.upper())
    title = " · ".join([heading, "Evidence-synced production guide"])
    css = """
:root{color-scheme:light;font-family:Arial,Helvetica,sans-serif;color:#130F25}
*{box-sizing:border-box}body{max-width:1180px;margin:24px auto;padding:0 16px;
background:#EBEFF5;line-height:1.55}
header{padding:26px 30px;background:#130F25;color:white;border-radius:18px}
header h1{margin:8px 0;font-size:1.7rem}header p{margin:8px 0}
.pill{display:inline-block;border-radius:16px;background:#FF1675;color:#fff;
padding:6px 13px;margin-right:5px;font-weight:bold;font-size:0.8rem}
.pill.blue{background:#00A3FF;color:#130F25}.pill.green{background:#02E088;
color:#130F25}
.step{background:white;border:1px solid #ccd4e2;border-radius:14px;margin:16px 0;
overflow:hidden}.step>summary{background:#1B1834;color:white;padding:16px 20px;
cursor:pointer;font-weight:bold;list-style:none;font-size:1.1rem}
.step:nth-child(2)>summary{border-left:7px solid #FF1675}
.step section{padding:18px 22px}
details details{border:1px solid #ddd;border-radius:9px;margin:14px 0}
details details>summary{background:#E2E8F0;color:#130F25;cursor:pointer;
padding:10px 14px;font-weight:bold}
details details[open]>summary{border-left:6px solid #00A3FF}
details details>table,details details>p{margin:12px}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#352B6F;
color:#EBEFF5;border-radius:10px;padding:16px;font:0.94rem/1.75 Menlo,monospace}
pre.command{background:#1B1834;color:#FFC942;font-weight:bold}
.pass{color:#02E088;font-weight:bold}.stop{color:#fff;background:#B9004B;padding:0 4px;border-radius:3px;font-weight:bold}
.focus{color:#FFC942;font-weight:bold}
table{width:calc(100% - 24px);border-collapse:collapse;font-size:0.92rem}
th,td{padding:9px;border:1px solid #d4dcec;text-align:left;vertical-align:top}
th{background:#130F25;color:#fff}.gate{border-left:5px solid #FFC942;
background:#fff9e8;padding:10px}
.notice{background:#fff;border-left:6px solid #FF1675;padding:16px;margin:16px 0}
"""
    body = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>' + title + '</title><style>' + css + '</style></head><body>'
            '<header><span class="pill">RECORDER</span>'
            '<span class="pill blue">EDITOR</span>'
            '<span class="pill green">NARRATOR</span>'
            '<h1>' + title + '</h1><p>Completed branch: ' + heading +
            '-after · Commit: <code>' + html.escape(sha) +
            '</code></p><p>Four real step commands, outputs and edit beats. '
            'Illustrative architecture is separate from observed evidence.</p>'
            '</header><p class="notice"><b>Author-only production draft.</b>'
            ' This file is generated only after successful real preflight.'
            ' GUI Script Console and GitHub Actions proof must be independently'
            ' checked against the recorded take before freezing narration.</p>'
            + "".join(cards) + '</body></html>')
    output_file = destination / "production-guide.html"
    output_file.write_text(body, encoding="utf-8")
    return output_file
