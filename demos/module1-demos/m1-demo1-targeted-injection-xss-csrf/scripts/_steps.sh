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
source "${REPO_ROOT}/runtime/scripts/lib.sh"
FMT="${REPO_ROOT}/runtime/scripts/fmt.py"
fm() { python3 "${FMT}" "$@"; }

APP_INTERNAL="http://app:8000"        # how ZAP reaches the app (compose DNS)
ZAP="http://localhost:8090"           # ZAP API + proxy (same port)
PROXY="http://localhost:8090"
K="${ZAP_API_KEY:-}"   # lazy: the reference panel needs no key; ensure_ready checks it
POLICY="m1demo1"
POLICY_IDS="40018 40019 40020 40021 40022 40027 40033 90020 90037"
XSS_POLICY="m1xss"
XSS_IDS="40012"   # reflected XSS active rule (persistent-XSS rules are out of scope here)

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

build_policy_quiet() { # returns non-zero if ZAP rejects the policy or a rule
    zap ascan/action/removeScanPolicy "scanPolicyName=${POLICY}" >/dev/null 2>&1 || true
    zap ascan/action/addScanPolicy "scanPolicyName=${POLICY}" >/dev/null || return 1
    zap ascan/action/disableAllScanners "scanPolicyName=${POLICY}" >/dev/null || return 1
    local id
    for id in ${POLICY_IDS}; do
        zap ascan/action/enableScanners "ids=${id}&scanPolicyName=${POLICY}" >/dev/null || return 1
    done
}

enabled_rules() { # <policy> -> space-separated rule IDs ZAP reports as enabled
    zap ascan/view/scanners "scanPolicyName=$1" | python3 -c '
import json,sys
print(" ".join(sorted(s["id"] for s in json.load(sys.stdin)["scanners"] if s.get("enabled")=="true")))'
}

clear_alerts() { zap core/action/deleteAllAlerts >/dev/null; }

clear_alerts_for() { # <url> <pluginId> -- delete only that rule's old alerts on that URL
    local base id; base="$(enc "${1%%\?*}")"
    for id in $(zap core/view/alerts "baseurl=${base}" | python3 -c '
import json,sys
print(" ".join(a["id"] for a in json.load(sys.stdin)["alerts"] if a.get("pluginId")==sys.argv[1]))' "$2"); do
        zap core/action/deleteAlert "id=${id}" >/dev/null || return 1
    done
}

scan_url_quiet() { # <url>  -- active-scan one endpoint, wait, no output
    local url="$1" eu sid st waited=0
    eu="$(enc "${url}")"
    local try
    for try in 1 2 3 4 5; do
        zap core/action/accessUrl "url=${eu}&followRedirects=false" >/dev/null 2>&1 || true
        sid="$(zap ascan/action/scan "url=${eu}&recurse=false&scanPolicyName=${POLICY}" | jget scan 2>/dev/null)"
        [[ "${sid}" =~ ^[0-9]+$ ]] && break
        sleep 3   # the sites tree may not hold the URL yet on a fresh ZAP
    done
    [[ "${sid}" =~ ^[0-9]+$ ]] || return 1
    while :; do
        st="$(zap ascan/view/status "scanId=${sid}" | jget status 2>/dev/null)"
        [ "${st}" = "100" ] && return 0
        sleep 3; waited=$((waited+3)); [ "${waited}" -gt 300 ] && return 2   # timed out
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
    zap ascan/action/addScanPolicy "scanPolicyName=${XSS_POLICY}" >/dev/null || return 1
    zap ascan/action/disableAllScanners "scanPolicyName=${XSS_POLICY}" >/dev/null || return 1
    local id
    for id in ${XSS_IDS}; do
        zap ascan/action/enableScanners "ids=${id}&scanPolicyName=${XSS_POLICY}" >/dev/null || return 1
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
        [ "${st}" = "100" ] && return 0
        sleep 3; waited=$((waited+3)); [ "${waited}" -gt 180 ] && return 2   # timed out
    done
}

# ZAP's reflected-XSS alert on a URL -> "name|param|attack|evidence|risk|confidence" (empty if none).
xss_alert() { # <url>
    local base; base="$(enc "${1%%\?*}")"
    zap core/view/alerts "baseurl=${base}" | python3 -c '
import json,sys
for a in json.load(sys.stdin)["alerts"]:
    if a.get("pluginId")=="40012":
        print("|".join(a.get(k,"").replace("|","/").replace("\n"," ") for k in ("alert","param","attack","evidence","risk","confidence")))
        break
'
}

# ---- reference panel (not a step) -----------------------------------------
print_reference() {
    fm header "Before you test: map each case to its context / state" \
              "The context and the token state decide the test you run (EO1b, EO1c)."
    fm section "XSS execution contexts"
    fm item "HTML body, input lands between tags"
    fm item "HTML attribute, input lands inside a quoted attribute value"
    fm item "JavaScript string, input lands inside a quoted JS string"
    fm section "CSRF token states"
    fm item "valid for this session, the request should succeed"
    fm item "missing or invalid, the request should be rejected"
    fm item "replayed, a token that was already used once is sent again: the request should be rejected"
    fm item "cross-session, a token issued to another session is sent with this session's cookie: the request should be rejected"
}

# ===========================================================================
# STEP 1, Targeted injection scan (EO1a)  → "Targeted scan policy and rule list"
# ===========================================================================
step1_injection() {
    fm header "Targeted injection scan, one policy, three endpoints" \
              "Proves ZAP detects SQL, NoSQL, and command injection as real findings (EO1a)."
    clear_alerts || { fail "could not clear old alerts" "ZAP API refused deleteAllAlerts" "restart ZAP with ./scripts/demo_reset.sh"; return 1; }
    build_policy_quiet || { fail "ZAP rejected the scan policy" "a rule ID is not installed" "check ascanrulesBeta (40033) is installed"; return 1; }
    local rules; rules="$(enabled_rules "${POLICY}")"
    fm star "Policy ${POLICY} · rules ZAP reports enabled" "${rules:-<none>}"

    fm note "running the focused scan across the three endpoints..."
    local u rc scan_ok=1
    for u in "${APP_INTERNAL}/search?q=Router" "${APP_INTERNAL}/api/account?username=alice" "${APP_INTERNAL}/admin/ping?host=127.0.0.1"; do
        scan_url_quiet "${u}"; rc=$?
        if [ "${rc}" != 0 ]; then
            fm star "Scan ${u#${APP_INTERNAL}}" "$([ "${rc}" = 2 ] && echo 'TIMED OUT' || echo 'DID NOT START')"; scan_ok=0
        fi
    done

    fm section "Findings, alert raised per endpoint (this run only)"
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

    local need missing=""
    for need in 40018 40022 40033 90020 90037; do [[ " ${rules} " == *" ${need} "* ]] || missing="${missing} ${need}"; done
    if [ "${allok}" = 1 ] && [ "${scan_ok}" = 1 ] && [ -z "${missing}" ]; then
        pass "targeted scan raised all three injection alerts"
    else
        fail "one or more injection alerts did not fire (scans ok=${scan_ok}; missing rules:${missing:- none})" \
             "an endpoint, a scan or the scan policy changed" \
             "re-check the endpoint that raised no alert; fix the endpoint, not the check"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2, XSS request and response body (EO1b)
# ===========================================================================
step2_xss() {
    fm header "Reflected XSS, a context-matched payload, then ZAP confirms it" \
              "The output context decides the payload; ZAP's reflected-XSS rule 40012 then confirms the finding (EO1b)."
    clear_alerts_for "${APP_INTERNAL}/greet" 40012 || { fail "could not clear old XSS alerts" "ZAP API refused deleteAlert" "restart ZAP with ./scripts/demo_reset.sh"; return 1; }

    # Part A, Maya's context-matched cases. Each payload is sent through ZAP; the
    # exact request and the response line that reflects it are printed.
    local n=0 ctx payload needle body line
    fm section "Context-matched cases (request → response body line)"
    while IFS='|' read -r ctx payload needle; do
        body="$(curl -s -x "${PROXY}" -G --data-urlencode "name=${payload}" "${APP_INTERNAL}/greet")"
        # Show the reflection IN CONTEXT: a window centred on the injected payload, not the first N
        # characters of the page (that only showed the doctype/head). The payload is never cut off;
        # fmt.py wraps the window onto aligned lines, so nothing is truncated.
        line="$(printf '%s\n' "${body}" | grep -F -- "${needle}" | head -1 | sed 's/^[[:space:]]*//' \
                | needle="${needle}" awk '{n=ENVIRON["needle"]; i=index($0,n);
                    if (i==0) print $0;
                    else { s=(i>45?i-45:1); print substr($0, s, length(n)+90) } }')"
        fm star "${ctx} · request" "GET /greet?name=${payload}"
        if [ -n "${line}" ]; then
            fm star "${ctx} · response body" "${line}" focus; n=$((n+1))
        else
            fm star "${ctx} · response body" "payload NOT reflected unescaped"
        fi
    done <<'CASES'
HTML body|<script>alert(1)</script>|<p>Hello <script>alert(1)</script>
HTML attribute|"><svg onload=alert(1)>|value=""><svg onload=alert(1)>
JavaScript string|";alert(1);//|greeting = "";alert(1);//
CASES

    # Part B, ZAP actively scans 'name' with reflected-XSS rule 40012.
    build_xss_policy_quiet || { fail "ZAP rejected the XSS policy" "rule 40012 missing" "check the ZAP image"; return 1; }
    fm note "running ZAP's reflected-XSS rule 40012 against /greet (name)..."
    scan_xss_quiet "${APP_INTERNAL}/greet?name=zzMARKzz"; local rc=$?
    local rec name param attack evidence risk conf
    rec="$(xss_alert "${APP_INTERNAL}/greet")"
    IFS='|' read -r name param attack evidence risk conf <<<"${rec}"

    fm section "ZAP's confirmed finding (this run only)"
    fm star "Alert" "${name:-NO ALERT RAISED}${risk:+ · ${risk}/${conf}}" focus
    fm star "Affected parameter" "${param:-<none>}"
    fm star "Payload ZAP injected" "${attack:-<none>}" focus
    fm star "Evidence (reflected in the response)" "${evidence:-<none>}"

    if [ "${n}" = 3 ] && [ "${rc}" = 0 ] && [ "${param}" = "name" ] && [ -n "${attack}" ]; then
        pass "all three context-matched payloads reflected unescaped, and ZAP rule 40012 confirmed reflected XSS on 'name'"
    else
        fail "reflected XSS was not confirmed (contexts ${n}/3; scan rc=${rc}; ZAP param='${param:-}')" \
             "the vulnerable build should reflect each payload unescaped and ZAP should raise 40012 on name" \
             "check the /greet endpoint and that APP_BUILD=vulnerable"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3, CSRF token replay result (EO1c)
# ===========================================================================
step3_csrf() {
    fm header "CSRF, valid, missing, replayed and cross-session tokens" \
              "A CSRF token must be single-use and tied to its session. A used token is replayed, and a token from another session is tried; both should be rejected (EO1c)."
    local A=/tmp/.c_a B=/tmp/.c_b
    local legit="alice@globomantics.example" replayed="replayed@evil.example" attack="attacker@evil.example"
    local tokenA tokenB v m r x before_r after_r after_x
    rm -f "${A}" "${B}"

    _post() { # <cookiejar> <data> -> HTTP code
        curl -s -x "${PROXY}" -o /dev/null -w '%{http_code}' -b "$1" -X POST --data "$2" "${APP_INTERNAL}/account/email"
    }
    _email() { # <cookiejar> -> stored email for that session
        curl -s -x "${PROXY}" -b "$1" "${APP_INTERNAL}/account/email/current" \
            | python3 -c 'import json,sys;print(json.load(sys.stdin).get("email",""))' 2>/dev/null
    }

    curl -s -x "${PROXY}" -o /dev/null -c "${A}" -X POST --data 'username=mallory' "${APP_INTERNAL}/login" >/dev/null
    curl -s -x "${PROXY}" -o /dev/null -c "${B}" -X POST --data 'username=alice'   "${APP_INTERNAL}/login" >/dev/null
    tokenA="$(curl -s -x "${PROXY}" -b "${A}" "${APP_INTERNAL}/account/email" | grep -o '[a-f0-9]\{32\}' | head -1)"
    tokenB="$(curl -s -x "${PROXY}" -b "${B}" "${APP_INTERNAL}/account/email" | grep -o '[a-f0-9]\{32\}' | head -1)"

    v="$(_post "${B}" "email=${legit}&csrf_token=${tokenB}")"      # valid: B's own fresh token
    m="$(_post "${B}" "email=${attack}")"                          # missing token
    before_r="$(_email "${B}")"
    r="$(_post "${B}" "email=${replayed}&csrf_token=${tokenB}")"   # replay: the SAME, already-used token
    after_r="$(_email "${B}")"
    x="$(_post "${B}" "email=${attack}&csrf_token=${tokenA}")"     # cross-session: A's token, B's cookie
    after_x="$(_email "${B}")"

    fm star "valid token (session B's own, first use)" "${v}"
    fm star "missing token" "${m}"
    fm star "replayed used token (same token, second use)" "${r}  (should be rejected)" focus
    fm star "session B's email: before → after the replay" "${before_r} → ${after_r}" focus
    fm star "token from session A, submitted with session B's cookie" "${x}  (should be rejected)"
    fm star "session B's email after the cross-session request" "${after_x}"

    if [ "${v} ${m} ${r}" = "200 403 200" ] && [ "${before_r}" = "${legit}" ] && [ "${after_r}" = "${replayed}" ]; then
        if [ "${x}" = 200 ] && [ "${after_x}" = "${attack}" ]; then
            pass "the used token was accepted again (200) and changed the email; a token from another session was also accepted, tokens are neither single-use nor session-bound"
        else
            pass "the used token was accepted again (200) and changed the email, tokens are not single-use"
        fi
    else
        fail "CSRF result was valid=${v} missing=${m} replay=${r}, email ${before_r:-<empty>} -> ${after_r:-<empty>} (expected 200/403/200 and ${legit} -> ${replayed})" \
             "the vulnerable build should accept a replayed token and change state" \
             "check APP_BUILD=vulnerable and the /account/email handler"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4, Alert disposition record (TO1: EO1a + EO1b + EO1c)
# Reads the alerts ZAP raised in Steps 1-2, reconciles each with live behaviour,
# and writes the record to logs/alert-disposition.md.
# ===========================================================================
step4_disposition() {
    fm header "Alert disposition, reconcile each ZAP alert with app behavior" \
              "Turns ZAP alerts into recorded decisions you can defend (EO1a, EO1b, EO1c)."
    local sqlerr b i ping xss csrf rec_sql rec_nosql rec_cmd rec_xss record ok=1
    rec_sql="$(first_alert "${APP_INTERNAL}/search?q=Router" "40018 40022")"
    rec_nosql="$(first_alert "${APP_INTERNAL}/api/account?username=alice" "40033")"
    rec_cmd="$(first_alert "${APP_INTERNAL}/admin/ping?host=127.0.0.1" "90020 90037")"
    rec_xss="$(first_alert "${APP_INTERNAL}/greet" "40012")"

    sqlerr="$(curl -s -x "${PROXY}" "${APP_INTERNAL}/search?q=Router%27" | grep -o 'unterminated[^<]*' | head -1 \
              | python3 -c 'import html,sys;print(html.unescape(sys.stdin.read().strip()))')"
    b="$(curl -s -x "${PROXY}" "${APP_INTERNAL}/api/account?username=alice"     | python3 -c 'import json,sys;print(json.load(sys.stdin).get("count",""))' 2>/dev/null)"
    i="$(curl -s -x "${PROXY}" "${APP_INTERNAL}/api/account?username%5B%24ne%5D=" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("count",""))' 2>/dev/null)"
    ping="$(curl -s -x "${PROXY}" -G --data-urlencode 'host=127.0.0.1; printf ZAP_CMD_PROOF' "${APP_INTERNAL}/admin/ping" | grep -o 'ZAP_CMD_PROOF' | head -1)"
    if curl -s -x "${PROXY}" -G --data-urlencode 'name=<script>alert(1)</script>' "${APP_INTERNAL}/greet" | grep -qF '<p>Hello <script>alert(1)</script>'; then xss="payload reflected unescaped"; fi
    # CSRF has no ZAP alert in this policy; its row is backed by a fresh replay check.
    local C=/tmp/.c_d t c1 c2
    curl -s -x "${PROXY}" -o /dev/null -c "${C}" -X POST --data 'username=alice' "${APP_INTERNAL}/login" >/dev/null
    t="$(curl -s -x "${PROXY}" -b "${C}" "${APP_INTERNAL}/account/email" | grep -o '[a-f0-9]\{32\}' | head -1)"
    c1="$(curl -s -x "${PROXY}" -o /dev/null -w '%{http_code}' -b "${C}" -X POST --data "email=alice@globomantics.example&csrf_token=${t}" "${APP_INTERNAL}/account/email")"
    c2="$(curl -s -x "${PROXY}" -o /dev/null -w '%{http_code}' -b "${C}" -X POST --data "email=replayed@evil.example&csrf_token=${t}" "${APP_INTERNAL}/account/email")"
    [ "${c1} ${c2}" = "200 200" ] && csrf="used token accepted twice (${c1}, ${c2})"

    _disp() { # <zap record or "-"> <evidence or empty> -> "True Positive" | "Not confirmed"
        if [ -n "$1" ] && [ -n "$2" ]; then echo "True Positive"; else echo "Not confirmed"; ok=0; fi
    }
    local d_sql d_nosql d_cmd d_xss d_csrf
    [[ "${b}" =~ ^[0-9]+$ && "${i}" =~ ^[0-9]+$ && "${i}" -gt "${b}" ]] && nosql="accounts ${b} → ${i}" || nosql=""
    d_sql="$(_disp "${rec_sql}" "${sqlerr}")";  d_nosql="$(_disp "${rec_nosql}" "${nosql}")"
    d_cmd="$(_disp "${rec_cmd}" "${ping}")";    d_xss="$(_disp "${rec_xss}" "${xss}")"
    d_csrf="$(_disp "-" "${csrf}")"

    fm star "${rec_sql%%|*} SQL injection · /search (q)" "${d_sql}, DB error: ${sqlerr:-none}" focus
    fm star "${rec_nosql%%|*} NoSQL injection · /api/account (username)" "${d_nosql}, ${nosql:-no count change}" focus
    fm star "${rec_cmd%%|*} Command injection · /admin/ping (host)" "${d_cmd}, injected shell marker: ${ping:-none}" focus
    fm star "${rec_xss%%|*} Reflected XSS · /greet (name)" "${d_xss}, ${xss:-not reflected}" focus
    fm star "CSRF · /account/email (csrf_token)" "${d_csrf}, ${csrf:-replay rejected}" focus

    record="${HERE_STEPS}/../logs/alert-disposition.md"
    mkdir -p "$(dirname "${record}")"
    {
        echo "# Alert disposition record, m1-demo1 ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
        echo
        echo "| Alert ID | Rule | Endpoint | Disposition | Evidence |"
        echo "|---|---|---|---|---|"
        echo "| ${rec_sql%%|*} | SQL Injection | GET /search?q= | ${d_sql} | ${sqlerr:-no DB error} |"
        echo "| ${rec_nosql%%|*} | NoSQL Injection - MongoDB | GET /api/account?username= | ${d_nosql} | ${nosql:-no count change} |"
        echo "| ${rec_cmd%%|*} | Remote OS Command Injection | GET /admin/ping?host= | ${d_cmd} | shell marker: ${ping:-none} |"
        echo "| ${rec_xss%%|*} | Cross Site Scripting (Reflected) | GET /greet?name= | ${d_xss} | ${xss:-not reflected} |"
        echo "|, | CSRF token replay | POST /account/email | ${d_csrf} | ${csrf:-replay rejected} |"
    } > "${record}"
    fm star "Disposition record written" "logs/alert-disposition.md"

    if [ "${ok}" = 1 ]; then
        pass "every ZAP alert and the CSRF case reconciled with observed behavior and recorded"
    else
        fail "a finding could not be reconciled (missing ZAP alert or behaviour evidence)" \
             "run Steps 1 and 2 first in this ZAP session, on the vulnerable build" \
             "re-run Steps 1-2, then Step 4"
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
