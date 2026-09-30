#!/bin/bash
# Shared step library for m1-demo3 "Write Python scan and authentication scripts
# in ZAP".
#
# Sourced by preflight_check.sh (author tooling). The demo itself is authored in
# ZAP's Script Console (GUI); this library proves, through the ZAP API, that the
# two Jython scripts behave as the runbook describes:
#   1. Python active-rule source        2. Authentication script source
#   3. Authenticated custom-scan result 4. Custom alert record
#
# Every request targets ONLY the local Globomantics app on the compose network.

HERE_STEPS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO_DIR="$(cd "${HERE_STEPS}/.." && pwd)"
REPO_ROOT="$(cd "${DEMO_DIR}/../.." && pwd)"
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/lib.sh"
FMT="${REPO_ROOT}/scripts/fmt.py"
fm() { python3 "${FMT}" "$@"; }

APP_INTERNAL="http://app:8000"
ZAP="http://localhost:8090"
PROXY="http://localhost:8090"
K="${ZAP_API_KEY:-}"

RULE_NAME="globomantics-active-rule"
RULE_FILE_HOST="${DEMO_DIR}/zap-scripts/globomantics-active-rule.py"
RULE_FILE_ZAP="/zap-scripts-py/globomantics-active-rule.py"

AUTH_NAME="globomantics-auth"
AUTH_FILE_HOST="${DEMO_DIR}/zap-scripts/globomantics-auth.py"
AUTH_FILE_ZAP="/zap-scripts-py/globomantics-auth.py"

ALERT_NAME="Globomantics unsafe reflection (custom rule)"
LOGIN_USER="alice"
PROFILE_URL="${APP_INTERNAL}/account/profile?note=seed"
SCRIPT_RULES_ID="50000"   # ZAP "Script Active Scan Rules" plugin

PASS=0; FAIL=0; STEP_RC=0
pass() { fm ok "$1"; PASS=$((PASS+1)); STEP_RC=0; }
fail() { fm fail "$1" "${2:-}" "${3:-}"; FAIL=$((FAIL+1)); STEP_RC=1; }
enc()  { python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=""))' "$1"; }

zap() { # <path> <query> -> body (asserts HTTP 200)
    local path="$1" query="${2:-}" code
    code="$(curl -s -o /tmp/.z3body -w '%{http_code}' "${ZAP}/JSON/${path}/?apikey=${K}&${query}")"
    [ "${code}" = "200" ] || { echo "  (ZAP API ${path} -> HTTP ${code})" >&2; return 1; }
    cat /tmp/.z3body
}

detect_jython_engine() {
    zap script/view/listEngines | python3 -c '
import json,sys
engs = json.load(sys.stdin).get("listEngines", [])
for e in engs:
    if "jython" in e.lower() or "python" in e.lower():
        print(e); raise SystemExit
print("")'
}

load_script() { # <name> <type> <engine> <fileName>
    zap script/action/remove "scriptName=$(enc "$1")" >/dev/null 2>&1 || true
    zap script/action/load \
        "scriptName=$(enc "$1")&scriptType=$(enc "$2")&scriptEngine=$(enc "$3")&fileName=$(enc "$4")&scriptDescription=$(enc 'Globomantics course demo')" \
        >/dev/null 2>&1 || return 1
    return 0
}

script_info() { # <name> -> name|type|engine|enabled (empty if absent)
    zap script/view/listScripts | python3 -c '
import json,sys
name = sys.argv[1]
try:
    data = json.load(sys.stdin)
except Exception:
    print(""); raise SystemExit
for s in data.get("listScripts", []):
    if s.get("name") == name:
        print("%s|%s|%s|%s" % (s.get("name"), s.get("type"), s.get("engine"), s.get("enabled")))
        raise SystemExit
print("")' "$1"
}

# --- authentication helpers (host-side proof of EO2c behavior) --------------
login_cookie() { # -> the session cookie value (empty on failure)
    curl -s -x "${PROXY}" -D - -o /dev/null -X POST "${APP_INTERNAL}/login" \
        --data "username=${LOGIN_USER}" \
        | grep -i '^set-cookie:' | sed -E 's/.*session=([^;]+).*/\1/I' | head -1 | tr -d '\r'
}

status_with_cookie() { # <url> <cookie> -> HTTP code (through the ZAP proxy)
    curl -s -x "${PROXY}" -o /tmp/.z3profile -w '%{http_code}' -b "session=$2" "$1"
}
status_no_cookie() {  # <url> -> HTTP code (through the ZAP proxy)
    curl -s -x "${PROXY}" -o /dev/null -w '%{http_code}' "$1"
}

# --- active scan helpers ----------------------------------------------------
# Use the full default policy so ZAP discovers the parameter and runs every
# enabled active rule (our script rule included). Re-enable all scanners in case
# an earlier run left the policy stripped down.
enable_all_scanners() {
    zap ascan/action/enableAllScanners >/dev/null 2>&1 || true
    zap ascan/action/enableScanners "ids=${SCRIPT_RULES_ID}" >/dev/null 2>&1 || true
}
scan_messages_count() { # <scanId> -> number of probe requests the scan sent
    zap ascan/view/messagesIds "scanId=$1" | python3 -c 'import json,sys
try: print(len(json.load(sys.stdin).get("messagesIds",[])))
except Exception: print("0")'
}
# Force every scanner request to carry the session cookie, so the active scan
# runs authenticated regardless of ZAP's session management (best-effort: needs
# the Replacer add-on, which ships with ZAP).
add_auth_cookie_header() { # <cookie>
    zap replacer/action/addRule \
        "description=globo-auth-cookie&enabled=true&matchType=REQ_HEADER&matchString=Cookie&matchRegex=false&replacement=$(enc "session=$1")&initiators=" \
        >/dev/null 2>&1 || true
}
remove_auth_cookie_header() {
    zap replacer/action/removeRule "description=$(enc 'globo-auth-cookie')" >/dev/null 2>&1 || true
}
start_scan() { # <url> -> scanId (empty on failure)
    zap ascan/action/scan "url=$(enc "$1")&recurse=false&inScopeOnly=false" \
        | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("scan",""))
except Exception: print("")'
}
scan_done() { # <scanId> -> 0 when status is 100
    local pct
    pct="$(zap ascan/view/status "scanId=$1" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("status",""))
except Exception: print("")')"
    [ "${pct}" = "100" ]
}
custom_alert() { # -> name|risk|param|evidence  (empty if not raised)
    zap core/view/alerts "baseurl=$(enc "${APP_INTERNAL}/account/profile")" | python3 -c '
import json,sys
name = sys.argv[1]
try:
    data = json.load(sys.stdin)
except Exception:
    print(""); raise SystemExit
for a in data.get("alerts", []):
    if a.get("alert") == name or a.get("name") == name:
        print("%s|%s|%s|%s" % (a.get("alert") or a.get("name"), a.get("risk"), a.get("param"), a.get("evidence")))
        raise SystemExit
print("")' "${ALERT_NAME}"
}

ensure_ready() {
    [ -n "${K}" ] || { fail "ZAP_API_KEY is not set" "the .env file is missing or not loaded" "run from the repo so .env loads"; return 1; }
    zap core/view/version | grep -q '"version"' || {
        fail "ZAP API not reachable" "the stack may still be starting" "run scripts/demo_up.sh, wait for 'Up', then retry"; return 1; }
    [ -f "${RULE_FILE_HOST}" ] || {
        fail "active-rule script not found" "zap-scripts/globomantics-active-rule.py is missing" "restore the file from the repo"; return 1; }
    [ -f "${AUTH_FILE_HOST}" ] || {
        fail "authentication script not found" "zap-scripts/globomantics-auth.py is missing" "restore the file from the repo"; return 1; }
    local eng; eng="$(detect_jython_engine)"
    [ -n "${eng}" ] || {
        fail "no Python (jython) engine in ZAP" "the Python Scripting (jython) add-on is not installed" \
             "recreate ZAP so the entrypoint installs it: docker compose up -d --force-recreate zap"; return 1; }
    JYTHON_ENGINE="${eng}"
    return 0
}

# ===========================================================================
# STEP 1 — Python active-rule source (EO2b)
# ===========================================================================
step1_active_rule_source() {
    fm header "The custom Python active-scan rule" \
              "A Jython active rule runs your own check during an active scan — the house-specific test a built-in rule does not cover (EO2b)."
    local ok=1
    grep -q 'def scan(' "${RULE_FILE_HOST}" || ok=0
    grep -q 'newAlert(' "${RULE_FILE_HOST}" || ok=0
    grep -q 'Globomantics unsafe reflection' "${RULE_FILE_HOST}" || ok=0
    fm star "Script name" "${RULE_NAME}   (type: active · engine: ${JYTHON_ENGINE:-Jython})"
    fm star "Alert it raises" "${ALERT_NAME}" focus
    if [ "${ok}" = 1 ] && load_script "${RULE_NAME}" "active" "${JYTHON_ENGINE}" "${RULE_FILE_ZAP}"; then
        zap script/action/enable "scriptName=$(enc "${RULE_NAME}")" >/dev/null 2>&1 || true
        pass "active-rule script is valid and loaded into ZAP as an active rule"
    else
        fail "active-rule script did not validate or load" \
             "the source is missing scan()/raiseAlert(), or ZAP rejected the load" \
             "ask: 'the globomantics-active-rule Jython script failed to load; check the engine name and script body'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2 — Authentication script source (EO2c)
# ===========================================================================
step2_auth_script_source() {
    fm header "The scripted authentication" \
              "A ZAP authentication script logs in for you, so scans run as a real user (EO2c)."
    local ok=1
    grep -q 'def authenticate(' "${AUTH_FILE_HOST}" || ok=0
    grep -q 'getCredentialsParamsNames' "${AUTH_FILE_HOST}" || ok=0
    grep -q '/login' <(grep -i 'login' "${AUTH_FILE_HOST}") || true
    fm star "Script name" "${AUTH_NAME}   (type: authentication · engine: ${JYTHON_ENGINE:-Jython})"
    fm star "It submits" "username=${LOGIN_USER} to POST /login, then ZAP reuses the session cookie" focus
    if [ "${ok}" = 1 ] && load_script "${AUTH_NAME}" "authentication" "${JYTHON_ENGINE}" "${AUTH_FILE_ZAP}"; then
        local info; info="$(script_info "${AUTH_NAME}")"
        if [ -n "${info}" ]; then
            pass "authentication script is valid and registered in ZAP"
        else
            fail "authentication script loaded but is not registered" "ZAP did not list it" \
                 "ask: 're-load globomantics-auth with scriptType=authentication'"
        fi
    else
        fail "authentication script did not validate or load" \
             "the source is missing authenticate()/getCredentialsParamsNames(), or ZAP rejected the load" \
             "ask: 'the globomantics-auth Jython script failed to load; check the engine name and script body'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3 — Authenticated custom-scan result (EO2b · EO2c)
# ===========================================================================
step3_authenticated_scan() {
    fm header "The custom rule running against the authenticated endpoint" \
              "Scripted authentication logs in; the custom rule then scans a page that only exists when logged in (EO2b · EO2c)."

    # 3a. Prove the endpoint is truly session-gated, then log in.
    local no_cookie; no_cookie="$(status_no_cookie "${PROFILE_URL}")"
    local cookie; cookie="$(login_cookie)"
    if [ -z "${cookie}" ]; then
        fail "login did not return a session cookie" "POST /login via the proxy produced no session" \
             "ask: 'the Globomantics login did not set a session cookie; check POST /login'"
        return "${STEP_RC}"
    fi
    local with_cookie; with_cookie="$(status_with_cookie "${PROFILE_URL}" "${cookie}")"
    fm star "Without login" "/account/profile -> HTTP ${no_cookie}  (gated)"
    fm star "After scripted login" "/account/profile -> HTTP ${with_cookie}  (reachable)" focus

    if [ "${no_cookie}" != "401" ] || [ "${with_cookie}" != "200" ]; then
        fail "the authenticated endpoint did not behave as expected" \
             "expected 401 without login and 200 with the session cookie" \
             "ask: 'check /account/profile is 401 without a session and 200 with one'"
        return "${STEP_RC}"
    fi

    # 3b. Run an active scan with the full default policy (so ZAP discovers the
    #     note parameter and runs every enabled active rule, ours included).
    #     Inject the session cookie into all scan traffic, and re-seed the
    #     authenticated request so the scanned node carries the cookie + note.
    enable_all_scanners
    add_auth_cookie_header "${cookie}"
    curl -s -x "${PROXY}" -o /dev/null -b "session=${cookie}" "${PROFILE_URL}"
    local sid; sid="$(start_scan "${PROFILE_URL}")"
    if [ -z "${sid}" ]; then
        remove_auth_cookie_header
        fail "could not start the active scan" "ascan/action/scan returned no scan id" \
             "ask: 'the active scan did not start against the authenticated profile URL'"
        return "${STEP_RC}"
    fi
    local i
    for i in $(seq 1 90); do
        scan_done "${sid}" && break
        sleep 2
    done
    remove_auth_cookie_header
    local sent; sent="$(scan_messages_count "${sid}")"
    if scan_done "${sid}"; then
        fm star "Scan target" "${PROFILE_URL} (param: note)"
        fm star "Probe requests the scan sent" "${sent}"
        pass "the custom rule ran an authenticated active scan to completion"
    else
        fail "the active scan did not finish in time" "it is still running after ~2 minutes" \
             "ask: 're-run; if it persists, check the ZAP active scan status'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4 — Custom alert record (EO2b)
# ===========================================================================
step4_custom_alert() {
    fm header "The custom alert the rule raised" \
              "A rule you can trust raises a clear, named alert you can hand to a pipeline (EO2b)."
    local rec; rec="$(custom_alert)"
    if [ -n "${rec}" ]; then
        IFS='|' read -r n r p e <<<"${rec}"
        fm star "Alert" "${n}" focus
        fm star "Risk" "${r}"
        fm star "Parameter" "${p}"
        fm star "Evidence" "${e}"
        pass "the custom rule raised its intended alert on the authenticated endpoint"
    else
        fail "the custom alert was not raised" \
             "the scan finished but no Globomantics custom alert is recorded" \
             "ask: 'the globomantics-active-rule did not raise its alert; check the rule is enabled and the scan ran authenticated'"
    fi
    return "${STEP_RC}"
}
