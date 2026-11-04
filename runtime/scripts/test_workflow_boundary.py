#!/usr/bin/env python3
"""Check that the student lab workflow remains self-contained."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

class WorkflowBoundaryTests(unittest.TestCase):
    def test_lab_preserves_student_execution_and_evidence(self):
        workflow = (ROOT / ".github/workflows/lab-end-to-end.yml").read_text()
        self.assertIn("./preflight-check", workflow)
        self.assertIn("uses: actions/upload-artifact@v4", workflow)
        self.assertIn("run: ./lab down || docker compose down -v --remove-orphans", workflow)

    def test_lab_does_not_dispatch_cross_repository_events(self):
        workflow = (ROOT / ".github/workflows/lab-end-to-end.yml").read_text()
        self.assertNotIn("repository_dispatch", workflow)
        self.assertNotIn("/dispatches", workflow)

if __name__ == "__main__":
    unittest.main()
