# Validate Injection, XSS, and CSRF with ZAP

A hands-on lab where you turn a broad ZAP scan into **four proven security
checks** against a deliberately vulnerable web app — the **Globomantics Store**.

You will run each step yourself, one screen at a time, and see the evidence that
each finding is real.

---

## The problem you are solving

A default scan hands you a long list of alerts, but a list is not a decision.
Which findings are real? Can you reproduce each one against the app's actual
behavior? In this lab you confirm SQL, NoSQL, and command injection, capture
reflected XSS across its output contexts, replay a CSRF token, and record a
disposition for every alert — the difference between "I ran a scanner" and "I
validated the risk."

> **Authorization and scope.** Every request here targets **only** the local
> Globomantics Store. Never point these techniques at any system you are not
> explicitly authorized to test.

---

## How to follow along

**1. Install the tools (once).** From the repo root:
```bash
./env-setup/setup-macos.sh
```
Wait until the readiness table shows every component **READY**.

**2. Start the lab.** From the repo root:
```bash
./module1/m1-c3-validate-injection-xss-and-csrf-with-zap/scripts/demo_reset.sh
```
This brings up the Globomantics Store on the **vulnerable** build and prints
**Up** when everything is healthy (ZAP takes ~90 seconds the first time). Open
the store at <http://localhost:8000/> to see what you are testing.

**3. Move into the lab folder** (every command below is relative to it):
```bash
cd module1/m1-c3-validate-injection-xss-and-csrf-with-zap
```

**4. Run the four steps, one at a time.** Read each screen, then run the next:
```bash
./scripts/run_step.sh 1     # targeted injection scan
./scripts/run_step.sh 2     # reflected XSS in three contexts
./scripts/run_step.sh 3     # CSRF token replay
./scripts/run_step.sh 4     # alert disposition
```
Each step is self-contained and prints one clean screen. Step 1 runs a real scan
(~30–60s); Steps 2–4 are instant.

> **Tip:** the exact alert IDs, risk, and confidence you see are the live values
> from your run. The samples below are from one run and may differ slightly.

---

## How to read this lab

| Label | Meaning |
|-------|---------|
| 💻 **Run in your terminal** | Copy-paste these commands into your terminal. |
| ✅ **You'll see** | This is the **output the command prints** — read it to confirm success. **Never type it as a command.** |

> **Golden rule:** the only things you ever *type* are the 💻 commands. Anything
> under ✅ is output you *read*, not a command.

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

Print this same reference in the terminal any time with `./scripts/run_step.sh ref`.

---

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Run one targeted scan and confirm SQL, NoSQL, and command injection | EO1a | Targeted scan policy and rule list |
| 2 | Capture reflected XSS across its three output contexts | EO1b | XSS request and response body |
| 3 | Replay a CSRF token and show it is accepted | EO1c | CSRF token replay result |
| 4 | Reconcile every alert with app behavior and record it | EO1a · EO1b · EO1c | Alert disposition record |

---

## Step 1 — Targeted injection scan

**Why you run this:** a scoped policy turns a broad scan into a targeted test of
specific weaknesses.
**What you learn:** how ZAP confirms SQL, NoSQL, and command injection from the
app's own responses — three injection types in one focused scan.

```bash
./scripts/run_step.sh 1
```

✅ **You'll see** this terminal output — read it, don't type it:

```text
┌──────────────────────────────────────────────────────────────────────┐
│ WHAT:  Targeted injection scan — one policy, three endpoints           │
│ WHY:   Proves SQL, NoSQL, and command injection are real findings      │
└──────────────────────────────────────────────────────────────────────┘

  ★ Policy rules enabled: SQL-injection family + NoSQL 40033 + command 90020/90037

Findings — alert raised per endpoint:

  ★ SQL injection · /search (q): alert 40018 · High/Medium

  ★ NoSQL injection · /api/account (username): alert 40033 · Medium/Medium

  ★ Command injection · /admin/ping (host): alert 90020 (or 90037)
```

Read the highlighted alert IDs — one real finding per endpoint.

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

✅ **You'll see** this terminal output — read it, don't type it:

```text
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

✅ **You'll see** this terminal output — read it, don't type it:

```text
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
**What you learn:** to reconcile each alert with what the app actually did and
mark it confirmed.

```bash
./scripts/run_step.sh 4
```

✅ **You'll see** this terminal output — read it, don't type it:

```text
┌──────────────────────────────────────────────────────────────────────┐
│ WHAT:  Alert disposition — reconcile each alert with app behavior      │
│ WHY:   Turns raw alerts into decisions you can defend (EO1a/b/c)       │
└──────────────────────────────────────────────────────────────────────┘

  ★ 40018 SQL injection · /search: confirmed — DB error: unterminated quoted string at or near "'"

  ★ 40033 NoSQL injection · /api/account: confirmed — accounts 1 → 4 under operator injection

  ★ 90020/90037 Command injection · /admin/ping: confirmed — OS command ran: bytes from 127.0.0.1

  ★ XSS reflected · /greet: confirmed — reflected unescaped
```

Record the full table in [`docs/alert-disposition-template.md`](../../docs/alert-disposition-template.md).

**Proof artifact:** *Alert disposition record.*

---

## Optional — see why a finding is exploitable (the vulnerable code)

Any time you want the "why," print the exact vulnerable line(s) from the app:

```bash
./scripts/show_code.sh sqli    # or: nosql · cmd · xss · csrf
```

It shows the line numbers, so in your editor you can jump straight to them
(VS Code: `Cmd+P` → `main.py`, then `Ctrl+G` → the line). This is a reference
aid, not one of the four steps.

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

## See the fixes hold (optional exploration)

The same app ships a **remediated** build — parameterized SQL, type-checked Mongo
input, a validated command with no shell, context-encoded XSS output, and
single-use, session-bound CSRF tokens:

```bash
APP_BUILD=remediated docker compose up -d --build app
```

Re-run the steps: the injection alerts disappear, the XSS output becomes encoded,
and the replayed CSRF token is rejected with `403`. Switch back with
`./scripts/demo_reset.sh`.
