# Module 1 · Demo 1 — Injection, XSS and CSRF · Production guide

<div align="center">

![Recorder](https://img.shields.io/badge/RECORDER-Show_Real_Evidence-00A3FF?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-One_Highlight-02E088?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-ElevenLabs_Words-770EF7?style=for-the-badge)

<img src="../learner-diagrams/m1-demo1-architecture.svg" width="100%" alt="Training evidence flow for m1-demo1"/>
<sub>Illustrative architecture · Generated using ChatGPT · Temporary PUBLIC production material</sub>

</div>

[← Production dashboard](README.md) · [Open student's Module 1 demo README](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo1-before/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf/README.md)

<!-- demo-navigation:start -->
<p align="center"><b>Author production guide · Demo 1 of 6</b></p>
<p align="center">
  <a href="README.md"><img alt="All author production guides" src="https://img.shields.io/badge/%E2%86%90_Back_to-All_Demos-585FA2?style=for-the-badge"></a>
  <a href="m1-demo2.md"><img alt="Next author guide: Module 1 Demo 2 — JavaScript HTTP Sender" src="https://img.shields.io/badge/Next_%E2%86%92-M1_Demo_2-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->

## Recorder assignment

**Work only on `m1-demo1-before`**, completing missing exercise source where applicable. The Recorder must receive the Developer's **actually successful** batch proof, four real reference transcripts, and timestamped `~/zap-course-deliverables/batch-YYYYMMDD-HHMMSS/m1-demo1/` package before filming. Do not assume that a package exists before the Developer verifies it. **Do not rerun Mac setup or batch preflight as part of filming.** Read the [one-time setup and Developer responsibilities](README.md) on the author dashboard.

**Start privately before recording:** from repository root, `git switch m1-demo1-before`, then `cd demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`; start the vulnerable lab with `./scripts/demo_reset.sh`. Confirm the app is reachable at `http://localhost:8000/`, and preserve all intended authored changes. Run commands from the specified VS Code integrated Terminal or macOS Terminal in the appropriate step.

**Recording order:** show source/context → display exact command for approximately 8 seconds → Enter once → show real output in 6–8-second proof windows → switch screens only as the current claim requires. The Editor trims long waits. A mismatched recording transcript is a retake, not a chance to create a fake PASS.

## Follow these four steps

## Step 1 — Run one targeted injection scan

<details open>
<summary><b>Open step 1 — command, real expected fields and role instructions</b></summary>


### The small problem to solve

The search, account and administrative endpoints reach three different execution boundaries; a generic alert total hides those differences.

**Learning focus:** Configure specialized SQL, NoSQL and command-injection checks *(EO1a)*

### Where to go


**Required directory navigation:** Open VS Code integrated Terminal manually. Do not browse through folders in Finder or type a relative path. Paste this complete command and press Enter before running the named step:

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf"
```

**Branch:** `m1-demo1-before` (complete any deliberately missing student source first). The separate `./steps/01-*.sh` command below is the only on-camera execution for this step.

**Open VS Code.** Use File → Open Folder to open the repository. In the editor open `runtime/app/main.py`. In the integrated Terminal, inspect the three prepared views by running `./scripts/show_code.sh sqli`, `./scripts/show_code.sh nosql` and `./scripts/show_code.sh cmd`. Keep source functions `search`, `account` and `admin_ping` accessible.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`.

```bash
./steps/01-run-targeted-injection-scan.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Policy rules enabled</b></td><td><code>SQL-injection family + NoSQL 40033 + command 90020/90037</code></td><td>Confirm the policy is focused</td></tr>
<tr><td><b>SQL injection · /search (q)</b></td><td><code>alert 40018 or 40022 · &lt;live risk&gt;/&lt;live confidence&gt;</code></td><td>Correlate the SQL alert with q</td></tr>
<tr><td><b>NoSQL injection · /api/account (username)</b></td><td><code>alert 40033 · &lt;live risk&gt;/&lt;live confidence&gt;</code></td><td>Correlate NoSQL with username</td></tr>
<tr><td><b>Command injection · /admin/ping (host)</b></td><td><code>alert 90020 or 90037 · &lt;live risk&gt;/&lt;live confidence&gt;</code></td><td>Correlate OS command with host</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS targeted scan raised all three injection alerts</code></td><td>Only pass with three actual findings</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

Three different request parameters are now associated with targeted ZAP findings. The risk/confidence fields report the current engine's result; the mere presence of an alert is not yet a defensible confirmation of all three defects.

**How this connects:** Now validate the page-output context rather than treating every reflected input as XSS.

### Recorder — execute and show

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/> Exact Screen And Timing</summary>
<table>
<tr><th>Relative Footage</th><th>Required Screen / Action</th></tr>
<tr><td>Source context · 00:00–00:08</td><td>VS Code: Cmd+P → runtime/app/main.py. Show search() near line 149, account() near line 196, and admin_ping() near line 227. In the terminal use ./scripts/show_code.sh sqli, nosql and cmd to show exact sink lines.</td></tr>
<tr><td>Command · next 8 seconds</td><td>Show the full command above from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf` at readable zoom, keep the pointer away from key text and press Enter once.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Highlight the policy-rule line, then SQL injection alert and q parameter.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Highlight 40033 with username, then 90020 or 90037 with host. Do not claim normal ping output proves injection.</td></tr>
<tr><td>Completion · 6–8 seconds</td><td>Hold the actual PASS line or stop on FAIL. Capture the exact console output and screen/take timestamp. Do not leave any single proof frame static more than 10 seconds.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-Purple-d946ef"/> Exact ElevenLabs Narration</summary>
<table><tr><th>Visual Reveal</th><th>Spoken Words — Copy Exactly After Verifying Proof</th><th>Count</th></tr>
<tr><td>00:00–00:08 · command</td><td>Run this focused ZAP policy against the store’s search, account, and administrative endpoints. Each input reaches a different vulnerable boundary.</td><td>20 spoken words</td></tr>
<tr><td>After execution · proof A</td><td>The SQL rule reports the search parameter q. The MongoDB rule checks username, so these findings describe different application behavior.</td><td>20 spoken words</td></tr>
<tr><td>After execution · proof B</td><td>The command rule targets host. Three parameter-specific alerts establish where to investigate; the real requests and responses determine disposition.</td><td>19 spoken words</td></tr>
</table>
The lines are spoken sentences, not production notes. The second and third lines are recorded only if the named evidence is actually visible. If observed values change, revalidate the claims against the filmed take rather than adding invented numbers.
</details>

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/> Callouts, Cuts And Sync</summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Targeted injection results</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>SQL injection · /search (q)</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>NoSQL injection · /api/account (username)</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>Different inputs cross different execution boundaries</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Edit Point</th><th>Exact Action</th></tr>
<tr><td>Command entrance</td><td>Clean cut after source context; frame the entire named command with a subtle square or underline for ≤8 seconds. Narration line 1 accompanies this command.</td></tr>
<tr><td>First output</td><td>Use one square callout around the policy-rule line, then separate arrows to q, username and host with their actual alert IDs. One focus per eight-second proof window. Attach narration line 2 when the proof is fully displayed.</td></tr>
<tr><td>Decision / completion</td><td>Attach narration line 3 to the proof B or verified PASS frame; remove previous arrows immediately on screen or pane changes. Trim UI click handles and scanning waits.</td></tr>
<tr><td>Synchronization</td><td>Use `logs/preflight-step-01.log`, `logs/recorded-step-01.log`, raw proof, the actual take ID and editor timecodes. A normalized mismatch is a retake, not an edit-away problem.</td></tr>
</table>
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo1/logs/preflight-step-01.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence: 94%. This is not a claimed runtime pass; a completed same-evidence take and corre
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Step 2 — Validate reflected XSS in the correct context

<details>
<summary><b>Open step 2 — command, real expected fields and role instructions</b></summary>


### The small problem to solve

The `name` input appears in an HTML element, an attribute and a JavaScript string. The right test changes with the output context.

**Learning focus:** Test context-specific reflected XSS *(EO1b)*

### Where to go


**Required directory navigation:** Open VS Code integrated Terminal manually. Do not browse through folders in Finder or type a relative path. Paste this complete command and press Enter before running the named step:

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf"
```

**Branch:** `m1-demo1-before` (complete any deliberately missing student source first). The separate `./steps/02-*.sh` command below is the only on-camera execution for this step.

**Remain in VS Code.** Open `runtime/app/main.py` at the `greet` endpoint (approximately lines 257–277). In its integrated Terminal run `./scripts/show_code.sh xss` to see the source fragment.

### Run this exact command

**Where to type it:** the same VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`.

```bash
./steps/02-verify-reflected-xss-contexts.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>HTML body</b></td><td><code>&lt;p&gt;Hello zzMARKzz</code></td><td>Inspect the body sink</td></tr>
<tr><td><b>HTML attribute</b></td><td><code>value="zzMARKzz"</code></td><td>Inspect the quoted attribute sink</td></tr>
<tr><td><b>JavaScript string</b></td><td><code>var greeting = "zzMARKzz"</code></td><td>Inspect the JavaScript string sink</td></tr>
<tr><td><b>Alert</b></td><td><code>Cross Site Scripting (Reflected)</code></td><td>Look for the named ZAP alert</td></tr>
<tr><td><b>Affected parameter</b></td><td><code>name</code></td><td>Confirm the input</td></tr>
<tr><td><b>Payload ZAP injected</b></td><td><code>&lt;actual injected payload&gt;</code></td><td>Use the real payload from this run</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS ZAP confirmed reflected XSS on name</code></td><td>A real payload and reflected evidence are required</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

The first three lines map the input to three output contexts. ZAP then attempts a context-specific payload and reports the affected parameter and evidence; raw reflection alone is not proof of executable script in a browser.

**How this connects:** Next, move from output encoding to a state-changing request that depends on CSRF session ownership.

### Recorder — execute and show

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/> Exact Screen And Timing</summary>
<table>
<tr><th>Relative Footage</th><th>Required Screen / Action</th></tr>
<tr><td>Source context · 00:00–00:08</td><td>VS Code: Cmd+P → runtime/app/main.py, Cmd+G → 257–277, inspect greet(). Terminal: ./scripts/show_code.sh xss. ZAP's recorded finding is for the name parameter on /greet.</td></tr>
<tr><td>Command · next 8 seconds</td><td>Show the full command above from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf` at readable zoom, keep the pointer away from key text and press Enter once.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Box the three response contexts one at a time and then show the actual affected parameter name.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Put an arrow on the scanner's injected payload and the response evidence. Distinguish detected exploitability from unfilmed browser execution.</td></tr>
<tr><td>Completion · 6–8 seconds</td><td>Hold the actual PASS line or stop on FAIL. Capture the exact console output and screen/take timestamp. Do not leave any single proof frame static more than 10 seconds.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-Purple-d946ef"/> Exact ElevenLabs Narration</summary>
<table><tr><th>Visual Reveal</th><th>Spoken Words — Copy Exactly After Verifying Proof</th><th>Count</th></tr>
<tr><td>00:00–00:08 · command</td><td>The name value appears in HTML, an attribute, and JavaScript. Each context changes the characters an attacker needs to escape.</td><td>20 spoken words</td></tr>
<tr><td>After execution · proof A</td><td>ZAP targets the name parameter using a context-matched payload. Read the actual injected value before judging the result.</td><td>18 spoken words</td></tr>
<tr><td>After execution · proof B</td><td>Now compare that payload with the reflected response evidence. Reflection alone is insufficient; the alert supplies the security finding.</td><td>19 spoken words</td></tr>
</table>
The lines are spoken sentences, not production notes. The second and third lines are recorded only if the named evidence is actually visible. If observed values change, revalidate the claims against the filmed take rather than adding invented numbers.
</details>

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/> Callouts, Cuts And Sync</summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>XSS context and ZAP request/response</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Payload ZAP injected</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Evidence (reflected in the response)</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>Reflection alone is not browser execution</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Edit Point</th><th>Exact Action</th></tr>
<tr><td>Command entrance</td><td>Clean cut after source context; frame the entire named command with a subtle square or underline for ≤8 seconds. Narration line 1 accompanies this command.</td></tr>
<tr><td>First output</td><td>Three short squares for body, attribute and JavaScript, then cut to a two-column callout over payload and evidence. Never highlight all fields simultaneously. Attach narration line 2 when the proof is fully displayed.</td></tr>
<tr><td>Decision / completion</td><td>Attach narration line 3 to the proof B or verified PASS frame; remove previous arrows immediately on screen or pane changes. Trim UI click handles and scanning waits.</td></tr>
<tr><td>Synchronization</td><td>Use `logs/preflight-step-02.log`, `logs/recorded-step-02.log`, raw proof, the actual take ID and editor timecodes. A normalized mismatch is a retake, not an edit-away problem.</td></tr>
</table>
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo1/logs/preflight-step-02.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence: 93%. This is not a claimed runtime pass; a completed same-evidence take and corre
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Step 3 — Replay a CSRF token across two sessions

<details>
<summary><b>Open step 3 — command, real expected fields and role instructions</b></summary>


### The small problem to solve

A token check can exist yet fail if the server accepts a token from one person's session with another person's cookie.

**Learning focus:** Exercise CSRF bypass conditions in the email-change workflow *(EO1c)*

### Where to go


**Required directory navigation:** Open VS Code integrated Terminal manually. Do not browse through folders in Finder or type a relative path. Paste this complete command and press Enter before running the named step:

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf"
```

**Branch:** `m1-demo1-before` (complete any deliberately missing student source first). The separate `./steps/03-*.sh` command below is the only on-camera execution for this step.

**Remain in VS Code.** Open `runtime/app/main.py` at `change_email` and the token-issuing helper. In the integrated Terminal run `./scripts/show_code.sh csrf` before running the security step.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`.

```bash
./steps/03-test-cross-session-csrf-token.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Valid token, session B</b></td><td><code>200</code></td><td>Legitimate control accepted</td></tr>
<tr><td><b>Missing token</b></td><td><code>403</code></td><td>Missing-token control rejected</td></tr>
<tr><td><b>Before cross-session request</b></td><td><code>alice@globomantics.example</code></td><td>Check actual stored state</td></tr>
<tr><td><b>Session A token with B cookie</b></td><td><code>200 (should be rejected)</code></td><td>Spot the cross-session bypass</td></tr>
<tr><td><b>After cross-session request</b></td><td><code>attacker@evil.example</code></td><td>State actually changed</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS token was accepted across sessions</code></td><td>Proof requires status AND changed email</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

Controls show the application is checking for a token. The cross-session request nevertheless succeeds and changes the victim's stored email, showing the token is not adequately associated with its issuing session.

**How this connects:** The final step reconciles these observations with the alerts and records an actionable disposition.

### Recorder — execute and show

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/> Exact Screen And Timing</summary>
<table>
<tr><th>Relative Footage</th><th>Required Screen / Action</th></tr>
<tr><td>Source context · 00:00–00:08</td><td>VS Code: Cmd+P → runtime/app/main.py, Cmd+G → 326–337, show the ownership-check branch. Terminal: ./scripts/show_code.sh csrf.</td></tr>
<tr><td>Command · next 8 seconds</td><td>Show the full command above from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf` at readable zoom, keep the pointer away from key text and press Enter once.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Highlight valid 200 and missing-token 403 as the two controls, one at a time.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Highlight cross-session 200 and the changed email. Keep session labels A and B readable; do not display token secrets.</td></tr>
<tr><td>Completion · 6–8 seconds</td><td>Hold the actual PASS line or stop on FAIL. Capture the exact console output and screen/take timestamp. Do not leave any single proof frame static more than 10 seconds.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-Purple-d946ef"/> Exact ElevenLabs Narration</summary>
<table><tr><th>Visual Reveal</th><th>Spoken Words — Copy Exactly After Verifying Proof</th><th>Count</th></tr>
<tr><td>00:00–00:08 · command</td><td>Alice’s own token succeeds, while the missing-token request is denied. Those two controls establish that token checking is enabled.</td><td>19 spoken words</td></tr>
<tr><td>After execution · proof A</td><td>Next, a token issued to Mallory is submitted with Alice’s session cookie. That request should be rejected, but returns two hundred.</td><td>21 spoken words</td></tr>
<tr><td>After execution · proof B</td><td>Alice’s stored email then changes. The server checked token existence, not session ownership, so the cross-session forgery succeeded.</td><td>18 spoken words</td></tr>
</table>
The lines are spoken sentences, not production notes. The second and third lines are recorded only if the named evidence is actually visible. If observed values change, revalidate the claims against the filmed take rather than adding invented numbers.
</details>

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/> Callouts, Cuts And Sync</summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>CSRF session state and changed email</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>token from session A, submitted with session B's cookie</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>session B's email after the cross-session request</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>CSRF token must be tied to session ownership</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Edit Point</th><th>Exact Action</th></tr>
<tr><td>Command entrance</td><td>Clean cut after source context; frame the entire named command with a subtle square or underline for ≤8 seconds. Narration line 1 accompanies this command.</td></tr>
<tr><td>First output</td><td>Blue rectangles over two control status lines, then one high-contrast rectangle over cross-session 200 and an arrow to the email mutation. Cut before values become stale. Attach narration line 2 when the proof is fully displayed.</td></tr>
<tr><td>Decision / completion</td><td>Attach narration line 3 to the proof B or verified PASS frame; remove previous arrows immediately on screen or pane changes. Trim UI click handles and scanning waits.</td></tr>
<tr><td>Synchronization</td><td>Use `logs/preflight-step-03.log`, `logs/recorded-step-03.log`, raw proof, the actual take ID and editor timecodes. A normalized mismatch is a retake, not an edit-away problem.</td></tr>
</table>
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo1/logs/preflight-step-03.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence: 96%. This is not a claimed runtime pass; a completed same-evidence take and corre
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Step 4 — Reconcile the findings with application behavior

<details>
<summary><b>Open step 4 — command, real expected fields and role instructions</b></summary>


### The small problem to solve

The team must not ship an alert list that lacks reproducible evidence for each stated vulnerability.

**Learning focus:** Apply the three security checks to a final engineering disposition *(EO1a · EO1b · EO1c)*

### Where to go


**Required directory navigation:** Open VS Code integrated Terminal manually. Do not browse through folders in Finder or type a relative path. Paste this complete command and press Enter before running the named step:

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf"
```

**Branch:** `m1-demo1-before` (complete any deliberately missing student source first). The separate `./steps/04-*.sh` command below is the only on-camera execution for this step.

**Use VS Code with integrated Terminal.** Keep `runtime/app/main.py` open. Read the student disposition template at `docs/alert-disposition-template.md` from the repository root. Return to the demo Terminal before running the step.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`.

```bash
./steps/04-reconcile-security-alerts.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>SQL injection 40018 · /search</b></td><td><code>confirmed — DB error: &lt;actual SQL error&gt;</code></td><td>Request/response supports SQL issue</td></tr>
<tr><td><b>NoSQL injection 40033 · /api/account</b></td><td><code>confirmed — accounts &lt;before&gt; → &lt;after&gt;</code></td><td>Operator injection affects record count</td></tr>
<tr><td><b>Command injection 90020/90037 · /admin/ping</b></td><td><code>confirmed — OS command ran: &lt;actual bytes&gt;</code></td><td>Also inspect the injected host request; a normal ping is insufficient</td></tr>
<tr><td><b>XSS reflected · /greet</b></td><td><code>confirmed — unencoded reflection</code></td><td>Confirm actual injected payload and response evidence</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS all four findings reconciled with app behavior</code></td><td>Check the evidence before disposition</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

A raw rule ID is a lead; its actual request and application effect support the engineer's final decision. Do not use routine ping output alone as proof of shell-command injection.

**How this connects:** The investigation closes with documented findings that can be reviewed rather than mere scanner severity labels.

### Recorder — execute and show

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/> Exact Screen And Timing</summary>
<table>
<tr><th>Relative Footage</th><th>Required Screen / Action</th></tr>
<tr><td>Source context · 00:00–00:08</td><td>VS Code: inspect runtime/app/main.py for search, account, admin_ping and greet. Open docs/alert-disposition-template.md for the student record. Run the named step in integrated terminal.</td></tr>
<tr><td>Command · next 8 seconds</td><td>Show the full command above from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf` at readable zoom, keep the pointer away from key text and press Enter once.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Show SQL parse error and NoSQL count difference; these are independent effects.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Show the XSS reflection and command rule. The script's normal ping evidence is insufficient alone; open the original injected request if narrating command execution.</td></tr>
<tr><td>Completion · 6–8 seconds</td><td>Hold the actual PASS line or stop on FAIL. Capture the exact console output and screen/take timestamp. Do not leave any single proof frame static more than 10 seconds.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-Purple-d946ef"/> Exact ElevenLabs Narration</summary>
<table><tr><th>Visual Reveal</th><th>Spoken Words — Copy Exactly After Verifying Proof</th><th>Count</th></tr>
<tr><td>00:00–00:08 · command</td><td>The SQL error and changing MongoDB account count show two different unsafe data paths, beyond merely reading scanner labels.</td><td>19 spoken words</td></tr>
<tr><td>After execution · proof A</td><td>The reflected marker confirms unencoded output. A normal ping does not prove shell injection, so inspect the original injected host request.</td><td>21 spoken words</td></tr>
<tr><td>After execution · proof B</td><td>Record only findings whose observed behavior supports the diagnosis. An alert disposition must be defensible when another engineer reviews it.</td><td>20 spoken words</td></tr>
</table>
The lines are spoken sentences, not production notes. The second and third lines are recorded only if the named evidence is actually visible. If observed values change, revalidate the claims against the filmed take rather than adding invented numbers.
</details>

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/> Callouts, Cuts And Sync</summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Final alert disposition with supporting application evidence</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>40018 SQL injection · /search</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>40033 NoSQL injection · /api/account</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>No disposition from alert count alone</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Edit Point</th><th>Exact Action</th></tr>
<tr><td>Command entrance</td><td>Clean cut after source context; frame the entire named command with a subtle square or underline for ≤8 seconds. Narration line 1 accompanies this command.</td></tr>
<tr><td>First output</td><td>Highlight SQL error, MongoDB count, XSS reflection and the injected-command proof in separate eight-second cuts. Never add a simulated shell payload to the screen. Attach narration line 2 when the proof is fully displayed.</td></tr>
<tr><td>Decision / completion</td><td>Attach narration line 3 to the proof B or verified PASS frame; remove previous arrows immediately on screen or pane changes. Trim UI click handles and scanning waits.</td></tr>
<tr><td>Synchronization</td><td>Use `logs/preflight-step-04.log`, `logs/recorded-step-04.log`, raw proof, the actual take ID and editor timecodes. A normalized mismatch is a retake, not an edit-away problem.</td></tr>
</table>
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo1/logs/preflight-step-04.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence: 88%. This is not a claimed runtime pass; a completed same-evidence take and corre
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Finish the recording

1. Capture all four real step outcomes, their matching raw logs and GUI/CI evidence; preserve the recorded branch SHA
2. Stop the lab from the same demo folder: `./scripts/demo_down.sh`
3. Hand the video takes to the Editor and the Developer's generated narration draft and logs to the Narrator
4. Leave the developer-wide batch validation and its configuration in the landing page, not in this per-demo recording page

<!-- demo-navigation:start -->
<p align="center"><b>Author production guide · Demo 1 of 6</b></p>
<p align="center">
  <a href="README.md"><img alt="All author production guides" src="https://img.shields.io/badge/%E2%86%90_Back_to-All_Demos-585FA2?style=for-the-badge"></a>
  <a href="m1-demo2.md"><img alt="Next author guide: Module 1 Demo 2 — JavaScript HTTP Sender" src="https://img.shields.io/badge/Next_%E2%86%92-M1_Demo_2-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->
