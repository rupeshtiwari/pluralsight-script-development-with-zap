# M1-DEMO1 — Injection, XSS and CSRF

**Approved enabling objectives:** EO1a / EO1b / EO1c  
**Scenario / senior operator decision:** Maya must distinguish exploitable application behavior from large, unprioritized scanner alerts in the Globomantics store.  
**Exact demo folder:** `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`  
**Branch pair:** `m1-demo1-before` → `m1-demo1-after`  
**Primary UI:** VS Code source + integrated terminal; ZAP API/proxy localhost:8090  
**Required diagram:** `docs/learner-diagrams/m1-demo1-architecture.svg`

## Preparations and private handoff

1. From repo root, run `./setup/setup-macos.sh` once. Select the assigned demo branch and enter `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`. Start the stack with the setup or reset command shown in this demo's README. Do not execute preceding demos.
2. Run `./scripts/preflight_check.sh` and preserve the actual timestamped `logs/` output. The preflight log is not automatically the same capture as another take.
3. Recorder follows the four commands below in order; records live GUI/CI-only output separately and holds commands and click targets for the specified editing handles.
4. Narrator and Editor use an evidence manifest tied to the same branch SHA, take and output, not hypothetical numbers.

## Step 1: run targeted injection scan — EO1a

**Real-world problem:** A broad scan obscures three distinct injection sinks

**Exact on-screen command** (run from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`):

```bash
./steps/01-run-targeted-injection-scan.sh
```

**Recorder:** Read `runtime/app/main.py` through `./scripts/show_code.sh sqli`, `nosql` and `cmd`, then run the named step. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Focus on rules 40018, 40033 and 90020/90037; `q`, `username[$ne]` and `host` are distinct attack surfaces. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** Actual parameter-specific alerts, including exact live risk and confidence. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Establish that a selected rule set maps directly to separate vulnerable parameters. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 94% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Step 2: verify reflected xss contexts — EO1b

**Real-world problem:** A reflected string is not, by itself, executable XSS

**Exact on-screen command** (run from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`):

```bash
./steps/02-verify-reflected-xss-contexts.sh
```

**Recorder:** Inspect `./scripts/show_code.sh xss` and execute the context-specific ZAP scan. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Focus on `name` in HTML body, attribute and JavaScript string contexts; show the injected payload and evidence. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** ZAP reflected-XSS finding with request/response, do not assert actual browser execution unless filmed. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Show why output context dictates payload and encoding. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 93% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Step 3: test cross session csrf token — EO1c

**Real-world problem:** Token existence alone fails when ownership is not checked

**Exact on-screen command** (run from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`):

```bash
./steps/03-test-cross-session-csrf-token.sh
```

**Recorder:** Inspect `./scripts/show_code.sh csrf`, run the valid, missing, and cross-session controls. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Highlight session A token submitted with session B cookie and B's before/after email. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** Observed HTTP 200 / 403 / 200 plus actual state mutation on Alice's account. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Prove which session binding check is missing rather than calling any replay a flaw. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 96% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Step 4: reconcile security alerts — EO1a/b/c

**Real-world problem:** A scanner finding needs corroborating behavior before disposition

**Exact on-screen command** (run from `demos/module1-demos/m1-demo1-targeted-injection-xss-csrf`):

```bash
./steps/04-reconcile-security-alerts.sh
```

**Recorder:** Run the disposition step and examine the vulnerable sink and finding evidence. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Show SQL error, NoSQL count, command result and unencoded XSS; normal ping alone does not prove shell injection. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** ZAP's injected `host` request/response plus corroborating app behavior; recorded disposition. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** A professional triages individual proof, not merely a scanner's severity list. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 88% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Completion gate

Save the screen video, logs, GUI/CI proof, SHA and take ID. Compare against the approved LO and per-step CQA. No false PASS or silent unfreeze. The public learner README must be usable independently from its before branch. STOP if a proof artifact is unavailable and record the exact blocker.
