#!/usr/bin/env python3
"""Merge the tested main revision into EVERY remote child branch, never reset it.

No branch-name allowlist. No force push. Conflicts remain explicit failures.
The workflow validates candidates before publication and dispatches normal CI
because pushes authenticated with GITHUB_TOKEN do not trigger push workflows.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.request
import urllib.parse


def run(args, cwd, env=None, check=True):
    p=subprocess.run(args,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
    if check and p.returncode:
        raise RuntimeError('Command failed: '+repr(args)+'\n'+p.stdout[-5000:])
    return p


def branches(root):
    rows=run(['git','for-each-ref','--format=%(refname)\t%(objectname)\t%(symref)',
              'refs/remotes/origin/'],root).stdout.splitlines()
    result={}
    for row in rows:
        ref,sha,symbolic=row.split('\t')
        if symbolic:
            continue
        name=ref.removeprefix('refs/remotes/origin/')
        result[name]=sha
    return result


def ancestor(root, older, newer):
    return run(['git','merge-base','--is-ancestor',older,newer],root,check=False).returncode==0


def validate(root, branch):
    env=dict(os.environ, GITHUB_REF_NAME=branch)
    # All required source and offline checks; this never claims live Mac scans.
    for parent in ('setup','runtime','demos'):
        for file in sorted((root/parent).rglob('*.sh')):
            run(['bash','-n',str(file)],root,env)
    commands=[
        [sys.executable,'-m','compileall','-q','runtime/app','runtime/scripts'],
        [sys.executable,'-m','unittest','discover','-s','runtime/scripts','-p','test_recording_step.py','-v'],
        [sys.executable,'runtime/scripts/check_repository_layout.py'],
        [sys.executable,'runtime/scripts/repo_quality_check.py'],
    ]
    for command in commands:
        run(command,root,env)


def dispatch(repo, branch):
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        raise RuntimeError('CI dispatch requested without a token')
    if len(repo.split('/'))!=2 or any(not x for x in repo.split('/')):
        raise ValueError('Repository must be owner/name')
    req=urllib.request.Request(
        'https://api.github.com/repos/'+repo+'/actions/workflows/validate-repository-layout.yml/dispatches',
        data=json.dumps({'ref':branch}).encode(),method='POST',
        headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
                 'Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28'})
    with urllib.request.urlopen(req,timeout=30) as response:
        if response.status != 204:
            raise RuntimeError('Unexpected CI dispatch status '+str(response.status))


def sync_one(root, main_sha, branch, old_sha, apply, validator=validate):
    row={'branch':branch,'before_sha':old_sha,'after_sha':old_sha,'status':'PENDING',
         'static_validation':'NOT RUN','runtime_validation':'NOT RUN', 'ci_dispatch':'NOT REQUESTED'}
    if ancestor(root,main_sha,old_sha):
        row['status']='ALREADY SYNCHRONIZED'
        # The separate normal workflow validates already-synchronized heads.
        return row
    if not apply:
        row['status']='NEEDS MERGE'
        return row
    with tempfile.TemporaryDirectory(prefix='course-branch-sync-') as folder:
        checkout=Path(folder)/'checkout'
        added=False
        try:
            run(['git','worktree','add','--detach',str(checkout),old_sha],root)
            added=True
            merged=run(['git','merge','--no-ff','--no-edit',main_sha],checkout,check=False)
            if merged.returncode:
                row['status']='CONFLICT, NOT PUSHED'
                row['conflicts']=run(['git','diff','--name-only','--diff-filter=U'],checkout).stdout.splitlines()
                return row
            validator(checkout,branch)
            row['static_validation']='PASSED'
            new=run(['git','rev-parse','HEAD'],checkout).stdout.strip()
            if not ancestor(checkout,old_sha,new) or not ancestor(checkout,main_sha,new):
                raise RuntimeError('Merge lost main or original branch ancestry')
            current=run(['git','ls-remote','--heads','origin','refs/heads/'+branch],root).stdout.split()
            if not current or current[0]!=old_sha:
                raise RuntimeError('Remote branch moved during validation; refresh instead of overwriting it')
            # A normal push must remain a fast-forward of the ORIGINAL child head.
            run(['git','push','origin','HEAD:refs/heads/'+branch],checkout)
            row.update(after_sha=new,status='MERGED AND VALIDATED')
        except Exception as exc:
            row.update(status='FAILED, REVIEW REQUIRED',error=str(exc))
        finally:
            if added:
                removed=run(['git','worktree','remove','--force',str(checkout)],root,check=False)
                if removed.returncode:
                    row.update(status='CLEANUP FAILED',cleanup_error=removed.stdout[-1500:])
    return row


def synchronize(root, apply=False, repo=None, do_dispatch=False, validator=validate):
    root=Path(root).resolve()
    # Explicit refspec means narrow checkout defaults do not hide other branches.
    run(['git','fetch','--prune','origin','+refs/heads/*:refs/remotes/origin/*'],root)
    initial=branches(root)
    main=initial.get('main')
    if not main:
        raise RuntimeError('origin/main not found')
    if run(['git','rev-parse','HEAD'],root).stdout.strip()!=main:
        raise RuntimeError('Run from the latest reviewed main commit; source moved or wrong checkout')
    if run(['git','status','--porcelain'],root).stdout.strip():
        raise RuntimeError('Working checkout is dirty; no reset or deletion performed')
    rows=[]
    for branch,old in sorted(initial.items()):
        if branch=='main':
            continue
        row=sync_one(root,main,branch,old,apply,validator)
        if do_dispatch and row['status'] in ('MERGED AND VALIDATED','ALREADY SYNCHRONIZED'):
            try:
                dispatch(repo,branch)
                row['ci_dispatch']='REQUESTED, CHECK RUN RESULT'
            except Exception as exc:
                row['ci_dispatch']='FAILED: '+str(exc)
        print(branch+': '+row['status'],flush=True)
        rows.append(row)
    run(['git','fetch','--prune','origin','+refs/heads/*:refs/remotes/origin/*'],root)
    final=branches(root)
    for row in rows:
        sha=final.get(row['branch'])
        row['verified_remote_sha']=sha
        row['behind_main']=int(run(['git','rev-list','--count',f'{sha}..{main}'],root).stdout) if sha else None
        row['ahead_main']=int(run(['git','rev-list','--count',f'{main}..{sha}'],root).stdout) if sha else None
    drift=sorted(set(final)-set(initial))
    passed=bool(apply and final.get('main')==main and not drift and all(
        r['behind_main']==0 and r['status'] in ('MERGED AND VALIDATED','ALREADY SYNCHRONIZED') and
        not r['ci_dispatch'].startswith('FAILED') for r in rows))
    report={'tested_main_sha':main,'final_main_sha':final.get('main'),
            'checked_at':datetime.now(timezone.utc).isoformat(),'child_branches_discovered':len(initial)-1,
            'new_branches_during_run':drift,'synchronization_verified':passed,
            'hosted_child_ci':'DISPATCHED, NOT YET VERIFIED' if do_dispatch else 'NOT DISPATCHED',
            'runtime_proof':'NOT ASSERTED','branches':rows}
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--dispatch-ci',action='store_true')
    parser.add_argument('--repo',default=os.environ.get('GITHUB_REPOSITORY'))
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    try:
        report=synchronize(root,args.apply,args.repo,args.dispatch_ci)
    except Exception as exc:
        report={'synchronization_verified':False,'error':str(exc)}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    summary=os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary,'a',encoding='utf-8') as f:
            f.write('## All-Branch Synchronization\n\n')
            f.write('Main: `'+str(report.get('tested_main_sha','unknown'))+'`\n\n')
            f.write('| Branch | Status | Behind main |\n|---|---|---|\n')
            for r in report.get('branches',[]):
                f.write('| '+r['branch'].replace('|','&#124;')+' | '+r['status']+' | '+str(r['behind_main'])+' |\n')
            f.write('\nLive ZAP and recording proof are not asserted by branch validation.\n')
    sys.exit(0 if report.get('synchronization_verified') else 1)
