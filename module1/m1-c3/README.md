# Validate Injection, XSS, and CSRF with ZAP

Turn a broad ZAP scan into **four proven security checks** against a deliberately
vulnerable web app — the **Globomantics Store**. You run each step yourself, one
screen at a time, and read the evidence that each finding is real.

---

## The problem you are solving

A default scan hands you a long list of alerts, but a list is not a decision.
Which findings are real? Can you reproduce each one against the app's actual
behavior? Here you confirm SQL, NoSQL, and command injection, capture reflected
XSS across its output contexts, reuse a CSRF token across sessions, and record a disposition
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
./scripts/demo_step.sh 3     # CSRF token reused across sessions
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
| valid for this session | the request should succeed |
| missing / invalid | the request should be rejected |
| a valid token reused with a **different** session's cookie | the request should be rejected — a token must be tied to the session it was issued to (same-session reuse only matters when the app requires single-use tokens) |

---

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Run one targeted scan and confirm SQL, NoSQL, and command injection | EO1a | Targeted scan policy and rule list |
| 2 | Match the output context, then confirm reflected XSS with ZAP's own alert | EO1b | XSS request and response body |
| 3 | Reuse a token across sessions and show the protected action still runs | EO1c | CSRF token replay result |
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

## Step 2 — Match the context, then confirm reflected XSS

**Why you run this / what you learn:** the payload that works depends on *where*
your input lands, so you first map the output context for the `name` parameter —
then ZAP's active scanner injects a real payload and raises
**Cross Site Scripting (Reflected)** only when the reflection is actually
exploitable. Reflection alone is not the proof; ZAP's alert is.

**Do this:**
```bash
./scripts/demo_step.sh 2
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: Reflected XSS — match the context, then let ZAP confirm it
Output contexts for the 'name' parameter (choose a payload per context):
  ★ HTML body — use <script>…</script>: <p>Hello zzMARKzz
  ★ HTML attribute — break out with ">…: value="zzMARKzz"
  ★ JS string — break out with ";…: var greeting = "zzMARKzz"
ZAP's confirmed finding:
  ★ Alert: Cross Site Scripting (Reflected)
  ★ Affected parameter: name
  ★ Payload ZAP injected: </p><scrIpt>alert(1);</scRipt><p>
  ★ Evidence (reflected in the response): </p><scrIpt>alert(1);</scRipt><p>
✔ PASS  ZAP confirmed reflected XSS on 'name' with a context-specific payload (and the input lands in all three contexts)
```

**What to highlight:** ZAP's **Cross Site Scripting (Reflected)** alert on
parameter `name` — the payload it injected (`</p><scrIpt>…</scRipt><p>`) breaks
out of the HTML body context and is reflected verbatim as evidence. That alert,
not the plain reflection, is what confirms executable XSS.

**Proof artifact:** *XSS request and response body.*

---

## Step 3 — CSRF token reused across sessions

**Why you run this / what you learn:** a CSRF token must be **tied to the session
it was issued to**. You open two independent logins, mint a token in session A,
and submit it with session B's cookie. On the vulnerable build the protected
email change is accepted and session B's stored email actually changes — proof
the token is not bound to its session. (This is token reuse *across sessions*;
rejecting a token *reused in the same session* only matters if the app requires
single-use tokens.) Valid-token and missing-token cases are the controls.

**Do this:**
```bash
./scripts/demo_step.sh 3
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: CSRF — a token reused across sessions
  ★ valid token (session B's own): 200
  ★ missing token: 403
  ★ session B's email before the cross-session request: alice@globomantics.example
  ★ token from session A, submitted with session B's cookie: 200  (should be rejected)
  ★ session B's email after the cross-session request: attacker@evil.example
✔ PASS  session A's token was accepted with session B's cookie (200) and changed session B's email to attacker@evil.example — the token is not tied to its session
```

**What to highlight:** the controls behave (valid `200`, missing `403`), but the
highlighted cross-session `200` — session A's token accepted under session B's
cookie — **changes session B's email** from `alice@globomantics.example` to
`attacker@evil.example`. The state actually changed: that is the bypass.

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

Re-run the steps: the injection alerts disappear, the XSS output becomes encoded
(no `Cross Site Scripting (Reflected)` alert), and the cross-session CSRF request
is rejected with `403` because the token is now bound to its session. Switch back
with `./scripts/demo_reset.sh`.
