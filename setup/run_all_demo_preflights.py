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

def execute(command,cwd,log):
    with log.open("w",encoding="utf-8") as f:
        proc=subprocess.Popen(command,cwd=cwd,stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,text=True,errors="replace")
        for line in proc.stdout:
            print(line,end="",flush=True)
            f.write(line)
        return proc.wait()

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
    if not skip_setup and execute(["bash","./setup/setup-macos.sh"],ROOT,output/"setup.log"):
        return 1
    if execute(["docker","info"],ROOT,output/"docker.log"):
        return 1
    if execute(["git","fetch","origin"],ROOT,output/"fetch.log"):
        return 1
    results=[]
    for demo in ids:
        folder,startup=INDEX[demo]
        out=output/demo
        out.mkdir()
        row={"demo":demo,"branch":demo+"-after","sha":"","status":"NOT VERIFIED","startup_exit":None,"preflight_exit":None,"cleanup_exit":None,"narration":"NOT GENERATED"}
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
    summary=["# Six-Demo Preflight Batch","",
        "Real completed-branch execution. A terminal PASS does not validate external GUI or CI footage.","",
        "| Demo | Source SHA | Execution | Narration |","|---|---|---|---|"]
    for row in results:
        summary.append("| "+row["demo"]+" | "+row["sha"][:12]+" | "+row["status"]+" | "+row["narration"]+" |")
    summary+=["","Each passing demo includes steps-and-output.md, logs/, production-guide.html and narration-draft.md.","",
        "Upload this ZIP to ChatGPT with your recorded GUI/CI proof and request final per-step ElevenLabs narration. Never invent output.",""]
    (output/"README.md").write_text("\n".join(summary),encoding="utf-8")
    (output/"manifest.json").write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")
    archive=output.with_suffix(".zip")
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for file in sorted(output.rglob("*")):
            if file.is_file():
                z.write(file,Path(output.name)/file.relative_to(output))
    print("\nEVIDENCE: "+str(output)+"\nUPLOAD THIS ZIP: "+str(archive))
    return 0 if all(r["status"].startswith("PREFLIGHT PASSED") for r in results) else 1

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
    output=(a.output or (Path.home()/"zap-course-deliverables"/("batch-"+datetime.now().strftime("%Y%m%d-%H%M%S")))).expanduser().resolve()
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
