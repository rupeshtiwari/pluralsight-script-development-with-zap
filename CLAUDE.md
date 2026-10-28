# Script Development with ZAP (Pluralsight course)

Author: Rupesh Tiwari. The approved course outline is the source of truth for all
content in this repo. It is not a learner deliverable, so it lives in the private production
repository `rupeshtiwari/pluralsight-script-development-with-zap-production`
(`outline/course-outline.md`), together with the author guides, narration, recording/editing
plans, review records and the production-portal tooling.

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

- The approved outline (private repo, `outline/course-outline.md`) and its LOs are the source of truth.
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

## Directory naming
- Canonical folders: `setup/`, `demos/`, `runtime/`, `docs/`; do not reintroduce clip-number-only folder names.
- Root files `README.md`, `CLAUDE.md`, `.gitignore`, `.env`, `docker-compose.yaml` are tool entry points and remain at root.
- Student documentation is readable and visual, with real evidence locations, GitHub-safe HTML, diagrams and semantic step executable filenames.
- Production material is private (see "Public and private repositories" below). Never imply dotfolders or `.gitignore` provide privacy; git history still holds the earlier public copies of the author pack.
- Edit the course-approved source only for demonstrated technical defects. Keep before/after branch distinctions and CI path validation.

## Learner Documentation Contract — Read Before Writing READMEs

- Students receive the public GitHub repository as a standalone learning deliverable, **not the approved course outline**. The root and every demo README must state each relevant EO code **and its full approved plain-English learning-objective wording** from the approved outline. Do not show bare codes without explanation.
- The root README opens with the real engineering problem, why this tool is required, and practical skills/outcomes, then a complete LO table, annotated local/CI architecture, quick-start and standalone demo catalog. Avoid claims about live findings without the actual evidence.
- Each demo README opens with the situation and operator problem, complete EO description(s), the four named step commands, expected live proof and operator importance; include student-specific setup, branch role, safe comparison, cleanup and links/paths to real GUI/CI panels.
- GitHub presentation: semantic headings, compact GitHub-compatible HTML tables and `details`, deliberate diagrams (Mermaid for architecture/flow, checked-in SVGs when useful), labels legible on mobile screens and limited badges. Prefer clear problem-first education to decorative elements.
- **No large GitHub admonition alert boxes** (`[!WARNING]`, `[!TIP]`, `[!CAUTION]`, `[!NOTE]`, `[!IMPORTANT]`) in learner README pages. State authorized-use scope as a normal sentence. Do not suppress or misrepresent actual ZAP alert findings.
- Use actual vendor/component labels and correct boundaries in diagrams; GitHub Actions is not on the learner's Mac. For AWS or cloud courses use real documented cloud components, not invented icons, services or architecture links. Add a readable `Generated using ChatGPT` caption to AI-generated visual assets.
- Audit all Markdown and HTML links against the files on the relevant branch. A file intentionally absent in `*-before` must be identified as student-authored work; any reference image/source link must lead to a real file (possibly the explicitly labeled `*-after` solution), not a broken relative link.
- When changes touch shared READMEs or folder organization, update all numbered `before` and `after` branches without copying completed solution assets to starters. Verify zero branches behind `main`, correct before→after ancestry, and hosted static checks. Student code remains frozen unless an actual failure is proven.

## Current Student Contract
- No six per-demo `scripts/preflight_check.sh` wrappers should exist. The course-wide batch preflight is production tooling in the private repository.
- The shared internal source of execution remains `runtime/scripts/preflight_all_steps.sh` and each demo's existing `_run_step.sh` and `_steps.sh`; do not delete those engines.
- Every student demo README is a human-centered, problem-first, prescriptive guide with an exact terminal/GUI location, demo-specific startup, four step commands, structured illustrative output fields, interpretation and LO purpose. Only Step 1 expanded; Steps 2–4 collapsed.
- The student course README groups approved learning objectives under readable Module 1 / Module 2 demo names and includes the unlinked 'Watch the Pluralsight course' label to replace only after publication.
- Pluralsight palette for instructional graphics and console: Transform Pink #FF1675, Inky Blue #130F25, Blue #00A3FF, Purple #770EF7, Yellow #FFC942, Green #02E088. Reserve #B9004B for actual STOP/FAIL. AI-generated imagery must receive the readable credit 'Generated using ChatGPT'; avoid unsupported diagram claims and never treat expected values as live output.
- Technical claims require same-run proof: request, response, alert/rule, risk/confidence, or gate report and exact process exit. Never raise source-review or production confidence to 95% through a prose rewrite alone.

## Binding code rules (October 16, 2026)

- **Proven worktree defect fix:** Every demo `scripts/lab-up.sh`, `lab-down.sh`, and `lab-reset.sh` must resolve the repository root from exactly four parent levels below `demos/moduleN-demos/<demo>/scripts/`, not five. Keep the offline executable-wrapper test; a GitHub layout check cannot detect a broken runtime path by itself.
- **Security evidence exception:** A routine ping of `/admin/ping` cannot establish command injection. The approved fourth step now confirms a harmless injected marker from the authorized training target. Preserve this genuine proof, not a speculative `✔ PASS`.

## Public and private repositories (owner rule, 2026-10-16)

- This public repository is learner-only and must work without access to anything private.
- Author guides, the outline, narration, recording/editing plans, review records, the batch
  preflight and the production portal live in the private repository
  `rupeshtiwari/pluralsight-script-development-with-zap-production`. Never add them here
  (`runtime/scripts/check_repository_layout.py` fails if they reappear).
- After changing this repository, update the private repository in the same task: run its
  `tools/source_lock.py check`, update every asset it flags, then relock. Information flows
  public → private only.

## Terminal file paths (owner, October 28, 2026)

Use the module folder as the display root in terminal output: `module2-demos/m2-demo2-zap-api-scan-evidence/logs/report.json`. Omit personal home, repository and `demos/` prefixes. Apply the shared path display helper before wrapping all terminal field values, including JSON-driven rows. Preserve actual file locations, raw reports, URLs, container paths and authentication evidence. Use a plain `$ ` prompt with no username or hostname. Keep this formatter policy and its regression test in CI for all modules and future demos.
