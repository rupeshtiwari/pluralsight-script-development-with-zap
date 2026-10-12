#!/bin/bash
# Shared step library for m1-c3 "Validate injection, XSS, and CSRF with ZAP".
#
# Sourced by both preflight_check.sh (runs all 4 steps for the log) and
# run_step.sh (runs one step for recording). Defining the steps in ONE place
# means the runbook, the single-step runner, and the preflight can never drift.
#
# Every request targets ONLY the local Globomantics app on the compose network.

HERE_STEPS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${HERE_STEPS}/../../.." && pwd)"
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

# ---- reference panel (not a step) -----------------------------------------
print_reference() {
    fm header "Before you test: map each case to its context / state" \
              "The context and the token state decide the test you run (EO1b, EO1c)."
    fm section "XSS execution contexts"
    fm item "HTML body — input lands between tags"
    fm item "HTML attribute — input lands inside a quoted attribute value"
    fm item "JavaScript string — input lands inside a quoted JS string"
    fm section "CSRF token states"
    fm item "valid — the request should succeed"
    fm item "missing or invalid — the request should be rejected"
    fm item "replayed — a token already used once should be rejected"
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
    fm header "Reflected XSS — one input, three output contexts" \
              "The output context decides the payload, so you match context before testing (EO1b)."
    local marker='zzMARKzz' body b1 b2 b3
    body="$(curl -s -x "${PROXY}" "${APP_INTERNAL}/greet?name=$(enc "${marker}")")"
    fm star "Request" "GET /greet?name=${marker}"
    fm section "Response body — reflected unescaped"
    b1="$(echo "${body}" | grep -o '<p>Hello[^<]*' | head -1)"
    # Anchor to the greeting input so a future header 'value=' can never be
    # picked up as the attribute context; strip the type= prefix for display.
    b2="$(echo "${body}" | grep -oE 'type="text" value="[^"]*"' | head -1 | sed 's/^type="text" //')"
    b3="$(echo "${body}" | grep -o 'var greeting = "[^;]*' | head -1)"
    fm star "HTML body context" "${b1}" focus
    fm star "HTML attribute context" "${b2}" focus
    fm star "JavaScript string context" "${b3}" focus
    local n=0
    echo "${body}" | grep -q "<p>Hello ${marker}"     && n=$((n+1))
    echo "${body}" | grep -q "value=\"${marker}\""     && n=$((n+1))
    echo "${body}" | grep -q "greeting = \"${marker}\"" && n=$((n+1))
    [ "${n}" = 3 ] \
        && pass "input reflects unescaped in all three contexts" \
        || fail "input reflected in only ${n}/3 contexts" \
                "one context may already be encoding output" \
                "ask: 'the /greet endpoint is not reflecting in all three contexts on the vulnerable build'"
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3 — CSRF token replay result (EO1c)
# ===========================================================================
step3_csrf() {
    fm header "CSRF — token replay" \
              "A token checked for presence but not freshness can be replayed (EO1c)."
    local ca=/tmp/.c_a t v m r
    rm -f "${ca}"
    _post() { curl -s -x "${PROXY}" -o /dev/null -w '%{http_code}' -b "${ca}" -X POST --data "$1" "${APP_INTERNAL}/account/email"; }
    curl -s -x "${PROXY}" -o /dev/null -c "${ca}" -X POST --data 'username=alice' "${APP_INTERNAL}/login" >/dev/null
    t="$(curl -s -x "${PROXY}" -b "${ca}" "${APP_INTERNAL}/account/email" | grep -o '[a-f0-9]\{32\}' | head -1)"
    v="$(_post "email=a@globomantics.example&csrf_token=${t}")"   # valid token
    m="$(_post "email=a@globomantics.example")"                   # no token
    r="$(_post "email=b@globomantics.example&csrf_token=${t}")"   # replay the used token
    fm star "valid token" "${v}"
    fm star "missing token" "${m}"
    fm star "replayed token (already used once)" "${r}" focus
    [ "${v} ${m} ${r}" = "200 403 200" ] \
        && pass "replayed token is accepted (200) — the CSRF protection has no freshness check" \
        || fail "CSRF codes are ${v}/${m}/${r}, expected 200/403/200" \
                "token freshness or presence behaves unexpectedly" \
                "ask: 'the CSRF replay result is not 200/403/200 on the vulnerable build; inspect the email-change handler'"
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
