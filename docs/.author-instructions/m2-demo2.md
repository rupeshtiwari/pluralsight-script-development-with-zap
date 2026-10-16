# Module 2 · Demo 2 — ZAP API and Insights · Production guide

<div align="center">

![Recorder](https://img.shields.io/badge/RECORDER-Actual_Screens-00A3FF?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-Clean_Callouts-02E088?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-ElevenLabs-770EF7?style=for-the-badge)

<img src="../learner-diagrams/m2-demo2-architecture.svg" width="100%" alt="Demo 2 — ZAP API and Insights component diagram"/>
<sub>Illustrative architecture · Generated using ChatGPT · Temporary PUBLIC production material</sub>

</div>

[← Production dashboard](README.md) · [Open student's Module 2 demo README](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo2-before/demos/module2-demos/m2-demo2-zap-api-scan-evidence/README.md)

<!-- demo-navigation:start -->
<p align="center"><b>Author production guide · Demo 5 of 6</b></p>
<p align="center">
  <a href="m2-demo1.md"><img alt="Previous author guide: Module 2 Demo 1 — Authenticated ZAP in GitHub Actions" src="https://img.shields.io/badge/%E2%86%90_Previous-M2_Demo_1-130F25?style=for-the-badge"></a>
  <a href="m2-demo3.md"><img alt="Next author guide: Module 2 Demo 3 — Security quality gates" src="https://img.shields.io/badge/Next_%E2%86%92-M2_Demo_3-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->

## Recording assignment

**Record the `m2-demo2-before` branch**, completing the missing plan where applicable, and keep source changes traceable. The Developer runs the **one combined batch preflight before the recording team starts** and distributes `deliverables/m2-demo2/`: commands, verified logs, generated HTML and narration drafts.

**Off-camera preparation:** from the existing checkout root run `git switch m2-demo2-before`, then `cd demos/module2-demos/m2-demo2-zap-api-scan-evidence`, then `./scripts/demo_up.sh`. Check the local application at `http://localhost:8000/`. Confirm the lesson source/plan is ready before testing. One-time Mac preparation and the batch command live **only on the author dashboard**; do not repeat them during recorded steps.

**Recording sequence:** show code or GUI context, display exact command and its key parameters for about 8 seconds, execute once, then reveal real output in 6–8-second proof windows; show real GitHub Actions job and report where the LO requires hosted proof. The Editor cuts waiting and focus changes cleanly.

## Four fixed teaching steps

## Step 1 — Ask the API whether the scan finished

<details open>
<summary><b>Open step 1 — where, command, output and production roles</b></summary>


### The specific problem

The API can be available while the active scan is incomplete.

**What you are learning:** Query machine-readable scan status *(EO3b)*

### Which application and screen?


**Required directory navigation:** Open macOS Terminal manually. Do not browse through folders in Finder or type a relative path. Paste this complete command and press Enter before running the named step:

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module2-demos/m2-demo2-zap-api-scan-evidence"
```

**Branch:** `m2-demo2-before` (complete any deliberately missing student source first). The separate `./steps/01-*.sh` command below is the only on-camera execution for this step.

**Open macOS Terminal**, enter the demo folder, and inspect ZAP API endpoints used by `scripts/_steps.sh` when needed. No GUI is required for this step.

### Run this exact command

**Where:** macOS Terminal. **Current folder:** `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/01-check-zap-scan-status.sh
```

### Expected output and what it means

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>ZAP runtime (GET core/view/version)</b></td><td><code>2.17.0</code></td><td>Scanner version</td></tr>
<tr><td><b>Active scan (GET ascan/view/scans)</b></td><td><code>id=&lt;live scan ID&gt; · progress=100% · state=FINISHED</code></td><td>Complete scan, not merely open API</td></tr>
<tr><td><b>Requests the scan sent</b></td><td><code>&lt;live count&gt;</code></td><td>Actual telemetry may differ</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS API reports finished scan</code></td><td>Machine-readable readiness</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### How to interpret this result

The version confirms which engine generated the findings. Progress and finished status tell an automated consumer when scan results are ready.

**How the investigation advances:** Retrieve the one custom alert rather than treating every scanner finding as equivalent.

### Recorder — screen and timing

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>Terminal: show GET core/view/version and GET ascan/view/scans in scripts/_steps.sh; then full named command</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/01-check-zap-scan-status.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Box version 2.17.0 first</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Move callout to FINISHED and 100%; do not narrate a guessed request count</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

### Narrator — spoken lines

<details><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Query ZAP's version and scan status before processing any finding. An accessible engine does not prove the assessment finished.</td><td>19</td></tr>
<tr><td>Actual output A</td><td>The API reports full progress and a finished scan. These are machine-readable conditions the pipeline can wait for.</td><td>18</td></tr>
<tr><td>Actual output B</td><td>Request counts vary, so read the actual raw measurement. Never invent the count from an unrelated successful run.</td><td>18</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

### Editor — highlights and cuts

<details><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Live API runtime and scan state</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>ZAP runtime  (GET core/view/version)</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Active scan  (GET ascan/view/scans)</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>Query the scanner you actually ran</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>Square the version, then arrow to FINISHED. Keep separate proof frames, each six to eight seconds. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-01.log` and `logs/recorded-step-01.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

### Validation and confidence

- **Proof:** Compare filmed output against the Developer's actual `deliverables/m2-demo2/logs/preflight-step-01.log`, plus the matching live GUI or GitHub Actions artifact
- **Learning:** Validate the purpose and mechanism above; a command-only video does not meet the objective
- **Source review:** Source-review confidence: 95%. Do not inflate scores simply because documentation exists; release requires actua
- **Final release:** Do not invent an alert or inflate confidence. Unsupported GUI/CI steps remain explicitly NOT VERIFIED until corrected

</details>

## Step 2 — Query the custom rule's risk and confidence

<details>
<summary><b>Open step 2 — where, command, output and production roles</b></summary>


### The specific problem

A count of twenty alerts is not actionable without rule identity and affected parameter.

**What you are learning:** Retrieve a specific scanner finding through the API *(EO3b)*

### Which application and screen?


**Required directory navigation:** Open macOS Terminal manually. Do not browse through folders in Finder or type a relative path. Paste this complete command and press Enter before running the named step:

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module2-demos/m2-demo2-zap-api-scan-evidence"
```

**Branch:** `m2-demo2-before` (complete any deliberately missing student source first). The separate `./steps/02-*.sh` command below is the only on-camera execution for this step.

**Remain in macOS Terminal**. The command queries `core/view/alerts` using the authenticated profile URL. Inspect the response fields printed by the step.

### Run this exact command

**Where:** macOS Terminal. **Current folder:** `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/02-query-custom-rule-alert.sh
```

### Expected output and what it means

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>Rule identity (pluginId · alert)</b></td><td><code>50000 · Globomantics unsafe reflection (custom rule)</code></td><td>Script-generated finding</td></tr>
<tr><td><b>Disposition (risk · confidence)</b></td><td><code>Medium · Medium</code></td><td>Risk versus evidence strength</td></tr>
<tr><td><b>Parameter</b></td><td><code>note</code></td><td>Profile input</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS API returns custom alert</code></td><td>Named rule must be present</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### How to interpret this result

Rule ID and name distinguish the application-specific Jython finding from built-in XSS. Risk and confidence are separate fields that a pipeline can reason about.

**How the investigation advances:** Verify the officially generated report contains that same finding.

### Recorder — screen and timing

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>Terminal: scripts/_steps.sh core/view/alerts with authenticated baseurl; show script-generated record after step</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/02-query-custom-rule-alert.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Box pluginId and complete custom name</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Show risk versus confidence as separate concepts and point to note parameter</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

### Narrator — spoken lines

<details><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Read the authenticated alert using ZAP's API. The custom rule identity distinguishes the finding from a built-in XSS result.</td><td>19</td></tr>
<tr><td>Actual output A</td><td>Risk describes severity; confidence describes certainty of evidence. The reported finding is rated Medium on both dimensions.</td><td>17</td></tr>
<tr><td>Actual output B</td><td>The note parameter identifies the tested input. This is the specific evidence a release gate can evaluate.</td><td>17</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

### Editor — highlights and cuts

<details><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>API alert and scope</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Rule identity  (pluginId · alert)</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Disposition  (risk · confidence)</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>Risk and confidence answer different questions</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>Rectangle rule ID, then risk and confidence labels, then note, with each old highlight cleared. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-02.log` and `logs/recorded-step-02.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

### Validation and confidence

- **Proof:** Compare filmed output against the Developer's actual `deliverables/m2-demo2/logs/preflight-step-02.log`, plus the matching live GUI or GitHub Actions artifact
- **Learning:** Validate the purpose and mechanism above; a command-only video does not meet the objective
- **Source review:** Source-review confidence: 95%. Do not inflate scores simply because documentation exists; release requires actua
- **Final release:** Do not invent an alert or inflate confidence. Unsupported GUI/CI steps remain explicitly NOT VERIFIED until corrected

</details>

## Step 3 — Compare the JSON report with the API result

<details>
<summary><b>Open step 3 — where, command, output and production roles</b></summary>


### The specific problem

If the stored JSON disagrees with the current API, it cannot support a reliable release decision.

**What you are learning:** Generate and reconcile an official security report *(EO3b)*

### Which application and screen?


**Required directory navigation:** Open macOS Terminal manually. Do not browse through folders in Finder or type a relative path. Paste this complete command and press Enter before running the named step:

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module2-demos/m2-demo2-zap-api-scan-evidence"
```

**Branch:** `m2-demo2-before` (complete any deliberately missing student source first). The separate `./steps/03-*.sh` command below is the only on-camera execution for this step.

**Remain in macOS Terminal**. Inspect the official `reports/action/generate` request and `traditional-json` report type used by the script.

### Run this exact command

**Where:** macOS Terminal. **Current folder:** `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/03-reconcile-json-report.sh
```

### Expected output and what it means

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>Report template</b></td><td><code>traditional-json</code></td><td>Official ZAP report type</td></tr>
<tr><td><b>Report alert (pluginid · name)</b></td><td><code>50000 · Globomantics unsafe reflection (custom rule)</code></td><td>Same rule as live API</td></tr>
<tr><td><b>Report rating (riskdesc)</b></td><td><code>Medium (Medium)</code></td><td>Risk and confidence same as Step 2</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS JSON report reconciled with API</code></td><td>Archived and live evidence agree</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### How to interpret this result

The generated report preserves the named custom finding in a shareable format. Matching its identity and rating against the API prevents stale-report assumptions.

**How the investigation advances:** Inspect the scan's operational quality in addition to the vulnerability result.

### Recorder — screen and timing

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>Terminal: show reports/action/generate and template traditional-json in scripts/_steps.sh; then run named step</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/03-reconcile-json-report.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Highlight traditional-json report template and rule ID</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Arrow from report riskdesc Medium (Medium) to earlier API risk and confidence fields</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

### Narrator — spoken lines

<details><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Generate ZAP's official JSON report, instead of writing an unverified summary. The template produces an archivable finding record.</td><td>18</td></tr>
<tr><td>Actual output A</td><td>The report contains the same custom rule name and plugin identity returned by the live API.</td><td>16</td></tr>
<tr><td>Actual output B</td><td>Its risk and confidence match the API response. The release team can now reconcile the archived report with scanner evidence.</td><td>20</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

### Editor — highlights and cuts

<details><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Official traditional-json report</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Report alert  (pluginid · name)</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Report rating  (riskdesc)</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>Reconcile report identity with API, do not substitute stale JSON</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>Small box on report name and riskdesc, then remove it at the next focus. Do not show fake report contents. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-03.log` and `logs/recorded-step-03.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

### Validation and confidence

- **Proof:** Compare filmed output against the Developer's actual `deliverables/m2-demo2/logs/preflight-step-03.log`, plus the matching live GUI or GitHub Actions artifact
- **Learning:** Validate the purpose and mechanism above; a command-only video does not meet the objective
- **Source review:** Source-review confidence: 95%. Do not inflate scores simply because documentation exists; release requires actua
- **Final release:** Do not invent an alert or inflate confidence. Unsupported GUI/CI steps remain explicitly NOT VERIFIED until corrected

</details>

## Step 4 — Read the report's scan-effectiveness Insights

<details>
<summary><b>Open step 4 — where, command, output and production roles</b></summary>


### The specific problem

A scan might appear clean because it encountered an authentication, scope or execution problem.

**What you are learning:** Interpret operational findings exposed with the scan report *(EO3b)*

### Which application and screen?


**Required directory navigation:** Open macOS Terminal manually. Do not browse through folders in Finder or type a relative path. Paste this complete command and press Enter before running the named step:

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module2-demos/m2-demo2-zap-api-scan-evidence"
```

**Branch:** `m2-demo2-before` (complete any deliberately missing student source first). The separate `./steps/04-*.sh` command below is the only on-camera execution for this step.

**Remain in macOS Terminal**. Locate the actual `insights[]` entries returned by the report extraction, with the key and explanation readable.

### Run this exact command

**Where:** macOS Terminal. **Current folder:** `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/04-read-zap-insights.sh
```

### Expected output and what it means

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>Insight (level · key)</b></td><td><code>&lt;actual level&gt; · &lt;actual insight key&gt;</code></td><td>Must be from nonempty insights[]</td></tr>
<tr><td><b>Statistic · meaning</b></td><td><code>&lt;actual value&gt; · &lt;real description&gt;</code></td><td>Scan-effectiveness evidence</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS report Insights returned</code></td><td>Do not substitute unrelated counters</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### How to interpret this result

Insights describe scan behavior and confidence in coverage, not only vulnerability risk. A missing Insights section is a reason to investigate, not something to invent or ignore.

**How the investigation advances:** The four fields now support a programmatic, evidence-backed scan assessment.

### Recorder — screen and timing

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>Terminal: report insights[] extraction, show an actual nonempty insight key and explanation; run named step</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/04-read-zap-insights.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Box the actual insight level and key, as printed on this run</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Point to statistic and its meaning. If insights[] is empty, show FAIL instead of a substituted counter</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

### Narrator — spoken lines

<details><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Read ZAP's Insights to assess scan effectiveness, not the vulnerability severity of one finding.</td><td>14</td></tr>
<tr><td>Actual output A</td><td>The insight key names an operational condition, while its statistic and explanation show what happened during execution.</td><td>17</td></tr>
<tr><td>Actual output B</td><td>If the report lacks Insights, fail this evidence check. Ordinary statistics cannot substitute for missing scan-quality signals.</td><td>17</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

### Editor — highlights and cuts

<details><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>ZAP report Insights entries</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Insight  (level · key)</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Statistic · meaning</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>Insights show scan effectiveness, not a vulnerability alert</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>First square actual key, then arrow to explanatory field. Never narrate the placeholder values. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-04.log` and `logs/recorded-step-04.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

### Validation and confidence

- **Proof:** Compare filmed output against the Developer's actual `deliverables/m2-demo2/logs/preflight-step-04.log`, plus the matching live GUI or GitHub Actions artifact
- **Learning:** Validate the purpose and mechanism above; a command-only video does not meet the objective
- **Source review:** Source-review confidence: 90%. Do not inflate scores simply because documentation exists; release requires actua
- **Final release:** Do not invent an alert or inflate confidence. Unsupported GUI/CI steps remain explicitly NOT VERIFIED until corrected

</details>

## End the production take

Stop containers with `./scripts/demo_down.sh`, retain the before/after SHAs and proof, and deliver the take to the Editor. The Narrator uses the generated step transcripts plus the actual recorded output. Do not rerun the Developer's six-demo preflight in this per-demo process.

<!-- demo-navigation:start -->
<p align="center"><b>Author production guide · Demo 5 of 6</b></p>
<p align="center">
  <a href="m2-demo1.md"><img alt="Previous author guide: Module 2 Demo 1 — Authenticated ZAP in GitHub Actions" src="https://img.shields.io/badge/%E2%86%90_Previous-M2_Demo_1-130F25?style=for-the-badge"></a>
  <a href="m2-demo3.md"><img alt="Next author guide: Module 2 Demo 3 — Security quality gates" src="https://img.shields.io/badge/Next_%E2%86%92-M2_Demo_3-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->
