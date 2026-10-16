#!/usr/bin/env python3
"""One reviewed migration resolution, guarded by exact old branch SHA.

The retired module*/m*-c*/README paths were replaced by demos/module*-demos.
Their learner-facing intent already exists in the current learner guides.
The added legacy quality checker was moved to runtime/scripts and updated for
that layout. Keep the current checker, not the obsolete root/scripts variant.
All unrelated three-way merge results and both parent histories are preserved.
This is NOT a generic prefer-main conflict resolver.
"""
from pathlib import Path
import tempfile
from sync_all_branches import run, ancestor, validate

BRANCH='claude/stoic-cannon-nbupjt'
OLD='f45d62a9ffa3842f5c4e75adc0c10935797bc316'
RETIRED={f'module{m}/m{m}-c{c}/README.md' for m in (1,2) for c in (3,4,5)}
CHECKER='runtime/scripts/repo_quality_check.py'


def main():
    root=Path(__file__).resolve().parents[2]
    run(['git','fetch','--prune','origin','+refs/heads/*:refs/remotes/origin/*'],root)
    ref='refs/remotes/origin/'+BRANCH
    probe=run(['git','rev-parse','--verify',ref],root,check=False)
    if probe.returncode:
        print('Legacy branch absent; regular all-branch discovery will proceed.');return
    current=probe.stdout.strip()
    if current!=OLD:
        print('Legacy branch no longer at the reviewed conflict SHA; no special resolution applied.');return
    main_sha=run(['git','rev-parse','refs/remotes/origin/main'],root).stdout.strip()
    with tempfile.TemporaryDirectory(prefix='course-reviewed-merge-') as tmp:
        checkout=Path(tmp)/'checkout'
        run(['git','worktree','add','--detach',str(checkout),OLD],root)
        try:
            result=run(['git','merge','--no-commit','--no-ff',main_sha],checkout,check=False)
            conflicts=set(run(['git','diff','--name-only','--diff-filter=U'],checkout).stdout.splitlines())
            if result.returncode and conflicts != RETIRED|{CHECKER}:
                raise RuntimeError('Unexpected conflicts: '+repr(sorted(conflicts))+'; no push performed')
            if conflicts:
                # These exact paths no longer exist on main after the approved reorganization.
                for name in sorted(RETIRED):
                    if run(['git','cat-file','-e',main_sha+':'+name],root,check=False).returncode==0:
                        raise RuntimeError('Retired path returned on main; manual review required: '+name)
                    run(['git','rm','--',name],checkout)
                run(['git','checkout',main_sha,'--',CHECKER],checkout)
            if run(['git','diff','--name-only','--diff-filter=U'],checkout).stdout.strip():
                raise RuntimeError('Unresolved paths remain')
            validate(checkout,BRANCH)
            run(['python3','-m','unittest','discover','-s','setup','-p','test_*.py','-v'],checkout)
            run(['git','commit','-m','merge: reconcile retired learner paths and retain current validated quality checks'],checkout)
            new=run(['git','rev-parse','HEAD'],checkout).stdout.strip()
            if not ancestor(root,OLD,new) or not ancestor(root,main_sha,new):
                raise RuntimeError('Both parent histories must survive')
            live=run(['git','ls-remote','--heads','origin','refs/heads/'+BRANCH],root).stdout.split()
            if not live or live[0]!=OLD:
                raise RuntimeError('Remote branch changed; no overwrite permitted')
            run(['git','push','origin','HEAD:refs/heads/'+BRANCH],checkout)
            print('Reviewed legacy conflict resolved, tested and pushed: '+new)
        finally:
            run(['git','worktree','remove','--force',str(checkout)],root)

if __name__=='__main__':main()
