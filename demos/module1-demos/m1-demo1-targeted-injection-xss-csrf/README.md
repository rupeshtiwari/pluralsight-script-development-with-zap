# Module 1 · Demo 1 — Validate injection, XSS and CSRF

<div align="center">

![Training](https://img.shields.io/badge/Globomantics-Authorized_Lab-130F25?style=for-the-badge)
![ZAP](https://img.shields.io/badge/OWASP_ZAP-Targeted_Scanning-FF1675?style=for-the-badge)

<img width="100%" src="../../../docs/learner-diagrams/m1-demo1-architecture.svg" alt="Module 1 · Demo 1 — Validate injection, XSS and CSRF security architecture"/>

<sub>Illustrative architecture · Generated using ChatGPT; only live requests and reports prove findings</sub>

</div>

<!-- demo-navigation:start -->
<p align="center"><b>Student exercise · Demo 1 of 6</b></p>
<p align="center">
  <a href="../../../README.md"><img alt="All student demos" src="https://img.shields.io/badge/%E2%86%90_Back_to-All_Demos-585FA2?style=for-the-badge"></a>
  <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo2-before/demos/module1-demos/m1-demo2-javascript-http-sender/README.md"><img alt="Next student demo: Module 1 Demo 2 — JavaScript HTTP Sender" src="https://img.shields.io/badge/Next_%E2%86%92-M1_Demo_2-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->

## The problem you are solving

Maya is securing the Globomantics Store. A generic scan lists possible security issues but does not tell her which application input is unsafe, whether a reflection creates exploitable cross-site scripting, or whether a token belongs to its session. She needs a defensible finding with the request, response, and application behavior behind it.

**What success looks like:** A focused injection scan, context-specific XSS evidence, a cross-session CSRF check, and a final alert disposition. The four steps solve different parts of one problem. Read them in order: each adds evidence needed for the final decision.

## What you will learn in this demonstration

You will follow a single investigation from selecting focused scan rules through checking actual application responses:

- Find where SQL, MongoDB and operating-system command inputs cross unsafe boundaries *(EO1a)*
- Validate reflected XSS using the output context and ZAP's injected request *(EO1b)*
- Test whether CSRF tokens protect the intended authenticated session *(EO1c)*

No separate course outline is required to complete this lab.

## Follow the evidence

```mermaid
flowchart LR
  S1["Three injection targets"]
  S2["XSS output contexts"]
  S3["CSRF across sessions"]
  S4["Evidence-based disposition"]
  S1 --> S2
  S2 --> S3
  S3 --> S4
```

## Start the local demo

This step starts the actual vulnerable Globomantics web application and ZAP container. The Mac prerequisite installer, `setup/setup-macos.sh`, is a **one-time preparation task** explained in the [course README](../../../README.md). You do not need to reinstall tools for every demo.

<details open>
<summary><b>Start Module 1 Demo 1 — exact branch, folder and runtime</b></summary>

**Where:** macOS Terminal or the VS Code integrated terminal, starting in the root of your existing local repository.

```bash
git fetch origin
git switch m1-demo1-before
cd demos/module1-demos/m1-demo1-targeted-injection-xss-csrf
./scripts/demo_reset.sh
```

**Expected startup:** the script waits for the local services. For a reset it prints a clean-slate message and brings up the vulnerable build. Continue only after it reports readiness; a failed startup is not part of the four teaching steps.

**Open these actual interfaces:** [Globomantics app — localhost:8000](http://localhost:8000/) · [ZAP GUI — localhost:8080/zap/](http://localhost:8080/zap/) · [ZAP API/proxy — localhost:8090](http://localhost:8090/). Open only the interface called for by the current step. Use VS Code with the source editor and integrated terminal for this lab. The script prints the real ZAP findings in the terminal.

</details>

## The four teaching steps

<details open>
<summary><b>Step 1: Run one targeted injection scan</b> — Three injection targets</summary>

### The small problem to solve

The search, account and administrative endpoints reach three different execution boundaries; a generic alert total hides those differences.

**Learning focus:** Configure specialized SQL, NoSQL and command-injection checks *(EO1a)*

### Where to go

**Open VS Code.** Use File → Open Folder to open the repository. In the editor open `runtime/app/main.py`. In the integrated Terminal, inspect the three prepared views by running `./scripts/show_code.sh sqli`, `./scripts/show_code.sh nosql` and `./scripts/show_code.sh cmd`. Keep source functions `search`, `account` and `admin_ping` accessible.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`.

```bash
./steps/01-run-targeted-injection-scan.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Policy rules enabled</b></td><td><code>SQL-injection family + NoSQL 40033 + command 90020/90037</code></td><td>Confirm the policy is focused</td></tr>
<tr><td><b>SQL injection · /search (q)</b></td><td><code>alert 40018 or 40022 · &lt;live risk&gt;/&lt;live confidence&gt;</code></td><td>Correlate the SQL alert with q</td></tr>
<tr><td><b>NoSQL injection · /api/account (username)</b></td><td><code>alert 40033 · &lt;live risk&gt;/&lt;live confidence&gt;</code></td><td>Correlate NoSQL with username</td></tr>
<tr><td><b>Command injection · /admin/ping (host)</b></td><td><code>alert 90020 or 90037 · &lt;live risk&gt;/&lt;live confidence&gt;</code></td><td>Correlate OS command with host</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS targeted scan raised all three injection alerts</code></td><td>Only pass with three actual findings</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

Three different request parameters are now associated with targeted ZAP findings. The risk/confidence fields report the current engine's result; the mere presence of an alert is not yet a defensible confirmation of all three defects.

**How this connects:** Now validate the page-output context rather than treating every reflected input as XSS.

</details>

<details>
<summary><b>Step 2: Validate reflected XSS in the correct context</b> — XSS output contexts</summary>

### The small problem to solve

The `name` input appears in an HTML element, an attribute and a JavaScript string. The right test changes with the output context.

**Learning focus:** Test context-specific reflected XSS *(EO1b)*

### Where to go

**Remain in VS Code.** Open `runtime/app/main.py` at the `greet` endpoint (approximately lines 257–277). In its integrated Terminal run `./scripts/show_code.sh xss` to see the source fragment.

### Run this exact command

**Where to type it:** the same VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`.

```bash
./steps/02-verify-reflected-xss-contexts.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>HTML body</b></td><td><code>&lt;p&gt;Hello zzMARKzz</code></td><td>Inspect the body sink</td></tr>
<tr><td><b>HTML attribute</b></td><td><code>value="zzMARKzz"</code></td><td>Inspect the quoted attribute sink</td></tr>
<tr><td><b>JavaScript string</b></td><td><code>var greeting = "zzMARKzz"</code></td><td>Inspect the JavaScript string sink</td></tr>
<tr><td><b>Alert</b></td><td><code>Cross Site Scripting (Reflected)</code></td><td>Look for the named ZAP alert</td></tr>
<tr><td><b>Affected parameter</b></td><td><code>name</code></td><td>Confirm the input</td></tr>
<tr><td><b>Payload ZAP injected</b></td><td><code>&lt;actual injected payload&gt;</code></td><td>Use the real payload from this run</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS ZAP confirmed reflected XSS on name</code></td><td>A real payload and reflected evidence are required</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

The first three lines map the input to three output contexts. ZAP then attempts a context-specific payload and reports the affected parameter and evidence; raw reflection alone is not proof of executable script in a browser.

**How this connects:** Next, move from output encoding to a state-changing request that depends on CSRF session ownership.

</details>

<details>
<summary><b>Step 3: Replay a CSRF token across two sessions</b> — CSRF across sessions</summary>

### The small problem to solve

A token check can exist yet fail if the server accepts a token from one person's session with another person's cookie.

**Learning focus:** Exercise CSRF bypass conditions in the email-change workflow *(EO1c)*

### Where to go

**Remain in VS Code.** Open `runtime/app/main.py` at `change_email` and the token-issuing helper. In the integrated Terminal run `./scripts/show_code.sh csrf` before running the security step.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`.

```bash
./steps/03-test-cross-session-csrf-token.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>Valid token, session B</b></td><td><code>200</code></td><td>Legitimate control accepted</td></tr>
<tr><td><b>Missing token</b></td><td><code>403</code></td><td>Missing-token control rejected</td></tr>
<tr><td><b>Before cross-session request</b></td><td><code>alice@globomantics.example</code></td><td>Check actual stored state</td></tr>
<tr><td><b>Session A token with B cookie</b></td><td><code>200 (should be rejected)</code></td><td>Spot the cross-session bypass</td></tr>
<tr><td><b>After cross-session request</b></td><td><code>attacker@evil.example</code></td><td>State actually changed</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS token was accepted across sessions</code></td><td>Proof requires status AND changed email</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

Controls show the application is checking for a token. The cross-session request nevertheless succeeds and changes the victim's stored email, showing the token is not adequately associated with its issuing session.

**How this connects:** The final step reconciles these observations with the alerts and records an actionable disposition.

</details>

<details>
<summary><b>Step 4: Reconcile the findings with application behavior</b> — Evidence-based disposition</summary>

### The small problem to solve

The team must not ship an alert list that lacks reproducible evidence for each stated vulnerability.

**Learning focus:** Apply the three security checks to a final engineering disposition *(EO1a · EO1b · EO1c)*

### Where to go

**Use VS Code with integrated Terminal.** Keep `runtime/app/main.py` open. Read the student disposition template at `docs/alert-disposition-template.md` from the repository root. Return to the demo Terminal before running the step.

### Run this exact command

**Where to type it:** the VS Code integrated Terminal, while your current directory is `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`.

```bash
./steps/04-reconcile-security-alerts.sh
```

### What the script prints

The table shows the actual **field names and expected type of evidence** produced by the existing script. These are examples, **not results claimed from your computer**. Rule IDs and stable parameter names come from the demo; variable risk, request IDs and counters must be read from your live output.

<table>
<thead><tr><th>Displayed field</th><th>Example or expected value</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>SQL injection 40018 · /search</b></td><td><code>confirmed — DB error: &lt;actual SQL error&gt;</code></td><td>Request/response supports SQL issue</td></tr>
<tr><td><b>NoSQL injection 40033 · /api/account</b></td><td><code>confirmed — accounts &lt;before&gt; → &lt;after&gt;</code></td><td>Operator injection affects record count</td></tr>
<tr><td><b>Command injection 90020/90037 · /admin/ping</b></td><td><code>confirmed — OS command ran: &lt;actual bytes&gt;</code></td><td>Also inspect the injected host request; a normal ping is insufficient</td></tr>
<tr><td><b>XSS reflected · /greet</b></td><td><code>confirmed — unencoded reflection</code></td><td>Confirm actual injected payload and response evidence</td></tr>
<tr><td><b>Result</b></td><td><code>✔ PASS all four findings reconciled with app behavior</code></td><td>Check the evidence before disposition</td></tr>
</tbody></table>

**Do not continue on FAIL.** Read the command's diagnostic text and verify the right branch, app state, and script source instead of claiming an alert appeared.

### What you should understand

A raw rule ID is a lead; its actual request and application effect support the engineer's final decision. Do not use routine ping output alone as proof of shell-command injection.

**How this connects:** The investigation closes with documented findings that can be reviewed rather than mere scanner severity labels.

</details>

## Finish and clean up

After Step 4, you should be able to explain why a rule or alert deserves a confirmed disposition from real evidence rather than only recalling a command.

**Stop the demo's containers** from the same demo directory:

```bash
./scripts/demo_down.sh
```

To inspect the finished example, switch to `m1-demo1-after` **after preserving any exercise changes**. Compare without modifying files using `git diff m1-demo1-before..m1-demo1-after -- demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`. For operational-only demos, the important difference may be live scan evidence rather than source code.

**Course-wide validation:** The Developer can run `./setup/run-all-demo-preflights.sh` **once from the repository root** to validate all six completed demo branches and produce real evidence bundles. It is not another script to run after each step.

<!-- demo-navigation:start -->
<p align="center"><b>Student exercise · Demo 1 of 6</b></p>
<p align="center">
  <a href="../../../README.md"><img alt="All student demos" src="https://img.shields.io/badge/%E2%86%90_Back_to-All_Demos-585FA2?style=for-the-badge"></a>
  <a href="https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo2-before/demos/module1-demos/m1-demo2-javascript-http-sender/README.md"><img alt="Next student demo: Module 1 Demo 2 — JavaScript HTTP Sender" src="https://img.shields.io/badge/Next_%E2%86%92-M1_Demo_2-FF1675?style=for-the-badge"></a>
</p>
<!-- demo-navigation:end -->

[← Module 1 demo catalog](../README.md) · [← Course home](../../../README.md)

