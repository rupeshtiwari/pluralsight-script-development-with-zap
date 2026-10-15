<div align="center">

# 🛡️ Script Development with ZAP

### Hands-on labs for extending OWASP ZAP beyond default scans

_Targeted vulnerability validation · Custom scripting · DevSecOps automation_

<br/>

<img alt="OWASP ZAP 2.17.0" src="https://img.shields.io/badge/OWASP%20ZAP-2.17.0-E5522F?style=for-the-badge&logo=owasp&logoColor=white"/>
<img alt="Docker" src="https://img.shields.io/badge/Docker%20Compose-1D63ED?style=for-the-badge&logo=docker&logoColor=white"/>
<img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img alt="MongoDB" src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white"/>

<br/>

<img alt="Platform: macOS" src="https://img.shields.io/badge/Platform-macOS-black?style=flat-square&logo=apple"/>
<img alt="Level: Entry" src="https://img.shields.io/badge/Level-Entry--friendly-2EA043?style=flat-square"/>
<img alt="Labs: 6" src="https://img.shields.io/badge/Labs-6-8957E5?style=flat-square"/>
<img alt="Runs locally" src="https://img.shields.io/badge/Runs-100%25%20locally-0969DA?style=flat-square"/>

</div>

---

Every lab runs against **one deliberately vulnerable Globomantics training
application** (Python / FastAPI + PostgreSQL + MongoDB) on **your own machine**.
You start with focused scans, grow into writing your own ZAP scripts, and finish
by wiring ZAP into a CI/CD pipeline as an automated security gate.

> [!WARNING]
> **Authorization and scope.** All techniques in these labs target **only** the
> local Globomantics training app. Never point them at any system you are not
> explicitly authorized to test.

---

## 🚀 Set up your machine (once)

```bash
./env-setup/setup-macos.sh
```

<table>
<tr>
<td>✅</td><td>Checks &amp; installs every dependency — Homebrew, Colima, Docker, Docker Compose, tmux, Python</td>
</tr>
<tr>
<td>✅</td><td>Pulls the pinned ZAP image</td>
</tr>
<tr>
<td>✅</td><td>Prints a readiness table and writes a full transcript to <code>env-setup/logs/</code></td>
</tr>
</table>

> [!TIP]
> One script, one time. When it prints a green readiness table, you are ready
> for every lab in the course.

> [!NOTE]
> **You don't need to start Docker yourself.** Colima (the Docker engine on
> macOS) stops when your Mac sleeps or restarts — so each lab's `demo_up.sh`
> now **starts it automatically** if it's down and waits until it's ready.
> Just run the lab; the stack comes up on its own.

---

## 📚 Labs

Work through them in order — each one builds on the skills before it. Every lab
is self-contained: open its runbook and follow along.

Folders are named by their **outline clip** — `m<module>-c<clip>-<name>` — so each
demo maps straight to the approved outline (clips 1–2 of each module are
presentation clips; the demos are clips 3–5).

| Clip | Demo (runbook) | Learning objectives | Source |
|:----:|----------------|:-------------------:|:------:|
| **M1 · C3** | **[Validate injection, XSS, and CSRF with ZAP](module1/m1-c3/README.md)** — build a focused scan policy; prove SQL, NoSQL, and command injection; map reflected XSS to its three contexts; replay a CSRF token | EO1a · EO1b · EO1c | [code](module1/m1-c3) |
| **M1 · C4** | **[Write a JavaScript security script in ZAP](module1/m1-c4/README.md)** — extend ZAP with an HTTP Sender script that marks every request | EO2a | [code](module1/m1-c4) |
| **M1 · C5** | **[Write Python scan and authentication scripts in ZAP](module1/m1-c5/README.md)** — write a custom Python active-scan rule and a scripted login, then scan a login-only page | EO2b · EO2c | [code](module1/m1-c5) |
| **M2 · C3** | **[Run authenticated ZAP scripts in GitHub Actions](module2/m2-c3/README.md)** — run your Module 1 scripts headless and authenticated in a GitHub Actions pipeline, via the ZAP Automation Framework | EO3a | [code](module2/m2-c3) |
| **M2 · C4** | **[Query the ZAP API and inspect scan evidence](module2/m2-c4/README.md)** — query runtime + scan status, the finding's rule identity and disposition, the official JSON report, and ZAP 2.17.0 Insights, all over the HTTP API | EO3b | [code](module2/m2-c4) |
| **M2 · C5** | **[Enforce ZAP quality gates in GitHub Actions](module2/m2-c5/README.md)** — mark a benign finding False Positive with `alertFilter`, confirm job order, then gate the build on the remaining risk via `exitStatus` exit codes | EO3c | [code](module2/m2-c5) |

---

## 🌿 Branches — per-demo isolation for distributed recording

The course uses **per-demo `before`/`after` branches** so a team can record each demo
independently, and so students see a clean starting point and a clean finished state.

- **`main` = generic starter.** Shared app (vulnerable + remediated builds), compose,
  ZAP entrypoint, shared scripts, and every demo's runbook + tooling — **but none of
  the learner-authored solution files**. Clone this to begin any demo from scratch.
- **`m<module>-demo<N>-before` = that demo's starting point.** Its prerequisites are
  present (e.g. the Module 2 demos keep the Module 1 scripts they reuse), but the
  demo's own authored work is not done yet — you perform it live.
- **`m<module>-demo<N>-after` = that demo completed.** The authored artifact is present
  and the demo is in its finished, verified state.

| Demo branch stem | Clip | Author-live artifact (absent in `before`, present in `after`) |
|---|---|---|
| `m1-demo1` | M1 C3 — Injection/XSS/CSRF | *(run-only: scans + disposition)* |
| `m1-demo2` | M1 C4 — JavaScript HTTP Sender | `module1/m1-c4/zap-scripts/globomantics-marker.js` |
| `m1-demo3` | M1 C5 — Python rule + auth | `module1/m1-c5/zap-scripts/globomantics-active-rule.py`, `…/globomantics-auth.py` |
| `m2-demo1` | M2 C3 — Authenticated GitHub Actions | `module2/m2-c3/ci/af-plan.yaml` (keeps M1 scripts as prereqs) |
| `m2-demo2` | M2 C4 — ZAP API | *(run-only: API queries over a finished scan)* |
| `m2-demo3` | M2 C5 — Quality gates | `module2/m2-c5/ci/gate-plan.yaml` |

> [!NOTE]
> `claude/stoic-cannon-nbupjt` is the integration branch holding the full verified
> solution (all demos + CI/validation fixes). The `…-after` branches are carved from
> it so each shows only its own demo completed.

---

## 🗂️ Repository layout

```text
env-setup/
  setup-macos.sh          One-file dependency check + install (verbose log)
scripts/
  fmt.py                  Shared colored output formatter (one palette to swap)
  lib.sh                  Shared shell helpers
  demo_up.sh / demo_down.sh / preflight_check.sh   Shared stack engine
app/                      Globomantics FastAPI app (vulnerable + remediated builds)
zap/                      ZAP container entrypoint (Webswing GUI + add-on install)
docker-compose.yaml       zap + app + postgres + mongo (bound to 127.0.0.1)
data/payloads/            Per-lab step manifests
docs/                     Gap report, preflight report, alert-disposition template
module1/
  README.md               Overview of the first set of labs
  m1-c3-.../
    README.md             The lab runbook
    scripts/              demo_up · demo_down · demo_reset · capture · preflight_check
    logs/                 Validation logs (git-ignored)
module2/
  README.md               Overview of the pipeline labs
```

---

## 🧰 Technology used

<div align="center">

| Layer | Tech |
|:-----:|------|
| 🔎 **Scanner** | OWASP ZAP 2.17.0 (`ghcr.io/zaproxy/zaproxy`, pinned by digest = tag `20260807-stable`) + `ascanrules` / `ascanrulesBeta` add-ons |
| 🌐 **App** | FastAPI (Python) — the Globomantics Store |
| 🗄️ **Data** | PostgreSQL · MongoDB |
| 🐳 **Runtime** | Docker Compose · Colima |

</div>

Each lab uses the subset it needs; more of the stack appears as later labs land.

---

<div align="center">

**Built by [Rupesh Tiwari](https://github.com/rupeshtiwari)** · Learn security testing by doing 🛡️

</div>
