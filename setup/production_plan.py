#!/usr/bin/env python3
"""Approved display choreography: concrete ZAP output labels, no specimen values.

These labels are matched to live captured terminal fields; absence remains a HOLD.
The plan guides overlays and never manufactures security results or video footage.
"""
from __future__ import annotations

REPO_URL = 'https://github.com/rupeshtiwari/pluralsight-script-development-with-zap'
LAB_DIRS = {
'm1-demo1':'demos/module1-demos/m1-demo1-targeted-injection-xss-csrf',
'm1-demo2':'demos/module1-demos/m1-demo2-javascript-http-sender',
'm1-demo3':'demos/module1-demos/m1-demo3-python-scanning-authentication',
'm2-demo1':'demos/module2-demos/m2-demo1-authenticated-zap-github-actions',
'm2-demo2':'demos/module2-demos/m2-demo2-zap-api-scan-evidence',
'm2-demo3':'demos/module2-demos/m2-demo3-security-quality-gates'
}
LO = {
'm1-demo1':'EO1a Configure specialized SQL, NoSQL and command-injection scanners; EO1b validate context-specific XSS; EO1c test CSRF token bypass',
'm1-demo2':'EO2a Develop a JavaScript HTTP Sender script to extend ZAP',
'm1-demo3':'EO2b Implement a custom Python/Jython scanning rule; EO2c automate a scripted authentication sequence',
'm2-demo1':'EO3a Configure headless ZAP execution in GitHub Actions',
'm2-demo2':'EO3b Implement ZAP API-based scanning and evidence reconciliation',
'm2-demo3':'EO3c Enforce threshold-based quality gates for security findings in CI'
}
# Each entry: visual area, first exact output label, second exact output label,
# pointer from / to, temporary on-screen callout (editor-only, NOT speech).
PLAN = {
'm1-demo1':[
('Focused rule results covering SQL, MongoDB and command endpoints','SQL injection · /search (q)','NoSQL injection · /api/account (username)','SQL parameter → NoSQL parameter','Different inputs reach different execution boundaries; validate the matching request'),
('ZAP XSS context map and matched request/response fields','Payload ZAP injected','Evidence (reflected in the response)','Injected payload → reflected response','A reflection is a clue; confirm the right execution context'),
('CSRF test outcomes plus session B email before/after','token from session A, submitted with session B\'s cookie','session B\'s email after the cross-session request','Cross-session token outcome → changed email','A token must be bound to the session that owns it'),
('Four alert-disposition rows and corresponding application observations','40018 SQL injection · /search','40033 NoSQL injection · /api/account','Alert classification → observed input behavior','Disposition requires a request and application evidence, not just an alert count')],
'm1-demo2':[
('Script registration and marker declarations','Marker header it adds','Named console line it prints','Header constant → planned console marker','Registration enables request mutation; the file alone does not'),
('ZAP History outbound request and newly added header','Header added by the script','Outbound request','Marker header → exact captured request','A real outbound request proves the HTTP Sender hook ran'),
('Live ZAP Script Console; NOT an expected-format terminal line','Expected format (verify live ZAP Script Console)','', 'Expected format → separately recorded GUI line','The terminal predicts the line; only fresh Script Console output proves it was emitted'),
('ZAP Scripts tree and enabled registration record','Registered name','Enabled','Registered name → Enabled','Reuse depends on the saved name, engine and enabled state')],
'm1-demo3':[
('Custom active-rule source and the ZAP registration result','Alert it raises','Script name','Rule name → registered alert identity','A named rule must register before it can raise a finding'),
('Authentication source and actual ZAP registration','It submits','Script name','Login request → registered authentication engine','An authenticated scan requires a working session, not only a login file'),
('Protected endpoint unauthenticated vs authenticated responses','Without login','ZAP forced-user (script auth)','HTTP gated → HTTP reachable','A protected page becomes testable only under the scripted user'),
('Fresh custom-scan alert after cleared alert store','Alert','Evidence','Fresh alert → observed response evidence','A current named alert proves the custom rule ran in the authenticated context')],
'm2-demo1':[
('Automation Framework plan and actual GitHub Actions job log','Runner (CI)','Command','Hosted runner → headless launch command','A runner log is stronger proof than a locally displayed plan'),
('Automation Framework authentication environment and scope','Context','Authentication','Context → scripted authentication','Authentication settings determine which endpoints are actually tested'),
('Script job plus authenticated request evidence','Loaded by the plan','Ran authenticated against','Loaded scripts → authenticated request','Loading scripts is not equivalent to proving each side effect'),
('Official authenticated scan report custom-alert record','Alert','Parameter','Named alert → affected authenticated parameter','A built-in rule cannot replace the required custom finding')],
'm2-demo2':[
('ZAP API status response and scan completion','ZAP runtime  (GET core/view/version)','Active scan  (GET ascan/view/scans)','ZAP version → completed scan','A returned status only matters when the active scan is finished'),
('ZAP API custom alert and disposition','Rule identity  (pluginId · alert)','Disposition  (risk · confidence)','Alert identity → risk and confidence','Severity and confidence answer different operator questions'),
('Official traditional-json report fields aligned to the API','Report alert  (pluginid · name)','Report rating  (riskdesc)','Report alert → report risk','The archived JSON must describe the same finding as the live API'),
('Report-owned Insights entries and their explanation','Insight  (level · key)','Statistic · meaning','Insight key → operational meaning','Insights describe scan coverage; they are not another vulnerability alert')],
'm2-demo3':[
('Alert filter plan with rule ID, risk and target URL','Filtered rule  (ruleId)','New disposition  (newRisk)','Filtered rule → False Positive disposition','A narrow rule-level filter should not suppress unrelated alerts'),
('Automation Framework ordered jobs in the YAML plan','Job order (ci/gate-plan.yaml)','exitStatus runs last','alertFilter position → final exitStatus','Filter before scanning; decide only after the final report'),
('Executed gate: risk threshold, real High count and process result','High-risk alerts after filtering','Process exit code  (echo \\$?)','High remaining → nonzero process exit','A failed build is valid only when the report explains the exit code'),
('Report pair showing benign False Positive and remaining High','Benign finding  (rule 10021)','Real finding  (rule 40012)','False Positive record → surviving High','One reviewed false positive never authorizes ignoring the genuine High')]
}
# A scripted runner may evolve a field label intentionally. Never silently
# substitute another row: missing matching fields are flagged to the editor.


# Human-facing, explicit per-step navigation. These steps are authored from
# docs/.author-instructions and the approved demonstration choreography.
# Open an application/pane manually. Navigate directories with the exact cd
# command generated from LAB_DIRS, never via shell transcript guesses.
SCREENS = {
'm1-demo1':[
 ('VS Code','runtime/app/main.py','search, account, admin_ping','Run ./scripts/show_code.sh sqli, ./scripts/show_code.sh nosql, then ./scripts/show_code.sh cmd in the integrated terminal','VS Code integrated Terminal; compare the rule/parameter results and the authorized request/response'),
 ('VS Code','runtime/app/main.py','greet endpoint and HTML body/attribute/JavaScript contexts','Run ./scripts/show_code.sh xss in the integrated terminal; show the relevant output context','Integrated Terminal and matching ZAP History request/response; reflection alone is not browser execution'),
 ('VS Code','runtime/app/main.py','change_email and CSRF token-issuance helper','Run ./scripts/show_code.sh csrf before the named step','Integrated Terminal; keep token/session test states and the resulting account email change visible'),
 ('VS Code','docs/alert-disposition-template.md','alert disposition with runtime/app/main.py source in context','Open the disposition template in the editor; no extra command required','Integrated Terminal; reconcile SQL, NoSQL, command, XSS and CSRF observations, not just an alert count')],
'm1-demo2':[
 ('VS Code','zap-scripts/globomantics-marker.js','sendingRequest(), MARKER_HEADER, MARKER_VALUE, setHeader()','Create or finish the deliberately missing JavaScript file on the before branch before executing','Integrated Terminal; then ZAP Scripts → HTTP Sender script registration'),
 ('ZAP GUI + VS Code Terminal','zap-scripts/globomantics-marker.js','ZAP History → newest /greet?name=marker-* → Request','Open http://localhost:8080/zap/ full screen and select the newest matching request','Integrated Terminal + actual ZAP History request carrying the header'),
 ('ZAP GUI + VS Code Terminal','zap-scripts/globomantics-marker.js','ZAP Scripts → Script Console','Keep http://localhost:8080/zap/ and Script Console visible for a fresh request','Actual new Script Console line; the terminal EXPECTED format is insufficient proof'),
 ('ZAP GUI + VS Code Terminal','zap-scripts/globomantics-marker.js','ZAP Scripts → HTTP Sender → globomantics-marker','Show script name, engine, enabled state and source path in ZAP','Actual enabled script entry; the terminal source path is corroborating evidence')],
'm1-demo3':[
 ('VS Code + ZAP GUI','zap-scripts/globomantics-active-rule.py','Jython scan(), newAlert() or raiseAlert(); Scripts → Active Rules','Create or complete the Python 2.7-compatible rule in the starter branch','Integrated Terminal plus actual ZAP Scripts registration'),
 ('VS Code + ZAP GUI','zap-scripts/globomantics-auth.py','authenticate(), getCredentialsParamsNames(); Scripts → Authentication','Keep the login script distinct from the active-rule file','Integrated Terminal and actual authenticated-script registration'),
 ('ZAP GUI + VS Code Terminal','zap-scripts/globomantics-auth.py','Globomantics context → Users → Alice','Inspect real authenticated profile access without manually supplying a cookie to shell','Actual protected-profile HTTP status plus logged-in session evidence'),
 ('ZAP GUI + VS Code Terminal','zap-scripts/globomantics-active-rule.py','Alerts → newest custom alert on /account/profile','Clear stale findings, run the command, return to Alerts and select the new named rule','Alert name, plugin identity, parameter and authenticated URL from this run')],
'm2-demo1':[
 ('VS Code + GitHub Actions','ci/af-plan.yaml and .github/workflows/zap-authenticated-scan.yml','GitHub Actions → matching authenticated scan workflow job','Show the local AF plan and hosted run branch/SHA; source and runner are distinct','Actual workflow job log + terminal execution; hosted report is separate evidence'),
 ('VS Code','ci/af-plan.yaml','env.contexts, auth method, user alice and includePaths','Keep the YAML keys visible in the editor before the command','Integrated Terminal; compare configured authenticated context and exact scope'),
 ('VS Code + GitHub Actions','ci/af-plan.yaml','script jobs, requestor, active scan and protected-profile report','Show reused JavaScript/Jython paths and authenticated requestor','Integrated Terminal plus same-run hosted request/report; loading does not prove side effects'),
 ('GitHub Actions + VS Code Terminal','ci/af-plan.yaml','Actions → matching run → Artifacts → globo-ci-report','Keep branch and SHA visible and open real report','Named authenticated custom alert; do not substitute a built-in finding')],
'm2-demo2':[
 ('macOS Terminal','scripts/_steps.sh','core/view/version and ascan/view/scans','Open macOS Terminal; do not open a GUI when the API response is the proof','Actual version and completed active scan progress in terminal'),
 ('macOS Terminal','scripts/_steps.sh','core/view/alerts on /account/profile','Keep the authenticated baseurl, custom rule name and API query visible','Actual alert identity, parameter, risk and confidence; use raw JSON when that structure is the claim'),
 ('macOS Terminal','scripts/_steps.sh','reports/action/generate and traditional-json','Show the generation endpoint and template before execution','Official JSON report; inspect raw JSON only when comparing nested report structure'),
 ('macOS Terminal','scripts/_steps.sh','official report insights[] entries','Show the actual insight key/statistic and the corresponding explanation','Real nonempty Insights; absence is HOLD, not substitute statistics')],
'm2-demo3':[
 ('VS Code','ci/gate-plan.yaml','alertFilter ruleId, newRisk and exact URL','Frame only the scoped filter block','Integrated Terminal; actual rule and False Positive disposition'),
 ('VS Code','ci/gate-plan.yaml','ordered alertFilter, requestor, activeScan, report, exitStatus','Show the YAML jobs list without unrelated panels','Integrated Terminal; confirm filter is before scan and gate is last'),
 ('VS Code + GitHub Actions','ci/gate-plan.yaml','exitStatus configuration; Actions → quality-gate job','Frame errorLevel, warnLevel and matching hosted job SHA','Actual High count, exit code 1 and blocked job; only if observed'),
 ('GitHub Actions + VS Code Terminal','ci/gate-plan.yaml','matching gate report artifact rule 10021 and rule 40012','Open the same-run JSON report and show both entries','Actual False Positive for benign rule plus surviving High reflected XSS, from one report')]
}

def screen_action(demo: str, step: int) -> dict:
    app, source, pane, preparation, proof = SCREENS[demo][step-1]
    return {'application': app, 'source': source, 'pane': pane,
            'preparation': preparation, 'proof': proof}
