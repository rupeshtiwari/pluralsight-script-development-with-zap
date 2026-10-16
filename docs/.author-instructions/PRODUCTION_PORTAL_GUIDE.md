# Script Development with ZAP — Producer's Course Portal

> **Author-only production deliverable.** This folder is generated from the Developer's actual six-demo Mac batch. It is NOT the learner's course repo, not a simulated scan and not proof that UI/CI recordings were captured. The source of truth for teaching is `docs/course-outline.md` in the matching GitHub revision.

## Launch and navigate on the recording Mac

1. Open **macOS Terminal** (not VS Code or the ZAP GUI). From the repo root, the Developer runs `./setup/run-all-demo-preflights.sh` **once**, then inspects all six manifests. The runner packages the real batch outside the repo under `~/zap-course-deliverables/batch-YYYYMMDD-HHMMSS/`.
2. In macOS Terminal, run `cd "$HOME/zap-course-deliverables/batch-ACTUAL_TIMESTAMP"`, replacing the timestamp with the printed folder name. Then run `./serve.sh`. The launcher refreshes the HTML from the evidence and opens `http://127.0.0.1:8765/index.html`. It binds **only to the local Mac**. Stop with **Control+C**.
3. The left navigation selects a demo. The five role tabs select **Developer → Recorder → Narrator → Editor → Technical CQA**. Step 1–4 selects the approved action in that demo. Hash routes are shareable within the locally served folder.
4. The source SHA on the page is the completed reference revision. Follow links to the exact `*-before` and `*-after` GitHub source. Do not film the completed branch instead of the learner exercise.
5. To regenerate after a separate narrator has returned approved files, place `narration-final.json` and `narration-final.md` inside the corresponding `mN-demoN/` folder, run `./refresh.sh` from **this batch root**, then refresh the page. `./refresh.sh` neither calls ZAP nor rewrites the raw logs.

## Recorder — one checkout, four exact actions

Each step displays **Where to go**: open the indicated application or pane manually and **paste the full `cd` shell command** in VS Code's integrated Terminal or macOS Terminal. Never navigate directory trees by hand, and never substitute a command for the concept-named `./steps/0N-*.sh` displayed below it. Source editor instructions and browser/ZAP GUI locations are shown with the step. Stay within authorized Globomantics training endpoints.

Before Enter, show the relevant source context and hold the named command approximately 8 seconds. After actual execution, hold each meaningful real field approximately 6–8 seconds, using readable 26–30-point terminal/IDE text. For an important GUI click, hold 8 seconds before and after in the raw take; the Editor trims extra material. Do not record typos/backspaces, browser tabs, idle scans or an unexplained branch switch. Actual ZAP History, Script Console, Alerts or GitHub Actions proof must be captured separately when the terminal cannot prove them.

## Editor — exact overlays with one focus at a time

Every step's **Editor** panel has a six-row shot map: the named command, the large relevant-output area, the exact recorded primary value, the relationship arrow to its second field, a temporary gist callout for longer static shots, and the final result. **Never invent the value to highlight**: pink focus is derived from the real formatter's current raw proof. When a named field is absent, the editor map says HOLD.

Use a single large **blue `#00A3FF` outline** around the current source/result area. Introduce a small **Transform Pink `#FF1675` label** for the exact named value inside the box. When two actual fields are visible, use one small **purple `#770EF7` arrow** between them; remove stale callouts when the pane changes. If the same screen continues for more than 12 seconds, add the supplied concise **yellow `#FFC942` gist callout** for ~6–8 seconds, then change or remove it. The callout is visual teaching text, not fake terminal output. Use consistent thin strokes, rounded corners compatible with the Pluralsight template, readable type, and no spotlight effect.

Cut startup waits, scanning progress without new evidence, typing corrections, mismatched takes, click noise and idle end frames. Preserve the full executed action and operator decision. Edited clips must be 1920×1080, 30 fps, with matched sound levels and approximately one second of silent visual lead/tail. Do not exceed the owner's audio peak ceiling.

## Narrator — pass this bundle to the separate narration skill

For each of the six demo folders, `narration-handoff.json` contains: exact demo ID, approved LO meaning, `before` and `after` GitHub references, completed reference SHA, actual step script names and `cd` commands, the terminal's captured field/value pairs, transcript and raw log pointers, fixed three-beat script reference, and specific Editor visual anchors. `NARRATION_HANDOFF.md` explains the process in plain language. `narration-final.TEMPLATE.json` defines the import contract. The source logs stay immutable.

In a separate ChatGPT session attach the **generated batch ZIP**, plus the **Distributed Demo Production skill** and both owner-supplied **Rupesh teaching-style** and **Rupesh teaching-narration** skill packages, or install those skills in that environment. Give it this instruction:

> Review the attached ZAP production batch, its `mN-demoN/narration-handoff.json`, `NARRATION_HANDOFF.md`, the approved outline and any accompanying matching-take GUI or GitHub Actions evidence. Apply the Rupesh teaching and ElevenLabs skills. Preserve all four existing commands, source files, order, field names and learning objectives. Create human spoken narration in three on-screen beats per step: BEFORE command, DURING actual displayed result, AFTER operator decision. Each spoken beat must be 27 words or fewer. Show exact screen trigger, word count, proof reference and model-aware timing. Do not invent observed results, claim an unshown Script Console line, or silently treat successful structural CI as ZAP proof. Produce `narration-final.json` in the supplied schema and `narration-final.md` with the exact words to speak and Editor sync notes. Leave CQA approval fields false until independently verified. Return those files, preserving the input demo ID and SHA.

**Only the actual produced narration files from that follow-on task** are imported into the portal. A generated script cannot claim UI evidence it never saw. Preserve the approved narration across source changes only if the proof remains identical; otherwise regenerate and revalidate.

## ElevenLabs — copy exactly the model-compatible text

Open a demo → **Narrator** → select the **ElevenLabs model** → click **Copy entire demo narration** (or **Copy selected step**). The copy text is **spoken lines plus supported pause tags only**; source filenames, screen labels, slide labels, text notes and editor instructions are not included in the TTS payload. The initial authored lines are explicitly labeled **unverified drafts** until the later narration skill returns final reviewed text and proof sign-off.

- **Eleven Multilingual v2, Flash v2 and Flash v2.5:** supports `<break time="1.0s" />` for exact one-second *TTS-relative* pauses. Place a pause after Enter and before the result-focused speech, and between result and decision. Long-running scans must be shortened in the video editor while retaining real proof; a one-second tag cannot wait for a script that has not finished.
- **Eleven v3/v4:** does **not** support SSML break tags. Use the supported `[pause]` audio tag and natural punctuation. The pause is not guaranteed to measure exactly one second; the editor creates any exact one-second gap in post-production. Do not paste `<break>` into v3/v4.
- Choose the approved voice/model in ElevenLabs Text to Speech. Paste only the copied text, generate audio, listen for mispronounced rule IDs, ZAP names, Jython, HTTP codes, pacing, false pauses and artifacts. Regenerate any faulty sentence. Export per-demo audio using the approved file naming convention and store it with its matching take manifest. Never fabricate proof from voice or edit the final words after synchronization without another evidence review.

Official model-specific guides:
- https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech
- https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-can-i-add-pauses

## Technical CQA and provenance rules

The Developer's `manifest.json`, `steps-and-output.md`, `logs/`, and real source SHA determine whether terminal execution succeeded. This is **not** a claim of GUI/browser/Actions proof. `narration-final.json` does not self-approve anything: verify its `reference_sha`, named commands, take ID, current GUI/Actions media, actual field/value agreement and sign-off metadata. The portal says HOLD when fields/logs are unavailable or output contracts fail. Author-only files must move into private storage before learner publication; public dot directories remain visible in Git history even after deletion.

## Approved production order — narrator before editor

**Developer → Recorder → Narrator → Editor → Technical CQA.** The Narrator supplies the exact final spoken lines for the Recorder's visible evidence; the Editor then uses those lines to place the blue result frame, pink on-value label, purple relationship arrow, or short yellow gist callout. The portal's Editor tab shows three narration-to-visual rows under every step. A 12–15-second explanation does **not** require a new callout when another meaningful focus changes during that interval; add one only if the frame would otherwise remain static for longer than 12 seconds.

## Navigation cannot depend on manual folder browsing

The default Mac checkout used by this course is `~/pluralsight-script-development-with-zap`. Every step shows the exact application to open manually and a **copyable** `cd "$HOME/pluralsight-script-development-with-zap/demos/..."` command. Open the indicated VS Code integrated Terminal or macOS Terminal, paste the directory command, press Enter, then execute that step's single approved `./steps/0N-*.sh` command. The directory command changes the shell's location only; it does not change Git branches, source files, or demo state. If you cloned into a custom path, use the equivalent `cd` path for your actual checkout; do not clone a second repository.

For source files deliberately missing in a `*-before` starter, create the approved source through the student exercise **before** running the named command. The portal links to the starter directory instead of a nonexistent source file. When working in the demo, use `git branch --show-current` to verify the approved `mN-demoM-before` branch; do not film setup or branch switching as one of the four named teaching steps.

## Editor — Camtasia sequence keyed to the narrator

1. **Before Enter:** Keep source context and `./steps/0N-*.sh` in the recorded view. Cut typing mistakes and waits. Use a single blue region outline around the relevant source/command for up to ~8 seconds. Do not cover the command with text.
2. **After completion:** Cut to actual output, never a fabricated terminal sample. Move the **same blue region outline** around the relevant result table (not the whole desktop). Hold 6–8 seconds while the Narrator explains the cause or mechanism.
3. **Exact value:** Inside the region, add a short readable **Transform Pink `#FF1675`** label/underline exactly next to the real `ruleId`, `riskdesc`, `pluginid`, HTTP status, parameter, or exit value indicated by that step's current log. For Module 1 Demo 1, `40018` versus `40022` is a source-defined possibility, *not a value to draw unconditionally*. Use the value that really appeared. If it did not appear, remove the annotation and HOLD.
4. **Relationship:** When the Narrator explains two real values, remove the previous pink label and use a slim **Purple `#770EF7`** arrow between them, with one focus at a time. An arrow must connect content that is visible in the **same actual take**.
5. **Long still view:** When narration remains on an otherwise unchanged frame longer than 12 seconds, show the step's **Yellow `#FFC942`** short crux callout with Inky Blue text. Let it sit around 6–8 seconds, then remove. When the source/output/label/arrow changes already provide motion during the explanation, **no extra callout is necessary**. Do not use a spotlight effect.
6. **Exit and verification:** Remove every box/label/arrow as soon as its target scrolls or the pane switches. End with actual observed result, response or gate status, and source-linked operator decision. Leave 8-second raw handles around significant clicks, trim long scans or idle screens, and synchronize to the final Narrator beat before freezing.

## Narrator — prompt-ready machine handoff

The batch ZIP is not merely a report. It contains each demo's **`narration-handoff.json`**, `NARRATION_HANDOFF.md`, `narration-final.TEMPLATE.json`, normalized terminal transcripts, *unaltered* raw logs, source/branch/SHA, exact navigation and named commands, the approved learning objective, and per-step visual targets. It also includes `NARRATOR_NEXT_SESSION_PROMPT.md` in the root.

Transfer the **entire batch ZIP** and the separate Rupesh teaching-style, narration, and Distributed Demo Production skill packages to the Narrator's chat. That session must produce one `narration-final.json` and one `narration-final.md` per demo. These are external evidence-reviewed outputs, **not** invented automatically by the Developer script. Copy them into the matching `mN-demoM/` folder and run `./refresh.sh` to rebuild the locally hosted course portal. A revised line invalidates its previous Editor timeline until revalidated against the same footage.

In ElevenLabs, select the actual supported model before copying. The default preflight draft is **not final**. Only paste the voice payload generated for that model, without the role labels or notes. Multilingual v2/Flash v2 supports `\<break time="1.0s" /\>`; Eleven v3/v4 support `[pause]` but cannot promise a one-second duration. Playback and final video synchronization remain a separate Technical CQA gate. See https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-can-i-add-pauses.
