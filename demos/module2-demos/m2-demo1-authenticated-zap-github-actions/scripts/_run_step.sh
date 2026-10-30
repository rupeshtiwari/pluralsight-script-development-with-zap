#!/bin/bash
# =============================================================================
# Per-step runner for RECORDING m2-c3 one clip segment at a time.
# "Run authenticated ZAP scripts in GitHub Actions"
# =============================================================================
# Record each step as its own terminal segment:
#
#   ./scripts/demo_step.sh 1   # ZAP runs headless from the Automation plan
#   ./scripts/demo_step.sh 2   # The authenticated context, declared as config
#   ./scripts/demo_step.sh 3   # The Module 1 scripts run authenticated
#   ./scripts/demo_step.sh 4   # The authenticated finding the pipeline records
#
# Run them in order (1 -> 4). Step 1 runs the plan; steps 2-4 read its result.
# If you record a later step on its own, it primes itself by running the plan
# once first, so every step is self-sufficient.
# =============================================================================
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${HERE}/_steps.sh"
export FORCE_COLOR=1

usage() { echo "usage: ./scripts/demo_step.sh <1|2|3|4>"; exit 2; }
N="${1:-}"; case "${N}" in 1|2|3|4) ;; *) usage ;; esac

run_plan_and_wait() {
    run_plan || return 1
    local i; for i in $(seq 1 120); do plan_finished && break; sleep 3; done
    if ! plan_finished || [ "$(plan_field error)" != "0" ]; then
        fail "the priming plan did not finish successfully" "automation/view/planProgress is unfinished or reports errors" "check the plan and ZAP log before retrying this step"
        return 1
    fi
    return 0
}

# Steps 2-4 read the authenticated scan's result. When Step 1 (or an earlier
# step) already ran the plan in THIS long-lived local ZAP session, reuse that
# result instead of re-running the scan; only run the plan when there is
# genuinely nothing to reuse (you're recording a later step on its own).
#
# The reuse probe must look for the evidence THIS plan actually produces. The
# plan's activeScan-policy runs the custom rule ONLY (plugin 50000, every
# built-in rule threshold "off" in ci/af-plan.yaml), so it never raises a
# built-in "Cross Site Scripting (Reflected)" alert. Probing for that built-in
# finding never matched, so every sequential step re-primed and re-ran the whole
# plan. Probe for the named custom alert the plan does raise on the login-only
# page: sequential runs then reuse Step 1's evidence, while an independent
# single-step run (fresh session, no alert yet) still primes once.
prime_if_needed() {
    [ -n "$(custom_alert)" ] && return 0
    fm note "Priming: no scan result in this ZAP session yet, running the plan once so this step has data."
    run_plan_and_wait
}

ensure_ready || exit 1
echo

case "${N}" in
    1) step1_headless_run ;;
    2) prime_if_needed || exit 1; step2_context_config ;;
    3) prime_if_needed || exit 1; step3_script_job ;;
    4) prime_if_needed || exit 1; step4_custom_alert ;;
esac
exit "${STEP_RC:-0}"
