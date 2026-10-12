# Run authenticated ZAP scripts in GitHub Actions

Run the ZAP scripts you built in Module 1 automatically and headless inside a
GitHub Actions pipeline — logged in as a real user, driven entirely by one ZAP
Automation Framework plan.

> **Authorization and scope.** The scan runs only against the local Globomantics
> app started inside the workflow. Never point it at any system you are not
> authorized to test.

## Applications and locations used

| Application | Where | Used for |
|-------------|-------|----------|
| macOS Terminal | working directory `module2/m2-c3` | running the plan locally via `./scripts/demo_step.sh N` |
| GitHub Actions | `https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/actions/workflows/zap-authenticated-scan.yml` → latest run → job **authenticated-scan** | showing the same plan run headless on the hosted runner |
| Automation Framework plan | `module2/m2-c3/ci/af-plan.yaml` | the single config that binds context, auth, user, scope, and scan |
| CI artifact | run page → **Artifacts** → `globo-ci-report` | the archived report from the hosted run |

The local Terminal run and the GitHub Actions run execute the **same** plan; show
the Terminal for the mechanics and the Actions run for the hosted-runner proof.

## Setup

```bash
cd module2/m2-c3
./scripts/demo_up.sh             # prints "Up" when healthy
```

To show the hosted run, trigger the workflow from the Actions tab
(**Run workflow**, it is `workflow_dispatch`) or push to the repository, then open
the most recent run of *Globomantics authenticated ZAP scan*.

## Learning-objective coverage

| Step | Objective | Proof artifact |
|------|-----------|----------------|
| 1 | EO3a | GitHub Actions job log |
| 2 | EO3a | Authenticated context configuration |
| 3 | EO3a | Authenticated script job result |
| 4 | EO3a | Authenticated custom alert record |

## Step 1: Run ZAP headless from the plan (EO3a)

Goal: Run the whole scan with no GUI — ZAP reads one Automation Framework plan and
executes it headless, exactly as the hosted runner does.

Application: macOS Terminal, then GitHub Actions.
Open / Navigate: Terminal in `module2/m2-c3`. Then the Actions tab → workflow
*Globomantics authenticated ZAP scan* → the latest run → job **authenticated-scan**
→ step **Run ZAP headless with the Automation Framework plan**.
Execute: `./scripts/demo_step.sh 1` locally; in CI, read that job-log step.

Expected output: ZAP runs on `ubuntu-24.04` with `ghcr.io/zaproxy/zaproxy:stable`
(the approved baseline tag, currently ZAP 2.17.0) via `zap.sh -cmd -autorun …`,
and the plan runs headless to completion with no errors.

What the learner should notice: there is no window — one plan file drives the
entire authenticated scan, which is what makes it runnable unattended in CI.

Proof artifact: GitHub Actions job log.

## Step 2: Show the authenticated context configuration (EO3a)

Goal: A headless run cannot click a login form, so the plan declares how to log in
and what to scan — once, as config.

Application: macOS Terminal, with the source plan open for reference.
Open / Navigate: Terminal in `module2/m2-c3`; the source is
[`ci/af-plan.yaml`](ci/af-plan.yaml) (`env.contexts` block).
Execute: `./scripts/demo_step.sh 2`.

Expected output: the plan binds Context `Globomantics`, script-based authentication
via `globomantics-auth` (Login URL `/login`), user `alice`, and target scope
`http://app:8000` before any scanning.

What the learner should notice: authentication and scope are declared as data in the
plan, so the same login and target apply identically on every run.

Proof artifact: Authenticated context configuration.

## Step 3: See the Module 1 scripts run authenticated (EO3a)

Goal: The plan loads the exact scripts you wrote in Module 1 and runs them as
`alice` against the login-only page.

Application: macOS Terminal, then GitHub Actions.
Open / Navigate: Terminal in `module2/m2-c3`. In CI, the job log's **activeScan**
section of the **authenticated-scan** job.
Execute: `./scripts/demo_step.sh 3`.

Expected output: the plan loads `globomantics-marker` (JS), `globomantics-active-rule`
(Py), and `globomantics-auth` (Py), and runs authenticated against
`/account/profile` — the scan reaches the logged-in page.

What the learner should notice: the custom JavaScript and Python checks from Module 1
run unchanged inside the pipeline, now against an authenticated scope.

Proof artifact: Authenticated script job result.

## Step 4: Confirm the authenticated custom alert (EO3a)

Goal: Confirm the authenticated run records the unsafe-reflection finding on the
login-only page — the exact condition the Module 1 custom rule targets, reached only
because the scripted login worked (the page is HTTP 401 without it).

Application: macOS Terminal, then GitHub Actions.
Open / Navigate: Terminal in `module2/m2-c3`. In CI, the job-log step **Show the
authenticated finding from the report**, and the downloadable **`globo-ci-report`**
artifact on the run page.
Execute: `./scripts/demo_step.sh 4`.

Expected output: the custom rule's named alert
`Globomantics unsafe reflection (custom rule)` recorded on `/account/profile`,
parameter `note`, under the authenticated headless run — alongside ZAP's built-in
`Cross Site Scripting (Reflected)` on the same parameter.

What the learner should notice: the finding exists only under authentication, and
it is *your* Module 1 Python rule's named alert serialized by the headless
pipeline run — exactly what a quality gate can later pass or fail the build on.

Proof artifact: Authenticated custom alert record.

## Validate and reset

Run the same Automation Framework plan locally through the checker — it runs the
plan via the ZAP API, logs in, runs the scripts authenticated, and confirms the
finding, writing a reviewable log to `logs/`:

```bash
./scripts/preflight_check.sh
```

It ends with `5 checks passed, 0 failed`. Tear down with `./scripts/demo_down.sh`.
