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
| 4 | Confirm the custom rule **raises its alert** under the authenticated run | EO3a | Authenticated custom alert record |

---

## Step 1 — Run ZAP headless in the pipeline

ZAP normally opens a window. In a pipeline there is no window — it runs
**headless**, reading one plan file and doing the whole scan by itself.

🌐 **In GitHub:**

1. Open your repository → the **Actions** tab.
2. Choose **Globomantics authenticated ZAP scan** → **Run workflow**.
3. Open the running job and watch its log.

✅ **You'll see** the job start ZAP headless on the hosted runner (read it — don't
type it):

```text
Runner:  ubuntu-24.04
Image:   ghcr.io/zaproxy/zaproxy:stable
Command: zap.sh -cmd -autorun /zap/wrk/af-plan.yaml   (no GUI)
```

**Proof artifact:** *GitHub Actions job log.*

---

## Step 2 — Read the authenticated context configuration

A headless run can't click a login form. Instead, the **plan file** declares how
to log in and what to scan — once, as config.

📄 **In your editor:** open [`ci/af-plan.yaml`](ci/af-plan.yaml) and find the
`env.contexts` block.

✅ **You'll see** the context bind everything the scan needs (read it — don't type it):

```text
Context:        Globomantics
Authentication: script-based -> globomantics-auth  (Login URL: /login)
User:           alice
Target scope:   http://app:8000  (profile + greet paths)
```

**Proof artifact:** *Authenticated context configuration.*

---

## Step 3 — See the Module 1 scripts run authenticated

The plan loads the exact scripts you wrote in Module 1 and runs them **as alice**,
against the login-only page.

🌐 **In GitHub:** in the same job log, find the **activeScan** section.

✅ **You'll see** your scripts load and run against the authenticated scope:

```text
Scripts loaded: globomantics-marker (JS) · globomantics-active-rule (Py) · globomantics-auth (Py)
Scanned as:     alice  ->  /account/profile  (reached while logged in)
```

**Proof artifact:** *Authenticated script job result.*

---

## Step 4 — Confirm the custom alert under the authenticated run

The run ends in your own named finding — produced with no GUI, logged in, in CI.

🌐 **In GitHub:** at the end of the job log (and in the uploaded report), find the
alert your rule raised.

✅ **You'll see** your custom alert recorded by the authenticated run:

```text
Alert:      Globomantics unsafe reflection (custom rule)
Risk:       Medium
Parameter:  note
```

That finding is what a quality gate can later pass or fail the build on.
**Proof artifact:** *Authenticated custom alert record.*

---

## Check your work (optional, automated)

Before you push to CI, run the **same Automation Framework plan locally** through
the author checker. It runs the plan via ZAP's API, logs in, runs the scripts
authenticated, and confirms the finding — writing a reviewable log to `logs/`.

💻 **Run in your terminal:**

```bash
./scripts/demo_up.sh                       # from the repo root; wait for "Up"
./module2/m2-demo1-run-authenticated-zap-scripts-in-github-actions/scripts/preflight_check.sh
```

✅ **You'll see** each step report **PASS**, ending with
`5 checks passed, 0 failed`. (On a failure it prints the exact reason and how to
fix it.)

💻 When you are finished, tear the stack down:

```bash
./scripts/demo_down.sh
```
