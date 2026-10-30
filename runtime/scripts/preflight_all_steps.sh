#!/usr/bin/env bash
# Temporarily supply missing reference sources, run the unchanged named steps,
# then let the scope transaction clean only after total success. Existing work is never replaced.
set -uo pipefail
if [ "$#" -ne 1 ]; then
    echo "usage: preflight_all_steps.sh DEMO_DIRECTORY" >&2
    exit 2
fi
exec python3 - "$1" <<'PREFLIGHT_PY'
import contextlib
import datetime
import os
from pathlib import Path
import selectors
import shutil
import signal
import stat
import subprocess
import sys
import time

DEMO_FOLDERS = {
    "m1-demo1": "demos/module1-demos/m1-demo1-targeted-injection-xss-csrf",
    "m1-demo2": "demos/module1-demos/m1-demo2-javascript-http-sender",
    "m1-demo3": "demos/module1-demos/m1-demo3-python-scanning-authentication",
    "m2-demo1": "demos/module2-demos/m2-demo1-authenticated-zap-github-actions",
    "m2-demo2": "demos/module2-demos/m2-demo2-zap-api-scan-evidence",
    "m2-demo3": "demos/module2-demos/m2-demo3-security-quality-gates",
}
SOURCES = {
    "marker": ("m1-demo2", "zap-scripts/globomantics-marker.js"),
    "rule": ("m1-demo3", "zap-scripts/globomantics-active-rule.py"),
    "auth": ("m1-demo3", "zap-scripts/globomantics-auth.py"),
    "plan": ("m2-demo1", "ci/af-plan.yaml"),
    "gate": ("m2-demo3", "ci/gate-plan.yaml"),
}
# Reused prerequisites are needed even for a scoped check from main. They are
# removed only when this invocation supplied them; existing files stay untouched.
DEPENDENCIES = {
    "m1-demo1": (), "m1-demo2": ("marker",), "m1-demo3": ("rule", "auth"),
    "m2-demo1": ("marker", "rule", "auth", "plan"),
    "m2-demo2": ("marker", "rule", "auth", "plan"), "m2-demo3": ("gate",),
}
SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)

class PreflightInterrupted(BaseException):
    pass

def interrupted(signum, frame):
    raise PreflightInterrupted(signum)

for sig in SIGNALS:
    signal.signal(sig, interrupted)

@contextlib.contextmanager
def atomic_change():
    previous = signal.pthread_sigmask(signal.SIG_BLOCK, SIGNALS)
    try:
        yield
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK, previous)

def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60).stdout

def stop_process(child):
    # Defer a second interrupt until the owned process group has been stopped.
    with atomic_change():
        try:
            os.killpg(child.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        child.wait(timeout=5)

def main():
    demo = Path(sys.argv[1]).resolve(strict=True)
    root = Path(git(demo, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    key = next((k for k, folder in DEMO_FOLDERS.items() if root / folder == demo), None)
    if key is None:
        raise RuntimeError("unrecognized demo directory; no reference files were copied")
    managed = os.environ.get("PREFLIGHT_WORKSPACE_ACTIVE") == str(root / ".preflight-workspace")
    if not managed:
        return subprocess.call([sys.executable, str(root / "runtime/scripts/preflight_workspace.py"),
                                "demo", str(root), str(demo)])
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root / "runtime/scripts"))
    from preflight_workspace import load, register_source
    steps = sorted((demo / "steps").glob("0[1-4]-*.sh"))
    if len(steps) != 4 or any(not p.name.startswith("0%d-" % (i + 1)) for i, p in enumerate(steps)):
        raise RuntimeError("expected four concept-named step scripts in order")
    timeout = float(os.environ.get("PREFLIGHT_STEP_TIMEOUT", "1800"))
    if not 0 < timeout < float("inf"):
        raise RuntimeError("PREFLIGHT_STEP_TIMEOUT must be a positive number of seconds")
    lock = root / ".preflight-reference.lock"
    owns_lock = False
    copies, directories = [], []
    raw = None
    raw_path = full_path = None
    result = 1
    stdout_open = True
    logging_failed = False

    def emit(data):
        nonlocal stdout_open, logging_failed
        if isinstance(data, str):
            data = (data + "\n").encode()
        if raw is not None:
            try:
                raw.write(data)
                raw.flush()
            except OSError:
                logging_failed = True
        if stdout_open:
            try:
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            except OSError:
                logging_failed = True
                # A closed output pipe must never prevent source restoration.
                stdout_open = False
                os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())

    def safe_path(relative):
        target = root / relative
        for part in (target, *target.parents):
            if part == root:
                break
            if part.is_symlink():
                raise RuntimeError("refusing a symlink in required source path: " + str(part.relative_to(root)))
        return target

    try:
        with atomic_change():
            try:
                lock.mkdir()
            except FileExistsError:
                raise RuntimeError("another preflight owns .preflight-reference.lock; wait for it to finish. "
                                   "If interrupted by a forced kill, inspect its sources before removing the stale lock")
            owns_lock = True
        (lock / "owner").write_text("pid=%d\ndemo=%s\nworkspace_run=%s\n" %
                                    (os.getpid(), key, load(root)["run_id"]))
        logs = demo / "logs"
        logs.mkdir(exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        raw_path = logs / ("preflight-" + stamp + ".ansi.log")
        full_path = logs / ("preflight-" + stamp + ".log")
        raw = raw_path.open("xb")
        # A failed preparation must not leave old baselines looking current.
        for pattern in ("preflight-step-0[1-4].log", "preflight-step-0[1-4].exit"):
            for old in logs.glob(pattern):
                old.unlink()
        producer = logs / ".producer"
        producer.mkdir(exist_ok=True)
        for old in producer.glob("preflight-step-0[1-4].raw.log"):
            old.unlink()
        emit("PREFLIGHT · four actual demo steps, the same commands a learner runs")
        emit("Evidence is restricted to the authorized local Globomantics application.")
        refs = {}
        for label in DEPENDENCIES[key]:
            source_demo, name = SOURCES[label]
            relative = DEMO_FOLDERS[source_demo] + "/" + name
            target = safe_path(relative)
            if os.path.lexists(target):
                if not target.is_file():
                    raise RuntimeError("required source is not a regular file: " + relative)
                emit("PREFLIGHT SOURCE · preserving existing " + relative)
                continue
            ref = "refs/remotes/origin/" + source_demo + "-after"
            if ref not in refs:
                try:
                    refs[ref] = git(root, "rev-parse", "--verify", ref + "^{commit}").decode().strip()
                except subprocess.CalledProcessError:
                    git(root, "fetch", "origin", source_demo + "-after:" + ref)
                    refs[ref] = git(root, "rev-parse", "--verify", ref + "^{commit}").decode().strip()
            data = git(root, "show", refs[ref] + ":" + relative)
            if not data:
                raise RuntimeError("reference source is empty: " + relative)
            missing = []
            parent = target.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for folder in reversed(missing):
                with atomic_change():
                    folder.mkdir()
                    directories.append(folder)
            snapshot = lock / ("source-%d" % len(copies))
            snapshot.write_bytes(data)
            identity = snapshot.stat()
            with atomic_change():
                register_source(root, relative, data, identity)
                os.link(snapshot, target)  # Atomic creation; never overwrite an existing file.
                copies.append((target, snapshot, identity.st_dev, identity.st_ino, data))
            emit("PREFLIGHT SOURCE · temporary %s from %s@%s" % (relative, ref, refs[ref]))
        if os.environ.get("PREFLIGHT_CI_SOURCE") == "1":
            subprocess.run([sys.executable, str(root / "runtime/scripts/capture_ci_source.py"),
                            str(root), *[str(root / relative) for relative in load(root)["sources"]]], check=True, timeout=120)
        emit("")
        passed = 0
        env = dict(os.environ, DEMO_SYNC_MODE="1", DEMO_SYNC_PHASE="reference")
        for number, step in enumerate(steps, 1):
            emit("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            emit("STEP %d · command: ./steps/%s" % (number, step.name))
            emit("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            child = None
            stem = "preflight-step-%02d" % number
            # Capture the actual named command's combined output and process exit. These
            # sidecars are proof from this execution, never inferred from a PASS marker.
            step_raw_path = producer / (stem + ".raw.log")
            step_raw = step_raw_path.open("wb")
            try:
                with atomic_change():
                    child = subprocess.Popen(
                        [str(step)], cwd=demo, env=env, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, start_new_session=True,
                        preexec_fn=lambda: signal.pthread_sigmask(signal.SIG_UNBLOCK, SIGNALS))
                with selectors.DefaultSelector() as selector:
                    selector.register(child.stdout, selectors.EVENT_READ)
                    started = heartbeat = time.monotonic()
                    while selector.get_map():
                        now = time.monotonic()
                        if now - started >= timeout:
                            raise TimeoutError("Step %d exceeded %.0f seconds" % (number, timeout))
                        if now - heartbeat >= 10:
                            emit("PREFLIGHT · Step %d still running (%.0fs)" % (number, now - started))
                            heartbeat = now
                        for event, _ in selector.select(timeout=min(1, timeout - (now - started))):
                            data = os.read(event.fd, 65536)
                            if data:
                                step_raw.write(data)
                                step_raw.flush()
                                emit(data)
                            else:
                                selector.unregister(event.fileobj)
                status = child.wait(timeout=max(0.1, timeout - (time.monotonic() - started)))
            except BaseException:
                if child is not None:
                    stop_process(child)
                raise
            finally:
                step_raw.close()
                if child is not None and child.stdout is not None:
                    child.stdout.close()
                if child is not None and child.returncode is not None:
                    shutil.copyfile(step_raw_path, logs / (stem + ".log"))
                    (logs / (stem + ".exit")).write_text(str(child.returncode) + "\n")
            if status:
                emit("FAIL: Step %d failed; baseline is not recording-ready." % number)
                emit("RESULT: %d steps passed before failure" % passed)
                result = status if status > 0 else 1
                break
            passed += 1
            emit("")
        else:
            emit("RESULT: 4 steps passed, 0 failed")
            emit("REFERENCE: logs/preflight-step-01.log through logs/preflight-step-04.log")
            emit("CHECK: these are this run's named-step outputs; separate ZAP GUI or Actions proof is still required.")
            result = 0
    except PreflightInterrupted as error:
        result = 128 + int(error.args[0])
        emit("FAIL: preflight interrupted; all preflight files are retained for inspection.")
    except (OSError, RuntimeError, subprocess.SubprocessError, ValueError) as error:
        emit("FAIL: preflight could not complete: " + str(error))
        result = 1
    finally:
        # A second interrupt must not interrupt cleanup halfway through.
        for sig in SIGNALS:
            signal.signal(sig, signal.SIG_IGN)
        # The parent transaction owns source cleanup across the ENTIRE selected scope.
        # Release only this process lock; keep sources and evidence until total success.
        if owns_lock:
            shutil.rmtree(lock)
        if raw is not None:
            raw.close()
            raw = None
            shutil.copyfile(raw_path, full_path)
            emit("Full preflight log: " + str(full_path.relative_to(demo)))
    return 1 if logging_failed else result

try:
    sys.exit(main())
except (OSError, RuntimeError, subprocess.SubprocessError, ValueError) as error:
    print("FAIL: preflight could not start: " + str(error), file=sys.stderr)
    sys.exit(1)
PREFLIGHT_PY
