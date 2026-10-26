# Module 2 · Demo 2, Query the ZAP API and evidence reports

> ⚡ **Run from anywhere (shortcut).** You keep landing at the repo root, which is fine: the `./lab` helper there picks THIS demo from your branch, so you never fight directories.
>
> ```bash
> cd "$HOME/pluralsight-script-development-with-zap"   # the repo root (where ./lab lives)
> ./lab up      # start the lab (first time; waits until ready)
> ./lab run check-zap-scan-status   # run the first check (use the matching script name below)
> ./lab down    # stop the lab when you are done
> ```
>
> The walk-through below shows each command as `./steps/0N-...sh` (run inside the demo folder); `./lab run <name>` runs that same step from the repo root (it cd’s into the demo folder for you).
>
> 🧪 **Self-test before you start.** `preflight-check` runs every step and confirms each one works and prints the expected output, so you can fix any setup issue before you begin.
> ```bash
> (cd "$(git rev-parse --show-toplevel)" && ./preflight-check --m2d2)   # just this demo — runs from anywhere
> (cd "$(git rev-parse --show-toplevel)" && ./preflight-check)          # or the whole course, every demo in order
> ```


<div align="center">

![Training](https://img.shields.io/badge/Globomantics-Authorized_Lab-130F25?style=for-the-badge)
![ZAP](https://img.shields.io/badge/OWASP_ZAP-API_Evidence-FF1675?style=for-the-badge)

<img src="../../../docs/learner-diagrams/m2-demo2-architecture.svg" width="100%" alt="Module 2 · Demo 2, Query the ZAP API and evidence reports architecture"/>

<sub>Illustrative workflow · Generated using ChatGPT · Verify actual evidence in your own lab</sub>

</div>

<!-- demo-navigation:start -->
<p align="center"><b>Student exercise · Demo 5 of 6</b></p>
<p align="center">
  <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo1-before/demos/module2-demos/m2-demo1-authenticated-zap-github-actions/README.md"><img alt="Previous student demo: Module 2 Demo 1, Authenticated ZAP in GitHub Actions" src="https://img.shields.io/badge/%E2%86%90_Previous-M2_Demo_1-130F25?style=for-the-badge"></a>
  <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo3-before/demos/module2-demos/m2-demo3-security-quality-gates/README.md"><img alt="Next student demo: Module 2 Demo 3, Security quality gates" src="https://img.shields.io/badge/Next_%E2%86%92-M2_Demo_3-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->

## Your scenario

Picture the Globomantics release pipeline at two in the morning. No one is watching a ZAP window, a build step has to decide, on its own, whether the authenticated scan of the Store actually finished, whether it found the issue you care about, and whether the report it is about to attach to the release really describes *this* code. A screenshot or an alert count cannot answer any of that. A machine needs machine-readable answers.

That is the problem you and I solve in this demo. ZAP exposes a REST API on `http://localhost:8090/`, and everything the GUI shows you is also available as JSON over that API. We are going to ask ZAP four questions the way a pipeline would, *did the scan finish, what exactly did it find, does the saved report agree with the live engine, and was the scan even healthy*, and we are going to treat every answer as evidence to be checked, not taken on faith.

One honest framing before we start: this demo lives in the terminal on purpose, because the API *is* the lesson. We are not avoiding the GUI to save time; we are learning the contract a pipeline depends on. Every command below is one HTTP question, and the teaching is in reading the JSON it returns.

## Your learning goals

You will retrieve and reconcile machine-readable security evidence from a completed authenticated scan:

1. Query scan status and a specific finding using the official ZAP API *(EO3b)*
2. Reconcile the API's named custom rule against a generated JSON report and the report's own scan-effectiveness Insights *(EO3b)*

You do not need the separate course outline to follow along, each step states what you are checking and why.

## Your evidence path

```mermaid
flowchart LR
  S1["Did the scan finish?<br/>(version · plan · scan state)"]
  S2["What did it find?<br/>(rule identity · risk · confidence)"]
  S3["Does the report agree?<br/>(report vs live API)"]
  S4["Was the scan healthy?<br/>(report Insights)"]
  S1 --> S2 --> S3 --> S4
```

Read it as one investigation: each step only makes sense because of the one before it. You cannot trust a finding from a scan you have not confirmed finished, and you cannot trust a report you have not reconciled against the live engine.

## Start your lab

Mac dependencies are prepared **once for the course** with `setup/setup-macos.sh` (see the [course README](../../../README.md)). Each demo then starts its **own** local stack:

<details open>
<summary><b>Open the exact branch and start Module 2 Demo 2</b></summary>

**Where:** macOS Terminal or the VS Code integrated Terminal, from the root of your existing Git checkout.

```bash
cd "$HOME/pluralsight-script-development-with-zap"
git fetch origin
git switch m2-demo2-before
(cd demos/module2-demos/m2-demo2-zap-api-scan-evidence && ./scripts/lab-up.sh)
```

**Expected start:** the startup script reports healthy Globomantics, Postgres, MongoDB and ZAP services, and provisions this demo's authenticated scan so there is real evidence to query. If anything is not ready, stop and read the actual output before continuing.

**URLs:** <a href="http://localhost:8000/" target="_blank" rel="noopener">Training application</a> · <a href="http://localhost:8080/zap/" target="_blank" rel="noopener">ZAP GUI</a> · <a href="http://localhost:8090/" target="_blank" rel="noopener">ZAP API and proxy</a>. You will work from the terminal; the GUI is there only if you want to see the same data rendered.

</details>

## Your steps

<!-- source-focus:start -->
## Read the code that supports this exercise

Paths below are relative to this demo folder. Open the named file in VS Code and find the function or YAML block; inspect only the part that explains the current check.

| File | Function or block | What to understand |
|---|---|---|
| `scripts/_steps.sh` | `step1_api_status()` | Inspect the ascan/view/scans response extraction and its progress/state fields. Then compare those fields with the completed command output. |

The `steps/` folder contains the commands you run; `scripts/` contains their implementation. Files identified as copied references become available after the existing reference-copy step.

<!-- source-focus:end -->

<!-- learner-command-steps:start -->

Follow one numbered action set at a time. Opening the terminal, pasting a command and pressing Enter belong to the same step. Reading its source and interpreting its result stay with that step. Script filenames retain their stable 01–04 identifiers. Check numbers printed by the scripts identify those underlying lab checks, not the parent step numbers below. The numbered walkthrough steps also include entering the folder, reference copies and reruns where needed.

| Step | Action |
|---|---|
| [Step 1](#step-1) | directory change command |
| [Step 2](#step-2) | zap scan status script |
| [Step 3](#step-3) | query custom rule alert script |
| [Step 4](#step-4) | reconcile json report script |
| [Step 5](#step-5) | zap insights script |

<a id="step-1"></a>

## Step 1: directory change command

1. Open the VS Code integrated Terminal at the repository root after the lab setup above.
2. Paste this command and press Enter.

```bash
cd demos/module2-demos/m2-demo2-zap-api-scan-evidence
```

Confirm the returned prompt is inside `demos/module2-demos/m2-demo2-zap-api-scan-evidence` before running the first check. Stop if the directory change fails. This folder entry is Step 1; pasting and executing each later command is one new step, with its teaching and results kept together.

<a id="step-2"></a>

## Step 2: zap scan status script

<details>
<summary><b>Teaching, command and result</b></summary>

### What you are learning

Query machine-readable scan status, and understand why "the API answered" is not the same as "the scan is done." *(EO3b)*

### What we examine, and why

The script asks ZAP three questions over HTTP, and each one exists for a reason:

- **`GET core/view/version`**, which engine produced these findings. This matters more than it looks: detection logic changes between ZAP releases, so a report is only meaningful next to the version that generated it. You should see `2.17.0`, the version this course is built on.
- **`automation/view/planProgress?planId=…`**, did the Automation Framework plan that ran the authenticated scan actually complete, how many errors did it hit, and which user was it scanning as. A plan that errored out can still leave a half-populated session that looks fine from the outside.
- **`GET ascan/view/scans`**, the active scan's `id`, `progress`, and `state`. This is the one that keeps you honest: a pipeline that reads findings at `progress=50%` is reading half a scan.

**Predict before you run:** you expect version `2.17.0`, the plan `finished` with `0` errors scanning as the authenticated user, and a scan at `progress=100% · state=FINISHED`. Hold that prediction, the point of the step is to confirm it from the engine, not assume it.

### Run command

**Where:** macOS Terminal, in `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/01-check-zap-scan-status.sh
```

### Expected result (the script's output contract, not your run)

Values in `<…>` are run-specific and must be read from your own output. The named values are what the API returns on a healthy run.

| OBSERVED FIELD | ACTUAL VALUE |
|---|---|
| ZAP runtime  (GET core/view/version) | `2.17.0` |
| Authenticated plan  (automation/view/planProgress) | `plan 0 · finished · 0 errors · scanning as alice` |
| Active scan  (GET ascan/view/scans) | `id=0 · progress=100% · state=FINISHED` |
| Requests the scan sent | `<live count>` |

**`✔ PASS`** the API reports the ZAP runtime and a finished authenticated scan.

### Investigate, then decide

Read your own output against the prediction. If `state` is not `FINISHED` or `progress` is below `100`, you must **stop**, any finding you read now is from an incomplete scan. The engineering decision this step authorizes is simple and strict: *only consume findings once the engine itself says the scan is finished.* That is the rule a pipeline encodes so it never ships on a half-run scan.

**On FAIL:** the script tells you which of the three signals failed (version, plan, or scan). Fix that first; do not advance or reuse an earlier run.

**Next:** now that the scan is trustworthy, retrieve the one finding that matters instead of a count.

</details>

<a id="step-3"></a>

## Step 3: query custom rule alert script

<details>
<summary><b>Teaching, command and result</b></summary>

### What you are learning

Retrieve a specific scanner finding through the API and read the fields a pipeline reasons about. *(EO3b)*

### What we examine, and why

The script calls **`GET core/view/alerts?baseurl=<authenticated profile URL>`** and pulls the entry for our custom rule. Each alert in the JSON carries, among other fields: `pluginId`, `alertRef`, `alert` (the name), `risk`, `confidence`, `param`, and `evidence`. We read the ones that make a finding actionable:

- **`pluginId` and `alertRef`**, the rule's identity. You should see `50000`, that is *the Jython active-scan rule you wrote in Module 1, Demo 3*, not a built-in rule. This is the whole reason the custom rule existed: so your application-specific issue shows up as your own named finding here.
- **`param`**, `note`, the Store profile field the rule probes. Identity plus parameter is what tells a developer exactly where to look.
- **`risk` and `confidence`**, two *different* axes, and keeping them apart is the lesson. `risk` is how bad it is if real; `confidence` is how sure ZAP is that it is real. You should see `Medium · Medium`. Teams that collapse these into one number either panic over a low-confidence note or wave through a high-risk one.

**Predict before you run:** you expect `pluginId 50000`, name "Globomantics unsafe reflection (custom rule)", `param note`, and `Medium · Medium`. If a built-in XSS rule also fired on this page, that is *not* the finding we are proving, ours is the named custom one.

### Run command

**Where:** macOS Terminal, in `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/02-query-custom-rule-alert.sh
```

### Expected result (the script's output contract, not your run)

| OBSERVED FIELD | ACTUAL VALUE |
|---|---|
| Rule identity  (pluginId · alertRef) | `50000 · 50000` |
| Alert | `Globomantics unsafe reflection (custom rule)  (alert id <id>)` |
| Disposition  (risk · confidence) | `Medium · Medium` |
| Parameter | `note` |

**`✔ PASS`** the API returns the script-generated alert's rule identity and disposition.

### Investigate, then decide

Confirm the identity is `50000`, not a built-in reflected-XSS rule that happens to be on the same page. That connection, *this API alert is the rule I wrote*, is what makes the finding yours to own. The decision this authorizes: a pipeline routes and gates on **rule identity and disposition**, never on a raw alert count, because only identity tells you *what* broke and only risk-with-confidence tells you *how much to care*.

**On FAIL:** the API returned no `50000` on the profile URL. That usually means the authenticated scan did not reach the protected page (go back to Step 2), not that the rule is wrong.

**Next:** prove the report you would hand to a release owner says the same thing the live engine just said.

</details>

<a id="step-4"></a>

## Step 4: reconcile json report script

<details>
<summary><b>Teaching, command and result</b></summary>

### What you are learning

Generate an official report and reconcile it, field by field, against the live API. *(EO3b)*

### What we examine, and why

The script calls **`reports/action/generate` with the `traditional-json` template**, ZAP's official machine-readable report, the artifact a pipeline stores and attaches to a release. Then it reads back the same finding from that report (`pluginid`, `riskdesc`, and the instance `param`) and compares them to the values you captured from the live API in Step 3.

Why go to this trouble? Because **a report is a file, and files go stale.** The most dangerous mistake in this whole workflow is attaching last week's report to this week's release, the vulnerability you believe is fixed may simply have been scanned before the fix existed. Reconciliation is how you prove the archived evidence and the live engine are describing the same scan.

**Predict before you run:** the report's `pluginid` should be `50000` and its `riskdesc` should read `Medium (Medium)`, the same identity and the same rating the API gave you a moment ago. You are checking for *agreement*, and you should be a little suspicious until you see it.

### Run command

**Where:** macOS Terminal, in `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/03-reconcile-json-report.sh
```

### Expected result (the script's output contract, not your run)

| OBSERVED FIELD | ACTUAL VALUE |
|---|---|
| Report  pluginid · riskdesc · param | `50000 · Medium (Medium) · note` |
| API (Step 3)  pluginId · risk (confidence) · param | `50000 · Medium (Medium) · note` |
| Fields that match | `3 of 3` |

**`✔ PASS`** the official JSON report matches the API alert on rule ID, risk/confidence and parameter.

### Investigate, then decide

Look at the three fields side by side with your Step 3 values. If any of identity, scope, or rating disagrees, you do **not** have evidence, you have a question to chase (a stale file, a different scan, a scope mismatch). The decision: *a report is only release-grade when it reconciles with the current engine.* That sentence is the entire reason this step exists.

**On FAIL:** either the report failed to generate (check the reports add-on and Docker access to the ZAP container) or it disagreed with the API. A disagreement is a real finding about your process, not something to edit away.

**Next:** the finding checks out, but was the scan that produced it any good? Read its health.

</details>

<a id="step-5"></a>

## Step 5: zap insights script

<details>
<summary><b>Teaching, command and result</b></summary>

### What you are learning

Interpret the operational findings ZAP reports about the scan itself, not the application. *(EO3b)*

### What we examine, and why

The script reads the report's **`insights[]`** section and prints a real entry's level, key, statistic and meaning. Insights are a different kind of information from alerts: they describe *the scan*, not the app, how much was covered, how many requests went out, whether anything went wrong during the run.

Here is why this is the step people skip and shouldn't. **A scan can come back with zero findings for two opposite reasons: the application is clean, or the scan barely touched it.** An authentication failure, a scope that missed the real pages, or a run that died early all produce a reassuring, empty, and completely misleading result. Insights is how you tell a thorough scan from a shallow one.

**Predict before you run:** you expect a non-empty insight, a real level and key with a statistic and a plain-English meaning. You should be ready to treat an *empty* Insights section as a problem, not a pass.

### Run command

**Where:** macOS Terminal, in `demos/module2-demos/m2-demo2-zap-api-scan-evidence`.

```bash
./steps/04-read-zap-insights.sh
```

### Expected result (the script's output contract, not your run)

Insight values are genuinely run-specific; read yours from the output. The contract is that a real, non-empty insight must be present.

| OBSERVED FIELD | ACTUAL VALUE |
|---|---|
| Insight  (level · key) | `<level> · <insight key>` |
| Statistic · meaning | `<value> · <description>` |

The report lists one pair per insight. In the verified reference run the three top insights were `Low · insight.log.error` (`5`, ZAP errors logged), `Low · insight.log.warn` (`5`, ZAP warnings logged) and `Info · insight.code.2xx` (`68`, percentage of responses with a 2xx status). The exact keys and counts are genuinely run-specific, so read yours from the output, but notice that two of these three are *operational issues*, not a clean bill of health. The step also prints the report's path inside the ZAP container and a `logs/` copy saved on your Mac, so you can open the actual JSON and the referenced `zap.log` yourself.

**`✔ PASS`** the report's own Insights section reports scan effectiveness (interpret each entry; it is not a clean bill of health).

### Investigate, then decide

Read the real insights and say what each tells you about the scan's reach, then interpret the operational ones rather than glossing them green. The `insight.log.error` and `insight.log.warn` counts are lines ZAP wrote to its own `zap.log` during this run; the count alone does not say whether they hurt coverage, so you open the saved report and `zap.log` to see what they were (add-on and script-registration messages and passive-rule noise are common and harmless; a failed authentication or a request that never completed is not). The `insight.code.2xx` figure (`68` in the reference run) means roughly a third of responses were non-2xx; for an authenticated scan some of that is expected redirects, but a low figure can also mean requests failed to reach the app.

So do these issues invalidate the scan? For *this* demo, no: Step 2 showed the scan reached `progress=100% · state=FINISHED`, the custom rule `50000` fired on the authenticated page, and Step 4 reconciled 3 of 3 fields, so the finding you are proving is sound. The logged errors and warnings are operational noise you must still read, not evidence the scan failed. The decision this authorizes is the one that protects you from false confidence: *a clean result is only trustworthy next to evidence the scan actually did its job.* If Insights is empty, investigate the run; if it reports logged errors or warnings, read those too, never invent a number so the step looks complete.

**On FAIL:** empty or missing Insights is a HOLD by design. Investigate why the report has none rather than papering over it.

**Next:** you now have all four pieces, finished, found, reconciled, and scan health *assessed* (not assumed), the complete programmatic evidence a pipeline needs. A matching report from a scan with logged errors still needs those errors read before you trust it.

</details>

<!-- learner-command-steps:end -->

<!-- student-achievement:start -->
## What you achieved

You can now defend a scan's evidence the way a release pipeline has to, with the API, not a screenshot:

1. **(EO3b) You confirmed the scan was real before trusting it.** You asked the engine its version (`2.17.0`), confirmed the authenticated plan `finished` with no errors as `alice`, and read `progress=100% · state=FINISHED`, so you know the findings came from a complete scan, not a half-run one.
2. **(EO3b) You identified the finding by rule, not by count.** You pulled `pluginId 50000`, your own Jython rule from Module 1, on parameter `note`, and read `risk` and `confidence` as the two separate `Medium` axes a pipeline reasons about.
3. **(EO3b) You proved the report is release-grade.** You generated the official `traditional-json` report and reconciled its `pluginid` and `riskdesc` ("Medium (Medium)") field-by-field with the live API, so you can reject a stale or mismatched report instead of trusting it blindly.
4. **(EO3b) You checked the scan's health, not just its result.** You read the report's real `insights[]` entries, including the `insight.log.error` and `insight.log.warn` counts, and you know that neither an empty Insights section nor a non-empty one carrying logged errors and warnings is a clean bill of health, each is a reason to open the saved report and `zap.log` and investigate before you trust the result.

**How to apply it:** this is exactly the sequence you wire into CI, confirm completion, pull findings by identity, reconcile the stored report, and check coverage, so a build can make a defensible security decision with no human watching.

**Your final check:** explain each outcome using *your* captured values from this run. A README example, a missing result, or an earlier run does not satisfy this exercise.
<!-- student-achievement:end -->

## Finish your lab

A report is trustworthy only when its custom finding and its rating reconcile with the current API evidence *and* you have read its scan-quality Insights rather than assuming they are clean, which is exactly what you just did, in order.

From the same demo directory, stop the local services:

```bash
cd "$HOME/pluralsight-script-development-with-zap/demos/module2-demos/m2-demo2-zap-api-scan-evidence"
./scripts/lab-down.sh
```

The `m2-demo2-after` branch holds the completed reference. Preserve your changes before switching branches. For a safe comparison, run `git diff m2-demo2-before..m2-demo2-after -- demos/module2-demos/m2-demo2-zap-api-scan-evidence` from the repository root; this is an operational demo, so the difference is in the captured evidence, not in source files.

<!-- demo-navigation:start -->
<p align="center"><b>Student exercise · Demo 5 of 6</b></p>
<p align="center">
  <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo1-before/demos/module2-demos/m2-demo1-authenticated-zap-github-actions/README.md"><img alt="Previous student demo: Module 2 Demo 1, Authenticated ZAP in GitHub Actions" src="https://img.shields.io/badge/%E2%86%90_Previous-M2_Demo_1-130F25?style=for-the-badge"></a>
  <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo3-before/demos/module2-demos/m2-demo3-security-quality-gates/README.md"><img alt="Next student demo: Module 2 Demo 3, Security quality gates" src="https://img.shields.io/badge/Next_%E2%86%92-M2_Demo_3-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->

[← Module 2 catalog](../README.md) · [← Course home](../../../README.md)
