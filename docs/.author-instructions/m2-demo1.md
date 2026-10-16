# Module 2 · Demo 1 — Authenticated ZAP in GitHub Actions · Production guide

<div align="center">

![Recorder](https://img.shields.io/badge/RECORDER-Actual_Screens-00A3FF?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-Clean_Callouts-02E088?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-ElevenLabs-770EF7?style=for-the-badge)

<img src="../learner-diagrams/m2-demo1-architecture.svg" width="100%" alt="Demo 1 — Authenticated ZAP in GitHub Actions component diagram"/>
<sub>Illustrative architecture · Generated using ChatGPT · Temporary PUBLIC production material</sub>

</div>

[← Production dashboard](README.md) · [Open student's Module 2 demo README](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo1-before/demos/module2-demos/m2-demo1-authenticated-zap-github-actions/README.md)

<!-- demo-navigation:start -->
<p align="center"><b>Author production guide · Demo 4 of 6</b></p>
<p align="center">
  <a href="m1-demo3.md"><img alt="Previous author guide: Module 1 Demo 3 — Python scanning and authentication" src="https://img.shields.io/badge/%E2%86%90_Previous-M1_Demo_3-130F25?style=for-the-badge"></a>
  <a href="m2-demo2.md"><img alt="Next author guide: Module 2 Demo 2 — ZAP API and reports" src="https://img.shields.io/badge/Next_%E2%86%92-M2_Demo_2-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->

## Prepare Recording

**Record the `m2-demo1-before` branch**, completing the missing plan where applicable, and keep source changes traceable. The Developer runs the **one combined batch preflight before the recording team starts** and distributes `deliverables/m2-demo1/`: commands, verified logs, generated HTML and narration drafts.

**Off-camera preparation:** from the existing checkout root run `git switch m2-demo1-before`, then `cd demos/module2-demos/m2-demo1-authenticated-zap-github-actions`, then `./scripts/demo_up.sh`. Check the local application at `http://localhost:8000/`. Confirm the lesson source/plan is ready before testing. One-time Mac preparation and the batch command live **only on the author dashboard**; do not repeat them during recorded steps.

**Recording sequence:** show code or GUI context, display exact command and its key parameters for about 8 seconds, execute once, then reveal real output in 6–8-second proof windows; show real GitHub Actions job and report where the LO requires hosted proof. The Editor cuts waiting and focus changes cleanly.

## Recording Steps

<!-- demo-readiness:start -->
## Demo Readiness

**Approved duration:** 5 minutes. **Execution steps:** four, unchanged. **Acceptance target:** overall review score at least 98/100.

| Step | Current evidence-backed score | Blocking review |
|---|---|---|
| 1 | Not assessed | Matching Mac take, required GUI/Actions proof and final spoken coverage |
| 2 | Not assessed | Matching Mac take, required GUI/Actions proof and final spoken coverage |
| 3 | Not assessed | Matching Mac take, required GUI/Actions proof and final spoken coverage |
| 4 | Not assessed | Matching Mac take, required GUI/Actions proof and final spoken coverage |

**Overall confidence:** NOT ASSESSED. Once all four step scores are supported, calculate `(step1 + step2 + step3 + step4) / 4`; do not average only the reviewed steps. A missing critical proof keeps release on HOLD even when the average reaches 98.

**Speech budget:** current short-form draft 226 whitespace words; final 5-minute target 644 spoken words under the owner contract. Remaining before final audio validation: 418 words. This draft is not a complete timed recording script. Expand useful source/action/result teaching within the same four steps; do not fill time with invented stories.

**Recording budget:** approximately 75 seconds per step, including source work, execution and proof. This is an editing plan, not a measured duration or a reason to leave a static screen.

**Review method:** assess LO and outline coverage, technical correctness, example quality, learner clarity, operator decision-making and recorded proof against the exact source SHA. Record the reviewer, rationale and evidence for every numeric score. Old 88–96% source estimates lacked a documented common rubric and are retired, not promoted.
<!-- demo-readiness:end -->
## Step 1 — Run ZAP from the Automation Framework plan

<details open>
<summary><b>Open step 1 — where, command, output and production roles</b></summary>


### Learning Goal

A security test needing manual clicks is not a repeatable CI control.

**What you are learning:** Configure headless ZAP in CI/CD *(EO3a)*

### Demo Workspace


**Off-camera terminal setup:** Open VS Code integrated Terminal. Preserve any uncommitted work before changing branches. Paste these commands exactly; they select the demo starter and working folder.

```bash
cd "$HOME/pluralsight-script-development-with-zap"
git switch m2-demo1-before
cd "demos/module2-demos/m2-demo1-authenticated-zap-github-actions"
```

**Actual screen and browser check:** Check http://localhost:8000/ for local readiness off camera. Show ci/af-plan.yaml and the real GitHub Actions workflow at https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/actions/workflows/zap-authenticated-scan.yml; require current run SHA for hosted proof.


**Open VS Code.** Inspect `ci/af-plan.yaml` and the `.github/workflows/zap-authenticated-scan.yml` workflow. Open **GitHub → Actions → authenticated-scan** for hosted proof of the exact current commit.

### Run Command

**Where:** VS Code integrated Terminal for the local check; GitHub Actions page for CI evidence. **Current folder:** `demos/module2-demos/m2-demo1-authenticated-zap-github-actions`.

```bash
./steps/01-run-headless-automation-plan.sh
```

### Expected Results

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>Runner (CI)</b></td><td><code>ubuntu-24.04 · ZAP pinned container</code></td><td>Confirm correct hosted platform</td></tr>
<tr><td><b>Command</b></td><td><code>zap.sh -cmd -autorun /zap/wrk/af-plan.yaml</code></td><td>No desktop UI required</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS plan ran headlessly to completion</code></td><td>Compare to hosted job for this SHA</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### Operator Decision

The Automation Framework plan moves the scan configuration into versioned code. The local step proves that plan can execute headlessly; a hosted run must be verified separately against the same plan revision.

**How the investigation advances:** Inspect the user and scope declared by that plan.

<!-- capture-location:start -->
<table><tr><th>Capture moment</th><th>Exact action and result location</th></tr><tr><td>Before Enter</td><td>Use VS Code integrated Terminal. Show the named step command already provided below/above; keep its full filename readable for about eight seconds. Directory and branch setup are off camera.</td></tr><tr><td>After Enter</td><td>The local result stays in Terminal. For required hosted proof, open https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/actions/workflows/zap-authenticated-scan.yml, select the matching branch/SHA run, authenticated-scan job, and headless execution step.</td></tr><tr><td>Evidence to record</td><td>Actual hosted runner log, launch command and exact commit; a printed local Runner (CI) label is only configuration. Hold each meaningful field for six to eight seconds; retain the matching raw log and take ID.</td></tr><tr><td>Meaning and decision</td><td>Use the Spoken Narration for this exact field, then explain whether the evidence is enough to proceed. If it is absent, stop: neither a source declaration nor an expected output is an observed result.</td></tr><tr><td>Editor handoff</td><td>Mark the result region, then the actual value being explained. Clear old overlays on pane change. During an otherwise still explanation beyond 12 seconds, use one relevant 6–8-second takeaway callout; never invent a successful result.</td></tr></table>
<!-- capture-location:end -->

### Recorder Shots

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Precisely_What_To_Show-0284c7"/></summary>
<table>
<tr><th>Video Beat</th><th>Screen, Scroll, Hold And Proof</th></tr>
<tr><td>Source · 8s</td><td>VS Code: ci/af-plan.yaml at the top-level jobs, then GitHub Actions → Globomantics authenticated ZAP scan → job authenticated-scan. Show correct branch and SHA.</td></tr>
<tr><td>Command · 8s</td><td>Show the full named step command above; press Enter once without visible corrections. Any long scan wait is cut cleanly.</td></tr>
<tr><td>Output A · 6–8s</td><td>Box the runner platform and `zap.sh -cmd -autorun` command, then show the current Actions run.</td></tr>
<tr><td>Output B · 6–8s</td><td>Move highlight to green hosted plan step and the actual commit SHA. Do not use an older green job as current proof.</td></tr>
<tr><td>Completion · 6–8s</td><td>Hold the actual PASS and/or hosted evidence; on an important GUI click provide 8s before and 8s after in the source take.</td></tr>
</table></details>

### Spoken Narration

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Final_Spoken_Words-d946ef"/></summary>
<table><tr><th>Shot</th><th>Speak Exactly After Confirming The Screen</th><th>Words</th></tr>
<tr><td>Command</td><td>Run the Automation Framework plan headlessly so ZAP can assess Globomantics without clicking through a desktop interface.</td><td>17</td></tr>
<tr><td>Output A</td><td>The workflow specifies an Ubuntu runner and a pinned ZAP image. Confirm the hosted log actually used them before treating configuration as evidence.</td><td>23</td></tr>
<tr><td>Output B / decision</td><td>This local result supports headless execution. A matching GitHub Actions run and commit are still required before claiming hosted CI proof.</td><td>21</td></tr>
</table>
The voice must match actual displayed evidence. Never read a sample result as an observed finding.
</details>

### Editor Actions

<details><summary><img src="https://img.shields.io/badge/EDITOR-Single_Focus_Cuts-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>GitHub Actions workflow job and autorun command</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Runner (CI)</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Command</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>A hosted run is distinct from a local YAML plan</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Beat</th><th>Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut on pane switch. Thin square on the exact file/function, then clear it when the command appears.</td></tr>
<tr><td>First and second proof</td><td>Use a square on `-autorun`, an arrow to Actions' scan step, then a separate short callout around the matching SHA. Hold each focus 6–8s, then remove it immediately when switching.</td></tr>
<tr><td>Final PASS/report</td><td>Show the correct same-run output, not a static illustration. Align narrator line 3 with the actual decision field.</td></tr>
<tr><td>Evidence files</td><td>Compare `preflight-step-01.log` and `recorded-step-01.log`, retain raw proof and Actions run ID/SHA in the take manifest. Mismatch requires a retake.</td></tr>
</table></details>

### Proof Review

- **Proof:** Compare filmed output against the Developer's actual `deliverables/m2-demo1/logs/preflight-step-01.log`, plus the matching live GUI or GitHub Actions artifact
- **Learning:** Validate the purpose and mechanism above; a command-only video does not meet the objective
- **Release:** HOLD until evidence review; target overall score 98/100, never automatic approval

</details>
## Step 2 — Inspect the authenticated scan context

<details>
<summary><b>Open step 2 — where, command, output and production roles</b></summary>


### Learning Goal

A headless job can silently scan only the login page without valid context or identity.

**What you are learning:** Specify an authenticated context and bounded targets *(EO3a)*

### Demo Workspace


**Off-camera terminal setup:** Open VS Code integrated Terminal. Preserve any uncommitted work before changing branches. Paste these commands exactly; they select the demo starter and working folder.

```bash
cd "$HOME/pluralsight-script-development-with-zap"
git switch m2-demo1-before
cd "demos/module2-demos/m2-demo1-authenticated-zap-github-actions"
```

**Actual screen and browser check:** Show ci/af-plan.yaml → env.contexts, script authentication, alice and target scope in VS Code. Terminal confirms configuration; hosted access requires Actions proof.


**In VS Code**, scroll through `ci/af-plan.yaml` to `env.contexts`, authentication script, `alice` user, and `includePaths`. Keep the relevant YAML keys visible.

### Run Command

**Where:** the VS Code integrated Terminal. **Current folder:** `demos/module2-demos/m2-demo1-authenticated-zap-github-actions`.

```bash
./steps/02-inspect-authenticated-scan-context.sh
```

### Expected Results

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>Context</b></td><td><code>Globomantics</code></td><td>Correct test context</td></tr>
<tr><td><b>Authentication</b></td><td><code>script-based → globomantics-auth (/login)</code></td><td>Script supplies session</td></tr>
<tr><td><b>User</b></td><td><code>alice</code></td><td>Identity for protected scan</td></tr>
<tr><td><b>Target scope</b></td><td><code>http://app:8000 (profile and greet paths)</code></td><td>Target stays authorized</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS context and authentication configured</code></td><td>Configuration established</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### Operator Decision

The context specifies how ZAP logs in and where it is allowed to scan. This is the foundation for meaningful authenticated coverage.

**How the investigation advances:** Confirm the original JavaScript and Python scripts are reused rather than replaced.

<!-- capture-location:start -->
<table><tr><th>Capture moment</th><th>Exact action and result location</th></tr><tr><td>Before Enter</td><td>Use VS Code integrated Terminal. Show the named step command already provided below/above; keep its full filename readable for about eight seconds. Directory and branch setup are off camera.</td></tr><tr><td>After Enter</td><td>Stay in VS Code with ci/af-plan.yaml and the integrated terminal. Show env.contexts, script authentication, user alice and included paths.</td></tr><tr><td>Evidence to record</td><td>Context, authentication method, user and target scope; configuration alone is not a login success. Hold each meaningful field for six to eight seconds; retain the matching raw log and take ID.</td></tr><tr><td>Meaning and decision</td><td>Use the Spoken Narration for this exact field, then explain whether the evidence is enough to proceed. If it is absent, stop: neither a source declaration nor an expected output is an observed result.</td></tr><tr><td>Editor handoff</td><td>Mark the result region, then the actual value being explained. Clear old overlays on pane change. During an otherwise still explanation beyond 12 seconds, use one relevant 6–8-second takeaway callout; never invent a successful result.</td></tr></table>
<!-- capture-location:end -->

### Recorder Shots

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Precisely_What_To_Show-0284c7"/></summary>
<table>
<tr><th>Video Beat</th><th>Screen, Scroll, Hold And Proof</th></tr>
<tr><td>Source · 8s</td><td>VS Code: ci/af-plan.yaml → env.contexts, authentication script and loggedInRegex, users alice, includePaths. Scroll one section at a time; zoom until key names fit without wraps.</td></tr>
<tr><td>Command · 8s</td><td>Show the full named step command above; press Enter once without visible corrections. Any long scan wait is cut cleanly.</td></tr>
<tr><td>Output A · 6–8s</td><td>Box `Globomantics` and script-based authentication; point to Login URL `/login`.</td></tr>
<tr><td>Output B · 6–8s</td><td>Scroll gently to `alice` and the include paths, then show the corresponding terminal output.</td></tr>
<tr><td>Completion · 6–8s</td><td>Hold the actual PASS and/or hosted evidence; on an important GUI click provide 8s before and 8s after in the source take.</td></tr>
</table></details>

### Spoken Narration

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Final_Spoken_Words-d946ef"/></summary>
<table><tr><th>Shot</th><th>Speak Exactly After Confirming The Screen</th><th>Words</th></tr>
<tr><td>Command</td><td>Define the authenticated context before scanning, so the hosted runner knows how to log in without manual steps.</td><td>18</td></tr>
<tr><td>Output A</td><td>The plan names scripted authentication, user Alice, and approved target paths. Those settings are necessary but do not alone prove a successful login.</td><td>23</td></tr>
<tr><td>Output B / decision</td><td>Those settings decide coverage. A scanner that cannot reach the protected profile cannot substantiate its security findings.</td><td>17</td></tr>
</table>
The voice must match actual displayed evidence. Never read a sample result as an observed finding.
</details>

### Editor Actions

<details><summary><img src="https://img.shields.io/badge/EDITOR-Single_Focus_Cuts-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Automation Framework authentication configuration</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Context</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Authentication</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>Correct context determines covered endpoints</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Beat</th><th>Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut on pane switch. Thin square on the exact file/function, then clear it when the command appears.</td></tr>
<tr><td>First and second proof</td><td>Sequential boxes for authentication, users and includePaths; clear earlier boxes at each scroll or pane change. Hold each focus 6–8s, then remove it immediately when switching.</td></tr>
<tr><td>Final PASS/report</td><td>Show the correct same-run output, not a static illustration. Align narrator line 3 with the actual decision field.</td></tr>
<tr><td>Evidence files</td><td>Compare `preflight-step-02.log` and `recorded-step-02.log`, retain raw proof and Actions run ID/SHA in the take manifest. Mismatch requires a retake.</td></tr>
</table></details>

### Proof Review

- **Proof:** Compare filmed output against the Developer's actual `deliverables/m2-demo1/logs/preflight-step-02.log`, plus the matching live GUI or GitHub Actions artifact
- **Learning:** Validate the purpose and mechanism above; a command-only video does not meet the objective
- **Release:** HOLD until evidence review; target overall score 98/100, never automatic approval

</details>
## Step 3 — Verify the scripts run in the authenticated scope

<details>
<summary><b>Open step 3 — where, command, output and production roles</b></summary>


### Learning Goal

Rewriting the same script in CI introduces drift and makes the reported result harder to trust.

**What you are learning:** Reuse configured custom security scripts in automation *(EO3a)*

### Demo Workspace


**Off-camera terminal setup:** Open VS Code integrated Terminal. Preserve any uncommitted work before changing branches. Paste these commands exactly; they select the demo starter and working folder.

```bash
cd "$HOME/pluralsight-script-development-with-zap"
git switch m2-demo1-before
cd "demos/module2-demos/m2-demo1-authenticated-zap-github-actions"
```

**Actual screen and browser check:** Show script loading and requestor in VS Code then the authenticated GitHub Actions request/report. Loaded scripts alone do not prove outbound sender header.


**In VS Code**, inspect the plan's script-loading jobs, requestor, and active scan. Then inspect the protected profile request or report in the same hosted GitHub Actions run.

### Run Command

**Where:** the VS Code integrated Terminal. **Current folder:** `demos/module2-demos/m2-demo1-authenticated-zap-github-actions`.

```bash
./steps/03-verify-reused-security-scripts.sh
```

### Expected Results

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>Loaded by the plan</b></td><td><code>globomantics-marker (JS), active-rule (Py), auth (Py)</code></td><td>Original scripts reused</td></tr>
<tr><td><b>Ran authenticated against</b></td><td><code>/account/profile (note parameter)</code></td><td>Protected page reached</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS scripts executed against authenticated scope</code></td><td>Do not infer an unshown marker side effect</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### Operator Decision

The plan loads the original extensions and targets the authenticated profile. This confirms script reuse and coverage, not every possible side effect of the HTTP Sender script.

**How the investigation advances:** Locate the exact named custom finding in the current CI evidence.

<!-- capture-location:start -->
<table><tr><th>Capture moment</th><th>Exact action and result location</th></tr><tr><td>Before Enter</td><td>Use VS Code integrated Terminal. Show the named step command already provided below/above; keep its full filename readable for about eight seconds. Directory and branch setup are off camera.</td></tr><tr><td>After Enter</td><td>Show local fields, then the same hosted authenticated-scan run and protected-profile request/report. Keep the script jobs and requestor configuration accessible in VS Code.</td></tr><tr><td>Evidence to record</td><td>Reused script names and authenticated coverage; a loaded sender needs separate header evidence to prove its mutation. Hold each meaningful field for six to eight seconds; retain the matching raw log and take ID.</td></tr><tr><td>Meaning and decision</td><td>Use the Spoken Narration for this exact field, then explain whether the evidence is enough to proceed. If it is absent, stop: neither a source declaration nor an expected output is an observed result.</td></tr><tr><td>Editor handoff</td><td>Mark the result region, then the actual value being explained. Clear old overlays on pane change. During an otherwise still explanation beyond 12 seconds, use one relevant 6–8-second takeaway callout; never invent a successful result.</td></tr></table>
<!-- capture-location:end -->

### Recorder Shots

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Precisely_What_To_Show-0284c7"/></summary>
<table>
<tr><th>Video Beat</th><th>Screen, Scroll, Hold And Proof</th></tr>
<tr><td>Source · 8s</td><td>VS Code: ci/af-plan.yaml → script add/enable jobs, then requestor `account/profile?note=seed` and activeScan as context user. If needed open paths to original JS and Python sources.</td></tr>
<tr><td>Command · 8s</td><td>Show the full named step command above; press Enter once without visible corrections. Any long scan wait is cut cleanly.</td></tr>
<tr><td>Output A · 6–8s</td><td>Box the three loaded script names, one source group at a time.</td></tr>
<tr><td>Output B · 6–8s</td><td>Show authenticated `/account/profile` with `note`, then actual PASS. Sender-header side effects need separate request proof.</td></tr>
<tr><td>Completion · 6–8s</td><td>Hold the actual PASS and/or hosted evidence; on an important GUI click provide 8s before and 8s after in the source take.</td></tr>
</table></details>

### Spoken Narration

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Final_Spoken_Words-d946ef"/></summary>
<table><tr><th>Shot</th><th>Speak Exactly After Confirming The Screen</th><th>Words</th></tr>
<tr><td>Command</td><td>Reuse the original JavaScript sender, Python active rule, and login script rather than rebuilding their behavior for CI.</td><td>18</td></tr>
<tr><td>Output A</td><td>The requestor accesses the protected profile as Alice, enabling the custom rule to inspect the note parameter.</td><td>17</td></tr>
<tr><td>Output B / decision</td><td>Script loading and authenticated reflection are proven here. A specific sender header would require its own request evidence.</td><td>18</td></tr>
</table>
The voice must match actual displayed evidence. Never read a sample result as an observed finding.
</details>

### Editor Actions

<details><summary><img src="https://img.shields.io/badge/EDITOR-Single_Focus_Cuts-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Plan script jobs and authenticated request</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Loaded by the plan</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Ran authenticated against</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>A loaded script does not prove an observed side effect</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Beat</th><th>Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut on pane switch. Thin square on the exact file/function, then clear it when the command appears.</td></tr>
<tr><td>First and second proof</td><td>One square around script list followed by a distinct arrow to the authenticated URL; never manufacture an unshown header result. Hold each focus 6–8s, then remove it immediately when switching.</td></tr>
<tr><td>Final PASS/report</td><td>Show the correct same-run output, not a static illustration. Align narrator line 3 with the actual decision field.</td></tr>
<tr><td>Evidence files</td><td>Compare `preflight-step-03.log` and `recorded-step-03.log`, retain raw proof and Actions run ID/SHA in the take manifest. Mismatch requires a retake.</td></tr>
</table></details>

### Proof Review

- **Proof:** Compare filmed output against the Developer's actual `deliverables/m2-demo1/logs/preflight-step-03.log`, plus the matching live GUI or GitHub Actions artifact
- **Learning:** Validate the purpose and mechanism above; a command-only video does not meet the objective
- **Release:** HOLD until evidence review; target overall score 98/100, never automatic approval

</details>
## Step 4 — Confirm the custom Python alert in the report

<details>
<summary><b>Open step 4 — where, command, output and production roles</b></summary>


### Learning Goal

A successful job could still omit the application-specific finding it was supposed to prove.

**What you are learning:** Validate authenticated security results in a CI report *(EO3a)*

### Demo Workspace


**Off-camera terminal setup:** Open VS Code integrated Terminal. Preserve any uncommitted work before changing branches. Paste these commands exactly; they select the demo starter and working folder.

```bash
cd "$HOME/pluralsight-script-development-with-zap"
git switch m2-demo1-before
cd "demos/module2-demos/m2-demo1-authenticated-zap-github-actions"
```

**Actual screen and browser check:** Show Actions run matching the recorded SHA and its report artifact with the named Python alert, protected profile, note parameter and risk.


**Open GitHub → Actions → latest matching authenticated scan run → Artifacts / scan report**. Keep the run's branch and SHA visible. Run the terminal step in VS Code.

### Run Command

**Where:** the VS Code integrated Terminal; inspect the actual GitHub Actions artifact separately. **Current folder:** `demos/module2-demos/m2-demo1-authenticated-zap-github-actions`.

```bash
./steps/04-confirm-authenticated-custom-alert.sh
```

### Expected Results

This is the existing script's **output field contract**, not a manufactured scan result. The field values containing angle brackets vary and must be taken from the real output.

<table><thead><tr><th>Output field</th><th>Expected value or example</th><th>What to inspect</th></tr></thead>
<tbody><tr><td><b>Alert</b></td><td><code>Globomantics unsafe reflection (custom rule)</code></td><td>Exact named Python finding</td></tr>
<tr><td><b>Risk</b></td><td><code>Medium</code></td><td>Current report rating</td></tr>
<tr><td><b>Parameter</b></td><td><code>note</code></td><td>Affected protected-page input</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS named custom alert recorded</code></td><td>Must be the script's alert, not built-in XSS</td></tr></tbody></table>

**Failure handling:** If the script reports FAIL, the required result is not established. Review the diagnostic and do not advance or substitute a prior run.

### Operator Decision

The report's named custom finding, risk and affected parameter connect the headless job to the original application-specific security check. A historical successful job does not prove a newer commit.

**How the investigation advances:** A repeatable authenticated CI report can now become a trusted source for API-driven decisions.

<!-- capture-location:start -->
<table><tr><th>Capture moment</th><th>Exact action and result location</th></tr><tr><td>Before Enter</td><td>Use VS Code integrated Terminal. Show the named step command already provided below/above; keep its full filename readable for about eight seconds. Directory and branch setup are off camera.</td></tr><tr><td>After Enter</td><td>After the local check, open the same hosted run, Artifacts, globo-ci-report; download and open the JSON in VS Code. Keep the run SHA available, not a historical report.</td></tr><tr><td>Evidence to record</td><td>Named custom finding, protected URL, note parameter and actual rating in that hosted report. Hold each meaningful field for six to eight seconds; retain the matching raw log and take ID.</td></tr><tr><td>Meaning and decision</td><td>Use the Spoken Narration for this exact field, then explain whether the evidence is enough to proceed. If it is absent, stop: neither a source declaration nor an expected output is an observed result.</td></tr><tr><td>Editor handoff</td><td>Mark the result region, then the actual value being explained. Clear old overlays on pane change. During an otherwise still explanation beyond 12 seconds, use one relevant 6–8-second takeaway callout; never invent a successful result.</td></tr></table>
<!-- capture-location:end -->

### Recorder Shots

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Precisely_What_To_Show-0284c7"/></summary>
<table>
<tr><th>Video Beat</th><th>Screen, Scroll, Hold And Proof</th></tr>
<tr><td>Source · 8s</td><td>GitHub Actions current run → Artifacts → globo-ci-report. Inspect actual report finding instance for `/account/profile` and `note`; terminal runs named verification step.</td></tr>
<tr><td>Command · 8s</td><td>Show the full named step command above; press Enter once without visible corrections. Any long scan wait is cut cleanly.</td></tr>
<tr><td>Output A · 6–8s</td><td>Highlight exact custom rule name, not built-in reflected XSS.</td></tr>
<tr><td>Output B · 6–8s</td><td>Box `Medium` and `note`, then show matching Actions fail-closed assertion and artifact name.</td></tr>
<tr><td>Completion · 6–8s</td><td>Hold the actual PASS and/or hosted evidence; on an important GUI click provide 8s before and 8s after in the source take.</td></tr>
</table></details>

### Spoken Narration

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Final_Spoken_Words-d946ef"/></summary>
<table><tr><th>Shot</th><th>Speak Exactly After Confirming The Screen</th><th>Words</th></tr>
<tr><td>Command</td><td>Inspect the report for the exact custom Python finding, not just the workflow's successful status.</td><td>15</td></tr>
<tr><td>Output A</td><td>Read the reported risk and note parameter from the current report. Never substitute an older successful scan for this commit's actual evidence.</td><td>22</td></tr>
<tr><td>Output B / decision</td><td>The pipeline explicitly asserts this custom name. A built-in XSS finding cannot replace the required application-specific rule.</td><td>17</td></tr>
</table>
The voice must match actual displayed evidence. Never read a sample result as an observed finding.
</details>

### Editor Actions

<details><summary><img src="https://img.shields.io/badge/EDITOR-Single_Focus_Cuts-16a34a"/></summary>
<p><b>Concrete Camtasia shot map — use actual values from the current recording, never sample values</b></p>
<table>
<tr><th>Moment</th><th>Exact action</th></tr>
<tr><td>Source then command</td><td>Cut code typing and corrections. Put one BLUE <code>#00A3FF</code> region box on the current source, then on the single named step command; remove the previous box on Enter. Source and command must be readable.</td></tr>
<tr><td>Real output appears</td><td>Cut long scan waiting. Put one BLUE region box around <b>Authenticated scan report custom alert</b>. Keep the actual table readable for about 6–8 seconds, not the entire desktop.</td></tr>
<tr><td>Primary evidence</td><td>Inside the box, use a small PINK <code>#FF1675</code> label/underline for the actual value of <code>Alert</code>. Read the captured result first. Missing field → HOLD, never draw a hypothetical number.</td></tr>
<tr><td>Cause/effect relationship</td><td>When both fields are visible in the same take, use a slim PURPLE <code>#770EF7</code> arrow toward the actual value of <code>Parameter</code>. Otherwise omit the arrow.</td></tr>
<tr><td>Only if still frame exceeds 12 seconds</td><td>If the narrator continues without a meaningful highlight, box or arrow change, show a short YELLOW <code>#FFC942</code> callout with Inky Blue text for 6–8 seconds: <b>A built-in alert does not replace the Python custom finding</b>. Omit this callout when focus already changes naturally.</td></tr>
<tr><td>Final</td><td>Remove all old highlights on pane change. Align with the approved AFTER-result narration beat, hold the real result, preserve eight-second raw handles around important clicks, and trim idle footage.</td></tr>
</table>
<p><b>Synchronize to Narrator:</b> The narrator's three lines immediately above govern the edits: BEFORE the command, DURING visible result, AFTER operator decision. After `narration-final.json` is imported into the batch portal, use the updated spoken lines rather than the old draft timings.</p>

<table><tr><th>Beat</th><th>Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut on pane switch. Thin square on the exact file/function, then clear it when the command appears.</td></tr>
<tr><td>First and second proof</td><td>Move a square from custom name to risk and parameter, then cut to the corresponding successful assertion in Actions. Hold each focus 6–8s, then remove it immediately when switching.</td></tr>
<tr><td>Final PASS/report</td><td>Show the correct same-run output, not a static illustration. Align narrator line 3 with the actual decision field.</td></tr>
<tr><td>Evidence files</td><td>Compare `preflight-step-04.log` and `recorded-step-04.log`, retain raw proof and Actions run ID/SHA in the take manifest. Mismatch requires a retake.</td></tr>
</table></details>

### Proof Review

- **Proof:** Compare filmed output against the Developer's actual `deliverables/m2-demo1/logs/preflight-step-04.log`, plus the matching live GUI or GitHub Actions artifact
- **Learning:** Validate the purpose and mechanism above; a command-only video does not meet the objective
- **Release:** HOLD until evidence review; target overall score 98/100, never automatic approval

</details>

## End the production take

Stop containers with `./scripts/demo_down.sh`, retain the before/after SHAs and proof, and deliver the take to the Editor. The Narrator uses the generated step transcripts plus the actual recorded output. Do not rerun the Developer's six-demo preflight in this per-demo process.

<!-- demo-navigation:start -->
<p align="center"><b>Author production guide · Demo 4 of 6</b></p>
<p align="center">
  <a href="m1-demo3.md"><img alt="Previous author guide: Module 1 Demo 3 — Python scanning and authentication" src="https://img.shields.io/badge/%E2%86%90_Previous-M1_Demo_3-130F25?style=for-the-badge"></a>
  <a href="m2-demo2.md"><img alt="Next author guide: Module 2 Demo 2 — ZAP API and reports" src="https://img.shields.io/badge/Next_%E2%86%92-M2_Demo_2-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->
