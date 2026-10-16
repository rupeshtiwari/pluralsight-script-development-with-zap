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
        fields=d.rows_from_terminal(proc.stdout)
        self.assertEqual(fields,[{"label":"Rule identity","value":"40012"}])
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

if __name__=='__main__':unittest.main()
