#!/usr/bin/env python3
"""Run independent real ZAP preflights, collect evidence, draft narration."""
import argparse
from datetime import datetime
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
DEMOS=[
 ("m1-demo1","demos/module1-demos/m1-demo1-targeted-injection-xss-csrf","demo_reset.sh"),
 ("m1-demo2","demos/module1-demos/m1-demo2-javascript-http-sender","demo_up.sh"),
 ("m1-demo3","demos/module1-demos/m1-demo3-python-scanning-authentication","demo_reset.sh"),
 ("m2-demo1","demos/module2-demos/m2-demo1-authenticated-zap-github-actions","demo_up.sh"),
 ("m2-demo2","demos/module2-demos/m2-demo2-zap-api-scan-evidence","demo_up.sh"),
 ("m2-demo3","demos/module2-demos/m2-demo3-security-quality-gates","demo_up.sh"),
]
INDEX={k:(p,u) for k,p,u in DEMOS}
FENCE=chr(96)*3

def execute(command,cwd,log,verbose=False,heartbeat_label=None):
    """Capture every raw line, but keep the operator console concise."""
    import threading
    log.parent.mkdir(parents=True,exist_ok=True)
    stop=threading.Event()
    def pulse():
        while not stop.wait(25):
            if heartbeat_label:
                print("  … "+heartbeat_label+" still running; full output is being saved",flush=True)
    if heartbeat_label:
        threading.Thread(target=pulse,daemon=True).start()
    try:
        with log.open("w",encoding="utf-8") as f:
            proc=subprocess.Popen(command,cwd=cwd,stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,text=True,errors="replace")
            for line in proc.stdout:
                f.write(line)
                f.flush()
                if verbose:
                    print(line,end="",flush=True)
            return proc.wait()
    finally:
        stop.set()


def color(text,code):
    """Pluralsight brand palette, disabled in redirected/file output."""
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return text
    return "\033[38;2;"+code+"m"+text+"\033[0m"


def heading(text):
    print()
    print(color("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","0;163;255"))
    print(color(text,"255;22;117"))
    print(color("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","0;163;255"))


def show_result(index,total,row,out):
    status=row["status"]
    passed=status.startswith("PREFLIGHT PASSED") and row["cleanup_exit"]==0
    icon=color("✓","2;224;136") if passed else color("✗","185;0;75")
    label="PASS • GUI/CI review pending" if passed else status
    print(f"  {icon} {index:>2}/{total}  {row['demo']:<9}  {label}")
    if not passed:
        hint={"STARTUP FAILED":"startup.log","PREFLIGHT FAILED":"preflight-console.log",
              "CLEANUP FAILED":"cleanup.log","BRANCH MISSING":"ref.log",
              "WORKTREE FAILED":"worktree.log"}.get(status,"error.txt")
        log_path=out/hint
        print("       Diagnose: "+str(log_path))
        if log_path.is_file():
            last=[t.strip() for t in log_path.read_text(errors="replace").splitlines()
                  if t.strip() and any(k in t.lower() for k in
                  ("no such file","not found","failed","error","fatal","missing"))]
            for line in last[-2:]:
                print("       "+line[:145])


def show_next_steps(output,archive,rows,exit_code):
    heading("BATCH COMPLETE • "+str(len(rows))+" demos checked")
    print("  Demo         Result")
    print("  ─────────────────────────────────────────────────────────")
    for row in rows:
        ok=row["status"].startswith("PREFLIGHT PASSED") and row["cleanup_exit"]==0
        word="PASS • evidence review pending" if ok else "HOLD • "+row["status"]
        print(f"  {row['demo']:<12} {color(word,'2;224;136' if ok else '185;0;75')}")
    print()
    print("  Evidence folder: "+str(output))
    print("  Complete ZIP:    "+str(archive))
    heading("NEXT • OPEN THE PRODUCTION PORTAL")
    print("  Open macOS Terminal and run these TWO exact commands:")
    print()
    print('  cd "'+str(output)+'"')
    print("  ./serve.sh")
    print()
    print("  Browser: http://127.0.0.1:8765/index.html")
    print("  Stop the viewer with Ctrl+C.")
    print("  New run after any fix: ./setup/run-all-demo-preflights.sh from repo root")
    print("  Every run creates a NEW timestamped folder. Previous proof stays intact.")
    if exit_code:
        print(color("  ATTENTION: Some demos failed. Open the logs in this batch; do not record from a failed preflight.","185;0;75"))
    else:
        print(color("  Terminal preflight passed. GUI, Actions and same-take CQA still required.","2;224;136"))

def references_ready(logs):
    parts=[logs/("preflight-step-%02d.log"%i) for i in range(1,5)]
    for p in parts:
        if not p.is_file():
            return False
        text=p.read_text(errors="replace")
        if "✔ PASS" not in text or "✘ FAIL" in text:
            return False
    return any("RESULT: 5 checks passed, 0 failed" in p.read_text(errors="replace")
               for p in logs.glob("preflight-*.log") if "-step-" not in p.name)

def narrator_groups(source):
    blocks=re.split(r"(?=^## Step [1-4]\b)",source,flags=re.M)
    groups=[]
    for block in blocks[1:5]:
        m=re.search(r"<summary>[^<]*<img[^>]*NARRATOR[^>]*>.*?</summary>\s*<table>(.*?)</table>",block,re.S|re.I)
        rows=[]
        if m:
            for shot,speech,n in re.findall(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(\d+)(?:\s+spoken\s+words)?</td>\s*</tr>",m.group(1),re.S|re.I):
                clean=lambda x: html.unescape(re.sub(r"<[^>]+>","",x)).strip()
                rows.append((clean(shot),clean(speech),int(n)))
        groups.append(rows)
    return groups

def write_documents(demo,sha,lab,out):
    lines=["# "+demo+" — Actual Step Commands And Output","",
           "Completed branch "+demo+"-after at "+sha,"",
           "Each output block was captured by the real preflight. For actual request IDs, counts and timestamps inspect logs/.producer.",""]
    for i,script in enumerate(sorted((lab/"steps").glob("0[1-4]-*.sh")),1):
        source=lab/"logs"/("preflight-step-%02d.log"%i)
        lines+=["## Step %d — ./steps/%s"%(i,script.name),"",FENCE+"text",source.read_text(errors="replace").rstrip(),FENCE,""]
    (out/"steps-and-output.md").write_text("\n".join(lines),encoding="utf-8")
    author=lab.parents[2]/"docs/.author-instructions"/(demo+".md")
    groups=narrator_groups(author.read_text()) if author.is_file() else []
    draft=["# "+demo+" — ElevenLabs Narration Draft","",
           "Evidence: actual completed-branch preflight at "+sha,"",
           "NOT FINAL. Confirm the Recorder's matching take and ZAP GUI / GitHub Actions evidence before freezing audio.",""]
    for i in range(1,5):
        draft+=["## Step "+str(i),""]
        rows=groups[i-1] if len(groups)>=i else []
        if not rows:
            draft+=["HOLD — author narration is missing; no content has been invented.",""]
        for shot,speech,count in rows:
            draft+=["**"+shot+" ("+str(count)+" words):** "+speech,""]
        draft+=["Evidence: logs/preflight-step-%02d.log"%i,"External GUI/CI proof: PENDING",""]
    draft+=["## Finalize with ChatGPT after recording","",
            "Upload this batch ZIP with real GUI/CI screenshots or run links. Ask ChatGPT to validate each output and produce frozen exact ElevenLabs narration without inventing values.",""]
    (out/"narration-draft.md").write_text("\n".join(draft),encoding="utf-8")
    from evidence_report import render
    render(demo, sha, lab, out)

def batch(ids,output,skip_setup):
    if sys.platform!="darwin":
        print("ERROR: live ZAP preflights require a Mac with Docker/Colima; no results simulated.",file=sys.stderr)
        return 2
    if not (ROOT/".git").is_dir():
        print("ERROR: run from a local Git checkout.",file=sys.stderr)
        return 2
    output.mkdir(parents=True)
    heading("SCRIPT DEVELOPMENT WITH ZAP • DEVELOPER PREFLIGHT")
    print("  Validating "+str(len(ids))+" completed branches in isolated temporary worktrees")
    print("  Every attempt preserves raw logs in its unique batch folder")
    print("  Batch folder: "+str(output))
    if not skip_setup and execute(["bash","./setup/setup-macos.sh"],ROOT,output/"setup.log",verbose=True):
        return 1
    if execute(["docker","info"],ROOT,output/"docker.log"):
        return 1
    if execute(["git","fetch","origin"],ROOT,output/"fetch.log"):
        return 1
    results=[]
    for index,demo in enumerate(ids,1):
        folder,startup=INDEX[demo]
        heading(f"DEMO {index}/{len(ids)} • {demo} • {demo}-after")
        out=output/demo
        out.mkdir()
        row={"demo":demo,"branch":demo+"-after","sha":"","status":"NOT VERIFIED","startup_exit":None,"preflight_exit":None,"cleanup_exit":None,"narration":"NOT GENERATED","step_commands":[]}
        with tempfile.TemporaryDirectory(prefix="zap-batch-"+demo+"-") as temp:
            worktree=Path(temp)/"checkout"
            lab=worktree/folder
            added=False
            try:
                remote="refs/remotes/origin/"+row["branch"]
                if execute(["git","rev-parse","--verify",remote],ROOT,out/"ref.log"):
                    row["status"]="BRANCH MISSING"
                    continue
                if execute(["git","worktree","add","--detach",str(worktree),remote],ROOT,out/"worktree.log"):
                    row["status"]="WORKTREE FAILED"
                    continue
                added=True
                row["sha"]=subprocess.check_output(["git","rev-parse","HEAD"],cwd=worktree,text=True).strip()
                row["step_commands"]=["./steps/"+p.name for p in sorted((lab/"steps").glob("0[1-4]-*.sh"))]
                if len(row["step_commands"]) != 4:
                    row["status"]="FOUR NAMED STEPS MISSING"
                    continue
                row["startup_exit"]=execute(["bash","./scripts/"+startup],lab,out/"startup.log")
                if row["startup_exit"]:
                    row["status"]="STARTUP FAILED"
                    continue
                row["preflight_exit"]=execute(["bash",str(worktree/"runtime/scripts/preflight_all_steps.sh"),str(lab)],lab,out/"preflight-console.log")
                if row["preflight_exit"] or not references_ready(lab/"logs"):
                    row["status"]="PREFLIGHT FAILED"
                    continue
                write_documents(demo,row["sha"],lab,out)
                row["status"]="PREFLIGHT PASSED; GUI/CI REVIEW PENDING"
                row["narration"]="DRAFT CREATED; NOT FROZEN"
            except (OSError,subprocess.SubprocessError) as e:
                row["status"]="ERROR"
                (out/"error.txt").write_text(str(e),encoding="utf-8")
            finally:
                if added:
                    try:
                        row["cleanup_exit"]=execute(["bash","./scripts/demo_down.sh"],lab,out/"cleanup.log")
                        if (lab/"logs").is_dir():
                            shutil.copytree(lab/"logs",out/"logs",dirs_exist_ok=True)
                        if row["cleanup_exit"]:
                            row["status"]="CLEANUP FAILED"
                    finally:
                        execute(["git","worktree","remove","--force",str(worktree)],ROOT,out/"worktree-remove.log")
                (out/"manifest.json").write_text(json.dumps(row,indent=2)+"\n",encoding="utf-8")
                results.append(row)
                show_result(index,len(ids),row,out)
    summary=["# Six-Demo Preflight Batch","",
        "Real completed-branch execution. A terminal PASS does not validate external GUI or CI footage.","",
        "| Demo | Source SHA | Execution | Narration |","|---|---|---|---|"]
    for row in results:
        summary.append("| "+row["demo"]+" | "+row["sha"][:12]+" | "+row["status"]+" | "+row["narration"]+" |")
    summary+=["","Each passing demo includes steps-and-output.md, logs/, production-guide.html and narration-draft.md.","","Run ./serve.sh in the actual batch folder to open the navigable local production HTML.","",
        "Upload this ZIP to ChatGPT with your recorded GUI/CI proof and request final per-step ElevenLabs narration. Never invent output.",""]
    (output/"README.md").write_text("\n".join(summary),encoding="utf-8")
    (output/"manifest.json").write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")
    # Assemble a portable, locally hosted author portal from the ACTUAL outputs.
    # Includes renderer and playbooks so a separate Narrator can import final
    # speech by ./refresh.sh without network access or rerunning ZAP.
    dashboard_ok=True
    try:
        from production_dashboard import render_dashboard
        tools_dir=output/"tools"
        tools_dir.mkdir(parents=True,exist_ok=True)
        for source in ("production_dashboard.py","production_plan.py","narration_handoff.py"):
            shutil.copy2(ROOT/"setup"/source,tools_dir/source)
        author_sources=ROOT/"docs/.author-instructions"
        shutil.copytree(author_sources,output/"author-playbooks",dirs_exist_ok=True)
        for source,destination in (("serve-production-deliverables.sh","serve.sh"),
                                   ("refresh-production-deliverables.sh","refresh.sh")):
            shutil.copy2(ROOT/"setup"/source,output/destination)
            (output/destination).chmod(0o755)
        for source in ("PRODUCTION_PORTAL_GUIDE.md","NARRATOR_NEXT_SESSION_PROMPT.md"):
            shutil.copy2(author_sources/source,output/source)
        render_dashboard(output,results,output/"author-playbooks")
    except (OSError,ValueError,KeyError,ImportError) as exc:
        dashboard_ok=False
        (output/"dashboard-error.txt").write_text(str(exc)+"\n",encoding="utf-8")
        print("ERROR: production HTML dashboard generation failed: "+str(exc),file=sys.stderr)
    archive=output.with_suffix(".zip")
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for file in sorted(output.rglob("*")):
            if file.is_file():
                z.write(file,Path(output.name)/file.relative_to(output))
    final_exit=0 if dashboard_ok and all(r["status"].startswith("PREFLIGHT PASSED") and r["cleanup_exit"]==0 for r in results) else 1
    show_next_steps(output,archive,results,final_exit)
    return final_exit

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--only",help="Comma separated demo IDs")
    p.add_argument("--skip-setup",action="store_true")
    p.add_argument("--dry-run",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    ids=a.only.split(",") if a.only else [d[0] for d in DEMOS]
    if not ids or len(ids)!=len(set(ids)) or any(x not in INDEX for x in ids):
        p.error("unknown or duplicate demo ID")
    output=(a.output or (Path.home()/"zap-course-deliverables"/("batch-"+datetime.now().strftime("%Y%m%d-%H%M%S-%f")))).expanduser().resolve()
    if a.dry_run:
        print("DRY RUN: No Docker, Git, setup or file writes.")
        for demo in ids:
            folder,startup=INDEX[demo]
            print(demo+"-after → "+folder+"/scripts/"+startup+" → shared four-step validator")
        print("Output: "+str(output))
        return 0
    if output.exists():
        p.error("output directory already exists; choose new --output")
    return batch(ids,output,a.skip_setup)
if __name__=="__main__":
    raise SystemExit(main())
