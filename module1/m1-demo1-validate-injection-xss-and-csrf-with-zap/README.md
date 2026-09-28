# Validate Injection, XSS, and CSRF with ZAP

A hands-on lab where you turn a broad ZAP scan into **four proven security
checks** against one deliberately vulnerable application — the Globomantics
training app.

---

## The problem you are solving

A default scan hands you a long list of alerts, but a list is not a decision.
Which findings are real? Can you reproduce each one against the application's
actual behavior? Security engineer **Maya Chen** at Globomantics needs to
confirm injection, XSS, and CSRF findings against concrete behavior — then write
down a defensible disposition for each. That is the difference between "I ran a
scanner" and "I validated the risk."

**What you gain:** in four short steps you run one targeted scan that proves
three injection findings, capture reflected XSS across its output contexts, show
a CSRF token being replayed, and record a disposition for every alert.

> **Authorization and scope.** Every request here targets **only** the local
> Globomantics training app. Never point these techniques at any system you are
> not explicitly authorized to test.

---

## Before you test: map each case to its context / state

| XSS execution context | Where the input lands |
|-----------------------|-----------------------|
| HTML body | between tags |
| HTML attribute | inside a quoted attribute value |
| JavaScript string | inside a quoted JS string |

| CSRF token state | Expected result |
|------------------|-----------------|
| valid | the request should succeed |
| missing / invalid | the request should be rejected |
| replayed (already used once) | the request should be rejected |

`./scripts/run_step.sh ref` prints this same reference in the terminal.

---

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Run one targeted scan and confirm SQL, NoSQL, and command injection | EO1a | Targeted scan policy and rule list |
| 2 | Capture reflected XSS across its three output contexts | EO1b | XSS request and response body |
| 3 | Replay a CSRF token and show it is accepted | EO1c | CSRF token replay result |
| 4 | Reconcile every alert with app behavior and record it | EO1a · EO1b · EO1c | Alert disposition record |

---

## Before you start

```bash
./env-setup/setup-macos.sh          # once — installs dependencies, pulls ZAP
./module1/m1-demo1-validate-injection-xss-and-csrf-with-zap/scripts/demo_reset.sh
```

Run each step on its own when you are ready (any order; each is self-contained):

```bash
cd module1/m1-demo1-validate-injection-xss-and-csrf-with-zap
./scripts/run_step.sh 1
```

`APP` below is `http://app:8000` as ZAP sees it on the container network.

---

## Step 1 — Targeted injection scan

**Why you run this:** a scoped policy turns a broad scan into a targeted test of
specific weaknesses.
**What you learn:** how ZAP confirms SQL, NoSQL, and command injection from the
application's own responses — three injection types in one focused scan.

```bash
./scripts/run_step.sh 1
```

```
┌──────────────────────────────────────────────────────────────────────┐
│ WHAT:  Targeted injection scan — one policy, three endpoints           │
│ WHY:   Proves SQL, NoSQL, and command injection are real findings      │
└──────────────────────────────────────────────────────────────────────┘

  ★ Policy rules enabled: SQL-injection family + NoSQL 40033 + command 90020/90037

Findings — alert raised per endpoint:

  ★ SQL injection · /search (q): alert 40018 · High/Medium

  ★ NoSQL injection · /api/account (username): alert 40033 · Medium/Medium

  ★ Command injection · /admin/ping (host): alert 90037 · High/Medium
```

Read the three highlighted alert IDs — one real finding per endpoint.

**Proof artifact:** *Targeted scan policy and rule list.*

---

## Step 2 — Reflected XSS in three contexts

**Why you run this:** the payload that works depends on *where* your input lands
in the page.
**What you learn:** to identify the output context first, because it decides the
payload you would use.

```bash
./scripts/run_step.sh 2
```

```
┌──────────────────────────────────────────────────────────────────────┐
│ WHAT:  Reflected XSS — one input, three output contexts                │
│ WHY:   The output context decides the payload (EO1b)                    │
└──────────────────────────────────────────────────────────────────────┘

  ★ Request: GET /greet?name=zzMARKzz

Response body — reflected unescaped:

  ★ HTML body context: <p>Hello zzMARKzz

  ★ HTML attribute context: value="zzMARKzz"

  ★ JavaScript string context: var greeting = "zzMARKzz"
```

One input, reflected unescaped in all three contexts.

**Proof artifact:** *XSS request and response body.*

---

## Step 3 — CSRF token replay

**Why you run this:** a CSRF token is only as good as its rules. A token checked
for *presence* but not *freshness* can be replayed.
**What you learn:** to test a protection by replaying a token that was already
used once.

```bash
./scripts/run_step.sh 3
```

```
┌──────────────────────────────────────────────────────────────────────┐
│ WHAT:  CSRF — token replay                                             │
│ WHY:   A token with no freshness check can be replayed (EO1c)          │
└──────────────────────────────────────────────────────────────────────┘

  ★ valid token: 200

  ★ missing token: 403

  ★ replayed token (already used once): 200
```

Presence is checked (missing = `403`), but the highlighted `200` shows the token
is **not single-use** — it can be replayed.

**Proof artifact:** *CSRF token replay result.*

---

## Step 4 — Alert disposition record

**Why you run this:** validation ends in a decision. A disposition is what you
hand to a developer or keep for the record.
**What you learn:** to reconcile each alert with what the application actually
did and mark it confirmed.

```bash
./scripts/run_step.sh 4
```

```
┌──────────────────────────────────────────────────────────────────────┐
│ WHAT:  Alert disposition — reconcile each alert with app behavior      │
│ WHY:   Turns raw alerts into decisions you can defend (EO1a/b/c)       │
└──────────────────────────────────────────────────────────────────────┘

  ★ 40018 SQL injection · /search: confirmed — DB error: unterminated quoted string

  ★ 40033 NoSQL injection · /api/account: confirmed — accounts 1 → 4 under operator injection

  ★ 90020/90037 Command injection · /admin/ping: confirmed — OS command ran: bytes from 127.0.0.1

  ★ XSS reflected · /greet: confirmed — reflected unescaped
```

Record the full table in [`docs/alert-disposition-template.md`](../../docs/alert-disposition-template.md).

**Proof artifact:** *Alert disposition record.*

---

## Check your work

Run all four steps in order and write a reviewable log to `logs/`:

```bash
./scripts/preflight_check.sh
```

Every step prints **PASS** or **FAIL**; on a failure it prints the reason and a
prompt to fix it. When you are done:

```bash
./scripts/demo_down.sh
```

---

## Optional reference — the vulnerable code (not a recorded step)

To see *why* a finding is exploitable, print the exact vulnerable line(s) from
the app. This is a reference aid, not one of the four steps above:

```bash
./scripts/show_code.sh sqli    # or: nosql · cmd · xss · csrf
```

---

## See the fixes hold (optional exploration)

The same application ships a remediated build — parameterized SQL, type-checked
Mongo input, a validated command with no shell, context-encoded XSS output, and
single-use, session-bound CSRF tokens:

```bash
APP_BUILD=remediated docker compose up -d --build app
```

Re-run the steps: the injection alerts disappear, the XSS output becomes encoded,
and the replayed CSRF token is rejected with `403`.
