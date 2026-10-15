# Technical CQA: Source-Level Proof Gaps

These are source-level findings, **not authorization to alter frozen demo code**. Confirm them with current live evidence and the latest approved outline.

| Demo / step | Finding | Required visible proof |
|---|---|---|
| M1 Demo 1 / 4 | Normal ping output on `/admin/ping?host=127.0.0.1` alone cannot prove shell-command injection | Actual injected parameter plus response or ZAP's alert request/response |
| M1 Demo 1 / 2 | Reflecting input does not automatically demonstrate browser execution of XSS | Real context-specific payload with request/response; do not claim a browser execution was observed if not shown |
| M1 Demo 2 / 3 | Terminal preflight validates source `print` and proxied request, not ZAP's Script Console stream | Real `[globo-marker]` line visibly emitted in Script Console for the fresh request |
| M1 Demo 3 / 2 | Training login takes username without realistic password flow | Label as deliberate lab simplification, not a secure production auth recipe |
| M2 Demo 1 / 3 | Plan may show scripts loaded but not each distinct side effect | Real marker-bearing request as needed; named Python alert belongs to the authenticated scan |
| M2 Demo 2 / 4 | Insights are separate scan-quality evidence, not vulnerability alerts | Real official report `insights[]` content and meaningful entries |
| M2 Demo 3 / 3 | Gate preflight accepts any nonzero code; does not strictly require exit=1 and actual High | Explicit process exit `1` + report High finding; inspect failed job logs |
| M2 Demo 3 / 4 | Code can show a default fallback 'filtered to False Positive' without real FP item | Actual `10021` riskdesc False Positive and `40012` High in report; fail closed on missing proof |

Use current ZAP documentation as the technical reference: `https://www.zaproxy.org/docs/desktop/addons/automation-framework/` and `https://www.zaproxy.org/docs/desktop/addons/alert-filters/automation/`.

**Recording release:** Under owner's 95%-and-above content acceptance policy, content may be frozen while runtime proof remains pending. Never upgrade source-review confidence to a claim of runtime verification. Fix an actual blocker only with explicit approval to unfreeze the affected step.
