#!/bin/bash
# =============================================================================
# Preflight / demo-step validator — m2-c5
# "Enforce ZAP quality gates in GitHub Actions"  (TO3, EO3c)
# =============================================================================
# AUTHOR tooling. Runs every demo step in the SAME ORDER as the README, printing
# the command a learner runs for each step followed by that step's output, so the
# plain-text log in logs/ can be checked against the learning objective before you
# record. Exits non-zero if any step fails.
# =============================================================================
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO_DIR="$(cd "${HERE}/.." && pwd)"
LOG_DIR="${DEMO_DIR}/logs"
mkdir -p "${LOG_DIR}"
STAMP="$(date +%Y%m%d-%H%M%S)"
RAW_LOG="${LOG_DIR}/preflight-${STAMP}.ansi.log"
LOG="${LOG_DIR}/preflight-${STAMP}.log"

# shellcheck disable=SC1091
source "${HERE}/_steps.sh"
export FORCE_COLOR=1

runstep() { # <n> <title> <fn>
    echo; echo
    fm section "STEP $1 — $2"
    fm item "command: ./scripts/demo_step.sh $1"
    echo
    "$3"
}

main() {
    fm header "Preflight — Enforce ZAP quality gates in GitHub Actions" \
              "Proves the gate works end to end: a benign finding is filtered to False Positive before scanning, the job order applies it, and exitStatus turns the remaining High-risk alert into a non-zero process exit code that blocks the build (EO3c)."
    fm star "Scope" "local Globomantics training app only (compose network)" focus

    echo; echo
    if ensure_ready; then
        pass "the stack is up and the headless gate run produced a report and an exit code"
    else
        summary; return 1
    fi

    runstep 1 "False Positive alert filter (EO3c)"    step1_fp_filter
    runstep 2 "Automation Framework job order (EO3c)" step2_job_order
    runstep 3 "Gate JSON report and exit code (EO3c)" step3_gate_exit
    runstep 4 "Filtered alert report (EO3c)"          step4_filtered_report

    summary
    [ "${FAIL}" -eq 0 ]
}

summary() {
    echo; echo
    fm header "Preflight summary" "Green means the gate filters, orders, reports, and decides exactly as the runbook describes."
    if [ "${FAIL}" -eq 0 ]; then
        fm star "Result" "${PASS} checks passed, 0 failed" focus
        fm note "Aligned with EO3c (TO3). Ready to record."
    else
        fm star "Result" "${PASS} passed, ${FAIL} FAILED" focus
        echo
        fm section "Prompt to fix this demo"
        fm item "\"Read the latest log in module2/m2-c5-enforce-zap-quality-gates-in-github-actions/logs/, find every FAIL, fix ci/gate-plan.yaml or the step query in scripts/_steps.sh (never weaken the check), then re-run scripts/preflight_check.sh until all four steps pass.\""
    fi
}

{ main; } 2>&1 | tee "${RAW_LOG}"
rc=${PIPESTATUS[0]}
sed 's/\x1b\[[0-9;]*m//g' "${RAW_LOG}" > "${LOG}"
echo
echo "plain-text log for review: ${LOG}"
exit "${rc}"
