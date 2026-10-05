# Write a JavaScript Security Script in ZAP

In this lab you **extend ZAP itself**: you write a small **JavaScript HTTP Sender
script** that stamps a marker header on every request ZAP sends, and reports what
it did.

You read the script in your **code editor** and run each step from your
**terminal**. The script runs *inside ZAP* (an HTTP Sender script only runs
there); each terminal command drives ZAP for you and shows the result, so you
never have to click through the ZAP window.

---

## How to read this lab

| Label | Meaning |
|-------|---------|
| 📄 **In your editor** | Open or read this file in your code editor. |
| 💻 **Run in your terminal** | Copy-paste this command. |
| ✅ **You'll see** | A **result to read** — confirm it. **Never type it as a command.** |

> **Golden rule:** the only thing you *type* is the line under 💻. Everything under
> ✅ is output you *read*.

---

## The problem you are solving

Default scanning applies the same behavior to every target. Real testing often
needs *your* behavior on every request — a marker header, a tenant tag, a custom
signature. ZAP's scripting lets you add exactly that. Here you write an HTTP
Sender script that stamps a marker header on each outbound request and reports
what it did, then save it so it can be reused later without editing ZAP.

**What you gain:** you can extend ZAP with your own JavaScript instead of being
limited to its built-in behavior — the first step toward custom, repeatable
security checks.

> **Authorization and scope.** This script runs **only** against the local
> Globomantics app. Never point it at any system you are not authorized to test.

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

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Read the HTTP Sender script source and load it into ZAP | EO2a | JavaScript source file |
| 2 | Confirm the script adds the marker header to a real request | EO2a | Modified HTTP request |
| 3 | See the named line the script prints to the console | EO2a | Script console output |
| 4 | Confirm the reusable script name and path | EO2a | Saved script registration |

---

## Run it step by step

Bring the stack up once, then run each step on its own screen. Each command
prints a header saying **what** it shows and **why**, then a green **PASS**.

```bash
cd module1/m1-c4-write-a-javascript-security-script-in-zap
./scripts/demo_up.sh        # wait for "Up" (starts Colima + the stack if needed)
./scripts/demo_step.sh 1    # JavaScript source file  (loads it into ZAP)
./scripts/demo_step.sh 2    # Modified HTTP request    (marker header added)
./scripts/demo_step.sh 3    # Script console output    (named console line)
./scripts/demo_step.sh 4    # Saved script registration
```

Open [`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js)
in your editor to read the source alongside the steps. (To validate all four at
once, run `./scripts/preflight_check.sh`; when finished, `./scripts/demo_down.sh`.)

---

## Step 1 — Read the script source and load it into ZAP

An HTTP Sender script is the hook ZAP runs for **every** message it sends — the
perfect place to add your own behavior.

📄 **In your editor:** open
[`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js) and
read `sendingRequest()` — it adds the marker header and prints the named line.

💻 **Run in your terminal** to load that source into ZAP as an HTTP Sender script:

```bash
./scripts/demo_step.sh 1
```

✅ **You'll see** the source validated and loaded (output — read it, don't type it):

```text
WHAT: The JavaScript HTTP Sender script
  ★ Script name: globomantics-marker   (type: HTTP Sender · engine: ECMAScript : Graal.js)
  ★ Marker header it adds: X-Globomantics-Marker: GLOBO-DEMO
  ★ Named console line it prints: [globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to <url>
✔ PASS  script is a valid HTTP Sender action and loaded into ZAP
```

**Proof artifact:** *JavaScript source file.*

---

## Step 2 — Confirm the marker header is added to a real request

Loading a script is not enough — you want to *see* it change a real message.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 2
```

✅ **You'll see** the marker header on a real outbound request ZAP sent (output —
read it, don't type it):

```text
WHAT: The marker header on an outbound request
  ★ Outbound request: GET http://app:8000/greet?name=marker-check HTTP/1.1
  ★ Header added by the script: X-Globomantics-Marker: GLOBO-DEMO
✔ PASS  the script added X-Globomantics-Marker to the outbound request
```

**Proof artifact:** *Modified HTTP request.*

---

## Step 3 — See the named console output

A script you can trust tells you what it did. Your script prints a named line
every time it runs.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 3
```

✅ **You'll see** the named console line the script prints each time it runs
(output — read it, don't type it):

```text
WHAT: The named console output the script prints
  ★ Console line (seen in ZAP's Script Console): [globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to <url>
✔ PASS  the script prints a named console line each time its action runs
```

**Proof artifact:** *Script console output.*

---

## Step 4 — Confirm the reusable script registration

A saved, named script is what an automated run can call later without editing
ZAP. Here you confirm exactly how it is registered.

💻 **Run in your terminal:**

```bash
./scripts/demo_step.sh 4
```

✅ **You'll see** the registration details (output — read it, don't type it):

```text
WHAT: The saved, reusable script registration
  ★ Registered name: globomantics-marker
  ★ Type: httpsender
  ★ Engine: ECMAScript : Graal.js
  ★ Enabled: true
  ★ Path (repo): zap-scripts/globomantics-marker.js
✔ PASS  script is registered as a reusable HTTP Sender script
```

**Proof artifact:** *Saved script registration.*

---

## Check your work (automated)

Run every step in order through the checker; it writes a reviewable plain-text
log to `logs/` with each step's command and output in sequence.

💻 **Run in your terminal:**

```bash
./scripts/preflight_check.sh
```

✅ **You'll see** each step report **PASS**, ending with
`5 checks passed, 0 failed`. (On a failure it prints the exact reason and how to
fix it.)

💻 When you are finished, tear the stack down:

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
