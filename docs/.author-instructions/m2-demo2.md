# M2-DEMO2 — ZAP API and Insights · Recorder, Narrator And Editor

<div align="center">
![Recorder](https://img.shields.io/badge/RECORDER-Capture-0284c7?style=for-the-badge)
![Narrator](https://img.shields.io/badge/NARRATOR-ElevenLabs-d946ef?style=for-the-badge)
![Editor](https://img.shields.io/badge/EDITOR-Camtasia-16a34a?style=for-the-badge)

<img src="../learner-diagrams/m2-demo2-architecture.svg" width="100%" alt="Illustrative architecture of ZAP API and Insights"/>

<sub>Illustration · Generated using ChatGPT · Author guidance is temporarily PUBLIC</sub>
</div>

## Operator Goal And Approved Objective

Maya needs to verify finished scan state, identify the exact custom finding, reconcile an official JSON report, and inspect scan-health Insights. These are four distinct operational questions, not a generic dashboard tour.

**Learning objective:** EO3b — Implement ZAP API for programmatic security testing

## Preflight FIRST — Enable Parallel Narration Work

Create a clean reference clone from the completed branch. **The starting branch is the Recorder's student exercise; it may intentionally omit the completed plan.** Use independent checkouts.

```bash
git clone -b m2-demo2-after https://github.com/rupeshtiwari/pluralsight-script-development-with-zap.git ~/zap-m2-demo2-reference
cd ~/zap-m2-demo2-reference
./setup/setup-macos.sh
cd demos/module2-demos/m2-demo2-zap-api-scan-evidence
./scripts/demo_up.sh
./scripts/preflight_check.sh
ls logs/preflight-step-0[1-4].log
```

Expect `5 checks passed, 0 failed` only if all four real named steps passed; narration references must **never** be produced from a failed run. Each named command uses the same actual step engine, with immutable evidence retained in `logs/.producer/`. This transcript is authoritative for **terminal fields**, not an observation of a separate GitHub Actions run or ZAP Script Console. Send the four step-specific logs and the corresponding GitHub/GUI proof to the Narrator. Teardown after evidence capture.

The Recorder clones [`m2-demo2-before`](https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/tree/m2-demo2-before/demos/module2-demos/m2-demo2-zap-api-scan-evidence) independently, follows the demo README, completes missing source if required, and places the four approved preflight reference logs in the matching `logs/` folder before recording.

Set `DEMO_SYNC_MODE=1` and `DEMO_SYNC_PHASE=compare` off-camera. The visible terminal transcript can normalize live request IDs or request counts while saving raw values. **Risk, confidence, alert identity, HTTP status and process exit are never invented or normalized away.** A material mismatch stops the take rather than being hidden in Camtasia.

**Primary screens:** macOS Terminal with ZAP API on localhost:8090; source scripts/_steps.sh; report output. Full screen only; use readable zoom. Hold each complete named command for **8 seconds** before Enter. Hold one evidence region for **6–8 seconds**; no idle final shot longer than ten seconds. Position pointer for ~8 seconds before and hold ~8 seconds after a major click in source footage, then trim in editing. Cut lengthy scanning waits cleanly.

## Step 1 — Ask The API If Scanning Finished

**Problem and operator consequence:** An API endpoint can be reachable while the active scan is incomplete

**Exact command from `demos/module2-demos/m2-demo2-zap-api-scan-evidence`:**

```bash
./steps/01-check-zap-scan-status.sh
```

**Expected terminal fields from the existing script. Examples are illustrative; live values must come from the actual preflight and take:**

```text
ZAP runtime (GET core/view/version): 2.17.0
Active scan (GET ascan/view/scans): id=<live-id> · progress=100% · state=FINISHED
Requests the scan sent: <live count, see raw log>
✔ PASS the API reports the ZAP runtime and a finished scan
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>Terminal: show GET core/view/version and GET ascan/view/scans in scripts/_steps.sh; then full named command</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/01-check-zap-scan-status.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Box version 2.17.0 first</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Move callout to FINISHED and 100%; do not narrate a guessed request count</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Query ZAP's version and scan status before processing any finding. An accessible engine does not prove the assessment finished.</td><td>19</td></tr>
<tr><td>Actual output A</td><td>The API reports full progress and a finished scan. These are machine-readable conditions the pipeline can wait for.</td><td>18</td></tr>
<tr><td>Actual output B</td><td>Request counts vary, so read the actual raw measurement. Never invent the count from an unrelated successful run.</td><td>18</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>Square the version, then arrow to FINISHED. Keep separate proof frames, each six to eight seconds. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-01.log` and `logs/recorded-step-01.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

**Source-review confidence: 95%**. Do not inflate scores simply because documentation exists; release requires actual technical evidence.

---

## Step 2 — Query The Custom Finding Identity And Disposition

**Problem and operator consequence:** Aggregated alert counts do not identify what the application-specific rule actually found

**Exact command from `demos/module2-demos/m2-demo2-zap-api-scan-evidence`:**

```bash
./steps/02-query-custom-rule-alert.sh
```

**Expected terminal fields from the existing script. Examples are illustrative; live values must come from the actual preflight and take:**

```text
Rule identity (pluginId · alert): 50000 · Globomantics unsafe reflection (custom rule)
Disposition (risk · confidence): Medium · Medium
Parameter: note
✔ PASS the API returns the script-generated alert's rule identity and disposition
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>Terminal: scripts/_steps.sh core/view/alerts with authenticated baseurl; show script-generated record after step</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/02-query-custom-rule-alert.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Box pluginId and complete custom name</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Show risk versus confidence as separate concepts and point to note parameter</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Read the authenticated alert using ZAP's API. The custom rule identity distinguishes the finding from a built-in XSS result.</td><td>19</td></tr>
<tr><td>Actual output A</td><td>Risk describes severity; confidence describes certainty of evidence. The reported finding is rated Medium on both dimensions.</td><td>17</td></tr>
<tr><td>Actual output B</td><td>The note parameter identifies the tested input. This is the specific evidence a release gate can evaluate.</td><td>17</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>Rectangle rule ID, then risk and confidence labels, then note, with each old highlight cleared. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-02.log` and `logs/recorded-step-02.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

**Source-review confidence: 95%**. Do not inflate scores simply because documentation exists; release requires actual technical evidence.

---

## Step 3 — Reconcile The Official JSON Report With The API

**Problem and operator consequence:** Archived report data must match the live API finding

**Exact command from `demos/module2-demos/m2-demo2-zap-api-scan-evidence`:**

```bash
./steps/03-reconcile-json-report.sh
```

**Expected terminal fields from the existing script. Examples are illustrative; live values must come from the actual preflight and take:**

```text
Report template: traditional-json (reports/action/generate)
Report alert (pluginid · name): 50000 · Globomantics unsafe reflection (custom rule)
Report rating (riskdesc): Medium (Medium)
Reconciled with the API: same script-generated alert as the Step 2 alert response
✔ PASS the official JSON report carries the same script-generated alert as the API
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>Terminal: show reports/action/generate and template traditional-json in scripts/_steps.sh; then run named step</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/03-reconcile-json-report.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Highlight traditional-json report template and rule ID</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Arrow from report riskdesc Medium (Medium) to earlier API risk and confidence fields</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Generate ZAP's official JSON report, instead of writing an unverified summary. The template produces an archivable finding record.</td><td>18</td></tr>
<tr><td>Actual output A</td><td>The report contains the same custom rule name and plugin identity returned by the live API.</td><td>16</td></tr>
<tr><td>Actual output B</td><td>Its risk and confidence match the API response. The release team can now reconcile the archived report with scanner evidence.</td><td>20</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>Small box on report name and riskdesc, then remove it at the next focus. Do not show fake report contents. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-03.log` and `logs/recorded-step-03.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

**Source-review confidence: 95%**. Do not inflate scores simply because documentation exists; release requires actual technical evidence.

---

## Step 4 — Inspect The Scan's Operational Insights

**Problem and operator consequence:** A scan can produce findings even when authentication or scanning reliability is poor

**Exact command from `demos/module2-demos/m2-demo2-zap-api-scan-evidence`:**

```bash
./steps/04-read-zap-insights.sh
```

**Expected terminal fields from the existing script. Examples are illustrative; live values must come from the actual preflight and take:**

```text
Insight (level · key): <actual level> · <actual insight key>
Statistic · meaning: <actual numeric value> · <actual meaning>
✔ PASS the report's own Insights section reports scan effectiveness
```

<details open><summary><img src="https://img.shields.io/badge/RECORDER-Screen_%26_Scroll-0284c7"/></summary>
<table><tr><th>Time Handle</th><th>Required Screen Action</th></tr>
<tr><td>Open source · 8s</td><td>Terminal: report insights[] extraction, show an actual nonempty insight key and explanation; run named step</td></tr>
<tr><td>Show command · 8s</td><td>Display full `./steps/04-read-zap-insights.sh` in the terminal. Move pointer away from key text, press Enter once and do not type corrections.</td></tr>
<tr><td>Proof region A · 6–8s</td><td>Box the actual insight level and key, as printed on this run</td></tr>
<tr><td>Proof region B · 6–8s</td><td>Point to statistic and its meaning. If insights[] is empty, show FAIL instead of a substituted counter</td></tr>
<tr><td>Result · 6–8s</td><td>Keep the actual verified PASS or report result in view. Click handles are filmed for 8s before/after but trimmed; long scan waits are edited out.</td></tr>
</table></details>

<details open><summary><img src="https://img.shields.io/badge/NARRATOR-Exact_Spoken_Lines-d946ef"/></summary>
<table><tr><th>Visible Focus</th><th>ElevenLabs Spoken Words</th><th>Word Count</th></tr>
<tr><td>Named command</td><td>Read ZAP's Insights to assess scan effectiveness, not the vulnerability severity of one finding.</td><td>14</td></tr>
<tr><td>Actual output A</td><td>The insight key names an operational condition, while its statistic and explanation show what happened during execution.</td><td>17</td></tr>
<tr><td>Actual output B</td><td>If the report lacks Insights, fail this evidence check. Ordinary statistics cannot substitute for missing scan-quality signals.</td><td>17</td></tr>
</table>
These spoken lines teach only the visible evidence. Never say placeholder values aloud or claim a GUI/API fact a different command did not establish.
</details>

<details open><summary><img src="https://img.shields.io/badge/EDITOR-Precise_Callouts-16a34a"/></summary>
<table><tr><th>Beat</th><th>Exact Camtasia Action</th></tr>
<tr><td>Source → command</td><td>Cut cleanly at window/pane change. Square the relevant config key, remove before introducing the named command.</td></tr>
<tr><td>Proof A/B</td><td>First square actual key, then arrow to explanatory field. Never narrate the placeholder values. Keep one callout at a time for 6–8s, moving to the next value as the narrator speaks.</td></tr>
<tr><td>Final result</td><td>Show observed alert/report/exit and the actual PASSED condition; no fake overlays or stale arrows.</td></tr>
<tr><td>Sync artifact</td><td>Compare `logs/preflight-step-04.log` and `logs/recorded-step-04.log` with the same branch SHA and raw `logs/.producer/` proof. A mismatch is a retake, never a cosmetic correction.</td></tr>
</table></details>

**Source-review confidence: 90%**. Do not inflate scores simply because documentation exists; release requires actual technical evidence.

---

## Editor / Narrator Handoff

Publish the frozen narration reference together with exact branch/commit SHA, four preflight step logs, filmed comparison logs, unmodified raw evidence, GUI or Actions run references, and each spoken line's corresponding video timecode. The author folder is intentionally temporary and publicly visible. Move it to private storage before the learner deliverable is finalized.
