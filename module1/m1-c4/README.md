# Write a JavaScript security script in ZAP

Extend ZAP with a JavaScript HTTP Sender script that stamps a marker header on
every request it sends and logs what it did — the foundation for custom,
repeatable checks.

> **Authorization and scope.** This script runs only against the local
> Globomantics application.

## Applications and locations used

| Application | Where | Used for |
|-------------|-------|----------|
| ZAP GUI (Webswing) | `http://localhost:8080/zap/` → **Scripts** tab (HTTP Sender) and the Script Console output pane | authoring the script and showing its console output |
| macOS Terminal | working directory `module1/m1-c4` | running each `./scripts/demo_step.sh N` |
| Reference source | `module1/m1-c4/zap-scripts/globomantics-marker.js` | the JavaScript you paste into the Script Console |

You author the script in ZAP's Script Console; each Terminal command verifies one
beat against the same running ZAP instance (GUI on `:8080`, API on `:8090`).

## Setup

```bash
cd module1/m1-c4
./scripts/demo_up.sh             # prints "Up" when healthy
```

Open `http://localhost:8080/zap/` for the Script Console.

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

Application: ZAP GUI, then macOS Terminal.
Open / Navigate: ZAP GUI (`http://localhost:8080/zap/`) → **Scripts** tab →
**HTTP Sender** → new script on the GraalVM JavaScript engine, named
`globomantics-marker`.
Execute: in `sendingRequest()` set the `X-Globomantics-Marker` header and print the
named console line (source: `zap-scripts/globomantics-marker.js`); save. Then, in
the Terminal, run `./scripts/demo_step.sh 1` to validate and load it.

Expected output: the script validated and loaded as an HTTP Sender action on the
`ECMAScript : Graal.js` engine, adding header `X-Globomantics-Marker: GLOBO-DEMO`.

What the learner should notice: the HTTP Sender type is the hook that runs for every
outbound message, which is why a marker set here applies to all ZAP traffic.

Proof artifact: JavaScript source file.

## Step 2: Confirm the marker on a real request (EO2a)

Goal: Verify the script modifies an actual outbound message, not just that it
loaded.

Application: macOS Terminal.
Open / Navigate: Terminal in `module1/m1-c4`.
Execute: `./scripts/demo_step.sh 2`.

Expected output: an outbound `GET http://app:8000/greet?...` request carrying
`X-Globomantics-Marker: GLOBO-DEMO`.

What the learner should notice: the header appears on a request ZAP actually sent,
confirming the script executes in the sending path rather than only existing in the
editor.

Proof artifact: Modified HTTP request.

## Step 3: Produce named console output (EO2a)

Goal: Show the script reports what it did, so its behavior is observable and
auditable.

Application: macOS Terminal, with the same line visible in the ZAP Script Console.
Open / Navigate: Terminal in `module1/m1-c4`; the same output appears in the ZAP GUI
Script Console output pane (Scripts tab, `globomantics-marker` selected).
Execute: `./scripts/demo_step.sh 3`.

Expected output: the console line `[globo-marker] added X-Globomantics-Marker:
GLOBO-DEMO to <url>`.

What the learner should notice: a fixed, named output line makes the script's action
verifiable on each run — the basis for trusting it in automation.

Proof artifact: Script console output.

## Step 4: Save the reusable script registration (EO2a)

Goal: Confirm the saved name, type, and path that the Automation Framework will call
later.

Application: macOS Terminal.
Open / Navigate: Terminal in `module1/m1-c4`.
Execute: `./scripts/demo_step.sh 4`.

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
