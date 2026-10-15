# Author Production Pack — TEMPORARILY PUBLIC

> **REMOVE BEFORE PLURALSIGHT LEARNER DELIVERY.** This dot-prefixed folder is PUBLIC because the repository is public. Git history will continue to expose committed material even after deletion. Move the production pack to a **private repository or controlled workspace**, verify access, and remove all public refs and history exposure as appropriate. Never store secrets, private video takes, personal data, or sensitive internal notes here.

This operational material is for the author's distributed team only. It is **not** a student deliverable. The three Pluralsight deliverables are the learner GitHub repository, slides, and the edited video.

## Team use
1. Recorder opens the assigned `m*-demo*-before` branch, follows the per-demo playbook and runs the existing four **concept-named** step commands; never change code or order without approval
2. Narrator uses the **real terminal preflight log and matching GUI/Actions evidence** to write ElevenLabs-ready spoken lines, one distinct teaching decision per step
3. Editor synchronizes voiceover to the *same verified output*, adds short-lived single-focus highlights, and cuts at transitions
4. Technical CQA signs off against the approved outline, LO and actual evidence; percentages are estimates, not proof

## Files
- [Recorder, Narrator and Editor contract](01_PERSONA_PROTOCOLS.md)
- [Evidence and narration synchronization](02_LOG_SYNC_CONTRACT.md)
- [Technical proof gaps and fixes](03_CQA_FINDINGS.md)
- [Recording and release checklist](04_RELEASE_CHECKLIST.md)
- Six per-demo playbooks: `m1-demo1.md` through `m2-demo3.md`

Use `python3 runtime/scripts/repo_quality_check.py` for **static** checks, and each demo's own `./scripts/preflight_check.sh` for on-machine results.

When the code, source paths, parameters or step output changes, regenerate the log, update the narrator handoff, and reconfirm on-screen proof before recording. Do not label screenshots, example output or historic logs as live execution.
