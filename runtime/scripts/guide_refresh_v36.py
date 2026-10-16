#!/usr/bin/env python3
"""One-off v3.6 editorial migration. Reuses frozen commands and expected tables.

Run deliberately with --apply; never silently rewrite author prose on each push.
No execution proof, reviewer score or approval is manufactured here.
"""
from __future__ import annotations
import argparse
import html
import importlib.util
import json
import re
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
HEADINGS = {
    'The small problem to solve': 'Learning Goal', 'The specific problem': 'Learning Goal',
    'Where to go': 'Demo Workspace', 'Which application and screen?': 'Demo Workspace',
    'Run this exact command': 'Run Command', 'What the script prints': 'Expected Results',
    'Expected output and what it means': 'Expected Results',
    'What you should understand': 'Interpret Results', 'How to interpret this result': 'Interpret Results',
}
# Only learner promises are rewritten. The existing technical four-step bodies remain.
STORIES = {
'm1-demo1': (
    'You are reviewing a security scan for the Globomantics Store. A long alert list does not tell you which input is unsafe or whether a finding is reproducible. Your team needs a request, response and application effect it can investigate.',
    'I will guide you through one focused investigation. You will narrow SQL, MongoDB and command-injection checks, inspect XSS output contexts, test CSRF session ownership, and record evidence-backed dispositions.',
    'After completing the four checks and inspecting the required evidence, you can explain which input crosses each unsafe boundary. You can distinguish an alert from confirmation, show the token/session failure, and support a disposition with the actual request and response.', 6),
'm1-demo2': (
    'You need to distinguish authorized security-test traffic from normal Store requests. Saving a JavaScript file does not prove ZAP modified a message. You must show the hook, the outgoing header and its live diagnostic line.',
    'I will guide you from the HTTP Sender template to a reusable request marker. You will write and register the hook, inspect a modified request, verify the live Script Console output, and confirm the enabled script identity.',
    'After all four checks and the live Script Console inspection, you can extend ZAP at the HTTP Sender hook and prove an actual message was changed. You can reuse the saved script name and path without confusing current registration with persistence after container teardown.', 5),
'm1-demo3': (
    'Your custom security check needs a protected Store profile, but an unauthenticated scanner cannot reach it. You need separate scanning and login scripts, and evidence that ZAP used the authenticated session.',
    'I will guide you through a Jython-compatible active rule and a separate authentication script. You will compare denied and authenticated profile access, then require a fresh alert from your named custom rule.',
    'After the four checks, you can separate a scanning rule from authentication, prove protected-page coverage and distinguish a new custom alert from an old or built-in finding. You also know the username-only training login is not a production authentication design.', 6),
'm2-demo1': (
    'Your team needs the Store security checks on a hosted build runner. A successful local scan or a green workflow badge alone does not establish that the intended authenticated custom check ran.',
    'I will guide you through headless ZAP execution, the authenticated context, reuse of the existing scripts and the named custom alert. You will link the hosted job and report to the exact source commit.',
    'After the local checks and matching hosted run, you can explain how the Automation Framework binds user, authentication and scope, then prove the pipeline produced the intended custom finding. You can reject a stale report or a built-in alert offered as a substitute.', 5),
'm2-demo2': (
    'You need machine-readable evidence from a completed authenticated Store scan. An alert count or screenshot cannot tell your release process whether it is reading the right engine, finding and report.',
    'I will guide you through four API evidence checks: runtime and scan status, the named custom alert, the official JSON report and report-owned Insights. You will compare the actual fields rather than assume different artifacts agree.',
    'After the four checks, you can inspect ZAP programmatically, distinguish risk from confidence, and reconcile a report with the API. You can use actual Insights to discuss scan effectiveness, including operational failures, without replacing missing Insights with unrelated counters.', 5),
'm2-demo3': (
    'Your team has reviewed one benign header finding, but genuine High-risk reflected XSS must still stop the release. A failed build is not enough: the report must explain the policy decision.',
    'I will guide you through a narrowly scoped False Positive filter, job ordering, the real gate exit and the final report. You will preserve the genuine High-risk finding while checking the intended exception.',
    'After the four checks and matching gate evidence, you can explain why a release was blocked using the filtered report and actual process exit. You can separate a reviewed exception from blanket suppression and a security gate decision from an infrastructure failure.', 6),
}
# Proof instructions are concrete; values below are identifiers or expected contracts,
# not assertions that this session observed a successful run.
PROOF = {
'm1-demo1': [
('VS Code integrated Terminal', 'Stay in the same terminal for the scan table. Then open the browser at http://localhost:8080/zap/; select Alerts and each current SQL, MongoDB and command finding. Open its Request and Response views.', 'Rule identity and the corresponding q, username or host parameter; capture the actual risk and confidence plus affected URL'),
('VS Code integrated Terminal', 'After the terminal context check, switch to http://localhost:8080/zap/; select History, the matching /greet request, then Request and Response. Match the injected name value to the output context.', 'Exact injected payload, name parameter and reflected response; do not call reflection browser execution'),
('VS Code integrated Terminal', 'Stay in the same terminal. Keep the valid-token control, missing-token control, cross-session request and before/after email rows visible together. The browser form at http://localhost:8000/account/email is context, not proof of the shell session.', 'Actual HTTP states and account email mutation from the same test; explain session ownership rather than claiming a single-use-token test'),
('VS Code integrated Terminal', 'Stay in the same terminal for the disposition rows. Use http://localhost:8080/zap/ Alerts and the corresponding Request/Response to corroborate the current finding; open docs/alert-disposition-template.md in VS Code to record the reviewed decision.', 'Database error, changed account count, harmless injected shell marker and XSS request/response; normal ping is not injection proof')],
'm1-demo2': [
('VS Code integrated Terminal', 'Stay in the terminal for registration output. Then open http://localhost:8080/zap/ and select Scripts, HTTP Sender, globomantics-marker.', 'Actual name, detected JavaScript engine and enabled registration; declared marker format is not yet observed traffic'),
('VS Code integrated Terminal', 'Run in the terminal, then switch to http://localhost:8080/zap/. Select History, the newest /greet?name=marker- request matching this take, then Request.', 'Actual X-Globomantics-Marker header and its value in that captured request'),
('VS Code integrated Terminal', 'Trigger the request in the terminal; then switch to http://localhost:8080/zap/ and open Scripts, Script Console. Select the fresh line with the matching request URL.', 'Fresh [globo-marker] line from the GUI; the terminal EXPECTED-format line does not count as console proof'),
('VS Code integrated Terminal', 'Inspect terminal registration fields; then return to http://localhost:8080/zap/, Scripts, HTTP Sender, globomantics-marker.', 'Registered name, type, engine and enabled state from the same live ZAP session')],
'm1-demo3': [
('VS Code integrated Terminal', 'Show the completed active-rule source in VS Code before execution; after terminal registration, switch to http://localhost:8080/zap/, Scripts, Active Rules.', 'Actual loaded Jython rule, custom alert name and scan/alert-creation logic; loading is not a finding'),
('VS Code integrated Terminal', 'Show the separate authentication source in VS Code; after terminal registration switch to http://localhost:8080/zap/, Scripts, Authentication.', 'Login submission and registered script identity; explicitly bound the simplified lab login'),
('VS Code integrated Terminal', 'Stay in the terminal for denied and authenticated profile requests and the authentication trace. Then show http://localhost:8080/zap/, Globomantics context, Users, Alice when verifying context state.', 'Real protected-profile HTTP responses and ZAP script execution, not a manually supplied shell cookie'),
('VS Code integrated Terminal', 'Show absent-before and fresh-after terminal evidence. Switch to http://localhost:8080/zap/, Alerts, and select the newly named custom alert on /account/profile.', 'Fresh custom name, note parameter, risk and response evidence; built-in XSS is not equivalent')],
'm2-demo1': [
('VS Code integrated Terminal', 'The local result stays in Terminal. For required hosted proof, open https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/actions/workflows/zap-authenticated-scan.yml, select the matching branch/SHA run, authenticated-scan job, and headless execution step.', 'Actual hosted runner log, launch command and exact commit; a printed local Runner (CI) label is only configuration'),
('VS Code integrated Terminal', 'Stay in VS Code with ci/af-plan.yaml and the integrated terminal. Show env.contexts, script authentication, user alice and included paths.', 'Context, authentication method, user and target scope; configuration alone is not a login success'),
('VS Code integrated Terminal', 'Show local fields, then the same hosted authenticated-scan run and protected-profile request/report. Keep the script jobs and requestor configuration accessible in VS Code.', 'Reused script names and authenticated coverage; a loaded sender needs separate header evidence to prove its mutation'),
('VS Code integrated Terminal', 'After the local check, open the same hosted run, Artifacts, globo-ci-report; download and open the JSON in VS Code. Keep the run SHA available, not a historical report.', 'Named custom finding, protected URL, note parameter and actual rating in that hosted report')],
'm2-demo2': [
('macOS Terminal', 'Stay in the same terminal after the command. No ZAP GUI switch is required for the API status proof.', 'Current engine version, active scan identity and actual completed progress/state'),
('macOS Terminal', 'Stay in the same terminal. Show the API query context and custom alert fields; inspect raw JSON only when teaching its structure.', 'Custom plugin identity, affected parameter, risk and confidence as distinct fields'),
('macOS Terminal', 'Stay in the terminal for the generated report fields; show official report JSON when comparing nested fields. Compare to the API result already captured in this take.', 'Same custom identity, scope and rating; investigate any mismatch rather than assuming freshness'),
('macOS Terminal', 'Stay in the terminal and show actual report insights[] entries with their explanations. No browser tour is required.', 'Real insight key, statistic and meaning, including operational failures; empty Insights is HOLD')],
'm2-demo3': [
('VS Code integrated Terminal', 'Stay in VS Code with ci/gate-plan.yaml and the terminal fields. Frame alertFilter, ruleId, newRisk and scoped URL.', 'Configured 10021 False Positive exception and exact scope; whether it took effect is proved in the report'),
('VS Code integrated Terminal', 'Stay in VS Code and the integrated terminal; scroll only to the ordered YAML jobs.', 'alertFilter before scanning, report before exitStatus and exitStatus last for this plan'),
('VS Code integrated Terminal', 'Show local High count and process exit. Then open https://github.com/rupeshtiwari/pluralsight-script-development-with-zap/actions/workflows/zap-quality-gate.yml, select the matching run, quality-gate job and execution log.', 'Real High finding plus exit 1 and the corresponding blocked hosted step; distinguish scanner errors'),
('VS Code integrated Terminal', 'Show local report fields. For hosted proof, open the same Actions run, Artifacts, globo-gate-report; download and open the JSON in VS Code.', 'Actual 10021 False Positive and 40012 High from the same report, aligned with the gate exit')],
}


def load_plan(root: Path):
    spec = importlib.util.spec_from_file_location('course_plan', root/'setup/production_plan.py')
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def overall(scores):
    if len(scores) != 4 or any(x is None for x in scores):
        return None
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not 0 <= x <= 100 for x in scores):
        raise ValueError('Four numeric scores between 0 and 100 are required')
    return round(mean(scores), 2)


def managed(text: str, name: str, body: str, before: str | None = None) -> str:
    start, end = f'<!-- {name}:start -->', f'<!-- {name}:end -->'
    block = start+'\n'+body.strip()+'\n'+end+'\n'
    rx = re.escape(start)+r'.*?'+re.escape(end)+r'\n?'
    if start in text:
        return re.sub(rx, lambda _: block, text, flags=re.S)
    if before:
        if before not in text:
            raise ValueError('Missing insertion anchor '+before)
        return text.replace(before, block+'\n'+before, 1)
    return text.rstrip()+'\n\n'+block


def learning_intro(text, demo):
    scenario, goal, _, _ = STORIES[demo]
    rx = r'^## (?:The problem you are solving|Your Scenario)\n.*?(?=^## )'
    section = '## Your Scenario\n\n'+scenario+'\n\n**Your practical goal:** '+goal+'\n\n'
    text, n = re.subn(rx, lambda _: section, text, count=1, flags=re.M|re.S)
    if n != 1:
        raise ValueError(demo+': missing scenario section')
    return text


def student(text, demo, folder):
    text = learning_intro(text, demo)
    for old, new in HEADINGS.items():
        text = text.replace('### '+old+'\n', '### '+new+'\n')
    for old, new in {
        'What you will learn in this demonstration': 'Your Learning Goals',
        'Follow the evidence': 'Your Evidence Path',
        'From setup to a defensible decision': 'Your Evidence Path',
        'Start the local demo': 'Start Your Lab', "Start the demo's application": 'Start Your Lab',
        'The four teaching steps': 'Your Four Steps', 'Complete the four demo steps': 'Your Four Steps',
        'Finish and clean up': 'Finish Your Lab', 'Complete the exercise': 'Finish Your Lab',
    }.items():
        text = text.replace('## '+old+'\n', '## '+new+'\n')
    # Make the startup code independent of the reader's previous working directory.
    text = text.replace('```bash\ngit fetch origin\n', '```bash\ncd "$HOME/pluralsight-script-development-with-zap"\ngit fetch origin\n')
    parts = re.split(r'(?=<summary><b>Step [1-4](?::| —))', text)
    if len(parts) != 5:
        raise ValueError(demo+': expected four student cards')
    for i in range(1, 5):
        terminal, location, evidence = PROOF[demo][i-1]
        body = '**Run in:** '+terminal+'.\n\n```bash\ncd "$HOME/pluralsight-script-development-with-zap/'+folder+'"\n```\n\n'
        parts[i] = managed(parts[i], 'student-location', body, before='### Run Command')
        body = '**Where your result appears:** '+location+'\n\n**Inspect this evidence:** '+evidence+'.'
        parts[i] = managed(parts[i], 'student-proof', body, before='### Expected Results')
    text = ''.join(parts)
    closing = '## What You Achieved\n\n'+STORIES[demo][2]+'\n\n**Your final check:** Explain the result using your own captured evidence. A README example, missing result or earlier run does not satisfy this exercise.'
    text = managed(text, 'student-achievement', closing, before='## Finish Your Lab')
    return text


def narrator_words(text):
    # Only the three-cell speech rows; never count editor directions as spoken words.
    rows = re.findall(r'<tr>\s*<td>[^<]*</td>\s*<td>([^<]*)</td>\s*<td>\d+(?: spoken words)?</td>\s*</tr>', text)
    return sum(len(html.unescape(x).split()) for x in rows)


def author(text, demo, folder):
    parts = re.split(r'(?=^## Step [1-4]\b)', text, flags=re.M)
    if len(parts) != 5:
        raise ValueError(demo+': expected four author cards')
    minute_budget = STORIES[demo][3]
    block_seconds = minute_budget*60//4
    target = 774 if minute_budget == 6 else 644
    count = narrator_words(text)
    summary = (
        '## Demo Readiness\n\n'
        f'**Approved duration:** {minute_budget} minutes. **Execution steps:** four, unchanged. '
        f'**Acceptance target:** overall review score at least 98/100.\n\n'
        '| Step | Current evidence-backed score | Blocking review |\n|---|---|---|\n'+
        '\n'.join(f'| {i} | Not assessed | Matching Mac take, required GUI/Actions proof and final spoken coverage |' for i in range(1,5))+
        '\n\n**Overall confidence:** NOT ASSESSED. Once all four step scores are supported, calculate '
        '`(step1 + step2 + step3 + step4) / 4`; do not average only the reviewed steps. '
        'A missing critical proof keeps release on HOLD even when the average reaches 98.\n\n'
        f'**Speech budget:** current short-form draft {count} whitespace words; final {minute_budget}-minute target {target} spoken words under the owner contract. '
        f'Remaining before final audio validation: {max(0,target-count)} words. '
        'This draft is not a complete timed recording script. Expand useful source/action/result teaching within the same four steps; do not fill time with invented stories.\n\n'
        f'**Recording budget:** approximately {block_seconds} seconds per step, including source work, execution and proof. '
        'This is an editing plan, not a measured duration or a reason to leave a static screen.\n\n'
        '**Review method:** assess LO and outline coverage, technical correctness, example quality, learner clarity, '
        'operator decision-making and recorded proof against the exact source SHA. Record the reviewer, rationale and evidence for every numeric score. '
        'Old 88–96% source estimates lacked a documented common rubric and are retired, not promoted.'
    )
    parts[0] = managed(parts[0], 'demo-readiness', summary)
    for i in range(1,5):
        terminal, location, evidence = PROOF[demo][i-1]
        body = (
            '<table><tr><th>Capture moment</th><th>Exact action and result location</th></tr>'
            '<tr><td>Before Enter</td><td>Use '+html.escape(terminal)+'. Show the named step command already provided below/above; '
            'keep its full filename readable for about eight seconds. Directory and branch setup are off camera.</td></tr>'
            '<tr><td>After Enter</td><td>'+html.escape(location)+'</td></tr>'
            '<tr><td>Evidence to record</td><td>'+html.escape(evidence)+'. Hold each meaningful field for six to eight seconds; retain the matching raw log and take ID.</td></tr>'
            '<tr><td>Meaning and decision</td><td>Use the Spoken Narration for this exact field, then explain whether the evidence is enough to proceed. '
            'If it is absent, stop: neither a source declaration nor an expected output is an observed result.</td></tr>'
            '<tr><td>Editor handoff</td><td>Mark the result region, then the actual value being explained. Clear old overlays on pane change. '
            'During an otherwise still explanation beyond 12 seconds, use one relevant 6–8-second takeaway callout; never invent a successful result.</td></tr></table>'
        )
        parts[i] = managed(parts[i], 'capture-location', body, before='### Recorder Shots')
        parts[i] = re.sub(r'^- \*\*Source (?:confidence|review):\*\*.*\n?', '', parts[i], flags=re.M)
        parts[i] = re.sub(r'^- \*\*(?:Release|Final release):\*\*.*$',
                         '- **Release:** HOLD until evidence review; target overall score 98/100, never automatic approval', parts[i], flags=re.M)
    return '\n'.join(p.rstrip() for p in parts)+'\n'


def migrate(root: Path, apply=False):
    plan = load_plan(root)
    changes = {}
    for demo, folder in plan.LAB_DIRS.items():
        for path, transform in [(root/folder/'README.md', student),
                                (root/'docs/.author-instructions'/f'{demo}.md', author)]:
            old = path.read_text(encoding='utf-8')
            new = transform(old, demo, folder)
            # Never alter the actual numbered commands or narration strings here.
            commands = lambda s: re.findall(r'^\./steps/0[1-4]-[^\s]+', s, re.M)
            if commands(old) != commands(new):
                raise ValueError('Numbered command drift: '+str(path))
            if old != new:
                changes[str(path.relative_to(root))] = new
    if apply:
        for path, value in changes.items():
            (root/path).write_text(value,encoding='utf-8')
    print(json.dumps({'changed_paths':list(changes),'applied':apply,'runtime_verified':False},indent=2))
    return changes


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--apply',action='store_true')
    p.add_argument('--root',type=Path,default=ROOT)
    args=p.parse_args()
    migrate(args.root.resolve(),args.apply)
