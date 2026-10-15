# M2-DEMO2 — ZAP API Evidence and Insights

**Approved LO:** EO3b  
**Operator problem:** Maya needs structured scan evidence a pipeline can consume and reconcile with an archived report.  
**Demo folder:** `demos/module2-demos/m2-demo2-zap-api-scan-evidence`  
**Branch pair:** `m2-demo2-before` and `m2-demo2-after`  
**Primary UI:** Terminal only; ZAP API localhost:8090 and generated traditional-json report  
**Architecture diagram:** `docs/learner-diagrams/m2-demo2-architecture.svg`

## Run Preparation

From the repository root, run `./setup/setup-macos.sh` on a target Mac once, select the assigned branch, enter `demos/module2-demos/m2-demo2-zap-api-scan-evidence` and follow its README setup command. Then run `./scripts/preflight_check.sh` and retain the timestamped `logs/` evidence. The local preflight is **not** equivalent to GitHub Actions proof when a hosted artifact is the outline requirement. Record a fresh take and reconcile evidence to the exact SHA and command.

## Step 1: check zap scan status — EO3b

**Real-world problem:** A pipeline must distinguish scanner readiness from scan completion

**Exact command from demo directory:**

```bash
./steps/01-check-zap-scan-status.sh
```

**Recorder:** Execute named status command; this demo provisions its own authenticated scan when absent. Hold the full legible command for 8–10 seconds before Enter. Highlight Highlight `core/view/version`, `ascan/view/scans`, finished/progress and actual request count. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** ZAP 2.17.0 version and truly finished scan status from HTTP API. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** Machine-readable completion controls when findings become trustworthy. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 95%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Step 2: query custom rule alert — EO3b

**Real-world problem:** A gate cannot act on a generic count; it needs specific rule identity

**Exact command from demo directory:**

```bash
./steps/02-query-custom-rule-alert.sh
```

**Recorder:** Query `core/view/alerts` and inspect named Python script finding. Hold the full legible command for 8–10 seconds before Enter. Highlight Focus on `pluginId 50000` plus custom name, Medium risk/confidence and parameter `note`. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** Actual script-generated alert returned by API against authenticated profile. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** Rule identity and disposition prevent confusing a built-in alert with the custom script. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 95%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Step 3: reconcile json report — EO3b

**Real-world problem:** Archived security evidence can drift from the current API state

**Exact command from demo directory:**

```bash
./steps/03-reconcile-json-report.sh
```

**Recorder:** Invoke official reports API for `traditional-json` then compare finding. Hold the full legible command for 8–10 seconds before Enter. Highlight Focus on alert name, `pluginid`, `riskdesc` and report path. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** Current report carries same custom alert and rating as previous live API response. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** Reconcile point-in-time report against current results before preserving artifacts. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 95%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Step 4: read zap insights — EO3b

**Real-world problem:** An alert result may be unreliable if the scan had operational failures

**Exact command from demo directory:**

```bash
./steps/04-read-zap-insights.sh
```

**Recorder:** Inspect actual report `insights[]` via named command. Hold the full legible command for 8–10 seconds before Enter. Highlight Focus on actual `level`, `key`, `statistic` and explanatory field. Show actual output, click target and resulting state, with 8-second handles around a significant click. Record exact source line and scroll/pane position.

**Required evidence:** Nonempty real report Insights; missing Insights is failure, not generic statistics fallback. Do not infer confirmation from a static YAML snippet, historic run or a successful upload alone.

**Narrator's distinct teaching focus:** Operational scan health and vulnerability risk answer different questions. Speak naturally for ElevenLabs, ground every claim in the recorded job/report value and avoid repeating other steps. Write ~18–22 words for the command hold; continue only while proof is visible.

**Editor:** Cut on focus transitions; show command or YAML key, actual response/report, then decision. Remove stale callouts. Preserve the exit code and exact alert text long enough to read, not a speculative overlay.

**Source-review confidence:** 90%, **runtime not verified by this playbook**. The owner's content threshold is 95%; this lower result requires actual proof or a narrowly approved correction, not artificial scoring.

---

## Completion gate

Do not claim READY solely because a hosted action shows red or green. Inspect the report and return code, tie them to the exact current branch SHA and authorized Globomantics target, capture screenshot or job artifact ID, and complete Recorder/Narrator/Editor checks. If no live proof is available, mark it NOT VERIFIED and identify the next actual command.
