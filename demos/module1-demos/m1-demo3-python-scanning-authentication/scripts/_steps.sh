#!/bin/bash
# Shared step library for m1-c5 "Write Python scan and authentication scripts
# in ZAP".
#
# Sourced by preflight_check.sh (author tooling). The demo itself is authored in
# ZAP's Script Console (GUI); this library proves, through the ZAP API, that the
# two Jython scripts behave as the runbook describes:
#   1. Python active-rule source
#   2. Authentication script source
#   3. ZAP runs the authentication script and holds the session (EO2c)
#   4. The custom rule raises a FRESH named alert on that scan (EO2b)
#
# Every request targets ONLY the local Globomantics app on the compose network.

HERE_STEPS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO_DIR="$(cd "${HERE_STEPS}/.." && pwd)"
REPO_ROOT="$(cd "${DEMO_DIR}/../../.." && pwd)"
# shellcheck disable=SC1091
source "${REPO_ROOT}/runtime/scripts/lib.sh"
FMT="${REPO_ROOT}/runtime/scripts/fmt.py"
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
LOGIN_URL="${APP_INTERNAL}/login"
PROFILE_URL="${APP_INTERNAL}/account/profile?note=seed"
SCRIPT_RULES_ID="50000"   # ZAP "Script Active Scan Rules" plugin
SCRIPT_POLICY="m1c5-script"   # policy that runs the custom rule at LOW threshold
RULE_TRACE_ZAP="/tmp/globo-rule-trace.log"   # author diagnostics the rule writes
AUTH_TRACE_ZAP="/tmp/globo-auth-trace.log"   # author diagnostics the auth script writes
CTX_NAME="globo-m1c5"                        # context the preflight configures

# Set by step 3 and reused by step 4.
CTX_ID=""
USER_ID=""

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

# Pull a single key out of a flat ZAP JSON response.
json_get() { python3 -c 'import json,sys
key=sys.argv[1]
try: print(json.load(sys.stdin).get(key,""))
except Exception: print("")' "$1"; }

detect_jython_engine() {
    zap script/view/listEngines | python3 -c '
import json,sys
engs = json.load(sys.stdin).get("listEngines", [])
for e in engs:
    if "jython" in e.lower() or "python" in e.lower():
        print(e); raise SystemExit
print("")'
}

load_script() { # <name> <type> <engine> <fileName>  -> sets LOAD_SOURCE
    # Never remove a script the author wrote in ZAP's Script Console: keep it.
    if [ -n "$(script_info "$1")" ]; then
        LOAD_SOURCE="already in ZAP (Script Console)"; return 0
    fi
    zap script/action/load \
        "scriptName=$(enc "$1")&scriptType=$(enc "$2")&scriptEngine=$(enc "$3")&fileName=$(enc "$4")&scriptDescription=$(enc 'Globomantics course demo')" \
        >/dev/null || return 1
    LOAD_SOURCE="loaded from $4"
}

addon_version() { # <addon id> -> installed version (empty if absent)
    zap autoupdate/view/installedAddons | python3 -c '
import json,sys
print(next((a.get("version","") for a in json.load(sys.stdin).get("installedAddons",[]) if a.get("id")==sys.argv[1]), ""))' "$1"
}

script_has_error() { # <name> -> "true" / "false" / "" (ZAP's own compile/run error flag)
    zap script/view/listScripts | python3 -c '
import json,sys
for s in json.load(sys.stdin).get("listScripts",[]):
    if s.get("name")==sys.argv[1]: print(str(s.get("error","")).lower()); break' "$1"
}

STATE_FILE="${DEMO_DIR}/logs/.m1demo3-state"   # carries absent-before + scan id from Step 3 to Step 4

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

status_no_cookie() {  # <url> -> HTTP code (through the ZAP proxy)
    curl -s -x "${PROXY}" -o /tmp/.z3profile -w '%{http_code}' "$1"
}

# --- container diagnostics (author-only) ------------------------------------
# Resolve the running ZAP container id the same way demo_up.sh brought it up:
# docker compose from the repo root, so the project name matches.
zap_container() {
    ( cd "${REPO_ROOT}" && docker compose ps -q zap 2>/dev/null ) | head -1
}
# Reset a trace file so a run's trace reflects only this scan. Remove (don't
# truncate) it: the scripts run as uid 1000 and must be able to create the file
# themselves, so we never leave a root-owned file they cannot append to.
reset_trace() { # <path-in-container>
    local c; c="$(zap_container)"
    [ -n "${c}" ] && docker exec "${c}" sh -c "rm -f $1" >/dev/null 2>&1 || true
}
read_trace() { # <path-in-container>
    local c; c="$(zap_container)"
    [ -n "${c}" ] && docker exec "${c}" sh -c "cat $1 2>/dev/null" || true
}
reset_rule_trace() { reset_trace "${RULE_TRACE_ZAP}"; }
rule_trace()       { read_trace  "${RULE_TRACE_ZAP}"; }
reset_auth_trace() { reset_trace "${AUTH_TRACE_ZAP}"; }
auth_trace()       { read_trace  "${AUTH_TRACE_ZAP}"; }

# ZAP's own record of whether the script errored at load/invocation time.
script_error_json() { # <name> -> compact JSON (empty if absent)
    zap script/view/listScripts | python3 -c '
import json,sys
name=sys.argv[1]
try: d=json.load(sys.stdin)
except Exception: print(""); raise SystemExit
for s in d.get("listScripts",[]):
    if s.get("name")==name:
        keep={k:s.get(k) for k in ("type","engine","enabled","error","errorDetails","lastErrorDetails") if k in s}
        print(json.dumps(keep)); raise SystemExit
print("")' "$1"
}
script_rules_enabled() { # -> "true"/"false"/""  (plugin 50000 in the policy)
    zap ascan/view/scanners | python3 -c '
import json,sys
try: data=json.load(sys.stdin)
except Exception: print(""); raise SystemExit
for s in data.get("scanners", []):
    if str(s.get("id"))=="50000":
        print(s.get("enabled","")); raise SystemExit
print("")'
}

# --- ZAP script-based authentication setup (EO2c) ---------------------------
# Configure a context so ZAP ITSELF logs in by running the authentication
# script, instead of the preflight logging in and injecting a cookie.
get_or_create_context() { # <name> -> contextId
    local id
    id="$(zap context/action/newContext "contextName=$(enc "$1")" 2>/dev/null | json_get contextId)"
    if [ -z "${id}" ]; then
        id="$(zap context/view/context "contextName=$(enc "$1")" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("context",{}).get("id",""))
except Exception: print("")')"
    fi
    echo "${id}"
}
forced_user_mode() { # <true|false>
    zap forcedUser/action/setForcedUserModeEnabled "boolean=$1" >/dev/null 2>&1 || true
}
# Run the full context + user setup. Appends any failed call to SETUP_ERRS.
SETUP_ERRS=""
setup_script_auth() { # sets CTX_ID and USER_ID
    SETUP_ERRS=""
    CTX_ID="$(get_or_create_context "${CTX_NAME}")"
    [ -n "${CTX_ID}" ] || { SETUP_ERRS="${SETUP_ERRS} newContext"; return 1; }

    zap context/action/includeInContext \
        "contextName=$(enc "${CTX_NAME}")&regex=$(enc 'http://app:8000.*')" >/dev/null 2>&1 \
        || SETUP_ERRS="${SETUP_ERRS} includeInContext"

    zap sessionManagement/action/setSessionManagementMethod \
        "contextId=${CTX_ID}&methodName=cookieBasedSessionManagement&methodconfigparams=" >/dev/null 2>&1 \
        || SETUP_ERRS="${SETUP_ERRS} sessionManagement"

    # scriptBasedAuthentication: the whole inner config is one URL-encoded value.
    local inner="scriptName=${AUTH_NAME}&Login URL=${LOGIN_URL}"
    zap authentication/action/setAuthenticationMethod \
        "contextId=${CTX_ID}&authMethodName=scriptBasedAuthentication&authMethodConfigParams=$(enc "${inner}")" >/dev/null 2>&1 \
        || SETUP_ERRS="${SETUP_ERRS} setAuthenticationMethod"

    # The profile page shows "Signed in as <user>" only when authenticated, so
    # this logged-in indicator tells ZAP when the login script has succeeded.
    # (Same indicator the runbook configures in the Context dialog.)
    zap authentication/action/setLoggedInIndicator \
        "contextId=${CTX_ID}&loggedInIndicatorRegex=$(enc 'Signed in as')" >/dev/null 2>&1 \
        || SETUP_ERRS="${SETUP_ERRS} loggedInIndicator"

    # Reuse the user if a previous run already created it (no duplicate users).
    USER_ID="$(zap users/view/usersList "contextId=${CTX_ID}" | python3 -c '
import json,sys
print(next((u.get("id","") for u in json.load(sys.stdin).get("usersList",[]) if u.get("name")==sys.argv[1]), ""))' "${LOGIN_USER}")"
    [ -n "${USER_ID}" ] || USER_ID="$(zap users/action/newUser "contextId=${CTX_ID}&name=$(enc "${LOGIN_USER}")" 2>/dev/null | json_get userId)"
    [ -n "${USER_ID}" ] || { SETUP_ERRS="${SETUP_ERRS} newUser"; return 1; }

    zap users/action/setAuthenticationCredentials \
        "contextId=${CTX_ID}&userId=${USER_ID}&authCredentialsConfigParams=$(enc "username=${LOGIN_USER}")" >/dev/null 2>&1 \
        || SETUP_ERRS="${SETUP_ERRS} setCredentials"
    zap users/action/setUserEnabled \
        "contextId=${CTX_ID}&userId=${USER_ID}&enabled=true" >/dev/null 2>&1 \
        || SETUP_ERRS="${SETUP_ERRS} enableUser"
    zap forcedUser/action/setForcedUser \
        "contextId=${CTX_ID}&userId=${USER_ID}" >/dev/null 2>&1 \
        || SETUP_ERRS="${SETUP_ERRS} setForcedUser"
    return 0
}

# --- active scan helpers ----------------------------------------------------
enable_all_scanners() {
    zap ascan/action/enableAllScanners >/dev/null 2>&1 || true
    zap ascan/action/enableScanners "ids=${SCRIPT_RULES_ID}" >/dev/null 2>&1 || true
}
# Build a focused policy that runs ONLY the Script Active Scan Rules plugin
# (50000) at LOW threshold / MEDIUM strength — the same configuration the
# Module 2 AF plan uses, which reliably routes the scan into the custom rule.
# The default policy does not always invoke the script rule on a single node.
build_script_policy() {
    zap ascan/action/removeScanPolicy "scanPolicyName=$(enc "${SCRIPT_POLICY}")" >/dev/null 2>&1 || true
    zap ascan/action/addScanPolicy "scanPolicyName=$(enc "${SCRIPT_POLICY}")" >/dev/null 2>&1 || true
    zap ascan/action/disableAllScanners "scanPolicyName=$(enc "${SCRIPT_POLICY}")" >/dev/null 2>&1 || true
    zap ascan/action/enableScanners "ids=${SCRIPT_RULES_ID}&scanPolicyName=$(enc "${SCRIPT_POLICY}")" >/dev/null 2>&1 || true
    zap ascan/action/setScannerAttackStrength "id=${SCRIPT_RULES_ID}&attackStrength=MEDIUM&scanPolicyName=$(enc "${SCRIPT_POLICY}")" >/dev/null 2>&1 || true
    zap ascan/action/setScannerAlertThreshold "id=${SCRIPT_RULES_ID}&alertThreshold=LOW&scanPolicyName=$(enc "${SCRIPT_POLICY}")" >/dev/null 2>&1 || true
}
del_all_alerts() { zap core/action/deleteAllAlerts >/dev/null 2>&1 || true; }
scan_messages_count() { # <scanId> -> number of probe requests the scan sent
    zap ascan/view/messagesIds "scanId=$1" | python3 -c 'import json,sys
try: print(len(json.load(sys.stdin).get("messagesIds",[])))
except Exception: print("0")'
}
start_scan_as_user() { # <url> <contextId> <userId> -> scanId (empty on failure)
    zap ascan/action/scanAsUser \
        "url=$(enc "$1")&contextId=$2&userId=$3&recurse=false&scanPolicyName=$(enc "${SCRIPT_POLICY}")" | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin); print(d.get("scanAsUser") or d.get("scan") or "")
except Exception: print("")'
}
scan_done() { # <scanId> -> 0 when status is 100
    local pct
    pct="$(zap ascan/view/status "scanId=$1" | json_get status)"
    [ "${pct}" = "100" ]
}
custom_alert() { # -> name|risk|param|evidence  (empty if not raised)
    zap core/view/alerts | python3 -c '
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
    local ok=1 jv
    jv="$(addon_version jython)"
    fm star "Python Scripting (jython) add-on installed" "${jv:-NOT INSTALLED}" focus
    grep -q 'def scan(' "${RULE_FILE_HOST}" || ok=0
    grep -qE 'raiseAlert\(|newAlert\(' "${RULE_FILE_HOST}" || ok=0
    fm star "Saved rule source" "zap-scripts/globomantics-active-rule.py  (sha256 $(sha256sum "${RULE_FILE_HOST}" | cut -c1-12))"
    fm star "Alert name in the source" "$(grep -o 'Globomantics unsafe reflection[^"]*' "${RULE_FILE_HOST}" | head -1)" focus
    if [ "${ok}" = 1 ] && [ -n "${jv}" ] && load_script "${RULE_NAME}" "active" "${JYTHON_ENGINE}" "${RULE_FILE_ZAP}"; then
        zap script/action/enable "scriptName=$(enc "${RULE_NAME}")" >/dev/null || ok=0
        local info err; info="$(script_info "${RULE_NAME}")"; err="$(script_has_error "${RULE_NAME}")"
        IFS='|' read -r n t e en <<<"${info}"
        fm star "Registered in ZAP" "${n} · type ${t} · engine ${e} · enabled ${en}"
        fm star "ZAP compile/run error flag" "${err:-unknown}" focus
        fm star "Source" "${LOAD_SOURCE}"
        if [ "${ok}" = 1 ] && [ "${t}" = "active" ] && [ "${en}" = "true" ] && [ "${err}" = "false" ]; then
            pass "the Jython active rule is registered, enabled and loaded without errors"
        else
            fail "the active rule is not usable (type=${t} enabled=${en} error=${err})" "the Jython source has an error or did not register" "fix the script in the Script Console and save it again"
        fi
    else
        fail "active-rule script did not validate or load" \
             "jython missing, the source lacks scan()/newAlert(), or ZAP rejected the load" \
             "check the add-on and the script body"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2 — Authentication script source (EO2c)
# ===========================================================================
step2_auth_script_source() {
    fm header "The scripted authentication" \
              "A ZAP authentication script submits the credentials; a logged-in check tells ZAP the login worked (EO2c)."
    local ok=1
    grep -q 'def authenticate(' "${AUTH_FILE_HOST}" || ok=0
    grep -q 'getCredentialsParamsNames' "${AUTH_FILE_HOST}" || ok=0
    fm star "Saved auth source" "zap-scripts/globomantics-auth.py  (sha256 $(sha256sum "${AUTH_FILE_HOST}" | cut -c1-12))"
    fm star "Credential submission in authenticate()" "$(grep -oE 'POST|/login|username' "${AUTH_FILE_HOST}" | sort -u | tr '\n' ' ')" focus
    if [ "${ok}" = 1 ] && load_script "${AUTH_NAME}" "authentication" "${JYTHON_ENGINE}" "${AUTH_FILE_ZAP}"; then
        local err; err="$(script_has_error "${AUTH_NAME}")"
        setup_script_auth || ok=0
        local ind; ind="$(zap authentication/view/getLoggedInIndicator "contextId=${CTX_ID}" | json_get logged_in_regex)"
        # Prove the logged-in check matches a real logged-in page and not a logged-out one.
        local J=/tmp/.z3login page_in page_out
        curl -s -o /dev/null -c "${J}" -X POST --data "username=${LOGIN_USER}" "http://localhost:8000/login" >/dev/null
        page_in="$(curl -s -b "${J}" "http://localhost:8000/account/profile?note=x" | grep -c "${ind:-Signed in as}")"
        page_out="$(curl -s "http://localhost:8000/account/profile?note=x" | grep -c "${ind:-Signed in as}")"
        fm star "Registered in ZAP" "${AUTH_NAME} · type authentication · error flag ${err:-unknown}"
        fm star "Logged-in verification (regex ZAP uses)" "${ind:-<none>}" focus
        fm star "Regex matches logged-in page / logged-out page" "${page_in} / ${page_out}" focus
        if [ "${ok}" = 1 ] && [ "${err}" = "false" ] && [ -n "${ind}" ] && [ "${page_in}" -ge 1 ] && [ "${page_out}" = 0 ]; then
            pass "authentication script registered and its logged-in check tells a logged-in page from a logged-out one"
        else
            fail "authentication setup incomplete (error=${err} indicator='${ind}' in=${page_in} out=${page_out}; failed calls:${SETUP_ERRS:- none})" \
                 "the script or the logged-in check is not valid" "fix the script or the indicator, then re-run"
        fi
    else
        fail "authentication script did not validate or load" \
             "the source lacks authenticate()/getCredentialsParamsNames(), or ZAP rejected the load" \
             "check the engine name and script body"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3 — Scripted authentication + custom rule on the authenticated endpoint (EO2b, EO2c)
# ===========================================================================
step3_auth_executes() {
    fm header "ZAP logs in with your script, then runs your rule as that user" \
              "ZAP executes the login script to get a session and scans the logged-in-only page with the custom Python rule — no cookie supplied by us (EO2b, EO2c)."
    forced_user_mode false
    local gated; gated="$(status_no_cookie "${PROFILE_URL}")"
    setup_script_auth
    reset_auth_trace
    forced_user_mode true
    local authed; authed="$(status_no_cookie "${APP_INTERNAL}/account/profile?note=authprobe")"
    local tr; tr="$(auth_trace)"
    fm star "Without login" "/account/profile -> HTTP ${gated}"
    fm star "ZAP forced-user (script auth)" "/account/profile -> HTTP ${authed}" focus
    fm star "Auth script ran" "$(echo "${tr}" | grep -m1 'authenticate:')"

    # Fresh alert store, then the custom rule scans the page AS the scripted user.
    del_all_alerts
    local before; before="$(custom_alert)"
    build_script_policy
    reset_rule_trace
    local sid="" i done=0
    [ -n "${CTX_ID}" ] && [ -n "${USER_ID}" ] && sid="$(start_scan_as_user "${PROFILE_URL}" "${CTX_ID}" "${USER_ID}")"
    if [ -n "${sid}" ]; then
        for i in $(seq 1 90); do scan_done "${sid}" && { done=1; break; }; sleep 2; done
    fi
    local sent; sent="$(scan_messages_count "${sid:-0}")"
    local rtr; rtr="$(rule_trace)"
    forced_user_mode false
    fm star "Custom rule scan as user ${LOGIN_USER}" "scan ${sid:-none} · $([ "${done}" = 1 ] && echo finished || echo NOT finished) · ${sent} probe requests" focus
    fm star "Rule saw the logged-in page (note reflected)" "$(echo "${rtr}" | grep -m1 -E '^(raised|reflected):' || echo 'no — rule trace: '"$(echo "${rtr}" | head -1)")"
    mkdir -p "$(dirname "${STATE_FILE}")"
    printf 'before=%s\nscan=%s\n' "$([ -z "${before}" ] && echo absent || echo present)" "${sid}" > "${STATE_FILE}"

    if [ "${gated}" = "401" ] && [ "${authed}" = "200" ] && echo "${tr}" | grep -q 'authenticate:' \
       && [ "${done}" = 1 ] && [ "${sent:-0}" -gt 0 ] && echo "${rtr}" | grep -qE '^(raised|reflected):'; then
        pass "ZAP authenticated with the script and ran the custom rule against the logged-in page"
    else
        fail "scripted authentication or the authenticated rule scan did not complete" \
             "expected 401 → 200 with an authenticate() trace, then a finished scan with authenticated probes" \
             "re-run Steps 1-2; check the context user (ctx=${CTX_ID:-none} user=${USER_ID:-none}; failed calls:${SETUP_ERRS:- none})"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4 — The custom rule raised its intended alert; record it for reuse (EO2b)
# ===========================================================================
step4_fresh_alert() {
    fm header "The custom alert the rule raised — recorded for the pipeline" \
              "The rule raised its named alert on the authenticated scan; the record is saved so Module 2 can expect the same alert (EO2b)."
    local before="" scan=""
    [ -f "${STATE_FILE}" ] && { before="$(grep '^before=' "${STATE_FILE}" | cut -d= -f2)"; scan="$(grep '^scan=' "${STATE_FILE}" | cut -d= -f2)"; }
    local rec; rec="$(zap core/view/alerts | python3 -c '
import json,sys
for a in json.load(sys.stdin).get("alerts",[]):
    if a.get("alert")==sys.argv[1]:
        print(json.dumps({k:a.get(k,"") for k in ("alert","pluginId","url","param","risk","confidence","evidence")})); break' "${ALERT_NAME}")"
    fm star "Before Step 3 scan" "${before:-unknown (run Step 3 first)}"
    if [ -n "${rec}" ]; then
        local f; for f in alert pluginId url param risk confidence; do
            fm star "${f}" "$(printf '%s' "${rec}" | python3 -c 'import json,sys;print(json.load(sys.stdin)[sys.argv[1]])' "${f}")" $([ "${f}" = alert ] && echo focus)
        done
        local out="${DEMO_DIR}/logs/custom-alert-record.json"
        printf '%s\n' "${rec}" | python3 -c 'import json,sys;d=json.load(sys.stdin);d["scanId"]=sys.argv[1];print(json.dumps(d,indent=2))' "${scan}" > "${out}"
        fm star "Alert record saved for Module 2" "logs/custom-alert-record.json" focus
    fi
    if [ "${before}" = "absent" ] && [ -n "${rec}" ]; then
        pass "the custom rule raised its named alert on this authenticated scan (absent before, present after) and the record is saved"
    else
        fail "no fresh custom alert to record (before=${before:-unknown})" \
             "Step 3 did not run, or the rule did not raise its alert" \
             "run Step 3, then Step 4"
    fi
    return "${STEP_RC}"
}
