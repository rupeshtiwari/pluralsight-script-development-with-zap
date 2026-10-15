# Recorder, Narrator and Editor — Exact Contract

## Recorder: prescriptive full-screen footage
- Work from a clean and independent checkout of the assigned **before** branch. Record the branch SHA, OS, ZAP image digest and lab URL before recording; no previous demo session is a prerequisite.
- Use `setup/setup-macos.sh` once per Mac, then the demo's `./scripts/demo_up.sh` or `./scripts/demo_reset.sh` (where required). Use descriptive `./steps/01-*.sh` through `./steps/04-*.sh` only. No on-screen `demo_step.sh 1` commands.
- Start with the real business/security problem and one operator goal. Each step must teach an individual concept, not another step's definition.
- Record **full screen**; when the target is terminal, do not display distracting browser tabs. Use mobile-readable font/zoom proactively; one primary pane at a time. Show source+integrated terminal in VS Code when source is the proof; use standalone terminal when only commands matter; show ZAP GUI when it uniquely establishes proof.
- Before executing a step, place its entire concept-named command and important parameter on screen for **8–10 seconds**. Explain its purpose and expected evidence briefly; then run it, hold the relevant actual output readable. Do not leave the frame idle longer than 20–30 seconds.
- Before a significant UI click, position the pointer on the target and provide ~8 seconds of footage; click once and hold the resulting state ~8 more seconds. Those are editing handles, **not mandatory final-video dead air**.
- Track the exact pane/URL, tab, path, line or parameter, scroll position, mouse location, and proof region in the step's private recording manifest. No on-screen corrections/backspaces; redo the take and cut cleanly.
- A literal script printed in Terminal is not the same thing as a ZAP Script Console line. Capture separate live GUI/CI proof where mandated. Every technical assertion needs visible output, alert, trace, process exit, or log/report line.

## Narrator: ElevenLabs, grounded in evidence
- Use the **same-run preflight log and matching take's GUI/CI evidence manifest** to create exact spoken narration, not speculative sample values. Do not hardcode variable request IDs, counts, session handles or scan timings.
- Teaching flow per step: concrete production problem → bounded mechanism and parameter → observed proof → operator decision. Every step adds **one unique** mechanism or consequence; eliminate duplication.
- Natural TTS phrasing: say 'trust boundary one', 'LLM one', and 'rag' where TTS needs it; avoid abbreviation stacks, punctuation-heavy scripts and artificial transitions. No 'this module', 'previous clip', 'on this slide', 'next section', or other relative course navigation.
- For an 8–10-second command hold, use ~18–22 spoken words. For slide reveals follow max **27 spoken words per 12 seconds**. Clip narration targets only the approved LO and visible evidence; do not narrate hidden setup as if shown.
- Revision must be completed **before freeze**. Regenerate narration for any changed step command, branch SHA, visible proof, screenshot/callout, query, or report. Finalize with per-step word count and LO traceability.

## Editor: precise video/audio/evidence synchronization
- Assemble approved full-screen footage and separate ElevenLabs voice files. Cut during source/terminal/GUI transitions, before visible script typing if it risks typo/backspace, and after actual output is held steady. Never cut away before the evidence is legible.
- Highlight one parameter, pane, button or output region at a time. Use transient callouts/arrows when switching panes; **remove as soon as the focus changes or becomes blank**. Avoid stale highlights.
- Do not fabricate missing alerts or replace a failed command with a PASS from a different run. When narration references live identifiers, match the exact video evidence; if impossible, rewrite the spoken line to describe stable fields instead.
- Aim for consistent course loudness: average **−6 to −12 dB**, with **no peaks above −6 dB**. Confirm clean readability on a phone and no awkward line/token wraps.
- Keep visual activity meaningful every 20–30 seconds, but never speed through the key response, request, job result, or gate decision.
- Maintain source SHA, step ID, take number, terminal log file, GUI screenshot/timestamp, narration filename and editor timecode in the private manifest.

## CQA and delivery
- Check outline alignment and source correctness **slide first, narration second** where applicable. Also check technical currency, professional realism, student repeatability, and whether any definition-only step lacks an operator choice.
- Check for duplication, early spill into other topics, and proof overclaims. Label each finding CONFIRMED / REPORTED BUT UNVERIFIED / NOT VERIFIED / FAILED.
- The course is eligible for content freeze at the owner's accepted threshold **95% and above**, but runtime verification is a separate status. Do not assign false 95% evidence; flag risk at individual steps and fix only with approved code changes.
