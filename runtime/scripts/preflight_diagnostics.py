"""Read-only preflight diagnostics. Never print credentials, env dumps or home paths."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

from terminal_paths import display_text


def build_report(root, emit=None):
    lines = ['PREFLIGHT DIAGNOSTICS', 'Generated UTC: '+datetime.now(timezone.utc).isoformat(timespec='seconds')]
    if emit:
        for line in lines: emit(line)
    def sanitize(value):
        text = str(value)
        # Do not disclose injected or training credentials even in tool errors.
        for key in ('ZAP_API_KEY', 'GITHUB_TOKEN', 'GH_TOKEN', 'POSTGRES_PASSWORD'):
            value = os.environ.get(key)
            if value:
                text = text.replace(value, '<redacted>')
        return display_text(text)
    def add(label, value):
        line=label+': '+sanitize(value)
        lines.append(line)
        if emit: emit(line)
    def command(label, args):
        try:
            proc = subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=10)
            output=sanitize((proc.stdout or proc.stderr).strip())
            add(label, f'exit {proc.returncode}; '+output[:4000])
        except (OSError, subprocess.SubprocessError) as exc:
            add(label, type(exc).__name__+' (command unavailable or timed out)')
    def http(label, url, fields=None, authenticated=False):
        try:
            request=urllib.request.Request(url,headers={'User-Agent':'Globomantics-preflight-diagnostics'})
            if authenticated and os.environ.get('GITHUB_TOKEN'):
                request.add_header('Authorization','Bearer '+os.environ['GITHUB_TOKEN'])
            opener=urllib.request.build_opener(urllib.request.ProxyHandler({})) if label in ('App health','ZAP API') else urllib.request.build_opener()
            with opener.open(request,timeout=8) as response:
                data=json.load(response)
                if fields:
                    # Database exception strings may contain connection details.
                    selected={k:data.get(k) for k in fields}
                    for db in ('postgres','mongo'):
                        if db in selected:selected[db]='ok' if selected[db]=='ok' else 'not ready'
                    add(label,f'HTTP {response.status}; '+json.dumps(selected,sort_keys=True))
                else:
                    add(label,f'HTTP {response.status}; API reachable')
        except urllib.error.HTTPError as exc:
            add(label,f'HTTP {exc.code} ({exc.reason})')
        except (OSError, ValueError) as exc:
            add(label,type(exc).__name__+'; connection failed or invalid response: '+str(getattr(exc,'reason',exc)))
    command('OS', ['uname','-srm'])
    add('Python',sys.version.split()[0])
    command('Git revision',['git','rev-parse','--short=12','HEAD'])
    command('Git branch',['git','branch','--show-current'])
    command('Docker versions',['docker','version','--format','client={{.Client.Version}} server={{if .Server}}{{.Server.Version}}{{else}}unreachable{{end}}'])
    command('Compose version',['docker','compose','version','--short'])
    command('Service status',['docker','compose','ps','--all','--format','{{.Service}} | {{.State}} | {{.Health}}'])
    for key in ('ZAP_API_KEY','GITHUB_TOKEN','GH_TOKEN'):
        add(key, 'present (value hidden)' if os.environ.get(key) else 'not set')
    http('App health','http://localhost:8000/health',('build','vulnerable','postgres','mongo'))
    key=os.environ.get('ZAP_API_KEY','')
    http('ZAP API','http://localhost:8090/JSON/core/view/version/?'+urllib.parse.urlencode({'apikey':key}),('version',))
    command('Completed reference branches',['git','for-each-ref','--format=%(refname:short) %(objectname:short=12)','refs/remotes/origin/m1-demo2-after','refs/remotes/origin/m1-demo3-after','refs/remotes/origin/m2-demo1-after','refs/remotes/origin/m2-demo3-after'])
    lock=root/'.preflight-reference.lock'
    add('Preflight source lock','present; inspect owner before removing' if lock.exists() else 'absent')
    for log in sorted(root.glob('FAIL-*.log')):
        text=log.read_text(errors='replace')
        # Keep the actual failing-step context, not arbitrary raw application responses.
        hints=[line for line in text.splitlines() if re.search(r'^(STEP |FAIL:|SYNC HOLD|PREFLIGHT SETUP)|✘ FAIL|HTTP [045]\d\d|another preflight',line)]
        add('Failure '+log.name, '\n'.join(hints[-12:]) or 'see this current-run failure log')
    http('GitHub authenticated-scan API', 'https://api.github.com/repos/rupeshtiwari/pluralsight-script-development-with-zap/actions/workflows/zap-authenticated-scan.yml/runs?branch=m2-demo1-after&status=completed&per_page=1', authenticated=True)
    lines.append('No credential values or environment dumps are included. Report locations and Git state were not changed.')
    return '\n'.join(lines)+'\n'


def main():
    root=Path(__file__).resolve().parents[2]
    report=build_report(root, emit=lambda line: print(line,flush=True))
    (root/'preflight-diagnostics.txt').write_text(report)
    print('No credential values or environment dumps are included.')
    print('Saved: preflight-diagnostics.txt')
    return 0

if __name__=='__main__':raise SystemExit(main())
