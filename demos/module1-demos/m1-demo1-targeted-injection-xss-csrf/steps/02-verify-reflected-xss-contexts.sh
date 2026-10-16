#!/usr/bin/env bash
# verify reflected xss contexts.
# This public command calls the same real ZAP step engine in preflight and recording.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "${DEMO_SYNC_MODE:-0}" = "1" ]; then
    ROOT="$(cd "${HERE}/../../../.." && pwd)"
    exec python3 "${ROOT}/runtime/scripts/recording_step.py" "${HERE}/.." 2 "${HERE}/../scripts/_run_step.sh" 2
fi
exec "${HERE}/../scripts/_run_step.sh" 2
