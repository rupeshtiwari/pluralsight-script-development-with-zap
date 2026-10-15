# M2-DEMO1 — Authenticated Headless ZAP in GitHub Actions

**Approved LO:** EO3a  
**Operator problem:** Maya needs the same authenticated script checks to execute unattended on ubuntu-24.04.  
**Demo folder:** `demos/module2-demos/m2-demo1-authenticated-zap-github-actions`  
**Branch pair:** `m2-demo1-before` and `m2-demo1-after`  
**Primary UI:** VS Code AF plan + integrated terminal; GitHub Actions authenticated-scan job and report artifact  
**Architecture diagram:** `docs/learner-diagrams/m2-demo1-architecture.svg`

## Run Preparation

From the repository root, run `./setup/setup-macos.sh` on a target Mac once, select the assigned branch, enter `demos/module2-demos/m2-demo1-authenticated-zap-github-actions` and follow its README setup command. Then run `./scripts/preflight_check.sh` and retain the timestamped `logs/` evidence. The local preflight is **not** equivalent to GitHub Actions proof when a hosted artifact is the outline requirement. Record a fresh take and reconcile evidence to the exact SHA and command.

## Step 1: run headless automation plan — EO3a

**Real-world problem:** A GUI-only scan cannot be reproduced on a CI runner

**Exact command from demo directory:**

```bash
./steps/01-run-headless-automation-plan.sh
```

**Recorder:** Show `ci/af-plan.yaml`, run headless step and open the actual hosted job. Hold the full legible command for 8–10 seconds before Enter. Highlight Show `zap.sh -cmd -autorun`, pinned ZAP digest, successful Actions job on current SHA. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** Completed Automation Framework plan and real Actions run success, not an old run. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** One YAML plan makes the authenticated test reproducible. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 96%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Step 2: inspect authenticated scan context — EO3a

**Real-world problem:** A blind headless scan may only see public endpoints

**Exact command from demo directory:**

```bash
./steps/02-inspect-authenticated-scan-context.sh
```

**Recorder:** Inspect AF plan `env.contexts` authentication/user/scope, then invoke named step. Hold the full legible command for 8–10 seconds before Enter. Highlight Focus on `Globomantics`, `authentication: script`, `alice`, and protected profile includePaths. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** Real context configuration and auth indicators; training username-only auth noted. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** Declare authentication and scope as environment data rather than clicking login. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 96%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Step 3: verify reused security scripts — EO3a

**Real-world problem:** CI must use the original authoring scripts, not substitutes

**Exact command from demo directory:**

```bash
./steps/03-verify-reused-security-scripts.sh
```

**Recorder:** Inspect AF script jobs and activeScan as Alice; invoke named step. Hold the full legible command for 8–10 seconds before Enter. Highlight Focus on JS sender, Python active rule and Jython login names, requestor `/account/profile?note=seed`. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** Actual loaded scripts and authenticated reflection; a marker side effect requires its own real request proof. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** Reuse source artifacts across execution environments without overclaiming effects. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 94%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Step 4: confirm authenticated custom alert — EO3a

**Real-world problem:** An unattended green job must still prove the custom application finding

**Exact command from demo directory:**

```bash
./steps/04-confirm-authenticated-custom-alert.sh
```

**Recorder:** Run named step, open report artifact on the same Actions SHA. Hold the full legible command for 8–10 seconds before Enter. Highlight Focus on exact custom alert name, profile URL and `note` parameter. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** Real JSON custom alert and hosted fail-closed assertion; not a built-in XSS stand-in. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** The pipeline should fail closed when this named script-created finding is missing. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 96%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Completion gate

Do not claim READY solely because a hosted action shows red or green. Inspect the report and return code, tie them to the exact current branch SHA and authorized Globomantics target, capture screenshot or job artifact ID, and complete Recorder/Narrator/Editor checks. If no live proof is available, mark it NOT VERIFIED and identify the next actual command.
