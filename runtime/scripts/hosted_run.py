#!/usr/bin/env python3
"""Find the GitHub Actions run that proves the current code, from the public Actions API.

    hosted_run.py <repo-root> <workflow-file> <branch> <path> [<path> ...]

Prints one line: run_id|conclusion|head_sha|runner_labels|covers_head|html_url|step_conclusions
covers_head is "yes" only when the run's commit is locally available and the watched
paths in the current working tree match that commit, including untracked authored files.
Unknown commits or failed comparisons produce "no"; branch identity alone is not proof.
Repository comes from HOSTED_REPO or the checkout's origin URL. GITHUB_TOKEN is used if set.
Prints nothing and exits 1 when no completed run exists.
"""
import json, os, re, subprocess, sys, tempfile, urllib.request

root, wf, branch, paths = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]

def git(*a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)

def worktree_covers(sha):
    """True when the watched paths in the WORKING TREE match the hosted run's commit.

    The learner brings the taught file into the working tree on the -before branch (often
    untracked), so comparing committed trees (sha vs HEAD) would always differ there and the
    proof could never pass. We stage the current working-tree content of the watched paths into
    a throwaway index (brought-in and untracked files included) and diff that tree against the
    run's commit, so the check reflects what the learner is actually about to scan. The learner's
    real index is never touched. Git handles content as bytes (including binary files);
    only the ASCII tree object ID is decoded. Any failed Git command denies coverage."""
    if not paths or git("cat-file", "-e", sha + "^{commit}").returncode != 0:
        return False
    with tempfile.NamedTemporaryFile(prefix="hosted-idx-") as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=tmp.name)
        def g(*a):
            return subprocess.run(["git", "-C", root, *a], env=env, capture_output=True)
        if g("read-tree", "HEAD").returncode != 0:
            return False
        if g("add", "-A", "--", *paths).returncode != 0:
            return False
        written = g("write-tree")
        if written.returncode != 0:
            return False
        tree = written.stdout.strip()
        if not re.fullmatch(rb"[0-9a-f]{40,64}", tree):
            return False
        return g("diff", "--quiet", sha, tree.decode("ascii"), "--", *paths).returncode == 0

repo = os.environ.get("HOSTED_REPO", "")
if not repo:
    m = re.search(r"github\.com[:/]([^/]+/[^/.]+?)(?:\.git)?/?$", git("remote", "get-url", "origin").stdout.strip())
    repo = m.group(1) if m else ""
if not repo:
    sys.exit(1)

def api(path):
    # The GitHub Actions API is called from inside CI (and locally). Two transient conditions make a
    # single call unreliable and used to flip the hosted proof red at random: an UNAUTHENTICATED call
    # (no GITHUB_TOKEN) shares a 60-request/hour budget across GitHub's runner IPs and is throttled with
    # HTTP 403, and the ?branch= filter is eventually consistent, so it can briefly return an empty list
    # right after a push. Retry transient HTTP (403/429/5xx), network errors and timeouts with backoff so
    # a hiccup does not read as "no hosted run exists". A 404 (genuinely absent) is not retried.
    import time, urllib.error
    last = None
    for attempt in range(5):
        req = urllib.request.Request("https://api.github.com/repos/%s/%s" % (repo, path),
                                     headers={"Accept": "application/vnd.github+json", "User-Agent": "globo-demo"})
        tok = os.environ.get("GITHUB_TOKEN")
        if tok:
            req.add_header("Authorization", "Bearer " + tok)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (403, 429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(2 ** attempt); continue
            raise
        except Exception as e:  # URLError, timeout, transient JSON/read errors
            last = e
            if attempt < 4:
                time.sleep(2 ** attempt); continue
            raise
    if last:
        raise last
    return {}

# Fetch the completed runs for this workflow + branch. The branch filter is eventually consistent, so an
# empty list right after a push is not proof that no run exists: retry a few times before giving up.
runs = []
import time as _time
for _attempt in range(5):
    try:
        runs = api("actions/workflows/%s/runs?branch=%s&status=completed&per_page=20" % (wf, branch)).get("workflow_runs", [])
    except Exception:
        sys.exit(1)
    if runs:
        break
    if _attempt < 4:
        _time.sleep(2 ** _attempt)
if not runs:
    sys.exit(1)
for run in runs:
    sha = run["head_sha"]
    # Even a run at HEAD must be compared with the current working tree. A dirty or
    # untracked taught file is not covered by a clean HEAD run. Unavailable commits and
    # temporary-index errors must not fall back to weaker branch/committed-tree proof.
    covers = "yes" if worktree_covers(sha) else "no"
    jobs = api("actions/runs/%s/jobs" % run["id"]).get("jobs", [])
    labels = ",".join(sorted({l for j in jobs for l in j.get("labels", [])}))
    steps = ";".join("%s=%s" % (s["name"], s.get("conclusion")) for j in jobs for s in j.get("steps", []))
    print("|".join([str(run["id"]), str(run.get("conclusion")), sha[:7], labels, covers, run["html_url"], steps]))
    sys.exit(0)
sys.exit(1)
