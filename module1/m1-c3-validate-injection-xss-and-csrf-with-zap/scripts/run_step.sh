#!/bin/bash
# Run ONE demo step and stop — convenient for recording one screen at a time.
#
#   ./scripts/run_step.sh ref     # the context / token-state reference panel
#   ./scripts/run_step.sh 1       # targeted injection scan
#   ./scripts/run_step.sh 2       # reflected XSS in three contexts
#   ./scripts/run_step.sh 3       # CSRF token replay
#   ./scripts/run_step.sh 4       # alert disposition record
#
# Each step prints a header (what / why) and only the fields you read on camera,
# highlighted and never truncated, then a PASS/FAIL line. Every step is
# self-contained, so you can run them in any order.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${HERE}/_steps.sh"

STEP="${1:-}"
[ -n "${STEP}" ] || { echo "usage: run_step.sh {ref|1|2|3|4}"; exit 2; }

# The reference panel needs no ZAP; the numbered steps do.
if [ "${STEP}" != "ref" ]; then
    ensure_ready || exit 1
fi

run_step_by_number "${STEP}"
exit "${STEP_RC}"
