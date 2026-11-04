#!/usr/bin/env python3
"""Check that the lab workflow has a self-contained execution boundary."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

class WorkflowBoundaryTests(unittest.TestCase):
    def test_lab_workflow_finishes_with_local_cleanup(self):
        workflow = (ROOT / ".github/workflows/lab-end-to-end.yml").read_text()
        self.assertIn("uses: actions/upload-artifact@v4", workflow)
        self.assertIn("run: ./lab down || docker compose down -v --remove-orphans", workflow)
        self.assertNotIn("repository_dispatch", workflow)
        self.assertNotIn("/dispatches", workflow)
        self.assertEqual(workflow.count("    needs: end-to-end"), 0)

if __name__ == "__main__":
    unittest.main()
