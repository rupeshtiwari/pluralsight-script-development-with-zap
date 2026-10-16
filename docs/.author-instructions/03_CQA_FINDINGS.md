# Technical CQA: Source-Level Proof Gaps

These are source-level findings, **not authorization to alter frozen demo code**. Confirm them with current live evidence and the latest approved outline.

| Demo / step | Finding | Required visible proof |
|---|---|---|
| M1 Demo 1 / 4 | **Source corrected:** ordinary ping was not sufficient; the existing Step 4 now sends a harmless injected shell marker to the authorized training app and fails if that marker is absent. Runtime remains UNVERIFIED | Show the actual `ZAP_CMD_PROOF` response and its original injected host request, then reconcile the ZAP alert |
| M1 Demo 1 / 2 | Reflecting input does not automatically demonstrate browser execution of XSS | Real context-specific payload with request/response; do not claim a browser execution was observed if not shown |
| M1 Demo 2 / 3 | Terminal preflight validates source `print` and proxied request, not ZAP's Script Console stream | Real `[globo-marker]` line visibly emitted in Script Console for the fresh request |
| M1 Demo 3 / 2 | Training login takes username without realistic password flow | Label as deliberate lab simplification, not a secure production auth recipe |
| M2 Demo 1 / 3 | Plan may show scripts loaded but not each distinct side effect | Real marker-bearing request as needed; named Python alert belongs to the authenticated scan |
| M2 Demo 2 / 4 | Insights are separate scan-quality evidence, not vulnerability alerts | Real official report `insights[]` content and meaningful entries |
| M2 Demo 3 / 3 | **Source corrected:** the current `_steps.sh` requires exit code `1` and a positive High alert count; runtime still unverified | Show actual exit `1`, genuine High alert in report and blocked GitHub Actions job |
| M2 Demo 3 / 4 | **Source corrected:** the current `_steps.sh` fails if the report lacks either real finding; runtime still unverified | Actual rule `10021` False Positive and `40012` High in the same report |

Use current ZAP documentation as the technical reference: `https://www.zaproxy.org/docs/desktop/addons/automation-framework/` and `https://www.zaproxy.org/docs/desktop/addons/alert-filters/automation/`.

**Recording release:** Under owner's 95%-and-above content acceptance policy, content may be frozen while runtime proof remains pending. Never upgrade source-review confidence to a claim of runtime verification. Fix an actual blocker only with explicit approval to unfreeze the affected step.
