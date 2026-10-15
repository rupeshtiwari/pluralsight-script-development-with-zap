#!/bin/bash
# Bring the demo stack up and wait for all four services to be healthy.
#   APP_BUILD=vulnerable|remediated ./scripts/demo_up.sh
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
cd "${REPO_ROOT}"

ensure_docker

BUILD="${APP_BUILD:-vulnerable}"
log "Starting demo stack (APP_BUILD=${BUILD})..."
APP_BUILD="${BUILD}" ${COMPOSE} up -d --build

SERVICES="postgres mongo app zap"
log "Waiting for services to become healthy: ${SERVICES}"

# ZAP's first boot (Webswing + add-on install) can take several minutes on a
# cold engine, so wait generously and show a heartbeat so a long boot never
# looks like a hang. Override with HEALTH_TIMEOUT=<seconds> if you need more.
WAIT_SECS="${HEALTH_TIMEOUT:-600}"
start=$(date +%s)
deadline=$(( start + WAIT_SECS ))
last_beat=0
while :; do
    pending=""
    for svc in ${SERVICES}; do
        cid="$(${COMPOSE} ps -q "${svc}")"
        if [ -z "${cid}" ]; then pending="${pending} ${svc}(no-container)"; continue; fi
        health="$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "${cid}")"
        [ "${health}" = "healthy" ] || pending="${pending} ${svc}(${health})"
    done
    [ -z "${pending}" ] && break
    now=$(date +%s)
    if [ "${now}" -ge "${deadline}" ]; then
        warn "Timed out after ${WAIT_SECS}s. Current status:"
        ${COMPOSE} ps
        die "Stack did not become healthy in time. ZAP's first boot can be slow on a cold engine — re-run ./scripts/demo_up.sh, or give it longer with: HEALTH_TIMEOUT=900 ./scripts/demo_up.sh"
    fi
    if [ $(( now - last_beat )) -ge 30 ]; then
        log "still starting ($(( now - start ))s elapsed) — waiting on:${pending}"
        last_beat="${now}"
    fi
    sleep 3
done

echo
log "All services healthy."
echo "  App (Globomantics):   http://localhost:8000/"
echo "  App health:           http://localhost:8000/health"
echo "  ZAP GUI (Webswing):   http://localhost:8080/zap/"
echo "  ZAP API / proxy:      http://localhost:8090  (proxy on the same port)"
echo "  Postgres:             localhost:5432"
echo "  Mongo:                localhost:27017"
echo
echo "Up"
