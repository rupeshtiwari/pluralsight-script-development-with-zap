# M1-DEMO2 · JavaScript HTTP Sender — Author Production Playbook

<div align="center">

![Recorder](https://img.shields.io/badge/Recorder-Exact_Screen-0284c7?style=for-the-badge)
![Narrator](https://img.shields.io/badge/Narrator-Verified_Script-9333ea?style=for-the-badge)
![Editor](https://img.shields.io/badge/Editor-Timed_Highlights-16a34a?style=for-the-badge)

<img src="../learner-diagrams/m1-demo2-architecture.svg" alt="Illustrative JavaScript HTTP Sender workflow" width="100%"/>

<sub>Generated using ChatGPT · Temporary PUBLIC author guidance</sub>

</div>

[← **All Six Production Playbooks**](README.md) · [**Student Starter README ↗**](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo2-before/demos/module1-demos/m1-demo2-javascript-http-sender/README.md) · [**Completed README ↗**](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo2-after/demos/module1-demos/m1-demo2-javascript-http-sender/README.md)

## Recording Assignment

<table>
<tr><th>Field</th><th>Exact Value</th></tr>
<tr><td>Demonstration</td><td><b>JavaScript HTTP Sender</b> · m1-demo2</td></tr>
<tr><td>Approved Objectives</td><td>EO2a — check the complete wording in the linked learner README</td></tr>
<tr><td>Reference branch</td><td><code>m1-demo2-after</code> — completed source for preflight</td></tr>
<tr><td>Recording branch</td><td><code>m1-demo2-before</code> — follow the student workflow</td></tr>
<tr><td>Demo directory</td><td><code>demos/module1-demos/m1-demo2-javascript-http-sender</code></td></tr>
<tr><td>Student exercise state</td><td>The starter intentionally lacks globomantics-marker.js; author it before the recording checks</td></tr>
</table>

## Start Here — One Clone, Two Branches, One Demo

**Do not clone this repository separately for every demo.** Each recorder clones the course once, then switches to the specific demo's `after` branch for preflight and `before` branch for recording. Before switching, stop the old demo environment and preserve the narration references.

<details open>
<summary><b><font color="#0284c7">A · Clone Once and Prepare the Mac</font></b></summary>

Use this step only for your first assigned demo. For second and third demos, keep the same repository folder and skip the clone/setup if already complete.

```bash
cd ~
git clone https://github.com/rupeshtiwari/pluralsight-script-development-with-zap.git
cd pluralsight-script-development-with-zap
./setup/setup-macos.sh
git fetch origin
```

**Where is the folder?** It is `~/pluralsight-script-development-with-zap` by default. `git switch` does not create a second or third folder; it changes the checked-out branch in the same directory.

</details>

<details open>
<summary><b><font color="#9333ea">B · Run Preflight From the Completed Branch FIRST</font></b></summary>

This is the **narration evidence source**. It executes all four real named commands, saves raw live proof, and produces stable per-step reference logs so the Narrator can start while footage is still being recorded.

```bash
cd ~/pluralsight-script-development-with-zap
git status --short
git fetch origin
git switch m1-demo2-after
git rev-parse HEAD
cd demos/module1-demos/m1-demo2-javascript-http-sender
./scripts/demo_up.sh
./scripts/preflight_check.sh
ls -l logs/preflight-step-0[1-4].log
```

**Only proceed when preflight exits 0 and prints the actual summary below** (this is the expected format, not a fabricated test run):

```text
RESULT: 5 checks passed, 0 failed
REFERENCE: logs/preflight-step-01.log through logs/preflight-step-04.log
```

**Proof stays real:** `logs/preflight-step-01.log` through `04.log` are the Narrator's four outputs. `logs/.producer/` holds untouched raw details. Separate ZAP GUI / GitHub Actions evidence must be checked independently when a terminal command cannot observe it.

**Optional but strongly recommended repeatability check:** after successful preflight, set `DEMO_SYNC_MODE=1` and `DEMO_SYNC_PHASE=compare` off-camera, then execute the same four named steps while still on this completed reference. Each must match its baseline; a material mismatch blocks recording.

**Archive the references and stop the stack before switching:**

```bash
mkdir -p ~/zap-production-evidence/m1-demo2
cp logs/preflight-step-0[1-4].log ~/zap-production-evidence/m1-demo2/
./scripts/demo_down.sh
cd ~/pluralsight-script-development-with-zap
git status --short
```

Never delete the reference logs with a destructive Git cleanup.

</details>

<details open>
<summary><b><font color="#0284c7">C · Switch to the Student Starting Branch and Record</font></b></summary>

```bash
cd ~/pluralsight-script-development-with-zap
git switch m1-demo2-before
git rev-parse HEAD
cd demos/module1-demos/m1-demo2-javascript-http-sender
cp ~/zap-production-evidence/m1-demo2/preflight-step-0[1-4].log logs/
./scripts/demo_up.sh

# Off-camera recording parity settings
export DEMO_SYNC_MODE=1
export DEMO_SYNC_PHASE=compare
```

**The starter intentionally lacks globomantics-marker.js; author it before the recording checks.** Follow the [student README on this exact starter branch](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo2-before/demos/module1-demos/m1-demo2-javascript-http-sender/README.md) to complete any required source writing, then record the four exact commands listed below. The starter branch may be intentionally incomplete and **must not** be expected to pass its final checks before the work has been done.

After the four named commands, capture the GUI/CI proof, then:

```bash
./scripts/demo_down.sh
cd ~/pluralsight-script-development-with-zap
git status --short
```

**If Git refuses the next branch switch:** preserve the changed code on a task branch or in a deliberate backup before switching. Do not use force/reset to discard recorded work.

</details>

<details><summary><b><font color="#16a34a">D · Recording More Demos From This Same Clone</font></b></summary>

```bash
cd ~/pluralsight-script-development-with-zap
git status --short
git fetch origin
# Example: select another assigned demo (replace as needed):
git switch m1-demo3-after
```

For a different demo, replace the branch and folder with the corresponding entry on the [six-demo author dashboard](README.md). Repeat preflight → archive logs → cleanup → branch switch → record. One local repository is sufficient for sequential recordings. A separate worktree is optional when you need two branches open concurrently.

</details>

## Camera, Narration and Edit Contract

<table>
<tr><td width="18%"><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/></td><td>Record full-screen at readable zoom. Open the source/GUI pane specified in the relevant step, then hold the complete named command ~8 seconds before Enter. Hold each actual output focus 6–8 seconds. On significant UI clicks provide 8-second pre-click and post-click handles in raw footage for the editor.</td></tr>
<tr><td><img src="https://img.shields.io/badge/NARRATOR-Purple-9333ea"/></td><td>Use the real `preflight-step-0N.log` plus the corresponding filmed GUI/CI evidence. The step tables below give exact ElevenLabs lines with word counts, one mechanism and one operator consequence per reveal. Do not narrate sample placeholders.</td></tr>
<tr><td><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/></td><td>Cut cleanly at source/terminal/GUI transitions and scanning waits. Highlight one field using a small square, arrow or callout; remove it immediately as the focus changes. Match voice to the same take, not a historic preflight value from a different implementation.</td></tr>
</table>

## Four Fixed Teaching Steps — Follow In Order

## Step 1 — Load And Enable The HTTP Sender Script

**Why it matters:** A JavaScript file cannot modify traffic until it is registered with ZAP.

**Exact on-screen command**, executed in `demos/module1-demos/m1-demo2-javascript-http-sender`:

```bash
./steps/01-load-javascript-http-sender.sh
```

**Expected output format from the real step engine (ILLUSTRATIVE; replace with the current preflight log):**

```text
Script name: globomantics-marker (type: HTTP Sender · engine: <detected JavaScript engine>)
Marker header it adds: X-Globomantics-Marker: GLOBO-DEMO
Named console line it prints: [globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to <url>
✔ PASS script is a valid HTTP Sender action and loaded into ZAP
```

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Exact_Shots-0284c7"/></summary>
<table>
<tr><th>Relative shot / duration</th><th>Prescriptive actions</th></tr>
<tr><td>Before terminal · 8 seconds</td><td>VS Code / ZAP script editor: show zap-scripts/globomantics-marker.js, `MARKER_HEADER`, `MARKER_VALUE`, `sendingRequest()`, and `setHeader()`. In starter worktree author the JavaScript source first.</td></tr>
<tr><td>Command · 8 seconds</td><td>Run <code>./steps/01-load-javascript-http-sender.sh</code> once. Keep full filename readable, cursor clear, and no visible typo or backspace.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Highlight the script name and HTTP Sender type only.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Move the callout to X-Globomantics-Marker and GLOBO-DEMO, then the PASS line.</td></tr>
<tr><td>Exit / decision · 6–8 seconds</td><td>Show the actual PASS and any GUI proof. For a ZAP click, stage a pointer on its target 8 seconds before click, hold result 8 seconds after, then cut extra dead air.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Load the JavaScript HTTP Sender script. Its sending request hook can change a message only after ZAP registers and enables it.</td><td>21</td></tr>
<tr><td>First actual output</td><td>The marker header has a fixed name and value. These parameters identify precisely what the hook will attach to traffic.</td><td>20</td></tr>
<tr><td>Second output / decision</td><td>The successful registration proves ZAP accepted the script. It does not yet prove an outbound request carried the header.</td><td>19</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Square `sendingRequest()` and `setHeader()`, then arrow to the marker-header value in the terminal. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-01.log</code> and <code>logs/recorded-step-01.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

**Source-review confidence 95%**, before live rehearsal. An estimate below the owner's release threshold cannot be increased without a matching real proof and reviewer approval.

---

## Step 2 — Prove A Marker On An Outbound Request

**Why it matters:** A successfully loaded script is not evidence that it ran against actual traffic.

**Exact on-screen command**, executed in `demos/module1-demos/m1-demo2-javascript-http-sender`:

```bash
./steps/02-prove-outbound-marker-header.sh
```

**Expected output format from the real step engine (ILLUSTRATIVE; replace with the current preflight log):**

```text
Outbound request: GET http://app:8000/greet?name=marker-<live-request-id> HTTP/1.1
Header added by the script: X-Globomantics-Marker: GLOBO-DEMO
✔ PASS the script added X-Globomantics-Marker to the outbound request
```

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Exact_Shots-0284c7"/></summary>
<table>
<tr><th>Relative shot / duration</th><th>Prescriptive actions</th></tr>
<tr><td>Before terminal · 8 seconds</td><td>ZAP GUI http://localhost:8080/zap/ → History → latest /greet?name=marker-... → Request; keep Terminal in demo folder. Scroll the Request pane just enough to show the header.</td></tr>
<tr><td>Command · 8 seconds</td><td>Run <code>./steps/02-prove-outbound-marker-header.sh</code> once. Keep full filename readable, cursor clear, and no visible typo or backspace.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Box the new request line and visually match the request ID to the current terminal proof.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Arrow to `X-Globomantics-Marker: GLOBO-DEMO` in ZAP Request; cut to PASS.</td></tr>
<tr><td>Exit / decision · 6–8 seconds</td><td>Show the actual PASS and any GUI proof. For a ZAP click, stage a pointer on its target 8 seconds before click, hold result 8 seconds after, then cut extra dead air.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Send a fresh request through ZAP instead of directly to the store. The HTTP Sender hook runs only on proxied messages.</td><td>21</td></tr>
<tr><td>First actual output</td><td>The captured request contains the marker header and its fixed value. That is proof of an actual outbound modification.</td><td>19</td></tr>
<tr><td>Second output / decision</td><td>The request identifier changes on every execution, but the script's header and the technical result must remain consistent.</td><td>18</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Separate rectangles on request URL and header. Never highlight an earlier History entry. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-02.log</code> and <code>logs/recorded-step-02.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

**Source-review confidence 96%**, before live rehearsal. An estimate below the owner's release threshold cannot be increased without a matching real proof and reviewer approval.

---

## Step 3 — Verify The Live Script Console Line

**Why it matters:** A terminal helper can print the expected format without observing JavaScript's actual console output.

**Exact on-screen command**, executed in `demos/module1-demos/m1-demo2-javascript-http-sender`:

```bash
./steps/03-check-live-script-console.sh
```

**Expected output format from the real step engine (ILLUSTRATIVE; replace with the current preflight log):**

```text
Expected format (verify live ZAP Script Console): [globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to <url>
✔ PASS fresh marked request confirmed; verify emitted line in live ZAP Script Console
[GUI-ONLY PROOF] [globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to http://app:8000/greet?name=marker-<live-request-id>
```

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Exact_Shots-0284c7"/></summary>
<table>
<tr><th>Relative shot / duration</th><th>Prescriptive actions</th></tr>
<tr><td>Before terminal · 8 seconds</td><td>Before command: ZAP GUI → Scripts → globomantics-marker → Script Console output. Clear or note prior entries, execute command in terminal, then return to the fresh console line.</td></tr>
<tr><td>Command · 8 seconds</td><td>Run <code>./steps/03-check-live-script-console.sh</code> once. Keep full filename readable, cursor clear, and no visible typo or backspace.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Highlight the terminal field labeled Expected format without treating it as observed console output.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Show the actual fresh `[globo-marker]` line in the ZAP Script Console and highlight the matching request URL.</td></tr>
<tr><td>Exit / decision · 6–8 seconds</td><td>Show the actual PASS and any GUI proof. For a ZAP click, stage a pointer on its target 8 seconds before click, hold result 8 seconds after, then cut extra dead air.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Trigger a new request to make the JavaScript print its marker. The terminal displays the expected format, not the console itself.</td><td>21</td></tr>
<tr><td>First actual output</td><td>Open the live Script Console and find the fresh marker line. Match its URL to the request sent through ZAP.</td><td>20</td></tr>
<tr><td>Second output / decision</td><td>The console proves the script reported a real action. A copied expected line would not establish that behavior.</td><td>18</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Use a short arrow from expected-format label to the real Script Console pane, then a rectangle on the live marker line. Do not simulate output. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-03.log</code> and <code>logs/recorded-step-03.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

**Source-review confidence 86%**, before live rehearsal. An estimate below the owner's release threshold cannot be increased without a matching real proof and reviewer approval.

---

## Step 4 — Confirm Reusable Script Registration

**Why it matters:** The team needs a reliably named, enabled HTTP Sender registration for later automation.

**Exact on-screen command**, executed in `demos/module1-demos/m1-demo2-javascript-http-sender`:

```bash
./steps/04-verify-enabled-script-registration.sh
```

**Expected output format from the real step engine (ILLUSTRATIVE; replace with the current preflight log):**

```text
Registered name: globomantics-marker
Type: httpsender
Engine: <detected engine>
Enabled: true
Path (repo): zap-scripts/globomantics-marker.js
✔ PASS script registered and enabled as HTTP Sender
```

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Exact_Shots-0284c7"/></summary>
<table>
<tr><th>Relative shot / duration</th><th>Prescriptive actions</th></tr>
<tr><td>Before terminal · 8 seconds</td><td>ZAP GUI → Scripts → HTTP Sender → globomantics-marker. Open selected script properties, and terminal result; scroll to enabled state.</td></tr>
<tr><td>Command · 8 seconds</td><td>Run <code>./steps/04-verify-enabled-script-registration.sh</code> once. Keep full filename readable, cursor clear, and no visible typo or backspace.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Box registered name `globomantics-marker` and type `httpsender`.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Arrow to `Enabled: true` and show the source path, then PASS.</td></tr>
<tr><td>Exit / decision · 6–8 seconds</td><td>Show the actual PASS and any GUI proof. For a ZAP click, stage a pointer on its target 8 seconds before click, hold result 8 seconds after, then cut extra dead air.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>A reusable automation needs a stable script identity, not just one marked request. Inspect its registration before depending on it.</td><td>20</td></tr>
<tr><td>First actual output</td><td>The type identifies the HTTP Sender hook, and the enabled flag confirms ZAP can use that registered script.</td><td>18</td></tr>
<tr><td>Second output / decision</td><td>The source path provides a stable reference for automation. It does not promise persistence after the container is destroyed.</td><td>19</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Sequential boxes on name, type and enabled, not all fields simultaneously. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-04.log</code> and <code>logs/recorded-step-04.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

**Source-review confidence 95%**, before live rehearsal. An estimate below the owner's release threshold cannot be increased without a matching real proof and reviewer approval.

---

## Delivery Gate

Deliver both branch refs and SHA, full preflight plus step logs, normalized parity result, untouched raw proof, GUI screenshots with timestamps, exact ElevenLabs script or audio, and Editor timeline. Record each live step from the authorized training target only. Never call an old scan or estimated screenshot actual evidence.
