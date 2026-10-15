# Validate Injection, XSS and CSRF

<details><summary><b>Branch: m1-demo1-before — Student Starting Point</b></summary>

This is the independent starting point. Follow the four commands and create the evidence yourself. No previously run demo is required.

</details>


<div align="center">

![ZAP](https://img.shields.io/badge/OWASP_ZAP-Targeted_Scanning-0284c7?style=for-the-badge)
![Lab](https://img.shields.io/badge/Practice-m1-demo1-d946ef?style=for-the-badge)

<img src="../../../docs/learner-diagrams/m1-demo1-architecture.svg" width="100%" alt="Validate Injection, XSS and CSRF: application, tool and evidence architecture"/>

<sub>Illustrative architecture · Generated using ChatGPT · Verify real results in your own lab</sub>

</div>

## What Problem Are You Solving?

Maya Chen receives scanner findings about the Globomantics search, account and admin endpoints. She must show which inputs actually change SQL, MongoDB, or shell behavior, whether reflected HTML can be exploited in its output context, and whether a CSRF token belongs to the right session. A long alert list is not an engineering decision.

**Your outcome:** Complete four practical checks and be able to explain both the actual evidence and the engineering decision it supports. This page is self-contained; you do not need access to a separate course outline.

## Learning Objectives Covered

<table><thead><tr><th>Objective</th><th>What You Will Learn</th></tr></thead><tbody>
<tr><td><code>EO1a</code></td><td>Configure specialized scanners for injection vulnerabilities (SQL, NoSQL, Command)</td></tr>
<tr><td><code>EO1b</code></td><td>Implement Cross-Site Scripting (XSS) validation with context-specific payloads</td></tr>
<tr><td><code>EO1c</code></td><td>Execute CSRF token bypass techniques for testing anti-CSRF protections</td></tr>
</tbody></table>

## Your Four-Step Learning Path

```mermaid
flowchart LR
  N0["Focused injection scan"]
  N1["XSS context evidence"]
  N2["Session-token replay"]
  N3["Confirmed disposition"]
  N0 --> N1 --> N2 --> N3
```

<table>
<thead><tr><th>Step</th><th>Exact Command</th><th>What You Do</th><th>What To Verify</th><th>Why It Matters</th></tr></thead>
<tbody><tr><td><b>1</b></td><td><code>./steps/01-run-targeted-injection-scan.sh</code></td><td>Target SQL, MongoDB and command-injection parameters</td><td>Rule/parameter-specific ZAP alerts and scan policy</td><td>Focused scanning separates three different unsafe sinks</td></tr>
<tr><td><b>2</b></td><td><code>./steps/02-verify-reflected-xss-contexts.sh</code></td><td>Test HTML body, attribute and JavaScript contexts</td><td>Injected request, reflected response and ZAP finding</td><td>Output context determines payload and required encoding</td></tr>
<tr><td><b>3</b></td><td><code>./steps/03-test-cross-session-csrf-token.sh</code></td><td>Compare valid, missing and cross-session token behavior</td><td>HTTP 200 / 403 / 200 and actual account email mutation</td><td>Token presence is insufficient without session ownership</td></tr>
<tr><td><b>4</b></td><td><code>./steps/04-reconcile-security-alerts.sh</code></td><td>Compare alerts against live application evidence</td><td>SQL error, NoSQL count, injected-command proof and XSS evidence</td><td>A finding needs behavior to support its disposition</td></tr></tbody></table>

## Start This Exercise

From the repository root:

```bash
git fetch origin
git switch m1-demo1-before
./setup/setup-macos.sh
cd demos/module1-demos/m1-demo1-targeted-injection-xss-csrf
./scripts/demo_reset.sh
```

If you already prepared your Mac, the one-time setup script can be skipped. Run **Steps 1–4 above** from this demo directory, in order. Then validate and stop:

```bash
./scripts/preflight_check.sh
./scripts/demo_down.sh
```

The preflight writes a timestamped log to `logs/`; GUI-only evidence must also be verified in the real ZAP interface at <http://localhost:8080/zap/>. The app runs at <http://localhost:8000/> and ZAP's local API/proxy at <http://localhost:8090/>.

**Compare with the completed version:** `git diff m1-demo1-before..m1-demo1-after -- demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`. This command does not overwrite your files. The `before` branch starts the exercise; the `after` branch provides its completed reference, where applicable.

**Technical evidence note:** A normal successful ping alone does not prove command injection. Confirm the injected host parameter and relevant alert request/response before describing it as exploitable.

All testing must stay within the authorized Globomantics training application.

---

## Detailed Instructions And Expected Evidence

<details><summary><b>View The Four Executable Steps</b></summary>

```bash
./steps/01-run-targeted-injection-scan.sh
./steps/02-verify-reflected-xss-contexts.sh
./steps/03-test-cross-session-csrf-token.sh
./steps/04-reconcile-security-alerts.sh
```

Run these commands in order from this demo's folder, then execute `./scripts/preflight_check.sh`. Inspect actual ZAP GUI or GitHub Actions evidence where indicated.
</details>


Turn a broad ZAP scan into four validated findings against the deliberately
vulnerable Globomantics Store. For each finding you first read the exact
application code that creates the flaw, then prove the behavior with ZAP and the
app's own response — the way a security engineer connects a scanner alert to a
real defect.

> **Authorization and scope.** Every request targets only the local Globomantics
> Store. Never run these techniques against systems you are not authorized to test.

## Applications and locations used

| Application | Where | Used for |
|-------------|-------|----------|
| VS Code | `runtime/app/main.py` + the integrated terminal in `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf` | reading each vulnerable sink, then running `./scripts/demo_step.sh N` in the same window |
| ZAP (one container) | API/proxy on `:8090` | the same instance the terminal drives; alerts a step raises are ZAP's own findings, printed back by the command |
| Local Globomantics app | `http://localhost:8000/` | the target under test |

Work in **VS Code** with the integrated terminal: read the sink in the editor
pane, then run the step in the terminal pane. The terminal output is the
authoritative evidence; `./scripts/show_code.sh` prints the live vulnerable lines
straight from `runtime/app/main.py`, so they never drift.

## Setup

Install once from the repo root: `./setup/setup-macos.sh` (wait for the
readiness table). Then start the vulnerable build:

```bash
cd demos/module1-demos/m1-demo1-targeted-injection-xss-csrf
./scripts/demo_reset.sh          # vulnerable build; prints "Up" when healthy
```

Exact alert IDs, risk, and confidence are the live values from your run.

## Step-by-step LO traceability

| Step | LO | Code inspected (`runtime/app/main.py`) | Commands | Observed result | Proof artifact |
|------|----|--------------------------------|----------|-----------------|----------------|
| 1 | EO1a | `search` 149–153 · `account` 196–204 (regex 180) · `admin_ping` 227–231 | `show_code.sh sqli\|nosql\|cmd` · `steps/01-run-targeted-injection-scan.sh` | alerts `40018` / `40033` / `90020`, one per parameter | Targeted scan policy and rule list |
| 2 | EO1b | `greet` 257–277 | `show_code.sh xss` · `steps/02-verify-reflected-xss-contexts.sh` | *Cross Site Scripting (Reflected)* on `name` with injected payload + reflected evidence | XSS request and response body |
| 3 | EO1c | `change_email` 332–337 (token issued `284–287`) | `show_code.sh csrf` · `steps/03-test-cross-session-csrf-token.sh` | `200` / `403` / `200`; email `alice@globomantics.example` → `attacker@evil.example` | CSRF token replay result |
| 4 | EO1a · EO1b · EO1c | — (reconciles Steps 1–3 findings) | `steps/04-reconcile-security-alerts.sh` | SQL error · NoSQL count `1→4` · ping bytes · XSS reflected unescaped | Alert disposition record |

---

## Step 1: Run one targeted injection scan (EO1a)

**The problem.** A default scan floods you with alerts. Maya wants the opposite:
one focused policy that confirms three *different* injection classes — SQL, NoSQL,
and command — each from the application's own response, on three endpoints.

**Inspect the vulnerable code in VS Code.** Read the three sinks before scanning —
they fail in three distinct ways. In the integrated terminal:

```bash
./scripts/show_code.sh sqli     # runtime/app/main.py  search()      lines 149–153
./scripts/show_code.sh nosql    # runtime/app/main.py  account()     lines 196–204 (regex at 180)
./scripts/show_code.sh cmd      # runtime/app/main.py  admin_ping()  lines 227–231
```

**Why each is vulnerable — the distinct mechanism:**

- **SQL injection (`search`).** The `q` value is concatenated straight into the
  SQL string (`"… ILIKE '%" + q + "%'"`), so input containing a quote escapes the
  string literal and becomes SQL.
- **NoSQL injection (`account`).** The query string is parsed qs-style, so the
  *parameter name* `username[$ne]=` smuggles a MongoDB operator into the filter
  object — an equality lookup silently becomes an operator query.
- **Command injection (`admin_ping`).** The `host` value is concatenated into a
  shell string run with `shell=True`, so shell metacharacters run arbitrary OS
  commands.

**Run the ZAP test.**

```bash
./steps/01-run-targeted-injection-scan.sh
```

**Inspect the actual evidence.** The step builds the `m1demo1` policy (only the
injection rules enabled), scans the three endpoints, and prints one alert per
endpoint, each tied to a specific parameter:

- SQL injection — alert `40018` on `/search`, parameter `q`
- MongoDB NoSQL injection — alert `40033` on `/api/account`, parameter `username`
- Command injection — alert `90020` on `/admin/ping`, parameter `host`

Each line shows the live risk/confidence from your run. These are ZAP's own
findings, returned from the scan the command just ran.

**The engineer's decision.** Three code sinks, three distinct mechanisms, three
parameter-specific alerts from one focused policy — not a broad rule dump. That is
a targeted scan Maya can defend.

Proof artifact: Targeted scan policy and rule list.

---

## Step 2: Confirm reflected XSS in its output context (EO1b)

**The problem.** Input appearing in a page is not proof of XSS. The single `name`
value lands in three output contexts, and a payload that executes in one is inert
in another. Maya must prove the reflection is *executable*, not merely present.

**Inspect the vulnerable code in VS Code.**

```bash
./scripts/show_code.sh xss       # runtime/app/main.py  greet()  lines 257–277
```

**Why it's vulnerable.** The vulnerable build assigns the raw `name` to all three
sinks with no encoding (lines 257–261), then writes them into three contexts
(lines 271–277):

- **HTML body** — `<p>Hello {name}</p>` → a `<script>` tag executes directly.
- **HTML attribute** — `value="{name}"` → a payload must first break out with `">`.
- **JavaScript string** — `var greeting = "{name}"` → a payload must break out with `";`.

The context decides the payload. The remediated build encodes each sink
differently (`html.escape`, attribute-quoting, JS-string escaping), which is why
one fix does not cover all three.

**Run the ZAP test.**

```bash
./steps/02-verify-reflected-xss-contexts.sh
```

**Inspect the actual evidence.** The step first shows `name` reflected in all three
contexts, then runs ZAP's reflected-XSS rules and raises **Cross Site Scripting
(Reflected)** on parameter `name`, printing the payload ZAP injected (for example
`</p><scrIpt>alert(1);</scRipt><p>`) and the evidence string reflected verbatim in
the response — the request and response that confirm execution, not just reflection.

**The engineer's decision.** The context mapping chose where the payload must break
out; ZAP's alert is what confirms the reflection is executable there. Reflection
alone is not that proof — the active-scanner alert is.

Proof artifact: XSS request and response body.

---

## Step 3: Reuse a CSRF token across sessions (EO1c)

**The problem.** An anti-CSRF token defends a state change only if it is bound to
the session it was issued to. If the server checks only that *a* token exists, a
token minted in one session can be replayed with a different session's cookie.

**Inspect the vulnerable code in VS Code.**

```bash
./scripts/show_code.sh csrf      # runtime/app/main.py  change_email()  lines 332–336
```

**Why it's vulnerable.** `change_email()` looks the token up and rejects a missing
one (lines 326–330), so a token check *is* present. But in the vulnerable build the
branch that should enforce ownership is a bare `pass` (lines 332–337): it never
compares `record["session"]` to the submitting session's cookie, and never marks
the token used, before applying the change. The token is minted *with* its session
in `_issue_csrf()` (lines 284–287), yet that binding is never checked. The
remediated build adds exactly that check (`record["session"] != sid → 403`).

**Run the ZAP test.**

```bash
./steps/03-test-cross-session-csrf-token.sh
```

**Inspect the actual evidence.** The step opens two independent authenticated
sessions (A = `mallory`, B = `alice`) and sends three requests to `/account/email`:

- valid control — session B's own token → `200`
- missing-token control → `403`
- **cross-session** — session A's token submitted with session B's cookie → `200`,
  and session B's stored email changes from `alice@globomantics.example` to
  `attacker@evil.example`

**The engineer's decision.** The two controls prove the token check is active, yet
the cross-session request still succeeds and mutates state — exactly what the empty
`pass` branch allows. This is token reuse *across sessions*, caused by validating a
token's existence but not its session ownership; it is not a claim that same-session
replay is inherently vulnerable (that matters only when the app requires single-use
tokens).

Proof artifact: CSRF token replay result.

---

## Step 4: Record an alert disposition (EO1a · EO1b · EO1c)

**The problem.** Raw scanner output is not a decision. Each finding must be
reconciled with observed application behavior before it is recorded as confirmed.

**Open the record template.** The disposition template is
[`docs/alert-disposition-template.md`](../../../docs/alert-disposition-template.md) —
one row per finding, pairing the alert with the behavior that confirms it.

**Run the reconciliation.**

```bash
./steps/04-reconcile-security-alerts.sh
```

**Inspect the actual evidence.** The step re-confirms each finding directly from the
live app:

- SQL injection — the database error `unterminated quoted string` from `/search`
- NoSQL injection — the account count rising (1 → 4) under an operator-injection
  query on `/api/account`
- Command injection — the ping output `bytes from 127.0.0.1` from `/admin/ping`
- Reflected XSS — the marker reflected unescaped from `/greet`

**The engineer's decision.** Every alert is now tied to an observed application
behavior, turning raw scanner output into a defensible disposition recorded in the
template.

Proof artifact: Alert disposition record.

---

## Validate and reset

`./scripts/preflight_check.sh` runs all four steps and writes a reviewable log to
`logs/`, ending with `5 checks passed, 0 failed`. Tear down with
`./scripts/demo_down.sh`.

Optional: `./scripts/show_code.sh {sqli|nosql|cmd|xss|csrf}` prints the exact
vulnerable line(s) from `runtime/app/main.py`. The remediated build
(`APP_BUILD=remediated docker compose up -d --build app`) removes the injection
alerts, encodes the XSS output (no reflected-XSS alert), and rejects the
cross-session CSRF request with `403`.
