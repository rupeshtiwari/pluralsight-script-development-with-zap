#!/bin/bash
# =============================================================================
# Preflight / demo-step validator — m2-c4
# "Query the ZAP API and inspect scan evidence"  (TO3, EO3b)
# =============================================================================
# AUTHOR tooling. Runs every demo step in the SAME ORDER as the README, printing
# the command a learner runs for each step followed by that step's output, so the
# plain-text log in logs/ can be checked against the learning objective before
# you record. Exits non-zero if any step fails.
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

# Print the exact command the learner runs for this step, then run it.
runstep() { # <n> <title> <fn>
    echo; echo
    fm section "STEP $1 — $2"
    fm item "command: ./scripts/demo_step.sh $1"
    echo
    "$3"
}

main() {
    fm header "Preflight — Query the ZAP API and inspect scan evidence" \
              "Proves each step inspects a finished authenticated scan THROUGH the ZAP API: runtime/scan status, the alert's rule identity and disposition, the official JSON report, and ZAP 2.17.0 Insights (EO3b)."
    fm star "Scope" "local Globomantics training app only (compose network)" focus

    echo; echo
    if ensure_ready; then
        pass "ZAP is up, a finished authenticated scan exists, and the API is reachable"
    else
        summary; return 1
    fi

    runstep 1 "ZAP API status response (EO3b)" step1_api_status
    runstep 2 "ZAP API alert response (EO3b)"  step2_api_alert
    runstep 3 "ZAP JSON report (EO3b)"         step3_json_report
    runstep 4 "ZAP Insights evidence (EO3b)"   step4_insights

    summary
    [ "${FAIL}" -eq 0 ]
}

summary() {
    echo; echo
    fm header "Preflight summary" "Green means every step inspects the scan evidence through the API as the runbook describes."
    if [ "${FAIL}" -eq 0 ]; then
        fm star "Result" "${PASS} checks passed, 0 failed" focus
        fm note "Aligned with EO3b (TO3). Ready to record."
    else
        fm star "Result" "${PASS} passed, ${FAIL} FAILED" focus
        echo
        fm section "Prompt to fix this demo"
        fm item "\"Read the latest log in module2/m2-c4-query-the-zap-api-and-inspect-scan-evidence/logs/, find every FAIL, fix the step's ZAP API query in scripts/_steps.sh (never weaken the check), then re-run scripts/preflight_check.sh until all four steps pass.\""
    fi
}

{ main; } 2>&1 | tee "${RAW_LOG}"
rc=${PIPESTATUS[0]}
sed 's/\x1b\[[0-9;]*m//g' "${RAW_LOG}" > "${LOG}"
echo
echo "plain-text log for review: ${LOG}"
exit "${rc}"
