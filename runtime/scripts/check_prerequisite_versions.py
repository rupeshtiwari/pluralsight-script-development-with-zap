#!/usr/bin/env python3
"""Reject stale reused source copies while preserving intentionally absent answers."""
from pathlib import Path
import subprocess
import sys

from check_before_never_breaks import TAUGHT


def check(root, branches=None):
    def git(*args):
        return subprocess.run(['git', '-C', str(root), *args], capture_output=True,
                              check=True, text=True, timeout=30).stdout.strip()
    if branches is None:
        branches = [line for line in git('for-each-ref', '--format=%(refname)',
                                         'refs/remotes/origin').splitlines()
                    if not line.endswith('/HEAD')]
    canonical = {}
    for demo, paths in TAUGHT.items():
        for path in paths:
            canonical[path] = git('rev-parse', f'refs/remotes/origin/{demo}-after:{path}')
    problems = []
    for branch in branches:
        tree = set(git('ls-tree', '-r', '--name-only', branch, '--', *canonical).splitlines())
        for path in sorted(tree):
            if git('rev-parse', branch + ':' + path) != canonical[path]:
                problems.append(f'{branch}: stale prerequisite {path}; align its existing copy with the owning demo after branch')
    return problems


if __name__ == '__main__':
    try:
        problems = check(Path(__file__).resolve().parents[2])
        for problem in problems:
            print('FAIL: ' + problem)
        if problems:
            sys.exit(1)
        print('PASS: every existing reused source matches its owning demo reference; absent starter answers preserved')
    except (OSError, subprocess.SubprocessError) as error:
        print('FAIL: prerequisite version audit could not complete: ' + str(error), file=sys.stderr)
        sys.exit(1)
