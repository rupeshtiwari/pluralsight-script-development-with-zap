# Enforce ZAP quality gates in GitHub Actions

Turn a ZAP scan into a build decision. Mark a known benign finding as a False
Positive, prove the plan applies that decision before scanning, then let ZAP's
`exitStatus` job convert the remaining alert risk into a process exit code — the
signal a pipeline uses to pass or block the build. You read the gate plan in VS
Code to see how each decision is encoded, then run it headless and read the verdict.

> **Authorization and scope.** The gate scans only the local Globomantics training
> app on the compose network. Never point it at any system you are not authorized
> to test.

## Applications and locations used

| Application | Where | Used for |
|-------------|-------|----------|
| VS Code | `demos/module2-demos/m2-demo3-security-quality-gates/ci/gate-plan.yaml` + the integrated terminal | reading the filter, job order, and thresholds, then running `./scripts/demo_step.sh N` |
| GitHub Actions | `https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/actions/workflows/zap-quality-gate.yml` → latest run → job **quality-gate** | the gate pass/fail on the hosted build |
| CI artifact | run page → **Artifacts** → `globo-gate-report` | the archived gate report |

The gate workflow is `workflow_dispatch` (run it from the Actions tab). The exit
code is the build decision: `0` ok · `1` error · `2` warning.

## Setup

```bash
cd demos/module2-demos/m2-demo3-security-quality-gates
./scripts/demo_up.sh             # prints "Up" when healthy
```

## Step-by-step LO traceability

| Step | LO | Config / mechanism (`ci/gate-plan.yaml`) | Command | Observed result | Proof artifact |
|------|----|------------------------------------------|---------|-----------------|----------------|
| 1 | EO3c | `alertFilter` 27–32 (ruleId `10021` → False Positive, url-scoped) | `steps/01-inspect-false-positive-filter.sh` | rule `10021` marked `newRisk: False Positive`, scoped to `/greet.*` | False Positive alert filter |
| 2 | EO3c | `jobs` order 24–64 | `steps/02-check-automation-job-order.sh` | `alertFilter → requestor → activeScan → report → exitStatus`; filter before scan, gate last | Automation Framework job order |
| 3 | EO3c | `exitStatus` 61–64 (`errorLevel HIGH`, `warnLevel MEDIUM`) | `steps/03-run-security-quality-gate.sh` | High-risk alert remains after filtering; process exit code `1`; build blocked | Gate JSON report and exit code |
| 4 | EO3c | `report` 51–56 output | `steps/04-verify-filtered-alert-report.sh` | `10021` disposed False Positive; `40012` kept High | Filtered alert report |

---

## Step 1: Mark a benign finding as a False Positive (EO3c)

**The problem.** A quality gate must ignore noise it has already judged benign, and
that decision has to live in config — not in a person's memory — so every run
applies it the same way.

**Inspect the plan in VS Code.** Open `demos/module2-demos/m2-demo3-security-quality-gates/ci/gate-plan.yaml` →
`alertFilter` job (lines 27–32):

- **`ruleId: 10021`** — X-Content-Type-Options Header Missing, the known-benign
  finding for this app.
- **`newRisk: "False Positive"`** — the disposition the filter assigns.
- **`url` / `urlRegex`** — scoped to `http://app:8000/greet.*`, so only this finding
  on this path is reclassified.

**Execute.**

```bash
./steps/01-inspect-false-positive-filter.sh
```

**Inspect the actual evidence.** The plan marks rule `10021` as
`newRisk: False Positive`, scoped to `http://app:8000/greet.*`.

**The engineer's decision.** The disposition lives in config, so the gate ignores
this noise identically on every run.

Proof artifact: False Positive alert filter.

---

## Step 2: Confirm the job order applies the filter before scanning (EO3c)

**The problem.** A filter applied *after* the scan would be too late to change the
alerts the gate sees. Order is the mechanism.

**Inspect the plan in VS Code.** In the same file, the `jobs` list (lines 24–64) runs
in order: `alertFilter` → `requestor` → `activeScan` → `report` → `exitStatus`. The
filter precedes the scan, so every alert the scan raises inherits the intended
disposition; `exitStatus` is last, so the gate evaluates the final alert set.

**Execute.**

```bash
./steps/02-check-automation-job-order.sh
```

**Inspect the actual evidence.** The step reports the job order
`alertFilter -> requestor -> activeScan -> report -> exitStatus`, confirming
`alertFilter` runs before `activeScan` and `exitStatus` runs last.

**The engineer's decision.** Because the filter is applied before scanning and the
gate runs last, the disposition is already in effect when the gate makes its call.

Proof artifact: Automation Framework job order.

---

## Step 3: Run the gate and read the report plus exit code (EO3c)

**The problem.** The remaining alerts must be compared against thresholds and turned
into the one signal a pipeline blocks on — a process exit code.

**Inspect the plan in VS Code.** The `exitStatus` job (lines 61–64) sets
`errorLevel: "HIGH"` and `warnLevel: "MEDIUM"`: a High alert is at or above
`errorLevel`, so the run must exit non-zero (process result: `0` ok, `1` error,
`2` warning).

**Execute.**

```bash
./steps/03-run-security-quality-gate.sh
```

**Inspect the actual evidence.** With thresholds `errorLevel HIGH` · `warnLevel
MEDIUM`, at least one High-risk alert (the reflected-XSS finding) remains after
filtering, the process exits `1`, and the gate blocks the build. In CI, the
**quality-gate** job's gate step shows the same exit code decide the run.

**The engineer's decision.** A remaining High-risk alert maps, through `errorLevel`,
to a non-zero exit code — the scan result has become an automatic build verdict.

Proof artifact: Gate JSON report and exit code.

---

## Step 4: Confirm the filtered report disposition (EO3c)

**The problem.** Maya must prove the filter held — that the benign finding now
carries the False Positive disposition while the real High finding remains, which is
exactly why the gate blocked.

**Execute.**

```bash
./steps/04-verify-filtered-alert-report.sh
```

**Inspect the actual evidence.** In the gate report, rule `10021`
(X-Content-Type-Options Header Missing) is disposed as False Positive, while rule
`40012` (Cross Site Scripting (Reflected)) is kept at High risk — benign filtered
out, High kept → build blocked. In CI this is the downloadable `globo-gate-report`
artifact on the quality-gate run page.

**The engineer's decision.** Filtering changed disposition, not the gate logic; the
gate still blocked on real risk, so noise suppression did not weaken the check.

Proof artifact: Filtered alert report.

## Validate and reset

`./scripts/preflight_check.sh` runs all four steps and writes a reviewable log to
`logs/`, ending with `5 checks passed, 0 failed`. Tear down with
`./scripts/demo_down.sh`.
