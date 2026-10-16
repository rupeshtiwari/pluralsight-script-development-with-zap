#!/usr/bin/env python3
"""Real subprocess regression tests; fixtures are not ZAP evidence."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

P=Path(__file__).with_name('preflight_process.py')
spec=importlib.util.spec_from_file_location('preflight_process',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class CaptureTests(unittest.TestCase):
    def invoke(self,source,timeout=3):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.log=Path(self.temp.name)/'raw.log';self.console=io.StringIO()
        with contextlib.redirect_stdout(self.console):
            return m.capture([sys.executable,'-u','-c',source],self.temp.name,self.log,
                             label='fixture',timeout=timeout,heartbeat=.1)
    def test_quiet_subprocess_has_progress_and_deadline(self):
        began=time.monotonic()
        self.assertEqual(self.invoke('import time; time.sleep(30)',timeout=.5),124)
        self.assertLess(time.monotonic()-began,5)
        self.assertIn('WAIT',self.console.getvalue())
        self.assertEqual(json.loads(self.log.with_suffix('.log.status.json').read_text())['state'],'TIMED OUT')
    def test_partial_line_never_blocks_watchdog(self):
        self.assertEqual(self.invoke("import sys,time;sys.stdout.write('partial');sys.stdout.flush();time.sleep(30)",timeout=2.0),124)
        self.assertEqual(self.log.read_bytes(),b'partial')
    def test_raw_ansi_bytes_preserved(self):
        self.assertEqual(self.invoke("import sys;sys.stdout.buffer.write(b'\\x1b[31mraw\\x1b[0m\\n')"),0)
        self.assertEqual(self.log.read_bytes(),b'\x1b[31mraw\x1b[0m\n')
        self.assertNotIn('\x1b[31m',self.console.getvalue())
    def test_child_return_code_not_replaced(self):
        self.assertEqual(self.invoke("print('actual failure');raise SystemExit(7)"),7)
        self.assertIn('actual failure',self.log.read_text())
    def test_grandchild_pipe_cannot_hold_batch_forever(self):
        self.assertEqual(self.invoke("import subprocess,sys;subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'])",timeout=.5),124)
    def test_missing_executable_is_failure(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            code=m.capture(['/definitely/missing/program'],tmp,Path(tmp)/'missing.log',timeout=1)
        self.assertEqual(code,127)

class BatchFailureTests(unittest.TestCase):
    def test_prerequisite_failure_still_has_browser_package(self):
        script=Path(__file__).with_name('run_all_demo_preflights.py')
        spec=importlib.util.spec_from_file_location('batch_under_test',script)
        batch=importlib.util.module_from_spec(spec);spec.loader.exec_module(batch)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'repo';root.mkdir();(root/'.git').mkdir()
            output=Path(tmp)/'batch-failure'
            with patch.object(batch,'ROOT',root),patch.object(batch.sys,'platform','darwin'),patch.object(batch,'execute',return_value=7),contextlib.redirect_stdout(io.StringIO()):
                code=batch.batch(['m1-demo1','m2-demo3'],output,True)
            self.assertEqual(code,1)
            for name in ('index.html','serve.sh','manifest.json'):
                self.assertTrue((output/name).is_file())
            self.assertTrue(output.with_suffix('.zip').is_file())
            manifest=json.loads((output/'manifest.json').read_text())
            self.assertTrue(all(x['status'].startswith('NOT ATTEMPTED') for x in manifest))
            self.assertFalse(any(x['sha'] for x in manifest))

if __name__=='__main__':unittest.main()
