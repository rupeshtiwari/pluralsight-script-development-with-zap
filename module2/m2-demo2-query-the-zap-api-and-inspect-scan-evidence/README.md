# Query the ZAP API and Inspect Scan Evidence

In this lab you inspect a finished authenticated scan **entirely through ZAP's
HTTP API** — no GUI. You ask the running engine for its status, pull the exact
finding with its rule identity and rating, generate ZAP's official JSON report,
and read ZAP 2.17.0 **Insights** to judge how well the scan actually ran.

---

## The problem you are solving

A pipeline has no screen to click. Once a scan finishes, something has to read
its evidence **programmatically** — the status, the findings, the report, and
whether the scan was even effective — and decide what to do. ZAP exposes all of
this over a local HTTP API. Learn to query it and you can wire scan evidence into
any tool: a dashboard, a ticket, or the quality gate you build next.

**What you gain:** you can pull a finished scan's evidence over HTTP and trust
it — rule identity, risk disposition, an archivable report, and Insights that
tell you the scan did its job — without opening the ZAP window.

> **Authorization and scope.** Every request targets **only** the local
> Globomantics training app on the compose network. Never point these queries at
> any system you are not authorized to test.

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
| ZAP API | `http://localhost:8090` (JSON API, local only) |
| Engine status | `GET core/view/version` · `GET ascan/view/scans` |
| Findings | `GET core/view/alerts` |
| Official report | `POST reports/action/generate` (template `traditional-json`) |
| Insights | the report's `insights[]` section · `GET stats/view/allSitesStats` |
| Evidence under inspection | a finished authenticated scan of `http://app:8000/account/profile` |

---

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Ask the API for the **runtime and scan status** | EO3b | ZAP API status response |
| 2 | Ask the API for the finding's **rule identity and disposition** | EO3b | ZAP API alert response |
| 3 | Generate the **official JSON report** and reconcile it with the API | EO3b | ZAP JSON report |
| 4 | Read **ZAP 2.17.0 Insights** to judge scan effectiveness | EO3b | ZAP Insights evidence |

---

## Run it step by step

Bring the stack up once, then run each step on its own screen. Each command
prints a header saying **what** it shows and **why**, then a green **PASS**.

```bash
cd module2/m2-demo2-query-the-zap-api-and-inspect-scan-evidence
./scripts/demo_up.sh        # wait for "Up" (starts Colima + the stack if needed)
./scripts/demo_step.sh 1    # ZAP API status response
./scripts/demo_step.sh 2    # ZAP API alert response
./scripts/demo_step.sh 3    # ZAP JSON report
./scripts/demo_step.sh 4    # ZAP Insights evidence
```

The first step you run inspects a finished scan; if none exists yet in this ZAP
session, the step runs the authenticated plan once to create the evidence, then
inspects it. (To validate all four at once, run `./scripts/preflight_check.sh`;
when finished, `./scripts/demo_down.sh`.)

---

## Step 1 — Ask the API for runtime and scan status

A pipeline's first question is simple: *is the engine there, and is the scan
done?* You ask ZAP directly over HTTP.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 1
```

✅ **You'll see** the API report the engine version and a finished scan (output —
read it, don't type it):

```text
WHAT: The ZAP API answers: what engine, and is the scan done?
  ★ ZAP runtime  (GET core/view/version): 2.17.0
  ★ Active scan  (GET ascan/view/scans): id=0 · progress=100% · state=FINISHED
  ★ Requests the scan sent: 412
✔ PASS  the API reports the ZAP runtime and a finished scan
```

**Proof artifact:** *ZAP API status response.*

---

## Step 2 — Ask the API for the finding's rule identity and disposition

A finished scan holds findings. You ask the API for the one the authenticated
scan generated and read the two things a gate cares about: **which rule** found
it, and **how it is rated**.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 2
```

✅ **You'll see** the finding's rule identity and disposition (output — read it,
don't type it):

```text
WHAT: The ZAP API answers: what did the scan find, and how is it rated?
  ★ Rule identity  (pluginId · alert): 40012 · Cross Site Scripting (Reflected)
  ★ Disposition  (risk · confidence): High · Medium
  ★ Parameter: note
✔ PASS  the API returns the finding's rule identity and disposition
```

**Proof artifact:** *ZAP API alert response.*

---

## Step 3 — Generate the official JSON report and reconcile it

The API response is live state; the **report** is the archivable record. You
generate ZAP's own JSON report through the API and confirm it carries the same
finding — so what you archive matches what you queried.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 3
```

✅ **You'll see** the report carry the same rule identity and rating (output —
read it, don't type it):

```text
WHAT: The official JSON report reconciles with the API
  ★ Report template: traditional-json  (reports/action/generate)
  ★ Report alert  (pluginid · name): 40012 · Cross Site Scripting (Reflected)
  ★ Report rating  (riskdesc): High (Medium)
  ★ Reconciled with the API: same rule id and risk as the Step 2 alert response
✔ PASS  the official JSON report carries the same finding as the API
```

**Proof artifact:** *ZAP JSON report.*

---

## Step 4 — Read ZAP 2.17.0 Insights

Findings tell you *what was found*. **Insights** tell you *how well the scan
ran* — signals about effectiveness and operational issues, drawn from ZAP's
statistics and included in the report. You read them to trust the result.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 4
```

✅ **You'll see** Insights that assess the scan, alongside the report (output —
read it, don't type it):

```text
WHAT: ZAP 2.17.0 Insights assess scan effectiveness, not just findings
  ★ Insight  (level · key): Low · insight.log.error
  ★ Statistic · meaning: 17 · ZAP errors logged — see the zap.log file for details
  ★ Insight  (level · key): Low · insight.log.warn
  ★ Statistic · meaning: 3 · ZAP warnings logged — see the zap.log file for details
  ★ Insight  (level · key): Info · insight.network.failure
  ★ Statistic · meaning: 1 · Percentage of network failures
✔ PASS  the report's Insights section reports scan effectiveness
```

Insights are **operational signals, not vulnerabilities** — here they flag logged
errors/warnings and network reliability, so you know whether to trust the scan's
coverage before acting on its findings.

**Proof artifact:** *ZAP Insights evidence.*

---

## Check your work (automated)

Run every step in order through the checker; it writes a reviewable plain-text
log to `logs/` with each step's command and output in sequence.

💻 **Run in your terminal:**

```bash
./scripts/preflight_check.sh
```

✅ **You'll see** each step report **PASS**, ending with `4 checks passed, 0
failed`. (On a failure it prints the exact reason and how to fix it.)

💻 When you are finished, tear the stack down:

```bash
./scripts/demo_down.sh
```
