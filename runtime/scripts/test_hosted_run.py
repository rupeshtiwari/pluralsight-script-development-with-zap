#!/usr/bin/env python3
"""Offline coverage regressions using real temporary Git trees and mocked Actions responses."""
import contextlib
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).with_name('hosted_run.py')


class HostedRunTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Offline Test')
        self.git('config', 'user.email', 'offline@example.invalid')
        self.watched = self.root / 'watched.bin'
        self.watched.write_bytes(b'\x00\xfforiginal\n')
        self.git('add', '.')
        self.git('commit', '-m', 'original')
        self.sha = self.git('rev-parse', 'HEAD').stdout.strip()

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args],
                              capture_output=True, text=True, check=True)

    def coverage(self, sha=None, fail_command=None, paths=('watched.bin',)):
        run = {'id': 123, 'head_sha': sha or self.sha, 'conclusion': 'success',
               'html_url': 'https://example.invalid/run/123'}
        index = (self.root / '.git/index').read_bytes()
        real_run = subprocess.run

        def local_git(args, **kwargs):
            if (fail_command and 'GIT_INDEX_FILE' in kwargs.get('env', {})
                    and args[3] == fail_command):
                # Stale stdout must never salvage a failed Git operation.
                return subprocess.CompletedProcess(args, 128, self.sha.encode(), b'forced failure')
            return real_run(args, **kwargs)

        def response(request, **kwargs):
            body = {'jobs': [{'labels': ['ubuntu'], 'steps': [{'name': 'scan', 'conclusion': 'success'}]}]}
            if '/workflows/' in request.full_url:
                body = {'workflow_runs': [run]}
            return io.BytesIO(json.dumps(body).encode())

        output = io.StringIO()
        with patch.dict(os.environ, {'HOSTED_REPO': 'example/offline', 'GITHUB_TOKEN': ''}), \
             patch.object(sys, 'argv', [str(SCRIPT), str(self.root), 'scan.yml', 'main', *paths]), \
             patch('urllib.request.urlopen', side_effect=response), \
             patch('subprocess.run', side_effect=local_git), contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as exited:
                runpy.run_path(str(SCRIPT), run_name='__main__')
        self.assertEqual(exited.exception.code, 0)
        self.assertEqual((self.root / '.git/index').read_bytes(), index,
                         'coverage must not modify the learner index')
        return output.getvalue().strip().split('|')[4]

    def test_clean_binary_worktree_at_head_is_covered(self):
        self.assertEqual(self.coverage(), 'yes')

    def test_dirty_binary_worktree_at_head_is_not_covered(self):
        self.watched.write_bytes(b'\x00\xfedirty\n')
        self.assertEqual(self.coverage(), 'no')

    def test_staged_change_at_head_is_not_covered(self):
        self.watched.write_bytes(b'changed and staged\n')
        self.git('add', 'watched.bin')
        self.assertEqual(self.coverage(), 'no')

    def test_deleted_watched_file_is_not_covered(self):
        self.watched.unlink()
        self.assertEqual(self.coverage(), 'no')

    def test_missing_run_commit_is_not_branch_proof(self):
        self.assertEqual(self.coverage(sha='a' * 40), 'no')

    def test_temporary_index_failures_deny_even_when_head_matches(self):
        for command in ('read-tree', 'add', 'write-tree', 'diff'):
            with self.subTest(command=command):
                self.assertEqual(self.coverage(fail_command=command), 'no')

    def test_failed_add_cannot_reuse_clean_index_for_dirty_worktree(self):
        self.watched.write_bytes(b'changed\n')
        self.assertEqual(self.coverage(fail_command='add'), 'no')

    def test_untracked_taught_file_can_match_a_different_run_commit(self):
        authored = self.root / 'authored.bin'
        authored.write_bytes(b'\x00\xfftaught file\n')
        self.git('add', '.')
        self.git('commit', '-m', 'authored')
        run_sha = self.git('rev-parse', 'HEAD').stdout.strip()
        self.git('reset', '--mixed', self.sha)
        self.assertEqual(self.coverage(sha=run_sha, paths=('watched.bin', 'authored.bin')), 'yes')
        authored.write_bytes(b'different taught file\n')
        self.assertEqual(self.coverage(sha=run_sha, paths=('watched.bin', 'authored.bin')), 'no')

    def test_unwatched_changes_do_not_invalidate_watched_proof(self):
        (self.root / 'unrelated.txt').write_text('unrelated\n')
        self.assertEqual(self.coverage(), 'yes')

    def test_empty_watch_list_cannot_claim_coverage(self):
        self.assertEqual(self.coverage(paths=()), 'no')


if __name__ == '__main__':
    unittest.main()
