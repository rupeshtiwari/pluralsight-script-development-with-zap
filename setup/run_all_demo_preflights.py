#!/usr/bin/env python3
"""Run six isolated ZAP checks with visible progress and preserved failure evidence."""
import argparse
from datetime import datetime
import fcntl
import html
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import zipfile

try:
    from .preflight_process import execute
except ImportError:
    from preflight_process import execute

ROOT=Path(__file__).resolve().parents[1]
DEMOS=[
 ('m1-demo1','demos/module1-demos/m1-demo1-targeted-injection-xss-csrf','demo_reset.sh'),
 ('m1-demo2','demos/module1-demos/m1-demo2-javascript-http-sender','demo_up.sh'),
 ('m1-demo3','demos/module1-demos/m1-demo3-python-scanning-authentication','demo_reset.sh'),
 ('m2-demo1','demos/module2-demos/m2-demo1-authenticated-zap-github-actions','demo_up.sh'),
 ('m2-demo2','demos/module2-demos/m2-demo2-zap-api-scan-evidence','demo_up.sh'),
 ('m2-demo3','demos/module2-demos/m2-demo3-security-quality-gates','demo_up.sh'),
]
INDEX={k:(p,u) for k,p,u in DEMOS}
FENCE=chr(96)*3


def color(text,code):
    if not sys.stdout.isatty() or os.environ.get('NO_COLOR'):
        return text
    return '\033[38;2;'+code+'m'+text+'\033[0m'


def heading(text):
    print('\n'+color('━'*68,'0;163;255'),flush=True)
    print(color(text,'255;22;117'),flush=True)
    print(color('━'*68,'0;163;255'),flush=True)


def good(row):
    return row['status'].startswith('PREFLIGHT PASSED') and row.get('cleanup_exit')==0 and row.get('worktree_remove_exit',0)==0


def show_result(index,total,row,out):
    print(f"  {index}/{total} {row['demo']} | {row['status']}",flush=True)
    if not good(row):
        for name in row.get('failure_logs',[]):
            print('  Inspect: '+str(out/name),flush=True)


def show_next_steps(output,archive,rows,exit_code):
    heading('BATCH COMPLETE • '+str(len(rows))+' demo records')
    print('  Demo         Result\n  '+'─'*62)
    for row in rows:
        word='PASS • GUI/CI review pending' if good(row) else 'HOLD • '+row['status']
        print(f"  {row['demo']:<12} {color(word,'2;224;136' if good(row) else '185;0;75')}")
    print('\n  Evidence folder: '+str(output))
    print('  Complete ZIP:    '+str(archive))
    heading('NEXT • OPEN THIS EXACT BATCH')
    print('  In macOS Terminal, run:')
    print('  cd '+chr(34)+str(output).replace(chr(34),chr(92)+chr(34))+chr(34))
    print('  ./serve.sh')
    print('\n  Browser: http://127.0.0.1:8765/index.html')
    print('  Stop the viewer with Ctrl+C. Keep this failed or successful batch unchanged.')
    print('\n  After a fix, start a NEW batch:')
    print('  cd '+shlex.quote(str(ROOT)))
    print('  ./setup/run-all-demo-preflights.sh')
    print('  Every retry creates a new timestamped folder; earlier logs are never overwritten.')
    print('  GUI/CI footage and same-take review are still separate approval gates.')
    if exit_code:
        print('  STOP: This is a diagnostic package, not recording approval.')


def references_ready(logs):
    for i in range(1,5):
        p=logs/('preflight-step-%02d.log'%i)
        if not p.is_file():
            return False
        text=p.read_text(errors='replace')
        if '✔ PASS' not in text or '✘ FAIL' in text:
            return False
    return any('RESULT: 5 checks passed, 0 failed' in p.read_text(errors='replace')
               for p in logs.glob('preflight-*.log') if '-step-' not in p.name)


def narrator_groups(source):
    blocks=re.split(r'(?=^## Step [1-4]\b)',source,flags=re.M)
    groups=[]
    for block in blocks[1:5]:
        m=re.search(r'<summary>[^<]*<img[^>]*NARRATOR[^>]*>.*?</summary>\s*<table>(.*?)</table>',block,re.S|re.I)
        rows=[]
        if m:
            for shot,speech,n in re.findall(r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(\d+)(?:\s+spoken\s+words)?</td>\s*</tr>',m.group(1),re.S|re.I):
                clean=lambda x:html.unescape(re.sub(r'<[^>]+>','',x)).strip()
                rows.append((clean(shot),clean(speech),int(n)))
        groups.append(rows)
    return groups


def write_documents(demo,sha,lab,out):
    lines=['# '+demo+' — Actual Step Commands And Output','',
           'Completed branch '+demo+'-after at '+sha,'',
           'Only captured preflight output follows. Raw bytes remain in logs/.producer.','']
    for i,script in enumerate(sorted((lab/'steps').glob('0[1-4]-*.sh')),1):
        source=lab/'logs'/('preflight-step-%02d.log'%i)
        lines+=['## Step %d — ./steps/%s'%(i,script.name),'',FENCE+'text',source.read_text(errors='replace').rstrip(),FENCE,'']
    (out/'steps-and-output.md').write_text('\n'.join(lines),encoding='utf-8')
    author=lab.parents[2]/'docs/.author-instructions'/(demo+'.md')
    groups=narrator_groups(author.read_text()) if author.is_file() else []
    draft=['# '+demo+' — Narration Draft','',
           'Reference SHA: '+sha,'NOT FINAL: same-take GUI/CI and timed narration review are required.','']
    for i in range(1,5):
        draft+=['## Step '+str(i),'']
        rows=groups[i-1] if len(groups)>=i else []
        if not rows:
            draft+=['HOLD: no authored speech was found.','']
        for shot,speech,count in rows:
            draft+=['**'+shot+' ('+str(count)+' words):** '+speech,'']
        draft+=['Evidence: logs/preflight-step-%02d.log'%i,'External GUI/CI proof: PENDING','']
    (out/'narration-draft.md').write_text('\n'.join(draft),encoding='utf-8')
    from evidence_report import render
    render(demo,sha,lab,out)


def initial_row(demo):
    return dict(demo=demo,branch=demo+'-after',sha='',status='NOT ATTEMPTED',
                startup_exit=None,preflight_exit=None,cleanup_exit=None,
                worktree_remove_exit=None,narration='NOT GENERATED',step_commands=[],failure_logs=[])


def save_row(out,row):
    out.mkdir(parents=True,exist_ok=True)
    (out/'manifest.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')


def publish_bundle(output,results):
    """Always supply a diagnostic page, even when prerequisites fail."""
    summary=['# ZAP Batch Results','',
             'These records describe actual attempts, not a guarantee of successful findings.','',
             '| Demo | Source SHA | Status |','|---|---|---|']
    summary+=['| '+r['demo']+' | '+r['sha']+' | '+r['status']+' |' for r in results]
    summary+=['','Open macOS Terminal:','','```bash','cd '+shlex.quote(str(output)),'./serve.sh','```',
              '', 'Raw phase logs and *.log.status.json include elapsed time, process exit and timeout state.']
    (output/'README.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
    (output/'manifest.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    rendered=True
    try:
        from production_dashboard import render_dashboard
        tools_dir=output/'tools';tools_dir.mkdir(exist_ok=True)
        for source in ('production_dashboard.py','production_plan.py','narration_handoff.py'):
            shutil.copy2(ROOT/'setup'/source,tools_dir/source)
        author_sources=ROOT/'docs/.author-instructions'
        shutil.copytree(author_sources,output/'author-playbooks',dirs_exist_ok=True)
        for source,destination in (('serve-production-deliverables.sh','serve.sh'),
                                   ('refresh-production-deliverables.sh','refresh.sh')):
            shutil.copy2(ROOT/'setup'/source,output/destination)
            (output/destination).chmod(0o755)
        for source in ('PRODUCTION_PORTAL_GUIDE.md','NARRATOR_NEXT_SESSION_PROMPT.md'):
            shutil.copy2(author_sources/source,output/source)
        render_dashboard(output,results,output/'author-playbooks')
    except Exception as exc:
        rendered=False
        (output/'dashboard-error.txt').write_text(str(exc)+'\n',encoding='utf-8')
        cards=''.join('<tr><td>'+html.escape(r['demo'])+'</td><td>'+html.escape(r['status'])+
                      '</td><td><a href="'+r['demo']+'/manifest.json">Manifest</a></td></tr>' for r in results)
        (output/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1"><title>Batch diagnostics</title>'
            '<body><h1>HOLD — batch diagnostics</h1><p>The full production renderer was unavailable. '
            'No missing evidence has been invented.</p><table><tr><th>Demo</th><th>Status</th><th>Evidence</th></tr>'+
            cards+'</table><p><a href="dashboard-error.txt">Renderer error</a> · '
            '<a href="manifest.json">Batch manifest</a></p></body></html>',encoding='utf-8')
        (output/'serve.sh').write_text('#!/usr/bin/env bash\nset -euo pipefail\n'
            'HERE="$(cd "$(dirname "$0")" && pwd)"\n'
            '( sleep 1; open "http://127.0.0.1:8765/index.html" >/dev/null 2>&1 || true ) &\n'
            'exec python3 -m http.server 8765 --bind 127.0.0.1 --directory "$HERE"\n',encoding='utf-8')
        (output/'serve.sh').chmod(0o755)
    archive=output.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for file in sorted(output.rglob('*')):
            if file.is_file():
                z.write(file,Path(output.name)/file.relative_to(output))
    code=0 if rendered and results and all(good(r) for r in results) else 1
    show_next_steps(output,archive,results,code)
    return code


def batch(ids,output,skip_setup):
    if sys.platform!='darwin':
        print('ERROR: live course preflights must run on the recording Mac; no results simulated.',file=sys.stderr)
        return 2
    if not (ROOT/'.git').exists():
        print('ERROR: use a local Git checkout.',file=sys.stderr);return 2
    output.mkdir(parents=True,exist_ok=False)
    heading('SCRIPT DEVELOPMENT WITH ZAP • DEVELOPER PREFLIGHT')
    print('  Batch folder: '+str(output),flush=True)
    print('  Each active phase prints a heartbeat every ten seconds and has a deadline.',flush=True)
    print('  START/WAIT are progress only, not successful scan evidence.',flush=True)
    results=[]
    lock=(output.parent/'.zap-course-preflight.lock').open('a+')
    acquired=False
    blocked=''
    try:
        try:
            fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
            acquired=True
        except BlockingIOError:
            blocked='ANOTHER BATCH IS RUNNING — stop it cleanly before retrying'
        checks=[] if blocked else ([] if skip_setup else [('setup',['bash','./setup/setup-macos.sh'])])
        if not blocked:
            checks += [('docker',['docker','info']),('fetch',['git','fetch','origin'])]
        for phase,command in checks:
            rc=execute(command,ROOT,output/(phase+'.log'),verbose=(phase=='setup'))
            if rc:
                blocked=phase.upper()+' '+('TIMED OUT' if rc==124 else 'INTERRUPTED' if rc==130 else 'FAILED')
                break
        for index,demo in enumerate(ids,1):
            row=initial_row(demo);out=output/demo
            if blocked:
                row['status']='NOT ATTEMPTED — '+blocked
                save_row(out,row);results.append(row);continue
            folder,startup=INDEX[demo]
            heading(f'DEMO {index}/{len(ids)} • {demo} • {demo}-after')
            out.mkdir()
            temp=Path(tempfile.mkdtemp(prefix='zap-batch-'+demo+'-'))
            worktree=temp/'checkout';lab=worktree/folder
            added=False;started=False
            try:
                remote='refs/remotes/origin/'+row['branch']
                if execute(['git','rev-parse','--verify',remote],ROOT,out/'ref.log'):
                    row.update(status='BRANCH MISSING',failure_logs=['ref.log']);continue
                rc=execute(['git','worktree','add','--detach',str(worktree),remote],ROOT,out/'worktree.log')
                if rc:
                    row.update(status='WORKTREE FAILED',failure_logs=['worktree.log']);continue
                added=True
                row['sha']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=worktree,text=True,timeout=30).strip()
                row['step_commands']=['./steps/'+p.name for p in sorted((lab/'steps').glob('0[1-4]-*.sh'))]
                if len(row['step_commands'])!=4:
                    row['status']='FOUR NAMED STEPS MISSING';continue
                row['status']='STARTING';save_row(out,row)
                started=True
                rc=row['startup_exit']=execute(['bash','./scripts/'+startup],lab,out/'startup.log')
                if rc:
                    row.update(status='STARTUP '+('TIMED OUT' if rc==124 else 'INTERRUPTED' if rc==130 else 'FAILED'),failure_logs=['startup.log'])
                    if rc==130:blocked='USER INTERRUPTED THE BATCH'
                    execute(['docker','compose','ps','--all'],worktree,out/'diagnostics.log')
                    continue
                row['status']='CHECKING FOUR STEPS';save_row(out,row)
                rc=row['preflight_exit']=execute(['bash',str(worktree/'runtime/scripts/preflight_all_steps.sh'),str(lab)],lab,out/'preflight-console.log')
                if rc or not references_ready(lab/'logs'):
                    row.update(status='PREFLIGHT '+('TIMED OUT' if rc==124 else 'INTERRUPTED' if rc==130 else 'FAILED'),failure_logs=['preflight-console.log'])
                    if rc==130:blocked='USER INTERRUPTED THE BATCH'
                    continue
                write_documents(demo,row['sha'],lab,out)
                row.update(status='PREFLIGHT PASSED; GUI/CI REVIEW PENDING',narration='DRAFT CREATED; NOT FROZEN')
            except Exception as exc:
                row.update(status='ERROR',failure_logs=['error.txt'])
                (out/'error.txt').write_text(str(exc)+'\n',encoding='utf-8')
            finally:
                if added:
                    if started:
                        row['cleanup_exit']=execute(['bash','./scripts/demo_down.sh'],lab,out/'cleanup.log')
                        if row['cleanup_exit']:
                            row['status']='CLEANUP FAILED; '+row['status']
                            row['failure_logs'].append('cleanup.log')
                            blocked='PREVIOUS CLEANUP FAILED — inspect retained diagnostics'
                    if (lab/'logs').is_dir():
                        shutil.copytree(lab/'logs',out/'logs',dirs_exist_ok=True)
                    row['worktree_remove_exit']=execute(['git','worktree','remove','--force',str(worktree)],ROOT,out/'worktree-remove.log')
                    if row['worktree_remove_exit']:
                        row['status']='WORKTREE CLEANUP FAILED; '+row['status']
                        row['retained_worktree']=str(worktree)
                        row['failure_logs'].append('worktree-remove.log')
                    else:
                        shutil.rmtree(temp,ignore_errors=True)
                elif not worktree.exists():
                    shutil.rmtree(temp,ignore_errors=True)
                save_row(out,row);results.append(row)
                show_result(index,len(ids),row,out)
        return publish_bundle(output,results)
    finally:
        if acquired:fcntl.flock(lock.fileno(),fcntl.LOCK_UN)
        lock.close()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--only',help='Comma separated demo IDs')
    p.add_argument('--skip-setup',action='store_true')
    p.add_argument('--dry-run',action='store_true')
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    ids=a.only.split(',') if a.only else [d[0] for d in DEMOS]
    if not ids or len(ids)!=len(set(ids)) or any(x not in INDEX for x in ids):p.error('unknown or duplicate demo ID')
    output=(a.output or Path.home()/'zap-course-deliverables'/('batch-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f'))).expanduser().resolve()
    if a.dry_run:
        print('DRY RUN: No Docker, Git, setup or file writes.')
        for demo in ids:
            folder,startup=INDEX[demo]
            print(demo+'-after → '+folder+'/scripts/'+startup+' → shared four-step validator')
        print('Output: '+str(output));return 0
    if output.exists():p.error('output directory already exists; choose a new --output')
    return batch(ids,output,a.skip_setup)

if __name__=='__main__':raise SystemExit(main())
