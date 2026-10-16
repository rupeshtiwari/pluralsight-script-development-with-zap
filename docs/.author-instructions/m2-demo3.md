# M2-DEMO3 · Security Quality Gates — Author Production Playbook

<div align="center">

![Recorder](https://img.shields.io/badge/Recorder-Exact_Screen-0284c7?style=for-the-badge)
![Narrator](https://img.shields.io/badge/Narrator-Verified_Script-9333ea?style=for-the-badge)
![Editor](https://img.shields.io/badge/Editor-Timed_Highlights-16a34a?style=for-the-badge)

<img src="../learner-diagrams/m2-demo3-architecture.svg" alt="Illustrative Security Quality Gates workflow" width="100%"/>

<sub>Generated using ChatGPT · Temporary PUBLIC author guidance</sub>

</div>

[← **All Six Production Playbooks**](README.md) · [**Student Starter README ↗**](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo3-before/demos/module2-demos/m2-demo3-security-quality-gates/README.md) · [**Completed README ↗**](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo3-after/demos/module2-demos/m2-demo3-security-quality-gates/README.md)

## Recording Assignment

<table>
<tr><th>Field</th><th>Exact Value</th></tr>
<tr><td>Demonstration</td><td><b>Security Quality Gates</b> · m2-demo3</td></tr>
<tr><td>Approved Objectives</td><td>EO3c — check the complete wording in the linked learner README</td></tr>
<tr><td>Reference branch</td><td><code>m2-demo3-after</code> — completed source for preflight</td></tr>
<tr><td>Recording branch</td><td><code>m2-demo3-before</code> — follow the student workflow</td></tr>
<tr><td>Demo directory</td><td><code>demos/module2-demos/m2-demo3-security-quality-gates</code></td></tr>
<tr><td>Student exercise state</td><td>The starter intentionally omits ci/gate-plan.yaml; create the finished plan before testing</td></tr>
</table>

## Start Here — One Clone, Two Branches, One Demo

**Do not clone this repository separately for every demo.** Each recorder clones the course once, then switches to the specific demo's `after` branch for preflight and `before` branch for recording. Before switching, stop the old demo environment and preserve the narration references.

<details open>
<summary><b><font color="#0284c7">A · Clone Once and Prepare the Mac</font></b></summary>

Use this step only for your first assigned demo. For second and third demos, keep the same repository folder and skip the clone/setup if already complete.

```bash
cd ~
git clone https://github.com/rupeshtiwari/pluralsight-script-development-with-zap.git
cd pluralsight-script-development-with-zap
./setup/setup-macos.sh
git fetch origin
```

**Where is the folder?** It is `~/pluralsight-script-development-with-zap` by default. `git switch` does not create a second or third folder; it changes the checked-out branch in the same directory.

</details>

<details open>
<summary><b><font color="#9333ea">B · Run Preflight From the Completed Branch FIRST</font></b></summary>

This is the **narration evidence source**. It executes all four real named commands, saves raw live proof, and produces stable per-step reference logs so the Narrator can start while footage is still being recorded.

```bash
cd ~/pluralsight-script-development-with-zap
git status --short
git fetch origin
git switch m2-demo3-after
git rev-parse HEAD
cd demos/module2-demos/m2-demo3-security-quality-gates
./scripts/demo_up.sh
./scripts/preflight_check.sh
ls -l logs/preflight-step-0[1-4].log
```

**Only proceed when preflight exits 0 and prints the actual summary below** (this is the expected format, not a fabricated test run):

```text
RESULT: 5 checks passed, 0 failed
REFERENCE: logs/preflight-step-01.log through logs/preflight-step-04.log
```

**Proof stays real:** `logs/preflight-step-01.log` through `04.log` are the Narrator's four outputs. `logs/.producer/` holds untouched raw details. Separate ZAP GUI / GitHub Actions evidence must be checked independently when a terminal command cannot observe it.

**Optional but strongly recommended repeatability check:** after successful preflight, set `DEMO_SYNC_MODE=1` and `DEMO_SYNC_PHASE=compare` off-camera, then execute the same four named steps while still on this completed reference. Each must match its baseline; a material mismatch blocks recording.

**Archive the references and stop the stack before switching:**

```bash
mkdir -p ~/zap-production-evidence/m2-demo3
cp logs/preflight-step-0[1-4].log ~/zap-production-evidence/m2-demo3/
./scripts/demo_down.sh
cd ~/pluralsight-script-development-with-zap
git status --short
```

Never delete the reference logs with a destructive Git cleanup.

</details>

<details open>
<summary><b><font color="#0284c7">C · Switch to the Student Starting Branch and Record</font></b></summary>

```bash
cd ~/pluralsight-script-development-with-zap
git switch m2-demo3-before
git rev-parse HEAD
cd demos/module2-demos/m2-demo3-security-quality-gates
cp ~/zap-production-evidence/m2-demo3/preflight-step-0[1-4].log logs/
./scripts/demo_up.sh

# Off-camera recording parity settings
export DEMO_SYNC_MODE=1
export DEMO_SYNC_PHASE=compare
```

**The starter intentionally omits ci/gate-plan.yaml; create the finished plan before testing.** Follow the [student README on this exact starter branch](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo3-before/demos/module2-demos/m2-demo3-security-quality-gates/README.md) to complete any required source writing, then record the four exact commands listed below. The starter branch may be intentionally incomplete and **must not** be expected to pass its final checks before the work has been done.

After the four named commands, capture the GUI/CI proof, then:

```bash
./scripts/demo_down.sh
cd ~/pluralsight-script-development-with-zap
git status --short
```

**If Git refuses the next branch switch:** preserve the changed code on a task branch or in a deliberate backup before switching. Do not use force/reset to discard recorded work.

</details>

<details><summary><b><font color="#16a34a">D · Recording More Demos From This Same Clone</font></b></summary>

```bash
cd ~/pluralsight-script-development-with-zap
git status --short
git fetch origin
# Example: select another assigned demo (replace as needed):
git switch m1-demo1-after
```

For a different demo, replace the branch and folder with the corresponding entry on the [six-demo author dashboard](README.md). Repeat preflight → archive logs → cleanup → branch switch → record. One local repository is sufficient for sequential recordings. A separate worktree is optional when you need two branches open concurrently.

</details>

## Camera, Narration and Edit Contract

<table>
<tr><td width="18%"><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/></td><td>Record full-screen at readable zoom. Open the source/GUI pane specified in the relevant step, then hold the complete named command ~8 seconds before Enter. Hold each actual output focus 6–8 seconds. On significant UI clicks provide 8-second pre-click and post-click handles in raw footage for the editor.</td></tr>
<tr><td><img src="https://img.shields.io/badge/NARRATOR-Purple-9333ea"/></td><td>Use the real `preflight-step-0N.log` plus the corresponding filmed GUI/CI evidence. The step tables below give exact ElevenLabs lines with word counts, one mechanism and one operator consequence per reveal. Do not narrate sample placeholders.</td></tr>
<tr><td><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/></td><td>Cut cleanly at source/terminal/GUI transitions and scanning waits. Highlight one field using a small square, arrow or callout; remove it immediately as the focus changes. Match voice to the same take, not a historic preflight value from a different implementation.</td></tr>
</table>

## Four Fixed Teaching Steps — Follow In Order

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
