# Production Handoff — Create Evidence-Locked ZAP Narration

Apply the **Distributed Demo Production skill** and the supplied **Rupesh teaching-style** and **Rupesh teaching-narration** skill references to the attached actual Mac-generated six-demo production batch. The source of truth for content is the approved `docs/course-outline.md` in the matching GitHub revision, and the source of truth for observed results is the provided batch's real step logs plus separately supplied matching-take ZAP GUI or GitHub Actions proof.

## Non-negotiable output

Create, for **each named demo requested**, exactly two files in its existing batch folder:

- `narration-final.json` — conform to that demo's `narration-final.TEMPLATE.json` and `narration-handoff.json` schema. Preserve the `demo`, `reference_sha`, all four step indexes, `command` strings, and exact order; supply separate nonempty `before`, `during`, and `after` natural spoken lines (each at most 27 words), with verified real request/response or alert evidence where that claim is made. Keep `quality_checks.cqa_approved` false until the actual same-take evidence is independently checked.
- `narration-final.md` — ready to record: per-step exact spoken lines, BEFORE command trigger, result/field DURING trigger, AFTER operator consequence, actual proof file references, word counts, demonstrated LO, and distinct Editor sync instructions. Include a separate **whole-demo voice payload** for the selected ElevenLabs model that includes only spoken words and model-compatible pause tags. Never mix narrator metadata with copyable speech.

Use the **real** observed fields in the JSON handoff. For a ZAP Script Console assertion, require an actual Script Console capture. For GitHub Actions assertions, require an actual workflow run/artifact from the same approved SHA. For XSS browser execution, require execution evidence or explicitly teach only reflection and alert investigation. For the CI gate, check both the real remaining High finding and actual process exit. A formatted expected-output table in the student README is not real proof.

Three stage constraints per step: **BEFORE** the user presses Enter, **DURING** examination of the verified command output and relevant GUI, **AFTER** the result to explain the operator decision. Do not verbally pronounce code abbreviations awkwardly; translate to human-spoken names such as `rule four zero zero one eight` only where the subject is an exact ID actually shown. Do not read filenames or command punctuation verbatim unless teaching the meaning of a parameter. Avoid relative clip/module references and the language of slide labels.

For ElevenLabs **Multilingual v2 / Flash v2 or v2.5**, export `\<break time="1.0s" /\>` between the three phases. For **Eleven v3 / v4**, export `[pause]` instead; it has approximate length, so the Editor must time video cuts independently. Tags must not be nested in individual raw spoken beat fields; the portal creates them on export. Check the official pause documentation.

If any user-supplied file contradicts approved slide content, source code, or the actual recording, report HOLD and the exact mismatch before finalizing speech. Do not create a fictional video result, invent a new endpoint, change command order, alter branch choreography, or approve missing evidence to reach an arbitrary numeric confidence score. The final narration must sound like a calm experienced operator guiding another professional.

Return the two files for the matching demo(s) and have the production team place them in the **original batch folder**, then run `./refresh.sh` and use the Narrator/Editor tabs to align audio, overlays, and video.
