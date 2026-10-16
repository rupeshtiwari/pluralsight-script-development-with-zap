# Replay Parity And Evidence Synchronization Contract

## The requirement

The Narrator, Recorder and Editor need the **same meaning and same visible terminal fields** for every demo step. It is not realistic or truthful to guarantee the same raw request ID, timestamp, scan ID or fluctuating count across two fresh ZAP executions. Our contract uses **stable replay output plus an untouched audit log**.

## Single execution path

```text
preflight_check.sh
   → preflight_all_steps.sh
   → steps/01-concept.sh → scripts/_run_step.sh → scripts/_steps.sh
   → steps/02-concept.sh → scripts/_run_step.sh → scripts/_steps.sh
   → steps/03-concept.sh → scripts/_run_step.sh → scripts/_steps.sh
   → steps/04-concept.sh → scripts/_run_step.sh → scripts/_steps.sh

recorded named step
   → steps/0N-concept.sh → recording_step.py (comparison mode)
   → scripts/_run_step.sh → scripts/_steps.sh
```

The same internal rule engine executes in both cases. A successful preflight produces `logs/preflight-step-01.log` through `logs/preflight-step-04.log`; the filmed execution produces matching `logs/recorded-step-0N.log` after comparison. Every live raw output is retained in `logs/.producer/`.

## Approved normalization only

| May be normalized in the visible transcript | Must remain real and must match |
|---|---|
| Random request identifiers and timestamps | Actual scan-rule and alert identity |
| Running scan identifiers | Parameter names and affected endpoint |
| Clearly marked live scan-request counters | Alert risk and confidence |
| Some unstable telemetry, with real raw value retained | HTTP 401 / 200 / 403 and real state mutations |
| Priming notes that depend on an already-finished plan | Script registration and enabled state |
| | Actual gate exit code and the High-risk finding |
| | Script Console text or external CI data; these require separate observed proof |

**No normalization may change PASS into FAIL or vice versa, or invent an alert.** Risk, confidence, process exit and application state must reflect the current run. Review the raw proof alongside the normalized narration reference.

## Exact procedure

1. Clean checkout of the specific `m*-demo*-after` reference branch. Record the full Git SHA and pinned runtime version
2. Prepare Mac, start isolated demo, run `./scripts/preflight_check.sh`. Require exit 0 and the final summary `5 checks passed, 0 failed`
3. Share the four per-step normalized logs, full preflight transcript, **and unaltered raw logs** with Narrator
4. Narrator drafts exact spoken lines based only on these fields and relevant live ZAP GUI or GitHub Actions proof
5. Recorder checks out matching `m*-demo*-before`, performs necessary authored work, brings the exercise to the verified completed state, and places approved per-step baseline logs in the demo's `logs/` directory
6. Off-camera set `DEMO_SYNC_MODE=1`, `DEMO_SYNC_PHASE=compare`. Run the four exact public `steps/0N-name.sh` commands on camera
7. Each run writes `logs/recorded-step-0N.log`. A mismatch prints `SYNC MISMATCH` and exits nonzero; its diff is in `logs/.producer/`
8. Verify every GUI-only or Actions-only result separately against exact branch SHA, request URL and take. A terminal 'expected console' field **does not** prove the Script Console emitted it
9. Editor places the spoken line on the actual displayed field and highlights it for 6–8 seconds. Remove callouts when switching panes
10. Any changed command, source, scan configuration, query, title, report, or expected proof invalidates the prior reference: rerun preflight and regenerate the Narrator handoff

## Per-Take Manifest

```text
Demo ID / step number:
Learning objective (full wording):
Git reference / full commit SHA:
Before/after script diff completed:
Take ID / timestamp:
OS and pinned ZAP image:
Exact executed command:
Preflight full log and step reference:
Recorded normalized step log:
Unchanged raw runtime evidence:
Actual ZAP GUI pane, timestamp and request URL:
GitHub Actions workflow run + SHA + report:
Stable narration words and audio filename:
Editor highlight target and start/end timecode:
Comparison status and raw mismatch:
Technical CQA approval:
```

**Production quality bar:** 8-second clean command holds, one proof target at a time for 6–8 seconds, no single idle final frame over ten seconds, important click handles staged in raw footage, no on-screen typos, and consistent loudness averaging −6 to −12 dB with no peaks above −6 dB.

The skill must preserve this contract for all future demo repositories. Use source-driven output contracts and tests instead of assuming arbitrary dynamic output is naturally idempotent.
