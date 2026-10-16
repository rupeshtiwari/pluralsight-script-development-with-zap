# M1-DEMO1 · Injection, XSS and CSRF — Production Playbook

<div align="center">

![Recorder](https://img.shields.io/badge/RECORDER-Precise_Screens-0284c7?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-ElevenLabs-d946ef?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-One_Focus-16a34a?style=for-the-badge)

<img src="../learner-diagrams/m1-demo1-architecture.svg" width="100%" alt="Globomantics Injection, XSS and CSRF architecture"/>

<sub>Illustrative diagram · Generated using ChatGPT · Production instructions are temporarily public here</sub>

</div>

## Why This Demonstration Exists

Maya must decide which Globomantics security findings are real and how the observed requests support each disposition. The target is the authorized local training application.

**Approved objective(s):** EO1a — targeted SQL, NoSQL and command injection; EO1b — context-specific reflected XSS; EO1c — CSRF token bypass and session-binding checks

**Audience:** Developers and security testers learning to make operator decisions through real HTTP evidence.

## Start Here — Preflight Before Narration Or Recording

The **completed** branch is the authoritative source for a successful preflight. A starter branch intentionally lacks authored assets where that exercise requires them. The narrator can work in parallel, while the recorder later completes the starter exercise to the same final source state.

```bash
git clone -b m1-demo1-after https://github.com/rupeshtiwari/pluralsight-script-development-with-zap.git ~/zap-producer-m1-demo1-reference
cd ~/zap-producer-m1-demo1-reference
./setup/setup-macos.sh
cd demos/module1-demos/m1-demo1-targeted-injection-xss-csrf
./scripts/demo_reset.sh
./scripts/preflight_check.sh
ls logs/preflight-step-0[1-4].log
```

The preflight **actually executes all four named step scripts** using the same step engine the Recorder will run. It saves the combined timestamped log, four per-step narration baselines, and unchanged raw proof under `logs/.producer/`. Expect **5 checks passed, 0 failed** only after all four return PASS. Run `./scripts/demo_down.sh` after evidence capture.

**Recorder's independent starting branch:** `m1-demo1-before` — [open the correct GitHub branch](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/tree/m1-demo1-before/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf). Clone that branch into a *separate* directory, prepare the required code or configuration to match the approved finished state, and transfer the four `preflight-step-0N.log` reference files into its demo `logs/` directory. **Do not execute the starter branch preflight before authoring its missing solution.** Keep recording and reference environments separate; do not run both Docker stacks at once on the same ports.

Before filming, in the Recorder's terminal **off-camera**:

```bash
export DEMO_SYNC_MODE=1
export DEMO_SYNC_PHASE=compare
```

Now each named step executes live, retains the unaltered raw proof, displays a normalized stable transcript, and **exits nonzero on a material mismatch** against its preflight reference. A different request ID or scan count can be normalized; the actual values remain in raw logs. **Risk, parameter, alert identity, HTTP status and gate decisions must not be fabricated or normalized away.** The matching visible transcript, not two unrelated raw runs, is the narration synchronization contract.

**Primary recording UI:** VS Code integrated terminal; source runtime/app/main.py; optional ZAP GUI at http://localhost:8080/zap/. Full-screen capture, readable text on a phone, no browser tabs. Editing handles: hold command **8 seconds before Enter**; show each meaningful proof region **6–8 seconds**, never exceed **10 seconds of idle final footage**. For important GUI clicks provide roughly **8 seconds before** and **8 seconds after** in the raw take; trim for the final video. Do not linger through scanner waits; make a clean edit.

## Four Fixed Teaching Steps

## Step 1: Prove Three Injection Classes With One Focused Policy

**LO:** EO1a · **Operator problem:** A full scan produces noise; this focuses the rule set on three separate unsafe input boundaries.

**What the script does:** Run the same first validated part of the source step engine; inspect the exact parameters in the source pane below. The command name tells learners what they are testing.

```bash
./steps/01-run-targeted-injection-scan.sh
```

**Expected terminal fields, based on the actual `_steps.sh` output (illustrative, NOT a captured runtime log):**

```text
Policy rules enabled: SQL-injection family + NoSQL 40033 + command 90020/90037
SQL injection · /search (q): alert 40018 · <actual risk>/<actual confidence>
NoSQL injection · /api/account (username): alert 40033 · <actual risk>/<actual confidence>
Command injection · /admin/ping (host): alert 90020 or 90037 · <actual risk>/<actual confidence>
✔ PASS targeted scan raised all three injection alerts
```

Replace variable markers with the **real preflight-step-01.log** and filmed-take evidence. Never narrate placeholders as observed results.

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/> Exact Screen And Timing</summary>
<table>
<tr><th>Relative Footage</th><th>Required Screen / Action</th></tr>
<tr><td>Source context · 00:00–00:08</td><td>VS Code: Cmd+P → runtime/app/main.py. Show search() near line 149, account() near line 196, and admin_ping() near line 227. In the terminal use ./scripts/show_code.sh sqli, nosql and cmd to show exact sink lines.</td></tr>
<tr><td>Command · next 8 seconds</td><td>Show the full command above from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf` at readable zoom, keep the pointer away from key text and press Enter once.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Highlight the policy-rule line, then SQL injection alert and q parameter.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Highlight 40033 with username, then 90020 or 90037 with host. Do not claim normal ping output proves injection.</td></tr>
<tr><td>Completion · 6–8 seconds</td><td>Hold the actual PASS line or stop on FAIL. Capture the exact console output and screen/take timestamp. Do not leave any single proof frame static more than 10 seconds.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-Purple-d946ef"/> Exact ElevenLabs Narration</summary>
<table><tr><th>Visual Reveal</th><th>Spoken Words — Copy Exactly After Verifying Proof</th><th>Count</th></tr>
<tr><td>00:00–00:08 · command</td><td>Run this focused ZAP policy against the store’s search, account, and administrative endpoints. Each input reaches a different vulnerable boundary.</td><td>20 spoken words</td></tr>
<tr><td>After execution · proof A</td><td>The SQL rule reports the search parameter q. The MongoDB rule checks username, so these findings describe different application behavior.</td><td>20 spoken words</td></tr>
<tr><td>After execution · proof B</td><td>The command rule targets host. Three parameter-specific alerts establish where to investigate; the real requests and responses determine disposition.</td><td>19 spoken words</td></tr>
</table>
The lines are spoken sentences, not production notes. The second and third lines are recorded only if the named evidence is actually visible. If observed values change, revalidate the claims against the filmed take rather than adding invented numbers.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/> Callouts, Cuts And Sync</summary>
<table><tr><th>Edit Point</th><th>Exact Action</th></tr>
<tr><td>Command entrance</td><td>Clean cut after source context; frame the entire named command with a subtle square or underline for ≤8 seconds. Narration line 1 accompanies this command.</td></tr>
<tr><td>First output</td><td>Use one square callout around the policy-rule line, then separate arrows to q, username and host with their actual alert IDs. One focus per eight-second proof window. Attach narration line 2 when the proof is fully displayed.</td></tr>
<tr><td>Decision / completion</td><td>Attach narration line 3 to the proof B or verified PASS frame; remove previous arrows immediately on screen or pane changes. Trim UI click handles and scanning waits.</td></tr>
<tr><td>Synchronization</td><td>Use `logs/preflight-step-01.log`, `logs/recorded-step-01.log`, raw proof, the actual take ID and editor timecodes. A normalized mismatch is a retake, not an edit-away problem.</td></tr>
</table>
</details>

**Source-review confidence: 94%.** This is not a claimed runtime pass; a completed same-evidence take and correct technical proof determine final release.

---

## Step 2: Match The Payload To The Output Context

**LO:** EO1b · **Operator problem:** A reflected string is not necessarily exploitable. HTML body, attribute and JavaScript string contexts need different breakouts.

**What the script does:** Run the same second validated part of the source step engine; inspect the exact parameters in the source pane below. The command name tells learners what they are testing.

```bash
./steps/02-verify-reflected-xss-contexts.sh
```

**Expected terminal fields, based on the actual `_steps.sh` output (illustrative, NOT a captured runtime log):**

```text
HTML body — use <script>…</script>: <p>Hello zzMARKzz
HTML attribute — break out with ">…: value="zzMARKzz"
JS string — break out with ";…: var greeting = "zzMARKzz"
Alert: Cross Site Scripting (Reflected)
Affected parameter: name
Payload ZAP injected: <actual scanner payload>
Evidence (reflected in the response): <actual text>
✔ PASS ZAP confirmed reflected XSS on name
```

Replace variable markers with the **real preflight-step-02.log** and filmed-take evidence. Never narrate placeholders as observed results.

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/> Exact Screen And Timing</summary>
<table>
<tr><th>Relative Footage</th><th>Required Screen / Action</th></tr>
<tr><td>Source context · 00:00–00:08</td><td>VS Code: Cmd+P → runtime/app/main.py, Cmd+G → 257–277, inspect greet(). Terminal: ./scripts/show_code.sh xss. ZAP's recorded finding is for the name parameter on /greet.</td></tr>
<tr><td>Command · next 8 seconds</td><td>Show the full command above from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf` at readable zoom, keep the pointer away from key text and press Enter once.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Box the three response contexts one at a time and then show the actual affected parameter name.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Put an arrow on the scanner's injected payload and the response evidence. Distinguish detected exploitability from unfilmed browser execution.</td></tr>
<tr><td>Completion · 6–8 seconds</td><td>Hold the actual PASS line or stop on FAIL. Capture the exact console output and screen/take timestamp. Do not leave any single proof frame static more than 10 seconds.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-Purple-d946ef"/> Exact ElevenLabs Narration</summary>
<table><tr><th>Visual Reveal</th><th>Spoken Words — Copy Exactly After Verifying Proof</th><th>Count</th></tr>
<tr><td>00:00–00:08 · command</td><td>The name value appears in HTML, an attribute, and JavaScript. Each context changes the characters an attacker needs to escape.</td><td>20 spoken words</td></tr>
<tr><td>After execution · proof A</td><td>ZAP targets the name parameter using a context-matched payload. Read the actual injected value before judging the result.</td><td>18 spoken words</td></tr>
<tr><td>After execution · proof B</td><td>Now compare that payload with the reflected response evidence. Reflection alone is insufficient; the alert supplies the security finding.</td><td>19 spoken words</td></tr>
</table>
The lines are spoken sentences, not production notes. The second and third lines are recorded only if the named evidence is actually visible. If observed values change, revalidate the claims against the filmed take rather than adding invented numbers.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/> Callouts, Cuts And Sync</summary>
<table><tr><th>Edit Point</th><th>Exact Action</th></tr>
<tr><td>Command entrance</td><td>Clean cut after source context; frame the entire named command with a subtle square or underline for ≤8 seconds. Narration line 1 accompanies this command.</td></tr>
<tr><td>First output</td><td>Three short squares for body, attribute and JavaScript, then cut to a two-column callout over payload and evidence. Never highlight all fields simultaneously. Attach narration line 2 when the proof is fully displayed.</td></tr>
<tr><td>Decision / completion</td><td>Attach narration line 3 to the proof B or verified PASS frame; remove previous arrows immediately on screen or pane changes. Trim UI click handles and scanning waits.</td></tr>
<tr><td>Synchronization</td><td>Use `logs/preflight-step-02.log`, `logs/recorded-step-02.log`, raw proof, the actual take ID and editor timecodes. A normalized mismatch is a retake, not an edit-away problem.</td></tr>
</table>
</details>

**Source-review confidence: 93%.** This is not a claimed runtime pass; a completed same-evidence take and correct technical proof determine final release.

---

## Step 3: Replay A Token Across Session Boundaries

**LO:** EO1c · **Operator problem:** The email-change workflow validates token existence but fails to bind the token to its issuing session.

**What the script does:** Run the same third validated part of the source step engine; inspect the exact parameters in the source pane below. The command name tells learners what they are testing.

```bash
./steps/03-test-cross-session-csrf-token.sh
```

**Expected terminal fields, based on the actual `_steps.sh` output (illustrative, NOT a captured runtime log):**

```text
valid token (session B's own): 200
missing token: 403
session B's email before the cross-session request: alice@globomantics.example
token from session A, submitted with session B's cookie: 200 (should be rejected)
session B's email after the cross-session request: attacker@evil.example
✔ PASS session A's token was accepted with session B's cookie and changed session B's email
```

Replace variable markers with the **real preflight-step-03.log** and filmed-take evidence. Never narrate placeholders as observed results.

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/> Exact Screen And Timing</summary>
<table>
<tr><th>Relative Footage</th><th>Required Screen / Action</th></tr>
<tr><td>Source context · 00:00–00:08</td><td>VS Code: Cmd+P → runtime/app/main.py, Cmd+G → 326–337, show the ownership-check branch. Terminal: ./scripts/show_code.sh csrf.</td></tr>
<tr><td>Command · next 8 seconds</td><td>Show the full command above from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf` at readable zoom, keep the pointer away from key text and press Enter once.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Highlight valid 200 and missing-token 403 as the two controls, one at a time.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Highlight cross-session 200 and the changed email. Keep session labels A and B readable; do not display token secrets.</td></tr>
<tr><td>Completion · 6–8 seconds</td><td>Hold the actual PASS line or stop on FAIL. Capture the exact console output and screen/take timestamp. Do not leave any single proof frame static more than 10 seconds.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-Purple-d946ef"/> Exact ElevenLabs Narration</summary>
<table><tr><th>Visual Reveal</th><th>Spoken Words — Copy Exactly After Verifying Proof</th><th>Count</th></tr>
<tr><td>00:00–00:08 · command</td><td>Alice’s own token succeeds, while the missing-token request is denied. Those two controls establish that token checking is enabled.</td><td>19 spoken words</td></tr>
<tr><td>After execution · proof A</td><td>Next, a token issued to Mallory is submitted with Alice’s session cookie. That request should be rejected, but returns two hundred.</td><td>21 spoken words</td></tr>
<tr><td>After execution · proof B</td><td>Alice’s stored email then changes. The server checked token existence, not session ownership, so the cross-session forgery succeeded.</td><td>18 spoken words</td></tr>
</table>
The lines are spoken sentences, not production notes. The second and third lines are recorded only if the named evidence is actually visible. If observed values change, revalidate the claims against the filmed take rather than adding invented numbers.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/> Callouts, Cuts And Sync</summary>
<table><tr><th>Edit Point</th><th>Exact Action</th></tr>
<tr><td>Command entrance</td><td>Clean cut after source context; frame the entire named command with a subtle square or underline for ≤8 seconds. Narration line 1 accompanies this command.</td></tr>
<tr><td>First output</td><td>Blue rectangles over two control status lines, then one high-contrast rectangle over cross-session 200 and an arrow to the email mutation. Cut before values become stale. Attach narration line 2 when the proof is fully displayed.</td></tr>
<tr><td>Decision / completion</td><td>Attach narration line 3 to the proof B or verified PASS frame; remove previous arrows immediately on screen or pane changes. Trim UI click handles and scanning waits.</td></tr>
<tr><td>Synchronization</td><td>Use `logs/preflight-step-03.log`, `logs/recorded-step-03.log`, raw proof, the actual take ID and editor timecodes. A normalized mismatch is a retake, not an edit-away problem.</td></tr>
</table>
</details>

**Source-review confidence: 96%.** This is not a claimed runtime pass; a completed same-evidence take and correct technical proof determine final release.

---

## Step 4: Turn Scanner Alerts Into Defensible Decisions

**LO:** EO1a · EO1b · EO1c · **Operator problem:** A scanner's severity is only a lead; the engineer needs application-behavior evidence before recording a confirmed finding.

**What the script does:** Run the same final validated part of the source step engine; inspect the exact parameters in the source pane below. The command name tells learners what they are testing.

```bash
./steps/04-reconcile-security-alerts.sh
```

**Expected terminal fields, based on the actual `_steps.sh` output (illustrative, NOT a captured runtime log):**

```text
40018 SQL injection · /search: confirmed — DB error: <live SQL error>
40033 NoSQL injection · /api/account: confirmed — accounts 1 → 4
90020/90037 Command injection · /admin/ping: confirmed — OS command ran: <live ping text>
XSS reflected · /greet: confirmed — reflected unescaped
✔ PASS all four findings reconciled with app behavior and recorded as confirmed
```

Replace variable markers with the **real preflight-step-04.log** and filmed-take evidence. Never narrate placeholders as observed results.

<details open>
<summary><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/> Exact Screen And Timing</summary>
<table>
<tr><th>Relative Footage</th><th>Required Screen / Action</th></tr>
<tr><td>Source context · 00:00–00:08</td><td>VS Code: inspect runtime/app/main.py for search, account, admin_ping and greet. Open docs/alert-disposition-template.md for the student record. Run the named step in integrated terminal.</td></tr>
<tr><td>Command · next 8 seconds</td><td>Show the full command above from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf` at readable zoom, keep the pointer away from key text and press Enter once.</td></tr>
<tr><td>Proof A · 6–8 seconds</td><td>Show SQL parse error and NoSQL count difference; these are independent effects.</td></tr>
<tr><td>Proof B · 6–8 seconds</td><td>Show the XSS reflection and command rule. The script's normal ping evidence is insufficient alone; open the original injected request if narrating command execution.</td></tr>
<tr><td>Completion · 6–8 seconds</td><td>Hold the actual PASS line or stop on FAIL. Capture the exact console output and screen/take timestamp. Do not leave any single proof frame static more than 10 seconds.</td></tr>
</table>
</details>

<details open>
<summary><img src="https://img.shields.io/badge/NARRATOR-Purple-d946ef"/> Exact ElevenLabs Narration</summary>
<table><tr><th>Visual Reveal</th><th>Spoken Words — Copy Exactly After Verifying Proof</th><th>Count</th></tr>
<tr><td>00:00–00:08 · command</td><td>The SQL error and changing MongoDB account count show two different unsafe data paths, beyond merely reading scanner labels.</td><td>19 spoken words</td></tr>
<tr><td>After execution · proof A</td><td>The reflected marker confirms unencoded output. A normal ping does not prove shell injection, so inspect the original injected host request.</td><td>21 spoken words</td></tr>
<tr><td>After execution · proof B</td><td>Record only findings whose observed behavior supports the diagnosis. An alert disposition must be defensible when another engineer reviews it.</td><td>20 spoken words</td></tr>
</table>
The lines are spoken sentences, not production notes. The second and third lines are recorded only if the named evidence is actually visible. If observed values change, revalidate the claims against the filmed take rather than adding invented numbers.
</details>

<details open>
<summary><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/> Callouts, Cuts And Sync</summary>
<table><tr><th>Edit Point</th><th>Exact Action</th></tr>
<tr><td>Command entrance</td><td>Clean cut after source context; frame the entire named command with a subtle square or underline for ≤8 seconds. Narration line 1 accompanies this command.</td></tr>
<tr><td>First output</td><td>Highlight SQL error, MongoDB count, XSS reflection and the injected-command proof in separate eight-second cuts. Never add a simulated shell payload to the screen. Attach narration line 2 when the proof is fully displayed.</td></tr>
<tr><td>Decision / completion</td><td>Attach narration line 3 to the proof B or verified PASS frame; remove previous arrows immediately on screen or pane changes. Trim UI click handles and scanning waits.</td></tr>
<tr><td>Synchronization</td><td>Use `logs/preflight-step-04.log`, `logs/recorded-step-04.log`, raw proof, the actual take ID and editor timecodes. A normalized mismatch is a retake, not an edit-away problem.</td></tr>
</table>
</details>

**Source-review confidence: 88%.** This is not a claimed runtime pass; a completed same-evidence take and correct technical proof determine final release.

---

## Final Handoff

Deliver branch and SHA, preflight full log, four normalized per-step logs, four raw proof logs, GUI/CI evidence index, actual screen take IDs, ElevenLabs audio filenames, Editor cut/timecode sheet, and the CQA pass/fail decision. If any required proof is absent, do not substitute prior-run or expected text. Stop and correct only the failing step.
