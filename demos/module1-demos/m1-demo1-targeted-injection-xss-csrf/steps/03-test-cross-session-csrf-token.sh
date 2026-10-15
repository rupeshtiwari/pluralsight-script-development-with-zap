#!/usr/bin/env bash
# test cross session csrf token — demonstration step 3 of 4
# Run from the demo directory. The named command delegates to the frozen step engine.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${HERE}/../scripts/_run_step.sh" 3
