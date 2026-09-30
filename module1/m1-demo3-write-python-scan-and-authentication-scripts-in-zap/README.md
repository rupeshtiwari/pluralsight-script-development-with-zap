# Write Python Scan and Authentication Scripts in ZAP

In this lab you extend ZAP with **two Python (Jython) scripts**:

1. a **custom active-scan rule** that runs your own check during a scan, and
2. an **authentication script** that logs in for you, so the scan runs as a real
   user.

You then run the rule against a **login-only** Globomantics page and confirm it
raises your alert. You do this in the **ZAP GUI** (open
<http://localhost:8080/zap/>), not the terminal.

---

## How to read this lab

| Label | Meaning |
|-------|---------|
| 🖱️ **Do this in ZAP** | Click or type these **inside the ZAP GUI**. |
| 💻 **Run in your terminal** | Copy-paste these commands into your terminal. |
| ✅ **You'll see** | This is a **result ZAP shows you** — read it to confirm success. **Never type it as a command.** |

> **Golden rule:** the only things you ever *type* are under 🖱️ or 💻. Anything
> under ✅ is output you *read*, not a command.

---

## The problem you are solving

Built-in rules cover common issues, but every app has checks that are specific to
*it* — and the pages that matter most are usually **behind a login**. Here you
write your own active-scan rule in Python, write an authentication script so ZAP
can reach a logged-in page, and prove the rule fires there. That is the pattern
for real, repeatable, house-specific security testing.

**What you gain:** you can add your own Python checks *and* test authenticated
areas — the two things a default, unauthenticated scan cannot do for you.

> **Authorization and scope.** These scripts run **only** against the local
> Globomantics app. Never point them at any system you are not authorized to test.

---

## What you will build (reference)

| Piece | Value |
|-------|-------|
| Language / engine | Python — **Jython 2.7.2** (ZAP "Python Scripting (jython)" add-on) |
| Custom rule type | Active Rules (runs during an active scan) |
| Custom rule name | `globomantics-active-rule` |
| Alert it raises | `Globomantics unsafe reflection (custom rule)` |
| Auth script type | Authentication |
| Auth script name | `globomantics-auth` |
| It logs in via | `POST /login` (username `alice`), then ZAP reuses the session cookie |
| Authenticated target | `GET /account/profile?note=…` — **401 without login**, reflects `note` when logged in |

The full sources are in
[`zap-scripts/globomantics-active-rule.py`](zap-scripts/globomantics-active-rule.py)
and [`zap-scripts/globomantics-auth.py`](zap-scripts/globomantics-auth.py) — you
copy each into the Script Console.

---

## What each step teaches (learning-objective coverage)

| Step | You will… | Objective | Proof artifact |
|------|-----------|-----------|----------------|
| 1 | Install jython, write the Python active-scan rule, save it | EO2b | Python active-rule source |
| 2 | Write the authentication script and save it separately | EO2c | Authentication script source |
| 3 | Run scripted auth + the custom rule against the login-only page | EO2b · EO2c | Authenticated custom-scan result |
| 4 | Confirm the rule raises its intended alert and record it | EO2b | Custom alert record |

---

## Before you start

💻 **Run in your terminal** — bring the stack up and open the ZAP GUI:

```bash
./module1/m1-demo3-write-python-scan-and-authentication-scripts-in-zap/scripts/demo_reset.sh
```

Wait until it prints **`Up`**, then open <http://localhost:8080/zap/>. (If the
Docker engine is stopped, this starts it for you and waits — you do not need to
start Colima yourself. The **Python Scripting (jython)** add-on is installed in
the ZAP container automatically at startup.)

---

## Step 1 — Write the custom Python active-scan rule

An **active-scan rule** runs *your* check while ZAP scans a parameter. This one
sends a probe and flags the parameter if the response reflects it without
encoding — a Globomantics-specific check.

🖱️ **Do this in ZAP:**

1. Open the **Scripts** tab. Under **Active Rules**, choose **New Script**.
2. Set **Engine** to **Python (jython)** and name it `globomantics-active-rule`.
3. Paste the contents of
   [`zap-scripts/globomantics-active-rule.py`](zap-scripts/globomantics-active-rule.py),
   click **Save**, then **enable** it (the checkbox in the Scripts tree).

✅ **You'll see** `globomantics-active-rule` listed under **Active Rules**, in the
Python (jython) engine. That saved file **is** your Python active-rule source.

**Proof artifact:** *Python active-rule source.*

---

## Step 2 — Write the authentication script

An **authentication script** tells ZAP how to log in, so it can reach pages that
require a session.

🖱️ **Do this in ZAP:**

1. In the **Scripts** tab, under **Authentication**, choose **New Script**.
2. Set **Engine** to **Python (jython)** and name it `globomantics-auth`.
3. Paste the contents of
   [`zap-scripts/globomantics-auth.py`](zap-scripts/globomantics-auth.py) and
   click **Save**.

✅ **You'll see** `globomantics-auth` listed under **Authentication**, saved
separately from the rule. That is your authentication script source.

**Proof artifact:** *Authentication script source.*

---

## Step 3 — Run scripted authentication and the custom rule together

Now prove the two work as a pair: log in with the script, then let the custom
rule scan a page that only exists **when you are logged in**.

🖱️ **Do this in ZAP:**

1. Create a **Context**, add `http://localhost:8000` to it, and set its
   **Authentication** to **Script-based** → `globomantics-auth`, with **Login
   URL** `http://localhost:8000/login`.
2. Add a **user** (`alice`) and set a **logged-in indicator** of `Signed in as`.
3. Enable **forced-user mode** for that user, then **Active Scan** the URL
   `http://localhost:8000/account/profile?note=seed`.

✅ **You'll see** the page is **HTTP 401 without login** and **HTTP 200 once the
script authenticates** — so the scan runs as `alice`, and the custom rule reaches
the authenticated content:

```text
Without login:        /account/profile -> 401 (gated)
After scripted login: /account/profile -> 200 (reachable)
```

**Proof artifact:** *Authenticated custom-scan result.*

---

## Step 4 — Confirm the custom alert

A rule you can trust ends in a clear, named alert.

🖱️ **Do this in ZAP:**

1. Open the **Alerts** tab.
2. Find the alert your rule raised on `/account/profile`.

✅ **You'll see** your custom alert recorded (read it — do not type it):

```text
Alert:      Globomantics unsafe reflection (custom rule)
Risk:       Medium
Parameter:  note
```

That alert is what a pipeline can later gate on. **Proof artifact:** *Custom alert record.*

---

## Check your work (optional, automated)

You authored the demo in the GUI. To **prove** both scripts behave correctly, run
the checker: it loads both scripts through the ZAP API, logs in, runs the custom
rule against the authenticated page, and confirms the alert — writing a reviewable
log to `logs/`.

💻 **Run in your terminal:**

```bash
cd module1/m1-demo3-write-python-scan-and-authentication-scripts-in-zap
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

## The scripts

**Custom active-scan rule — `globomantics-active-rule.py`** (Jython 2.7.2):

```python
PROBE = "GLOBOxss7'\"<globo>"
ALERT_NAME = "Globomantics unsafe reflection (custom rule)"

def scan(sas, msg, param, value):
    probe_msg = msg.cloneRequest()
    sas.setParam(probe_msg, param, PROBE)
    sas.sendAndReceive(probe_msg)
    body = probe_msg.getResponseBody().toString()
    if PROBE in body:
        sas.raiseAlert(2, 2, ALERT_NAME,
            "The parameter value is reflected without output encoding.",
            probe_msg.getRequestHeader().getURI().toString(),
            param, PROBE, "", "Encode output for its context.", PROBE,
            79, 20, probe_msg)

def scanNode(sas, msg):
    pass
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
