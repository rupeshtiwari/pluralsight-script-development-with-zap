# Write Python scan and authentication scripts in ZAP

Extend ZAP with two Jython scripts — a custom active-scan rule and an
authentication script — then run the rule against a login-only Globomantics page
and confirm it raises your alert. You author both scripts in ZAP's Script Console;
each Terminal command verifies one beat.

> **Authorization and scope.** These scripts run only against the local
> Globomantics application.

## Applications and locations used

| Application | Where | Used for |
|-------------|-------|----------|
| ZAP GUI (Webswing) | `http://localhost:8080/zap/` → **Scripts**, **Sites** (Context dialog), **Alerts** tabs | authoring the scripts, configuring script-based authentication, viewing the alert |
| macOS Terminal | working directory `module1/m1-c5` | running each `./scripts/demo_step.sh N` |
| Local Globomantics app | `http://localhost:8000/account/profile?note=seed` | the login-only target (401 before login, 200 after) |
| Reference sources | `module1/m1-c5/zap-scripts/globomantics-active-rule.py`, `…/globomantics-auth.py` | the Jython you paste into the Script Console |

The Terminal commands drive the same ZAP instance the GUI shows (GUI on `:8080`,
API on `:8090`).

## Setup

```bash
cd module1/m1-c5
./scripts/demo_reset.sh          # prints "Up"; then open http://localhost:8080/zap/
```

The Python Scripting (jython) add-on installs in the ZAP container at startup.

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

Application: ZAP GUI, then macOS Terminal.
Open / Navigate: ZAP GUI (`http://localhost:8080/zap/`) → **Scripts** tab →
**Active Rules** → new script on the Python (jython) engine, named
`globomantics-active-rule`.
Execute: paste the source (`zap-scripts/globomantics-active-rule.py`), save, and
enable it. Then run `./scripts/demo_step.sh 1` in the Terminal to validate the load.

Expected output: the rule validated and loaded as an active rule on the
`python : jython` engine, declaring the alert `Globomantics unsafe reflection
(custom rule)`.

What the learner should notice: the rule registers as an Active Rules script, so ZAP
invokes it during an active scan alongside the built-in rules — this is how you add
a house-specific check.

Proof artifact: Python active-rule source.

## Step 2: Write the authentication script (EO2c)

Goal: Teach ZAP how to log in, so a scan can reach pages that require a session.

Application: ZAP GUI, then macOS Terminal.
Open / Navigate: ZAP GUI → **Scripts** tab → **Authentication** → new script on the
Python (jython) engine, named `globomantics-auth`.
Execute: paste the source (`zap-scripts/globomantics-auth.py`; it submits `username`
to `POST /login`) and save. Then run `./scripts/demo_step.sh 2` to validate the
registration.

Expected output: the script validated and registered as an authentication script on
the `python : jython` engine, submitting `username=alice` to `POST /login`.

What the learner should notice: the authentication type is separate from the active
rule; ZAP uses it to obtain and reuse a session so scans run as a real user.

Proof artifact: Authentication script source.

## Step 3: Run scripted authentication against the login-only page (EO2c)

Goal: Have ZAP run the authentication script to obtain a session and reach a page
gated behind login — with no cookie supplied by hand.

Application: ZAP GUI (Context + Forced User Mode), then macOS Terminal.
Open / Navigate: ZAP GUI → **Sites** tree → right-click `http://localhost:8000` →
**Include in Context → New Context**.
Execute: in the Context dialog —
- **Authentication** → **Script-based Authentication** → select `globomantics-auth`;
  set **Login URL** `http://localhost:8000/login` and **Logged-in indicator (regex)**
  `Signed in as`.
- **Users** → **Add** user `alice` (username `alice`).
- Enable **Forced User Mode** (toolbar) and select `alice`, then right-click
  `/account/profile?note=seed` → **Attack → Active Scan**.

Then run `./scripts/demo_step.sh 3` in the Terminal to reproduce and verify the same
scripted login.

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

Application: ZAP GUI (Alerts tab), then macOS Terminal.
Open / Navigate: ZAP GUI → **Alerts** tab → the alert raised on `/account/profile`.
Execute: `./scripts/demo_step.sh 4` in the Terminal (it clears the alert store,
scans as `alice`, and reads the alert back).

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
