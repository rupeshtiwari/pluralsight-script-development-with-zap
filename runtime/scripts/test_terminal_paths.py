"""Test user-facing path formatting; report locations on disk must not change."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

FMT = Path(__file__).with_name('fmt.py')

class TerminalPathTests(unittest.TestCase):
    def test_saved_report_starts_at_module_folder_before_wrapping(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'Users/nandini/pluralsight-script-development-with-zap'
            formatter = root / 'runtime/scripts/fmt.py'
            formatter.parent.mkdir(parents=True)
            shutil.copy2(FMT, formatter)
            shutil.copy2(FMT.with_name('terminal_paths.py'), formatter.with_name('terminal_paths.py'))
            relative = 'demos/module2-demos/m2-demo2-zap-api-scan-evidence/logs/report.json'
            report = root / relative
            report.parent.mkdir(parents=True)
            report.write_text('{"site": []}')
            before = report.read_bytes()
            result = subprocess.run(['python3', str(formatter), 'star',
                                     'Saved for inspection (from module folder)', str(report)],
                                    capture_output=True, text=True, check=True)
            self.assertNotIn(str(root), result.stdout)
            self.assertNotIn('nandini', result.stdout)
            # Rejoin the formatter's wrapped value column.
            rows = [line.split(' │ ', 2)[-1] for line in result.stdout.splitlines() if ' │ ' in line]
            self.assertEqual(''.join(rows), relative.removeprefix('demos/'))
            self.assertEqual(report.read_bytes(), before)

    def test_future_modules_and_all_formatter_entry_points(self):
        root = FMT.resolve().parents[2]
        for module in ('module1-demos', 'module2-demos', 'module19-demos'):
            relative = f'{module}/future-demo/logs/report.json'
            for path in (str(root / 'demos' / relative), 'demos/' + relative, relative):
                for command in (['star', 'Saved file', path], ['note', path],
                                ['ok', path], ['fail', path], ['todo', path]):
                    with self.subTest(module=module, path=path, command=command[0]):
                        result = subprocess.run(['python3', str(FMT), *command],
                                                capture_output=True, text=True, check=True)
                        self.assertIn(relative, result.stdout)
                        self.assertNotIn('demos/' + relative, result.stdout)
                        self.assertNotIn(str(root), result.stdout)
                result = subprocess.run(['python3', str(FMT), 'json'],
                                        input=json.dumps({'file': path}), capture_output=True,
                                        text=True, check=True)
                self.assertIn(relative, result.stdout)
                self.assertNotIn(str(root), result.stdout)

    def test_container_paths_and_auth_evidence_unchanged(self):
        for value in ('/tmp/globo-api-report-123.json', 'http://app:8000/account/profile',
                      'username=alice', '50000 · Medium (Medium) · note'):
            result = subprocess.run(['python3', str(FMT), 'star', 'Evidence', value],
                                    capture_output=True, text=True, check=True)
            self.assertIn(value, result.stdout)

    def test_other_home_paths_hidden_in_messages_and_json_fields(self):
        result = subprocess.run(['python3', str(FMT), 'fail', 'Cannot open /Users/nandini/report.json'],
                                capture_output=True, text=True, check=True)
        self.assertIn('~/report.json', result.stdout)
        self.assertNotIn('nandini', result.stdout)
        result = subprocess.run(['python3', str(FMT), 'json'],
                                input=json.dumps({'file': '/home/recorder/report.json'}),
                                capture_output=True, text=True, check=True)
        self.assertIn('~/report.json', result.stdout)
        self.assertNotIn('recorder', result.stdout)

    def test_author_this_first_copy_command_keeps_full_demos_path(self):
        # The 4th 'todo' arg is a RUNNABLE copy command the learner pastes. Its repo-relative path must
        # stay complete (demos/module.../...), or it fails with 'no such file or directory'. Only a home
        # prefix may be hidden (owner rule F). The message/reason/fix are still shortened as usual.
        path = 'demos/module2-demos/m2-demo1-authenticated-zap-github-actions/ci/af-plan.yaml'
        command = (f'(cd "$(git rev-parse --show-toplevel)" && git show origin/m2-demo1-after:{path} '
                   f'> {path})')
        result = subprocess.run(['python3', str(FMT), 'todo', 'you have not written the plan yet',
                                 'the -before branch ships without it', 'author ci/af-plan.yaml', command],
                                capture_output=True, text=True, check=True)
        self.assertIn(command, result.stdout)                 # command intact and runnable
        self.assertNotIn('origin/m2-demo1-after:module2-demos/', result.stdout)  # demos/ not stripped
        # a home prefix inside such a command is still hidden, but the demos/ path is preserved
        homed = subprocess.run(['python3', str(FMT), 'todo', 'x', '', '',
                                f'cat /Users/nandini/{path}'], capture_output=True, text=True, check=True)
        self.assertIn(f'cat ~/{path}', homed.stdout)
        self.assertNotIn('nandini', homed.stdout)

if __name__ == '__main__':
    unittest.main()
