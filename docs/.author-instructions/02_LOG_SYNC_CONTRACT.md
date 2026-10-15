# Same-Evidence Contract: Recorder → Narrator → Editor

## Canonical evidence identifiers
Every recorded step must bind: `course`, `module`, `demo_id`, `step_number`, exact **branch and SHA**, **take ID**, exact **command**, environment version, **actual exit code**, preflight log path, captured GUI/Actions proof path, final audio file and editor timestamp.

1. From the demo directory, run `./scripts/preflight_check.sh` in a clean environment. Keep the generated timestamped plain-text log under `logs/`. It is a validation run, not automatically the same footage as a later take.
2. Run each named `./steps/0N-concept.sh` during the footage capture, collecting the step's actual unedited stdout/stderr and process status. Prefer recording a terminal session with both visible output and separate log capture.
3. Reconcile the preflight against the filmed **same-take** output: normalize known variable fields only (request IDs, timestamps, session ids, counts) and write down any difference. Never pretend distinct runs are byte-for-byte identical.
4. For GUI proof (not reachable through the shell), capture the **actual** ZAP Script Console line, script enablement, request History header or Alerts tab; capture the exact HTTP message or alert name matching the take.
5. For GitHub Actions proof, bind to the exact workflow **run ID** and **commit SHA**. A successful/failed step is not sufficient to prove an intended risk decision without inspecting the associated report and process code.
6. Narrator receives a frozen handoff with stable visible facts, the screenshot/timestamp index and unresolved gaps. Spoken narration must match exactly what is visible.
7. Editor uses one source for each narrated claim. Highlight the displayed parameter, filename, output line, rule ID, risk rating, report or process exit; never a different request.
8. Re-run validation and regenerate the handoff whenever the command, source file, API path, script order or expected result changes.

## Producer handoff record (copy per take)
```text
Demo/Step:
Approved LO:
Before/after branch + SHA:
Take ID / timestamp:
Screen and exact URL / UI pane:
Command:
Parameter or rule ID shown:
Actual stdout/stderr log and exit:
Actual GUI screenshot or GitHub Actions URL:
Narration audio and exact words:
Editor highlight start/end timecode:
Source-vs-take mismatch:
CQA verdict and confidence:
```

## Live versus example output
A README example is not an observed result; a static command inspection is not active rule execution; a source `print()` is not a live Script Console message. Preflight may verify a fresh proxied header without querying the Script Console. Treat these evidence boundaries explicitly.
