# Validate injection, XSS, and CSRF with ZAP

Turn a broad ZAP scan into four validated findings against the deliberately
vulnerable Globomantics Store, confirming each against the application's actual
behavior.

> **Authorization and scope.** Every request targets only the local Globomantics
> Store. Never run these techniques against systems you are not authorized to test.

## Applications and locations used

| Application | Where | Used for |
|-------------|-------|----------|
| macOS Terminal | working directory `module1/m1-c3` | running each `./scripts/demo_step.sh N` |
| ZAP GUI (Webswing) | `http://localhost:8080/zap/` → **Alerts** tab | showing the raised alerts and the reflected-XSS request/response |
| Local Globomantics app | `http://localhost:8000/` | the target under test |

The Terminal commands drive the same ZAP instance the GUI shows (one container,
API on `:8090`, GUI on `:8080`), so alerts raised by a step appear in the Alerts
tab. This clip needs no code editor.

## Setup

Install once from the repository root (wait for the readiness table):

```bash
./env-setup/setup-macos.sh
```

Then navigate to this clip's directory from the repository root:

```bash
cd module1/m1-c3
```

Start the vulnerable build and wait for the healthy `Up` output:

```bash
./scripts/demo_reset.sh
```

**Run each command below from `module1/m1-c3`.** Copy one command block at a time into Terminal, wait for its output, and then inspect the specified GUI view when applicable.

Open `http://localhost:8080/zap/` for the Alerts tab. Exact alert IDs, risk, and
confidence are the live values from your run.

## Learning-objective coverage

| Step | Objective | Proof artifact |
|------|-----------|----------------|
| 1 | EO1a | Targeted scan policy and rule list |
| 2 | EO1b | XSS request and response body |
| 3 | EO1c | CSRF token replay result |
| 4 | EO1a · EO1b · EO1c | Alert disposition record |

## Step 1: Run one targeted injection scan (EO1a)

Goal: Prove that a single focused scan policy confirms SQL, NoSQL, and command
injection from the application's own responses, instead of a broad, unfiltered
alert list.

Application: macOS Terminal, then ZAP GUI.
Open / Navigate: Terminal in `module1/m1-c3`. Then switch to the ZAP GUI
(`http://localhost:8080/zap/`) → **Alerts** tab.
Execute in Terminal:

```bash
./scripts/demo_step.sh 1
```

Then in the ZAP Alerts tab expand the three injection alerts.

Expected output: three injection alerts, one per endpoint — SQL injection (alert
40018) on `/search` `q`, MongoDB NoSQL injection (alert 40033) on `/api/account`
`username`, and command injection (alert 90020) on `/admin/ping` `host`.

What the learner should notice: each endpoint raises a distinct rule tied to a
specific parameter, so one focused policy exercises three injection classes — the
targeted scan, not the default rule set.

Proof artifact: Targeted scan policy and rule list.

## Step 2: Confirm reflected XSS in its output context (EO1b)

Goal: Show the `name` parameter reflected into three output contexts, then let
ZAP's active scanner confirm an exploitable reflected XSS with a context-specific
payload — not merely that input appears in the page.

Application: macOS Terminal, then ZAP GUI.
Open / Navigate: Terminal in `module1/m1-c3`. Then switch to the ZAP GUI → **Alerts**
tab → the **Cross Site Scripting (Reflected)** alert; the lower pane shows its
Request and Response.
Execute in Terminal:

```bash
./scripts/demo_step.sh 2
```

Then select that alert in the ZAP Alerts tab.

Expected output: the `name` value reflected in the HTML body, an HTML attribute,
and a JavaScript string; then ZAP's **Cross Site Scripting (Reflected)** alert on
parameter `name`, with the injected payload `</p><scrIpt>alert(1);</scRipt><p>`
reflected verbatim in the response as the supporting evidence.

What the learner should notice: the context mapping decides where a payload must
break out; ZAP's alert is what confirms the reflection is executable. The payload
closes the `<p>` element and injects a script tag, returned unescaped — reflection
alone is not that proof.

Proof artifact: XSS request and response body.

## Step 3: Reuse a CSRF token across sessions (EO1c)

Goal: Demonstrate that the anti-CSRF token is not bound to its session, so a token
issued to one session is accepted with a second session's cookie and changes that
session's state.

Application: macOS Terminal (this step is terminal-driven; no GUI needed).
Open / Navigate: Terminal in `module1/m1-c3`.
Execute in Terminal:

```bash
./scripts/demo_step.sh 3
```

Expected output: the valid control (session B's own token) returns 200; the
missing-token control returns 403; and session A's token submitted with session B's
cookie returns 200, changing session B's stored email from
`alice@globomantics.example` to `attacker@evil.example`.

What the learner should notice: the controls show the token check is active, yet the
cross-session request still succeeds and mutates state. The flaw is that the server
validates the token's existence but not that it belongs to the submitting session.
This is token reuse across sessions; rejecting same-session reuse matters only when
the application requires single-use tokens.

Proof artifact: CSRF token replay result.

## Step 4: Record an alert disposition (EO1a · EO1b · EO1c)

Goal: Reconcile each finding with concrete application behavior and record it as
confirmed — the decision a validated scan produces.

Application: macOS Terminal (record into the disposition template with any editor).
Open / Navigate: Terminal in `module1/m1-c3`; the record template is
`docs/alert-disposition-template.md`.
Execute in Terminal:

```bash
./scripts/demo_step.sh 4
```

Expected output: each finding confirmed against live behavior — the SQL error
("unterminated quoted string"), the NoSQL account count rising from 1 to 4 under
operator injection, the command-injection ping output ("bytes from 127.0.0.1"),
and the unescaped XSS reflection.

What the learner should notice: every alert is tied to an observed application
behavior, turning raw scanner output into a defensible disposition recorded in
[`docs/alert-disposition-template.md`](../../docs/alert-disposition-template.md).

Proof artifact: Alert disposition record.

## Validate and reset

To validate all four steps and save a reviewable log in `logs/`, run:

```bash
./scripts/preflight_check.sh
```

Expected final line: `5 checks passed, 0 failed`.

After recording, stop the local demo stack with:

```bash
./scripts/demo_down.sh
```

Optional: `./scripts/show_code.sh {sqli|nosql|cmd|xss|csrf}` prints the exact
vulnerable line(s) from `app/main.py`. The remediated build
(`APP_BUILD=remediated docker compose up -d --build app`) removes the injection
alerts, encodes the XSS output (no reflected-XSS alert), and rejects the
cross-session CSRF request with `403`.
