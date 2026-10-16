#!/usr/bin/env python3
"""Offline batch-runner tests. Real ZAP proof is tested separately on a Mac."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
SPEC=importlib.util.spec_from_file_location("batch_runner",HERE/"run_all_demo_preflights.py")
MODULE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class BatchContractTests(unittest.TestCase):
    def test_all_six_have_completed_branch_and_script(self):
        self.assertEqual(len(MODULE.DEMOS),6)
        for id_,folder,start in MODULE.DEMOS:
            self.assertTrue((ROOT/folder/"scripts"/start).is_file())
            self.assertEqual(len(list((ROOT/folder/"steps").glob("0[1-4]-*.sh"))),4)

    def test_narrator_spoken_lines_are_reused_not_invented(self):
        for id_,_,_ in MODULE.DEMOS:
            source=(ROOT/"docs/.author-instructions"/(id_+".md")).read_text()
            groups=MODULE.narrator_groups(source)
            self.assertEqual(len(groups),4,id_)
            for i,rows in enumerate(groups):
                self.assertEqual(len(rows),3,(id_,i))
                for _shot,speech,n in rows:
                    self.assertTrue(speech)
                    self.assertLessEqual(len(speech.split()),27)
                    self.assertGreater(n,0)

    def test_no_success_from_failed_or_incomplete_logs(self):
        with tempfile.TemporaryDirectory() as t:
            logs=Path(t)
            self.assertFalse(MODULE.references_ready(logs))
            for index in range(1,5):
                (logs/("preflight-step-%02d.log"%index)).write_text("✔ PASS observed")
            self.assertFalse(MODULE.references_ready(logs))
            (logs/"preflight-20261016.log").write_text("RESULT: 5 checks passed, 0 failed")
            self.assertTrue(MODULE.references_ready(logs))
            (logs/"preflight-step-04.log").write_text("✘ FAIL missing live alert")
            self.assertFalse(MODULE.references_ready(logs))

    def test_offline_generated_html_has_real_roles(self):
        from setup.evidence_report import section_html,narrator_rows
        for id_,_,_ in MODULE.DEMOS:
            source=(ROOT/"docs/.author-instructions"/(id_+".md")).read_text()
            steps=__import__("re").split(r"(?=^## Step [1-4]\b)",source,flags=__import__("re").M)
            self.assertEqual(len(steps),5,id_)
            for i,step in enumerate(steps[1:],1):
                self.assertGreater(len(section_html(step,"RECORDER")),120)
                self.assertGreater(len(section_html(step,"EDITOR")),100)
                self.assertEqual(len(narrator_rows(step)),3,(id_,i))


    def test_author_step_cards_have_valid_collapsible_markers(self):
        import re
        for id_,_,_ in MODULE.DEMOS:
            source=(ROOT/"docs/.author-instructions"/(id_+".md")).read_text()
            blocks=re.split(r"(?=^## Step [1-4]\b)",source,flags=re.M)[1:]
            self.assertEqual(len(blocks),4,id_)
            for number,block in enumerate(blocks,1):
                self.assertEqual(len(re.findall(r"<details(?:\s+open)?>",block)),4,(id_,number))
                self.assertEqual(block.count("<summary>"),4,(id_,number))
                self.assertTrue(block.lstrip().splitlines()[2].strip()=="<details open>" if number==1 else block.lstrip().splitlines()[2].strip()=="<details>",(id_,number))

    def test_demo_wrappers_find_shared_runtime_inside_a_temporary_worktree(self):
        """All six startup/reset/teardown wrappers must resolve FOUR parents."""
        import shutil
        with tempfile.TemporaryDirectory(prefix="zap-batch-path-test-") as tmp:
            tree = Path(tmp)/"checkout"
            runtime = tree/"runtime"/"scripts"
            runtime.mkdir(parents=True)
            for name in ("demo_up.sh", "demo_down.sh"):
                fake = runtime/name
                fake.write_text("#!/bin/bash" + chr(10) + "echo SHARED:" + name + chr(10), encoding="utf-8")
                fake.chmod(0o755)
            for demo, folder, _ in MODULE.DEMOS:
                source = ROOT/folder/"scripts"
                dest = tree/folder/"scripts"
                dest.mkdir(parents=True)
                for name in ("demo_up.sh", "demo_down.sh", "demo_reset.sh"):
                    shutil.copy2(source/name, dest/name)
                    run = subprocess.run(["bash", str(dest/name)],
                                         cwd=tree/folder, capture_output=True, text=True)
                    self.assertEqual(run.returncode, 0,
                                     f"{demo}/{name}: {run.stdout} {run.stderr}")
                    expected = 2 if name == "demo_reset.sh" else 1
                    self.assertEqual(run.stdout.count("SHARED:"), expected,
                                     f"{demo}/{name}: did not call correct shared runtime")

    def test_console_summary_gives_exact_folder_browser_steps_and_failed_evidence(self):
        import contextlib
        import io
        target=Path("/tmp/zap-course-deliverables/batch-20261016-180200-123456")
        rows=[{"demo":"m1-demo1","status":"STARTUP FAILED","sha":"",
               "cleanup_exit":None,"narration":"NOT GENERATED"},
              {"demo":"m2-demo3","status":"PREFLIGHT PASSED; GUI/CI REVIEW PENDING",
               "sha":"test-only","cleanup_exit":0,"narration":"DRAFT CREATED; NOT FROZEN"}]
        capture=io.StringIO()
        with contextlib.redirect_stdout(capture):
            MODULE.show_next_steps(target,target.with_suffix(".zip"),rows,1)
        text=capture.getvalue()
        self.assertIn('cd "'+str(target)+'"',text)
        self.assertIn("./serve.sh",text)
        self.assertIn("http://127.0.0.1:8765/index.html",text)
        self.assertIn("STARTUP FAILED",text)
        self.assertIn("GUI/CI",text)

    def test_raw_console_output_is_saved_without_noisy_stream(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as temp:
            raw=Path(temp)/"raw.log"
            captured=io.StringIO()
            with contextlib.redirect_stdout(captured):
                code=MODULE.execute([sys.executable,"-c",
                                     "print('A sensitive line of real raw output')"],
                                    ROOT,raw)
            self.assertEqual(code,0)
            self.assertEqual(captured.getvalue(),"")
            self.assertIn("sensitive line",raw.read_text())

    def test_author_playbooks_expose_exact_workspaces_and_spoken_beats(self):
        import re
        for demo,folder,_ in MODULE.DEMOS:
            author=(ROOT/"docs/.author-instructions"/(demo+".md")).read_text()
            steps=re.split(r"(?=^## Step [1-4]\b)",author,flags=re.M)[1:]
            self.assertEqual(len(steps),4,demo)
            self.assertIn("http://localhost:8000",author, demo)
            for i,step in enumerate(steps,1):
                for heading in ("Learning Goal","Demo Workspace","Run Command",
                                "Expected Results","Operator Decision","Spoken Narration"):
                    self.assertIn("### "+heading,step,(demo,i))
                self.assertIn("git switch "+demo+"-before",step,(demo,i))
                self.assertIn("cd \""+folder+"\"",step,(demo,i))
                self.assertIn("**Actual screen and browser check:**",step,(demo,i))
                self.assertIn("<details open>",step,(demo,i))
                narrator=MODULE.narrator_groups(step)[0]
                self.assertEqual(len(narrator),3,(demo,i))
                self.assertTrue(all(0 < len(words.split()) <= 27 for _,words,_ in narrator))

    def test_command_disposition_requires_injected_evidence_not_a_normal_ping(self):
        source=(ROOT/"demos/module1-demos/m1-demo1-targeted-injection-xss-csrf/"
                "scripts/_steps.sh").read_text()
        final=source[source.index("step4_disposition() {"):]
        self.assertIn("ZAP_CMD_PROOF",final)
        self.assertIn("--data-urlencode",final)
        self.assertIn("injected shell marker",final)
        self.assertNotIn("bytes from [0-9.]+",final)

    def test_dry_run_does_not_create_evidence(self):
        with tempfile.TemporaryDirectory() as t:
            output=Path(t)/"not-created"
            result=subprocess.run([sys.executable,str(HERE/"run_all_demo_preflights.py"),
                                   "--only","m1-demo1,m2-demo3","--dry-run",
                                   "--output",str(output)],text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn("m1-demo1-after",result.stdout)
            self.assertIn("m2-demo3-after",result.stdout)
            self.assertFalse(output.exists())

if __name__=="__main__":
    unittest.main()
