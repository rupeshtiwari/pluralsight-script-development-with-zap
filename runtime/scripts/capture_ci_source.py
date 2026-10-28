#!/usr/bin/env python3
"""Capture the actual CI execution source after temporary prerequisites are supplied.

Workflow identity and executed source are deliberately separate. A disposable index
includes tracked working files and the explicit temporary prerequisite paths only;
logs/generated output never enter the tree. This helper does not change the real index.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def capture(root, supplied=()):
    root = Path(root).resolve()

    def git(*args, env=None):
        return subprocess.run(['git', '-C', str(root), *args], env=env,
                              capture_output=True, check=True, timeout=60).stdout

    def full_sha(value):
        if not re.fullmatch(r'[0-9a-f]{40}', value):
            raise ValueError('expected a full source SHA')
        return value

    workflow = full_sha((root / 'SOURCE.txt').read_text().strip())
    if workflow != os.environ['GITHUB_SHA']:
        raise ValueError('workflow source mismatch')
    head = full_sha(git('rev-parse', '--verify', 'HEAD').decode().strip())
    after = full_sha((root / 'AFTER_SHA.txt').read_text().strip())
    git('cat-file', '-e', after + '^{commit}')
    git('merge-base', '--is-ancestor', workflow, head)
    supplied = [str(Path(p).relative_to(root)) if Path(p).is_absolute() else p for p in supplied]
    for relative in supplied:
        path = Path(relative)
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('unsafe supplied source path')
    with tempfile.TemporaryDirectory(prefix='ci-source-index-') as temporary:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(temporary) / 'index'))
        git('read-tree', 'HEAD', env=env)
        git('add', '-u', env=env)
        if supplied:
            git('add', '--', *supplied, env=env)
        tree = full_sha(git('write-tree', env=env).decode().strip())
        source_paths = git('ls-files', '-z', env=env).split(b'\0')
    hashes = {}
    for encoded in source_paths:
        if not encoded:
            continue
        relative = os.fsdecode(encoded)
        path = root / relative
        content = os.fsencode(os.readlink(path)) if path.is_symlink() else path.read_bytes()
        hashes[relative] = hashlib.sha256(content).hexdigest()
    patch = git('diff', '--binary', workflow, tree, '--')
    (root / 'AUTHORED.patch').write_bytes(patch)
    (root / 'EXECUTED_HEAD.txt').write_text(head + '\n')
    (root / 'EXECUTED_TREE.txt').write_text(tree + '\n')
    manifest = {'workflow_sha': workflow, 'executed_head': head, 'executed_tree': tree,
                'after_sha': after, 'authored_patch_sha256': hashlib.sha256(patch).hexdigest(),
                'source_hashes': hashes}
    (root / 'EXECUTION.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    names = ('SOURCE.txt', 'AFTER_SHA.txt', 'EXECUTED_HEAD.txt', 'EXECUTED_TREE.txt',
             'AUTHORED.patch', 'EXECUTION.json')
    (root / 'SOURCE_SHA256SUMS.txt').write_text(''.join(
        hashlib.sha256((root / name).read_bytes()).hexdigest() + '  ' + name + '\n' for name in names))
    return manifest


if __name__ == '__main__':
    try:
        capture(sys.argv[1], sys.argv[2:])
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print('CI source capture failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
