# Write Python scan and authentication scripts in ZAP

Extend ZAP with two Jython scripts — a custom active-scan rule and an
authentication script — then run the rule against a login-only Globomantics page
and confirm it raises your alert. You author both scripts in ZAP's Script Console;
each `./scripts/demo_step.sh N` command verifies one beat.

> **Authorization and scope.** These scripts run only against the local
> Globomantics application.

## Setup

From `module1/m1-c5`, start the stack and open the ZAP GUI:

```bash
./scripts/demo_reset.sh          # prints "Up"; then open http://localhost:8080/zap/
```

The Python Scripting (jython) add-on installs in the ZAP container at startup.
Reference sources:
[`zap-scripts/globomantics-active-rule.py`](zap-scripts/globomantics-active-rule.py)
and [`zap-scripts/globomantics-auth.py`](zap-scripts/globomantics-auth.py).

## Learning-objective coverage

| Step | Objective | Proof artifact |
|------|-----------|----------------|
| 1 | EO2b | Python active-rule source |
| 2 | EO2c | Authentication script source |
| 3 | EO2c | Authenticated custom-scan result |
| 4 | EO2b | Custom alert record |

## Step 1: Write the Jython active-scan rule (EO2b)

Goal: Create a Globomantics-specific active-scan rule that a built-in rule does not
cover — it probes a parameter and raises a named alert when the response reflects
the probe without encoding.

In ZAP: Scripts → Active Rules → new script on the Python (jython) engine, named
`globomantics-active-rule`; paste the source, save, and enable it.

```bash
./scripts/demo_step.sh 1
```

Expected output: the rule validated and loaded as an active rule on the
`python : jython` engine, declaring the alert `Globomantics unsafe reflection
(custom rule)`.

What the learner should notice: the rule registers as an Active Rules script, so ZAP
invokes it during an active scan alongside the built-in rules — this is how you add
a house-specific check.

Proof artifact: Python active-rule source.

## Step 2: Write the authentication script (EO2c)

Goal: Teach ZAP how to log in, so a scan can reach pages that require a session.

In ZAP: Scripts → Authentication → new script on the Python (jython) engine, named
`globomantics-auth`; paste the source (it submits `username` to `POST /login`) and
save.

```bash
./scripts/demo_step.sh 2
```

Expected output: the script validated and registered as an authentication script on
the `python : jython` engine, submitting `username=alice` to `POST /login`.

What the learner should notice: the authentication type is separate from the active
rule; ZAP uses it to obtain and reuse a session so scans run as a real user.

Proof artifact: Authentication script source.

## Step 3: Run scripted authentication against the login-only page (EO2c)

Goal: Have ZAP run the authentication script to obtain a session and reach a page
gated behind login — with no cookie supplied by hand.

In ZAP: add `http://localhost:8000` to a new Context; set Authentication to
Script-based using `globomantics-auth` (Login URL `http://localhost:8000/login`,
logged-in indicator `Signed in as`); add user `alice`; enable Forced User Mode; then
Active Scan `/account/profile?note=seed`.

```bash
./scripts/demo_step.sh 3
```

Expected output: `/account/profile` returns 401 without login and 200 once ZAP
authenticates via the script, with the authentication script's trace confirming it
logged in as `alice` (`authenticate: response=200`).

What the learner should notice: the same URL moves from 401 to 200 only because ZAP
ran the authentication script — the session comes from the script, demonstrating
scripted authentication end to end.

Proof artifact: Authenticated custom-scan result.

## Step 4: Confirm the custom alert (EO2b)

Goal: Verify the custom rule raises its named alert on the authenticated scan,
freshly produced by this run.

In ZAP: open the Alerts tab and find the alert raised on `/account/profile`.

```bash
./scripts/demo_step.sh 4
```

Expected output: with the alert store cleared first (named alert absent), the
authenticated scan of `/account/profile` (parameter `note`, as user `alice`) raises
`Globomantics unsafe reflection (custom rule)` — Medium risk, parameter `note`,
evidence `GLOBOxss7marker`.

What the learner should notice: absent-before and present-after proves the alert is
from this scan, and it was produced by your rule on a session ZAP authenticated
itself — the alert a pipeline can later gate on.

Proof artifact: Custom alert record.

## Validate and reset

`./scripts/preflight_check.sh` runs all four steps, ending with
`5 checks passed, 0 failed`. Tear down with `./scripts/demo_down.sh`.

## The scripts

**Custom active-scan rule — `globomantics-active-rule.py`** (Jython 2.7.2). It
checks each query parameter by cloning the request (keeping the logged-in session),
putting a probe in the parameter, and raising the named alert if the probe reflects
unencoded. It runs from `scanNode()` so it does not depend on how ZAP enumerates
parameters:

```python
PROBE = "GLOBOxss7marker"
ALERT_NAME = "Globomantics unsafe reflection (custom rule)"

def _check(sas, msg, param):
    probe = msg.cloneRequest()                      # keeps the logged-in cookie
    pairs = ["%s=%s" % (p.getName(), PROBE if p.getName() == param else p.getValue())
             for p in msg.getUrlParams()]
    uri = probe.getRequestHeader().getURI()
    uri.setQuery("&".join(pairs))                   # put the probe in this parameter
    probe.getRequestHeader().setURI(uri)
    sas.sendAndReceive(probe, False, False)
    if PROBE in probe.getResponseBody().toString():
        alert = (sas.newAlert().setRisk(2).setConfidence(2).setName(ALERT_NAME)
                 .setDescription("Reflected without output encoding.")
                 .setParam(param).setAttack(PROBE).setEvidence(PROBE).setMessage(probe))
        getattr(alert, "raise")()                   # 'raise' is a keyword in Python

def scan(sas, msg, param, value):
    _check(sas, msg, param)

def scanNode(sas, msg):
    for p in msg.getUrlParams():
        _check(sas, msg, p.getName())
```

**Authentication script — `globomantics-auth.py`** (Jython 2.7.2):

```python
from org.apache.commons.httpclient import URI
from org.parosproxy.paros.network import HttpRequestHeader, HttpHeader
from java.net import URLEncoder
from java.lang import String
from jarray import array

def authenticate(helper, paramsValues, credentials):
    login_url = paramsValues.get("Login URL")
    username = credentials.getParam("username")
    body = "username=" + URLEncoder.encode(username, "UTF-8")
    msg = helper.prepareMessage()
    msg.setRequestHeader(
        HttpRequestHeader(HttpRequestHeader.POST, URI(login_url, False), HttpHeader.HTTP11))
    msg.getRequestHeader().setHeader(HttpHeader.CONTENT_TYPE, "application/x-www-form-urlencoded")
    msg.setRequestBody(body)
    msg.getRequestHeader().setContentLength(msg.getRequestBody().length())
    helper.sendAndReceive(msg)
    return msg

def getRequiredParamsNames():
    return array(["Login URL"], String)

def getOptionalParamsNames():
    return array([], String)

def getCredentialsParamsNames():
    return array(["username"], String)
```
