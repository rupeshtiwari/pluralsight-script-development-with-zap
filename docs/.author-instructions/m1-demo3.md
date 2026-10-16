# M1-DEMO3 · Python Scanning and Authentication — Author Production Playbook

<div align="center">

![Recorder](https://img.shields.io/badge/Recorder-Exact_Screen-0284c7?style=for-the-badge)
![Narrator](https://img.shields.io/badge/Narrator-Verified_Script-9333ea?style=for-the-badge)
![Editor](https://img.shields.io/badge/Editor-Timed_Highlights-16a34a?style=for-the-badge)

<img src="../learner-diagrams/m1-demo3-architecture.svg" alt="Illustrative Python Scanning and Authentication workflow" width="100%"/>

<sub>Generated using ChatGPT · Temporary PUBLIC author guidance</sub>

</div>

[← **All Six Production Playbooks**](README.md) · [**Student Starter README ↗**](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo3-before/demos/module1-demos/m1-demo3-python-scanning-authentication/README.md) · [**Completed README ↗**](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo3-after/demos/module1-demos/m1-demo3-python-scanning-authentication/README.md)

## Recording Assignment

<table>
<tr><th>Field</th><th>Exact Value</th></tr>
<tr><td>Demonstration</td><td><b>Python Scanning and Authentication</b> · m1-demo3</td></tr>
<tr><td>Approved Objectives</td><td>EO2b · EO2c — check the complete wording in the linked learner README</td></tr>
<tr><td>Reference branch</td><td><code>m1-demo3-after</code> — completed source for preflight</td></tr>
<tr><td>Recording branch</td><td><code>m1-demo3-before</code> — follow the student workflow</td></tr>
<tr><td>Demo directory</td><td><code>demos/module1-demos/m1-demo3-python-scanning-authentication</code></td></tr>
<tr><td>Student exercise state</td><td>The starter intentionally lacks the completed Jython active rule and authentication scripts</td></tr>
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
git switch m1-demo3-after
git rev-parse HEAD
cd demos/module1-demos/m1-demo3-python-scanning-authentication
./scripts/demo_reset.sh
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
mkdir -p ~/zap-production-evidence/m1-demo3
cp logs/preflight-step-0[1-4].log ~/zap-production-evidence/m1-demo3/
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
git switch m1-demo3-before
git rev-parse HEAD
cd demos/module1-demos/m1-demo3-python-scanning-authentication
cp ~/zap-production-evidence/m1-demo3/preflight-step-0[1-4].log logs/
./scripts/demo_reset.sh

# Off-camera recording parity settings
export DEMO_SYNC_MODE=1
export DEMO_SYNC_PHASE=compare
```

**The starter intentionally lacks the completed Jython active rule and authentication scripts.** Follow the [student README on this exact starter branch](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo3-before/demos/module1-demos/m1-demo3-python-scanning-authentication/README.md) to complete any required source writing, then record the four exact commands listed below. The starter branch may be intentionally incomplete and **must not** be expected to pass its final checks before the work has been done.

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
git switch m2-demo1-after
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

## Step 1 — Load A Jython Active Scan Rule

**Why it matters:** Built-in scanning does not demonstrate application-specific reflection checks.

**Exact on-screen command**, executed in `demos/module1-demos/m1-demo3-python-scanning-authentication`:

```bash
./steps/01-load-python-active-scan-rule.sh
```

**Expected output format from the real step engine (ILLUSTRATIVE; replace with the current preflight log):**

```text
Script name: globomantics-active-rule (type: active · engine: <Jython engine>)
Alert it raises: Globomantics unsafe reflection (custom rule)
✔ PASS active-rule script is valid and loaded into ZAP as an active rule
```

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Exact_Shots-0284c7"/></summary>
<table>
<tr><th>Relative shot / duration</th><th>Prescriptive actions</th></tr>
<tr><td>Before terminal · 8 seconds</td><td>VS Code: zap-scripts/globomantics-active-rule.py. Hold on `_probe_request()`, `_check()`, `sas.newAlert()`, then ZAP GUI → Scripts → Active Rules.</td></tr>
<tr><td>Command · 8 seconds</td><td>Run <code>./steps/01-load-python-active-scan-rule.sh</code> once. Keep full filename readable, cursor clear, and no visible typo or backspace.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Highlight `globomantics-active-rule` and script type active.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Box exact custom alert name, then the PASS confirmation.</td></tr>
<tr><td>Exit / decision · 6–8 seconds</td><td>Show the actual PASS and any GUI proof. For a ZAP click, stage a pointer on its target 8 seconds before click, hold result 8 seconds after, then cut extra dead air.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Load a Jython active rule for the profile's note parameter. The rule clones requests and looks for unencoded reflection.</td><td>19</td></tr>
<tr><td>First actual output</td><td>The rule declares a named custom alert so teams can distinguish it from ZAP's built-in reflected XSS findings.</td><td>18</td></tr>
<tr><td>Second output / decision</td><td>A successful load means the rule can participate in scans. The actual alert still needs to be raised and verified.</td><td>20</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Highlight `_check()` and newAlert in source, then arrow to script name/alert in output. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-01.log</code> and <code>logs/recorded-step-01.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

**Source-review confidence 95%**, before live rehearsal. An estimate below the owner's release threshold cannot be increased without a matching real proof and reviewer approval.

---

## Step 2 — Register A Script-Based Login

**Why it matters:** Automated security scanning cannot rely on a manually pasted session cookie.

**Exact on-screen command**, executed in `demos/module1-demos/m1-demo3-python-scanning-authentication`:

```bash
./steps/02-register-scripted-authentication.sh
```

**Expected output format from the real step engine (ILLUSTRATIVE; replace with the current preflight log):**

```text
Script name: globomantics-auth (type: authentication · engine: <Jython engine>)
It submits: username=alice to POST /login, then ZAP reuses the session cookie
✔ PASS authentication script is valid and registered in ZAP
```

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Exact_Shots-0284c7"/></summary>
<table>
<tr><th>Relative shot / duration</th><th>Prescriptive actions</th></tr>
<tr><td>Before terminal · 8 seconds</td><td>VS Code: zap-scripts/globomantics-auth.py, focus on `authenticate`, `getRequiredParamsNames`, `getCredentialsParamsNames`. ZAP Scripts → Authentication.</td></tr>
<tr><td>Command · 8 seconds</td><td>Run <code>./steps/02-register-scripted-authentication.sh</code> once. Keep full filename readable, cursor clear, and no visible typo or backspace.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Box script name and `authentication` type.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Arrow to `username=alice` and `POST /login`; show PASS.</td></tr>
<tr><td>Exit / decision · 6–8 seconds</td><td>Show the actual PASS and any GUI proof. For a ZAP click, stage a pointer on its target 8 seconds before click, hold result 8 seconds after, then cut extra dead air.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Register a separate authentication script. It sends the login form so ZAP obtains a session without manually copied cookies.</td><td>19</td></tr>
<tr><td>First actual output</td><td>The training login submits username Alice to the login endpoint. A real production login would also enforce credential security.</td><td>19</td></tr>
<tr><td>Second output / decision</td><td>This registration gives ZAP a repeatable login mechanism, but the protected endpoint must still demonstrate authenticated access.</td><td>17</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Box `authenticate()` and POST login, then use a clean callout for submitted username. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-02.log</code> and <code>logs/recorded-step-02.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

**Source-review confidence 95%**, before live rehearsal. An estimate below the owner's release threshold cannot be increased without a matching real proof and reviewer approval.

---

## Step 3 — Prove Authenticated Profile Access

**Why it matters:** A scanner may report a clean site simply because it could not pass the login wall.

**Exact on-screen command**, executed in `demos/module1-demos/m1-demo3-python-scanning-authentication`:

```bash
./steps/03-confirm-authenticated-profile-access.sh
```

**Expected output format from the real step engine (ILLUSTRATIVE; replace with the current preflight log):**

```text
Without login: /account/profile -> HTTP 401 (gated)
ZAP forced-user (script auth): /account/profile -> HTTP 200 (reachable)
Auth script ran: authenticate: response=200
✔ PASS ZAP executed the authentication script and holds the session
```

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Exact_Shots-0284c7"/></summary>
<table>
<tr><th>Relative shot / duration</th><th>Prescriptive actions</th></tr>
<tr><td>Before terminal · 8 seconds</td><td>ZAP GUI → Sites → Globomantics context → Authentication and Users → Alice; ensure forced-user mode. Terminal shows the access comparison.</td></tr>
<tr><td>Command · 8 seconds</td><td>Run <code>./steps/03-confirm-authenticated-profile-access.sh</code> once. Keep full filename readable, cursor clear, and no visible typo or backspace.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Highlight unauthenticated HTTP 401 while showing protected profile URL.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Arrow to HTTP 200 and `authenticate:` trace from the same tested user.</td></tr>
<tr><td>Exit / decision · 6–8 seconds</td><td>Show the actual PASS and any GUI proof. For a ZAP click, stage a pointer on its target 8 seconds before click, hold result 8 seconds after, then cut extra dead air.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>First access the protected profile without login. The server returns unauthorized, confirming that the page is genuinely restricted.</td><td>18</td></tr>
<tr><td>First actual output</td><td>Enable ZAP's scripted user and repeat the request. The successful response shows the scanner reached the authenticated page.</td><td>18</td></tr>
<tr><td>Second output / decision</td><td>The authentication trace confirms ZAP ran the login script. A manual cookie would not prove this automated behavior.</td><td>18</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Place separate blue boxes on 401 and 200; arrow to auth trace, never claim only a login page was scanned. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-03.log</code> and <code>logs/recorded-step-03.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

**Source-review confidence 93%**, before live rehearsal. An estimate below the owner's release threshold cannot be increased without a matching real proof and reviewer approval.

---

## Step 4 — Raise The Fresh Custom Finding

**Why it matters:** Existing alerts can falsely suggest a custom rule worked during the current authenticated scan.

**Exact on-screen command**, executed in `demos/module1-demos/m1-demo3-python-scanning-authentication`:

```bash
./steps/04-confirm-custom-scan-alert.sh
```

**Expected output format from the real step engine (ILLUSTRATIVE; replace with the current preflight log):**

```text
Before scan (store cleared): absent
Scan target: http://app:8000/account/profile?note=seed (param: note, as user alice)
Probe requests the scan sent: <live-count>
Alert: Globomantics unsafe reflection (custom rule)
Risk: Medium
Parameter: note
Evidence: GLOBOxss7marker
✔ PASS the custom rule RAISED its named alert on this scan
```

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Exact_Shots-0284c7"/></summary>
<table>
<tr><th>Relative shot / duration</th><th>Prescriptive actions</th></tr>
<tr><td>Before terminal · 8 seconds</td><td>ZAP GUI → Alerts tab; in terminal run named step. The script clears the alert store, then scans as user Alice.</td></tr>
<tr><td>Command · 8 seconds</td><td>Run <code>./steps/04-confirm-custom-scan-alert.sh</code> once. Keep full filename readable, cursor clear, and no visible typo or backspace.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Show 'absent' before scan and authenticated profile with note parameter.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Highlight named alert, Medium risk, note, marker, then real GUI Alerts entry.</td></tr>
<tr><td>Exit / decision · 6–8 seconds</td><td>Show the actual PASS and any GUI proof. For a ZAP click, stage a pointer on its target 8 seconds before click, hold result 8 seconds after, then cut extra dead air.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Clear earlier alerts so a stale result cannot satisfy the check. Then scan the protected profile as authenticated user Alice.</td><td>20</td></tr>
<tr><td>First actual output</td><td>The fresh alert names the custom rule and the note parameter. Read the risk and marker evidence actually returned.</td><td>19</td></tr>
<tr><td>Second output / decision</td><td>This finding confirms the custom check executed under authentication. A built-in reflected XSS alert would not be equivalent.</td><td>18</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Use arrows from scan target to note parameter, then boxes on named custom alert and evidence marker. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-04.log</code> and <code>logs/recorded-step-04.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

**Source-review confidence 94%**, before live rehearsal. An estimate below the owner's release threshold cannot be increased without a matching real proof and reviewer approval.

---

## Delivery Gate

Deliver both branch refs and SHA, full preflight plus step logs, normalized parity result, untouched raw proof, GUI screenshots with timestamps, exact ElevenLabs script or audio, and Editor timeline. Record each live step from the authorized training target only. Never call an old scan or estimated screenshot actual evidence.
