# Author production hub — Script Development with ZAP

<div align="center">

![Developer](https://img.shields.io/badge/01-Developer-130F25?style=for-the-badge)
![Recorder](https://img.shields.io/badge/02-Recorder-00A3FF?style=for-the-badge)
![Editor](https://img.shields.io/badge/03-Editor-02E088?style=for-the-badge)
![Narrator](https://img.shields.io/badge/04-Narrator-770EF7?style=for-the-badge)

**One batch preflight · Six demo deliverables · One recording checkout per engineer**

</div>

This directory is a **temporary, PUBLIC author-production workspace** inside the public GitHub repository. Move it to private storage before Pluralsight learner release; a dot-prefixed name and later deletion do not protect past commits.

## 1. Developer — prepare GitHub and generate all evidence

The Developer prepares the repo, verifies its branches and prerequisites, then runs **one command** that validates all six completed references. Recorder, Editor and Narrator do not repeat Mac installation or production preflight per demo.

<table>
<tr><th>Developer responsibility</th><th>Required result</th></tr>
<tr><td><b>Repository</b></td><td>Student root README with problems, complete grouped learning objectives, accurate architecture and the <b>Watch the Pluralsight course</b> link placeholder</td></tr>
<tr><td><b>Branches</b></td><td><code>main</code> starter plus six independent <code>-before</code>/<code>-after</code> pairs; all pairs up to date, with no completed source leaked into starters</td></tr>
<tr><td><b>Runtime</b></td><td>Reusable macOS prerequisite setup in <code>setup/</code>, individual demo startup/teardown scripts, stable concept-named step scripts</td></tr>
<tr><td><b>Production package</b></td><td>One real batch validation and local deliverables directory containing six demo folders, each with actual logs, exact step commands/output, a readable HTML production guide and narration draft</td></tr>
<tr><td><b>Proof</b></td><td>Verified process status and SHA; missing GUI or hosted evidence must remain pending, not fabricated</td></tr>
</table>

<details>
<summary><b>One-time setup — expand only on a new Mac</b></summary>

**Where:** macOS Terminal, one initial clone of this course.

```bash
cd ~
git clone https://github.com/rupeshtiwari/pluralsight-script-development-with-zap.git
cd pluralsight-script-development-with-zap
./setup/setup-macos.sh
```

This creates `~/pluralsight-script-development-with-zap` once. Running `git switch` changes the current branch inside this **same folder**. On later demos do not clone the repository again.

</details>

<details open>
<summary><b>Developer's single batch command — execute once to generate all deliverables</b></summary>

**Where:** macOS Terminal at the **course repository root**.

```bash
cd ~/pluralsight-script-development-with-zap
./setup/run-all-demo-preflights.sh
```

The script checks dependencies, fetches the completed branches, creates and removes temporary worktrees, starts each isolated demo **sequentially**, executes its four real named steps and saves actual output. It cleans up one demo before starting another; the Developer's current branch is not changed.

**Expected generated folder** (only after a real Mac run):

```text
~/zap-course-deliverables/batch-YYYYMMDD-HHMMSS/
  README.md
  manifest.json
  m1-demo1/
    steps-and-output.md       Exact 4 commands and actual terminal output
    logs/                     Raw audit logs + normalized per-step transcripts
    production-guide.html     Real step output + Recorder/Editor/Narrator cards
    narration-draft.md        Initial spoken lines, not yet frozen
    manifest.json             Real SHA, exit codes and status
  m1-demo2/                   Same structure when validation passed
  m1-demo3/
  m2-demo1/
  m2-demo2/
  m2-demo3/
```

A failed demo retains diagnostic logs and its failure status; it does **not** receive a falsely successful guide or narration. The script also creates a ZIP beside the folder so the Narrator can upload it for evidence-grounded finalization.

**Locally served production cockpit.** After the recording Mac actually generates the batch output, open its timestamped folder and run `./serve.sh`. It opens `http://127.0.0.1:8765/index.html` using a local-only HTTP server. Alternatively run `./setup/serve-production-deliverables.sh ~/zap-course-deliverables/batch-YYYYMMDD-HHMMSS` from the course repo (substitute the real timestamp). The navigable dashboard covers all six demos with Developer, Recorder, Editor, Narrator and Technical CQA views. Each step shows the exact named command, field/value table built from the real terminal transcript, the captured unmodified raw log, and spoken words mapped to the current screen. Missing or failed evidence stays on HOLD. Stop the server with Ctrl+C. No dependencies beyond Python 3 and the Mac's default browser.

**The recording team receives the deliverables package plus the current source SHAs before filming.** The individual demo playbooks below do not rerun preflight.

</details>

### GitHub About, Topics, Releases and Packages — developer checklist

These are the actual values to enter using the repository **About → gear icon** when the connected GitHub integration cannot update settings.

<table>
<tr><th>GitHub field</th><th>Exact text or action</th></tr>
<tr><td><b>About description</b></td><td><code>Hands-on OWASP ZAP labs for injection, XSS, CSRF, custom scripting, authenticated scans, API reporting, and security quality gates.</code></td></tr>
<tr><td><b>Topics</b></td><td><code>owasp-zap</code>, <code>appsec</code>, <code>devsecops</code>, <code>security-testing</code>, <code>github-actions</code>, <code>fastapi</code>, <code>python</code>, <code>javascript</code>, <code>docker-compose</code>, <code>pluralsight</code></td></tr>
<tr><td><b>Website</b></td><td>Enter the verified **direct Pluralsight course URL after publication**; replace the placeholder in the student README at the same time. Never invent it</td></tr>
<tr><td><b>Releases</b></td><td>Publish a versioned release with genuine learner artifacts only after final recording and runtime CQA approval. Do not create a dummy release</td></tr>
<tr><td><b>Packages</b></td><td>Leave empty. This project consumes a pinned upstream ZAP image and does not publish its own installable package</td></tr>
</table>

These metadata values are **prepared for manual entry**, not claims they have been applied. The reusable skill must apply them automatically in future only when authenticated GitHub administrative actions are available.

## 2. Recorder — choose your Module and Demo

**Follow the exact before-branch demonstration**, using one existing repository checkout per engineer. Before recording, receive the Developer's corresponding real step logs; complete any missing student-authored scripts or plans in your own working copy. Run only the demo startup and four named commands, showing the exact values called for by your playbook.

<table><thead><tr><th>Module / Demo</th><th>Security story</th><th>Recorder instructions</th><th>Student steps</th><th>Completed reference</th></tr></thead>
<tbody><tr><td><b>Module 1 · Demo 1</b></td><td>Injection, XSS and CSRF</td><td><a href="m1-demo1.md">Recorder, Editor and Narrator guide</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo1-before/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf/README.md">Student exercise</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo1-after/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf/README.md">Completed reference</a></td></tr>
<tr><td><b>Module 1 · Demo 2</b></td><td>JavaScript HTTP Sender</td><td><a href="m1-demo2.md">Recorder, Editor and Narrator guide</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo2-before/demos/module1-demos/m1-demo2-javascript-http-sender/README.md">Student exercise</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo2-after/demos/module1-demos/m1-demo2-javascript-http-sender/README.md">Completed reference</a></td></tr>
<tr><td><b>Module 1 · Demo 3</b></td><td>Python scanning and authentication</td><td><a href="m1-demo3.md">Recorder, Editor and Narrator guide</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo3-before/demos/module1-demos/m1-demo3-python-scanning-authentication/README.md">Student exercise</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo3-after/demos/module1-demos/m1-demo3-python-scanning-authentication/README.md">Completed reference</a></td></tr>
<tr><td><b>Module 2 · Demo 1</b></td><td>Authenticated CI scanning</td><td><a href="m2-demo1.md">Recorder, Editor and Narrator guide</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo1-before/demos/module2-demos/m2-demo1-authenticated-zap-github-actions/README.md">Student exercise</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo1-after/demos/module2-demos/m2-demo1-authenticated-zap-github-actions/README.md">Completed reference</a></td></tr>
<tr><td><b>Module 2 · Demo 2</b></td><td>ZAP API and Insights</td><td><a href="m2-demo2.md">Recorder, Editor and Narrator guide</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo2-before/demos/module2-demos/m2-demo2-zap-api-scan-evidence/README.md">Student exercise</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo2-after/demos/module2-demos/m2-demo2-zap-api-scan-evidence/README.md">Completed reference</a></td></tr>
<tr><td><b>Module 2 · Demo 3</b></td><td>Security quality gate</td><td><a href="m2-demo3.md">Recorder, Editor and Narrator guide</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo3-before/demos/module2-demos/m2-demo3-security-quality-gates/README.md">Student exercise</a></td><td><a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo3-after/demos/module2-demos/m2-demo3-security-quality-gates/README.md">Completed reference</a></td></tr></tbody></table>

The first step in each production guide is expanded. Other steps are collapsed so you can focus. Within an expanded step, the **Recorder** panel is open and the **Editor** and **Narrator** panels are collapsed.

## 3. Editor — synchronize real footage and highlights

Use `production-guide.html` in each generated deliverables folder for the current step's real terminal output and role cards. Start with the Recorder's footage, then add one square or arrow to the stated source parameter, request field, alert ID, HTTP status, report value or exit code at a time. Cut during pane changes and long scans, remove the old callout as soon as the highlighted region changes, and preserve the visible proof for 6–8 seconds per focus. Retain the important mouse-click handles in raw footage and trim them in the final delivery.

[Editor timing and callout standards](01_PERSONA_PROTOCOLS.md) · [Output synchronization contract](02_LOG_SYNC_CONTRACT.md)

## 4. Narrator — use actual logs and narration draft

Open the same demo folder in the generated deliverables: `steps-and-output.md`, `logs/preflight-step-0N.log`, raw `logs/.producer/`, and `narration-draft.md`. Those are the **real outputs from the Developer's preflight** and the approved starter spoken lines, not a substitute for the Recorder's footage.

Read the Developer's `production-guide.html` and compare with the Recorder's actual take. Use natural ElevenLabs speech about the exact command, its parameters, the relevant output, and the operator decision. Each step teaches a distinct mechanism aligned with its objective. Do not narrate an estimated counter, fake GUI Script Console line, or an older Actions report.

Once the recording and actual GUI/CI evidence are shared, upload the generated ZIP with that proof to ChatGPT for final per-step narration, word count, LO coverage and video/audio synchronization. Never label a draft as final before those checks.

## 5. Technical CQA and release

[Technical proof findings](03_CQA_FINDINGS.md) · [Recording checklist](04_RELEASE_CHECKLIST.md) · [All six step-level playbooks](README.md)

The owner's minimum content-confidence threshold is **95%**. Documentation alone cannot establish it, and an unverified runtime or GUI claim remains on HOLD regardless of a source-review estimate. Do not inflate confidence by rewriting narration. Preserve the branch and run SHA and all evidence.

**Only student GitHub assets, approved slides, and edited video are Pluralsight deliverables.** This temporary author hub must be removed from the learner repo before publishing, with a private copy retained.
