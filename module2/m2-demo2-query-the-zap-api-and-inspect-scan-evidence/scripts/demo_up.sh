#!/bin/bash
# Start the Globomantics stack for this demo (vulnerable build by default).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
exec "${REPO_ROOT}/scripts/demo_up.sh" "$@"
