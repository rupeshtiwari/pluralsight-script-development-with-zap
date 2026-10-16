#!/usr/bin/env python3
"""Offline dashboard regression checks. Fixture text is not ZAP runtime proof."""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

P=Path(__file__).with_name('production_dashboard.py')
s=importlib.util.spec_from_file_location('production_dashboard',P)
d=importlib.util.module_from_spec(s);s.loader.exec_module(d)

class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.batch=self.root/'batch';self.batch.mkdir()
        self.auth=self.root/'auth';self.auth.mkdir()
        lab=self.batch/'m1-demo1';(lab/'logs'/'.producer').mkdir(parents=True)
        self.proof='''┌────────────┐\n│ WHAT: fixture testing │\n└────────────┘\n  ★ │ Probe requests the scan sent          │ <live-count-in-raw-log>\n  ★ │ Current status                         │ 200\n  ✔ PASS synthetic fixture only\n'''
        (lab/'logs'/'preflight-step-01.log').write_text(self.proof)
        (lab/'logs'/'.producer'/'reference-step-01.raw.log').write_text('\x1b[38;2;255;22;117mTEST\x1b[0m marker-111111')
        (lab/'steps-and-output.md').write_text('## Step 1 — ./steps/01-named-fixture.sh\n')
        self.row={'demo':'m1-demo1','status':'PREFLIGHT PASSED; GUI/CI REVIEW PENDING',
                  'sha':'0'*40,'startup_exit':0,'preflight_exit':0,'cleanup_exit':0,
                  'step_commands':['./steps/01-named-fixture.sh','./steps/02-two-fixture.sh','./steps/03-three-fixture.sh','./steps/04-four-fixture.sh']}
        (lab/'manifest.json').write_text(json.dumps(self.row))
        self.doc='''## Step 1 — Inspect a fixture\n\n<details open><summary>Step one</summary>\n### The small problem to solve\nA report must come from a real log.\n### Where to go\nMac Terminal in the lab folder.\n<details open><summary><img src="x-RECORDER-y"/> Recorder</summary><p>Show source and command.</p></details>\n<details><summary><img src="x-EDITOR-y"/> Editor</summary><p>Highlight actual field.</p></details>\n<details><summary><img src="x-NARRATOR-y"/> Narrator</summary><table><tr><td>Command shown</td><td>Show the correct named step.</td><td>5</td></tr><tr><td>After execution proof A</td><td>The current status is two hundred.</td><td>6</td></tr><tr><td>After execution proof B</td><td>Only real proof can justify approval.</td><td>6</td></tr></table></details>\n</details>\n'''
        self.auth.joinpath('m1-demo1.md').write_text(self.doc+''.join(f'## Step {i} — Fixture {i}\n' for i in [2,3,4]))

    def test_field_values_roundtrip_and_escape(self):
        parsed=d.rows_from_terminal('  ★ │ Marker                             │ <script>alert(1)</script>\n'+self.proof)
        self.assertEqual(parsed[0],{'label':'Marker','value':'<script>alert(1)</script>','focus':False})
        self.assertEqual(parsed[1]['value'],'<live-count-in-raw-log>')
        self.assertEqual(len(parsed),3)
        self.assertEqual(d.rows_from_terminal('  ★ Old format: value')[0]['value'],'value')

    def test_full_document_renders_without_inventing_missing_proof(self):
        path=d.render_dashboard(self.batch,[self.row],self.auth)
        text=path.read_text()
        self.assertTrue(text.startswith('<!doctype html>'))
        self.assertIn('200',text)
        self.assertIn('01-named-fixture.sh',text)
        self.assertIn('0'*40,text)
        self.assertIn('NO VERIFIED STEP PROOF',text)
        self.assertIn('Script Development with ZAP',text)
        self.assertIn('Developer',text)
        self.assertIn('Recorder',text)
        self.assertIn('Editor',text)
        self.assertIn('Narrator',text)
        self.assertIn('Technical CQA',text)
        self.assertIn('Only real proof can justify approval.',text)
        self.assertNotIn('No standalone JSON file captured in the deliverables. Raw logs remain available.</a>',text)
        self.assertNotIn('href="m1-demo1/production-guide.html"',text)
        self.assertIn('m1-demo1/steps-and-output.md',text)
        self.assertNotIn('<script>alert(1)</script>',text)

    def test_fail_or_missing_log_never_shows_ready(self):
        self.row['status']='PREFLIGHT FAILED'
        (self.batch/'m1-demo1'/'logs'/'preflight-step-01.log').write_text('✘ FAIL synthetic fixture')
        result=d.render_dashboard(self.batch,[self.row],self.auth).read_text()
        self.assertIn('HOLD — NO VERIFIED STEP PROOF',result)
        self.assertIn('0/1 terminal preflights verified',result)

    def test_real_terminal_formatter_parser_contract(self):
        formatter=P.parents[1]/"runtime/scripts/fmt.py"
        if not formatter.is_file():
            # Local fixtures may run outside the repository; hosted CI checks this.
            self.skipTest("Full repository formatter not mounted beside fixture")
        env=os.environ.copy()
        env["FORCE_COLOR"]="1"
        proc=subprocess.run([sys.executable,str(formatter),"star","Rule identity","40012","focus"],
                            text=True,capture_output=True,env=env,check=True)
        self.assertIn("\x1b[38;2;255;22;117m",proc.stdout)
        fields=d.rows_from_terminal(proc.stdout,proc.stdout)
        self.assertEqual(fields,[{"label":"Rule identity","value":"40012","focus":True}])
        self.assertIn("│",proc.stdout)

    def test_invalid_empty_manifest(self):
        with self.assertRaises(ValueError): d.render_dashboard(self.batch,[],self.auth)

    def test_primary_pink_focus_tracks_real_ansi_value_only(self):
        terminal="  ★ │ Current status                         │ 200\n  ★ │ Risk                                   │ High\n"
        raw="  ★ │ Current status                         │ 200\n  ★ │ Risk                                   │ \x1b[38;2;255;22;117mHigh\x1b[0m\n"
        rows=d.rows_from_terminal(terminal,raw)
        self.assertEqual([r["focus"] for r in rows],[False,True])
        rendered=d.style_terminal(terminal,d.focused_labels(raw))
        self.assertIn('class="focused-value"',rendered)
        self.assertIn('class="ordinary-value"',rendered)
        import re
        from html import unescape
        self.assertEqual(unescape(re.sub(r"<[^>]+>","",rendered)),terminal.rstrip("\n"))

    def test_quoted_source_security(self):
        value='  ★ │ Request ID │ <svg onload=alert(1)>\n'
        out=d.style_terminal(value)
        self.assertIn('&lt;svg',out)
        self.assertNotIn('<svg',out)

    def test_exact_command_and_location_navigation_all_demos(self):
        from production_plan import PLAN, LAB_DIRS, REPO_URL
        self.assertEqual(len(PLAN),6)
        self.assertEqual(sum(map(len,PLAN.values())),24)
        self.assertTrue(all(len(items)==4 for items in PLAN.values()))
        path=d.render_dashboard(self.batch,[self.row],self.auth)
        html=path.read_text()
        self.assertIn('cd &quot;$HOME/pluralsight-script-development-with-zap/',html)
        self.assertIn('Step A · open application manually',html)
        self.assertIn('Starter',html)
        self.assertIn(REPO_URL,html)
        self.assertIn('Process', ''.join(PLAN['m2-demo3'][2]))

    def test_editor_has_individual_box_label_arrow_and_timed_gist(self):
        html=d.render_dashboard(self.batch,[self.row],self.auth).read_text()
        self.assertIn('single large blue region box',html)
        self.assertIn('Transform Pink',html)
        self.assertIn('purple arrow',html)
        self.assertIn('6–8 s',html)
        self.assertIn('same screen stays beyond 12 s',html)
        self.assertIn('NO VERIFIED STEP PROOF',html)

    def test_machine_handoff_has_actual_capture_and_draft_not_frozen(self):
        d.render_dashboard(self.batch,[self.row],self.auth)
        handoff=json.loads((self.batch/'m1-demo1/narration-handoff.json').read_text())
        self.assertEqual(handoff['reference_sha'],'0'*40)
        self.assertEqual(handoff['steps'][0]['observed_fields'][0]['value'],'<live-count-in-raw-log>')
        self.assertFalse(handoff['steps'][1]['proof_verified'])
        self.assertEqual(handoff['steps'][0]['command'],'./steps/01-named-fixture.sh')
        self.assertTrue((self.batch/'m1-demo1/narration-final.TEMPLATE.json').exists())
        self.assertFalse((self.batch/'m1-demo1/narration-final.json').exists())
        self.assertIn('BEFORE command', (self.batch/'m1-demo1/NARRATION_HANDOFF.md').read_text())

    def test_final_import_and_tts_models_require_exact_sha(self):
        from narration_handoff import validate_final,tts_text,evidence_ready
        d.render_dashboard(self.batch,[self.row],self.auth)
        src=json.loads((self.batch/'m1-demo1/narration-final.TEMPLATE.json').read_text())
        for item in src['steps']:
            for stage in ('before','during','after'):
                if not item[stage]:item[stage]='Test-only fixture speech for the selected evidence.' 
        imported,errors=validate_final(src,'m1-demo1',self.row['sha'],self.row['step_commands'])
        self.assertFalse(errors)
        self.assertFalse(evidence_ready(imported))
        self.assertIn('<break time="1.0s" />',tts_text(imported,'v2'))
        self.assertIn('[pause]',tts_text(imported,'v4'))
        src['reference_sha']='bad-sha'
        bad,errors=validate_final(src,'m1-demo1',self.row['sha'],self.row['step_commands'])
        self.assertIsNone(bad)
        self.assertTrue(any('reference_sha' in x for x in errors))

    def test_imported_speech_rendered_but_not_self_approved(self):
        d.render_dashboard(self.batch,[self.row],self.auth)
        src=json.loads((self.batch/'m1-demo1/narration-final.TEMPLATE.json').read_text())
        for item in src['steps']:
            for stage in ('before','during','after'):
                if not item[stage]:item[stage]='Test-only fixture speech for the selected evidence.' 
        src['steps'][0]['before']='Custom operator narration for the approved action.'
        (self.batch/'m1-demo1/narration-final.json').write_text(json.dumps(src))
        html=d.render_dashboard(self.batch,[self.row],self.auth).read_text()
        self.assertIn('Custom operator narration',html)
        self.assertIn('same-take evidence and CQA still pending',html)
        self.assertIn('class=\'copy-demo-narration\'',html)
        self.assertIn('class=\'copy-narration-step\'',html)

    def test_all_24_workflows_specify_real_app_source_pane_and_navigation(self):
        from production_plan import SCREENS, PLAN, LAB_DIRS, screen_action
        self.assertEqual(len(SCREENS),6)
        self.assertEqual(sum(len(x) for x in SCREENS.values()),24)
        for demo, steps in SCREENS.items():
            self.assertEqual(len(steps),4,demo)
            self.assertIn(demo,PLAN)
            for number in range(1,5):
                item=screen_action(demo,number)
                for needed in ('application','source','pane','preparation','proof'):
                    self.assertTrue(item[needed].strip(), (demo,number,needed))
                self.assertIn('demos/module',LAB_DIRS[demo])

    def test_role_order_and_copyable_cd_command_for_each_step(self):
        page=d.render_dashboard(self.batch,[self.row],self.auth).read_text()
        order=[page.find('data-role="'+x+'"') for x in ('developer','recorder','narrator','editor','cqa')]
        self.assertEqual(order,sorted(order))
        self.assertEqual(page.count("class='copy-nav'"),12)
        self.assertIn('data-cd=',page)
        self.assertIn('copy-narration-step',page)
        self.assertIn('Synchronize with the narrator',page)

    def test_editor_changes_with_imported_final_narration(self):
        d.render_dashboard(self.batch,[self.row],self.auth)
        final=json.loads((self.batch/'m1-demo1/narration-final.TEMPLATE.json').read_text())
        for entry in final['steps']:
            for phase in ('before','during','after'):
                if not entry[phase]:entry[phase]='Temporary test fixture speech only.'
        final['steps'][0]['during']='Inspect the recorded current status and justify the security decision.'
        (self.batch/'m1-demo1/narration-final.json').write_text(json.dumps(final))
        page=d.render_dashboard(self.batch,[self.row],self.auth).read_text()
        self.assertIn('Inspect the recorded current status',page)
        self.assertIn('imported narration',page)
        self.assertIn('HOLD — primary value not observed',page)

    def test_script_export_has_model_appropriate_tags_only(self):
        from narration_handoff import tts_text
        data={'steps':[{'before':'One cause.','during':'Observed field means X.','after':'Keep this decision.'}]}
        v2=tts_text(data,'v2');v4=tts_text(data,'v4')
        self.assertIn('<break time="1.0s" />',v2)
        self.assertNotIn('[pause]',v2)
        self.assertIn('[pause]',v4)
        self.assertNotIn('<break',v4)
        self.assertNotIn('Step',v2)
        self.assertNotIn('Step',v4)

if __name__=='__main__':unittest.main()
