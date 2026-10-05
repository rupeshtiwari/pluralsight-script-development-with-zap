# Run Authenticated ZAP Scripts in GitHub Actions

In this lab you take the ZAP scripts you built in Module 1 and run them
**automatically, with no GUI, inside a GitHub Actions pipeline** — logged in as a
real user, driven entirely by one configuration file (ZAP's **Automation
Framework**).

---

## How to read this lab

| Label | Meaning |
|-------|---------|
| 📄 **In your editor** | Open or read this file in your code editor. |
| 🌐 **In GitHub** | Do this in your repository on github.com (the **Actions** tab). |
| 💻 **Run in your terminal** | Copy-paste these commands into your terminal. |
| ✅ **You'll see** | A **result to read** — confirm success. **Never type it as a command.** |

> **Golden rule:** the only things you ever *type* are under 💻. Everything under
> ✅ is output you *read*, not a command.

---

## The problem you are solving

Scripts that only run on your laptop protect nothing. Real security testing has to
run **on every change, by itself, inside the build** — and it has to reach the
pages that require a login. Here you run your Module 1 checks **headless** in
GitHub Actions, logged in automatically, so the same custom security test fires
on every push without anyone clicking a button.

**What you gain:** your security checks become part of the pipeline — unattended,
authenticated, and repeatable — the foundation every quality gate is built on.

> **Authorization and scope.** The scan runs **only** against the local
> Globomantics app started inside the workflow. Never point it at any system you
> are not authorized to test.

---

## What you will use (reference)

| Piece | Value |
|-------|-------|
| Runner | GitHub-hosted **ubuntu-24.04** |
| ZAP image | `ghcr.io/zaproxy/zaproxy:stable`, run **headless** |
| Driven by | ZAP **Automation Framework** plan — [`ci/af-plan.yaml`](ci/af-plan.yaml) |
| Workflow | [`.github/workflows/zap-authenticated-scan.yml`](../../.github/workflows/zap-authenticated-scan.yml) |
| Scripts it runs | `globomantics-marker` (JS), `globomantics-active-rule` (Py), `globomantics-auth` (Py) — from Module 1 |
| Logs in as | user `alice` via scripted authentication |
| Scanned (authenticated) | `http://app:8000/account/profile` |

---

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Run the workflow so ZAP starts **headless** on ubuntu-24.04 | EO3a | GitHub Actions job log |
| 2 | Read the plan that binds **context + scripted auth + user + scope** | EO3a | Authenticated context configuration |
| 3 | See the **Module 1 scripts** run against the authenticated scope | EO3a | Authenticated script job result |
| 4 | See the authenticated run **record the reflection** your custom rule targets | EO3a | Authenticated finding recorded by the pipeline |

---

## Record it step by step

Bring the stack up once, then record each step as its own terminal segment. Each
command prints its own header and a green **PASS** — one clean screen per step.

```bash
cd module2/m2-c3-run-authenticated-zap-scripts-in-github-actions
./scripts/demo_up.sh        # wait for "Up" (starts Colima + the stack if needed)
./scripts/demo_step.sh 1    # ZAP runs headless from the Automation plan
./scripts/demo_step.sh 2    # the authenticated context, declared as config
./scripts/demo_step.sh 3    # the Module 1 scripts run authenticated
./scripts/demo_step.sh 4    # the authenticated finding recorded
```

Run them **in order** — step 1 runs the plan, steps 2–4 read its result. (To
validate all four at once, run `./scripts/preflight_check.sh`. When finished,
`./scripts/demo_down.sh`.)

---

## Step 1 — Run ZAP headless from the plan

ZAP normally opens a window. In a pipeline there is no window — it runs
**headless**, reading one plan file and doing the whole scan by itself. This is
the exact run the GitHub Actions job performs; here you run it locally.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 1
```

✅ **You'll see** ZAP run the whole Automation Framework plan headless and report
back (this is output — read it, don't type it):

```text
WHAT: ZAP runs headless from the Automation Framework plan
  ★ Runner (CI): ubuntu-24.04 · ghcr.io/zaproxy/zaproxy:stable
  ★ Command: zap.sh -cmd -autorun /zap/wrk/af-plan.yaml  (headless)
✔ PASS  the plan ran headless to completion with no errors
```

🌐 **Same beat in CI:** in the **Actions** tab, the *Globomantics authenticated ZAP
scan* job runs this same plan — its **job log** is the on-screen proof artifact.

**Proof artifact:** *GitHub Actions job log (headless run).*

---

## Step 2 — Show the authenticated context configuration

A headless run can't click a login form. Instead, the **plan file** declares how
to log in and what to scan — once, as config.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 2
```

✅ **You'll see** the plan bind everything the scan needs — context, scripted
login, user, and scope — before any scanning (output — read it, don't type it):

```text
WHAT: The authenticated context, declared as config
  ★ Context: Globomantics
  ★ Authentication: script-based → globomantics-auth (Login URL: /login)
  ★ User: alice
  ★ Target scope: http://app:8000 (profile + greet paths)
✔ PASS  the plan binds context + scripted auth + user + scope before scanning
```

📄 **The source:** this reads [`ci/af-plan.yaml`](ci/af-plan.yaml) — open its
`env.contexts` block to show the same config in your editor.

**Proof artifact:** *Authenticated context configuration.*

---

## Step 3 — See the Module 1 scripts run authenticated

The plan loads the exact scripts you wrote in Module 1 and runs them **as alice**,
against the login-only page.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 3
```

✅ **You'll see** your Module 1 scripts run against the authenticated scope — the
scan reaches the logged-in page (output — read it, don't type it):

```text
WHAT: The Module 1 scripts running under the authenticated scope
  ★ Loaded by the plan: globomantics-marker (JS) · globomantics-active-rule (Py) · globomantics-auth (Py)
  ★ Ran authenticated against: /account/profile — reflection reached while logged in
✔ PASS  the scripts executed against the authenticated scope
```

🌐 **Same beat in CI:** in the job log's **activeScan** section, the marker stamps
every request and the scan runs as alice against `/account/profile`.

**Proof artifact:** *Authenticated script job result.*

---

## Step 4 — Confirm the authenticated finding

The run ends by **recording the unsafe-reflection finding** on the login-only
page — produced with no GUI, logged in as alice. This is the exact condition your
Module 1 custom rule targets: a value reflected without output encoding.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 4
```

✅ **You'll see** the authenticated run record the reflection the custom rule
targets (output — read it, don't type it):

```text
WHAT: The authenticated finding recorded by the pipeline
  ★ Reflection reached while authenticated: Cross Site Scripting (Reflected) | param=note
✔ PASS  the authenticated run records the reflection the custom rule targets
```

The scan reached this **only because the scripted login worked** — without it the
page is HTTP 401. That recorded finding is what a quality gate can later pass or
fail the build on.

🌐 **Same beat in CI:** at the end of the job log (and in the uploaded
`globo-ci-report` artifact) the run prints the authenticated finding:
`Cross Site Scripting (Reflected)` on `/account/profile`, parameter `note`.

**Proof artifact:** *Authenticated finding recorded by the pipeline.*

> **About your custom rule.** Your Module 1 Python rule runs in this same
> authenticated scan and targets the identical reflection. This version of ZAP
> does not serialize script-rule alerts into the headless report, so the record
> above is ZAP's **built-in** confirmation of the same finding. You see the custom
> rule's own named alert — *Globomantics unsafe reflection (custom rule)* — in the
> ZAP GUI in **Module 1, Clip 3**, where you build and run it.

---

## Check your work (optional, automated)

Before you push to CI, run the **same Automation Framework plan locally** through
the author checker. It runs the plan via ZAP's API, logs in, runs the scripts
authenticated, and confirms the finding — writing a reviewable log to `logs/`.

💻 **Run in your terminal:**

```bash
./scripts/demo_up.sh                       # from the repo root; wait for "Up"
./module2/m2-c3-run-authenticated-zap-scripts-in-github-actions/scripts/preflight_check.sh
```

✅ **You'll see** each step report **PASS**, ending with
`5 checks passed, 0 failed`. (On a failure it prints the exact reason and how to
fix it.)

💻 When you are finished, tear the stack down:

```bash
./scripts/demo_down.sh
```
