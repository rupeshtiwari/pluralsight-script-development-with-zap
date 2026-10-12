#!/bin/bash
# Tear the Globomantics stack down for this demo.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
exec "${REPO_ROOT}/scripts/demo_down.sh" "$@"
