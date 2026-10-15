# Release Checkpoint for All Six Demos

## Required for each demo
- [ ] Approved outline and exact LO mapped to each of the four teaching steps
- [ ] Correct descriptive demo directory, before branch and after branch
- [ ] Both branches contain latest shared `main` foundation (zero commits behind)
- [ ] Starter does not expose completed answer; after contains expected solution or operational proof
- [ ] `./setup/setup-macos.sh` verified on target Mac and command-line prerequisites report READY
- [ ] `./scripts/demo_up.sh` / reset / preflight / down run independently in a fresh checkout
- [ ] Four conceptual `./steps/0N-*.sh` commands are visible, readable and stable
- [ ] Per-step observed evidence satisfies exactly its LO; no stale or substituted proof
- [ ] Preflight and recording evidence bound to same SHA and reconciled to recorded take
- [ ] GUI-only and CI-only proof separately captured where preflight cannot see it
- [ ] Recorder, Narrator and Editor sign off per step with real take ID
- [ ] Technical source-level CQA findings resolved or visibly and accurately bounded
- [ ] No public secrets, personal footage or team-private data in GitHub
- [ ] Move `docs/.author-instructions/` to PRIVATE WORKSPACE and remove public copy before Pluralsight submission

## Six-demo matrix to complete at freeze
| Demo | LO | Source-review confidence | Runtime verification | Final decision |
|---|---|---|---|---|
| M1 Demo 1 | EO1a/b/c | assess per step | NOT VERIFIED until tested | READY / HOLD |
| M1 Demo 2 | EO2a | assess per step | NOT VERIFIED until console shown | READY / HOLD |
| M1 Demo 3 | EO2b/c | assess per step | NOT VERIFIED until run | READY / HOLD |
| M2 Demo 1 | EO3a | assess per step | fresh Actions run + learner preflight | READY / HOLD |
| M2 Demo 2 | EO3b | assess per step | NOT VERIFIED until Insights shown | READY / HOLD |
| M2 Demo 3 | EO3c | assess per step | actual FP + High + exit code | READY / HOLD |

Each iteration shows current/previous confidence and delta; no score increases for documentation alone. Only verified technical changes unlock claims about runtime reliability.
