# M2-DEMO3 — Security Quality Gates · Recorder, Narrator And Editor

<div align="center">
![Recorder](https://img.shields.io/badge/RECORDER-Capture-0284c7?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-ElevenLabs-d946ef?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-Camtasia-16a34a?style=for-the-badge)

<img src="../learner-diagrams/m2-demo3-architecture.svg" width="100%" alt="Illustrative architecture of Security Quality Gates"/>

<sub>Illustration · Generated using ChatGPT · Author guidance is temporarily PUBLIC</sub>
</div>

## Operator Goal And Approved Objective

The Globomantics release gate must reclassify one scoped benign header finding while blocking real High-risk reflected XSS. The filter, scan order, actual report, and process exit must reconcile.

**Learning objective:** EO3c — Apply threshold-based quality gates for security findings in build pipelines

## Preflight FIRST — Enable Parallel Narration Work

Create a clean reference clone from the completed branch. **The starting branch is the Recorder's student exercise; it may intentionally omit the completed plan.** Use independent checkouts.

```bash
git clone -b m2-demo3-after https://github.com/rupeshtiwari/pluralsight-script-development-with-zap.git ~/zap-m2-demo3-reference
cd ~/zap-m2-demo3-reference
./setup/setup-macos.sh
cd demos/module2-demos/m2-demo3-security-quality-gates
./scripts/demo_up.sh
./scripts/preflight_check.sh
ls logs/preflight-step-0[1-4].log
```

Expect `5 checks passed, 0 failed` only if all four real named steps passed; narration references must **never** be produced from a failed run. Each named command uses the same actual step engine, with immutable evidence retained in `logs/.producer/`. This transcript is authoritative for **terminal fields**, not an observation of a separate GitHub Actions run or ZAP Script Console. Send the four step-specific logs and the corresponding GitHub/GUI proof to the Narrator. Teardown after evidence capture.

The Recorder clones [`m2-demo3-before`](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/tree/m2-demo3-before/demos/module2-demos/m2-demo3-security-quality-gates) independently, follows the demo README, completes missing source if required, and places the four approved preflight reference logs in the matching `logs/` folder before recording.

Set `DEMO_SYNC_MODE=1` and `DEMO_SYNC_PHASE=compare` off-camera. The visible terminal transcript can normalize live request IDs or request counts while saving raw values. **Risk, confidence, alert identity, HTTP status and process exit are never invented or normalized away.** A material mismatch stops the take rather than being hidden in Camtasia.

**Primary screens:** VS Code gate-plan.yaml and integrated Terminal; GitHub Actions quality-gate job and report artifact. Full screen only; use readable zoom. Hold each complete named command for **8 seconds** before Enter. Hold one evidence region for **6–8 seconds**; no idle final shot longer than ten seconds. Position pointer for ~8 seconds before and hold ~8 seconds after a major click in source footage, then trim in editing. Cut lengthy scanning waits cleanly.

## Step 1 — Inspect A Scoped False Positive Filter

**Problem and operator consequence:** A global ignore rule could hide unrelated security problems

**Exact command from `demos/module2-demos/m2-demo3-security-quality-gates`:**

```bash
./steps/01-inspect-false-positive-filter.sh
```

**Expected terminal fields from the existing script. Examples are illustrative; live values must come from the actual preflight and take:**

```text
Filtered rule (ruleId): 10021 (X-Content-Type-Options Header Missing)
New disposition (newRisk): False Positive
Scope (url): http://app:8000/greet.*
✔ PASS the plan marks the benign finding as a False Positive
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>VS Code: ci/gate-plan.yaml → alertFilter, near ruleId 10021, newRisk and URL; run named step</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/01-inspect-false-positive-filter.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Box ruleId 10021 and header alert name</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Move box to newRisk False Positive and URL /greet.*; the report is not checked yet</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Reclassify only the reviewed benign header finding. A blanket filter would conceal unrelated security risks.</td><td>15</td></tr>
<tr><td>Actual output A</td><td>Rule ten thousand twenty-one receives the False Positive disposition specifically for the greeting endpoint.</td><td>14</td></tr>
<tr><td>Actual output B</td><td>This proves the filter configuration. We still need the actual report to establish that its disposition took effect.</td><td>18</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>Separate squares on ID, newRisk and URL; use no persistent decoration after scrolling. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-01.log` and `logs/recorded-step-01.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

**Source-review confidence: 95%**. Do not inflate scores simply because documentation exists; release requires actual technical evidence.

---

## Step 2 — Verify Filter, Scan, Report And Gate Sequence

**Problem and operator consequence:** A filter added after scanning may not affect findings already raised

**Exact command from `demos/module2-demos/m2-demo3-security-quality-gates`:**

```bash
./steps/02-check-automation-job-order.sh
```

**Expected terminal fields from the existing script. Examples are illustrative; live values must come from the actual preflight and take:**

```text
Job order (ci/gate-plan.yaml): alertFilter -> requestor -> activeScan -> report -> exitStatus
alertFilter before activeScan: yes — later alerts inherit the disposition
exitStatus runs last: yes — the gate decides on the final alert set
✔ PASS the job order applies the filter before scanning and gates last
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>VS Code: ci/gate-plan.yaml → jobs list, keep five job names visible or scroll with short holds</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/02-check-automation-job-order.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Highlight alertFilter before activeScan</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Move arrow from report to exitStatus and show PASS</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Confirm the Automation Framework job order before running the gate. The filter must exist when the scan creates findings.</td><td>19</td></tr>
<tr><td>Actual output A</td><td>The report follows scanning, and exit status evaluates the resulting alert set at the end.</td><td>15</td></tr>
<tr><td>Actual output B</td><td>This sequence makes the policy repeatable. Moving the filter later could invalidate the intended noise suppression.</td><td>16</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>Show short arrow filter → scan, then another report → exitStatus. Only one arrow at any moment. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-02.log` and `logs/recorded-step-02.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

**Source-review confidence: 96%**. Do not inflate scores simply because documentation exists; release requires actual technical evidence.

---

## Step 3 — Prove A High-Risk Gate Exit Code

**Problem and operator consequence:** A red GitHub Actions job might be an infrastructure error, not a security decision

**Exact command from `demos/module2-demos/m2-demo3-security-quality-gates`:**

```bash
./steps/03-run-security-quality-gate.sh
```

**Expected terminal fields from the existing script. Examples are illustrative; live values must come from the actual preflight and take:**

```text
Gate thresholds (errorLevel · warnLevel): HIGH · MEDIUM
High-risk alerts after filtering: <positive count from current report>
Process exit code (echo $?): 1
Build decision: exit 1 → the gate BLOCKED the build
✔ PASS the gate exited 1 with at least one remaining High-risk alert
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>VS Code: gate-plan.yaml exitStatus errorLevel HIGH, warnLevel MEDIUM; Terminal run step; show current Actions gate log</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/03-run-security-quality-gate.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Square HIGH and MEDIUM thresholds, then the High count</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Box exact exit code 1 and matching High-risk report; verify no setup failure</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Set High as the error threshold and Medium as the warning threshold. Then run the actual headless gate.</td><td>18</td></tr>
<tr><td>Actual output A</td><td>At least one High-risk finding remains. That real finding must explain the build decision rather than an arbitrary failure.</td><td>19</td></tr>
<tr><td>Actual output B</td><td>The ZAP process exits one and blocks the build. A generic nonzero result would not establish the security cause.</td><td>19</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>Three distinct proof frames: threshold, positive High count, actual exit 1. Never use a red run icon alone. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-03.log` and `logs/recorded-step-03.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

**Source-review confidence: 84%**. Do not inflate scores simply because documentation exists; release requires actual technical evidence.

---

## Step 4 — Verify The Benign Finding And Remaining High In The Report

**Problem and operator consequence:** A successful filter configuration is not necessarily proof of applied disposition

**Exact command from `demos/module2-demos/m2-demo3-security-quality-gates`:**

```bash
./steps/04-verify-filtered-alert-report.sh
```

**Expected terminal fields from the existing script. Examples are illustrative; live values must come from the actual preflight and take:**

```text
Benign finding (rule 10021): X-Content-Type-Options Header Missing — Low (False Positive)
Real finding (rule 40012): Cross Site Scripting (Reflected) — High (Medium)
Gate outcome: benign filtered out, High kept → build blocked
✔ PASS the filtered report shows the benign finding disposed and the High kept
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>GitHub Actions → matching run → Artifacts → globo-gate-report, inspect pluginid 10021 and 40012; Terminal named report step</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/04-verify-filtered-alert-report.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Box 10021 and riskdesc containing False Positive</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Move box to 40012 High (Medium), then match exit 1. Must be actual same-run report</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Read the JSON report to confirm the scoped header alert received its False Positive disposition.</td><td>15</td></tr>
<tr><td>Actual output A</td><td>The reflected XSS finding remains High, with Medium confidence. Filtering the benign alert did not weaken the risk policy.</td><td>19</td></tr>
<tr><td>Actual output B</td><td>Those two records explain the blocked build. The report and process exit must represent the same run.</td><td>17</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>One rectangle on 10021 False Positive, then a separate one on 40012 High, then on exit 1. No fallbacks. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-04.log` and `logs/recorded-step-04.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

**Source-review confidence: 78%**. Do not inflate scores simply because documentation exists; release requires actual technical evidence.

---

## Editor / Narrator Handoff

Publish the frozen narration reference together with exact branch/commit SHA, four preflight step logs, filmed comparison logs, unmodified raw evidence, GUI or Actions run references, and each spoken line's corresponding video timecode. The author folder is intentionally temporary and publicly visible. Move it to private storage before the learner deliverable is finalized.
