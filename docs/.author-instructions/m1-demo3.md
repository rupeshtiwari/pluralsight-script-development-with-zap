# M1-DEMO3 — Python Rules and Authentication

**Approved enabling objectives:** EO2b / EO2c  
**Scenario / senior operator decision:** Maya must reach a protected profile as a real ZAP context user before her custom Jython rule can test the profile's reflection.  
**Exact demo folder:** `demos/module1-demos/m1-demo3-python-scanning-authentication`  
**Branch pair:** `m1-demo3-before` → `m1-demo3-after`  
**Primary UI:** VS Code + ZAP GUI http://localhost:8080/zap/ + integrated terminal  
**Required diagram:** `docs/learner-diagrams/m1-demo3-architecture.svg`

## Preparations and private handoff

1. From repo root, run `./setup/setup-macos.sh` once. Select the assigned demo branch and enter `demos/module1-demos/m1-demo3-python-scanning-authentication`. Start the stack with the setup or reset command shown in this demo's README. Do not execute preceding demos.
2. Run `./scripts/preflight_check.sh` and preserve the actual timestamped `logs/` output. The preflight log is not automatically the same capture as another take.
3. Recorder follows the four commands below in order; records live GUI/CI-only output separately and holds commands and click targets for the specified editing handles.
4. Narrator and Editor use an evidence manifest tied to the same branch SHA, take and output, not hypothetical numbers.

## Step 1: load python active scan rule — EO2b

**Real-world problem:** A generic scanner may miss application-specific unsafe reflection

**Exact on-screen command** (run from `demos/module1-demos/m1-demo3-python-scanning-authentication`):

```bash
./steps/01-load-python-active-scan-rule.sh
```

**Recorder:** Show `zap-scripts/globomantics-active-rule.py` and load as ZAP Active Rules Jython script. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Focus on `_probe_request`, `_check`, `sas.newAlert()` and `note` parameter. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** Actual loaded active rule and source; named alert is not yet claimed fired. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Teach cloned request, encoded parameter replacement and named alert mechanism. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 95% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Step 2: register scripted authentication — EO2c

**Real-world problem:** Protected pages require reproducible login, not manually pasted cookies

**Exact on-screen command** (run from `demos/module1-demos/m1-demo3-python-scanning-authentication`):

```bash
./steps/02-register-scripted-authentication.sh
```

**Recorder:** Inspect `zap-scripts/globomantics-auth.py` and register it under Authentication scripts. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Focus on `authenticate`, Login URL and `username=alice`; this training login omits a production password flow. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** Actual script registration with required context/credentials parameters. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Session management is automated; acknowledge this lab's deliberately simplified login. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 95% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Step 3: confirm authenticated profile access — EO2c

**Real-world problem:** A scan can silently assess only the login wall if auth fails

**Exact on-screen command** (run from `demos/module1-demos/m1-demo3-python-scanning-authentication`):

```bash
./steps/03-confirm-authenticated-profile-access.sh
```

**Recorder:** Use ZAP context user Alice and execute authenticated profile step. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Focus on unauthenticated 401 versus scripted-authenticated 200; verification regex and auth trace. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** Observed independent 401 and 200 responses; script executed within ZAP. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Prove coverage before trusting any security result. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 93% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Step 4: confirm custom scan alert — EO2b

**Real-world problem:** An active rule is only useful if it produces the intended finding under an authenticated scan

**Exact on-screen command** (run from `demos/module1-demos/m1-demo3-python-scanning-authentication`):

```bash
./steps/04-confirm-custom-scan-alert.sh
```

**Recorder:** Run named custom-alert scan after clearing stale results. Show the command in a mobile-readable terminal for 8–10 seconds before Enter. Highlight only Focus on `Globomantics unsafe reflection (custom rule)`, Medium risk, `note` and evidence `GLOBOxss7marker`. Hold real output legibly; for GUI clicks, keep 8-second pre-click and post-click handles. Record screen location and exact line, source or URL in the take manifest.

**Required evidence:** Named alert absent before and present after; GUI Alerts tab and request proof. Stop rather than claim a PASS if missing.

**Narrator's unique teaching focus:** Tie custom finding identity to the authenticated profile and parameter. Use the actual same-SHA/take log plus GUI evidence. Write 18–22 natural spoken words for the initial 8–10-second command hold, then teach what is visible. Do not duplicate another step or say 'on this slide'.

**Editor:** Cut cleanly at the command/source/GUI transition. Highlight only the command parameter, output or UI element named above, remove the previous callout on the next focus change, and sync to this take's actual result. Keep the actionable result steady.

**Source-review confidence:** 94% (not live-runtime verified). **Release:** only after required real proof is captured; do not raise confidence to 95 by assertion.

---

## Completion gate

Save the screen video, logs, GUI/CI proof, SHA and take ID. Compare against the approved LO and per-step CQA. No false PASS or silent unfreeze. The public learner README must be usable independently from its before branch. STOP if a proof artifact is unavailable and record the exact blocker.
