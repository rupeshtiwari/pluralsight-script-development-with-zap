#!/usr/bin/env python3
"""Guardrail: a demo's -before branch must NEVER break when a student follows the steps.

Owner's hard rule (2026-10): we record every demo FROM the -before branch. When a student switches
to a -before branch and runs the steps, the ONLY thing they may hit that is not a clean pass is the
friendly "AUTHOR THIS FIRST" cue for the one artifact the clip teaches them to write on camera. They
must never hit a missing prerequisite, a missing helper, a broken path, or a syntax error. Everything
the demo needs to proceed that is NOT the on-camera lesson must be pre-present on -before. -after is
-before plus exactly the code authored/tweaked on camera.

This validator proves that invariant statically, from one checkout, using git refs for both branches:

  1. before/after invariant  the ONLY files that differ between -before and -after under the demo
     folder are that demo's declared TAUGHT set (the on-camera authored artifacts). A prerequisite
     accidentally missing from -before would show up here and FAIL, naming the file to pre-add.
  2. every taught artifact is GATED  each taught file that is absent on -before is guarded by a
     need_author cue in that demo's _steps.sh, so its absence is a teaching prompt, never a crash.
  3. the movie has all its reels  -before has exactly four named step scripts plus the shared
     engine (_steps.sh, _run_step.sh, lib.sh, fmt.py).
  4. no missing prerequisite  every *_HOST file the steps depend on is present on -before, unless it
     is a gated taught artifact.
  5. it parses  every step script, _steps.sh and lib.sh is `bash -n` clean on -before; fmt.py compiles.

    python3 runtime/scripts/check_before_never_breaks.py            # validate all demos
    python3 runtime/scripts/check_before_never_breaks.py m1-demo2   # one demo

Exit 0 = every demo's -before is safe to hand a student. Non-zero = a listed violation to fix.
This runs with no Docker and no ZAP, so it can be run as many times as you like and in CI.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile

# demo key -> folder under the repo
DEMO_DIR = {
    "m1-demo1": "demos/module1-demos/m1-demo1-targeted-injection-xss-csrf",
    "m1-demo2": "demos/module1-demos/m1-demo2-javascript-http-sender",
    "m1-demo3": "demos/module1-demos/m1-demo3-python-scanning-authentication",
    "m2-demo1": "demos/module2-demos/m2-demo1-authenticated-zap-github-actions",
    "m2-demo2": "demos/module2-demos/m2-demo2-zap-api-scan-evidence",
    "m2-demo3": "demos/module2-demos/m2-demo3-security-quality-gates",
}

# The on-camera authored artifacts per demo (repo-relative). This is the ONLY thing allowed to differ
# between -before and -after. Empty = the clip teaches no file (it runs a scan), so -before == -after.
def _p(demo: str, *rel: str) -> set:
    return {f"{DEMO_DIR[demo]}/{r}" for r in rel}

TAUGHT = {
    "m1-demo1": set(),
    "m1-demo2": _p("m1-demo2", "zap-scripts/globomantics-marker.js"),
    "m1-demo3": _p("m1-demo3", "zap-scripts/globomantics-active-rule.py", "zap-scripts/globomantics-auth.py"),
    "m2-demo1": _p("m2-demo1", "ci/af-plan.yaml"),
    "m2-demo2": set(),
    "m2-demo3": _p("m2-demo3", "ci/gate-plan.yaml"),
}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def ref_for(branch: str) -> str:
    """Prefer origin/<branch> (always current after a fetch); fall back to a local branch."""
    if git("rev-parse", "--verify", "--quiet", f"origin/{branch}").strip():
        return f"origin/{branch}"
    if git("rev-parse", "--verify", "--quiet", branch).strip():
        return branch
    return ""


def tree(ref: str) -> set:
    return set(git("ls-tree", "-r", "--name-only", ref).splitlines())


def blob(ref: str, path: str) -> str:
    return git("show", f"{ref}:{path}")


def bash_n(text: str, name: str) -> str:
    """Return '' if `bash -n` is clean, else the error."""
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as f:
        f.write(text)
        tmp = f.name
    try:
        r = subprocess.run(["bash", "-n", tmp], capture_output=True, text=True)
        return "" if r.returncode == 0 else r.stderr.strip().replace(tmp, name)
    finally:
        os.unlink(tmp)


def check_demo(demo: str) -> list:
    folder = DEMO_DIR[demo]
    taught = TAUGHT[demo]
    before, after = ref_for(f"{demo}-before"), ref_for(f"{demo}-after")
    problems = []
    if not before:
        return [f"{demo}: cannot find {demo}-before (fetch origin first)"]
    if not after:
        return [f"{demo}: cannot find {demo}-after (fetch origin first)"]

    # 1. before/after invariant: only the taught set may differ, under the demo folder.
    diff = git("diff", "--name-status", before, after, "--", folder)
    changed = {ln.split("\t", 1)[1].strip() for ln in diff.splitlines() if "\t" in ln}
    extra = changed - taught
    missing = taught - changed
    for f in sorted(extra):
        problems.append(f"{demo}: {f} differs between -before and -after but is NOT a declared taught "
                        f"artifact. If it is a prerequisite, pre-add it to -before so the two match; if "
                        f"it is taught on camera, add it to TAUGHT.")
    for f in sorted(missing):
        problems.append(f"{demo}: declared taught artifact {f} does not actually differ between "
                        f"-before and -after (is it present on -before by mistake, or already on both?).")

    btree = tree(before)

    # 2. every taught artifact absent on -before must be GATED by a need_author cue.
    steps_path = f"{folder}/scripts/_steps.sh"
    steps_src = blob(before, steps_path) if steps_path in btree else ""
    for f in sorted(taught):
        if f in btree:
            continue  # present on -before (a tweak, not an absent-and-gated artifact) -> no gate needed
        base = os.path.basename(f)
        if "need_author" not in steps_src or base not in steps_src:
            problems.append(f"{demo}: taught artifact {base} is absent on -before but not guarded by a "
                            f"need_author cue in {steps_path}, so the step would crash instead of "
                            f"prompting the author.")

    # 3. the movie has all its reels: four named steps + the shared engine, on -before.
    steps = sorted(p for p in btree if re.match(rf"^{re.escape(folder)}/steps/0[1-4]-.*\.sh$", p))
    if len(steps) != 4:
        problems.append(f"{demo}: expected four steps/0[1-4]-*.sh on -before, found {len(steps)}.")
    for needed in ("scripts/_steps.sh", "scripts/_run_step.sh"):
        if f"{folder}/{needed}" not in btree:
            problems.append(f"{demo}: {needed} is missing on -before.")
    for shared in ("runtime/scripts/lib.sh", "runtime/scripts/fmt.py"):
        if shared not in btree:
            problems.append(f"{demo}: shared engine {shared} is missing on -before.")

    # 4. no missing prerequisite: every *_HOST file the steps depend on exists on -before (or is gated).
    for var, root, rel in re.findall(r'(\w+_HOST)="\$\{(DEMO_DIR|REPO_ROOT)\}/([^"]+)"', steps_src):
        path = f"{folder}/{rel}" if root == "DEMO_DIR" else rel
        if path in btree or path in taught:
            continue
        problems.append(f"{demo}: {var} points at {path}, which is NOT on -before and is NOT a taught "
                        f"artifact. A student would hit a missing prerequisite. Pre-add it to -before.")

    # 5. it parses: bash -n every step script + the engine, on -before; fmt.py compiles.
    for p in steps + [f"{folder}/scripts/_steps.sh", f"{folder}/scripts/_run_step.sh",
                      "runtime/scripts/lib.sh"]:
        if p in btree:
            err = bash_n(blob(before, p), p)
            if err:
                problems.append(f"{demo}: syntax error on -before in {p}: {err.splitlines()[0]}")
    if "runtime/scripts/fmt.py" in btree:
        try:
            compile(blob(before, "runtime/scripts/fmt.py"), "fmt.py", "exec")
        except SyntaxError as e:
            problems.append(f"{demo}: fmt.py does not compile on -before: {e}")

    return problems


def main(argv) -> int:
    demos = [a for a in argv if a in DEMO_DIR] or list(DEMO_DIR)
    git("fetch", "origin", "--quiet")
    all_problems, ok = [], []
    for d in demos:
        probs = check_demo(d)
        if probs:
            all_problems += probs
        else:
            ok.append(d)
    for d in ok:
        print(f"  PASS  {d}-before never breaks (only its taught artifact is absent, and it is gated)")
    if all_problems:
        print("\nBEFORE-BRANCH GUARDRAIL FAILURES:")
        for p in all_problems:
            print(f"  FAIL  {p}")
        print(f"\n{len(all_problems)} violation(s). A -before branch must run the student steps without "
              f"breaking; fix each above.")
        return 1
    print(f"\nAll {len(demos)} demo -before branches pass the never-breaks guardrail.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
