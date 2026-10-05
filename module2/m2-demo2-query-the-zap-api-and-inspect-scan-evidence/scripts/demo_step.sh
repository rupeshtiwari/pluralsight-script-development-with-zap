#!/bin/bash
# =============================================================================
# Per-step runner for m2-demo2 "Query the ZAP API and inspect scan evidence".
# Run each step on its own terminal screen:
#
#   ./scripts/demo_step.sh 1   # ZAP API status response
#   ./scripts/demo_step.sh 2   # ZAP API alert response
#   ./scripts/demo_step.sh 3   # ZAP JSON report
#   ./scripts/demo_step.sh 4   # ZAP Insights evidence
#
# Every step inspects a finished authenticated scan. If this ZAP session has no
# scan yet, the step primes itself by running the authenticated plan once, so
# each step is self-sufficient and can be shown in any order.
# =============================================================================
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${HERE}/_steps.sh"
export FORCE_COLOR=1

usage() { echo "usage: ./scripts/demo_step.sh <1|2|3|4>"; exit 2; }
N="${1:-}"; case "${N}" in 1|2|3|4) ;; *) usage ;; esac

ensure_ready || exit 1
echo

case "${N}" in
    1) step1_api_status ;;
    2) step2_api_alert ;;
    3) step3_json_report ;;
    4) step4_insights ;;
esac
exit "${STEP_RC:-0}"
