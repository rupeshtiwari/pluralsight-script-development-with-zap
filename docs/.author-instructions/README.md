# Author Production Runbooks — Temporary Public Staging

<div align="center">

![Recorder](https://img.shields.io/badge/RECORDER-Real_Footage-0284c7?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-Verified_Evidence-d946ef?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-Camtasia_Sync-16a34a?style=for-the-badge)

**Six demonstrations · Four steps each · One controlled output contract**

</div>

**Privacy notice:** This dot folder is PUBLIC because the GitHub repository is public. It is temporarily staged here at the owner's request. Move it into a private repository before Pluralsight learner delivery. Deleting it later does not erase public Git history. Do not commit real private audio files, footage, secrets or confidential review notes.

## Why We Run Preflight First

The Recorder and Narrator work in parallel. The Narrator needs to know what each command **actually prints** before the footage is captured. The Recorder then executes the same four concept-named commands using the same source revision, and a replay check compares a normalized visible transcript with the preflight reference. This removes script/text drift without pretending two independent raw ZAP runs generate identical IDs or counts.

**The successful preflight is a mandatory gate**, not a script that prints expected PASS statements. It runs each genuine step. Failed executions cannot publish a narration reference. The raw logs remain unchanged.

## Five-Part Handoff

1. **Reference environment:** Clone the assigned **`m*-demo*-after`** branch into a separate folder, run `./setup/setup-macos.sh` once, run the demo's `./scripts/demo_up.sh` (or `demo_reset.sh` where instructed), then `./scripts/preflight_check.sh`
2. **Approve logs:** Require `5 checks passed, 0 failed`, inspect `logs/preflight-<timestamp>.log`, and share `logs/preflight-step-01.log` through `logs/preflight-step-04.log`. Record the branch SHA and external GUI/Actions evidence separately
3. **Recorder:** Clone the matching **`m*-demo*-before`** branch independently, create its missing source/plan as the student would, and capture full-screen real execution. Set `DEMO_SYNC_MODE=1` and `DEMO_SYNC_PHASE=compare` off-camera
4. **Narrator:** Use the actual preflight reference plus the same-SHA GUI/CI proof; record the exact spoken lines from the playbook only after confirming every claim is visible in the footage
5. **Editor:** Match each spoken beat to that same recorded result, show a single highlighted parameter/finding at a time for 6–8 seconds, cut waiting/typos, remove obsolete callouts, and retain the evidence manifest

## The Six Production Playbooks

| Playbook | Recorded problem | Student starter | Full author guidance |
|---|---|---|---|
| M1 Demo 1 | Injection, XSS and CSRF | `m1-demo1-before` | [Recorder / Narrator / Editor](m1-demo1.md) |
| M1 Demo 2 | HTTP Sender JavaScript | `m1-demo2-before` | [Recorder / Narrator / Editor](m1-demo2.md) |
| M1 Demo 3 | Jython custom rule and authentication | `m1-demo3-before` | [Recorder / Narrator / Editor](m1-demo3.md) |
| M2 Demo 1 | Headless authenticated CI | `m2-demo1-before` | [Recorder / Narrator / Editor](m2-demo1.md) |
| M2 Demo 2 | ZAP API and Insights | `m2-demo2-before` | [Recorder / Narrator / Editor](m2-demo2.md) |
| M2 Demo 3 | False Positive filter and quality gate | `m2-demo3-before` | [Recorder / Narrator / Editor](m2-demo3.md) |

Additional controls: [Persona Protocols](01_PERSONA_PROTOCOLS.md) · [Output Parity Contract](02_LOG_SYNC_CONTRACT.md) · [Technical CQA Findings](03_CQA_FINDINGS.md) · [Recording Release Checklist](04_RELEASE_CHECKLIST.md)

## Recorder Command Pattern

```bash
# In the authorized, completed demo source state:
./scripts/preflight_check.sh     # all four real step commands + reference logs

# Off-camera in the separate recorder checkout:
export DEMO_SYNC_MODE=1
export DEMO_SYNC_PHASE=compare

./steps/01-<concept>.sh
./steps/02-<concept>.sh
./steps/03-<concept>.sh
./steps/04-<concept>.sh
```

The names shown in angle brackets above are examples; every actual playbook supplies all four exact filenames. The same evidence must appear on the terminal screen, but a live GUI output, CI result, or security value cannot be invented by normalization. If a comparison fails, repeat the step only after investigation; do not substitute a PASS from an earlier recording.
