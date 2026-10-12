# Write a JavaScript Security Script in ZAP

**Extend ZAP itself:** you write a small **JavaScript HTTP Sender script** that
stamps a marker header on every request ZAP sends and reports what it did. You
read the script in your **code editor** and run each step from your **terminal**;
the script runs *inside ZAP*, and each command drives ZAP for you and shows the
result, so you never click through the ZAP window.

---

## The problem you are solving

Default scanning applies the same behavior to every target. Real testing often
needs *your* behavior on every request — a marker header, a tenant tag, a custom
signature. ZAP's scripting lets you add exactly that. Here you write an HTTP
Sender script that stamps a marker header on each outbound request and reports
what it did, then save it so it can be reused later without editing ZAP.

**What you gain:** you extend ZAP with your own JavaScript instead of being
limited to its built-in behavior — the first step toward custom, repeatable
security checks.

> **Authorization and scope.** This script runs **only** against the local
> Globomantics app. Never point it at any system you are not authorized to test.

---

## How to read this lab

| Label | Meaning |
|-------|---------|
| 📄 **In your editor** | Open or read this file in your code editor. |
| 💻 **Run in your terminal** | Copy-paste this command. It is the only thing you type. |
| ✅ **You'll see** | Output to **read** and confirm. **Never type it as a command.** |

> **Golden rule:** the only thing you *type* is the line under 💻. Everything
> under ✅ is output you *read*.

---

## What this script does (reference)

| Piece | Value |
|-------|-------|
| Script type | HTTP Sender (runs for every message ZAP sends) |
| Language / engine | JavaScript (GraalVM) |
| Marker header it adds | `X-Globomantics-Marker: GLOBO-DEMO` |
| Named console line it prints | `[globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to <url>` |
| Saved name | `globomantics-marker` |

The full source is in
[`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js) — open
it in your editor to read it in Step 1.

---

## Set up and run

Bring the stack up once, then run each step on its own screen:

```bash
cd module1/m1-c4
./scripts/demo_up.sh        # wait for "Up" (starts Colima + the stack if needed)
./scripts/demo_step.sh 1    # JavaScript source file      (loads it into ZAP)
./scripts/demo_step.sh 2    # Modified HTTP request        (marker header added)
./scripts/demo_step.sh 3    # Script console output        (named console line)
./scripts/demo_step.sh 4    # Saved script registration
```

Open [`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js)
in your editor to read the source alongside the steps.

---

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Read the HTTP Sender script source and load it into ZAP | EO2a | JavaScript source file |
| 2 | Confirm the script adds the marker header to a real request | EO2a | Modified HTTP request |
| 3 | See the named line the script prints to the console | EO2a | Script console output |
| 4 | Confirm the reusable script name and path | EO2a | Saved script registration |

---

## Step 1 — Read the script source and load it into ZAP

**Why you run this / what you learn:** an HTTP Sender script is the hook ZAP runs
for **every** message it sends — the perfect place to add your own behavior. You
read the source, then load it into ZAP as an HTTP Sender script.

**Do this:**

📄 **In your editor:** open
[`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js) and
read `sendingRequest()` — it adds the marker header and prints the named line.

💻 **In your terminal:**
```bash
./scripts/demo_step.sh 1
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: The JavaScript HTTP Sender script
  ★ Script name: globomantics-marker   (type: HTTP Sender · engine: ECMAScript : Graal.js)
  ★ Marker header it adds: X-Globomantics-Marker: GLOBO-DEMO
  ★ Named console line it prints: [globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to <url>
✔ PASS  script is a valid HTTP Sender action and loaded into ZAP
```

**What to highlight:** the script is registered as an **HTTP Sender** action on
the **Graal.js** engine — the hook type that runs on every message.

**Proof artifact:** *JavaScript source file.*

---

## Step 2 — Confirm the marker header is added to a real request

**Why you run this / what you learn:** loading a script is not enough — you want
to *see* it change a real message ZAP sends.

**Do this:**
```bash
./scripts/demo_step.sh 2
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: The marker header on an outbound request
  ★ Outbound request: GET http://app:8000/greet?name=marker-check HTTP/1.1
  ★ Header added by the script: X-Globomantics-Marker: GLOBO-DEMO
✔ PASS  the script added X-Globomantics-Marker to the outbound request
```

**What to highlight:** the `X-Globomantics-Marker: GLOBO-DEMO` header on a real
outbound request — proof the script changed the message, not just loaded.

**Proof artifact:** *Modified HTTP request.*

---

## Step 3 — See the named console output

**Why you run this / what you learn:** a script you can trust tells you what it
did. Yours prints a named line every time it runs.

**Do this:**
```bash
./scripts/demo_step.sh 3
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: The named console output the script prints
  ★ Console line (seen in ZAP's Script Console): [globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to <url>
✔ PASS  the script prints a named console line each time its action runs
```

**What to highlight:** the `[globo-marker]` console line — the same line you see
in ZAP's Script Console output pane each time the script runs.

**Proof artifact:** *Script console output.*

---

## Step 4 — Confirm the reusable script registration

**Why you run this / what you learn:** a saved, named script is what an automated
run can call later without editing ZAP. Here you confirm exactly how it is
registered.

**Do this:**
```bash
./scripts/demo_step.sh 4
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: The saved, reusable script registration
  ★ Registered name: globomantics-marker
  ★ Type: httpsender
  ★ Engine: Graal.js
  ★ Enabled: true
  ★ Path (repo): zap-scripts/globomantics-marker.js
✔ PASS  script is registered as a reusable HTTP Sender script
```

**What to highlight:** the saved name `globomantics-marker`, type `httpsender`,
and `Enabled: true` — the exact identity the Automation Framework calls later.

**Proof artifact:** *Saved script registration.*

---

## Check your work

Run every step in order through the checker; it writes a reviewable plain-text
log to `logs/` with each step's command and output in sequence:

```bash
./scripts/preflight_check.sh
```

Each step reports **PASS**, ending with `5 checks passed, 0 failed`. (On a
failure it prints the exact reason and how to fix it.) When you are finished:

```bash
./scripts/demo_down.sh
```

---

## The script

```javascript
var MARKER_HEADER = "X-Globomantics-Marker";
var MARKER_VALUE  = "GLOBO-DEMO";
var CONSOLE_TAG   = "[globo-marker]";

function sendingRequest(msg, initiator, helper) {
    msg.getRequestHeader().setHeader(MARKER_HEADER, MARKER_VALUE);
    print(CONSOLE_TAG + " added " + MARKER_HEADER + ": " + MARKER_VALUE +
          " to " + msg.getRequestHeader().getURI().toString());
}

function responseReceived(msg, initiator, helper) {
}
```
