#!/usr/bin/env python3
"""Bounded subprocess capture. Progress is NOT a fabricated ZAP result."""
from __future__ import annotations
import codecs
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import selectors
import shlex
import signal
import subprocess
import sys
import time

LIMITS = {'setup': 3600, 'docker': 45, 'fetch': 120, 'ref': 30,
          'worktree': 120, 'startup': 1200, 'preflight-console': 2400,
          'cleanup': 180, 'worktree-remove': 60, 'diagnostics': 30}


def stop_group(proc: subprocess.Popen, grace: float = 3.0) -> None:
    """Stop only the process group started here, never all Docker processes."""
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        proc.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait(timeout=max(grace, 1.0))


def capture(command, cwd, log, *, verbose=False, label=None,
            timeout=300.0, heartbeat=10.0, interactive=False) -> int:
    """Preserve raw stdout/stderr bytes; exit 124 on deadline, 130 on interrupt.

    Poll pipe availability instead of blocking in readline(). A quiet command,
    partial line or child holding a pipe open cannot silence the watchdog.
    """
    if timeout <= 0 or heartbeat <= 0:
        raise ValueError('Timeout and heartbeat must be positive')
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    stage = label or log.stem.replace('-', ' ')
    status = {'stage': stage, 'command': list(map(str, command)), 'cwd': str(cwd),
              'started_at': datetime.now(timezone.utc).isoformat(), 'state': 'RUNNING',
              'timeout_seconds': timeout, 'exit_code': None, 'bytes_captured': 0,
              'runtime_proof': 'No claim: read the actual output and manifest'}
    metadata = log.with_suffix(log.suffix + '.status.json')
    def save():
        temp = metadata.with_suffix(metadata.suffix + '.tmp')
        temp.write_text(json.dumps(status, indent=2) + '\n', encoding='utf-8')
        temp.replace(metadata)
    save()
    print(f'  START  {stage} | limit {timeout:g}s', flush=True)
    print('         Live log: tail -f ' + shlex.quote(str(log)), flush=True)
    start = last_beat = time.monotonic()
    last_output = start
    proc = None
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', PYTHONUNBUFFERED='1')
    code = 127
    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    try:
        with log.open('wb') as raw:
            proc = subprocess.Popen(command, cwd=cwd, env=env,
                                    stdin=None if interactive else subprocess.DEVNULL,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    start_new_session=True, bufsize=0)
            selector = selectors.DefaultSelector()
            try:
                selector.register(proc.stdout, selectors.EVENT_READ)
                while selector.get_map() or proc.poll() is None:
                    now = time.monotonic()
                    elapsed = now - start
                    if elapsed >= timeout:
                        status['state'] = 'TIMED OUT'
                        stop_group(proc)
                        code = 124
                        break
                    if now - last_beat >= heartbeat:
                        quiet = int(now - last_output)
                        print(f'  WAIT   {stage} | {int(elapsed)}s elapsed | '
                              f'{status["bytes_captured"]} bytes saved | last output {quiet}s ago',
                              flush=True)
                        last_beat = now
                        status['elapsed_seconds'] = round(elapsed, 1)
                        save()
                    for key, _ in selector.select(timeout=min(0.25, timeout-elapsed)):
                        chunk = os.read(key.fileobj.fileno(), 65536)
                        if not chunk:
                            selector.unregister(key.fileobj)
                            continue
                        raw.write(chunk)
                        raw.flush()
                        status['bytes_captured'] += len(chunk)
                        last_output = time.monotonic()
                        if verbose:
                            print(decoder.decode(chunk), end='', flush=True)
                else:
                    code = proc.wait()
                if status['state'] == 'RUNNING':
                    status['state'] = 'PASSED' if code == 0 else 'FAILED'
            finally:
                selector.close()
                proc.stdout.close()
    except KeyboardInterrupt:
        status['state'] = 'INTERRUPTED'
        code = 130
        if proc is not None:
            stop_group(proc)
    except OSError as exc:
        status.update(state='LAUNCH FAILED', error=str(exc))
        with log.open('ab') as raw:
            raw.write(('Launch error: ' + str(exc) + '\n').encode())
        code = 127
    finally:
        if proc is not None and proc.poll() is None:
            stop_group(proc)
        status.update(exit_code=code, elapsed_seconds=round(time.monotonic()-start, 2),
                      finished_at=datetime.now(timezone.utc).isoformat())
        save()
        print(f'  {status["state"]:<11} {stage} | exit {code} | {status["elapsed_seconds"]}s',
              flush=True)
        if code:
            print('         Inspect: ' + str(log), flush=True)
    return code


def execute(command, cwd, log, verbose=False, heartbeat_label=None):
    stem = Path(log).stem
    key = 'ZAP_BATCH_' + stem.upper().replace('-', '_') + '_TIMEOUT'
    timeout = float(os.environ.get(key, LIMITS.get(stem, 300)))
    return capture(command, cwd, log, verbose=verbose,
                   label=heartbeat_label or stem.replace('-', ' '), timeout=timeout,
                   interactive=(stem == 'setup'))
