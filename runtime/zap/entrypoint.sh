#!/bin/bash
# Start ZAP with the Webswing GUI, boot the ZAP core so its API/proxy is
# available, then install and verify the ascanrulesBeta add-on (rule 40033).
#
# The Webswing GUI only launches the ZAP core when a browser attaches. We kick
# that with an in-container headless Firefox; the ZAP core then keeps running
# (sessionMode CONTINUE_FOR_USER) after the kick browser exits, and the author
# can attach their own browser to the GUI at any time.
set -euo pipefail

API_KEY="${ZAP_API_KEY:?ZAP_API_KEY must be set}"
GUI_PORT=8080
API_PORT=8090

# ZAP core options applied when the GUI launches the core:
#  - fixed API key and open API addresses (author tooling reaches it via 8090)
#  - suppress the first-run "persist session?" dialog that otherwise blocks boot
#  - skip update/add-on-update checks at startup for a deterministic boot
#  - view.fontSize=24 enlarges the whole Swing UI so the GUI reads clearly on a
#    recording (menus, tabs, tables, Quick Start). This is ZAP's REAL UI font,
#    so it stays crisp in the Webswing canvas, unlike browser zoom which blurs.
#    Override at run time with ZAP_UI_FONT_SIZE=NN ./lab up if you want a
#    different size. The same control lives in the GUI at Tools > Options >
#    Display > Font size; this just makes 24 the default for every boot.
UI_FONT_SIZE="${ZAP_UI_FONT_SIZE:-24}"
export ZAP_WEBSWING_OPTS="-host 0.0.0.0 -port ${API_PORT} \
-config api.key=${API_KEY} \
-config api.addrs.addr.name=.* -config api.addrs.addr.regex=true \
-config database.newsessionprompt=false \
-config start.checkForUpdates=false \
-config start.checkAddonUpdates=false \
-config view.fontSize=${UI_FONT_SIZE} \
-config view.scaleImages=true \
-config connection.dnsTtlSuccessfulQueries=-1"

# Persist the ZAP core after the kick browser disconnects.
sed -i 's/CONTINUE_FOR_BROWSER/CONTINUE_FOR_USER/' /zap/webswing/webswing.config

echo "[zap-entrypoint] starting Webswing GUI..."
zap-webswing.sh &
WEBSWING_PID=$!

echo "[zap-entrypoint] waiting for Webswing GUI on :${GUI_PORT}..."
for _ in $(seq 1 60); do
    if [ "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:${GUI_PORT}/zap/")" = "200" ]; then
        break
    fi
    sleep 2
done

kick_browser() {
    firefox-esr --headless --no-remote --profile "$(mktemp -d)" \
        "http://localhost:${GUI_PORT}/zap/" >/tmp/zap-kick.log 2>&1 &
    KICK_PID=$!
}

echo "[zap-entrypoint] kicking the ZAP core via headless browser..."
kick_browser

echo "[zap-entrypoint] waiting for the ZAP API on :${API_PORT}..."
API_UP=""
for i in $(seq 1 150); do
    # `|| echo 000` keeps a pre-boot connection failure (curl exit 7) from
    # tripping `set -e` via the command substitution.
    code="$(curl -s -o /dev/null -w '%{http_code}' \
        "http://localhost:${API_PORT}/JSON/core/view/version/?apikey=${API_KEY}" || echo 000)"
    if [ "${code}" = "200" ]; then
        API_UP=1
        break
    fi
    # If the kick browser died before the core booted, kick again.
    if ! kill -0 "${KICK_PID}" 2>/dev/null; then
        echo "[zap-entrypoint] kick browser exited; re-kicking..."
        kick_browser
    fi
    sleep 2
done
if [ -z "${API_UP}" ]; then
    echo "[zap-entrypoint] ERROR: ZAP API did not come up" >&2
    exit 1
fi
echo "[zap-entrypoint] ZAP core is up: $(curl -s "http://localhost:${API_PORT}/JSON/core/view/version/?apikey=${API_KEY}")"

# The kick browser has served its purpose; the core persists without it.
kill "${KICK_PID}" >/dev/null 2>&1 || true

api() {
    # Bounded time so a stalled ZAP or marketplace call can never hang the whole boot:
    # --connect-timeout caps the connect, --max-time caps the entire call. A single
    # installAddon call with no cap used to block here until the outer health timeout
    # killed the container (seen on CI: 16 minutes stuck at "installing ascanrulesBeta").
    # `|| true` so a transient curl failure never trips `set -e`.
    curl -s --connect-timeout 10 --max-time 120 \
        "http://localhost:${API_PORT}/JSON/$1/?apikey=${API_KEY}&${2:-}" || true
}

# Install a marketplace add-on, then wait until <check-fn> passes. The marketplace
# download is network-dependent and occasionally STALLS; firing the install once and
# waiting on it forever is what hung boot. Instead re-kick the install each attempt,
# with every attempt bounded, so a transient stall costs ~a minute and a retry, not
# the whole health budget. Args: <addon-id> <human-name> <check-fn>
install_addon() {
    local id="$1" name="$2" check="$3" attempt i
    if api autoupdate/view/installedAddons | grep -q "\"${id}\""; then
        echo "[zap-entrypoint] ${name} already installed."
        return 0
    fi
    for attempt in 1 2 3; do
        echo "[zap-entrypoint] installing ${name} from the marketplace (attempt ${attempt})..."
        api autoupdate/action/installAddon "id=${id}" >/dev/null
        for i in $(seq 1 30); do          # ~60s per attempt
            if "${check}"; then
                echo "[zap-entrypoint] ${name} installed."
                return 0
            fi
            sleep 2
        done
        echo "[zap-entrypoint] ${name} not registered after attempt ${attempt}; re-kicking the install..." >&2
    done
    echo "[zap-entrypoint] ERROR: ${name} did not install after 3 attempts (marketplace unreachable?)" >&2
    return 1
}

beta_present()       { api autoupdate/view/installedAddons | grep -q '"ascanrulesBeta"'; }
jython_present()     { api script/view/listEngines         | grep -iq 'jython'; }
automation_present() { api autoupdate/view/installedAddons | grep -q '"automation"'; }

# ascanrulesBeta provides the NoSQL MongoDB rule 40033.
install_addon ascanrulesBeta "ascanrulesBeta" beta_present || exit 1

# Verify NoSQL rule 40033 is now available as an active-scan rule.
RULE_OK=""
for _ in $(seq 1 30); do
    if api ascan/view/scanners | grep -q '"id":"40033"'; then
        RULE_OK=1
        break
    fi
    sleep 2
done
if [ -z "${RULE_OK}" ]; then
    echo "[zap-entrypoint] ERROR: NoSQL rule 40033 not available after install" >&2
    exit 1
fi

# Parse the installed version defensively (never let a no-match exit the script).
BETA_VER="$(api autoupdate/view/installedAddons \
    | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin)
    print(next(a.get("version","") for a in d["installedAddons"] if a.get("id")=="ascanrulesBeta"))
except Exception:
    print("")' 2>/dev/null || true)"
BETA_MAJOR="${BETA_VER%%.*}"
if [ -n "${BETA_MAJOR}" ] && [ "${BETA_MAJOR}" -lt 66 ] 2>/dev/null; then
    echo "[zap-entrypoint] WARNING: ascanrulesBeta version ${BETA_VER} is below v66" >&2
fi
echo "[zap-entrypoint] ascanrulesBeta v${BETA_VER:-unknown} installed; NoSQL rule 40033 available."

# Python Scripting (jython) so ZAP can run Jython 2.7.2 scripts (custom active-scan
# rules and authentication scripts). Registration is proven by the engine appearing.
install_addon jython "Python Scripting (jython)" jython_present || exit 1
echo "[zap-entrypoint] Python Scripting (jython) installed; Jython engine available."

# Automation Framework so the author preflight can run the Module 2 AF plan via the
# ZAP API (it ships by default, but install to be safe).
install_addon automation "Automation Framework" automation_present || exit 1
echo "[zap-entrypoint] Automation Framework available."

touch /tmp/zap-ready
echo "[zap-entrypoint] READY. GUI: http://localhost:${GUI_PORT}/zap/  API/proxy: :${API_PORT}"

# Hand back to Webswing in the foreground so the container stays up.
wait "${WEBSWING_PID}"
