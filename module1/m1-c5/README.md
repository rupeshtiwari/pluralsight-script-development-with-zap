# Write Python Scan and Authentication Scripts in ZAP

Extend ZAP with **two Python (Jython) scripts**:

1. a **custom active-scan rule** that runs your own check during a scan, and
2. an **authentication script** that logs in for you, so the scan runs as a real
   user.

You **write both scripts in the ZAP GUI** (open <http://localhost:8080/zap/>),
then run the rule against a **login-only** Globomantics page and confirm it
raises your alert. Each step also has an exact terminal command that reproduces
the same beat through the ZAP API, so you can verify your work the same way every
time.

---

## The problem you are solving

Built-in rules cover common issues, but every app has checks specific to *it* —
and the pages that matter most are usually **behind a login**. Here you write
your own active-scan rule in Python, write an authentication script so ZAP can
reach a logged-in page, and prove the rule fires there. That is the pattern for
real, repeatable, house-specific security testing.

**What you gain:** you add your own Python checks *and* test authenticated areas
— the two things a default, unauthenticated scan cannot do for you.

> **Authorization and scope.** These scripts run **only** against the local
> Globomantics app. Never point them at any system you are not authorized to test.

---

## How to read this lab

| Label | Meaning |
|-------|---------|
| 📄 **In your editor** | Open this source file to copy its contents. |
| 🖱️ **Do this in ZAP** | Click or type these **inside the ZAP GUI**. |
| 💻 **Run in your terminal** | Copy-paste this command. It reproduces/verifies the step. |
| ✅ **You'll see** | Output to **read** and confirm. **Never type it as a command.** |

> **Golden rule:** the only things you ever *type* are under 🖱️ or 💻. Anything
> under ✅ is output you *read*.

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
| 1 | Write the custom Python active-scan rule and load it | EO2b | Python active-rule source |
| 2 | Write the authentication script and register it | EO2c | Authentication script source |
| 3 | Have ZAP run the auth script to reach the login-only page | EO2c | Authenticated custom-scan result |
| 4 | Confirm the rule raises its named alert, fresh from this scan | EO2b | Custom alert record |

---

## Before you start

💻 **Run in your terminal** — bring the stack up and open the ZAP GUI:

```bash
cd module1/m1-c5
./scripts/demo_reset.sh
```

Wait until it prints **`Up`**, then open <http://localhost:8080/zap/>. (If the
Docker engine is stopped, this starts it for you. The **Python Scripting
(jython)** add-on is installed in the ZAP container automatically at startup.)

---

## Step 1 — Write the custom Python active-scan rule

**Why you run this / what you learn:** an **active-scan rule** runs *your* check
while ZAP scans a parameter. This one sends a probe and flags the parameter if
the response reflects it without encoding — a Globomantics-specific check a
built-in rule does not cover.

**Do this:**

📄 **In your editor:** open
[`zap-scripts/globomantics-active-rule.py`](zap-scripts/globomantics-active-rule.py)
to copy its contents.

🖱️ **In ZAP:** open the **Scripts** tab → under **Active Rules** choose **New
Script** → set **Engine** to **Python (jython)**, name it
`globomantics-active-rule`, paste the source, **Save**, then **enable** it (the
checkbox in the Scripts tree). It now appears under **Active Rules**.

💻 **In your terminal** (reproduces and verifies the load):
```bash
./scripts/demo_step.sh 1
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: The custom Python active-scan rule
  ★ Script name: globomantics-active-rule   (type: active · engine: python : jython)
  ★ Alert it raises: Globomantics unsafe reflection (custom rule)
✔ PASS  active-rule script is valid and loaded into ZAP as an active rule
```

**What to highlight:** the rule is registered as an **active** rule on the
**jython** engine, and names the exact alert it will raise.

**Proof artifact:** *Python active-rule source.*

---

## Step 2 — Write the authentication script

**Why you run this / what you learn:** an **authentication script** tells ZAP how
to log in, so it can reach pages that require a session.

**Do this:**

📄 **In your editor:** open
[`zap-scripts/globomantics-auth.py`](zap-scripts/globomantics-auth.py) to copy
its contents.

🖱️ **In ZAP:** in the **Scripts** tab → under **Authentication** choose **New
Script** → set **Engine** to **Python (jython)**, name it `globomantics-auth`,
paste the source, and **Save**. It now appears under **Authentication**, saved
separately from the rule.

💻 **In your terminal** (reproduces and verifies the registration):
```bash
./scripts/demo_step.sh 2
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: The scripted authentication
  ★ Script name: globomantics-auth   (type: authentication · engine: python : jython)
  ★ It submits: username=alice to POST /login, then ZAP reuses the session cookie
✔ PASS  authentication script is valid and registered in ZAP
```

**What to highlight:** the script is registered as an **authentication** script —
a different type from the rule — ready to attach to a Context.

**Proof artifact:** *Authentication script source.*

---

## Step 3 — Have ZAP run the auth script to reach the login-only page

**Why you run this / what you learn:** ZAP runs your authentication script to get
a session, then reaches a page that only exists when logged in — the session
comes from the **script**, not from a cookie you supply.

**Do this:**

🖱️ **In ZAP** — attach the script to a Context and turn on the user:
1. Visit `http://localhost:8000/account/profile?note=seed` in your proxied
   browser (you'll get *"Please log in first"* / 401 — that proves the page is
   login-only, and it now appears in the **Sites** tree).
2. In the **Sites** tree, right-click `http://localhost:8000` → **Include in
   Context → New Context**, name it `Globomantics`.
3. In the Context dialog → **Authentication** → **Script-based Authentication** →
   select `globomantics-auth`; set **Login URL** to
   `http://localhost:8000/login` and **Logged-in indicator (regex)** to
   `Signed in as`.
4. **Users → Add**: name `alice`, username `alice`. Then click **Forced User
   Mode** on the toolbar and select `alice`.
5. Right-click `…/account/profile?note=seed` → **Attack → Active Scan → Start**.

💻 **In your terminal** (reproduces the same context script-auth + forced user and
verifies ZAP logs itself in):
```bash
./scripts/demo_step.sh 3
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: ZAP runs your authentication script
  ★ Without login: /account/profile -> HTTP 401  (gated)
  ★ ZAP forced-user (script auth): /account/profile -> HTTP 200  (reachable)
  ★ Auth script ran: authenticate: user=alice login_url=http://app:8000/login  authenticate: response=200
✔ PASS  ZAP executed the authentication script and holds the session (no cookie supplied by the preflight)
```

**What to highlight:** the same page is **401 before** and **200 after** — and the
`authenticate:` trace proves ZAP got there by **running your script**, with no
cookie supplied by hand.

**Proof artifact:** *Authenticated custom-scan result.*

---

## Step 4 — Confirm the custom alert, fresh from this scan

**Why you run this / what you learn:** a rule you can trust ends in a clear,
named alert. The check clears the alert store first, so the alert you see is
provably from **this** scan — not a leftover from an earlier run.

**Do this:**

🖱️ **In ZAP:** open the **Alerts** tab and find the alert your rule raised on
`/account/profile`.

💻 **In your terminal** (clears the store, scans the page as `alice`, then reads
the alert back):
```bash
./scripts/demo_step.sh 4
```

✅ **You'll see** (output — read it, don't type it):
```text
WHAT: The custom alert the rule raises
  ★ Before scan (store cleared): absent
  ★ Scan target: http://app:8000/account/profile?note=seed (param: note, as user alice)
  ★ Probe requests the scan sent: 135
  ★ Alert: Globomantics unsafe reflection (custom rule)
  ★ Risk: Medium
  ★ Parameter: note
  ★ Evidence: GLOBOxss7marker
✔ PASS  the custom rule RAISED its named alert on this scan — absent before, present after (verified via the ZAP API)
```

**What to highlight:** **absent before, present after** — the named alert, on
parameter `note`, with evidence `GLOBOxss7marker`, raised by *your* rule on a
scan ZAP authenticated itself. That alert is what a pipeline can later gate on.

**Proof artifact:** *Custom alert record.*

---

## Check your work

You authored the scripts in the GUI. To prove both behave correctly in one pass,
run the checker — it loads both scripts through the ZAP API, has ZAP log in with
your auth script, scans the authenticated page with your rule, and confirms a
fresh alert, writing a reviewable log to `logs/`:

```bash
./scripts/preflight_check.sh
```

Each step reports **PASS**, ending with `5 checks passed, 0 failed`. (On a
failure it prints the exact reason and how to fix it.) When you are finished:

```bash
./scripts/demo_down.sh
```

---

## The scripts

**Custom active-scan rule — `globomantics-active-rule.py`** (Jython 2.7.2). It
checks each query parameter by cloning the request (keeping the logged-in
session), putting a probe in the parameter, and raising the named alert if the
probe reflects unencoded. It runs from `scanNode()` so it does not depend on how
ZAP enumerates parameters:

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

> The source files in `zap-scripts/` also write a short diagnostic trace that the
> checker reads to prove exactly what ran; it has no effect on screen.
