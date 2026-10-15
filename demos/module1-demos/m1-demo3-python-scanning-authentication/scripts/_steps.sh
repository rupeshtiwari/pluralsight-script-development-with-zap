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

    USER_ID="$(zap users/action/newUser "contextId=${CTX_ID}&name=$(enc "${LOGIN_USER}")" 2>/dev/null | json_get userId)"
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
    local ok=1
    grep -q 'def scan(' "${RULE_FILE_HOST}" || ok=0
    grep -qE 'raiseAlert\(|newAlert\(' "${RULE_FILE_HOST}" || ok=0
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
# STEP 3 — ZAP runs the authentication script and holds the session (EO2c)
# ===========================================================================
# Prove that ZAP ITSELF authenticates by running the script: with a context
# configured for script-based authentication and a forced user, a request that
# carries NO cookie comes back 200, and the script's authenticate() leaves its
# trace. Nothing here supplies a cookie — the session comes from the script.
step3_auth_executes() {
    fm header "ZAP runs your authentication script" \
              "ZAP executes the login script to get a session, then reaches a page that only exists when logged in — no cookie supplied by us (EO2c)."

    # Clean auth state so the gating probe is honest (a prior run may have left
    # forced-user mode on).
    forced_user_mode false
    local gated; gated="$(status_no_cookie "${PROFILE_URL}")"

    setup_script_auth
    reset_auth_trace
    forced_user_mode true

    # Through the proxy, with NO cookie: forced-user mode makes ZAP authenticate
    # via the script before sending, so this should come back 200.
    local authed; authed="$(status_no_cookie "${APP_INTERNAL}/account/profile?note=authprobe")"
    local tr; tr="$(auth_trace)"

    fm star "Without login" "/account/profile -> HTTP ${gated}  (gated)"
    fm star "ZAP forced-user (script auth)" "/account/profile -> HTTP ${authed}  (reachable)" focus

    if [ "${gated}" = "401" ] && [ "${authed}" = "200" ] && echo "${tr}" | grep -q 'authenticate:'; then
        fm star "Auth script ran" "$(echo "${tr}" | tr '\n' ' ')"
        pass "ZAP executed the authentication script and holds the session (no cookie supplied by the preflight)"
    else
        fail "ZAP did not authenticate by running the script" \
             "expected gated=401 and authed=200 with an authenticate() trace; got gated=${gated} authed=${authed}" \
             "see the diagnosis below, then fix the context/auth setup (never weaken the check)"
        fm section "Why auth did not work — diagnosis"
        fm star "Context id" "${CTX_ID:-<none>}"
        fm star "User id" "${USER_ID:-<none>}"
        fm star "Setup calls that failed" "${SETUP_ERRS:- none}"
        fm note "Auth-script trace (empty = ZAP never called authenticate()):"
        echo "${tr:-<empty>}" | sed 's/^/      /'
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4 — The custom rule raises a FRESH named alert on that scan (EO2b)
# ===========================================================================
# Clear the alert store first and confirm the named alert is ABSENT, then scan
# the gated page AS THE AUTHENTICATED USER (ZAP's script provides the session)
# and confirm the alert is now PRESENT. Absent-before + present-after proves the
# alert is from this scan, not a leftover from an earlier run.
step4_fresh_alert() {
    fm header "The custom alert the rule raises" \
              "A rule you can trust raises a clear, named alert (EO2b). On screen it appears in ZAP's Alerts tab — the clip's proof artifact. We clear the store first so the alert is provably from this scan."

    del_all_alerts
    local before; before="$(custom_alert)"
    fm star "Before scan (store cleared)" "$([ -z "${before}" ] && echo 'absent' || echo "${before}")"

    build_script_policy
    reset_rule_trace
    # Seed the node as the forced user (no cookie), then scan it as that user.
    status_no_cookie "${PROFILE_URL}" >/dev/null
    local sid=""
    if [ -n "${CTX_ID}" ] && [ -n "${USER_ID}" ]; then
        sid="$(start_scan_as_user "${PROFILE_URL}" "${CTX_ID}" "${USER_ID}")"
    fi
    if [ -z "${sid}" ]; then
        fail "could not start the authenticated active scan" \
             "ascan/action/scanAsUser returned no scan id (context/user from step 3: ctx=${CTX_ID:-none} user=${USER_ID:-none})" \
             "re-run after step 3 passes; the scan reuses the script-authenticated user"
        forced_user_mode false
        return "${STEP_RC}"
    fi
    local i
    for i in $(seq 1 90); do scan_done "${sid}" && break; sleep 2; done
    local sent; sent="$(scan_messages_count "${sid}")"
    fm star "Scan target" "${PROFILE_URL} (param: note, as user ${LOGIN_USER})"
    fm star "Probe requests the scan sent" "${sent}"

    local after; after="$(custom_alert)"
    forced_user_mode false   # leave ZAP as we found it

    if [ -z "${before}" ] && [ -n "${after}" ]; then
        IFS='|' read -r n r p e <<<"${after}"
        fm star "Alert" "${n}" focus
        fm star "Risk" "${r}"
        fm star "Parameter" "${p}"
        fm star "Evidence" "${e}"
        pass "the custom rule RAISED its named alert on this scan — absent before, present after (verified via the ZAP API)"
    elif [ -n "${before}" ]; then
        fail "could not guarantee a fresh alert" \
             "the named alert was already present BEFORE the scan despite clearing the store" \
             "ask: 'core/action/deleteAllAlerts did not clear the store; check the ZAP API key and version'"
    else
        fail "the custom rule did not raise its named alert" \
             "core/view/alerts has no '${ALERT_NAME}' after the authenticated scan" \
             "see the diagnosis below, then fix accordingly (never weaken the check)"
        local se tr
        se="$(script_rules_enabled)"
        tr="$(rule_trace)"
        fm section "Why no alert — diagnosis"
        fm star "Script Active Scan Rules (50000) enabled" "${se:-unknown}"
        if [ -z "${tr}" ]; then
            fm note "The rule left NO trace — the scanner never entered our script."
            fm star "ZAP's record for this script" "$(script_error_json "${RULE_NAME}")"
            fm item "If error=true, the script failed to compile for Jython 2.7. If error=false, plugin 50000 did not route this scan to our script."
        elif echo "${tr}" | grep -q '^ERROR'; then
            fm note "The rule ran but a probe step threw:"
            echo "${tr}" | sed 's/^/      /'
            fm item "Fix the named call in globomantics-active-rule.py."
        elif echo "${tr}" | grep -q 'http=401'; then
            fm note "The rule ran but its probe was NOT authenticated (HTTP 401) — the scan is not carrying the script session:"
            echo "${tr}" | sed 's/^/      /'
            fm item "Fix: ensure the scan runs as the context user so ZAP applies the script-obtained session to probe requests."
        elif echo "${tr}" | grep -q '^raised:'; then
            fm note "The rule detected and raised, yet the alert is absent from the store:"
            echo "${tr}" | sed 's/^/      /'
            fm item "Investigate alert persistence for this build before weakening the check."
        else
            fm note "The rule ran but did not detect a reflection:"
            echo "${tr}" | sed 's/^/      /'
            fm item "Confirm note is reflected on /account/profile while authenticated."
        fi
    fi
    return "${STEP_RC}"
}
