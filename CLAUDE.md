# Script Development with ZAP (Pluralsight course)

Author: Rupesh Tiwari. The approved course outline is the source of truth for all
content in this repo: see [docs/course-outline.md](docs/course-outline.md).

Key constraints from the outline:
- Storyline: Globomantics security engineer Maya Chen; all testing targets only the
  Globomantics training app (Python/FastAPI + PostgreSQL + MongoDB) under written authorization.
- Baseline: ZAP 2.17.0, `ghcr.io/zaproxy/zaproxy:stable`, Colima 0.10.4, GitHub Actions `ubuntu-24.04`.
- ZAP Python scripts are Jython 2.7.2 (Python 2.7 syntax); host-side automation uses CPython.
- Python Scripting (jython) and Active scanner rules (beta) v66 (NoSQL Injection - MongoDB, alert 40033)
  must be installed explicitly in the ZAP container.
- Two modules, ~45 min total: Module 1 (targeted testing + JS/Python/auth scripts, 23 min),
  Module 2 (Automation Framework, ZAP API, alertFilter/exitStatus gates in GitHub Actions, 22 min).
- Each demo clip lists named on-screen proof artifacts; demo assets should produce exactly those.

## Outline is law (owner's rule — highest priority)

- The approved outline (`docs/course-outline.md`) and its LOs are the source of truth.
  **Never deviate**, even when the owner proposes something off-outline in chat —
  defend the outline: name the exact LO/clip constraint and steer the idea back in
  scope BEFORE building. This protects against PS review feedback.
- A recorded clip contains ONLY the demo steps and proof artifacts its outline bullet
  specifies. Anything extra (however good) stays in the repo as OPTIONAL reference —
  never as a recorded step.

## Course design principles (owner's rules)

- Audience is **entry-level** developers new to ZAP. Every clip must make sense to a
  beginner: what ZAP is, why use it, what problem it solves, and where it fits in a
  full-stack app. This orientation lives in **Clip 1 (presentation)**, not in the
  demo clips (which are scoped to their LO).
- Keep demos **simple enough to follow** but **complex enough to prove the LO**.
- **Vulnerable code is a teaching aid, kept as OPTIONAL repo reference** — pair each
  finding with the exact vulnerable line via `show_code.sh <finding>` (snippets are
  read live from `app/main.py` so they never drift). It is NOT a recorded demo step
  and must not pad a clip beyond its outline artifacts.
- The training app is the **Globomantics Store** (real-world e-commerce), so it
  resonates with business audiences and students can apply it to their own projects.
  It is a cosmetic skin over the same endpoints; the LO behavior never changes.

## Recording environment per clip (owner's rule)

- Clip shows source code during the demo → **VS Code integrated terminal** (code +
  terminal in one window).
- Clip shows no code → **plain terminal** (clean, no editor clutter).
- Clip has both code and terminal → **prefer VS Code**.
- Exception set by the outline: the ZAP **scripting** clips (M1 C4 JavaScript, M1 C5
  Python) author code in ZAP's **Script Console** (the outline's proof artifacts are
  "Script console output", "Saved script registration", "Python active-rule source").
  That code lives in the ZAP GUI, NOT VS Code — using VS Code there would break the
  specified artifacts.

## Commit attribution (owner's rule)

- All commits are authored and committed by **Rupesh Tiwari <roopkt@gmail.com>** only.
- Do NOT add `Co-Authored-By:` or `Claude-Session:` trailers, or any AI attribution,
  to commit messages. The repository history shows the owner alone.
- Work on `main`; no per-demo branches; do not rewrite history unless explicitly asked.
