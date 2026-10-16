# Module 1 · Demo 2 — JavaScript HTTP Sender · Production guide

<div align="center">

![Recorder](https://img.shields.io/badge/RECORDER-Show_Real_Evidence-00A3FF?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-One_Highlight-02E088?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-ElevenLabs_Words-770EF7?style=for-the-badge)

<img src="../learner-diagrams/m1-demo2-architecture.svg" width="100%" alt="Training evidence flow for m1-demo2"/>
<sub>Illustrative architecture · Generated using ChatGPT · Temporary PUBLIC production material</sub>

</div>

[← Production dashboard](README.md) · [Open student's Module 1 demo README](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo2-before/demos/module1-demos/m1-demo2-javascript-http-sender/README.md)

## Recorder assignment

**Work only on `m1-demo2-before`**, completing missing exercise source where applicable. The Developer has already generated the batch preflight, saved four approved baseline transcripts and made the `deliverables/m1-demo2/` package available. **Do not rerun Mac setup or batch preflight as part of filming.** Read the [one-time setup and Developer responsibilities](README.md) on the author dashboard.

**Start privately before recording:** from repository root, `git switch m1-demo2-before`, then `cd demos/module1-demos/m1-demo2-javascript-http-sender`; start the vulnerable lab with `./scripts/demo_up.sh`. Confirm the app is reachable at `http://localhost:8000/`, and preserve all intended authored changes. Run commands from the specified VS Code integrated Terminal or macOS Terminal in the appropriate step.

**Recording order:** show source/context → display exact command for approximately 8 seconds → Enter once → show real output in 6–8-second proof windows → switch screens only as the current claim requires. The Editor trims long waits. A mismatched recording transcript is a retake, not a chance to create a fake PASS.

## Follow these four steps

## Step 1 — Load the JavaScript HTTP Sender script

<details open>
<summary><b>Open step 1 — command, real expected fields and role instructions</b></summary>


### The small problem to solve

A JavaScript file cannot modify traffic merely by existing in the repository.

**Learning focus:** Develop a JavaScript extension at the request-sending boundary *(EO2a)*

### Where to go

**Open VS Code.** Create or inspect `zap-scripts/globomantics-marker.js` in the demo directory. Locate `sendingRequest()`, `MARKER_HEADER`, `MARKER_VALUE` and `setHeader()`. Then open the VS Code integrated Terminal in this demo directory.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo2-javascript-http-sender`.

```bash
./steps/01-load-javascript-http-sender.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Script name</b></td><td><code>globomantics-marker (HTTP Sender · &lt;detected JavaScript engine&gt;)</code></td><td>Script registered in ZAP</td></tr>
<tr><td><b>Marker header it adds</b></td><td><code>X-Globomantics-Marker: GLOBO-DEMO</code></td><td>Exact header and value</td></tr>
<tr><td><b>Named console line it prints</b></td><td><code>[globo-marker] added X-Globomantics-Marker ... to &lt;url&gt;</code></td><td>Expected script print format</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS script is a valid HTTP Sender action and loaded</code></td><td>Script registered; traffic not yet proven</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

Loading and enabling a script is separate from sending an HTTP message. The output establishes script identity, type and intended modification only.

**How this connects:** Send a fresh request through ZAP to prove the hook executed.

### Recorder — execute and show

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

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Square `sendingRequest()` and `setHeader()`, then arrow to the marker-header value in the terminal. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-01.log</code> and <code>logs/recorded-step-01.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Load the JavaScript HTTP Sender script. Its sending request hook can change a message only after ZAP registers and enables it.</td><td>21</td></tr>
<tr><td>First actual output</td><td>The marker header has a fixed name and value. These parameters identify precisely what the hook will attach to traffic.</td><td>20</td></tr>
<tr><td>Second output / decision</td><td>The successful registration proves ZAP accepted the script. It does not yet prove an outbound request carried the header.</td><td>19</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo2/logs/preflight-step-01.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence 95%, before live rehearsal. An estimate below the owner's release threshold cannot
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Step 2 — Prove the marker on an outbound request

<details>
<summary><b>Open step 2 — command, real expected fields and role instructions</b></summary>


### The small problem to solve

Script registration does not prove that an HTTP request actually passed through the hook.

**Learning focus:** Verify observable request modification *(EO2a)*

### Where to go

**Open ZAP GUI** at `http://localhost:8080/zap/` in a browser. Select **History**, then the newest `/greet?name=marker-...` request, and open its **Request** panel. Use the VS Code integrated Terminal for the command.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo2-javascript-http-sender`.

```bash
./steps/02-prove-outbound-marker-header.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Outbound request</b></td><td><code>GET /greet?name=marker-&lt;live ID&gt; ...</code></td><td>Fresh message, not a prior run</td></tr>
<tr><td><b>Header added by the script</b></td><td><code>X-Globomantics-Marker: GLOBO-DEMO</code></td><td>Inspect Request panel and terminal</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS script added header to outgoing request</code></td><td>Real outbound traffic carries marker</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

The header in the actual ZAP-captured request proves the JavaScript hook modified traffic. Request identifiers may vary, while the marker name and value remain stable.

**How this connects:** Now establish that the script also printed its named console message.

### Recorder — execute and show

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

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Separate rectangles on request URL and header. Never highlight an earlier History entry. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-02.log</code> and <code>logs/recorded-step-02.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Send a fresh request through ZAP instead of directly to the store. The HTTP Sender hook runs only on proxied messages.</td><td>21</td></tr>
<tr><td>First actual output</td><td>The captured request contains the marker header and its fixed value. That is proof of an actual outbound modification.</td><td>19</td></tr>
<tr><td>Second output / decision</td><td>The request identifier changes on every execution, but the script's header and the technical result must remain consistent.</td><td>18</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo2/logs/preflight-step-02.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence 96%, before live rehearsal. An estimate below the owner's release threshold cannot
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Step 3 — Verify the live Script Console output

<details>
<summary><b>Open step 3 — command, real expected fields and role instructions</b></summary>


### The small problem to solve

A terminal can show a predicted console string without actually observing ZAP's Script Console.

**Learning focus:** Validate the script's emitted diagnostic output *(EO2a)*

### Where to go

**Keep ZAP GUI open** at `http://localhost:8080/zap/`. Open **Scripts → Script Console** and inspect fresh lines after the command. The command itself runs in the integrated Terminal.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo2-javascript-http-sender`.

```bash
./steps/03-check-live-script-console.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Expected format (terminal)</b></td><td><code>[globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to &lt;url&gt;</code></td><td>Terminal explicitly says expected format</td></tr>
<tr><td><b>Real Script Console</b></td><td><code>[globo-marker] ... to &lt;actual fresh request URL&gt;</code></td><td>MUST inspect in GUI; not captured by shell</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS fresh marked request; verify live console</code></td><td>Terminal PASS alone does not prove GUI print</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

Compare the expected print format with the new line that actually appears in ZAP Script Console. Do not confuse the shell's expected format with live script execution proof.

**How this connects:** Confirm the script remains registered and enabled in this ZAP session.

### Recorder — execute and show

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

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Use a short arrow from expected-format label to the real Script Console pane, then a rectangle on the live marker line. Do not simulate output. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-03.log</code> and <code>logs/recorded-step-03.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>Trigger a new request to make the JavaScript print its marker. The terminal displays the expected format, not the console itself.</td><td>21</td></tr>
<tr><td>First actual output</td><td>Open the live Script Console and find the fresh marker line. Match its URL to the request sent through ZAP.</td><td>20</td></tr>
<tr><td>Second output / decision</td><td>The console proves the script reported a real action. A copied expected line would not establish that behavior.</td><td>18</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo2/logs/preflight-step-03.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence 86%, before live rehearsal. An estimate below the owner's release threshold cannot
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Step 4 — Verify the script registration

<details>
<summary><b>Open step 4 — command, real expected fields and role instructions</b></summary>


### The small problem to solve

Reusable automation needs a stable named script and a verifiable enabled state.

**Learning focus:** Confirm configured JavaScript extension state *(EO2a)*

### Where to go

**Open ZAP GUI** → **Scripts → HTTP Sender → globomantics-marker**. Keep its name/type/engine visible. Then return to VS Code Terminal for the command.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo2-javascript-http-sender`.

```bash
./steps/04-verify-enabled-script-registration.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Registered name</b></td><td><code>globomantics-marker</code></td><td>Stable name reused by automation</td></tr>
<tr><td><b>Type</b></td><td><code>httpsender</code></td><td>Correct hook category</td></tr>
<tr><td><b>Enabled</b></td><td><code>true</code></td><td>Script active in current ZAP session</td></tr>
<tr><td><b>Path (repo)</b></td><td><code>zap-scripts/globomantics-marker.js</code></td><td>Current script source</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS script registered and enabled</code></td><td>Registration is ready for reuse</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

The script has a stable source path, a valid HTTP Sender type, and enabled registration. This is not a claim it persists after the container is destroyed.

**How this connects:** The demo finishes with source, modified request, console message and registration all independently observed.

### Recorder — execute and show

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

### Editor — callouts and cut plan

<details>
<summary><img src="https://img.shields.io/badge/EDITOR-Highlight_Map-16a34a"/></summary>
<table><tr><th>Transition</th><th>Precise edit</th></tr>
<tr><td>Code → command</td><td>Clean cut or clear pane switch; square over the important function or parameter, remove it immediately when focus moves to the full named command.</td></tr>
<tr><td>Command → proof</td><td>Sequential boxes on name, type and enabled, not all fields simultaneously. Keep each separate proof region for 6–8 seconds; never leave a static frame more than ten seconds.</td></tr>
<tr><td>Proof → conclusion</td><td>Move the callout to the PASS/alert confirmation and remove the prior one. Narration line 3 must accompany the verified result, not an example block.</td></tr>
<tr><td>Evidence parity</td><td>Compare <code>logs/preflight-step-04.log</code> and <code>logs/recorded-step-04.log</code> plus untouched raw proof under <code>logs/.producer/</code>. Mismatch is a retake, never a visual cover-up.</td></tr>
</table>
</details>

### Narrator — spoken evidence

<details>
<summary><img src="https://img.shields.io/badge/NARRATOR-ElevenLabs_Script-d946ef"/></summary>
<table><tr><th>Match To Screen</th><th>Exact words to speak</th><th>Words</th></tr>
<tr><td>Command shown</td><td>A reusable automation needs a stable script identity, not just one marked request. Inspect its registration before depending on it.</td><td>20</td></tr>
<tr><td>First actual output</td><td>The type identifies the HTTP Sender hook, and the enabled flag confirms ZAP can use that registered script.</td><td>18</td></tr>
<tr><td>Second output / decision</td><td>The source path provides a stable reference for automation. It does not promise persistence after the container is destroyed.</td><td>19</td></tr>
</table>
Only record a statement after the matching evidence is visible in the take. The script is written for natural ElevenLabs speech, not technical notes; do not read placeholder values or substitute terminal expectations for real GUI proof.
</details>

### Technical approval

- **Operator proof:** Match the actual field values against the Developer's `deliverables/m1-demo2/logs/preflight-step-04.log` and the same-take GUI evidence
- **Learning objective:** Confirm the specific problem and outcome described above were demonstrated, not just a command executed
- **Source confidence:** Source-review confidence 95%, before live rehearsal. An estimate below the owner's release threshold cannot
- **Release:** Missing or contradictory proof remains NOT VERIFIED; do not increase a score to 94% without evidence

</details>

## Finish the recording

1. Capture all four real step outcomes, their matching raw logs and GUI/CI evidence; preserve the recorded branch SHA
2. Stop the lab from the same demo folder: `./scripts/demo_down.sh`
3. Hand the video takes to the Editor and the Developer's generated narration draft and logs to the Narrator
4. Leave the developer-wide batch validation and its configuration in the landing page, not in this per-demo recording page

