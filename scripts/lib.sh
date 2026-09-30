#!/bin/bash
# Shared helpers for the demo scripts. Sourced, not executed.

# Resolve repo root regardless of where the script is called from.
LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${LIB_DIR}/.." && pwd)"

# Load .env so compose variables and the ZAP API key are available to scripts.
if [ -f "${REPO_ROOT}/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    . "${REPO_ROOT}/.env"
    set +a
fi

COMPOSE="docker compose"

# Is the Docker engine reachable right now?
docker_up() { docker info >/dev/null 2>&1; }

# Make sure the Docker engine is running before we touch compose.
# On macOS the engine is Colima, which stops when the Mac sleeps or reboots —
# so if it is down and Colima is installed, start it automatically and wait
# until Docker answers. This keeps `demo_up.sh` working after a restart without
# the student having to know about Colima at all.
ensure_docker() {
    if docker_up; then return 0; fi
    if command -v colima >/dev/null 2>&1; then
        warn "Docker engine is not running — starting Colima (this can take ~30s)..."
        colima start || die "Could not start Colima. Run 'colima start' yourself, then retry."
        local i
        for i in $(seq 1 45); do
            if docker_up; then log "Docker engine is up."; return 0; fi
            sleep 2
        done
        die "Colima started but Docker did not become reachable. Try 'colima restart'."
    fi
    die "Docker engine is not running and Colima is not installed. Run ./env-setup/setup-macos.sh first."
}

# ANSI colours (fall back to empty if not a tty).
if [ -t 1 ]; then
    C_GREEN=$'\033[32m'; C_RED=$'\033[31m'; C_YEL=$'\033[33m'; C_RST=$'\033[0m'
else
    C_GREEN=""; C_RED=""; C_YEL=""; C_RST=""
fi

log()  { echo "[$(date +%H:%M:%S)] $*"; }
warn() { echo "${C_YEL}[warn]${C_RST} $*" >&2; }
die()  { echo "${C_RED}[fatal]${C_RST} $*" >&2; exit 1; }

# HTTP GET that asserts the status code. Never a bare `curl -s`.
#   http_get <url> [expected_code]
# Prints the response body to stdout; returns non-zero on mismatch.
http_get() {
    local url="$1" expected="${2:-200}" body code
    body="$(curl -s -o /tmp/.hg_body -w '%{http_code}' "${url}")"
    code="${body}"
    cat /tmp/.hg_body
    if [ "${code}" != "${expected}" ]; then
        echo "  (expected HTTP ${expected}, got ${code} for ${url})" >&2
        return 1
    fi
    return 0
}

# Return just the status code for a request (through an optional proxy).
#   status_code <url> [proxy]
status_code() {
    local url="$1" proxy="${2:-}"
    if [ -n "${proxy}" ]; then
        curl -s -o /dev/null -w '%{http_code}' -x "${proxy}" "${url}"
    else
        curl -s -o /dev/null -w '%{http_code}' "${url}"
    fi
}
