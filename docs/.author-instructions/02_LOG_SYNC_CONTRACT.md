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

1. Use the Recorder's **single existing course checkout**; switch to the specific `m*-demo*-after` reference branch. Record the full Git SHA and pinned runtime version
2. Prepare Mac, start isolated demo, run `./scripts/preflight_check.sh`. Require exit 0 and the final summary `5 checks passed, 0 failed`
3. Share the four per-step normalized logs, full preflight transcript, **and unaltered raw logs** with Narrator
4. Narrator drafts exact spoken lines based only on these fields and relevant live ZAP GUI or GitHub Actions proof
5. Recorder stops the demo, archives the reference logs outside the checkout, and **switches** the same repository to matching `m*-demo*-before`, then performs necessary authored work, brings the exercise to the verified completed state, and places approved per-step baseline logs in the demo's `logs/` directory
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


## Single-Checkout Production Workflow (Owner's Latest Decision)

- **One clone per Recorder for the course.** When the same engineer records multiple demos sequentially, use `git switch mN-demoM-after` for preflight, archive logs, clean up Docker, and `git switch mN-demoM-before` to perform/film the exercise within that same clone. The existing folder name never changes when switching branches.
- Default initial folder: `~/pluralsight-script-development-with-zap`. Do not ask the same Recorder to clone the repository three times for three separate demos. `git clone URL /custom/path` is allowed for the person's preferred initial folder name.
- Preflight `after` first, require live PASS and four per-step logs, then copy `preflight-step-0[1-4].log` into an independent safe evidence directory such as `~/zap-production-evidence/m1-demo1/` before stopping services and switching to the starter.
- Preserve authored work before switching away from a starter. `git switch` may refuse on dirty tracked files; do not force-reset or delete recordings. Optional `git worktree` creates separate working directories when two branches must be available at once; it is not the default.
- The Narrator can run a separate clone on their own machine in parallel. The Recorder does not need to clone per demo; the two roles naturally have separate machines/filesystems.
- Direct author dashboard must list all demo author playbooks, the matching `before` learner README, the finished `after` reference, and branch-specific GitHub links. Per-demo playbooks show exactly one clone-once starter, then copyable switch/prepare/preflight/record commands.
- GitHub-native formatting: colored category badges, aligned HTML tables and open/closed `details` panels with natural-language labels. Keep code fences copyable and exact. GitHub strips unsupported CSS; never depend on raw inline CSS for essential instructions.

