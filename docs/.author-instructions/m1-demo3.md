# Module 1 · Demo 3 — Python scanning and authentication · Production guide

<div align="center">

![Recorder](https://img.shields.io/badge/RECORDER-Show_Real_Evidence-00A3FF?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-One_Highlight-02E088?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-ElevenLabs_Words-770EF7?style=for-the-badge)

<img src="../learner-diagrams/m1-demo3-architecture.svg" width="100%" alt="Training evidence flow for m1-demo3"/>
<sub>Illustrative architecture · Generated using ChatGPT · Temporary PUBLIC production material</sub>

</div>

[← Production dashboard](README.md) · [Open student's Module 1 demo README](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo3-before/demos/module1-demos/m1-demo3-python-scanning-authentication/README.md)

## Recorder assignment

**Work only on `m1-demo3-before`**, completing missing exercise source where applicable. The Developer has already generated the batch preflight, saved four approved baseline transcripts and made the `deliverables/m1-demo3/` package available. **Do not rerun Mac setup or batch preflight as part of filming.** Read the [one-time setup and Developer responsibilities](README.md) on the author dashboard.

**Start privately before recording:** from repository root, `git switch m1-demo3-before`, then `cd demos/module1-demos/m1-demo3-python-scanning-authentication`; start the vulnerable lab with `./scripts/demo_reset.sh`. Confirm the app is reachable at `http://localhost:8000/`, and preserve all intended authored changes. Run commands from the specified VS Code integrated Terminal or macOS Terminal in the appropriate step.

**Recording order:** show source/context → display exact command for approximately 8 seconds → Enter once → show real output in 6–8-second proof windows → switch screens only as the current claim requires. The Editor trims long waits. A mismatched recording transcript is a retake, not a chance to create a fake PASS.

## Follow these four steps

## Step 1 — Register a custom Jython active-scan rule

<details open>
<summary><b>Open step 1 — command, real expected fields and role instructions</b></summary>

<summary><b>Step 1: Register a custom Jython active-scan rule</b> — Load custom rule</summary>

### The small problem to solve

A built-in scanner may not test the application's own unsafe reflection condition.

**Learning focus:** Implement a custom Python scanning rule *(EO2b)*

### Where to go

**Open VS Code.** Open `zap-scripts/globomantics-active-rule.py`. Inspect `scan` and `newAlert` / `raiseAlert`. Show **ZAP GUI → Scripts → Active Rules** if validating the loaded script.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo3-python-scanning-authentication`.

```bash
./steps/01-load-python-active-scan-rule.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Script name</b></td><td><code>globomantics-active-rule (active · Jython)</code></td><td>Correct script type and engine</td></tr>
<tr><td><b>Alert it raises</b></td><td><code>Globomantics unsafe reflection (custom rule)</code></td><td>Named finding, not generic built-in XSS</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS custom active rule loaded</code></td><td>Loading alone is not a fired alert</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

The custom rule is now registered with ZAP's active scanning mechanism, where it can inspect application-specific parameters.

**How this connects:** Provide the authentication sequence so the rule can reach the protected profile.

### Recorder — execute and show

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

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Highlight `_check()` and newAlert in source, then arrow to script name/alert in output. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-01.log</code> and <code>logs/recorded-step-01.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Load a Jython active rule for the profile's note parameter. The rule clones requests and looks for unencoded reflection.</td><td>19</td></tr>
<tr><td>First actual output</td><td>The rule declares a named custom alert so teams can distinguish it from ZAP's built-in reflected XSS findings.</td><td>18</td></tr>
<tr><td>Second output / decision</td><td>A successful load means the rule can participate in scans. The actual alert still needs to be raised and verified.</td><td>20</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo3/logs/preflight-step-01.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence 95%, before live rehearsal. An estimate below the owner's release threshold cannot
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Step 2 — Register the login script

<details>
<summary><b>Open step 2 — command, real expected fields and role instructions</b></summary>

<summary><b>Step 2: Register the login script</b> — Script authentication</summary>

### The small problem to solve

Manual cookie copying is unreliable in repeatable automated scanning.

**Learning focus:** Apply scripting to authentication sequence automation *(EO2c)*

### Where to go

**In VS Code**, inspect `zap-scripts/globomantics-auth.py`, focusing on `authenticate` and `getCredentialsParamsNames`. Use ZAP GUI → Scripts → Authentication for confirmation.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo3-python-scanning-authentication`.

```bash
./steps/02-register-scripted-authentication.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Script name</b></td><td><code>globomantics-auth (authentication · Jython)</code></td><td>Authentication script identity</td></tr>
<tr><td><b>It submits</b></td><td><code>username=alice to POST /login</code></td><td>Training-only simplified login</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS authentication script registered</code></td><td>The protected endpoint remains to be tested</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

ZAP can now obtain a session by running a script rather than accepting an operator's copied cookie. The course's simplified username-only login is not a production security model.

**How this connects:** Prove the script really changes access to the protected page.

### Recorder — execute and show

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

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Box `authenticate()` and POST login, then use a clean callout for submitted username. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-02.log</code> and <code>logs/recorded-step-02.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Register a separate authentication script. It sends the login form so ZAP obtains a session without manually copied cookies.</td><td>19</td></tr>
<tr><td>First actual output</td><td>The training login submits username Alice to the login endpoint. A real production login would also enforce credential security.</td><td>19</td></tr>
<tr><td>Second output / decision</td><td>This registration gives ZAP a repeatable login mechanism, but the protected endpoint must still demonstrate authenticated access.</td><td>17</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo3/logs/preflight-step-02.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence 95%, before live rehearsal. An estimate below the owner's release threshold cannot
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Step 3 — Compare unauthenticated and scripted access

<details>
<summary><b>Open step 3 — command, real expected fields and role instructions</b></summary>

<summary><b>Step 3: Compare unauthenticated and scripted access</b> — Prove protected access</summary>

### The small problem to solve

A scan can incorrectly look clean if it never passes the login wall.

**Learning focus:** Verify scripted authentication effectiveness *(EO2c)*

### Where to go

**In ZAP GUI**, inspect Globomantics context and user Alice. Then return to **VS Code Terminal** to run the comparison. No cookie is manually supplied by the shell probe.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo3-python-scanning-authentication`.

```bash
./steps/03-confirm-authenticated-profile-access.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Without login</b></td><td><code>/account/profile → HTTP 401</code></td><td>Endpoint truly protected</td></tr>
<tr><td><b>ZAP forced-user script auth</b></td><td><code>/account/profile → HTTP 200</code></td><td>ZAP obtains valid session</td></tr>
<tr><td><b>Auth script ran</b></td><td><code>authenticate: &lt;actual trace&gt;</code></td><td>Trace must prove script invocation</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS ZAP executed authentication script</code></td><td>Both HTTP status and auth trace required</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

HTTP 401 without login and HTTP 200 with ZAP's scripted user establish that the scanner can access the authenticated resource.

**How this connects:** Run the custom rule against the authenticated page, and reject stale findings.

### Recorder — execute and show

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

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Place separate blue boxes on 401 and 200; arrow to auth trace, never claim only a login page was scanned. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-03.log</code> and <code>logs/recorded-step-03.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>First access the protected profile without login. The server returns unauthorized, confirming that the page is genuinely restricted.</td><td>18</td></tr>
<tr><td>First actual output</td><td>Enable ZAP's scripted user and repeat the request. The successful response shows the scanner reached the authenticated page.</td><td>18</td></tr>
<tr><td>Second output / decision</td><td>The authentication trace confirms ZAP ran the login script. A manual cookie would not prove this automated behavior.</td><td>18</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo3/logs/preflight-step-03.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence 93%, before live rehearsal. An estimate below the owner's release threshold cannot
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Step 4 — Confirm a fresh custom scan alert

<details>
<summary><b>Open step 4 — command, real expected fields and role instructions</b></summary>

<summary><b>Step 4: Confirm a fresh custom scan alert</b> — Prove custom alert</summary>

### The small problem to solve

A previous alert can make a new scan seem successful when the custom rule never ran.

**Learning focus:** Demonstrate application-specific scanning proof *(EO2b)*

### Where to go

**Open ZAP GUI → Alerts** for the targeted profile. Run the command in **VS Code Terminal**, then return to the Alerts pane and inspect the newly produced named finding.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo3-python-scanning-authentication`.

```bash
./steps/04-confirm-custom-scan-alert.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Before scan</b></td><td><code>absent</code></td><td>Cleared alert store</td></tr>
<tr><td><b>Scan target</b></td><td><code>/account/profile?note=seed (as alice)</code></td><td>Authorized authenticated parameter</td></tr>
<tr><td><b>Alert</b></td><td><code>Globomantics unsafe reflection (custom rule)</code></td><td>Exact custom finding</td></tr>
<tr><td><b>Risk / Parameter</b></td><td><code>&lt;actual risk&gt; / note</code></td><td>Current result, not placeholder</td></tr>
<tr><td><b>Evidence</b></td><td><code>&lt;actual reflected marker&gt;</code></td><td>Evidence from real request</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS named alert raised on current scan</code></td><td>Absent before and present after</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

A new authenticated scan now produces the required custom alert tied to `note`. Built-in XSS alerts are not substitutes.

**How this connects:** The demo closes with repeatable authentication and an application-specific finding supported by a fresh scan.

### Recorder — execute and show

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

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Use arrows from scan target to note parameter, then boxes on named custom alert and evidence marker. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-04.log</code> and <code>logs/recorded-step-04.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Clear earlier alerts so a stale result cannot satisfy the check. Then scan the protected profile as authenticated user Alice.</td><td>20</td></tr>
<tr><td>First actual output</td><td>The fresh alert names the custom rule and the note parameter. Read the risk and marker evidence actually returned.</td><td>19</td></tr>
<tr><td>Second output / decision</td><td>This finding confirms the custom check executed under authentication. A built-in reflected XSS alert would not be equivalent.</td><td>18</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo3/logs/preflight-step-04.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence 94%, before live rehearsal. An estimate below the owner's release threshold cannot
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Finish the recording

1. Capture all four real step outcomes, their matching raw logs and GUI/CI evidence; preserve the recorded branch SHA
2. Stop the lab from the same demo folder: `./scripts/demo_down.sh`
3. Hand the video takes to the Editor and the Developer's generated narration draft and logs to the Narrator
4. Leave the developer-wide batch validation and its configuration in the landing page, not in this per-demo recording page

