#!/usr/bin/env python3
"""Offline tests of evidence synchronization; no Docker or live findings simulated."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ENGINE = Path(__file__).with_name("recording_step.py")


class RecordingParityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.demo = Path(self.tmp.name)
        (self.demo / "scripts").mkdir()
        self.dummy = self.demo / "dummy.py"
        self.dummy.write_text(
            'import os\n'
            'print("ZAP outgoing: /greet?name=marker-%s" % os.getenv("REQUEST_ID","123456"))\n'
            'print("Active scan: id=%s · progress=100%%" % os.getenv("SCAN_ID","9"))\n'
            'print("Requests the scan sent: %s" % os.getenv("COUNT","450"))\n'
            'print("Risk: %s" % os.getenv("RISK","High"))\n'
            'print("✔ PASS tested the actual request")\n',
            encoding="utf-8",
        )

    def run_step(self, mode, **env_extra):
        env = os.environ.copy()
        env.update(DEMO_SYNC_PHASE=mode)
        env.update(env_extra)
        return subprocess.run(
            [sys.executable, str(ENGINE), str(self.demo), "1",
             sys.executable, str(self.dummy)],
            capture_output=True, text=True, env=env,
        )

    def test_repeat_with_changed_request_id_and_count_matches(self):
        pre = self.run_step("reference", REQUEST_ID="123456", SCAN_ID="9", COUNT="450")
        self.assertEqual(pre.returncode, 0, pre.stderr)
        same = self.run_step("compare", REQUEST_ID="654321", SCAN_ID="10", COUNT="525")
        self.assertEqual(same.returncode, 0, same.stderr)
        self.assertEqual(pre.stdout, same.stdout)
        raw = (self.demo / "logs/.producer/recorded-step-01.raw.log").read_text()
        self.assertIn("marker-654321", raw)
        self.assertIn("525", raw)
        self.assertNotIn("654321", same.stdout)

    def test_changed_security_risk_fails_closed(self):
        self.assertEqual(self.run_step("reference").returncode, 0)
        drift = self.run_step("compare", RISK="Low")
        self.assertEqual(drift.returncode, 1)
        self.assertIn("SYNC MISMATCH", drift.stderr)

    def test_missing_preflight_reference_is_not_a_success(self):
        x = self.run_step("compare")
        self.assertEqual(x.returncode, 1)
        self.assertIn("SYNC HOLD", x.stderr)

    def test_underlying_failure_is_not_a_reference(self):
        self.dummy.write_text('print("✘ FAIL: missing custom finding")\n')
        x = self.run_step("reference")
        self.assertNotEqual(x.returncode, 0)
        self.assertFalse((self.demo / "logs/preflight-step-01.log").exists())


if __name__ == "__main__":
    unittest.main()
