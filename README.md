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

---

## 📚 Labs

<table>
<thead>
<tr>
<th align="center">Module</th>
<th>Title</th>
<th>Objectives</th>
<th align="center">Labs</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><a href="module1/README.md"><b>1</b></a></td>
<td>Targeted security testing and ZAP scripting</td>
<td><code>EO1a–c</code> · <code>EO2a–c</code></td>
<td align="center">🟢 1 ready · 2 to come</td>
</tr>
<tr>
<td align="center"><a href="module2/README.md"><b>2</b></a></td>
<td>Automated ZAP security gates in DevSecOps pipelines</td>
<td><code>EO3a–c</code></td>
<td align="center">🗓️ 3 planned</td>
</tr>
</tbody>
</table>

### 🧩 Module 1 — Targeted security testing and ZAP scripting

| # | Lab | You will learn | Objectives | Status |
|:-:|-----|----------------|:----------:|:------:|
| 1 | **[Validate injection, XSS, and CSRF with ZAP](module1/m1-demo1-validate-injection-xss-and-csrf-with-zap/README.md)** | Build a focused scan policy; prove SQL, NoSQL, and command injection; map reflected XSS to its three contexts; compare CSRF token states; record an alert disposition | `EO1a` · `EO1b` · `EO1c` | 🟢 Ready |
| 2 | **[Write a JavaScript security script in ZAP](module1/m1-demo2-write-a-javascript-security-script-in-zap/README.md)** | Extend ZAP with an HTTP Sender script that marks every request | `EO2a` | 🟢 Ready |
| 3 | Write Python scan and authentication scripts in ZAP | Custom Python scan rule and scripted login | `EO2b` · `EO2c` | 🗓️ Planned |

### ⚙️ Module 2 — Automated ZAP security gates in DevSecOps pipelines

| # | Lab | You will learn | Objectives | Status |
|:-:|-----|----------------|:----------:|:------:|
| 1 | Run authenticated ZAP scripts in GitHub Actions | Headless ZAP running your scripts in a pipeline | `EO3a` | 🗓️ Planned |
| 2 | Query the ZAP API and inspect scan evidence | Programmatic scan status, alerts, and reports | `EO3b` | 🗓️ Planned |
| 3 | Enforce ZAP quality gates in GitHub Actions | Alert filters and exit-code gates | `EO3c` | 🗓️ Planned |

---

## 🎯 Learning objectives

<table>
<tr>
<td valign="top" width="33%">

**1 · Scan for specific vulnerabilities**

- `EO1a` Configure specialized scanners for injection (SQL, NoSQL, command)
- `EO1b` Validate XSS with context-specific payloads
- `EO1c` Execute CSRF token-bypass techniques

</td>
<td valign="top" width="33%">

**2 · Script custom security tests**

- `EO2a` Develop **JavaScript** scripts to extend ZAP
- `EO2b` Implement **Python** scripts for custom scan rules
- `EO2c` Automate **authentication** sequences

</td>
<td valign="top" width="33%">

**3 · Integrate with DevSecOps**

- `EO3a` Run ZAP headless in CI/CD
- `EO3b` Drive ZAP through its API
- `EO3c` Enforce threshold-based quality gates

</td>
</tr>
</table>

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
  README.md               Module 1 overview: objectives and labs
  m1-demo1-.../
    README.md             The lab runbook
    scripts/              demo_up · demo_down · demo_reset · capture · preflight_check
    logs/                 Validation logs (git-ignored)
module2/
  README.md               Module 2 overview: objectives and labs
```

---

## 🧰 Technology used

<div align="center">

| Layer | Tech |
|:-----:|------|
| 🔎 **Scanner** | OWASP ZAP 2.17.0 (`ghcr.io/zaproxy/zaproxy:stable`, pinned by digest) + `ascanrules` / `ascanrulesBeta` add-ons |
| 🌐 **App** | FastAPI (Python) — the Globomantics Store |
| 🗄️ **Data** | PostgreSQL · MongoDB |
| 🐳 **Runtime** | Docker Compose · Colima |

</div>

Each lab uses the subset its objectives require; coverage of the full course tech
stack grows as more labs land.

---

<div align="center">

**Built by [Rupesh Tiwari](https://github.com/rupeshtiwari)** · Learn security testing by doing 🛡️

</div>
