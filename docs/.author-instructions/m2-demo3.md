# M2-DEMO3 — ZAP Security Quality Gates

**Approved LO:** EO3c  
**Operator problem:** Maya must suppress a demonstrated benign case without allowing a real high-risk XSS to pass the CI gate.  
**Demo folder:** `demos/module2-demos/m2-demo3-security-quality-gates`  
**Branch pair:** `m2-demo3-before` and `m2-demo3-after`  
**Primary UI:** VS Code `ci/gate-plan.yaml` + terminal; GitHub Actions quality-gate job and report artifact  
**Architecture diagram:** `docs/learner-diagrams/m2-demo3-architecture.svg`

## Run Preparation

From the repository root, run `./setup/setup-macos.sh` on a target Mac once, select the assigned branch, enter `demos/module2-demos/m2-demo3-security-quality-gates` and follow its README setup command. Then run `./scripts/preflight_check.sh` and retain the timestamped `logs/` evidence. The local preflight is **not** equivalent to GitHub Actions proof when a hosted artifact is the outline requirement. Record a fresh take and reconcile evidence to the exact SHA and command.

## Step 1: inspect false positive filter — EO3c

**Real-world problem:** Known benign issues should be scoped, not globally ignored

**Exact command from demo directory:**

```bash
./steps/01-inspect-false-positive-filter.sh
```

**Recorder:** Show `alertFilter` config and execute named inspection command. Hold the full legible command for 8–10 seconds before Enter. Highlight Focus on rule 10021, `newRisk: False Positive`, URL `http://app:8000/greet.*` and regex scope. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** Actual filter config; result requires report confirmation, not config alone. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** Precision noise suppression avoids weakening all other findings. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 95%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Step 2: check automation job order — EO3c

**Real-world problem:** Applying a filter after scanning may not change previously created alerts

**Exact command from demo directory:**

```bash
./steps/02-check-automation-job-order.sh
```

**Recorder:** Show order in plan, run named inspection. Hold the full legible command for 8–10 seconds before Enter. Highlight Focus on `alertFilter → requestor → activeScan → report → exitStatus`. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** Validated actual YAML job order; filter before alert generation, gate last. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** CI decisions are sensitive to sequencing. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 96%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Step 3: run security quality gate — EO3c

**Real-world problem:** Risk threshold must translate the remaining finding into a decisive process code

**Exact command from demo directory:**

```bash
./steps/03-run-security-quality-gate.sh
```

**Recorder:** Execute named headless gate; retain actual exit and complete log. Hold the full legible command for 8–10 seconds before Enter. Highlight Focus on `errorLevel HIGH`, `warnLevel MEDIUM`, observed exit code **1**, remaining High count. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** True exit code **1** plus actual High finding; any generic nonzero can be unrelated error. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** A deliberate security block differs from a broken runner or failed YAML parse. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 84%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Step 4: verify filtered alert report — EO3c

**Real-world problem:** A failed job is not enough evidence that the False Positive filter worked

**Exact command from demo directory:**

```bash
./steps/04-verify-filtered-alert-report.sh
```

**Recorder:** Inspect the real JSON report and current hosted Actions artifact. Hold the full legible command for 8–10 seconds before Enter. Highlight Focus on alert 10021 riskdesc `False Positive` and 40012 `High`; never show default placeholders as proven facts. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** Both actual alert records with correct dispositions, plus job failure attributed to High. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** Distinguish an intentionally blocked build from arbitrary scan failure. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 78%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Completion gate

Do not claim READY solely because a hosted action shows red or green. Inspect the report and return code, tie them to the exact current branch SHA and authorized Globomantics target, capture screenshot or job artifact ID, and complete Recorder/Narrator/Editor checks. If no live proof is available, mark it NOT VERIFIED and identify the next actual command.
