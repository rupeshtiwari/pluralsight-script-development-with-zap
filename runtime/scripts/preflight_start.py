"""Bound readiness/startup and cancel only this preflight's subprocess groups."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import urllib.parse

SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)

class Cancelled(Exception):
    def __init__(self, signum): self.signum = signum


def stop(child):
    previous = {sig: signal.signal(sig, signal.SIG_IGN) for sig in SIGNALS}
    try:
        try: os.killpg(child.pid, signal.SIGTERM)
        except ProcessLookupError: pass
        try: child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try: os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError: pass
            child.wait()
    finally:
        for sig, handler in previous.items(): signal.signal(sig, handler)


def read_command(args, env, timeout):
    child = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True, start_new_session=True)
    try:
        out, _ = child.communicate(timeout=timeout)
        return out.strip() if child.returncode == 0 else None
    except BaseException:
        stop(child)
        raise


def ready(env, timeout):
    try:
        if read_command(['docker', 'info'], env, timeout) is None: return False
        for service in ('postgres', 'mongo', 'app', 'zap'):
            cid = read_command(['docker', 'compose', 'ps', '-q', service], env, timeout)
            if not cid: return False
            health = read_command(['docker', 'inspect', '-f', '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}', cid], env, timeout)
            if health != 'healthy': return False
        curl = ['curl', '-fsS', '--noproxy', 'localhost,127.0.0.1', '--connect-timeout', '2', '--max-time', '5']
        health = json.loads(read_command(curl + ['http://localhost:8000/health'], env, timeout) or '{}')
        if not (health.get('vulnerable') is True and health.get('postgres') == health.get('mongo') == 'ok'): return False
        key = env.get('ZAP_API_KEY')
        if not key: return False
        url = 'http://localhost:8090/JSON/core/view/version/?' + urllib.parse.urlencode({'apikey': key})
        data = json.loads(read_command(curl + [url], env, timeout) or '{}')
        return data.get('version') == '2.17.0'
    except (OSError, ValueError, subprocess.SubprocessError):
        return False


def main():
    scripts = Path(sys.argv[1]).resolve()
    env = dict(os.environ, APP_BUILD='vulnerable')
    child = None
    status = 1
    def cancel(signum, frame): raise Cancelled(signum)
    for sig in SIGNALS: signal.signal(sig, cancel)
    try:
        timeout = float(os.environ.get('PREFLIGHT_START_TIMEOUT', '1200'))
        ready_timeout = float(os.environ.get('PREFLIGHT_READY_TIMEOUT', '5'))
        if not all(0 < value < float('inf') for value in (timeout, ready_timeout)):
            raise ValueError('PREFLIGHT_START_TIMEOUT and PREFLIGHT_READY_TIMEOUT must be positive seconds')
        if ready(env, ready_timeout):
            print('PREFLIGHT SETUP · existing vulnerable lab and ZAP are ready; reusing them.', flush=True)
            return 0
        print('PREFLIGHT SETUP · lab is not ready; starting the vulnerable app, databases and ZAP.', flush=True)
        child = subprocess.Popen([str(scripts / 'lab-up.sh')], env=env, start_new_session=True)
        status = child.wait(timeout=timeout)
        if status == 0:
            if ready(env, ready_timeout):
                print('PREFLIGHT SETUP · app, databases and ZAP are ready.', flush=True)
                return 0
            print('FAIL: startup returned but the vulnerable lab/ZAP readiness checks still fail.', flush=True)
        else:
            print(f'FAIL: lab startup failed (exit {status}); no demo steps were executed.', flush=True)
    except Cancelled as exc:
        print('FAIL: preflight setup interrupted; stopping its owned subprocesses.', flush=True)
        return 128 + exc.signum
    except subprocess.TimeoutExpired:
        print('FAIL: lab startup exceeded PREFLIGHT_START_TIMEOUT; no demo steps were executed.', flush=True)
    except (OSError, ValueError) as exc:
        print(f'FAIL: lab startup could not run: {exc}', flush=True)
    finally:
        for sig in SIGNALS: signal.signal(sig, signal.SIG_IGN)
        if child is not None and child.poll() is None: stop(child)
    print("Inspect the setup output above; run 'docker compose ps' and 'docker compose logs --tail=100 zap app' from the repository root.", flush=True)
    return status if status > 0 else 1

if __name__ == '__main__': raise SystemExit(main())
