# Enforce ZAP Quality Gates in GitHub Actions

In this lab you turn a ZAP scan into a **build decision**. You mark a known
benign finding as a False Positive, prove the plan applies that decision *before*
scanning, then let ZAP's `exitStatus` job convert the remaining alert risk into a
**process exit code** — the signal a pipeline uses to pass or block the build.

---

## The problem you are solving

A scan that only produces a report changes nothing — someone still has to read it
and decide. A real pipeline needs an **automatic verdict**: given this scan, does
the build go through or stop? But raw scans are noisy, so the gate must first set
aside findings you have already judged benign, then weigh what remains against a
threshold. Get this right and security becomes a pass/fail check like any test.

**What you gain:** you can filter known-benign noise once in config, then gate the
build on real risk automatically — turning ZAP from a reporting tool into an
enforcement point in your pipeline.

> **Authorization and scope.** The gate scans **only** the local Globomantics
> training app on the compose network. Never point it at any system you are not
> authorized to test.

---

## How to read this lab

| Label | Meaning |
|-------|---------|
| 💻 **Run in your terminal** | Copy-paste this command. |
| ✅ **You'll see** | A **result to read** — confirm it. **Never type it as a command.** |

> **Golden rule:** the only thing you *type* is the line under 💻. Everything under
> ✅ is output you *read*.

---

## What you will use (reference)

| Piece | Value |
|-------|-------|
| Gate plan | ZAP Automation Framework — [`ci/gate-plan.yaml`](ci/gate-plan.yaml) |
| Workflow | [`.github/workflows/zap-quality-gate.yml`](../../.github/workflows/zap-quality-gate.yml) |
| Filtered (benign) | rule `10021` — X-Content-Type-Options Header Missing → **False Positive** |
| Gated (real) | rule `40012` — Cross Site Scripting (Reflected), **High** |
| Gate thresholds | `errorLevel: HIGH` · `warnLevel: MEDIUM` |
| Decision | process exit code — `0` ok · `1` error · `2` warning |

---

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Mark a benign finding **False Positive** in config | EO3c | False Positive alert filter |
| 2 | Confirm the **job order** applies the filter before scanning | EO3c | Automation Framework job order |
| 3 | Run `exitStatus` and read the **report plus exit code** | EO3c | Gate JSON report and exit code |
| 4 | Confirm the **filtered report** disposition and the kept High | EO3c | Filtered alert report |

---

## Run it step by step

Bring the stack up once, then run each step on its own screen. Each command
prints a header saying **what** it shows and **why**, then a green **PASS**.

```bash
cd module2/m2-c5-enforce-zap-quality-gates-in-github-actions
./scripts/demo_up.sh        # wait for "Up" (starts Colima + the stack if needed)
./scripts/demo_step.sh 1    # False Positive alert filter
./scripts/demo_step.sh 2    # Automation Framework job order
./scripts/demo_step.sh 3    # Gate JSON report and exit code
./scripts/demo_step.sh 4    # Filtered alert report
```

Steps 1–2 read the plan. Step 3 runs the gate headless and captures the exit
code; step 4 reads that run's report. (To validate all four at once, run
`./scripts/preflight_check.sh`; when finished, `./scripts/demo_down.sh`.)

---

## Step 1 — Mark a benign finding as a False Positive

A gate must ignore noise it has already judged benign. The `alertFilter` job
records that decision once, in the plan.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 1
```

✅ **You'll see** the plan mark the benign header finding as a False Positive
(output — read it, don't type it):

```text
WHAT: A known benign finding is marked False Positive — by config
  ★ Filtered rule  (ruleId): 10021  (X-Content-Type-Options Header Missing)
  ★ New disposition  (newRisk): False Positive
  ★ Scope  (url): http://app:8000/greet.*
✔ PASS  the plan marks the benign finding as a False Positive
```

**Proof artifact:** *False Positive alert filter.*

---

## Step 2 — Confirm the job order applies the filter before scanning

A filter applied *after* scanning would be too late. The plan's job order makes
the disposition apply to every alert, and runs the gate last.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 2
```

✅ **You'll see** the filter run before the scan, and the gate run last (output —
read it, don't type it):

```text
WHAT: Order matters: filter BEFORE scan, gate LAST
  ★ Job order (ci/gate-plan.yaml): alertFilter -> requestor -> activeScan -> report -> exitStatus
  ★ alertFilter before activeScan: yes — later alerts inherit the disposition
  ★ exitStatus runs last: yes — the gate decides on the final alert set
✔ PASS  the job order applies the filter before scanning and gates last
```

**Proof artifact:** *Automation Framework job order.*

---

## Step 3 — Run the gate and read the report plus exit code

`exitStatus` compares the remaining alerts against the thresholds and sets the
**process exit code** — the signal a pipeline blocks on.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 3
```

✅ **You'll see** the gate turn the High-risk alert into a non-zero exit code
(output — read it, don't type it):

```text
WHAT: The gate turns alert risk into a build decision
  ★ Gate thresholds  (errorLevel · warnLevel): HIGH · MEDIUM
  ★ High-risk alerts after filtering: 1
  ★ Process exit code  (echo $?): 1
  ★ Build decision: exit 1 → the gate BLOCKED the build
✔ PASS  the gate blocked the build (non-zero exit) on the High-risk alert
```

**Proof artifact:** *Gate JSON report and exit code.*

---

## Step 4 — Confirm the filtered report disposition

The report proves the filter held: the benign finding now carries the False
Positive disposition, while the real High finding remains — exactly why the gate
blocked.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 4
```

✅ **You'll see** the benign finding disposed and the High kept (output — read it,
don't type it):

```text
WHAT: The report proves the filter held and the gate was right
  ★ Benign finding  (rule 10021): X-Content-Type-Options Header Missing — False Positive
  ★ Real finding  (rule 40012): Cross Site Scripting (Reflected) — High (Medium)
  ★ Gate outcome: benign filtered out, High kept → build blocked
✔ PASS  the filtered report shows the benign finding disposed and the High kept
```

**Proof artifact:** *Filtered alert report.*

---

## Check your work (automated)

Run every step in order through the checker; it writes a reviewable plain-text
log to `logs/` with each step's command and output in sequence.

💻 **Run in your terminal:**

```bash
./scripts/preflight_check.sh
```

✅ **You'll see** each step report **PASS**, ending with `5 checks passed, 0
failed`. (On a failure it prints the exact reason and how to fix it.)

💻 When you are finished, tear the stack down:

```bash
./scripts/demo_down.sh
```
