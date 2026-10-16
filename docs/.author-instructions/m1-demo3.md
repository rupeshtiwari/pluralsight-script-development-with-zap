# Module 1 · Demo 3 — Python scanning and authentication · Production guide

<div align="center">

![Recorder](https://img.shields.io/badge/RECORDER-Show_Real_Evidence-00A3FF?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-One_Highlight-02E088?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-ElevenLabs_Words-770EF7?style=for-the-badge)

<img src="../learner-diagrams/m1-demo3-architecture.svg" width="100%" alt="Training evidence flow for m1-demo3"/>
<sub>Illustrative architecture · Generated using ChatGPT · Temporary PUBLIC production material</sub>

</div>

[← Production dashboard](README.md) · [Open student's Module 1 demo README](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo3-before/demos/module1-demos/m1-demo3-python-scanning-authentication/README.md)

<!-- demo-navigation:start -->
<p align="center"><b>Author production guide · Demo 3 of 6</b></p>
<p align="center">
  <a href="m1-demo2.md"><img alt="Previous author guide: Module 1 Demo 2 — JavaScript HTTP Sender" src="https://img.shields.io/badge/%E2%86%90_Previous-M1_Demo_2-130F25?style=for-the-badge"></a>
  <a href="m2-demo1.md"><img alt="Next author guide: Module 2 Demo 1 — Authenticated ZAP in GitHub Actions" src="https://img.shields.io/badge/Next_%E2%86%92-M2_Demo_1-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->

## Prepare Recording

**Work only on `m1-demo3-before`**, completing missing exercise source where applicable. The Recorder must receive the Developer's **actually successful** batch proof, four real reference transcripts, and timestamped `~/zap-course-deliverables/batch-YYYYMMDD-HHMMSS/m1-demo3/` package before filming. Do not assume that a package exists before the Developer verifies it. **Do not rerun Mac setup or batch preflight as part of filming.** Read the [one-time setup and Developer responsibilities](README.md) on the author dashboard.

**Start privately before recording:** from repository root, `git switch m1-demo3-before`, then `cd demos/module1-demos/m1-demo3-python-scanning-authentication`; start the vulnerable lab with `./scripts/demo_reset.sh`. Confirm the app is reachable at `http://localhost:8000/`, and preserve all intended authored changes. Run commands from the specified VS Code integrated Terminal or macOS Terminal in the appropriate step.

**Recording order:** show source/context → display exact command for approximately 8 seconds → Enter once → show real output in 6–8-second proof windows → switch screens only as the current claim requires. The Editor trims long waits. A mismatched recording transcript is a retake, not a chance to create a fake PASS.

## Recording Steps

<!-- demo-readiness:start -->
## Demo Readiness

**Approved duration:** 6 minutes. **Execution steps:** four, unchanged. **Acceptance target:** overall review score at least 98/100.

| Step | Current evidence-backed score | Blocking review |
|---|---|---|
| 1 | Not assessed | Matching Mac take, required GUI/Actions proof and final spoken coverage |
| 2 | Not assessed | Matching Mac take, required GUI/Actions proof and final spoken coverage |
| 3 | Not assessed | Matching Mac take, required GUI/Actions proof and final spoken coverage |
| 4 | Not assessed | Matching Mac take, required GUI/Actions proof and final spoken coverage |

**Overall confidence:** NOT ASSESSED. Once all four step scores are supported, calculate `(step1 + step2 + step3 + step4) / 4`; do not average only the reviewed steps. A missing critical proof keeps release on HOLD even when the average reaches 98.

**Speech budget:** current short-form draft 223 whitespace words; final 6-minute target 774 spoken words under the owner contract. Remaining before final audio validation: 551 words. This draft is not a complete timed recording script. Expand useful source/action/result teaching within the same four steps; do not fill time with invented stories.

**Recording budget:** approximately 90 seconds per step, including source work, execution and proof. This is an editing plan, not a measured duration or a reason to leave a static screen.

**Review method:** assess LO and outline coverage, technical correctness, example quality, learner clarity, operator decision-making and recorded proof against the exact source SHA. Record the reviewer, rationale and evidence for every numeric score. Old 88–96% source estimates lacked a documented common rubric and are retired, not promoted.
<!-- demo-readiness:end -->
## Step 1 — Register a custom Jython active-scan rule

<details open>
<summary><b>Open step 1 — command, real expected fields and role instructions</b></summary>


### Learning Goal

A built-in scanner may not test the application's own unsafe reflection condition.

**Learning focus:** Implement a custom Python scanning rule *(EO2b)*

### Demo Workspace


**Off-camera terminal setup:** Open VS Code integrated Terminal. Preserve any uncommitted work before changing branches. Paste these commands exactly; they select the demo starter and working folder.

```bash
cd "$HOME/pluralsight-script-development-with-zap"
git switch m1-demo3-before
cd "demos/module1-demos/m1-demo3-python-scanning-authentication"
```

**Actual screen and browser check:** Check http://localhost:8000/ off camera. Open the Python active-rule source in VS Code; then http://localhost:8080/zap/ → Scripts → Active Rules to show loaded rule.


**Open VS Code.** Open `zap-scripts/globomantics-active-rule.py`. Inspect `scan` and `newAlert` / `raiseAlert`. Show **ZAP GUI → Scripts → Active Rules** if validating the loaded script.

### Run Command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo3-python-scanning-authentication`.

```bash
./steps/01-load-python-active-scan-rule.sh
```

### Expected Results

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Script name</b></td><td><code>globomantics-active-rule (active · Jython)</code></td><td>Correct script type and engine</td></tr>
<tr><td><b>Alert it raises</b></td><td><code>Globomantics unsafe reflection (custom rule)</code></td><td>Named finding, not generic built-in XSS</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS custom active rule loaded</code></td><td>Loading alone is not a fired alert</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### Operator Decision

The custom rule is now registered with ZAP's active scanning mechanism, where it can inspect application-specific parameters.

**How this connects:** Provide the authentication sequence so the rule can reach the protected profile.

<!-- capture-location:start -->
<table><tr><th>Capture moment</th><th>Exact action and result location</th></tr><tr><td>Before Enter</td><td>Use VS Code integrated Terminal. Show the named step command already provided below/above; keep its full filename readable for about eight seconds. Directory and branch setup are off camera.</td></tr><tr><td>After Enter</td><td>Show the completed active-rule source in VS Code before execution; after terminal registration, switch to http://localhost:8080/zap/, Scripts, Active Rules.</td></tr><tr><td>Evidence to record</td><td>Actual loaded Jython rule, custom alert name and scan/alert-creation logic; loading is not a finding. Hold each meaningful field for six to eight seconds; retain the matching raw log and take ID.</td></tr><tr><td>Meaning and decision</td><td>Use the Spoken Narration for this exact field, then explain whether the evidence is enough to proceed. If it is absent, stop: neither a source declaration nor an expected output is an observed result.</td></tr><tr><td>Editor handoff</td><td>Mark the result region, then the actual value being explained. Clear old overlays on pane change. During an otherwise still explanation beyond 12 seconds, use one relevant 6–8-second takeaway callout; never invent a successful result.</td></tr></table>
<!-- capture-location:end -->

### Recorder Shots

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

### Spoken Narration

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Load a Jython active rule for the profile's note parameter. The rule clones requests and looks for unencoded reflection.</td><td>19</td></tr>
<tr><td>First actual output</td><td>The rule declares a named custom alert so teams can distinguish it from ZAP's built-in reflected XSS findings.</td><td>18</td></tr>
<tr><td>Second output / decision</td><td>A successful load means the rule can participate in scans. The actual alert still needs to be raised and verified.</td><td>20</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Editor Actions

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Jython active-rule source and registration</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Alert it raises</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Script name</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>A named rule must load before it raises a finding</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Highlight `_check()` and newAlert in source, then arrow to script name/alert in output. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-01.log</code> and <code>logs/recorded-step-01.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Proof Review

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo3/logs/preflight-step-01.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Release:** HOLD until evidence review; target overall score 98/100, never automatic approval

</details>
## Step 2 — Register the login script

<details>
<summary><b>Open step 2 — command, real expected fields and role instructions</b></summary>


### Learning Goal

Manual cookie copying is unreliable in repeatable automated scanning.

**Learning focus:** Apply scripting to authentication sequence automation *(EO2c)*

### Demo Workspace


**Off-camera terminal setup:** Open VS Code integrated Terminal. Preserve any uncommitted work before changing branches. Paste these commands exactly; they select the demo starter and working folder.

```bash
cd "$HOME/pluralsight-script-development-with-zap"
git switch m1-demo3-before
cd "demos/module1-demos/m1-demo3-python-scanning-authentication"
```

**Actual screen and browser check:** Show authentication source in VS Code, then http://localhost:8080/zap/ → Scripts → Authentication for loaded login script. The demo login is deliberately simplified.


**In VS Code**, inspect `zap-scripts/globomantics-auth.py`, focusing on `authenticate` and `getCredentialsParamsNames`. Use ZAP GUI → Scripts → Authentication for confirmation.

### Run Command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo3-python-scanning-authentication`.

```bash
./steps/02-register-scripted-authentication.sh
```

### Expected Results

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Script name</b></td><td><code>globomantics-auth (authentication · Jython)</code></td><td>Authentication script identity</td></tr>
<tr><td><b>It submits</b></td><td><code>username=alice to POST /login</code></td><td>Training-only simplified login</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS authentication script registered</code></td><td>The protected endpoint remains to be tested</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### Operator Decision

ZAP can now obtain a session by running a script rather than accepting an operator's copied cookie. The course's simplified username-only login is not a production security model.

**How this connects:** Prove the script really changes access to the protected page.

<!-- capture-location:start -->
<table><tr><th>Capture moment</th><th>Exact action and result location</th></tr><tr><td>Before Enter</td><td>Use VS Code integrated Terminal. Show the named step command already provided below/above; keep its full filename readable for about eight seconds. Directory and branch setup are off camera.</td></tr><tr><td>After Enter</td><td>Show the separate authentication source in VS Code; after terminal registration switch to http://localhost:8080/zap/, Scripts, Authentication.</td></tr><tr><td>Evidence to record</td><td>Login submission and registered script identity; explicitly bound the simplified lab login. Hold each meaningful field for six to eight seconds; retain the matching raw log and take ID.</td></tr><tr><td>Meaning and decision</td><td>Use the Spoken Narration for this exact field, then explain whether the evidence is enough to proceed. If it is absent, stop: neither a source declaration nor an expected output is an observed result.</td></tr><tr><td>Editor handoff</td><td>Mark the result region, then the actual value being explained. Clear old overlays on pane change. During an otherwise still explanation beyond 12 seconds, use one relevant 6–8-second takeaway callout; never invent a successful result.</td></tr></table>
<!-- capture-location:end -->

### Recorder Shots

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

### Spoken Narration

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Register a separate authentication script. It sends the login form so ZAP obtains a session without manually copied cookies.</td><td>19</td></tr>
<tr><td>First actual output</td><td>The training login submits username Alice to the login endpoint. A real production login would also enforce credential security.</td><td>19</td></tr>
<tr><td>Second output / decision</td><td>This registration gives ZAP a repeatable login mechanism, but the protected endpoint must still demonstrate authenticated access.</td><td>17</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Editor Actions

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Separate Jython authentication source and registration</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>It submits</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Script name</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>Authentication is separate from scanning</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Box `authenticate()` and POST login, then use a clean callout for submitted username. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-02.log</code> and <code>logs/recorded-step-02.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Proof Review

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo3/logs/preflight-step-02.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Release:** HOLD until evidence review; target overall score 98/100, never automatic approval

</details>
## Step 3 — Compare unauthenticated and scripted access

<details>
<summary><b>Open step 3 — command, real expected fields and role instructions</b></summary>


### Learning Goal

A scan can incorrectly look clean if it never passes the login wall.

**Learning focus:** Verify scripted authentication effectiveness *(EO2c)*

### Demo Workspace


**Off-camera terminal setup:** Open VS Code integrated Terminal. Preserve any uncommitted work before changing branches. Paste these commands exactly; they select the demo starter and working folder.

```bash
cd "$HOME/pluralsight-script-development-with-zap"
git switch m1-demo3-before
cd "demos/module1-demos/m1-demo3-python-scanning-authentication"
```

**Actual screen and browser check:** Use http://localhost:8000/account/profile without login as a denied control, then ZAP scripted-user context and Terminal authenticated HTTP response; never treat copied cookies as scripted-auth proof.


**In ZAP GUI**, inspect Globomantics context and user Alice. Then return to **VS Code Terminal** to run the comparison. No cookie is manually supplied by the shell probe.

### Run Command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo3-python-scanning-authentication`.

```bash
./steps/03-confirm-authenticated-profile-access.sh
```

### Expected Results

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

### Operator Decision

HTTP 401 without login and HTTP 200 with ZAP's scripted user establish that the scanner can access the authenticated resource.

**How this connects:** Run the custom rule against the authenticated page, and reject stale findings.

<!-- capture-location:start -->
<table><tr><th>Capture moment</th><th>Exact action and result location</th></tr><tr><td>Before Enter</td><td>Use VS Code integrated Terminal. Show the named step command already provided below/above; keep its full filename readable for about eight seconds. Directory and branch setup are off camera.</td></tr><tr><td>After Enter</td><td>Stay in the terminal for denied and authenticated profile requests and the authentication trace. Then show http://localhost:8080/zap/, Globomantics context, Users, Alice when verifying context state.</td></tr><tr><td>Evidence to record</td><td>Real protected-profile HTTP responses and ZAP script execution, not a manually supplied shell cookie. Hold each meaningful field for six to eight seconds; retain the matching raw log and take ID.</td></tr><tr><td>Meaning and decision</td><td>Use the Spoken Narration for this exact field, then explain whether the evidence is enough to proceed. If it is absent, stop: neither a source declaration nor an expected output is an observed result.</td></tr><tr><td>Editor handoff</td><td>Mark the result region, then the actual value being explained. Clear old overlays on pane change. During an otherwise still explanation beyond 12 seconds, use one relevant 6–8-second takeaway callout; never invent a successful result.</td></tr></table>
<!-- capture-location:end -->

### Recorder Shots

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

### Spoken Narration

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>First access the protected profile without login. The server returns unauthorized, confirming that the page is genuinely restricted.</td><td>18</td></tr>
<tr><td>First actual output</td><td>Enable ZAP's scripted user and repeat the request. The successful response shows the scanner reached the authenticated page.</td><td>18</td></tr>
<tr><td>Second output / decision</td><td>The authentication trace confirms ZAP ran the login script. A manual cookie would not prove this automated behavior.</td><td>18</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Editor Actions

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Protected endpoint before/after authentication</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Without login</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>ZAP forced-user (script auth)</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>Prove the authenticated session and HTTP status</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Place separate blue boxes on 401 and 200; arrow to auth trace, never claim only a login page was scanned. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-03.log</code> and <code>logs/recorded-step-03.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Proof Review

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo3/logs/preflight-step-03.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Release:** HOLD until evidence review; target overall score 98/100, never automatic approval

</details>
## Step 4 — Confirm a fresh custom scan alert

<details>
<summary><b>Open step 4 — command, real expected fields and role instructions</b></summary>


### Learning Goal

A previous alert can make a new scan seem successful when the custom rule never ran.

**Learning focus:** Demonstrate application-specific scanning proof *(EO2b)*

### Demo Workspace


**Off-camera terminal setup:** Open VS Code integrated Terminal. Preserve any uncommitted work before changing branches. Paste these commands exactly; they select the demo starter and working folder.

```bash
cd "$HOME/pluralsight-script-development-with-zap"
git switch m1-demo3-before
cd "demos/module1-demos/m1-demo3-python-scanning-authentication"
```

**Actual screen and browser check:** Show fresh custom finding in http://localhost:8080/zap/ → Alerts, matching /account/profile and note parameter. Built-in XSS is not the custom rule.


**Open ZAP GUI → Alerts** for the targeted profile. Run the command in **VS Code Terminal**, then return to the Alerts pane and inspect the newly produced named finding.

### Run Command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo3-python-scanning-authentication`.

```bash
./steps/04-confirm-custom-scan-alert.sh
```

### Expected Results

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

### Operator Decision

A new authenticated scan now produces the required custom alert tied to `note`. Built-in XSS alerts are not substitutes.

**How this connects:** The demo closes with repeatable authentication and an application-specific finding supported by a fresh scan.

<!-- capture-location:start -->
<table><tr><th>Capture moment</th><th>Exact action and result location</th></tr><tr><td>Before Enter</td><td>Use VS Code integrated Terminal. Show the named step command already provided below/above; keep its full filename readable for about eight seconds. Directory and branch setup are off camera.</td></tr><tr><td>After Enter</td><td>Show absent-before and fresh-after terminal evidence. Switch to http://localhost:8080/zap/, Alerts, and select the newly named custom alert on /account/profile.</td></tr><tr><td>Evidence to record</td><td>Fresh custom name, note parameter, risk and response evidence; built-in XSS is not equivalent. Hold each meaningful field for six to eight seconds; retain the matching raw log and take ID.</td></tr><tr><td>Meaning and decision</td><td>Use the Spoken Narration for this exact field, then explain whether the evidence is enough to proceed. If it is absent, stop: neither a source declaration nor an expected output is an observed result.</td></tr><tr><td>Editor handoff</td><td>Mark the result region, then the actual value being explained. Clear old overlays on pane change. During an otherwise still explanation beyond 12 seconds, use one relevant 6–8-second takeaway callout; never invent a successful result.</td></tr></table>
<!-- capture-location:end -->

### Recorder Shots

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

### Spoken Narration

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Clear earlier alerts so a stale result cannot satisfy the check. Then scan the protected profile as authenticated user Alice.</td><td>20</td></tr>
<tr><td>First actual output</td><td>The fresh alert names the custom rule and the note parameter. Read the risk and marker evidence actually returned.</td><td>19</td></tr>
<tr><td>Second output / decision</td><td>This finding confirms the custom check executed under authentication. A built-in reflected XSS alert would not be equivalent.</td><td>18</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Editor Actions

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Fresh ZAP Alerts custom rule</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Alert</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Evidence</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>A fresh custom finding needs a real named alert</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Use arrows from scan target to note parameter, then boxes on named custom alert and evidence marker. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-04.log</code> and <code>logs/recorded-step-04.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Proof Review

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo3/logs/preflight-step-04.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Release:** HOLD until evidence review; target overall score 98/100, never automatic approval

</details>

## Finish the recording

1. Capture all four real step outcomes, their matching raw logs and GUI/CI evidence; preserve the recorded branch SHA
2. Stop the lab from the same demo folder: `./scripts/demo_down.sh`
3. Hand the video takes to the Editor and the Developer's generated narration draft and logs to the Narrator
4. Leave the developer-wide batch validation and its configuration in the landing page, not in this per-demo recording page

<!-- demo-navigation:start -->
<p align="center"><b>Author production guide · Demo 3 of 6</b></p>
<p align="center">
  <a href="m1-demo2.md"><img alt="Previous author guide: Module 1 Demo 2 — JavaScript HTTP Sender" src="https://img.shields.io/badge/%E2%86%90_Previous-M1_Demo_2-130F25?style=for-the-badge"></a>
  <a href="m2-demo1.md"><img alt="Next author guide: Module 2 Demo 1 — Authenticated ZAP in GitHub Actions" src="https://img.shields.io/badge/Next_%E2%86%92-M2_Demo_1-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->
