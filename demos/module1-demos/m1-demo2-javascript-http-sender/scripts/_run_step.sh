#!/bin/bash
# =============================================================================
# Per-step runner for m1-c4 "Write a JavaScript security script in ZAP".
# Run each step on its own screen (show the source in ZAP and the evidence in Terminal / ZAP):
#
#   ./scripts/steps/01-...sh   # JavaScript source file  (loads it into ZAP)
#   ./scripts/steps/02-...sh   # Modified HTTP request    (marker header added)
#   ./scripts/demo_step.sh 3   # Script console output    (named console line)
#   ./scripts/demo_step.sh 4   # Saved script registration
#
# The HTTP Sender script runs INSIDE ZAP; these commands drive ZAP through its
# API. Steps 2-4 require step 1; do not silently reload between GUI views.
# =============================================================================
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${HERE}/_steps.sh"
export FORCE_COLOR=1

usage() { echo "usage: ./scripts/demo_step.sh <1|2|3|4>"; exit 2; }
N="${1:-}"; case "${N}" in 1|2|3|4) ;; *) usage ;; esac

ensure_ready || exit 1
# Steps 2-4 must preserve the registration demonstrated in step 1.
if [ "${N}" != "1" ] && ! script_registration_valid; then
    fail "script not enabled or registered" "run step 1 first" "execute ./scripts/steps/01-...sh"
    exit 1
fi
echo

case "${N}" in
    1) step1_source ;;
    2) step2_modified_request ;;
    3) step3_console_output ;;
    4) step4_registration ;;
esac
exit "${STEP_RC:-0}"
