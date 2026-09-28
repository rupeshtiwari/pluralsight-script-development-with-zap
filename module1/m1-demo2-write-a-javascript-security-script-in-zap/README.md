# Write a JavaScript Security Script in ZAP

A hands-on lab where you extend ZAP itself: you write a small **JavaScript HTTP
Sender script** that marks every request ZAP sends, in ZAP's **Script Console**.

You do this in the ZAP GUI (open <http://localhost:8080/zap/>), not the terminal.

---

## The problem you are solving

Default scanning applies the same behavior to every target. Real testing often
needs *your* behavior on every request — a marker header, a tenant tag, a custom
signature. ZAP's scripting lets you add exactly that. In this lab you write an
HTTP Sender script that stamps a marker header on each outbound request and
reports what it did, then save it so it can be reused later without editing ZAP.

**What you gain:** you can extend ZAP with your own JavaScript instead of being
limited to its built-in behavior — the first step toward custom, repeatable
security checks.

> **Authorization and scope.** The script runs only against the local
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

The full source is in [`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js) — you copy it into the Script Console in Step 1.

---

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Write the HTTP Sender script from the template and save it | EO2a | JavaScript source file |
| 2 | Confirm the script adds the marker header to a real request | EO2a | Modified HTTP request |
| 3 | See the named line the script prints to the console | EO2a | Script console output |
| 4 | Save the reusable script name and path | EO2a | Saved script registration |

---

## Before you start

1. Bring the stack up and open the ZAP GUI:
   ```bash
   ./module1/m1-demo2-write-a-javascript-security-script-in-zap/scripts/demo_reset.sh
   ```
   When it prints **Up**, open <http://localhost:8080/zap/> in your browser.
2. In your browser, set the HTTP proxy to `localhost:8090` so your requests pass
   through ZAP.

---

## Step 1 — Write the HTTP Sender script and save it

**Why you do this:** an HTTP Sender script is the hook ZAP runs for every message
it sends — the place to add your own behavior.
**What you learn:** how to create a script from ZAP's template and save it with a
name.

In ZAP:
1. Open the **Scripts** tab (Tools → Scripts, or the Scripts tree).
2. Under **HTTP Sender**, choose **New Script**.
3. Set **Engine** to the JavaScript (GraalVM) engine, name it `globomantics-marker`.
4. Replace the template body with the contents of
   [`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js) and **Save**.

The saved script is your **JavaScript source file** — the marker header and the
console line are both defined in it.

**Proof artifact:** *JavaScript source file.*

---

## Step 2 — Confirm the marker header is added to a real request

**Why you do this:** loading a script proves nothing; you need to see it change a
real message.
**What you learn:** that an HTTP Sender script rewrites the outbound request.

1. Make sure the script is **enabled** (the checkbox next to it in the Scripts tree).
2. From your browser (proxied through ZAP), open the Globomantics store, e.g.
   `http://localhost:8000/greet?name=marker-check`.
3. In ZAP's **History**, select that request and open the **Request** tab.

You will see the header the script added:

```
  ★ X-Globomantics-Marker: GLOBO-DEMO
```

**Proof artifact:** *Modified HTTP request.*

---

## Step 3 — See the named console output

**Why you do this:** a script you can trust tells you what it did.
**What you learn:** how `print()` in a script surfaces named output you can read.

1. Open the **Script Console** output pane for `globomantics-marker`.
2. Send the request again (reload the page through the proxy).

The script writes a named line each time its action runs:

```
  ★ [globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to http://app:8000/greet?name=marker-check
```

**Proof artifact:** *Script console output.*

---

## Step 4 — Save the reusable script name and path

**Why you do this:** a saved, named script is what an automated run can call
later without opening ZAP.
**What you learn:** where the script is registered and how it is identified.

1. In the Scripts tree, confirm `globomantics-marker` is listed under **HTTP Sender**.
2. Note its **name** and the file it was saved from
   (`zap-scripts/globomantics-marker.js`).

```
  ★ Registered name: globomantics-marker

  ★ Type: httpsender

  ★ Path: zap-scripts/globomantics-marker.js
```

**Proof artifact:** *Saved script registration.*

---

## Check your work

The demo is authored in the GUI, but you can prove the script behaves correctly
from the terminal. This loads the script through the ZAP API, sends a request,
and verifies the marker header, the console line, and the registration — writing
a reviewable log to `logs/`:

```bash
cd module1/m1-demo2-write-a-javascript-security-script-in-zap
./scripts/preflight_check.sh
```

Every step prints **PASS** or **FAIL**; on a failure it prints the reason and a
prompt to fix it. When you are done:

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
