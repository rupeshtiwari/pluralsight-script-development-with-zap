#!/bin/bash
# Shared step library for m1-c4 "Write a JavaScript security script in ZAP".
#
# Sourced by preflight_check.sh (author tooling). The committed JavaScript is loaded by API;
# live output is inspected in ZAP's Script Console (GUI). this library proves, through the ZAP API, that the
# JavaScript HTTP Sender script behaves as the runbook describes:
#   1. JavaScript source file   2. Modified HTTP request
#   3. Script console output    4. Saved script registration
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

SCRIPT_NAME="globomantics-marker"
SCRIPT_FILE_HOST="${DEMO_DIR}/zap-scripts/globomantics-marker.js"
SCRIPT_FILE_ZAP="/zap-scripts/globomantics-marker.js"
MARKER_HEADER="X-Globomantics-Marker"
MARKER_VALUE="GLOBO-DEMO"
CONSOLE_TAG="[globo-marker]"

PASS=0; FAIL=0; STEP_RC=0
pass() { fm ok "$1"; PASS=$((PASS+1)); STEP_RC=0; }
fail() { fm fail "$1" "${2:-}" "${3:-}"; FAIL=$((FAIL+1)); STEP_RC=1; }
enc()  { python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=""))' "$1"; }

zap() { # <path> <query> -> body (asserts HTTP 200)
    local path="$1" query="${2:-}" code
    code="$(curl -s -o /tmp/.zbody -w '%{http_code}' "${ZAP}/JSON/${path}/?apikey=${K}&${query}")"
    [ "${code}" = "200" ] || { echo "  (ZAP API ${path} -> HTTP ${code})" >&2; return 1; }
    cat /tmp/.zbody
}

detect_js_engine() {
    zap script/view/listEngines | python3 -c '
import json,sys
engs = json.load(sys.stdin).get("listEngines", [])
for pref in ("Graal.js", "graal", "ECMAScript", "JavaScript", "Nashorn"):
    for e in engs:
        if pref.lower() in e.lower():
            print(e); raise SystemExit
print("")'
}

script_registered() { # is a script with this name already in ZAP (e.g. written in the Script Console)?
    zap script/view/listScripts | python3 -c '
import json,sys
sys.exit(0 if any(r.get("name")==sys.argv[1] for r in json.load(sys.stdin).get("listScripts",[])) else 1)' "${SCRIPT_NAME}"
}

load_and_enable() { # <engine>  -> sets LOAD_SOURCE
    # Never remove a script the author wrote in ZAP's Script Console: keep it and enable it.
    if script_registered; then
        LOAD_SOURCE="already in ZAP (Script Console)"
    else
        zap script/action/load \
            "scriptName=$(enc "${SCRIPT_NAME}")&scriptType=httpsender&scriptEngine=$(enc "$1")&fileName=$(enc "${SCRIPT_FILE_ZAP}")&scriptDescription=$(enc 'Globomantics HTTP Sender marker (course demo)')" \
            >/dev/null || return 1
        LOAD_SOURCE="loaded from ${SCRIPT_FILE_ZAP}"
    fi
    zap script/action/enable "scriptName=$(enc "${SCRIPT_NAME}")" >/dev/null || return 1
    script_registration_valid
}

script_info() { # -> "name|type|engine|enabled|description"
    zap script/view/listScripts | python3 -c '
import json,sys
for s in json.load(sys.stdin).get("listScripts",[]):
    if s.get("name")==sys.argv[1]:
        print("|".join(str(s.get(k,"")).replace("|","/") for k in ("name","type","engine","enabled","description"))); break
' "${SCRIPT_NAME}"
}

console_line() { # the exact line the script printed last, stored by the script itself
    zap script/view/globalVar "varKey=globo.marker.lastLine" | python3 -c '
import json,sys
try: print(json.load(sys.stdin).get("globalVar",""))
except Exception: print("")'
}

script_registration_valid() {
    zap script/view/listScripts | python3 -c '
import json,sys
try: rows=json.load(sys.stdin).get("listScripts",[])
except Exception: sys.exit(1)
for r in rows:
    if r.get("name")==sys.argv[1]:
        sys.exit(0 if r.get("type")=="httpsender" and str(r.get("enabled")).lower()=="true" else 1)
sys.exit(1)' "${SCRIPT_NAME}"
}

send_probe() {
    # Have ZAP ITSELF send the request (accessUrl). HTTP Sender scripts fire for
    # requests ZAP sends, and the SENT request, carrying the marker header, is
    # what ZAP records in History. (A client request proxied through ZAP records
    # the client's original request, without the header the script adds on send.)
    PROBE_NAME="marker-$(date +%s)-${BASHPID:-$$}-${RANDOM}"
    PROBE_URL="${APP_INTERNAL}/greet?name=${PROBE_NAME}"
    zap core/action/accessUrl "url=$(enc "${PROBE_URL}")&followRedirects=false" >/dev/null 2>&1 || return 1
}


marker_request_line() {
    # Read the NEWEST messages: ZAP returns history oldest-first, so start near the end.
    local total start
    total="$(zap core/view/numberOfMessages "baseurl=$(enc "${APP_INTERNAL}")" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("numberOfMessages",0))' 2>/dev/null)"
    start=$(( ${total:-0} > 50 ? ${total:-0} - 50 : 0 ))
    zap core/view/messages "baseurl=$(enc "${APP_INTERNAL}")&start=${start}&count=50" | python3 -c '
import json,sys
want=sys.argv[1]
try: ms=json.load(sys.stdin).get("messages",[])
except Exception: sys.exit(1)
for m in reversed(ms):
    lines=m.get("requestHeader","").splitlines()
    if not lines or want not in lines[0]: continue
    hdr=next((line.strip() for line in lines if line.lower().startswith("x-globomantics-marker:")), "")
    if hdr=="X-Globomantics-Marker: GLOBO-DEMO":
        print(lines[0].strip()+" || "+hdr)
        sys.exit(0)
sys.exit(1)' "${PROBE_NAME}"
}

# Send a fresh probe and look for its marked request, retrying briefly. Right
# after Step 1 enables the HTTP Sender script via the API, ZAP can take a moment
# to activate it on the sending path, so a single immediate probe may miss it.
# Each attempt sends a NEW uniquely-named probe. This never weakens the check, 
# it still requires a real proxied request carrying the exact marker header.
probe_until_marked() { # -> prints "request-line || header" on success; empty on failure
    local i rec
    for i in 1 2 3 4 5 6; do
        if send_probe; then
            rec="$(marker_request_line)"
            [ -n "${rec}" ] && { printf '%s' "${rec}"; return 0; }
        fi
        sleep 2
    done
    printf ''
    return 1
}

ensure_ready() {
    [ -n "${K}" ] || { fail "ZAP_API_KEY is not set" "the .env file is missing or not loaded" "run from the repo so .env loads"; return 1; }
    zap core/view/version | grep -q '"version"' || {
        fail "ZAP API not reachable" "the stack may still be starting" "run scripts/demo_up.sh, wait for 'Up', then retry"; return 1; }
    [ -f "${SCRIPT_FILE_HOST}" ] || {
        fail "script file not found" "zap-scripts/globomantics-marker.js is missing" "restore the file from the repo"; return 1; }
    local eng; eng="$(detect_js_engine)"
    [ -n "${eng}" ] || {
        fail "no JavaScript engine in ZAP" "the GraalVM JavaScript add-on is not installed" \
             "install the GraalVM JavaScript add-on in the ZAP container"; return 1; }
    JS_ENGINE="${eng}"
    return 0
}

# ===========================================================================
# STEP 1, JavaScript source file (EO2a)
# ===========================================================================
step1_source() {
    fm header "The JavaScript HTTP Sender script" \
              "An HTTP Sender script runs for every message ZAP sends; this is where custom behavior lives (EO2a)."
    local ok=1 sum
    grep -q 'function sendingRequest' "${SCRIPT_FILE_HOST}" || ok=0
    grep -q "setHeader(MARKER_HEADER" "${SCRIPT_FILE_HOST}" || ok=0
    grep -q 'print(' "${SCRIPT_FILE_HOST}" || ok=0
    sum="$(sha256sum "${SCRIPT_FILE_HOST}" | cut -c1-12)"
    fm star "Saved source file" "zap-scripts/globomantics-marker.js  (sha256 ${sum})"
    fm star "sendingRequest() adds" "$(grep -o 'MARKER_HEADER *= *"[^"]*"' "${SCRIPT_FILE_HOST}" | head -1 | cut -d'"' -f2): $(grep -o 'MARKER_VALUE *= *"[^"]*"' "${SCRIPT_FILE_HOST}" | head -1 | cut -d'"' -f2)" focus
    if [ "${ok}" = 1 ] && load_and_enable "${JS_ENGINE}"; then
        local n t e en d; IFS='|' read -r n t e en d <<<"$(script_info)"
        fm star "Registered in ZAP" "${n} · type ${t} · engine ${e} · enabled ${en}" focus
        fm star "Source" "${LOAD_SOURCE}"
        pass "script is a valid HTTP Sender action and registered in ZAP"
    else
        fail "script did not validate or register" \
             "the source is missing sendingRequest/setHeader/print, or ZAP rejected the load" \
             "check the engine name and script body, then save it again"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2, Modified HTTP request (EO2a)
# ===========================================================================
step2_modified_request() {
    fm header "The marker header on an outbound request" \
              "Confirms the script actually changes messages ZAP sends, not just that it loaded (EO2a)."
    local rec; rec="$(probe_until_marked)"
    if [ -n "${rec}" ]; then
        fm star "Outbound request" "${rec%% || *}"
        fm star "Header added by the script" "${rec##* || }" focus
        pass "the script added ${MARKER_HEADER} to the outbound request"
    else
        fm star "Outbound request" "no marked request found"
        fail "no request carried the marker header" \
             "the script is not enabled, or the request did not pass through ZAP" \
             "re-run Step 1, then retry"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3, Script console output (EO2a)
# ===========================================================================
step3_console_output() {
    fm header "The named console output the script prints" \
              "A script that reports what it did is one you can trust and reuse (EO2a)."
    local rec line
    rec="$(probe_until_marked)"
    line="$(console_line)"
    fm star "Request that triggered the script" "${rec%% || *}"
    fm star "Line the script printed (read back from ZAP)" "${line:-<none>}" focus
    local probe; probe="$(printf '%s' "${rec}" | grep -o 'marker-[0-9A-Za-z_-]*' | head -1)"   # rec comes from a subshell
    if [ -n "${probe}" ] && [[ "${line}" == *"${CONSOLE_TAG}"*"${probe}"* ]]; then
        pass "the script printed its named line for this request; the same line is in ZAP's Script Console"
    else
        fail "no console line from the script for this request" \
             "the script is not enabled, or it does not print/store its line" \
             "check the print() and ScriptVars lines in the script, then re-run Step 1"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4, Saved script registration (EO2a)
# ===========================================================================
step4_registration() {
    fm header "The saved, reusable script registration" \
              "A named, saved script is what the Automation Framework calls later (EO2a)."
    local info n t e en d sum
    info="$(script_info)"
    if [ -n "${info}" ]; then
        IFS='|' read -r n t e en d <<<"${info}"
        sum="$(sha256sum "${SCRIPT_FILE_HOST}" | cut -c1-12)"
        fm star "Registered name" "${n}" focus
        fm star "Type · engine · enabled" "${t} · ${e} · ${en}"
        fm star "Saved file" "${SCRIPT_FILE_ZAP} in ZAP = zap-scripts/globomantics-marker.js in the demo folder (sha256 ${sum})" focus
        fm section "What Module 2 reuses (Automation Framework script job)"
        fm item "name: ${n} · type: ${t} · engine: ${e} · source: ${SCRIPT_FILE_ZAP}"
        if [ "${t}" = "httpsender" ] && [ "${en}" = "true" ] && [ -n "${e}" ]; then
            pass "script saved and registered as an enabled HTTP Sender, ready for the Automation Framework"
        else
            fail "script registration is incomplete" "type=${t} enabled=${en} engine=${e}" "run Step 1"
        fi
    else
        fail "script is not registered in ZAP" "Step 1 did not complete" "re-run Step 1"
    fi
    return "${STEP_RC}"
}
