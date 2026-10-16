# Developer, Recorder, Editor, Narrator and Technical CQA — Course Production Roles

## Developer
- Prepare the Mac once. Run `./setup/run-all-demo-preflights.sh` **once** at repository root to validate all six completed branches using temporary worktrees without switching the Recorder's checkout.
- Share the timestamped ZIP with six SHA-bound manifests, exact commands and actual outputs, raw logs, and generated HTML. Structural CI success does not replace real Mac execution.
- Failed demos remain HOLD; never claim sample output was observed or narration approved from an unverified run.

## Recorder
- Clone the course repository **once per recorder**. Receive the Developer's successful batch proof from the completed `*-after` reference, then switch your existing checkout directly to the demo's `*-before` branch. Complete the authored exercise, start the stack and film the four named steps. Do not rerun the Developer batch. Use another clone only for another engineer or optional independent concurrent work.
- Use the exact public conceptual step script names. Prepare the source pane, hold the command for ~8 seconds before Enter, then show actual output fields, one field per 6–8 seconds. Proactively zoom to phone-readable text.
- Show exact application URL or GUI navigation. Do not jump between panes without a clean focus change. For significant mouse click: pointer on target for ~8 seconds, click once, show resulting state for ~8 seconds in source footage.
- Avoid browser tabs when recording full-screen application UI. No on-screen backspaces, corrections or idle long waits; cut and retake.
- Keep named command execution real. Off-camera use `DEMO_SYNC_MODE=1` and `DEMO_SYNC_PHASE=compare`; inspect the current per-step logs before marking footage accepted.
- Capture actual GUI-only ZAP Script Console lines, Alerts tab records, request History headers, and GitHub Actions reports separately when source-step output cannot observe them.

## Narrator
- Use successful preflight baseline logs per step and associated live GUI/Actions proof from the same approved source revision. Never script from a hypothetical PASS.
- Provide the **exact spoken words** for ElevenLabs, not production notes; one unique technical mechanism and practitioner decision per step, directly tied to what the Recorder shows.
- Lead with the security question; then introduce the exact named command, significant script parameters, result fields and operator consequence. Avoid module-relative course navigation.
- For an 8-second command hold write around 18–22 spoken words; additional output explanations each fit the displayed 6–8-second proof beat. Slide reveals max 27 words/12 seconds.
- Spoken forms should be natural: 'trust boundary one', 'LLM one', and 'rag' as appropriate, no slash-heavy syntax or acronym stacks. Narrate observed values only after validating the actual take.
- Any change to source, output, report or recorded value triggers revalidation and narration regeneration before freeze.

## Editor
- Match branch SHA, preflight reference, recording comparison log and audio to the same approved take. A retake must not silently change the proof.
- Cut at screen/pane transitions and before and after script writing or actual output display. Do not hide a failing step with a PASS from another run.
- Use a small, legible square box around key parameters, arrows between related evidence fields, or a single subtle callout. One focus only; immediately remove the previous overlay on focus change.
- Keep each proof stable 6–8 seconds, never over ten seconds of idle final footage. Cut long scans cleanly without deleting the proof. Important clicks have eight-second handles in raw footage; trim in final cut.
- Validate on phone, no watermarks obscuring code, readable metric/parameter names, no awkward text wraps.
- Audio: consistent level across clips, average −6 to −12 dB, peaks no higher than −6 dB.

## Final CQA
- Technical accuracy, current methods, correct learner workflow and scenario realism; inspect the approved outline for exact LO alignment
- Slide content reviewed before slide narration; demonstration narration tied to actual visible proof
- Per-step objective and proof artifact, exact command/script filename, real request/response and operator decision
- Source-review percentage distinct from verified runtime result; 95% and above is owner's content acceptance threshold, not permission to fabricate missing evidence
- Freeze a valid step, don't redesign an entire working repo because an unrelated demo lacks local Docker
- Internal author instructions remain temporary in PUBLIC dot folder only at owner's explicit request; private storage is required before learner release


## Single-Checkout Production Workflow (Owner's Latest Decision)

- **One clone per Recorder.** Switch to `mN-demoM-before` in the same checkout for each sequential exercise. Preserve all authored work before switching; never force-reset or delete recordings.
- **Developer-only batch.** The Developer runs the one Mac batch across `*-after` reference branches in disposable worktrees and distributes validated SHA-bound evidence. The Recorder does not run another preflight.
- **Location of real evidence.** Read the timestamped `~/zap-course-deliverables/batch-YYYYMMDD-HHMMSS/<demo>/` package. Do not claim it exists until the Developer provides a verified manifest and four real logs.
- **Starter exercise.** Record only after completing any missing lesson code on the `*-before` branch. Never copy completed answers into starter files just to manufacture a passing recording.
- **Comparison mode.** Stage the Developer's matching `preflight-step-0N.log` files inside the selected demo's `logs/` only when proof comparison is required. Volatile display fields may normalize; actual security facts, raw logs and real failures may not.
- **Editor, Narrator and CQA.** All must use the same recorded take, actual outputs and GUI/Actions proof. A mismatch is HOLD, not material for editing into a PASS.
- **Hub is authoritative.** It links the six per-demo playbooks and student `before` and completed `after` references. One-time installation and the batch command are documented only there.
