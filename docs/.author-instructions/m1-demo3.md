# M1-DEMO3 · Jython Active Rule And Authentication — Production Playbook

<div align="center">

![Recorder](https://img.shields.io/badge/RECORDER-Screen_Plan-0284c7?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-Spoken_Teaching-d946ef?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-Callouts-16a34a?style=for-the-badge)

<img src="../learner-diagrams/m1-demo3-architecture.svg" alt="Jython Active Rule And Authentication flow diagram" width="100%"/>
<sub>Illustrative architecture · Generated using ChatGPT · TEMPORARILY PUBLIC author file</sub>

</div>

## First: Preflight And Parallel Narration Handoff

**Scenario:** Maya must authenticate to a protected Globomantics profile and run a custom Jython rule against the note parameter. The named custom alert only matters if the authenticated request really reached the page.

**Objectives:** EO2b — Implement Python scripts for custom scanning rules; EO2c — Apply scripting for authentication sequence automation

**1. Validate from the completed reference branch**, because the student starter intentionally excludes authored source files.

```bash
git clone -b m1-demo3-after https://github.com/rupeshtiwari/pluralsight-script-development-with-zap.git ~/zap-m1-demo3-reference
cd ~/zap-m1-demo3-reference
./setup/setup-macos.sh
cd demos/module1-demos/m1-demo3-python-scanning-authentication
./scripts/demo_reset.sh
./scripts/preflight_check.sh
ls logs/preflight-step-0[1-4].log
```

All four named commands are executed by preflight, not simulated by a separate implementation. **The narrator receives the four actual output logs and the unaltered raw evidence**. A correct preflight finishes `5 checks passed, 0 failed`. Record GUI-only proof separately. Shut the reference stack down with `./scripts/demo_down.sh`.

**2. Recorder starts independently from the [m1-demo3-before branch](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/tree/m1-demo3-before/demos/module1-demos/m1-demo3-python-scanning-authentication)**. Clone to a different folder, create the missing script files during the exercise, and copy the four preflight-step logs from the reference to the recorder demo's `logs/` folder once source is completed. The actual preflight runs on the completed state: a starter lacking code cannot produce successful scan proof yet.

**3. Before filming, off-screen**, run `export DEMO_SYNC_MODE=1` and `export DEMO_SYNC_PHASE=compare`. Each command still executes live. The visible transcript normalizes variable identifiers and telemetry, compares material proof to preflight, and fails the take on mismatch; raw outputs are archived. Exact command names below match the student README. Do not use copied preflight values as live ZAP Script Console proof.

**Primary UI:** VS Code source + integrated terminal; ZAP GUI http://localhost:8080/zap/ → Scripts, Sites and Alerts. Capture full-screen. Increase zoom for phone readability. Command hold ~8 seconds before Enter; each meaningful output 6–8 seconds (maximum 10 seconds idle final frame). For important clicks, provide 8-second pre-click and post-click editing handles in raw footage; trim later.

## Exact Four-Step Recorder / Narrator / Editor Choreography

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
