#!/usr/bin/env python3
"""Find the GitHub Actions run that proves the current code, from the public Actions API.

    hosted_run.py <repo-root> <workflow-file> <branch> <path> [<path> ...]

Prints one line: run_id|conclusion|head_sha|runner_labels|covers_head|html_url|step_conclusions
covers_head is "yes" when the run's commit is HEAD, or when git shows no change to the
given paths between that commit and HEAD (so the hosted run still describes this code).
Repository comes from HOSTED_REPO or the checkout's origin URL. GITHUB_TOKEN is used if set.
Prints nothing and exits 1 when no completed run exists.
"""
import json, os, re, subprocess, sys, urllib.request

root, wf, branch, paths = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]

def git(*a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)

repo = os.environ.get("HOSTED_REPO", "")
if not repo:
    m = re.search(r"github\.com[:/]([^/]+/[^/.]+?)(?:\.git)?/?$", git("remote", "get-url", "origin").stdout.strip())
    repo = m.group(1) if m else ""
head = os.environ.get("HOSTED_HEAD") or git("rev-parse", "HEAD").stdout.strip()
if not repo:
    sys.exit(1)

def api(path):
    req = urllib.request.Request("https://api.github.com/repos/%s/%s" % (repo, path),
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "globo-demo"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", "Bearer " + tok)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

try:
    runs = api("actions/workflows/%s/runs?branch=%s&status=completed&per_page=20" % (wf, branch)).get("workflow_runs", [])
except Exception:
    sys.exit(1)
for run in runs:
    sha = run["head_sha"]
    if sha == head:
        covers = "yes"
    elif git("cat-file", "-e", sha + "^{commit}").returncode == 0:
        # Same repo: the run covers this code when the watched paths are unchanged since it.
        covers = "yes" if git("diff", "--quiet", sha, head, "--", *paths).returncode == 0 else "no"
    else:
        # The run is in a different repo (e.g. the public course repo while testing a mirror):
        # branch-level proof. The calling step still checks the specific step's conclusion
        # (a gate run concludes "failure" by design, so we do not filter on run conclusion here).
        covers = "branch"
    jobs = api("actions/runs/%s/jobs" % run["id"]).get("jobs", [])
    labels = ",".join(sorted({l for j in jobs for l in j.get("labels", [])}))
    steps = ";".join("%s=%s" % (s["name"], s.get("conclusion")) for j in jobs for s in j.get("steps", []))
    print("|".join([str(run["id"]), str(run.get("conclusion")), sha[:7], labels, covers, run["html_url"], steps]))
    sys.exit(0)
sys.exit(1)
