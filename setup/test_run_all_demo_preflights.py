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
                fake.write_text('#!/bin/bash\\nprintf "SHARED:%s\\\\n" "$(basename "$0")"\\n', encoding="utf-8")
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
