#!/usr/bin/env python3
"""Own preflight files across a complete scope; clean only after total success."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import uuid

STATE = '.preflight-workspace'
SOURCES = (
    'demos/module1-demos/m1-demo2-javascript-http-sender/zap-scripts/globomantics-marker.js',
    'demos/module1-demos/m1-demo3-python-scanning-authentication/zap-scripts/globomantics-active-rule.py',
    'demos/module1-demos/m1-demo3-python-scanning-authentication/zap-scripts/globomantics-auth.py',
    'demos/module2-demos/m2-demo1-authenticated-zap-github-actions/ci/af-plan.yaml',
    'demos/module2-demos/m2-demo3-security-quality-gates/ci/gate-plan.yaml',
)
ROOT_OUTPUTS = ('course-evidence.txt', 'preflight-diagnostics.txt', 'AUTHORED.patch',
                'EXECUTED_HEAD.txt', 'EXECUTED_TREE.txt', 'EXECUTION.json', 'SOURCE_SHA256SUMS.txt')
LOG_PATTERNS = ('preflight-*.log', 'preflight-step-*.exit', '.producer/*.log',
                'alert-disposition.md', '.m1demo3-state', 'custom-alert-record.json',
                '.m2demo2-state', 'globo-api-report-*.json', '.gate/*')


def safe(root, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise RuntimeError('unsafe cleanup path')
    target = root / path
    for part in (target, *target.parents):
        if part == root:
            break
        if part.is_symlink():
            raise RuntimeError('refusing symlink: ' + relative)
    return target


def fingerprint(path):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise RuntimeError('expected a regular file: ' + path.name)
    return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'mode': stat.S_IMODE(info.st_mode)}


def file_identity(path):
    if not path.exists():
        return None
    info = path.lstat()
    return dict(fingerprint(path), device=info.st_dev, inode=info.st_ino)


def directory_identity(path):
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode):
        raise RuntimeError('expected an output directory: ' + path.name)
    return {'mode': stat.S_IMODE(info.st_mode), 'device': info.st_dev, 'inode': info.st_ino}


def inventory(root):
    paths = {root / p for p in (*SOURCES, *ROOT_OUTPUTS)}
    paths.update(root.glob('FAIL-*.log'))
    directories = set()
    # Check every demo logs directory, including reused cross-demo dependencies.
    for demo in (root / 'demos').glob('module*-demos/*'):
        if not demo.is_dir():
            continue
        logs = safe(root, str((demo / 'logs').relative_to(root)))
        for pattern in LOG_PATTERNS:
            paths.update(logs.glob(pattern))
        for directory in (logs, logs / '.producer', logs / '.gate'):
            safe(root, str(directory.relative_to(root)))
            if directory.is_dir():
                directories.add(str(directory.relative_to(root)))
    files = {}
    for path in sorted(paths):
        relative = str(path.relative_to(root))
        safe(root, relative)
        if path.exists():
            files[relative] = fingerprint(path)
        if relative in SOURCES:
            for parent in path.parents:
                if parent == root:
                    break
                if parent.is_dir():
                    directories.add(str(parent.relative_to(root)))
    return files, {relative: directory_identity(safe(root, relative)) for relative in sorted(directories)}


def save(root, manifest):
    state = safe(root, STATE)
    temporary = state / 'manifest.tmp'
    temporary.write_text(json.dumps(manifest, indent=2) + '\n')
    temporary.replace(state / 'manifest.json')


def load(root):
    return json.loads(safe(root, STATE + '/manifest.json').read_text())


def register_source(root, relative, data, identity):
    """Register before exclusive creation, so a crash never loses file ownership."""
    if relative not in SOURCES:
        raise RuntimeError('unrecognized temporary source')
    manifest = load(root)
    manifest['sources'][relative] = {
        'sha256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(identity.st_mode),
        'device': identity.st_dev, 'inode': identity.st_ino}
    save(root, manifest)


def seal(root, manifest):
    manifest['after'], manifest['after_directories'] = inventory(root)
    manifest['phase'] = 'retained'
    save(root, manifest)


def stale_reference_lock(root, manifest):
    lock = safe(root, '.preflight-reference.lock')
    if not lock.exists():
        return False
    owner = dict(line.split('=', 1) for line in (lock / 'owner').read_text().splitlines())
    if owner.get('workspace_run') != manifest['run_id']:
        raise RuntimeError('reference lock has unknown ownership; inspect .preflight-reference.lock before cleanup')
    try:
        os.kill(int(owner['pid']), 0)
    except ProcessLookupError:
        pass
    else:
        raise RuntimeError('a native preflight runner is still running; wait before cleanup')
    for path in lock.iterdir():
        if path.name != 'owner' and not (path.name.startswith('source-') and path.name[7:].isdigit()):
            raise RuntimeError('unknown file in reference lock; preserved for inspection')
        safe(root, str(path.relative_to(root)))
        fingerprint(path)
    return True


def save_changed_files(root, changed):
    """Copy every changed owned file outside the checkout before any cleanup."""
    if not changed:
        return
    try:
        destination = Path(tempfile.mkdtemp(prefix=root.name + '-preflight-saved-', dir=root.parent))
    except OSError as error:
        raise RuntimeError('could not create a changed-file backup; checkout files preserved: ' + str(error.strerror)) from error
    location = os.path.relpath(destination, root)
    # Print the recovery location first, including if a later copy fails.
    print('Saving changed preflight files to: ' + location, flush=True)
    try:
        for relative, expected in changed:
            source = safe(root, relative)
            if fingerprint(source) != expected:
                raise RuntimeError('file changed while preparing backup: ' + relative)
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            if fingerprint(target) != expected:
                raise RuntimeError('backup verification failed: ' + relative)
        (destination / 'saved-files.json').write_text(json.dumps(dict(changed), indent=2) + '\n')
    except (OSError, RuntimeError) as error:
        detail = error.strerror if isinstance(error, OSError) else str(error)
        raise RuntimeError('changed-file backup failed; checkout files preserved. Partial backup: ' + location + '; ' + str(detail)) from error
    print('Changed files saved and verified: ' + location, flush=True)


def cleanup(root, manifest, save_changes=False):
    remove_stale_lock = stale_reference_lock(root, manifest)
    before, after = manifest['before'], manifest['after']
    actions = []
    changed = []
    approved = {}
    for relative in sorted(before.keys() | after.keys()):
        original, generated = before.get(relative), after.get(relative)
        # Existing learner source is never restored over or removed. Temporary
        # source ownership includes inode identity, not merely matching content.
        if relative in SOURCES:
            if original:
                continue
            expected = manifest['sources'].get(relative)
            if expected is None:
                continue
            target = safe(root, relative)
            if not target.exists():
                continue  # An explicit manual deletion already cleaned this copy.
            current = file_identity(target)
            if current != expected:
                if not save_changes:
                    raise RuntimeError('temporary source was edited or replaced; preserved: ' + relative + '; to back up changes and clean, run ./preflight-check --cleanup --save-changes')
                changed.append((relative, fingerprint(target)))
            approved[relative] = current
            actions.append((relative, None))
            continue
        if original == generated:
            continue
        target = safe(root, relative)
        observed = file_identity(target)
        current = {key: observed[key] for key in ('sha256', 'mode')} if observed else None
        if current == original:
            continue  # Already restored, or explicitly moved/deleted after the run.
        if current is not None and current != generated:
            if not save_changes:
                raise RuntimeError('file changed after preflight; preserved: ' + relative + '; to back up changes and clean, run ./preflight-check --cleanup --save-changes')
            changed.append((relative, current))
        if original:
            backup = safe(root, STATE + '/before/' + relative)
            if fingerprint(backup) != original:
                raise RuntimeError('original backup is missing or changed: ' + relative)
        approved[relative] = observed
        actions.append((relative, original))
    directory_modes = []
    approved_directories = {}
    for relative, original in manifest['before_directories'].items():
        generated = manifest['after_directories'].get(relative)
        if original == generated:
            continue
        target = safe(root, relative)
        if generated is None or directory_identity(target) != generated:
            raise RuntimeError('output directory changed; preserved: ' + relative)
        if (original['device'], original['inode']) != (generated['device'], generated['inode']):
            raise RuntimeError('output directory was replaced; preserved: ' + relative)
        directory_modes.append((relative, original['mode']))
        approved_directories[relative] = generated
    for relative in set(manifest['after_directories']) - set(manifest['before_directories']):
        target = safe(root, relative)
        if target.exists():
            expected = manifest['after_directories'][relative]
            if directory_identity(target) != expected:
                raise RuntimeError('output directory changed; preserved: ' + relative)
            approved_directories[relative] = expected
    # A slow archive must not make later editor changes disappear. Validate the
    # whole approved plan after every backup has finished and before any action.
    save_changed_files(root, changed)
    for relative, expected in approved_directories.items():
        if directory_identity(safe(root, relative)) != expected:
            raise RuntimeError('output directory changed while preparing cleanup; preserved: ' + relative)
    for relative, expected in approved.items():
        if file_identity(safe(root, relative)) != expected:
            raise RuntimeError('file changed while preparing cleanup; preserved: ' + relative)
    for relative, original in actions:
        target = safe(root, relative)
        if file_identity(target) != approved[relative]:
            raise RuntimeError('file changed during cleanup; preserved: ' + relative)
        if original:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(safe(root, STATE + '/before/' + relative), target)
        else:
            target.unlink(missing_ok=True)
    for relative, mode in directory_modes:
        target = safe(root, relative)
        if directory_identity(target) != approved_directories[relative]:
            raise RuntimeError('output directory changed during cleanup; preserved: ' + relative)
        target.chmod(mode)
    old_dirs = set(manifest['before_directories'])
    for relative in sorted(set(manifest['after_directories']) - old_dirs,
                           key=lambda p: len(Path(p).parts), reverse=True):
        target = safe(root, relative)
        if not target.exists():
            continue
        if relative not in approved_directories or directory_identity(target) != approved_directories[relative]:
            raise RuntimeError('output directory changed during cleanup; preserved: ' + relative)
        try:
            target.rmdir()  # Never remove unknown files or nonempty directories.
        except OSError:
            pass
    if remove_stale_lock:
        shutil.rmtree(safe(root, '.preflight-reference.lock'))
    shutil.rmtree(safe(root, STATE))
    print('PREFLIGHT CLEANUP COMPLETE · generated files removed; pre-existing files restored.', flush=True)


def export_evidence(root, manifest):
    destination = os.environ.get('PREFLIGHT_EVIDENCE_DIR')
    if not destination:
        return
    target = Path(destination).resolve()
    if target == root or root in target.parents:
        raise RuntimeError('PREFLIGHT_EVIDENCE_DIR must be outside the checkout')
    target.mkdir(parents=True, exist_ok=False)
    for relative in (*manifest['after'], 'SOURCE.txt', 'AFTER_SHA.txt'):
        if relative in SOURCES:
            continue
        source = safe(root, relative)
        if source.is_file():
            output = target / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, output)
    print('Preflight evidence exported outside the checkout for CI collection.', flush=True)


def manual(root, save_changes=False):
    if not (root / STATE).exists():
        print('No retained preflight files to clean.')
        return 0
    manifest = load(root)
    # The owner remains active while exporting and cleaning, including after seal().
    try:
        os.kill(manifest['pid'], 0)
    except ProcessLookupError:
        stale_reference_lock(root, manifest)
        if manifest['phase'] == 'running':
            seal(root, manifest)
    else:
        raise RuntimeError('preflight is still running; wait before cleanup')
    cleanup(root, manifest, save_changes=save_changes)
    return 0


def run(root, command):
    state = root / STATE
    try:
        state.mkdir(mode=0o700)
    except FileExistsError:
        raise RuntimeError('retained or active preflight files exist. Inspect them, then run ./preflight-check --cleanup before retrying')
    try:
        if (root / '.preflight-reference.lock').exists():
            raise RuntimeError('another runner or stale .preflight-reference.lock exists; inspect it before retrying')
        before, directories = inventory(root)
        manifest = {'version': 1, 'run_id': uuid.uuid4().hex, 'phase': 'running', 'pid': os.getpid(),
                    'before': before, 'before_directories': directories, 'sources': {}}
        for relative in before:
            source = safe(root, relative)
            backup = state / 'before' / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, backup)
        save(root, manifest)
    except BaseException:
        shutil.rmtree(state)
        raise
    child = None
    interrupted = 0

    def cancel(signum, frame):
        nonlocal interrupted
        interrupted = interrupted or signum
        if child is not None:
            child.send_signal(signal.SIGTERM)

    previous = {sig: signal.signal(sig, cancel) for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)}
    status = 1
    try:
        env = dict(os.environ, PREFLIGHT_WORKSPACE_ACTIVE=str(state), PYTHONDONTWRITEBYTECODE="1")
        child = subprocess.Popen(command, cwd=root, env=env)
        if interrupted:
            child.terminate()
        status = child.wait()
        if interrupted:
            status = 128 + interrupted
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)
        manifest = load(root)  # Native runners register temporary sources here.
        seal(root, manifest)
    export_evidence(root, manifest)
    if status == 0:
        cleanup(root, manifest)
        print('Ready for recording from your original source-file state.', flush=True)
    else:
        print('PREFLIGHT FILES RETAINED · a step/setup failed or the run was interrupted. No recording cleanup was performed.', flush=True)
        print('After inspecting the failure, manually run: ./preflight-check --cleanup', flush=True)
    return status if status >= 0 else 128 - status


def main():
    action, location, *arguments = sys.argv[1:]
    root = Path(location).resolve()
    if action == 'cleanup':
        if arguments not in ([], ['--save-changes']):
            raise ValueError('usage: ./preflight-check --cleanup [--save-changes]')
        return manual(root, save_changes=bool(arguments))
    if action == 'run':
        return run(root, [str(root / 'runtime/scripts/preflight_course.sh'), str(root), *arguments])
    if action == 'demo':
        return run(root, [str(root / 'runtime/scripts/preflight_all_steps.sh'), *arguments])
    raise RuntimeError('unknown preflight workspace action')


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as error:
        print('PREFLIGHT HOLD: ' + str(error), file=sys.stderr)
        print('Files preserved. Inspect them, then run ./preflight-check --cleanup.', file=sys.stderr)
        sys.exit(1)
