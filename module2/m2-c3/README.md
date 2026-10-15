# Run authenticated ZAP scripts in GitHub Actions

Run the ZAP scripts you built in Module 1 automatically and headless inside a
GitHub Actions pipeline — logged in as a real user, driven entirely by one ZAP
Automation Framework plan. You read the plan in VS Code to understand how it binds
authentication and scope, then prove the same plan runs headless and authenticated.

> **Authorization and scope.** The scan runs only against the local Globomantics
> app started inside the workflow. Never point it at any system you are not
> authorized to test.

## Applications and locations used

| Application | Where | Used for |
|-------------|-------|----------|
| VS Code | `module2/m2-c3/ci/af-plan.yaml` + the integrated terminal | reading the plan config, then running `./scripts/demo_step.sh N` |
| GitHub Actions | `https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/actions/workflows/zap-authenticated-scan.yml` → latest run → job **authenticated-scan** | the same plan run headless on the hosted runner |
| CI artifact | run page → **Artifacts** → `globo-ci-report` | the archived report from the hosted run |

The local run and the GitHub Actions run execute the **same** plan; show VS Code for
the config and mechanics, and the Actions run for the hosted-runner proof.

## Setup

```bash
cd module2/m2-c3
./scripts/demo_up.sh             # prints "Up" when healthy
```

To show the hosted run, trigger the workflow from the Actions tab (**Run workflow**,
it is `workflow_dispatch`) or push to the repository, then open the most recent run
of *Globomantics authenticated ZAP scan*.

## Step-by-step LO traceability

| Step | LO | Config / mechanism (`ci/af-plan.yaml`) | Command | Observed result | Proof artifact |
|------|----|----------------------------------------|---------|-----------------|----------------|
| 1 | EO3a | whole plan, run via `zap.sh -cmd -autorun` | `demo_step.sh 1` | plan runs headless to completion, no errors | GitHub Actions job log |
| 2 | EO3a | `authentication` 29–40 · `users` 44–47 · `includePaths` 26–28 | `demo_step.sh 2` | plan binds context `Globomantics`, scripted auth, user `alice`, scope `http://app:8000` | Authenticated context configuration |
| 3 | EO3a | `passiveScan-config` 60–62 · script `add`/`enable` 67–91 · `spider` 93–99 · `requestor` 109–119 · `activeScan` + rule `50000` 121–134 | `demo_step.sh 3` | Module 1 scripts load and run against `/account/profile` while logged in | Authenticated script job result |
| 4 | EO3a | `report` 141–146 | `demo_step.sh 4` | custom alert `Globomantics unsafe reflection (custom rule)` on `/account/profile`, param `note` | Authenticated custom alert record |

## Five-minute timing allocation

Recording budget: **5:00**. Active-scan wait time is edited out in post; the proof
evidence each command and the job log print is retained in full.

| Segment | Duration | Running total |
|---------|----------|---------------|
| Setup and problem | 0:25 | 0:25 |
| Step 1 — headless run | 0:55 | 1:20 |
| Step 2 — read the authenticated context in VS Code | 1:30 | 2:50 |
| Step 3 — Module 1 scripts run authenticated | 0:55 | 3:45 |
| Step 4 — authenticated custom alert | 0:55 | 4:40 |
| Wrap-up | 0:20 | 5:00 |

---

## Step 1: Run ZAP headless from the plan (EO3a)

**The problem.** A pipeline has no GUI to click. ZAP must run the entire
authenticated scan from one config file, unattended — exactly as the hosted runner
does.

**Execute.**

```bash
./scripts/demo_step.sh 1
```

**Inspect the actual evidence.** ZAP runs `ghcr.io/zaproxy/zaproxy` (pinned by
digest = tag `20260807-stable`, ZAP 2.17.0) via `zap.sh -cmd -autorun …` and the
plan runs headless to completion with no errors, following the canonical job order
`passiveScan-config → script → spider → passiveScan-wait → activeScan →
passiveScan-wait → report` (the gate jobs `alertFilter`/`exitStatus` are M2 C5).
In CI, the same beat is the **authenticated-scan** job's **Run ZAP headless with the
Automation Framework plan** step on `ubuntu-24.04`.

**The engineer's decision.** One plan file drives the whole authenticated scan with
no window — which is what makes it runnable unattended in CI.

Proof artifact: GitHub Actions job log.

---

## Step 2: Show the authenticated context configuration (EO3a)

**The problem.** A headless run cannot fill in a login form, so the plan must declare
*how to log in* and *what to scan* as data, once, before any scanning.

**Inspect the plan in VS Code.** Open `module2/m2-c3/ci/af-plan.yaml` →
`env.contexts`:

- **`authentication` (lines 29–40)** — `method: script` loads
  `globomantics-auth.py` by path, with `scriptEngine: "python : jython"` and the
  `Login URL` it needs. Verification is response-based: `loggedInRegex: "Signed in
  as"` and `loggedOutRegex: "Please log in first"` tell ZAP when the session is valid.
- **`users` (lines 44–47)** — the user the scan runs as: `alice`, with the
  `username` credential the auth script consumes.
- **`includePaths` (lines 26–28)** — the scope: the profile and greet paths on
  `http://app:8000`.

The mechanism: authentication and scope are declared as config, so the same login
and target apply identically on every run.

**Execute.**

```bash
./scripts/demo_step.sh 2
```

**Inspect the actual evidence.** The plan binds Context `Globomantics`, script-based
authentication via `globomantics-auth` (Login URL `/login`), user `alice`, and scope
`http://app:8000` before scanning.

**The engineer's decision.** Because the login and scope live in the plan, the
authenticated scan is reproducible on every unattended run.

Proof artifact: Authenticated context configuration.

---

## Step 3: See the Module 1 scripts run authenticated (EO3a)

**The problem.** The plan has to load the exact scripts from Module 1 and run them
as `alice` against the login-only page — not re-implement them.

**Inspect the jobs in VS Code.** In the same file, the `jobs` list follows the
canonical Automation Framework order (non-gate portion):

- **`passiveScan-config` (lines 60–62)** — enables scope-limited passive scanning
  before any traffic.
- **script `add` / `enable` (lines 67–91)** — loads `globomantics-active-rule` (Py)
  and `globomantics-marker` (JS) by path; the auth script is loaded by the context.
- **`spider` (lines 93–99)** — crawls the scope *as alice* so the sites tree is
  populated from inside the session.
- **`passiveScan-wait` (lines 101–103)** — drains the passive-scan queue.
- **`requestor` (lines 109–119)** — seeds `/account/profile?note=seed` into the sites
  tree *as alice*, guaranteeing the authenticated node (with the `note` param) the
  active scan and custom rule attack.
- **`activeScan` + rule `50000` (lines 121–134)** — runs the scan as the context user;
  the Script Active Scan Rules plugin (`50000`, inline policy at LOW threshold) is what
  runs the custom Python rule. A second `passiveScan-wait` then `report` follow.

**Execute.**

```bash
./scripts/demo_step.sh 3
```

**Inspect the actual evidence.** The plan loads `globomantics-marker` (JS),
`globomantics-active-rule` (Py), and `globomantics-auth` (Py) and runs authenticated
against `/account/profile` — the scan reaches the logged-in page.

**The engineer's decision.** The custom JavaScript and Python checks from Module 1
run unchanged inside the pipeline, now against an authenticated scope.

Proof artifact: Authenticated script job result.

---

## Step 4: Confirm the authenticated custom alert (EO3a)

**The problem.** The run must record the unsafe-reflection finding on the login-only
page — the exact condition the Module 1 custom rule targets, reachable only because
the scripted login worked (the page is HTTP 401 without it).

**Execute.**

```bash
./scripts/demo_step.sh 4
```

**Inspect the actual evidence.** The custom rule's named alert `Globomantics unsafe
reflection (custom rule)` is recorded on `/account/profile`, parameter `note`, under
the authenticated headless run — alongside ZAP's built-in `Cross Site Scripting
(Reflected)` on the same parameter. In CI it is written to the downloadable
`globo-ci-report` artifact.

**The engineer's decision.** The finding exists only under authentication, and it is
*your* Module 1 rule's named alert serialized by the headless pipeline run — exactly
what a quality gate can later pass or fail the build on.

Proof artifact: Authenticated custom alert record.

## Validate and reset

Run the same Automation Framework plan locally through the checker — it runs the plan
via the ZAP API, logs in, runs the scripts authenticated, and confirms the finding,
writing a reviewable log to `logs/`:

```bash
./scripts/preflight_check.sh
```

It ends with `5 checks passed, 0 failed`. Tear down with `./scripts/demo_down.sh`.
