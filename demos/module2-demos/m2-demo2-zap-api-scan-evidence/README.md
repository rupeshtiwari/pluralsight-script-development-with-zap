# Module 2 · Demo 2 — Query the ZAP API and evidence reports

<div align="center">

![Training](https://img.shields.io/badge/Globomantics-Authorized_Lab-130F25?style=for-the-badge)
![ZAP](https://img.shields.io/badge/OWASP_ZAP-API_Evidence-FF1675?style=for-the-badge)

<img src="../../../docs/learner-diagrams/m2-demo2-architecture.svg" width="100%" alt="Module 2 · Demo 2 — Query the ZAP API and evidence reports architecture"/>

<sub>Illustrative workflow · Generated using ChatGPT · Verify actual evidence in your own lab</sub>

</div>

<!-- demo-navigation:start -->
<p align="center"><b>Student exercise · Demo 5 of 6</b></p>
<p align="center">
  <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo1-before/demos/module2-demos/m2-demo1-authenticated-zap-github-actions/README.md"><img alt="Previous student demo: Module 2 Demo 1 — Authenticated ZAP in GitHub Actions" src="https://img.shields.io/badge/%E2%86%90_Previous-M2_Demo_1-130F25?style=for-the-badge"></a>
  <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo3-before/demos/module2-demos/m2-demo3-security-quality-gates/README.md"><img alt="Next student demo: Module 2 Demo 3 — Security quality gates" src="https://img.shields.io/badge/Next_%E2%86%92-M2_Demo_3-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->

## Your Scenario

You need machine-readable evidence from a completed authenticated Store scan. An alert count or screenshot cannot tell your release process whether it is reading the right engine, finding and report.

**Your practical goal:** I will guide you through four API evidence checks: runtime and scan status, the named custom alert, the official JSON report and report-owned Insights. You will compare the actual fields rather than assume different artifacts agree.

## Your Learning Goals

You will retrieve four kinds of evidence from ZAP programmatically:

- Query scan status and findings using the official ZAP API *(EO3b)*
- Reconcile the API's named custom rule with a generated JSON report and actual Insights about scan effectiveness *(EO3b)*

You do not need the separate course outline to understand the objective or follow the exercises.

## Your Evidence Path

```mermaid
flowchart LR
  S1["Check completion"]
  S2["Inspect custom alert"]
  S3["Reconcile JSON"]
  S4["Check Insights"]
  S1 --> S2
  S2 --> S3
  S3 --> S4
```

## Start Your Lab

Mac dependencies are prepared **once for the course** using `setup/setup-macos.sh`, as shown in the [course README](../../../README.md). Each demo must then start its **own local training stack**:

<details open>
<summary><b>Open the exact branch and start Module 2 Demo 2</b></summary>

**Where:** macOS Terminal or VS Code integrated Terminal, from the root of your existing Git checkout.

```bash
cd "$HOME/pluralsight-script-development-with-zap"
git fetch origin
git switch m2-demo2-before
cd demos/module2-demos/m2-demo2-zap-api-scan-evidence
./scripts/demo_up.sh
```

**Expected start:** healthy Globomantics, Postgres, MongoDB, and ZAP services, reported by the startup script. If they are not ready, stop and inspect the actual output before proceeding.

**URLs:** [Training application](http://localhost:8000/) · [ZAP GUI](http://localhost:8080/zap/) · [ZAP API and proxy](http://localhost:8090/). This independent exercise provisions its own authenticated scanning prerequisites, so you do not need to run another demonstration first.

</details>

## Your Four Steps

<details open>
<summary><b>Step 1 — Ask the API whether the scan finished</b> · Check completion</summary>

### Learning Goal

The API can be available while the active scan is incomplete.

**What you are learning:** Query machine-readable scan status *(EO3b)*

### Demo Workspace

**Open macOS Terminal**, enter the demo folder, and inspect ZAP API endpoints used by `scripts/_steps.sh` when needed. No GUI is required for this step.

<!-- student-location:start -->
**Run in:** macOS Terminal.

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module2-demos/m2-demo2-zap-api-scan-evidence"
```
<!-- student-location:end -->

### Run Command

**Where:** macOS Terminal. **Current folder:** `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/01-check-zap-scan-status.sh
```

<!-- student-proof:start -->
**Where your result appears:** Stay in the same terminal after the command. No ZAP GUI switch is required for the API status proof.

**Inspect this evidence:** Current engine version, active scan identity and actual completed progress/state.
<!-- student-proof:end -->

### Expected Results

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>ZAP runtime (GET core/view/version)</b></td><td><code>2.17.0</code></td><td>Scanner version</td></tr>
<tr><td><b>Active scan (GET ascan/view/scans)</b></td><td><code>id=&lt;live scan ID&gt; · progress=100% · state=FINISHED</code></td><td>Complete scan, not merely open API</td></tr>
<tr><td><b>Requests the scan sent</b></td><td><code>&lt;live count&gt;</code></td><td>Actual telemetry may differ</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS API reports finished scan</code></td><td>Machine-readable readiness</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### Interpret Results

The version confirms which engine generated the findings. Progress and finished status tell an automated consumer when scan results are ready.

**How the investigation advances:** Retrieve the one custom alert rather than treating every scanner finding as equivalent.

</details>

<details>
<summary><b>Step 2 — Query the custom rule's risk and confidence</b> · Inspect custom alert</summary>

### Learning Goal

A count of twenty alerts is not actionable without rule identity and affected parameter.

**What you are learning:** Retrieve a specific scanner finding through the API *(EO3b)*

### Demo Workspace

**Remain in macOS Terminal**. The command queries `core/view/alerts` using the authenticated profile URL. Inspect the response fields printed by the step.

<!-- student-location:start -->
**Run in:** macOS Terminal.

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module2-demos/m2-demo2-zap-api-scan-evidence"
```
<!-- student-location:end -->

### Run Command

**Where:** macOS Terminal. **Current folder:** `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/02-query-custom-rule-alert.sh
```

<!-- student-proof:start -->
**Where your result appears:** Stay in the same terminal. Show the API query context and custom alert fields; inspect raw JSON only when teaching its structure.

**Inspect this evidence:** Custom plugin identity, affected parameter, risk and confidence as distinct fields.
<!-- student-proof:end -->

### Expected Results

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>Rule identity (pluginId · alert)</b></td><td><code>50000 · Globomantics unsafe reflection (custom rule)</code></td><td>Script-generated finding</td></tr>
<tr><td><b>Disposition (risk · confidence)</b></td><td><code>Medium · Medium</code></td><td>Risk versus evidence strength</td></tr>
<tr><td><b>Parameter</b></td><td><code>note</code></td><td>Profile input</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS API returns custom alert</code></td><td>Named rule must be present</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### Interpret Results

Rule ID and name distinguish the application-specific Jython finding from built-in XSS. Risk and confidence are separate fields that a pipeline can reason about.

**How the investigation advances:** Verify the officially generated report contains that same finding.

</details>

<details>
<summary><b>Step 3 — Compare the JSON report with the API result</b> · Reconcile JSON</summary>

### Learning Goal

If the stored JSON disagrees with the current API, it cannot support a reliable release decision.

**What you are learning:** Generate and reconcile an official security report *(EO3b)*

### Demo Workspace

**Remain in macOS Terminal**. Inspect the official `reports/action/generate` request and `traditional-json` report type used by the script.

<!-- student-location:start -->
**Run in:** macOS Terminal.

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module2-demos/m2-demo2-zap-api-scan-evidence"
```
<!-- student-location:end -->

### Run Command

**Where:** macOS Terminal. **Current folder:** `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/03-reconcile-json-report.sh
```

<!-- student-proof:start -->
**Where your result appears:** Stay in the terminal for the generated report fields; show official report JSON when comparing nested fields. Compare to the API result already captured in this take.

**Inspect this evidence:** Same custom identity, scope and rating; investigate any mismatch rather than assuming freshness.
<!-- student-proof:end -->

### Expected Results

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>Report template</b></td><td><code>traditional-json</code></td><td>Official ZAP report type</td></tr>
<tr><td><b>Report alert (pluginid · name)</b></td><td><code>50000 · Globomantics unsafe reflection (custom rule)</code></td><td>Same rule as live API</td></tr>
<tr><td><b>Report rating (riskdesc)</b></td><td><code>Medium (Medium)</code></td><td>Risk and confidence same as Step 2</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS JSON report reconciled with API</code></td><td>Archived and live evidence agree</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### Interpret Results

The generated report preserves the named custom finding in a shareable format. Matching its identity and rating against the API prevents stale-report assumptions.

**How the investigation advances:** Inspect the scan's operational quality in addition to the vulnerability result.

</details>

<details>
<summary><b>Step 4 — Read the report's scan-effectiveness Insights</b> · Check Insights</summary>

### Learning Goal

A scan might appear clean because it encountered an authentication, scope or execution problem.

**What you are learning:** Interpret operational findings exposed with the scan report *(EO3b)*

### Demo Workspace

**Remain in macOS Terminal**. Locate the actual `insights[]` entries returned by the report extraction, with the key and explanation readable.

<!-- student-location:start -->
**Run in:** macOS Terminal.

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module2-demos/m2-demo2-zap-api-scan-evidence"
```
<!-- student-location:end -->

### Run Command

**Where:** macOS Terminal. **Current folder:** `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/04-read-zap-insights.sh
```

<!-- student-proof:start -->
**Where your result appears:** Stay in the terminal and show actual report insights[] entries with their explanations. No browser tour is required.

**Inspect this evidence:** Real insight key, statistic and meaning, including operational failures; empty Insights is HOLD.
<!-- student-proof:end -->

### Expected Results

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>Insight (level · key)</b></td><td><code>&lt;actual level&gt; · &lt;actual insight key&gt;</code></td><td>Must be from nonempty insights[]</td></tr>
<tr><td><b>Statistic · meaning</b></td><td><code>&lt;actual value&gt; · &lt;real description&gt;</code></td><td>Scan-effectiveness evidence</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS report Insights returned</code></td><td>Do not substitute unrelated counters</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### Interpret Results

Insights describe scan behavior and confidence in coverage, not only vulnerability risk. A missing Insights section is a reason to investigate, not something to invent or ignore.

**How the investigation advances:** The four fields now support a programmatic, evidence-backed scan assessment.

</details>

<!-- student-achievement:start -->
## What You Achieved

After the four checks, you can inspect ZAP programmatically, distinguish risk from confidence, and reconcile a report with the API. You can use actual Insights to discuss scan effectiveness, including operational failures, without replacing missing Insights with unrelated counters.

**Your final check:** Explain the result using your own captured evidence. A README example, missing result or earlier run does not satisfy this exercise.
<!-- student-achievement:end -->

## Finish Your Lab

A report is trustworthy only when its custom finding, rating and scan-quality context match the current API evidence.

From the same demo directory, stop the local services:

```bash
./scripts/demo_down.sh
```

The `m2-demo2-after` branch contains the completed example or reference behavior. Preserve student changes before switching branches. For a safe comparison run `git diff m2-demo2-before..m2-demo2-after -- demos/module2-demos/m2-demo2-zap-api-scan-evidence` from the repository root; operational-only exercises may have no source diff.

**One batch validation command for the course:** `./setup/run-all-demo-preflights.sh` from the repository root. This checks all six finished branches and creates real evidence bundles for the production team. There are no separate per-demo preflight commands.

<!-- demo-navigation:start -->
<p align="center"><b>Student exercise · Demo 5 of 6</b></p>
<p align="center">
  <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo1-before/demos/module2-demos/m2-demo1-authenticated-zap-github-actions/README.md"><img alt="Previous student demo: Module 2 Demo 1 — Authenticated ZAP in GitHub Actions" src="https://img.shields.io/badge/%E2%86%90_Previous-M2_Demo_1-130F25?style=for-the-badge"></a>
  <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo3-before/demos/module2-demos/m2-demo3-security-quality-gates/README.md"><img alt="Next student demo: Module 2 Demo 3 — Security quality gates" src="https://img.shields.io/badge/Next_%E2%86%92-M2_Demo_3-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->

[← Module 2 catalog](../README.md) · [← Course home](../../../README.md)
