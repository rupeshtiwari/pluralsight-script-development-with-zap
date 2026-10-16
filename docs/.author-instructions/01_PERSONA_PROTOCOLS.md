# Recorder, Narrator, Editor — Course Production Roles

## Recorder
- Clone the course repository **once per recorder**. For each assigned demo, switch to its matching `*-after` branch and run/approve preflight first; then stop the stack and switch within that same checkout to `*-before` to perform and film the student's authored steps. Another clone is needed only on a different engineer's machine or optional concurrent worktree.
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

- **One clone per Recorder for the course.** When the same engineer records multiple demos sequentially, use `git switch mN-demoM-after` for preflight, archive logs, clean up Docker, and `git switch mN-demoM-before` to perform/film the exercise within that same clone. The existing folder name never changes when switching branches.
- Default initial folder: `~/pluralsight-script-development-with-zap`. Do not ask the same Recorder to clone the repository three times for three separate demos. `git clone URL /custom/path` is allowed for the person's preferred initial folder name.
- Preflight `after` first, require live PASS and four per-step logs, then copy `preflight-step-0[1-4].log` into an independent safe evidence directory such as `~/zap-production-evidence/m1-demo1/` before stopping services and switching to the starter.
- Preserve authored work before switching away from a starter. `git switch` may refuse on dirty tracked files; do not force-reset or delete recordings. Optional `git worktree` creates separate working directories when two branches must be available at once; it is not the default.
- The Narrator can run a separate clone on their own machine in parallel. The Recorder does not need to clone per demo; the two roles naturally have separate machines/filesystems.
- Direct author dashboard must list all demo author playbooks, the matching `before` learner README, the finished `after` reference, and branch-specific GitHub links. Per-demo playbooks show exactly one clone-once starter, then copyable switch/prepare/preflight/record commands.
- GitHub-native formatting: colored category badges, aligned HTML tables and open/closed `details` panels with natural-language labels. Keep code fences copyable and exact. GitHub strips unsupported CSS; never depend on raw inline CSS for essential instructions.

