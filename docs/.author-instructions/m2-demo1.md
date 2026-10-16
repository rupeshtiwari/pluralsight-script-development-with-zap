# M2-DEMO1 · Authenticated ZAP in GitHub Actions — Author Production Playbook

<div align="center">

![Recorder](https://img.shields.io/badge/Recorder-Exact_Screen-0284c7?style=for-the-badge)
![Narrator](https://img.shields.io/badge/Narrator-Verified_Script-9333ea?style=for-the-badge)
![Editor](https://img.shields.io/badge/Editor-Timed_Highlights-16a34a?style=for-the-badge)

<img src="../learner-diagrams/m2-demo1-architecture.svg" alt="Illustrative Authenticated ZAP in GitHub Actions workflow" width="100%"/>

<sub>Generated using ChatGPT · Temporary PUBLIC author guidance</sub>

</div>

[← **All Six Production Playbooks**](README.md) · [**Student Starter README ↗**](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo1-before/demos/module2-demos/m2-demo1-authenticated-zap-github-actions/README.md) · [**Completed README ↗**](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo1-after/demos/module2-demos/m2-demo1-authenticated-zap-github-actions/README.md)

## Recording Assignment

<table>
<tr><th>Field</th><th>Exact Value</th></tr>
<tr><td>Demonstration</td><td><b>Authenticated ZAP in GitHub Actions</b> · m2-demo1</td></tr>
<tr><td>Approved Objectives</td><td>EO3a — check the complete wording in the linked learner README</td></tr>
<tr><td>Reference branch</td><td><code>m2-demo1-after</code> — completed source for preflight</td></tr>
<tr><td>Recording branch</td><td><code>m2-demo1-before</code> — follow the student workflow</td></tr>
<tr><td>Demo directory</td><td><code>demos/module2-demos/m2-demo1-authenticated-zap-github-actions</code></td></tr>
<tr><td>Student exercise state</td><td>The starter intentionally omits ci/af-plan.yaml; create it during the recorded exercise</td></tr>
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
git switch m2-demo1-after
git rev-parse HEAD
cd demos/module2-demos/m2-demo1-authenticated-zap-github-actions
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
mkdir -p ~/zap-production-evidence/m2-demo1
cp logs/preflight-step-0[1-4].log ~/zap-production-evidence/m2-demo1/
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
git switch m2-demo1-before
git rev-parse HEAD
cd demos/module2-demos/m2-demo1-authenticated-zap-github-actions
cp ~/zap-production-evidence/m2-demo1/preflight-step-0[1-4].log logs/
./scripts/demo_up.sh

# Off-camera recording parity settings
export DEMO_SYNC_MODE=1
export DEMO_SYNC_PHASE=compare
```

**The starter intentionally omits ci/af-plan.yaml; create it during the recorded exercise.** Follow the [student README on this exact starter branch](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m2-demo1-before/demos/module2-demos/m2-demo1-authenticated-zap-github-actions/README.md) to complete any required source writing, then record the four exact commands listed below. The starter branch may be intentionally incomplete and **must not** be expected to pass its final checks before the work has been done.

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
git switch m2-demo2-after
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

## Step 1 — Execute The Headless Automation Framework Plan

**Operator reason:** A desktop-only scan is not reproducible on a hosted runner.

```bash
./steps/01-run-headless-automation-plan.sh
```

**Expected output fields from the real step engine — EXAMPLE STRUCTURE, not a live capture:**

```text
Runner (CI): ubuntu-24.04 · ghcr.io/zaproxy/zaproxy:stable
Command: zap.sh -cmd -autorun /zap/wrk/af-plan.yaml (headless)
✔ PASS the plan ran headless to completion with no errors
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Precisely_What_To_Show-0284c7"/></summary>
<table>
<tr><th>Video Beat</th><th>Screen, Scroll, Hold And Proof</th></tr>
<tr><td>Source · 8s</td><td>VS Code: ci/af-plan.yaml at the top-level jobs, then GitHub Actions → Globomantics authenticated ZAP scan → job authenticated-scan. Show correct branch and SHA.</td></tr>
<tr><td>Command · 8s</td><td>Show the full named step command above; press Enter once without visible corrections. Any long scan wait is cut cleanly.</td></tr>
<tr><td>Output A · 6–8s</td><td>Box the runner platform and `zap.sh -cmd -autorun` command, then show the current Actions run.</td></tr>
<tr><td>Output B · 6–8s</td><td>Move highlight to green hosted plan step and the actual commit SHA. Do not use an older green job as current proof.</td></tr>
<tr><td>Completion · 6–8s</td><td>Hold the actual PASS and/or hosted evidence; on an important GUI click provide 8s before and 8s after in the source take.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Final_Spoken_Words-d946ef"/></summary>
<table><tr><th>Shot</th><th>Speak Exactly After Confirming The Screen</th><th>Words</th></tr>
<tr><td>Command</td><td>Run the Automation Framework plan headlessly so ZAP can assess Globomantics without clicking through a desktop interface.</td><td>17</td></tr>
<tr><td>Output A</td><td>The runner uses Ubuntu twenty-four oh-four and starts ZAP from the pinned container image with autorun.</td><td>16</td></tr>
<tr><td>Output B / decision</td><td>The completed job proves the plan executed. Always match the run's commit to the reference used during recording.</td><td>18</td></tr>
</table>
The voice must match actual displayed evidence. Never read a sample result as an observed finding.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Single_Focus_Cuts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut on pane switch. Thin square on the exact file/function, then clear it when the command appears.</td></tr>
<tr><td>First and second proof</td><td>Use a square on `-autorun`, an arrow to Actions' scan step, then a separate short callout around the matching SHA. Hold each focus 6–8s, then remove it immediately when switching.</td></tr>
<tr><td>Final PASS/report</td><td>Show the correct same-run output, not a static illustration. Align narrator line 3 with the actual decision field.</td></tr>
<tr><td>Evidence files</td><td>Compare `preflight-step-01.log` and `recorded-step-01.log`, retain raw proof and Actions run ID/SHA in the take manifest. Mismatch requires a retake.</td></tr>
</table></details>

**Source-review confidence 96%** · final runtime readiness still requires the named real evidence.

---

## Step 2 — Bind A Scripted User And Authorized Scope

**Operator reason:** A headless test that never logs in may miss the protected page.

```bash
./steps/02-inspect-authenticated-scan-context.sh
```

**Expected output fields from the real step engine — EXAMPLE STRUCTURE, not a live capture:**

```text
Context: Globomantics
Authentication: script-based → globomantics-auth (Login URL: /login)
User: alice
Target scope: http://app:8000 (profile + greet paths)
✔ PASS the plan binds context + scripted auth + user + scope before scanning
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Precisely_What_To_Show-0284c7"/></summary>
<table>
<tr><th>Video Beat</th><th>Screen, Scroll, Hold And Proof</th></tr>
<tr><td>Source · 8s</td><td>VS Code: ci/af-plan.yaml → env.contexts, authentication script and loggedInRegex, users alice, includePaths. Scroll one section at a time; zoom until key names fit without wraps.</td></tr>
<tr><td>Command · 8s</td><td>Show the full named step command above; press Enter once without visible corrections. Any long scan wait is cut cleanly.</td></tr>
<tr><td>Output A · 6–8s</td><td>Box `Globomantics` and script-based authentication; point to Login URL `/login`.</td></tr>
<tr><td>Output B · 6–8s</td><td>Scroll gently to `alice` and the include paths, then show the corresponding terminal output.</td></tr>
<tr><td>Completion · 6–8s</td><td>Hold the actual PASS and/or hosted evidence; on an important GUI click provide 8s before and 8s after in the source take.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Final_Spoken_Words-d946ef"/></summary>
<table><tr><th>Shot</th><th>Speak Exactly After Confirming The Screen</th><th>Words</th></tr>
<tr><td>Command</td><td>Define the authenticated context before scanning, so the hosted runner knows how to log in without manual steps.</td><td>18</td></tr>
<tr><td>Output A</td><td>The authentication script obtains the session for user Alice, while the plan restricts testing to the authorized endpoints.</td><td>18</td></tr>
<tr><td>Output B / decision</td><td>Those settings decide coverage. A scanner that cannot reach the protected profile cannot substantiate its security findings.</td><td>17</td></tr>
</table>
The voice must match actual displayed evidence. Never read a sample result as an observed finding.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Single_Focus_Cuts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut on pane switch. Thin square on the exact file/function, then clear it when the command appears.</td></tr>
<tr><td>First and second proof</td><td>Sequential boxes for authentication, users and includePaths; clear earlier boxes at each scroll or pane change. Hold each focus 6–8s, then remove it immediately when switching.</td></tr>
<tr><td>Final PASS/report</td><td>Show the correct same-run output, not a static illustration. Align narrator line 3 with the actual decision field.</td></tr>
<tr><td>Evidence files</td><td>Compare `preflight-step-02.log` and `recorded-step-02.log`, retain raw proof and Actions run ID/SHA in the take manifest. Mismatch requires a retake.</td></tr>
</table></details>

**Source-review confidence 96%** · final runtime readiness still requires the named real evidence.

---

## Step 3 — Reuse JavaScript And Jython Scripts Under Authentication

**Operator reason:** Duplicating script implementations in CI invites drift.

```bash
./steps/03-verify-reused-security-scripts.sh
```

**Expected output fields from the real step engine — EXAMPLE STRUCTURE, not a live capture:**

```text
Loaded by the plan: globomantics-marker (JS) · globomantics-active-rule (Py) · globomantics-auth (Py)
Ran authenticated against: /account/profile — reflection reached while logged in
✔ PASS the scripts executed against the authenticated scope
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Precisely_What_To_Show-0284c7"/></summary>
<table>
<tr><th>Video Beat</th><th>Screen, Scroll, Hold And Proof</th></tr>
<tr><td>Source · 8s</td><td>VS Code: ci/af-plan.yaml → script add/enable jobs, then requestor `account/profile?note=seed` and activeScan as context user. If needed open paths to original JS and Python sources.</td></tr>
<tr><td>Command · 8s</td><td>Show the full named step command above; press Enter once without visible corrections. Any long scan wait is cut cleanly.</td></tr>
<tr><td>Output A · 6–8s</td><td>Box the three loaded script names, one source group at a time.</td></tr>
<tr><td>Output B · 6–8s</td><td>Show authenticated `/account/profile` with `note`, then actual PASS. Sender-header side effects need separate request proof.</td></tr>
<tr><td>Completion · 6–8s</td><td>Hold the actual PASS and/or hosted evidence; on an important GUI click provide 8s before and 8s after in the source take.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Final_Spoken_Words-d946ef"/></summary>
<table><tr><th>Shot</th><th>Speak Exactly After Confirming The Screen</th><th>Words</th></tr>
<tr><td>Command</td><td>Reuse the original JavaScript sender, Python active rule, and login script rather than rebuilding their behavior for CI.</td><td>18</td></tr>
<tr><td>Output A</td><td>The requestor accesses the protected profile as Alice, enabling the custom rule to inspect the note parameter.</td><td>17</td></tr>
<tr><td>Output B / decision</td><td>Script loading and authenticated reflection are proven here. A specific sender header would require its own request evidence.</td><td>18</td></tr>
</table>
The voice must match actual displayed evidence. Never read a sample result as an observed finding.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Single_Focus_Cuts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut on pane switch. Thin square on the exact file/function, then clear it when the command appears.</td></tr>
<tr><td>First and second proof</td><td>One square around script list followed by a distinct arrow to the authenticated URL; never manufacture an unshown header result. Hold each focus 6–8s, then remove it immediately when switching.</td></tr>
<tr><td>Final PASS/report</td><td>Show the correct same-run output, not a static illustration. Align narrator line 3 with the actual decision field.</td></tr>
<tr><td>Evidence files</td><td>Compare `preflight-step-03.log` and `recorded-step-03.log`, retain raw proof and Actions run ID/SHA in the take manifest. Mismatch requires a retake.</td></tr>
</table></details>

**Source-review confidence 94%** · final runtime readiness still requires the named real evidence.

---

## Step 4 — Prove The Named Custom Alert Reached The CI Report

**Operator reason:** A green CI result is not proof that the intended rule found the issue.

```bash
./steps/04-confirm-authenticated-custom-alert.sh
```

**Expected output fields from the real step engine — EXAMPLE STRUCTURE, not a live capture:**

```text
Alert: Globomantics unsafe reflection (custom rule)
Risk: Medium
Parameter: note
✔ PASS the custom rule raised its named alert under the authenticated AF run
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Precisely_What_To_Show-0284c7"/></summary>
<table>
<tr><th>Video Beat</th><th>Screen, Scroll, Hold And Proof</th></tr>
<tr><td>Source · 8s</td><td>GitHub Actions current run → Artifacts → globo-ci-report. Inspect actual report finding instance for `/account/profile` and `note`; terminal runs named verification step.</td></tr>
<tr><td>Command · 8s</td><td>Show the full named step command above; press Enter once without visible corrections. Any long scan wait is cut cleanly.</td></tr>
<tr><td>Output A · 6–8s</td><td>Highlight exact custom rule name, not built-in reflected XSS.</td></tr>
<tr><td>Output B · 6–8s</td><td>Box `Medium` and `note`, then show matching Actions fail-closed assertion and artifact name.</td></tr>
<tr><td>Completion · 6–8s</td><td>Hold the actual PASS and/or hosted evidence; on an important GUI click provide 8s before and 8s after in the source take.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Final_Spoken_Words-d946ef"/></summary>
<table><tr><th>Shot</th><th>Speak Exactly After Confirming The Screen</th><th>Words</th></tr>
<tr><td>Command</td><td>Inspect the report for the exact custom Python finding, not just the workflow's successful status.</td><td>15</td></tr>
<tr><td>Output A</td><td>The finding identifies the protected profile's note parameter, and the reported risk is Medium.</td><td>14</td></tr>
<tr><td>Output B / decision</td><td>The pipeline explicitly asserts this custom name. A built-in XSS finding cannot replace the required application-specific rule.</td><td>17</td></tr>
</table>
The voice must match actual displayed evidence. Never read a sample result as an observed finding.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Single_Focus_Cuts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut on pane switch. Thin square on the exact file/function, then clear it when the command appears.</td></tr>
<tr><td>First and second proof</td><td>Move a square from custom name to risk and parameter, then cut to the corresponding successful assertion in Actions. Hold each focus 6–8s, then remove it immediately when switching.</td></tr>
<tr><td>Final PASS/report</td><td>Show the correct same-run output, not a static illustration. Align narrator line 3 with the actual decision field.</td></tr>
<tr><td>Evidence files</td><td>Compare `preflight-step-04.log` and `recorded-step-04.log`, retain raw proof and Actions run ID/SHA in the take manifest. Mismatch requires a retake.</td></tr>
</table></details>

**Source-review confidence 96%** · final runtime readiness still requires the named real evidence.

---

## Production Handoff

Deliver before/after SHAs, four preflight references, raw logs, recording comparison logs, correct GitHub Actions run URL and report, ElevenLabs audio, and editor timecodes. Every claim must have the actual observed on-screen proof. This playbook is temporarily public and must be moved to a private production workspace before student release.
