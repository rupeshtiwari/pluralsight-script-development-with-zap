# Validate Injection, XSS, and CSRF with ZAP

Turn a broad ZAP scan into **four proven security checks** against a deliberately
vulnerable web app — the **Globomantics Store**. You run each step yourself, one
screen at a time, and read the evidence that each finding is real.

---

## The problem you are solving

A default scan hands you a long list of alerts, but a list is not a decision.
Which findings are real? Can you reproduce each one against the app's actual
behavior? Here you confirm SQL, NoSQL, and command injection, capture reflected
XSS across its output contexts, replay a CSRF token, and record a disposition
for every alert — the difference between "I ran a scanner" and "I validated the
risk."

> **Authorization and scope.** Every request here targets **only** the local
> Globomantics Store. Never point these techniques at any system you are not
> explicitly authorized to test.

---

## How to read this lab

| Label | Meaning |
|-------|---------|
| 💻 **Run in your terminal** | Copy-paste this command. It is the only thing you type. |
| ✅ **You'll see** | Output to **read** and confirm. **Never type it as a command.** |

> **Golden rule:** the only things you ever *type* are the 💻 commands. Anything
> under ✅ is output you *read*.

---

## Set up and run

**1. Install the tools once**, from the repo root:
```bash
./env-setup/setup-macos.sh
```
Wait until the readiness table shows every component **READY**.

**2. Start the lab** (vulnerable build, prints **Up** when healthy; ZAP takes
~90s the first time):
```bash
./module1/m1-c3/scripts/demo_reset.sh
```

**3. Move into the lab folder** (every command below is relative to it):
```bash
cd module1/m1-c3
```

**4. Run the four steps, one at a time** — read each screen, then run the next:
```bash
./scripts/demo_step.sh 1     # targeted injection scan        (~30–60s)
./scripts/demo_step.sh 2     # reflected XSS in three contexts
./scripts/demo_step.sh 3     # CSRF token replay
./scripts/demo_step.sh 4     # alert disposition record
```

> **Tip:** the exact alert IDs, risk, and confidence are the live values from
> your run; the samples below are from one real run and may differ slightly.
> Print the context / token-state reference any time with
> `./scripts/demo_step.sh ref`.

---

## Reference — map each case to its context / state

| XSS output context | Where the input lands |
|--------------------|-----------------------|
| HTML body | between tags |
| HTML attribute | inside a quoted attribute value |
| JavaScript string | inside a quoted JS string |

| CSRF token state | Expected result |
|------------------|-----------------|
| valid | the request should succeed |
| missing / invalid | the request should be rejected |
| replayed (already used once) | the request should be rejected |

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

**Why you run this / what you learn:** a scoped policy turns a broad scan into a
targeted test of specific weaknesses — here, how ZAP confirms SQL, NoSQL, and
command injection from the app's own responses, three injection types in one
focused scan.

**Do this:**
```bash
./scripts/demo_step.sh 1
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: Targeted injection scan — one policy, three endpoints
  ★ Policy rules enabled: SQL-injection family + NoSQL 40033 + command 90020/90037
  ★ SQL injection · /search (q): alert 40018 · High/Medium
  ★ NoSQL injection · /api/account (username): alert 40033 · High/High
  ★ Command injection · /admin/ping (host): alert 90020 · High/Medium
✔ PASS  targeted scan raised all three injection alerts
```

**What to highlight:** one real finding per endpoint — the three highlighted
alert IDs (`40018`, `40033`, `90020`), each tied to a specific parameter.

**Proof artifact:** *Targeted scan policy and rule list.*

---

## Step 2 — Reflected XSS in three contexts

**Why you run this / what you learn:** the payload that works depends on *where*
your input lands in the page, so you identify the output context first — it
decides the payload you would use.

**Do this:**
```bash
./scripts/demo_step.sh 2
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: Reflected XSS — one input, three output contexts
  ★ Request: GET /greet?name=zzMARKzz
  ★ HTML body context: <p>Hello zzMARKzz
  ★ HTML attribute context: value="zzMARKzz"
  ★ JavaScript string context: var greeting = "zzMARKzz"
✔ PASS  input reflects unescaped in all three contexts
```

**What to highlight:** one input (`zzMARKzz`) reflected **unescaped** in all
three contexts — each context would need a different payload to exploit.

**Proof artifact:** *XSS request and response body.*

---

## Step 3 — CSRF token replay

**Why you run this / what you learn:** a CSRF token is only as good as its rules.
A token checked for *presence* but not *freshness* can be replayed — you test the
protection by reusing a token that was already used once.

**Do this:**
```bash
./scripts/demo_step.sh 3
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: CSRF — token replay
  ★ valid token: 200
  ★ missing token: 403
  ★ replayed token (already used once): 200
✔ PASS  replayed token is accepted (200) — the CSRF protection has no freshness check
```

**What to highlight:** presence *is* checked (missing = `403`), but the
highlighted `200` on replay shows the token is **not single-use** — it can be
replayed.

**Proof artifact:** *CSRF token replay result.*

---

## Step 4 — Alert disposition record

**Why you run this / what you learn:** validation ends in a decision. A
disposition reconciles each alert with what the app actually did and is what you
hand to a developer or keep for the record.

**Do this:**
```bash
./scripts/demo_step.sh 4
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: Alert disposition — reconcile each alert with app behavior
  ★ 40018 SQL injection · /search: confirmed — DB error: unterminated quoted string at or near "'"
  ★ 40033 NoSQL injection · /api/account: confirmed — accounts 1 → 4 under operator injection
  ★ 90020/90037 Command injection · /admin/ping: confirmed — OS command ran: bytes from 127.0.0.1
  ★ XSS reflected · /greet: confirmed — reflected unescaped
✔ PASS  all four findings reconciled with app behavior and recorded as confirmed
```

**What to highlight:** every alert is marked **confirmed** with the concrete app
behavior that proves it — not just "the scanner said so." Record the full table
in [`docs/alert-disposition-template.md`](../../docs/alert-disposition-template.md).

**Proof artifact:** *Alert disposition record.*

---

## Check your work

Run all four steps in order and write a reviewable log to `logs/`:

```bash
./scripts/preflight_check.sh
```

Each step prints **PASS** or **FAIL**; a failure prints the reason and a prompt
to fix it. It ends with `5 checks passed, 0 failed`. When you are done:

```bash
./scripts/demo_down.sh
```

---

## Optional — see the vulnerable code behind a finding

Print the exact vulnerable line(s) from the app any time:

```bash
./scripts/show_code.sh sqli    # or: nosql · cmd · xss · csrf
```

It shows line numbers so you can jump straight to them in your editor. This is a
reference aid, not one of the four steps.

---

## Optional — see the fixes hold

The same app ships a **remediated** build — parameterized SQL, type-checked Mongo
input, a validated command with no shell, context-encoded XSS output, and
single-use, session-bound CSRF tokens:

```bash
APP_BUILD=remediated docker compose up -d --build app
```

Re-run the steps: the injection alerts disappear, the XSS output becomes encoded,
and the replayed CSRF token is rejected with `403`. Switch back with
`./scripts/demo_reset.sh`.
