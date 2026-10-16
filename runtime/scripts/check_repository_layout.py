#!/usr/bin/env python3
"""Fail-closed, dependency-free structural validation for every student branch."""
from pathlib import Path
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LABS = {
    "m1-demo1": "demos/module1-demos/m1-demo1-targeted-injection-xss-csrf",
    "m1-demo2": "demos/module1-demos/m1-demo2-javascript-http-sender",
    "m1-demo3": "demos/module1-demos/m1-demo3-python-scanning-authentication",
    "m2-demo1": "demos/module2-demos/m2-demo1-authenticated-zap-github-actions",
    "m2-demo2": "demos/module2-demos/m2-demo2-zap-api-scan-evidence",
    "m2-demo3": "demos/module2-demos/m2-demo3-security-quality-gates",
}
SOLUTIONS = {
    "m1-demo2": ["demos/module1-demos/m1-demo2-javascript-http-sender/zap-scripts/globomantics-marker.js"],
    "m1-demo3": ["demos/module1-demos/m1-demo3-python-scanning-authentication/zap-scripts/globomantics-active-rule.py",
                 "demos/module1-demos/m1-demo3-python-scanning-authentication/zap-scripts/globomantics-auth.py"],
    "m2-demo1": ["demos/module2-demos/m2-demo1-authenticated-zap-github-actions/ci/af-plan.yaml"],
    "m2-demo3": ["demos/module2-demos/m2-demo3-security-quality-gates/ci/gate-plan.yaml"],
}
failures = []

def must(cond, description):
    if not cond:
        failures.append(description)

for folder in ("setup", "demos", "runtime", "docs"):
    must((ROOT / folder).is_dir(), f"missing directory: {folder}")
for name in ("README.md", "CLAUDE.md", ".gitignore", ".env", "docker-compose.yaml"):
    must((ROOT / name).is_file(), f"missing root entry point: {name}")
for old in ("before-running-demo-run-this", "app", "data", "zap", "scripts", "module1", "module2", "env-setup"):
    must(not (ROOT / old).exists(), f"deprecated root folder: {old}")
for f in ("runtime/app/main.py", "runtime/zap/entrypoint.sh",
          "runtime/scripts/lib.sh", "runtime/scripts/demo_up.sh",
          "runtime/scripts/demo_down.sh", "runtime/scripts/preflight_all_steps.sh",
          "setup/setup-macos.sh"):
    must((ROOT / f).is_file(), f"missing shared runtime file: {f}")

for lab, rel in LABS.items():
    path = ROOT / rel
    must((path / "README.md").is_file(), f"{lab}: README missing")
    steps = sorted((path / "steps").glob("[0-9][0-9]-*.sh"))
    must(len(steps) == 4, f"{lab}: expected four concept-named step scripts, found {len(steps)}")
    if len(steps) == 4:
        must([x.name[:2] for x in steps] == ["01", "02", "03", "04"], f"{lab}: step order must be 01 through 04")
    for step in steps:
        must(os.access(step, os.X_OK), f"{lab}: step not executable: {step.name}")
        must("_run_step.sh" in step.read_text(), f"{lab}: named step must reuse frozen step engine: {step.name}")
    for name in ("demo_up.sh", "demo_down.sh", "_run_step.sh", "_steps.sh"):
        must((path / "scripts" / name).is_file(), f"{lab}: missing scripts/{name}")
    if (path / "README.md").exists():
        body = (path / "README.md").read_text(encoding="utf-8")
        for step in steps:
            must(step.name in body, f"{lab}: README missing named command {step.name}")
        must("run-all-demo-preflights.sh" in body, f"{lab}: README missing batch preflight instructions")
        must("demo_down.sh" in body, f"{lab}: README missing teardown instructions")

branch = os.environ.get("GITHUB_REF_NAME", "").strip() or subprocess.run(
    ["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True
).stdout.strip()
if branch == "main":
    for lab, files in SOLUTIONS.items():
        for f in files:
            must(not (ROOT / f).exists(), f"main leaks finished {lab} answer: {f}")
for lab, files in SOLUTIONS.items():
    if branch == lab + "-before":
        for f in files:
            must(not (ROOT / f).exists(), f"{branch} exposes its finished answer: {f}")
    if branch == lab + "-after":
        for f in files:
            must((ROOT / f).is_file(), f"{branch} missing completed artifact: {f}")

print(f"Structural validation on {branch or '(detached)'}: " + ("PASS" if not failures else "FAIL"))
for failure in failures:
    print("ERROR: " + failure)
sys.exit(1 if failures else 0)
