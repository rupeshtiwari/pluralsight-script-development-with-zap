# M1-DEMO2 — JavaScript HTTP Sender

**Approved enabling objectives:** EO2a  
**Scenario / senior operator decision:** Maya needs to mark specific proxied requests and prove the JavaScript hook was actually executed.  
**Exact demo folder:** `demos/module1-demos/m1-demo2-javascript-http-sender`  
**Branch pair:** `m1-demo2-before` → `m1-demo2-after`  
**Primary UI:** ZAP GUI http://localhost:8080/zap/ + Terminal; source under zap-scripts/  
**Required diagram:** `docs/learner-diagrams/m1-demo2-architecture.svg`

## Preparations and private handoff

1. From repo root, run `./setup/setup-macos.sh` once. Select the assigned demo branch and enter `demos/module1-demos/m1-demo2-javascript-http-sender`. Start the stack with the setup or reset command shown in this demo's README. Do not execute preceding demos.
2. Run `./scripts/preflight_check.sh` and preserve the actual timestamped `logs/` output. The preflight log is not automatically the same capture as another take.
3. Recorder follows the four commands below in order; records live GUI/CI-only output separately and holds commands and click targets for the specified editing handles.
4. Narrator and Editor use an evidence manifest tied to the same branch SHA, take and output, not hypothetical numbers.

## Step 1: load javascript http sender — EO2a

**Real-world problem:** A source file does not run until ZAP registers and enables it

**Exact on-screen command** (run from `demos/module1-demos/m1-demo2-javascript-http-sender`):

```bash
./steps/01-load-javascript-http-sender.sh
```

**Recorder:** Show `zap-scripts/globomantics-marker.js` and the ZAP HTTP Sender script tree; run the named loader. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Focus on `sendingRequest`, `setHeader`, `print`, and `globomantics-marker` registered script name. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** Actual ZAP script registration and engine with successful load, not imaginary live execution. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Hook placement affects only requests handled by ZAP. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 95% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Step 2: prove outbound marker header — EO2a

**Real-world problem:** Registration alone does not prove traffic mutation

**Exact on-screen command** (run from `demos/module1-demos/m1-demo2-javascript-http-sender`):

```bash
./steps/02-prove-outbound-marker-header.sh
```

**Recorder:** Send a fresh proxied `/greet` request with the named command, then show ZAP History request. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Focus on header `X-Globomantics-Marker: GLOBO-DEMO` and its unique request URL. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** Real outgoing request header captured in ZAP or terminal helper. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Connect the source's header hook to observable network state. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 96% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Step 3: check live script console — EO2a

**Real-world problem:** A printed expected format is not actual Script Console evidence

**Exact on-screen command** (run from `demos/module1-demos/m1-demo2-javascript-http-sender`):

```bash
./steps/03-check-live-script-console.sh
```

**Recorder:** Open ZAP Scripts → Script Console and trigger a fresh request with named step. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Show live `[globo-marker]` line with the same request URL; terminal text is only expected format. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** Actual ZAP Script Console line visible, screenshot/take reference mandatory. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Differentiate script output from validation-harness output. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 86% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Step 4: verify enabled script registration — EO2a

**Real-world problem:** Teams need a reusable enabled script rather than a transient probe

**Exact on-screen command** (run from `demos/module1-demos/m1-demo2-javascript-http-sender`):

```bash
./steps/04-verify-enabled-script-registration.sh
```

**Recorder:** Inspect the registered HTTP Sender script in the GUI and query ZAP state. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Focus on name, script type, JavaScript engine, `enabled=true`. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** Current registration; do not claim persistence across a destroyed container. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Reusable script identity is a configuration contract. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 95% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Completion gate

Save the screen video, logs, GUI/CI proof, SHA and take ID. Compare against the approved LO and per-step CQA. No false PASS or silent unfreeze. The public learner README must be usable independently from its before branch. STOP if a proof artifact is unavailable and record the exact blocker.
