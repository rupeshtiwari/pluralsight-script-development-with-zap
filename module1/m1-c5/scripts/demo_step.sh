#!/bin/bash
# =============================================================================
# Per-step runner for m1-c5 "Write Python scan and authentication scripts in
# ZAP". Run each step on its own screen. You AUTHOR the scripts in ZAP's Script
# Console (see the runbook); these commands reproduce the same beats through the
# ZAP API so each one shows a clean, checkable result in the terminal.
#
#   ./scripts/demo_step.sh 1   # Python active-rule source      (loads it as an active rule)
#   ./scripts/demo_step.sh 2   # Authentication script source   (registers it)
#   ./scripts/demo_step.sh 3   # ZAP runs the auth script        (context script-auth + forced user)
#   ./scripts/demo_step.sh 4   # Fresh custom alert on the scan  (scan as the user)
#
# Both Jython scripts run INSIDE ZAP. Each step is self-contained: the scripts
# are loaded first, and step 4 sets up the authenticated context it needs, so
# the steps work in any order.
# =============================================================================
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${HERE}/_steps.sh"
export FORCE_COLOR=1

usage() { echo "usage: ./scripts/demo_step.sh <1|2|3|4>"; exit 2; }
N="${1:-}"; case "${N}" in 1|2|3|4) ;; *) usage ;; esac

ensure_ready || exit 1

# Steps 2-4 need both scripts registered; load them quietly so any step stands
# alone (step 1 and step 2 show that loading happen on screen).
if [ "${N}" != "1" ]; then
    load_script "${RULE_NAME}" active "${JYTHON_ENGINE}" "${RULE_FILE_ZAP}" >/dev/null 2>&1 || true
    zap script/action/enable "scriptName=$(enc "${RULE_NAME}")" >/dev/null 2>&1 || true
    load_script "${AUTH_NAME}" authentication "${JYTHON_ENGINE}" "${AUTH_FILE_ZAP}" >/dev/null 2>&1 || true
fi
# Step 4 scans as the authenticated user, so make sure the script-auth context
# and forced user exist (step 3 is what demonstrates this on screen).
if [ "${N}" = "4" ]; then
    setup_script_auth >/dev/null 2>&1 || true
    forced_user_mode true
fi
echo

case "${N}" in
    1) step1_active_rule_source ;;
    2) step2_auth_script_source ;;
    3) step3_auth_executes ;;
    4) step4_fresh_alert ;;
esac
exit "${STEP_RC:-0}"
