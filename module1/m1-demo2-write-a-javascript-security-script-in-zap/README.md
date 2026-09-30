# Write a JavaScript Security Script in ZAP

In this lab you **extend ZAP itself**: you write a small **JavaScript HTTP Sender
script** that stamps a marker header on every request ZAP sends, and reports what
it did — all inside ZAP's **Script Console**.

You do this in the **ZAP GUI** (open <http://localhost:8080/zap/>), not the terminal.

---

## How to read this lab

Each step is split into two clearly labeled parts so you always know what to do:

| Label | Meaning |
|-------|---------|
| 🖱️ **Do this in ZAP** | Click or type these **inside the ZAP GUI**. |
| 💻 **Run in your terminal** | Copy-paste these commands into your terminal. |
| ✅ **You'll see** | This is a **result ZAP shows you** — read it to confirm success. **Never type it as a command.** |

> **Golden rule:** the only things you ever *type* are under 🖱️ or 💻. Anything
> under ✅ is output you *read*, not a command.

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
[`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js) — you
copy it into the Script Console in Step 1.

---

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Write the HTTP Sender script from the template and save it | EO2a | JavaScript source file |
| 2 | Confirm the script adds the marker header to a real request | EO2a | Modified HTTP request |
| 3 | See the named line the script prints to the console | EO2a | Script console output |
| 4 | Confirm the reusable script name and path | EO2a | Saved script registration |

---

## Before you start

💻 **Run in your terminal** — bring the stack up and open the ZAP GUI:

```bash
./module1/m1-demo2-write-a-javascript-security-script-in-zap/scripts/demo_reset.sh
```

Wait until it prints **`Up`**, then open <http://localhost:8080/zap/> in your
browser. (If the Docker engine is stopped, this starts it for you and waits — you
do not need to start Colima yourself.)

🖱️ **Do this in ZAP** — set your browser's HTTP proxy to `localhost:8090` so your
requests pass through ZAP.

---

## Step 1 — Create and save the HTTP Sender script

An HTTP Sender script is the hook ZAP runs for **every** message it sends — the
perfect place to add your own behavior.

🖱️ **Do this in ZAP:**

1. Open the **Scripts** tab (Tools → Scripts, or the Scripts tree).
2. Under **HTTP Sender**, choose **New Script**.
3. Set **Engine** to the JavaScript (GraalVM) engine, and name it
   `globomantics-marker`.
4. Replace the template body with the contents of
   [`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js),
   then click **Save**.

✅ **You'll see** the script appear in the Scripts tree under **HTTP Sender**,
named `globomantics-marker`. That saved file **is** your JavaScript source — the
marker header and the console line are both defined in it.

**Proof artifact:** *JavaScript source file.*

---

## Step 2 — Confirm the marker header is added to a real request

Loading a script is not enough — you want to *see* it change a real message.

🖱️ **Do this in ZAP:**

1. Make sure the script is **enabled** (the checkbox next to it in the Scripts tree).
2. From your proxied browser, open a Globomantics page, for example
   `http://localhost:8000/greet?name=marker-check`.
3. In ZAP's **History**, select that request and open the **Request** tab.

✅ **You'll see** this header on the outbound request — added by your script (read
it to confirm; do not type it):

```text
X-Globomantics-Marker: GLOBO-DEMO
```

**Proof artifact:** *Modified HTTP request.*

---

## Step 3 — Read the named console output

A script you can trust tells you what it did. Your script prints a named line
every time it runs.

🖱️ **Do this in ZAP:**

1. Open the **Script Console** output pane for `globomantics-marker`.
2. Reload the page through the proxy so the script runs again.

✅ **You'll see** a line like this in the Script Console each time the script runs
(this is ZAP's output — read it, do not type it):

```text
[globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to http://app:8000/greet?name=marker-check
```

**Proof artifact:** *Script console output.*

---

## Step 4 — Confirm the reusable script registration

A saved, named script is what an automated run can call later without opening
ZAP. Here you confirm exactly how it is registered.

🖱️ **Do this in ZAP:**

1. In the Scripts tree, confirm `globomantics-marker` is listed under **HTTP Sender**.
2. Note its **name** and the file it was saved from.

✅ **You'll see** these registration details (read them to confirm; do not type them):

```text
Name:  globomantics-marker
Type:  httpsender
Path:  zap-scripts/globomantics-marker.js
```

**Proof artifact:** *Saved script registration.*

---

## Check your work (optional, automated)

You authored the demo in the GUI. To **prove** the script behaves correctly, run
the checker below: it loads the script through the ZAP API, sends a request, and
verifies the marker header, the console line, and the registration — writing a
reviewable log to `logs/`.

💻 **Run in your terminal:**

```bash
cd module1/m1-demo2-write-a-javascript-security-script-in-zap
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
