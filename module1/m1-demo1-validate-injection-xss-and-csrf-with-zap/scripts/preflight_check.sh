#!/bin/bash
# =============================================================================
# Preflight / demo-step validator — m1-demo1 "Validate injection, XSS, and CSRF"
# =============================================================================
# AUTHOR tooling. Runs the FOUR demo steps in the SAME ORDER as the runbook,
# proving each finding against the local Globomantics app, and writes a
# readable plain-text log to logs/ so you can check the demo against the
# learning objectives before you use it.
#
# For each step it prints a header (what / why), only the fields that are read
# on screen (highlighted, never truncated), and PASS or FAIL with the reason
# and a suggested fix prompt. Exits non-zero if any step fails.
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
    fm header "Preflight — Validate injection, XSS, and CSRF with ZAP" \
              "Runs all four demo steps against the local Globomantics app and proves each finding before you rely on it."
    fm star "Scope" "local Globomantics training app only (compose network)" focus

    echo; echo
    if ensure_ready; then
        pass "ZAP is up and NoSQL rule 40033 is installed"
    else
        summary; return 1
    fi

    echo; echo; fm section "Reference — contexts and token states (EO1b, EO1c)"
    print_reference

    banner 1 "Targeted injection scan (EO1a)";        step1_injection
    banner 2 "Reflected XSS in three contexts (EO1b)"; step2_xss
    banner 3 "CSRF token replay (EO1c)";               step3_csrf
    banner 4 "Alert disposition record (EO1a/b/c)";    step4_disposition

    summary
    [ "${FAIL}" -eq 0 ]
}

summary() {
    echo; echo
    fm header "Preflight summary" "Green means every demo step behaves as the runbook describes."
    if [ "${FAIL}" -eq 0 ]; then
        fm star "Result" "${PASS} checks passed, 0 failed" focus
        fm note "Aligned with EO1a, EO1b, EO1c (TO1). Ready to record."
    else
        fm star "Result" "${PASS} passed, ${FAIL} FAILED" focus
        echo
        fm section "Prompt to fix this demo"
        fm item "\"Read the latest log in module1/m1-demo1-validate-injection-xss-and-csrf-with-zap/logs/, find every FAIL, fix the app or the scan policy (never weaken the check), then re-run scripts/preflight_check.sh until all four steps pass on the vulnerable build.\""
    fi
}

{ main; } 2>&1 | tee "${RAW_LOG}"
rc=${PIPESTATUS[0]}
sed 's/\x1b\[[0-9;]*m//g' "${RAW_LOG}" > "${LOG}"
echo
echo "plain-text log for review: ${LOG}"
exit "${rc}"
