#!/usr/bin/env bash
# Load supported lab configuration, then supervise readiness and startup.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/lib.sh"
cd "$REPO_ROOT"
exec python3 "$HERE/preflight_start.py" "$HERE"
