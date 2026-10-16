#!/usr/bin/env bash
# confirm custom scan alert.
# This public command calls the same real ZAP step engine in preflight and recording.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "${DEMO_SYNC_MODE:-0}" = "1" ]; then
    ROOT="$(cd "${HERE}/../../../.." && pwd)"
    exec python3 "${ROOT}/runtime/scripts/recording_step.py" "${HERE}/.." 4 "${HERE}/../scripts/_run_step.sh" 4
fi
exec "${HERE}/../scripts/_run_step.sh" 4
