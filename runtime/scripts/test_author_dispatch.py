#!/usr/bin/env python3
"""Execute the dispatch shell offline; curl is a local stub, never a network call."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest

WORKFLOW = Path(__file__).resolve().parents[2] / '.github/workflows/lab-end-to-end.yml'
DESTINATION = ('https://api.github.com/repos/rupeshtiwari/'
               'pluralsight-author-13-script-development-with-zap/dispatches')


class AuthorDispatchTests(unittest.TestCase):
    def dispatch(self, status=0, token='offline-secret'):
        # Execute the exact workflow run block, with the Actions env supplied locally.
        workflow = WORKFLOW.read_text().split("      - name: Dispatch the author repo's evidence sync\n", 1)[1]
        self.assertIn('SYNC_BRANCH: ${{ github.ref_name }}', workflow)
        shell = textwrap.dedent(workflow.split('        run: |\n', 1)[1])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            stub = root / 'curl'
            stub.write_text('#!/usr/bin/env python3\nimport json, os, sys\n'
                            'from pathlib import Path\n'
                            'Path(os.environ["CURL_ARGS"]).write_text(json.dumps(sys.argv[1:]))\n'
                            'sys.exit(int(os.environ["CURL_STATUS"]))\n')
            stub.chmod(0o755)
            args_file = root / 'args.json'
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ['PATH'], TOKEN=token,
                       SYNC_BRANCH='feature/quoted-"branch', CURL_ARGS=str(args_file), CURL_STATUS=str(status))
            result = subprocess.run(['bash', '-c', shell], env=env, capture_output=True, text=True)
            args = json.loads(args_file.read_text()) if args_file.exists() else None
        self.assertNotIn('offline-secret', result.stdout + result.stderr)
        return result, args

    def test_success_dispatches_current_repo_and_json_branch(self):
        result, args = self.dispatch()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(DESTINATION, args)
        self.assertIn('--fail', args)
        self.assertIn('Content-Type: application/json', args)
        self.assertEqual(args[args.index('--max-time') + 1], '30')
        self.assertEqual(args[args.index('--output') + 1], '/dev/null')
        payload = json.loads(args[args.index('--data') + 1])
        self.assertEqual(payload, {'event_type': 'code-synced',
                                  'client_payload': {'branch': 'feature/quoted-"branch'}})
        self.assertIn('dispatched code-synced', result.stdout)

    def test_http_error_is_failure_and_never_claims_dispatch(self):
        # curl --fail returns 22 for either a 403 or 404 HTTP response.
        result, args = self.dispatch(status=22)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--fail', args)
        self.assertIn('dispatch failed', result.stdout)
        self.assertNotIn('dispatched code-synced', result.stdout)

    def test_missing_token_skips_without_attempting_dispatch(self):
        result, args = self.dispatch(token='')
        self.assertEqual(result.returncode, 0)
        self.assertIsNone(args)
        self.assertIn('skipping', result.stdout)
        self.assertNotIn('dispatched code-synced', result.stdout)


if __name__ == '__main__':
    unittest.main()
