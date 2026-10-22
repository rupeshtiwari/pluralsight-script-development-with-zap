#!/bin/bash
# Bring the demo stack up and wait for all four services to be healthy.
#   APP_BUILD=vulnerable|remediated ./scripts/lab-up.sh
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
cd "${REPO_ROOT}"

ensure_docker

BUILD="${APP_BUILD:-vulnerable}"
log "Starting demo stack (APP_BUILD=${BUILD})..."
# --force-recreate so a stale, UNHEALTHY container from an earlier run (e.g. a ZAP that never finished
# booting and sat "Up (unhealthy)") is replaced with a fresh one instead of silently reused. Data lives
# in named volumes, so Postgres/Mongo keep their seed; ZAP has no volume, so it gets a clean boot.
APP_BUILD="${BUILD}" ${COMPOSE} up -d --build --force-recreate --remove-orphans

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
        echo
        warn "Logs from the service(s) that never became healthy, this shows WHERE startup stuck:"
        for tok in ${pending}; do
            svc="${tok%%(*}"
            echo "----- ${svc}, last 100 lines ---------------------------------------------"
            ${COMPOSE} logs --tail=100 "${svc}" 2>&1 || true
            echo "-------------------------------------------------------------------------"
        done
        echo
        warn "The stack is LEFT RUNNING so you can inspect it. Useful next steps:"
        echo "    ${COMPOSE} logs -f zap        # follow ZAP's boot (add-on download / core boot)"
        echo "    HEALTH_TIMEOUT=1200 ./scripts/lab-up.sh   # give a cold first boot more time"
        echo "    ./scripts/lab-down.sh        # tear everything down when done"
        die "Stack did not become healthy in time. The ZAP log above shows the cause (usually a slow or blocked marketplace add-on download, or the ZAP core not staying up after first boot)."
    fi
    if [ $(( now - last_beat )) -ge 30 ]; then
        log "still starting ($(( now - start ))s elapsed), waiting on:${pending}"
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
