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
  read live from `runtime/app/main.py` so they never drift). It is NOT a recorded demo step
  and must not pad a clip beyond its outline artifacts.
- The training app is the **Globomantics Store** (real-world e-commerce), so it
  resonates with business audiences and students can apply it to their own projects.
  It is a cosmetic skin over the same endpoints; the LO behavior never changes.

## Commit attribution (owner's rule)

- All commits are authored and committed by **Rupesh Tiwari <roopkt@gmail.com>** only.
- Do NOT add `Co-Authored-By:` or `Claude-Session:` trailers, or any AI attribution,
  to commit messages. The repository history shows the owner alone.
- Branch policy (owner decision, 2026-10): the course uses **per-demo before/after
  branches** for distributed, isolated recording by a team. `main` is the **generic
  starter** (shared app, infra, runbooks, demo tooling — NO learner-authored solution
  files). Each demo has `m<module>-demo<N>-before` (its starting point: prerequisites
  present, this demo's own work not yet done) and `m<module>-demo<N>-after` (this
  demo completed). The independent `-after` branches contain each completed demonstration. Do not rewrite history unless explicitly asked.

## Learner-facing structure
- Root README is the navigation and macOS setup entry point.
- Demos live in `demos/module1-demos/` and `demos/module2-demos/` with descriptive folder names.
- Use `./steps/01-*.sh` through `./steps/04-*.sh` as the learner commands; internal engine scripts preserve approved behavior.
- Never commit Recorder/Narrator/Editor production material to the public repository.
- Keep all six branch pairs; `main` remains a generic starter without completed learner solutions.

## Directory naming and temporary production pack
- Canonical folders: `setup/`, `demos/`, `runtime/`, `docs/`; do not reintroduce clip-number-only folder names.
- Root files `README.md`, `CLAUDE.md`, `.gitignore`, `.env`, `docker-compose.yaml` are tool entry points and remain at root.
- Student documentation is readable and visual, with real evidence locations, GitHub-safe HTML, diagrams and semantic step executable filenames.
- The author-only pack under `docs/.author-instructions/` is temporarily committed at the owner's express direction; it is PUBLIC until moved to a private repo and removed from public history. Never imply dotfolders or gitignore provide privacy.
- Edit the course-approved source only for demonstrated technical defects. Keep before/after branch distinctions and CI path validation.

## Learner Documentation Contract — Read Before Writing READMEs

- Students receive the public GitHub repository as a standalone learning deliverable, **not the approved course outline**. The root and every demo README must state each relevant EO code **and its full approved plain-English learning-objective wording** from `docs/course-outline.md`. Do not show bare codes without explanation.
- The root README opens with the real engineering problem, why this tool is required, and practical skills/outcomes, then a complete LO table, annotated local/CI architecture, quick-start and standalone demo catalog. Avoid claims about live findings without the actual evidence.
- Each demo README opens with the situation and operator problem, complete EO description(s), the four named step commands, expected live proof and operator importance; include student-specific setup, branch role, safe comparison, preflight, cleanup and links/paths to real GUI/CI panels.
- GitHub presentation: semantic headings, compact GitHub-compatible HTML tables and `details`, deliberate diagrams (Mermaid for architecture/flow, checked-in SVGs when useful), labels legible on mobile screens and limited badges. Prefer clear problem-first education to decorative elements.
- **No large GitHub admonition alert boxes** (`[!WARNING]`, `[!TIP]`, `[!CAUTION]`, `[!NOTE]`, `[!IMPORTANT]`) in learner README pages. State authorized-use scope as a normal sentence. Do not suppress or misrepresent actual ZAP alert findings.
- Use actual vendor/component labels and correct boundaries in diagrams; GitHub Actions is not on the learner's Mac. For AWS or cloud courses use real documented cloud components, not invented icons, services or architecture links. Add a readable `Generated using ChatGPT` caption to AI-generated visual assets.
- Audit all Markdown and HTML links against the files on the relevant branch. A file intentionally absent in `*-before` must be identified as student-authored work; any reference image/source link must lead to a real file (possibly the explicitly labeled `*-after` solution), not a broken relative link.
- When changes touch shared READMEs or folder organization, update all numbered `before` and `after` branches without copying completed solution assets to starters. Verify zero branches behind `main`, correct before→after ancestry, and hosted static checks. Student code remains frozen unless an actual failure is proven.

## Author Hub And Clone-Once Recording Policy
- One clone per engineer, then switch demo branches sequentially; use worktrees only for concurrent views or separate local state. Never require a new clone for each demo by default.
- Preflight against the finished after branch first, save four verified step logs outside the checkout, clean up, then switch to before to author/record. A before branch with intentionally absent source cannot pass completed checks yet.
- Author landing README must have direct URLs to all author playbooks, before/after learner READMEs, and GitHub branch paths, with simple copyable shell commands and GitHub-compatible color/badge/HTML card layouts.
- Runtime values and GUI-only proof are not invented by normalization. Always check recording output against same source revision and matching preflight baselines.
- Set GitHub About description and topics via connected administrative actions when available; release/publish a tag only for a verified milestone, and publish Packages only for a real maintained distributable. When account integration lacks settings or release actions, prepare exact metadata and explicitly state it was not published.
