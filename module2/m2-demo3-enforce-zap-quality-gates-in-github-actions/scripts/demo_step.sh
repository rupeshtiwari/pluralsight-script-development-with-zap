#!/bin/bash
# =============================================================================
# Per-step runner for m2-demo3 "Enforce ZAP quality gates in GitHub Actions".
# Run each step on its own screen:
#
#   ./scripts/demo_step.sh 1   # False Positive alert filter
#   ./scripts/demo_step.sh 2   # Automation Framework job order
#   ./scripts/demo_step.sh 3   # Gate JSON report and exit code
#   ./scripts/demo_step.sh 4   # Filtered alert report
#
# Steps 1-2 read the plan. Step 3 runs the gate headless and captures the exit
# code. Step 4 reads that run's report (and primes itself if run on its own).
# =============================================================================
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${HERE}/_steps.sh"
export FORCE_COLOR=1

usage() { echo "usage: ./scripts/demo_step.sh <1|2|3|4>"; exit 2; }
N="${1:-}"; case "${N}" in 1|2|3|4) ;; *) usage ;; esac

# Steps 1 and 2 only read the plan file; steps 3 and 4 need the stack + a gate run.
case "${N}" in
    1|2) [ -f "${GATE_PLAN_HOST}" ] || { fail "gate plan not found"; exit 1; } ;;
    3|4) ensure_ready || exit 1 ;;
esac
echo

case "${N}" in
    1) step1_fp_filter ;;
    2) step2_job_order ;;
    3) step3_gate_exit ;;
    4) step4_filtered_report ;;
esac
exit "${STEP_RC:-0}"
