# Write a JavaScript security script in ZAP

Extend ZAP with a JavaScript HTTP Sender script that stamps a marker header on
every request it sends and logs what it did — the foundation for custom,
repeatable checks.

> **Authorization and scope.** This script runs only against the local
> Globomantics application.

## Setup

From `module1/m1-c4`, start the stack:

```bash
./scripts/demo_up.sh             # prints "Up" when healthy
```

You author the script in ZAP's Script Console; the reference source is in
[`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js). Each
`./scripts/demo_step.sh N` command verifies one beat against the running ZAP.

## Learning-objective coverage

| Step | Objective | Proof artifact |
|------|-----------|----------------|
| 1 | EO2a | JavaScript source file |
| 2 | EO2a | Modified HTTP request |
| 3 | EO2a | Script console output |
| 4 | EO2a | Saved script registration |

## Step 1: Write the HTTP Sender script (EO2a)

Goal: Create a request-marker action from ZAP's HTTP Sender template so your own
code runs on every message ZAP sends.

In ZAP: Scripts → HTTP Sender → new script on the GraalVM JavaScript engine, named
`globomantics-marker`; in `sendingRequest()` set the `X-Globomantics-Marker` header
and print the named console line; save.

```bash
./scripts/demo_step.sh 1
```

Expected output: the script validated and loaded as an HTTP Sender action on the
`ECMAScript : Graal.js` engine, adding header `X-Globomantics-Marker: GLOBO-DEMO`.

What the learner should notice: the HTTP Sender type is the hook that runs for every
outbound message, which is why a marker set here applies to all ZAP traffic.

Proof artifact: JavaScript source file.

## Step 2: Confirm the marker on a real request (EO2a)

Goal: Verify the script modifies an actual outbound message, not just that it
loaded.

```bash
./scripts/demo_step.sh 2
```

Expected output: an outbound `GET http://app:8000/greet?...` request carrying
`X-Globomantics-Marker: GLOBO-DEMO`.

What the learner should notice: the header appears on a request ZAP actually sent,
confirming the script executes in the sending path rather than only existing in the
editor.

Proof artifact: Modified HTTP request.

## Step 3: Produce named console output (EO2a)

Goal: Show the script reports what it did, so its behavior is observable and
auditable.

```bash
./scripts/demo_step.sh 3
```

Expected output: the console line `[globo-marker] added X-Globomantics-Marker:
GLOBO-DEMO to <url>`, as printed in ZAP's Script Console.

What the learner should notice: a fixed, named output line makes the script's action
verifiable on each run — the basis for trusting it in automation.

Proof artifact: Script console output.

## Step 4: Save the reusable script registration (EO2a)

Goal: Confirm the saved name, type, and path that the Automation Framework will call
later.

```bash
./scripts/demo_step.sh 4
```

Expected output: registration showing name `globomantics-marker`, type `httpsender`,
engine `Graal.js`, enabled `true`, path `zap-scripts/globomantics-marker.js`.

What the learner should notice: this saved identity is exactly what Module 2's
Automation Framework references, so the script is reusable without editing ZAP.

Proof artifact: Saved script registration.

## Validate and reset

`./scripts/preflight_check.sh` runs all four steps, ending with
`5 checks passed, 0 failed`. Tear down with `./scripts/demo_down.sh`.

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
