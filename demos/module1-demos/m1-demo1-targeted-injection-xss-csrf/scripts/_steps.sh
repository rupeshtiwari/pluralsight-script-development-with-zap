#!/bin/bash
# Shared step library for m1-c3 "Validate injection, XSS, and CSRF with ZAP".
#
# Sourced by both preflight_check.sh (runs all 4 steps for the log) and
# demo_step.sh (runs one step at a time). Defining the steps in ONE place
# means the runbook, the single-step runner, and the preflight can never drift.
#
# Every request targets ONLY the local Globomantics app on the compose network.

HERE_STEPS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${HERE_STEPS}/../../../.." && pwd)"
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/lib.sh"
FMT="${REPO_ROOT}/scripts/fmt.py"
fm() { python3 "${FMT}" "$@"; }

APP_INTERNAL="http://app:8000"        # how ZAP reaches the app (compose DNS)
ZAP="http://localhost:8090"           # ZAP API + proxy (same port)
PROXY="http://localhost:8090"
K="${ZAP_API_KEY:-}"   # lazy: the reference panel needs no key; ensure_ready checks it
POLICY="m1demo1"
POLICY_IDS="40018 40019 40020 40021 40022 40027 40033 90020 90037"
XSS_POLICY="m1xss"
XSS_IDS="40012 40014 40016 40017"   # reflected / persistent XSS active rules

PASS=0; FAIL=0; STEP_RC=0
pass() { fm ok "$1"; PASS=$((PASS+1)); STEP_RC=0; }
fail() { fm fail "$1" "${2:-}" "${3:-}"; FAIL=$((FAIL+1)); STEP_RC=1; }

enc()  { python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=""))' "$1"; }
jget() { python3 -c 'import json,sys;d=json.load(sys.stdin);ks=sys.argv[1].split(".");[d:=d[k] for k in ks];print(d)' "$1"; }

zap() { # <path> <query> -> body (asserts HTTP 200)
    local path="$1" query="${2:-}" code
    code="$(curl -s -o /tmp/.zbody -w '%{http_code}' "${ZAP}/JSON/${path}/?apikey=${K}&${query}")"
    [ "${code}" = "200" ] || { echo "  (ZAP API ${path} -> HTTP ${code})" >&2; return 1; }
    cat /tmp/.zbody
}

# ---- readiness -------------------------------------------------------------
ensure_ready() {
    [ -n "${K}" ] || {
        fail "ZAP_API_KEY is not set" "the .env file is missing or not loaded" \
             "run from the repo so .env loads, or export ZAP_API_KEY"
        return 1
    }
    zap core/view/version | grep -q '"version"' || {
        fail "ZAP API not reachable" "the stack may still be starting" \
             "run scripts/demo_up.sh, wait for 'Up', then retry"
        return 1
    }
    zap ascan/view/scanners | grep -q '"id":"40033"' || {
        fail "NoSQL rule 40033 not installed" "ascanrulesBeta did not install" \
             "check the zap container log for the add-on install step"
        return 1
    }
    return 0
}

build_policy_quiet() {
    zap ascan/action/removeScanPolicy "scanPolicyName=${POLICY}" >/dev/null 2>&1 || true
    zap ascan/action/addScanPolicy "scanPolicyName=${POLICY}" >/dev/null 2>&1 || true
    zap ascan/action/disableAllScanners "scanPolicyName=${POLICY}" >/dev/null 2>&1 || true
    local id
    for id in ${POLICY_IDS}; do
        zap ascan/action/enableScanners "ids=${id}&scanPolicyName=${POLICY}" >/dev/null 2>&1 || true
    done
}

scan_url_quiet() { # <url>  -- active-scan one endpoint, wait, no output
    local url="$1" eu sid st waited=0
    eu="$(enc "${url}")"
    zap core/action/accessUrl "url=${eu}&followRedirects=false" >/dev/null 2>&1 || return 1
    sid="$(zap ascan/action/scan "url=${eu}&recurse=false&scanPolicyName=${POLICY}" | jget scan 2>/dev/null)"
    [[ "${sid}" =~ ^[0-9]+$ ]] || return 1
    while :; do
        st="$(zap ascan/view/status "scanId=${sid}" | jget status 2>/dev/null)"
        [ "${st}" = "100" ] && break
        sleep 3; waited=$((waited+3)); [ "${waited}" -gt 300 ] && break
    done
}

first_alert() { # <url> "<id> <id>" -> "pluginId|risk|confidence" for the first match
    local url="$1" wanted="$2" base
    base="$(enc "${url%%\?*}")"
    zap core/view/alerts "baseurl=${base}" | python3 -c '
import json,sys
wanted=set(sys.argv[1].split())
for a in json.load(sys.stdin)["alerts"]:
    if a["pluginId"] in wanted:
        print("%s|%s|%s" % (a["pluginId"], a["risk"], a["confidence"])); break
' "${wanted}"
}

build_xss_policy_quiet() {
    zap ascan/action/removeScanPolicy "scanPolicyName=${XSS_POLICY}" >/dev/null 2>&1 || true
    zap ascan/action/addScanPolicy "scanPolicyName=${XSS_POLICY}" >/dev/null 2>&1 || true
    zap ascan/action/disableAllScanners "scanPolicyName=${XSS_POLICY}" >/dev/null 2>&1 || true
    local id
    for id in ${XSS_IDS}; do
        zap ascan/action/enableScanners "ids=${id}&scanPolicyName=${XSS_POLICY}" >/dev/null 2>&1 || true
    done
}

scan_xss_quiet() { # <url> -- active-scan one endpoint with the XSS policy, wait
    local url="$1" eu sid st waited=0
    eu="$(enc "${url}")"
    zap core/action/accessUrl "url=${eu}&followRedirects=false" >/dev/null 2>&1 || return 1
    sid="$(zap ascan/action/scan "url=${eu}&recurse=false&scanPolicyName=${XSS_POLICY}" | jget scan 2>/dev/null)"
    [[ "${sid}" =~ ^[0-9]+$ ]] || return 1
    while :; do
        st="$(zap ascan/view/status "scanId=${sid}" | jget status 2>/dev/null)"
        [ "${st}" = "100" ] && break
        sleep 3; waited=$((waited+3)); [ "${waited}" -gt 180 ] && break
    done
}

# ZAP's reflected-XSS alert on a URL -> "param|attack|evidence" (empty if none).
xss_alert() { # <url>
    local base; base="$(enc "${1%%\?*}")"
    zap core/view/alerts "baseurl=${base}" | python3 -c '
import json,sys
for a in json.load(sys.stdin)["alerts"]:
    nm = a.get("alert") or a.get("name") or ""
    if a.get("pluginId")=="40012" or "Cross Site Scripting (Reflected)" in nm:
        print("%s|%s|%s" % (a.get("param",""), a.get("attack",""), a.get("evidence","")))
        break
'
}

# ---- reference panel (not a step) -----------------------------------------
print_reference() {
    fm header "Before you test: map each case to its context / state" \
              "The context and the token state decide the test you run (EO1b, EO1c)."
    fm section "XSS execution contexts"
    fm item "HTML body — input lands between tags"
    fm item "HTML attribute — input lands inside a quoted attribute value"
    fm item "JavaScript string — input lands inside a quoted JS string"
    fm section "CSRF token states"
    fm item "valid for this session — the request should succeed"
    fm item "missing or invalid — the request should be rejected"
    fm item "a valid token reused with a DIFFERENT session's cookie — the request should be rejected: a token must be tied to the session it was issued to (same-session reuse is only a concern when the app requires single-use tokens)"
}

# ===========================================================================
# STEP 1 — Targeted injection scan (EO1a)  → "Targeted scan policy and rule list"
# ===========================================================================
step1_injection() {
    fm header "Targeted injection scan — one policy, three endpoints" \
              "Proves ZAP detects SQL, NoSQL, and command injection as real findings (EO1a)."
    build_policy_quiet
    fm star "Policy rules enabled" "SQL-injection family + NoSQL 40033 + command 90020/90037"

    fm note "running the focused scan across the three endpoints..."
    scan_url_quiet "${APP_INTERNAL}/search?q=Router"
    scan_url_quiet "${APP_INTERNAL}/api/account?username=alice"
    scan_url_quiet "${APP_INTERNAL}/admin/ping?host=127.0.0.1"

    fm section "Findings — alert raised per endpoint"
    local allok=1 rec pid risk conf
    _row() { # <label> <url> <ids>
        rec="$(first_alert "$2" "$3")"
        if [ -n "${rec}" ]; then
            IFS='|' read -r pid risk conf <<<"${rec}"
            fm star "$1" "alert ${pid} · ${risk}/${conf}" focus
        else
            fm star "$1" "NO ALERT RAISED" ; allok=0
        fi
    }
    _row "SQL injection · /search (q)"          "${APP_INTERNAL}/search?q=Router"          "40018 40022"
    _row "NoSQL injection · /api/account (username)" "${APP_INTERNAL}/api/account?username=alice" "40033"
    _row "Command injection · /admin/ping (host)"    "${APP_INTERNAL}/admin/ping?host=127.0.0.1" "90020 90037"

    [ "${allok}" = 1 ] \
        && pass "targeted scan raised all three injection alerts" \
        || fail "one or more injection alerts did not fire" \
                "an endpoint or the scan policy changed" \
                "ask: 're-check the injection endpoint in step 1 that raised no alert; fix the endpoint, not the check'"
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2 — XSS request and response body (EO1b)
# ===========================================================================
step2_xss() {
    fm header "Reflected XSS — match the context, then let ZAP confirm it" \
              "The output context decides the payload; ZAP's active scanner then proves an executable reflected XSS, not just a reflection (EO1b)."

    # Part A — the single 'name' input lands in three output contexts, so a real
    # test needs a context-specific payload for each. This is where you choose
    # the payload; it is NOT by itself proof of executable XSS.
    local marker='zzMARKzz' body b1 b2 b3
    body="$(curl -s -x "${PROXY}" "${APP_INTERNAL}/greet?name=$(enc "${marker}")")"
    fm section "Output contexts for the 'name' parameter (choose a payload per context)"
    b1="$(echo "${body}" | grep -o '<p>Hello[^<]*' | head -1)"
    b2="$(echo "${body}" | grep -oE 'type="text" value="[^"]*"' | head -1 | sed 's/^type="text" //')"
    b3="$(echo "${body}" | grep -o 'var greeting = "[^;]*' | head -1)"
    fm star "HTML body — use <script>…</script>" "${b1}"
    fm star "HTML attribute — break out with \">…" "${b2}"
    fm star "JS string — break out with \";…" "${b3}"
    local n=0
    echo "${body}" | grep -q "<p>Hello ${marker}"     && n=$((n+1))
    echo "${body}" | grep -q "value=\"${marker}\""     && n=$((n+1))
    echo "${body}" | grep -q "greeting = \"${marker}\"" && n=$((n+1))

    # Part B — ZAP actively scans 'name' with the reflected-XSS rules; it injects
    # real payloads and raises "Cross Site Scripting (Reflected)" only when the
    # reflection is actually exploitable in its context.
    build_xss_policy_quiet
    fm note "running ZAP's reflected-XSS scanner against /greet (name)..."
    scan_xss_quiet "${APP_INTERNAL}/greet?name=${marker}"
    local rec param attack evidence
    rec="$(xss_alert "${APP_INTERNAL}/greet")"
    IFS='|' read -r param attack evidence <<<"${rec}"

    fm section "ZAP's confirmed finding"
    fm star "Alert" "Cross Site Scripting (Reflected)" focus
    fm star "Affected parameter" "${param:-<none>}"
    fm star "Payload ZAP injected" "${attack:-<none>}" focus
    fm star "Evidence (reflected in the response)" "${evidence:-<none>}"

    if [ "${n}" = 3 ] && [ -n "${param}" ] && [ -n "${attack}" ]; then
        pass "ZAP confirmed reflected XSS on '${param}' with a context-specific payload (and the input lands in all three contexts)"
    else
        fail "reflected XSS was not confirmed (contexts ${n}/3; ZAP param='${param:-}')" \
             "the vulnerable build should reflect in 3 contexts and ZAP should raise Cross Site Scripting (Reflected) on name" \
             "ask: 'on the vulnerable build, /greet did not yield ZAP a Cross Site Scripting (Reflected) alert on name; check the XSS rules and the endpoint'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3 — CSRF token replay result (EO1c)
# ===========================================================================
step3_csrf() {
    fm header "CSRF — a token reused across sessions" \
              "A CSRF token must be tied to the session it was issued to. Here a token minted in one session is reused with a second session's cookie, and the protected email change still runs (EO1c)."
    local A=/tmp/.c_a B=/tmp/.c_b
    local legit="alice@globomantics.example" attack="attacker@evil.example"
    local tokenA tokenB v m before_x x after_x
    rm -f "${A}" "${B}"

    _post() { # <cookiejar> <data> -> HTTP code
        curl -s -x "${PROXY}" -o /dev/null -w '%{http_code}' -b "$1" -X POST --data "$2" "${APP_INTERNAL}/account/email"
    }
    _email() { # <cookiejar> -> stored email for that session
        curl -s -x "${PROXY}" -b "$1" "${APP_INTERNAL}/account/email/current" \
            | python3 -c 'import json,sys;print(json.load(sys.stdin).get("email",""))' 2>/dev/null
    }

    # Two independent authenticated sessions. A is where a valid token is minted;
    # B is the second session whose cookie rides the forged request.
    curl -s -x "${PROXY}" -o /dev/null -c "${A}" -X POST --data 'username=mallory' "${APP_INTERNAL}/login" >/dev/null
    curl -s -x "${PROXY}" -o /dev/null -c "${B}" -X POST --data 'username=alice'   "${APP_INTERNAL}/login" >/dev/null
    tokenA="$(curl -s -x "${PROXY}" -b "${A}" "${APP_INTERNAL}/account/email" | grep -o '[a-f0-9]\{32\}' | head -1)"
    tokenB="$(curl -s -x "${PROXY}" -b "${B}" "${APP_INTERNAL}/account/email" | grep -o '[a-f0-9]\{32\}' | head -1)"

    v="$(_post "${B}" "email=${legit}&csrf_token=${tokenB}")"   # control: B's own token
    m="$(_post "${B}" "email=${attack}")"                       # control: no token
    before_x="$(_email "${B}")"                                 # state after the valid control
    x="$(_post "${B}" "email=${attack}&csrf_token=${tokenA}")"  # A's token with B's cookie
    after_x="$(_email "${B}")"                                  # state after the cross-session request

    fm star "valid token (session B's own)" "${v}"
    fm star "missing token" "${m}"
    fm star "session B's email before the cross-session request" "${before_x}"
    fm star "token from session A, submitted with session B's cookie" "${x}  (should be rejected)" focus
    fm star "session B's email after the cross-session request" "${after_x}" focus

    if [ "${v} ${m} ${x}" = "200 403 200" ] && [ "${before_x}" = "${legit}" ] && [ "${after_x}" = "${attack}" ]; then
        pass "session A's token was accepted with session B's cookie (200) and changed session B's email to ${attack} — the token is not tied to its session"
    else
        fail "cross-session CSRF result was ${v}/${m}/${x}, email ${before_x:-<empty>} -> ${after_x:-<empty>} (expected 200/403/200 and ${legit} -> ${attack})" \
             "the vulnerable build should accept session A's token with session B's cookie and change state" \
             "ask: 'on the vulnerable build, the email-change handler is not accepting a cross-session token; inspect the CSRF check and /account/email/current'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4 — Alert disposition record (TO1: EO1a + EO1b + EO1c)
# Self-contained: re-confirms each finding from live app behavior.
# ===========================================================================
step4_disposition() {
    fm header "Alert disposition — reconcile each alert with app behavior" \
              "Turns raw alerts into decisions you can defend (EO1a, EO1b, EO1c)."
    local sqlerr b i ping xss
    sqlerr="$(curl -s -x "${PROXY}" "${APP_INTERNAL}/search?q=Router%27" | grep -o 'unterminated[^<]*' | head -1 \
              | python3 -c 'import html,sys;print(html.unescape(sys.stdin.read().strip()))')"
    b="$(curl -s -x "${PROXY}" "${APP_INTERNAL}/api/account?username=alice"     | python3 -c 'import json,sys;print(json.load(sys.stdin).get("count","?"))')"
    i="$(curl -s -x "${PROXY}" "${APP_INTERNAL}/api/account?username%5B%24ne%5D=" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("count","?"))')"
    ping="$(curl -s -x "${PROXY}" "${APP_INTERNAL}/admin/ping?host=127.0.0.1"    | grep -oE 'bytes from [0-9.]+' | head -1)"
    if curl -s -x "${PROXY}" "${APP_INTERNAL}/greet?name=zzMARKzz" | grep -q '<p>Hello zzMARKzz'; then xss="reflected unescaped"; else xss="encoded"; fi

    fm star "40018 SQL injection · /search" "confirmed — DB error: ${sqlerr:-none}" focus
    fm star "40033 NoSQL injection · /api/account" "confirmed — accounts ${b} → ${i} under operator injection" focus
    fm star "90020/90037 Command injection · /admin/ping" "confirmed — OS command ran: ${ping:-none}" focus
    fm star "XSS reflected · /greet" "confirmed — ${xss}" focus

    if [ -n "${sqlerr}" ] && [ "${i}" != "${b}" ] && [ -n "${ping}" ] && [ "${xss}" = "reflected unescaped" ]; then
        pass "all four findings reconciled with app behavior and recorded as confirmed"
    else
        fail "a finding could not be reconciled with app behavior" \
             "the app behaved differently than the disposition expects" \
             "ask: 're-check the disposition evidence for the finding that did not confirm on the vulnerable build'"
    fi
    return "${STEP_RC}"
}

run_step_by_number() { # <1|2|3|4|ref>
    case "$1" in
        ref) print_reference ;;
        1) step1_injection ;;
        2) step2_xss ;;
        3) step3_csrf ;;
        4) step4_disposition ;;
        *) echo "unknown step: $1 (use 1, 2, 3, 4, or ref)" >&2; return 2 ;;
    esac
}
