#!/usr/bin/env python3
"""Maintainers' repository quality check (static, no Docker required).

Reports, with actionable file paths and reasons:
  - production-only wording in learner-facing docs
  - per-demo README: setup + cleanup + preflight references, before/after links
  - demo branch naming compliance / missing demo branches (if a remote is given)

This is maintainers' tooling. It does NOT run ZAP or validate runtime behavior —
use the single setup/run-all-demo-preflights.sh command on a Mac Docker host for that.

Usage:
  python3 runtime/scripts/repo_quality_check.py            # check the working tree
  python3 runtime/scripts/repo_quality_check.py --branches # also check remote branch names
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Demo folder <-> branch stem. (Clips 1-2 of each module are presentation, no folder.)
DEMOS = [
    ("demos/module1-demos/m1-demo1-targeted-injection-xss-csrf", "m1-demo1"),
    ("demos/module1-demos/m1-demo2-javascript-http-sender", "m1-demo2"),
    ("demos/module1-demos/m1-demo3-python-scanning-authentication", "m1-demo3"),
    ("demos/module2-demos/m2-demo1-authenticated-zap-github-actions", "m2-demo1"),
    ("demos/module2-demos/m2-demo2-zap-api-scan-evidence", "m2-demo2"),
    ("demos/module2-demos/m2-demo3-security-quality-gates", "m2-demo3"),
]

# Internal production wording that must not appear in learner-facing docs.
# Specific phrases only — NOT broad words like "record" (legitimate in
# "Record an alert disposition"), so legitimate technical language is kept.
PROD_PATTERNS = [
    r"recording budget",
    r"timing allocation",
    r"edited out in post",
    r"recording focus",
    r"before recording",
    r"recording quality gate",
    r"full-screen (?:recording|capture|browser)",
    r"mobile-readable",
    r"clean cuts",
    r"screen recording",
    r"record it in\b",
    r"confidence\s*[:=]\s*\d{1,3}\s*%",   # internal CQA confidence scores
]

errors = []   # (severity, path, reason)


def add(sev, path, reason):
    errors.append((sev, path, reason))


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def check_production_wording():
    for dirpath, _dirs, files in os.walk(ROOT):
        if "/.git" in dirpath or "/.author-instructions" in dirpath:
            continue
        for name in files:
            if not name.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
            # The maintainers' policy docs may legitimately name these terms;
            # learner-facing assets (demo + root READMEs, docs/) may not.
            text = read(os.path.join(dirpath, name)).lower()
            for pat in PROD_PATTERNS:
                for m in re.finditer(pat, text):
                    line = text[: m.start()].count("\n") + 1
                    add("REQUIRED FIX", "%s:%d" % (rel, line),
                        "production-only wording: %r" % m.group(0))


def check_demo_readmes():
    for folder, stem in DEMOS:
        rp = os.path.join(ROOT, folder, "README.md")
        if not os.path.exists(rp):
            add("BLOCKER", "%s/README.md" % folder, "demo README missing")
            continue
        text = read(rp)
        low = text.lower()
        if "## setup" not in low and "setup" not in low:
            add("REQUIRED FIX", "%s/README.md" % folder, "no Setup section")
        if "demo_down.sh" not in text:
            add("REQUIRED FIX", "%s/README.md" % folder,
                "no cleanup reference (scripts/demo_down.sh)")
        if "run-all-demo-preflights.sh" not in text:
            add("OPTIONAL POLISH", "%s/README.md" % folder,
                "no link to batch preflight (setup/run-all-demo-preflights.sh)")
        # setup / cleanup scripts present on disk
        for script in ("demo_up.sh", "demo_down.sh"):
            sp = os.path.join(ROOT, folder, "scripts", script)
            if not os.path.exists(sp):
                add("REQUIRED FIX", "%s/scripts/%s" % (folder, script),
                    "expected demo script missing")


def check_branches():
    try:
        out = subprocess.check_output(
            ["git", "ls-remote", "--heads", "origin"], cwd=ROOT,
            stderr=subprocess.DEVNULL).decode()
    except Exception as exc:  # noqa: BLE001
        add("OPTIONAL POLISH", "(git)", "could not list remote branches: %s" % exc)
        return
    heads = {ln.split("refs/heads/")[1] for ln in out.splitlines() if "refs/heads/" in ln}
    expected = {"main"}
    for _folder, stem in DEMOS:
        expected |= {stem + "-before", stem + "-after"}
    for want in sorted(expected):
        if want not in heads:
            add("BLOCKER", "(branch)", "missing required branch: %s" % want)
    for h in sorted(heads):
        if h.startswith("demo/"):
            add("OPTIONAL POLISH", "(branch)",
                "old-style branch name still present: %s" % h)


def main():
    check_production_wording()
    check_demo_readmes()
    if "--branches" in sys.argv:
        check_branches()

    order = {"BLOCKER": 0, "REQUIRED FIX": 1, "OPTIONAL POLISH": 2}
    errors.sort(key=lambda e: (order.get(e[0], 9), e[1]))
    if not errors:
        print("repo_quality_check: PASS — no issues found")
        return 0
    counts = {}
    for sev, path, reason in errors:
        counts[sev] = counts.get(sev, 0) + 1
        print("%-14s %s\n               %s" % (sev, path, reason))
    print("\nsummary: " + ", ".join("%d %s" % (counts[k], k) for k in
                                     sorted(counts, key=lambda k: order.get(k, 9))))
    # Only BLOCKER / REQUIRED FIX fail the check.
    return 1 if (counts.get("BLOCKER") or counts.get("REQUIRED FIX")) else 0


if __name__ == "__main__":
    sys.exit(main())
