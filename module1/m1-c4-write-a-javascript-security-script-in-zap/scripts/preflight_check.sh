#!/bin/bash
# =============================================================================
# Preflight / demo-step validator — m1-c4 "Write a JavaScript security script"
# =============================================================================
# AUTHOR tooling. The demo is authored in ZAP's Script Console (GUI); this runs
# the same four beats through the ZAP API and proves each one, then writes a
# readable log to logs/ so you can check the demo against the objective before
# you use it. Exits non-zero if any step fails.
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

banner() { echo; echo; fm section "STEP $1 — $2"; }

main() {
    fm header "Preflight — Write a JavaScript security script in ZAP" \
              "Proves the JavaScript HTTP Sender script loads, marks requests, prints its named line, and is saved for reuse."
    fm star "Scope" "local Globomantics training app only (compose network)" focus

    echo; echo
    if ensure_ready; then
        pass "ZAP is up and a JavaScript engine is available"
    else
        summary; return 1
    fi

    banner 1 "JavaScript source file (EO2a)";     step1_source
    banner 2 "Modified HTTP request (EO2a)";       step2_modified_request
    banner 3 "Script console output (EO2a)";       step3_console_output
    banner 4 "Saved script registration (EO2a)";   step4_registration

    summary
    [ "${FAIL}" -eq 0 ]
}

summary() {
    echo; echo
    fm header "Preflight summary" "Green means the script behaves as the runbook describes."
    if [ "${FAIL}" -eq 0 ]; then
        fm star "Result" "${PASS} checks passed, 0 failed" focus
        fm note "Aligned with EO2a (TO2). Ready to record."
    else
        fm star "Result" "${PASS} passed, ${FAIL} FAILED" focus
        echo
        fm section "Prompt to fix this demo"
        fm item "\"Read the latest log in module1/m1-c4-write-a-javascript-security-script-in-zap/logs/, find every FAIL, fix the JavaScript script or how it is loaded (never weaken the check), then re-run scripts/preflight_check.sh until all four steps pass.\""
    fi
}

{ main; } 2>&1 | tee "${RAW_LOG}"
rc=${PIPESTATUS[0]}
sed 's/\x1b\[[0-9;]*m//g' "${RAW_LOG}" > "${LOG}"
echo
echo "plain-text log for review: ${LOG}"
exit "${rc}"
