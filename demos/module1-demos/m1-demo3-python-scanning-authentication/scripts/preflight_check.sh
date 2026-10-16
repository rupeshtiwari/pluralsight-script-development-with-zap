#!/usr/bin/env bash
# Preflight runs the same four concept-named commands as the Recorder.
# Produces complete preflight plus a stable, per-step narration reference.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/../../../.." && pwd)"
exec "${ROOT}/runtime/scripts/preflight_all_steps.sh" "${HERE}/.."
