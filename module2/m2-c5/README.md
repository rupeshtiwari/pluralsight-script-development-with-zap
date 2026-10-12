# Enforce ZAP quality gates in GitHub Actions

Turn a ZAP scan into a build decision. Mark a known benign finding as a False
Positive, prove the plan applies that decision before scanning, then let ZAP's
`exitStatus` job convert the remaining alert risk into a process exit code — the
signal a pipeline uses to pass or block the build.

> **Authorization and scope.** The gate scans only the local Globomantics training
> app on the compose network. Never point it at any system you are not authorized
> to test.

## Applications and locations used

| Application | Where | Used for |
|-------------|-------|----------|
| macOS Terminal | working directory `module2/m2-c5` | running each `./scripts/demo_step.sh N` |
| Automation Framework gate plan | [`ci/gate-plan.yaml`](ci/gate-plan.yaml) | the filter, job order, and `exitStatus` thresholds |
| GitHub Actions | `https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/actions/workflows/zap-quality-gate.yml` → latest run → job **quality-gate** | showing the gate pass/fail the hosted build |
| CI artifact | run page → **Artifacts** → `globo-gate-report` | the archived gate report |

The gate workflow is `workflow_dispatch` (run it from the Actions tab). The exit
code is the build decision: `0` ok · `1` error · `2` warning.

## Setup

```bash
cd module2/m2-c5
./scripts/demo_up.sh             # prints "Up" when healthy
```

## Learning-objective coverage

| Step | Objective | Proof artifact |
|------|-----------|----------------|
| 1 | EO3c | False Positive alert filter |
| 2 | EO3c | Automation Framework job order |
| 3 | EO3c | Gate JSON report and exit code |
| 4 | EO3c | Filtered alert report |

## Step 1: Mark a benign finding as a False Positive (EO3c)

Goal: Record, once in config, that a known benign finding should not count against
the gate.

Application: macOS Terminal, with the gate plan open for reference.
Open / Navigate: Terminal in `module2/m2-c5`; the source is
[`ci/gate-plan.yaml`](ci/gate-plan.yaml) (`alertFilter` job).
Execute: `./scripts/demo_step.sh 1`.

Expected output: the plan marks rule `10021` (X-Content-Type-Options Header Missing)
as `newRisk: False Positive`, scoped to `http://app:8000/greet.*`.

What the learner should notice: the disposition lives in config, not in a person's
head — the gate ignores this noise the same way on every run.

Proof artifact: False Positive alert filter.

## Step 2: Confirm the job order applies the filter before scanning (EO3c)

Goal: Show the plan applies the filter before the scan and runs the gate last, so
every alert inherits the intended disposition.

Application: macOS Terminal, with the gate plan open for reference.
Open / Navigate: Terminal in `module2/m2-c5`; `ci/gate-plan.yaml` job list.
Execute: `./scripts/demo_step.sh 2`.

Expected output: job order `alertFilter -> requestor -> activeScan -> report ->
exitStatus`; `alertFilter` runs before `activeScan`; `exitStatus` runs last.

What the learner should notice: order is the mechanism — a filter applied after the
scan would be too late, and the gate must evaluate the final alert set.

Proof artifact: Automation Framework job order.

## Step 3: Run the gate and read the report plus exit code (EO3c)

Goal: Compare the remaining alerts against the thresholds and emit the process exit
code the pipeline blocks on.

Application: macOS Terminal, then GitHub Actions.
Open / Navigate: Terminal in `module2/m2-c5` (the step runs the gate headless and
captures `echo $?`). In CI, the **quality-gate** job's gate step shows the same exit
code decide the run.
Execute: `./scripts/demo_step.sh 3`.

Expected output: thresholds `errorLevel HIGH` · `warnLevel MEDIUM`; at least one
High-risk alert remains after filtering (this run reported 2); process exit code
`1`; the gate blocks the build.

What the learner should notice: a remaining High-risk alert maps, through
`errorLevel`, to a non-zero exit code — a scan result has become an automatic build
verdict.

Proof artifact: Gate JSON report and exit code.

## Step 4: Confirm the filtered report disposition (EO3c)

Goal: Prove the filter held — the benign finding now carries the False Positive
disposition while the real High finding remains, which is exactly why the gate
blocked.

Application: macOS Terminal, then GitHub Actions.
Open / Navigate: Terminal in `module2/m2-c5`. In CI, the downloadable
**`globo-gate-report`** artifact on the quality-gate run page.
Execute: `./scripts/demo_step.sh 4`.

Expected output: rule `10021` (X-Content-Type-Options Header Missing) disposed as
False Positive; rule `40012` (Cross Site Scripting (Reflected)) kept at High
(Medium); benign filtered out, High kept → build blocked.

What the learner should notice: filtering changed disposition, not the gate logic;
the gate still blocked on real risk, so noise suppression did not weaken the check.

Proof artifact: Filtered alert report.

## Validate and reset

`./scripts/preflight_check.sh` runs all four steps and writes a reviewable log to
`logs/`, ending with `5 checks passed, 0 failed`. Tear down with
`./scripts/demo_down.sh`.
