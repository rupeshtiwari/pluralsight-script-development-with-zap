#!/bin/bash
# =============================================================================
# Preflight / demo-step validator — m2-demo1
# "Run authenticated ZAP scripts in GitHub Actions"
# =============================================================================
# AUTHOR tooling. The clip's on-screen proof is the GitHub Actions job log; this
# runs the SAME Automation Framework plan locally through ZAP's automation API
# and proves each of the four beats, then writes a readable log to logs/ so you
# can check the demo against the objective before you push to CI. Exits non-zero
# if any step fails.
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
    fm header "Preflight — Run authenticated ZAP scripts in GitHub Actions" \
              "Proves the Automation Framework plan runs ZAP headless, authenticated, with the Module 1 scripts, and surfaces the custom finding."
    fm star "Scope" "local Globomantics training app only (compose network)" focus

    echo; echo
    if ensure_ready; then
        pass "ZAP is up and the Automation Framework is available"
    else
        summary; return 1
    fi

    banner 1 "Headless Automation Framework run (EO3a)";      step1_headless_run
    banner 2 "Authenticated context configuration (EO3a)";    step2_context_config
    banner 3 "Authenticated script job result (EO3a)";        step3_script_job
    banner 4 "Authenticated custom alert record (EO3a)";      step4_custom_alert

    summary
    [ "${FAIL}" -eq 0 ]
}

summary() {
    echo; echo
    fm header "Preflight summary" "Green means the pipeline run behaves as the runbook describes."
    if [ "${FAIL}" -eq 0 ]; then
        fm star "Result" "${PASS} checks passed, 0 failed" focus
        fm note "Aligned with EO3a (TO3). Ready to record."
    else
        fm star "Result" "${PASS} passed, ${FAIL} FAILED" focus
        echo
        fm section "Prompt to fix this demo"
        fm item "\"Read the latest log in module2/m2-demo1-run-authenticated-zap-scripts-in-github-actions/logs/, find every FAIL, fix the Automation Framework plan (ci/af-plan.yaml) or the workflow (never weaken the check), then re-run scripts/preflight_check.sh until all four steps pass.\""
    fi
}

{ main; } 2>&1 | tee "${RAW_LOG}"
rc=${PIPESTATUS[0]}
sed 's/\x1b\[[0-9;]*m//g' "${RAW_LOG}" > "${LOG}"
echo
echo "plain-text log for review: ${LOG}"
exit "${rc}"
