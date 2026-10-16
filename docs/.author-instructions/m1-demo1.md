# M1-DEMO1 · Injection, XSS and CSRF — Author Production Playbook

<div align="center">

![Recorder](https://img.shields.io/badge/Recorder-Exact_Screen-0284c7?style=for-the-badge)
![Narrator](https://img.shields.io/badge/Narrator-Verified_Script-9333ea?style=for-the-badge)
![Editor](https://img.shields.io/badge/Editor-Timed_Highlights-16a34a?style=for-the-badge)

<img src="../learner-diagrams/m1-demo1-architecture.svg" alt="Illustrative Injection, XSS and CSRF workflow" width="100%"/>

<sub>Generated using ChatGPT · Temporary PUBLIC author guidance</sub>

</div>

[← **All Six Production Playbooks**](README.md) · [**Student Starter README ↗**](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo1-before/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf/README.md) · [**Completed README ↗**](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo1-after/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf/README.md)

## Recording Assignment

<table>
<tr><th>Field</th><th>Exact Value</th></tr>
<tr><td>Demonstration</td><td><b>Injection, XSS and CSRF</b> · m1-demo1</td></tr>
<tr><td>Approved Objectives</td><td>EO1a · EO1b · EO1c — check the complete wording in the linked learner README</td></tr>
<tr><td>Reference branch</td><td><code>m1-demo1-after</code> — completed source for preflight</td></tr>
<tr><td>Recording branch</td><td><code>m1-demo1-before</code> — follow the student workflow</td></tr>
<tr><td>Demo directory</td><td><code>demos/module1-demos/m1-demo1-targeted-injection-xss-csrf</code></td></tr>
<tr><td>Student exercise state</td><td>Run-only; no completed script is missing from the starter</td></tr>
</table>

## Start Here — One Clone, Two Branches, One Demo

**Do not clone this repository separately for every demo.** Each recorder clones the course once, then switches to the specific demo's `after` branch for preflight and `before` branch for recording. Before switching, stop the old demo environment and preserve the narration references.

<details open>
<summary><b><font color="#0284c7">A · Clone Once and Prepare the Mac</font></b></summary>

Use this step only for your first assigned demo. For second and third demos, keep the same repository folder and skip the clone/setup if already complete.

```bash
cd ~
git clone https://github.com/rupeshtiwari/pluralsight-script-development-with-zap.git
cd pluralsight-script-development-with-zap
./setup/setup-macos.sh
git fetch origin
```

**Where is the folder?** It is `~/pluralsight-script-development-with-zap` by default. `git switch` does not create a second or third folder; it changes the checked-out branch in the same directory.

</details>

<details open>
<summary><b><font color="#9333ea">B · Run Preflight From the Completed Branch FIRST</font></b></summary>

This is the **narration evidence source**. It executes all four real named commands, saves raw live proof, and produces stable per-step reference logs so the Narrator can start while footage is still being recorded.

```bash
cd ~/pluralsight-script-development-with-zap
git status --short
git fetch origin
git switch m1-demo1-after
git rev-parse HEAD
cd demos/module1-demos/m1-demo1-targeted-injection-xss-csrf
./scripts/demo_reset.sh
./scripts/preflight_check.sh
ls -l logs/preflight-step-0[1-4].log
```

**Only proceed when preflight exits 0 and prints the actual summary below** (this is the expected format, not a fabricated test run):

```text
RESULT: 5 checks passed, 0 failed
REFERENCE: logs/preflight-step-01.log through logs/preflight-step-04.log
```

**Proof stays real:** `logs/preflight-step-01.log` through `04.log` are the Narrator's four outputs. `logs/.producer/` holds untouched raw details. Separate ZAP GUI / GitHub Actions evidence must be checked independently when a terminal command cannot observe it.

**Optional but strongly recommended repeatability check:** after successful preflight, set `DEMO_SYNC_MODE=1` and `DEMO_SYNC_PHASE=compare` off-camera, then execute the same four named steps while still on this completed reference. Each must match its baseline; a material mismatch blocks recording.

**Archive the references and stop the stack before switching:**

```bash
mkdir -p ~/zap-production-evidence/m1-demo1
cp logs/preflight-step-0[1-4].log ~/zap-production-evidence/m1-demo1/
./scripts/demo_down.sh
cd ~/pluralsight-script-development-with-zap
git status --short
```

Never delete the reference logs with a destructive Git cleanup.

</details>

<details open>
<summary><b><font color="#0284c7">C · Switch to the Student Starting Branch and Record</font></b></summary>

```bash
cd ~/pluralsight-script-development-with-zap
git switch m1-demo1-before
git rev-parse HEAD
cd demos/module1-demos/m1-demo1-targeted-injection-xss-csrf
cp ~/zap-production-evidence/m1-demo1/preflight-step-0[1-4].log logs/
./scripts/demo_reset.sh

# Off-camera recording parity settings
export DEMO_SYNC_MODE=1
export DEMO_SYNC_PHASE=compare
```

**Run-only; no completed script is missing from the starter.** Follow the [student README on this exact starter branch](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/blob/m1-demo1-before/demos/module1-demos/m1-demo1-targeted-injection-xss-csrf/README.md) to complete any required source writing, then record the four exact commands listed below. The starter branch may be intentionally incomplete and **must not** be expected to pass its final checks before the work has been done.

After the four named commands, capture the GUI/CI proof, then:

```bash
./scripts/demo_down.sh
cd ~/pluralsight-script-development-with-zap
git status --short
```

**If Git refuses the next branch switch:** preserve the changed code on a task branch or in a deliberate backup before switching. Do not use force/reset to discard recorded work.

</details>

<details><summary><b><font color="#16a34a">D · Recording More Demos From This Same Clone</font></b></summary>

```bash
cd ~/pluralsight-script-development-with-zap
git status --short
git fetch origin
# Example: select another assigned demo (replace as needed):
git switch m1-demo2-after
```

For a different demo, replace the branch and folder with the corresponding entry on the [six-demo author dashboard](README.md). Repeat preflight → archive logs → cleanup → branch switch → record. One local repository is sufficient for sequential recordings. A separate worktree is optional when you need two branches open concurrently.

</details>

## Camera, Narration and Edit Contract

<table>
<tr><td width="18%"><img src="https://img.shields.io/badge/RECORDER-Blue-0284c7"/></td><td>Record full-screen at readable zoom. Open the source/GUI pane specified in the relevant step, then hold the complete named command ~8 seconds before Enter. Hold each actual output focus 6–8 seconds. On significant UI clicks provide 8-second pre-click and post-click handles in raw footage for the editor.</td></tr>
<tr><td><img src="https://img.shields.io/badge/NARRATOR-Purple-9333ea"/></td><td>Use the real `preflight-step-0N.log` plus the corresponding filmed GUI/CI evidence. The step tables below give exact ElevenLabs lines with word counts, one mechanism and one operator consequence per reveal. Do not narrate sample placeholders.</td></tr>
<tr><td><img src="https://img.shields.io/badge/EDITOR-Green-16a34a"/></td><td>Cut cleanly at source/terminal/GUI transitions and scanning waits. Highlight one field using a small square, arrow or callout; remove it immediately as the focus changes. Match voice to the same take, not a historic preflight value from a different implementation.</td></tr>
</table>

## Four Fixed Teaching Steps — Follow In Order

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
