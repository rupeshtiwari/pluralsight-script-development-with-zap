# Replay Parity And Evidence Synchronization Contract

## The requirement

The Narrator, Recorder and Editor need the **same meaning and same visible terminal fields** for every demo step. It is not realistic or truthful to guarantee the same raw request ID, timestamp, scan ID or fluctuating count across two fresh ZAP executions. Our contract uses **stable replay output plus an untouched audit log**.

## Single execution path

Developer, once from course repository root:

```text
setup/run-all-demo-preflights.sh
  → setup/run_all_demo_preflights.py
  → fetch origin and create temporary worktree for mN-demoM-after
  → demo startup → runtime/scripts/preflight_all_steps.sh
  → steps/01-concept.sh → scripts/_run_step.sh → scripts/_steps.sh
  → steps/02-concept.sh → same internal runner
  → steps/03-concept.sh → same internal runner
  → steps/04-concept.sh → same internal runner
  → teardown, copy real logs, generate per-demo documents and SHA manifest
```

Recorder, from one checkout at mN-demoM-before, after completing the exercise:

```text
steps/0N-concept.sh
  → scripts/_run_step.sh
  → recording_step.py when comparison mode is enabled
  → the same scripts/_steps.sh source
```

The Developer's completed-branch worktree generates `logs/preflight-step-01.log` through `logs/preflight-step-04.log` plus unmodified raw audit evidence in `logs/.producer/`. These are delivered outside the repository under the actual timestamped batch folder. For explicit comparison mode, place the approved baseline logs in the Recorder's demo `logs/` only after the starter implementation is complete. Fresh request IDs, scan IDs and counters can vary; compare meaningful, actual security facts.

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

1. **Developer:** Prepare the recording Mac once; run `./setup/run-all-demo-preflights.sh` once at repository root. It validates completed references in independent temporary worktrees and does not change the Recorder's checkout.
2. **Developer:** Inspect the batch process exit, each real `manifest.json`, branch SHA, startup/step/cleanup codes, four preflight logs, raw audit files and `production-guide.html`. A `RESULT: 5 checks passed, 0 failed` line only covers actual terminal steps, not GUI or hosted CI proof.
3. **Developer:** Distribute `~/zap-course-deliverables/batch-YYYYMMDD-HHMMSS.zip` and its actual extracted folder. Do not assert success or files exist before an observed Mac run creates them.
4. **Recorder:** Switch the existing checkout to `mN-demoM-before`, complete missing student source, start/reset the demo, verify application URLs, then film only its four concept-named commands in order.
5. **Recorder:** For strict replay comparison, stage the verified `preflight-step-0N.log` baseline files in this demo's `logs/` and run with `DEMO_SYNC_MODE=1 DEMO_SYNC_PHASE=compare` after matching source. A missing baseline or `SYNC MISMATCH` is a HOLD.
6. **Recorder:** Separately capture ZAP History, Script Console, Alerts, authenticated requests or GitHub Actions run evidence where terminal output cannot substantiate the claim. Record full SHA, URL, GUI pane and take ID.
7. **Narrator:** Use genuine Developer output for preparation but freeze ElevenLabs lines only against the Recorder's actual take and matching GUI/CI proof.
8. **Editor:** Align the spoken claim to the currently visible field and one 6–8-second highlight. Remove annotations on pane transitions; never hide a failed step.
9. **Technical CQA:** Validate material alert identities, risk, confidence, process exit, same-take output and source revisions. Green structural CI is not runtime proof.
10. **Change control:** Any changed command, source, plan, parameters, report or expected proof invalidates prior references and narration. Regenerate from the single batch and distribute updated evidence.

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


## Single-Checkout Production Workflow (Approved)

- **One clone per Recorder.** Sequential exercises use `git switch mN-demoM-before` in the same folder. Preserve authored changes; never force-delete local work.
- **Developer performs one batch.** The Developer checks completed `*-after` refs using temporary worktrees and distributes six reports. The Recorder does not redo the batch.
- **Exact evidence directory.** Use the real timestamped `~/zap-course-deliverables/batch-YYYYMMDD-HHMMSS/<demo>/`; an illustrative `deliverables/` path is not evidence of a real file.
- **Compare only verified source.** Stage four reference logs and execute the matching completed starter behavior. Preserve untouched raw values separately; never transplant a completed solution to bypass the exercise.
- **Role sequence:** Developer → Recorder → Editor → Narrator → Technical CQA. Final audio and visuals are accepted only against the same source and take.
- **Privacy:** The current author folder is temporarily public by explicit owner instruction. Before learner delivery move it to private storage; deleting a dot-folder does not remove its public Git history.
