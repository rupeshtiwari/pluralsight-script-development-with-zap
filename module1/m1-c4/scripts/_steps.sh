#!/bin/bash
# Shared step library for m1-c4 "Write a JavaScript security script in ZAP".
#
# Sourced by preflight_check.sh (author tooling). The demo itself is authored in
# ZAP's Script Console (GUI); this library proves, through the ZAP API, that the
# JavaScript HTTP Sender script behaves as the runbook describes:
#   1. JavaScript source file   2. Modified HTTP request
#   3. Script console output    4. Saved script registration
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

load_and_enable() { # <engine>
    zap script/action/remove "scriptName=$(enc "${SCRIPT_NAME}")" >/dev/null 2>&1 || true
    zap script/action/load \
        "scriptName=$(enc "${SCRIPT_NAME}")&scriptType=httpsender&scriptEngine=$(enc "$1")&fileName=$(enc "${SCRIPT_FILE_ZAP}")&scriptDescription=$(enc 'Globomantics HTTP Sender marker (course demo)')" \
        >/dev/null 2>&1 || return 1
    zap script/action/enable "scriptName=$(enc "${SCRIPT_NAME}")" >/dev/null 2>&1 || true
    return 0
}

send_probe() { curl -s -x "${PROXY}" -o /dev/null "${APP_INTERNAL}/greet?name=marker-check"; }

marker_request_line() {
    zap core/view/messages "baseurl=${APP_INTERNAL}&count=25" | python3 -c '
import json,sys
ms = json.load(sys.stdin).get("messages", [])
for m in reversed(ms):
    rh = m.get("requestHeader", "")
    if "X-Globomantics-Marker" in rh:
        lines = rh.splitlines()
        req = lines[0].strip() if lines else ""
        hdr = next((l.strip() for l in lines if l.lower().startswith("x-globomantics-marker")), "")
        print(req + " || " + hdr); raise SystemExit
print("")'
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
# STEP 1 — JavaScript source file (EO2a)
# ===========================================================================
step1_source() {
    fm header "The JavaScript HTTP Sender script" \
              "An HTTP Sender script runs for every message ZAP sends; this is where custom behavior lives (EO2a)."
    local ok=1
    grep -q 'function sendingRequest' "${SCRIPT_FILE_HOST}" || ok=0
    grep -q "setHeader(MARKER_HEADER" "${SCRIPT_FILE_HOST}" || ok=0
    grep -q 'print(CONSOLE_TAG' "${SCRIPT_FILE_HOST}" || ok=0
    fm star "Script name" "${SCRIPT_NAME}   (type: HTTP Sender · engine: ${JS_ENGINE:-GraalVM JS})"
    fm star "Marker header it adds" "${MARKER_HEADER}: ${MARKER_VALUE}" focus
    fm star "Named console line it prints" "${CONSOLE_TAG} added ${MARKER_HEADER}: ${MARKER_VALUE} to <url>" focus
    if [ "${ok}" = 1 ] && load_and_enable "${JS_ENGINE}"; then
        pass "script is a valid HTTP Sender action and loaded into ZAP"
    else
        fail "script did not validate or load" \
             "the source is missing sendingRequest/setHeader/print, or ZAP rejected the load" \
             "ask: 'the globomantics-marker HTTP Sender script failed to load in ZAP; check the engine name and script body'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2 — Modified HTTP request (EO2a)
# ===========================================================================
step2_modified_request() {
    fm header "The marker header on an outbound request" \
              "Confirms the script actually changes messages ZAP sends — not just that it loaded (EO2a)."
    send_probe
    local rec; rec="$(marker_request_line)"
    if [ -n "${rec}" ]; then
        fm star "Outbound request" "${rec%% || *}"
        fm star "Header added by the script" "${rec##* || }" focus
        pass "the script added ${MARKER_HEADER} to the outbound request"
    else
        fm star "Outbound request" "no marked request found"
        fail "no request carried the marker header" \
             "the script is not enabled, or the request did not pass through ZAP" \
             "ask: 'the globomantics-marker script did not add the header to a proxied request; check it is enabled'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3 — Script console output (EO2a)
# ===========================================================================
step3_console_output() {
    fm header "The named console output the script prints" \
              "A script that reports what it did is one you can trust and reuse (EO2a)."
    # The live console line appears in ZAP's Script Console. Here we confirm the
    # named line exists in the source and that the action runs (a fresh marked
    # request), which is what produces that console line.
    send_probe
    local rec; rec="$(marker_request_line)"
    fm star "Console line (seen in ZAP's Script Console)" "${CONSOLE_TAG} added ${MARKER_HEADER}: ${MARKER_VALUE} to <url>" focus
    if grep -q "print(CONSOLE_TAG" "${SCRIPT_FILE_HOST}" && [ -n "${rec}" ]; then
        pass "the script prints a named console line each time its action runs"
    else
        fail "the named console output was not produced" \
             "the print() line is missing or the action did not run" \
             "ask: 'the globomantics-marker script is not producing its named console line; check the print statement'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4 — Saved script registration (EO2a)
# ===========================================================================
step4_registration() {
    fm header "The saved, reusable script registration" \
              "A named, saved script is what the Automation Framework calls later (EO2a)."
    local info; info="$(zap script/view/listScripts | python3 -c '
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
print("")' "${SCRIPT_NAME}")"
    if [ -n "${info}" ]; then
        IFS='|' read -r n t e en <<<"${info}"
        fm star "Registered name" "${n}" focus
        fm star "Type" "${t}"
        fm star "Engine" "${e}"
        fm star "Enabled" "${en}"
        fm star "Path (repo)" "zap-scripts/globomantics-marker.js"
        [ "${t}" = "httpsender" ] \
            && pass "script is registered as a reusable HTTP Sender script" \
            || fail "script registered with the wrong type (${t})" "expected httpsender" \
                    "ask: 're-load globomantics-marker with scriptType=httpsender'"
    else
        fail "script is not registered in ZAP" "the load step did not complete" \
             "ask: 're-run step 1 to load and enable the globomantics-marker script'"
    fi
    return "${STEP_RC}"
}
