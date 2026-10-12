#!/bin/bash
# =============================================================================
# Per-step runner for m1-c4 "Write a JavaScript security script in ZAP".
# Run each step on its own screen (show the source in VS Code, the proof here):
#
#   ./scripts/demo_step.sh 1   # JavaScript source file  (loads it into ZAP)
#   ./scripts/demo_step.sh 2   # Modified HTTP request    (marker header added)
#   ./scripts/demo_step.sh 3   # Script console output    (named console line)
#   ./scripts/demo_step.sh 4   # Saved script registration
#
# The HTTP Sender script runs INSIDE ZAP; these commands drive ZAP through its
# API so each beat shows in the terminal. Each step is self-contained — the
# script is loaded first so steps 2-4 work in any order.
# =============================================================================
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${HERE}/_steps.sh"
export FORCE_COLOR=1

usage() { echo "usage: ./scripts/demo_step.sh <1|2|3|4>"; exit 2; }
N="${1:-}"; case "${N}" in 1|2|3|4) ;; *) usage ;; esac

ensure_ready || exit 1
# Steps 2-4 need the script already loaded and enabled; step 1 shows that happen.
[ "${N}" = "1" ] || load_and_enable "${JS_ENGINE}" >/dev/null 2>&1 || true
echo

case "${N}" in
    1) step1_source ;;
    2) step2_modified_request ;;
    3) step3_console_output ;;
    4) step4_registration ;;
esac
exit "${STEP_RC:-0}"
