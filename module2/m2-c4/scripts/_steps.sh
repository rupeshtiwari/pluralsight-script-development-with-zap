#!/bin/bash
# Shared step library for m2-c4 "Query the ZAP API and inspect scan evidence".
#
# Sourced by preflight_check.sh and demo_step.sh. Each step drives ZAP ONLY
# through its HTTP API (localhost:8090) — the point of this lab: inspecting a
# finished scan's evidence programmatically, not from the GUI (EO3b).
#   1. ZAP API status response     2. ZAP API alert response
#   3. ZAP JSON report             4. ZAP Insights evidence
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
PROFILE="${APP_INTERNAL}/account/profile"
ZAP="http://localhost:8090"
K="${ZAP_API_KEY:-}"
# The authenticated plan from the previous lab generates the evidence this lab
# inspects; we reuse the same plan mounted into the ZAP container at /af.
AF_PLAN_ZAP="/af/af-plan.yaml"
XSS_NAME="Cross Site Scripting (Reflected)"

PASS=0; FAIL=0; STEP_RC=0
pass() { fm ok "$1"; PASS=$((PASS+1)); STEP_RC=0; }
fail() { fm fail "$1" "${2:-}" "${3:-}"; FAIL=$((FAIL+1)); STEP_RC=1; }
enc()  { python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=""))' "$1"; }
jq_py() { python3 -c "$1"; }

zap() { # <path> <query> -> body (asserts HTTP 200)
    local path="$1" query="${2:-}" code
    code="$(curl -s -o /tmp/.m2d2body -w '%{http_code}' "${ZAP}/JSON/${path}/?apikey=${K}&${query}")"
    [ "${code}" = "200" ] || { echo "  (ZAP API ${path} -> HTTP ${code})" >&2; return 1; }
    cat /tmp/.m2d2body
}

zap_container() { docker ps --format '{{.Names}}' 2>/dev/null | grep -E 'zap' | head -1; }

# --- priming: make sure a finished scan exists to inspect --------------------
run_plan() { PLAN_ID="$(zap automation/action/runPlan "filePath=$(enc "${AF_PLAN_ZAP}")" | jq_py 'import json,sys
try: print(json.load(sys.stdin).get("planId",""))
except Exception: print("")')"; [ -n "${PLAN_ID:-}" ]; }
plan_finished() { zap automation/view/planProgress "planId=${PLAN_ID}" | grep -q '"finished"[^,]*[0-9T:-]'; }

reflection_present() {
    zap core/view/alerts "baseurl=$(enc "${PROFILE}")" | jq_py 'import json,sys
try: d=json.load(sys.stdin)
except Exception: raise SystemExit
for a in d.get("alerts",[]):
    if "Cross Site Scripting (Reflected)" in (a.get("alert") or a.get("name") or ""):
        print("yes"); break'
}

ensure_scan() { # prime once if there is no evidence yet in this ZAP session
    [ -n "$(reflection_present)" ] && return 0
    fm note "Priming: this ZAP session has no finished scan yet — running the authenticated plan once so there is evidence to inspect."
    run_plan || { fail "could not start the plan to generate evidence" "automation/action/runPlan returned no plan id" "ask: 'the AF plan did not run; check the automation add-on and /af/af-plan.yaml'"; return 1; }
    local i; for i in $(seq 1 120); do plan_finished && break; sleep 3; done
    [ -n "$(reflection_present)" ]
}

ensure_ready() {
    [ -n "${K}" ] || { fail "ZAP_API_KEY is not set" "the .env file is missing or not loaded" "run from the repo so .env loads"; return 1; }
    zap core/view/version | grep -q '"version"' || {
        fail "ZAP API not reachable" "the stack may still be starting" "run scripts/demo_up.sh, wait for 'Up', then retry"; return 1; }
    ensure_scan || return 1
    return 0
}

# Cache the generated report path so steps 3 and 4 read the same file.
REPORT_CONTAINER_PATH="/tmp/globo-api-report.json"
generate_report() { # -> writes the report inside the ZAP container, echoes host-read JSON
    local cid; cid="$(zap_container)"
    [ -n "${cid}" ] || return 1
    zap reports/action/generate \
        "title=$(enc 'Globomantics API evidence')&template=traditional-json&reportDir=/tmp&reportFileName=globo-api-report.json&display=false" \
        >/dev/null 2>&1 || true
    docker exec "${cid}" cat "${REPORT_CONTAINER_PATH}" 2>/dev/null
}

# ===========================================================================
# STEP 1 — ZAP API status response (EO3b)  -> "ZAP API status response"
# ===========================================================================
step1_api_status() {
    fm header "The ZAP API answers: what engine, and is the scan done?" \
              "You drive ZAP over HTTP, not the GUI — ask the running engine its version and whether the authenticated scan has finished (EO3b)."
    local ver; ver="$(zap core/view/version | jq_py 'import json,sys
try: print(json.load(sys.stdin).get("version",""))
except Exception: print("")')"
    local scan; scan="$(zap ascan/view/scans | jq_py 'import json,sys
try: s=json.load(sys.stdin).get("scans",[])
except Exception: s=[]
if not s: print("||"); raise SystemExit
a=s[-1]
print("%s|%s|%s|%s" % (a.get("id",""), a.get("progress",""), a.get("state",""), a.get("reqCount","")))')"
    IFS='|' read -r sid sprog sstate sreq <<<"${scan}"
    fm star "ZAP runtime  (GET core/view/version)" "${ver:-unknown}" focus
    fm star "Active scan  (GET ascan/view/scans)" "id=${sid:-?} · progress=${sprog:-?}% · state=${sstate:-?}"
    fm star "Requests the scan sent" "${sreq:-?}"
    if [ -n "${ver}" ] && [ "${sprog}" = "100" ]; then
        pass "the API reports the ZAP runtime and a finished scan"
    else
        fail "the API did not report a finished scan" \
             "version or scan status was missing (version='${ver}', progress='${sprog}')" \
             "ask: 'ZAP API status is incomplete; confirm the scan ran and ascan/view/scans returns progress 100'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2 — ZAP API alert response (EO3b)  -> "ZAP API alert response"
# ===========================================================================
step2_api_alert() {
    fm header "The ZAP API answers: what did the scan find, and how is it rated?" \
              "Ask the API for the alert the authenticated scan generated — its rule identity and its disposition (risk + confidence) — the data a pipeline reads to decide (EO3b)."
    local rec; rec="$(zap core/view/alerts "baseurl=$(enc "${PROFILE}")" | jq_py 'import json,sys
try: d=json.load(sys.stdin)
except Exception: print("||||"); raise SystemExit
for a in d.get("alerts",[]):
    if "Cross Site Scripting (Reflected)" in (a.get("alert") or a.get("name") or ""):
        print("%s|%s|%s|%s|%s" % (a.get("pluginId",""), a.get("alert") or a.get("name"), a.get("risk",""), a.get("confidence",""), a.get("param","")))
        break
else:
    print("||||")')"
    IFS='|' read -r pid name risk conf param <<<"${rec}"
    if [ -n "${name}" ]; then
        fm star "Rule identity  (pluginId · alert)" "${pid} · ${name}" focus
        fm star "Disposition  (risk · confidence)" "${risk} · ${conf}"
        fm star "Parameter" "${param}"
        pass "the API returns the finding's rule identity and disposition"
    else
        fail "the API returned no alert for the authenticated page" \
             "core/view/alerts had no reflected-XSS entry on /account/profile" \
             "ask: 'the ZAP API alert response is empty; confirm the authenticated scan reached /account/profile'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3 — ZAP JSON report (EO3b)  -> "ZAP JSON report"
# ===========================================================================
step3_json_report() {
    fm header "The official JSON report reconciles with the API" \
              "Generate ZAP's own JSON report through the API and confirm its alert data matches the API response — one source of truth a pipeline can archive (EO3b)."
    local rep; rep="$(generate_report)"
    if [ -z "${rep}" ]; then
        fail "could not read the generated JSON report" \
             "reports/action/generate or reading /tmp/globo-api-report.json failed" \
             "ask: 'the JSON report was not produced; confirm the reports add-on and docker access to the ZAP container'"
        return "${STEP_RC}"
    fi
    local line; line="$(printf '%s' "${rep}" | jq_py 'import json,sys
try: d=json.load(sys.stdin)
except Exception: print("|||"); raise SystemExit
for site in d.get("site",[]):
    for a in site.get("alerts",[]):
        if "Cross Site Scripting (Reflected)" in (a.get("alert") or a.get("name") or ""):
            inst=(a.get("instances") or [{}])[0]
            print("%s|%s|%s|%s" % (a.get("pluginid",""), a.get("alert") or a.get("name"), a.get("riskdesc",""), inst.get("param","")))
            raise SystemExit
print("|||")')"
    IFS='|' read -r pid name riskdesc param <<<"${line}"
    if [ -n "${name}" ]; then
        fm star "Report template" "traditional-json  (reports/action/generate)" focus
        fm star "Report alert  (pluginid · name)" "${pid} · ${name}"
        fm star "Report rating  (riskdesc)" "${riskdesc}"
        fm star "Reconciled with the API" "same rule id and risk as the Step 2 alert response"
        pass "the official JSON report carries the same finding as the API"
    else
        fail "the JSON report did not contain the expected finding" \
             "no reflected-XSS alert in the report's site[].alerts[]" \
             "ask: 'the JSON report is missing the authenticated finding; confirm the scan and the report template'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4 — ZAP Insights evidence (EO3b)  -> "ZAP Insights evidence"
# ===========================================================================
step4_insights() {
    fm header "ZAP 2.17.0 Insights assess scan effectiveness, not just findings" \
              "Read the report's Insights — signals about how well the scan ran and any operational issues — so you trust the result, not just the alert list (EO3b)."
    local rep; rep="$(generate_report)"
    local shown=0
    if [ -n "${rep}" ]; then
        local ins; ins="$(printf '%s' "${rep}" | jq_py 'import json,sys
try: d=json.load(sys.stdin)
except Exception: raise SystemExit
items=d.get("insights") or []
for it in items[:3]:
    print("%s\t%s\t%s\t%s" % (it.get("level",""), it.get("key",""), it.get("statistic",""), (it.get("description") or it.get("reason") or "")))')"
        if [ -n "${ins}" ]; then
            shown=1
            local first=1
            while IFS=$'\t' read -r lvl key stat desc; do
                [ -z "${lvl}${key}${stat}${desc}" ] && continue
                if [ "${first}" = 1 ]; then
                    fm star "Insight  (level · key)" "${lvl} · ${key}" focus; first=0
                else
                    fm star "Insight  (level · key)" "${lvl} · ${key}"
                fi
                fm star "Statistic · meaning" "${stat} · ${desc}"
            done <<<"${ins}"
            pass "the report's Insights section reports scan effectiveness"
        fi
    fi
    if [ "${shown}" = 0 ]; then
        # Fallback: the Insights add-on draws from ZAP statistics; show them directly.
        local stats; stats="$(zap stats/view/allSitesStats "keyPrefix=" | jq_py 'import json,sys
try: d=json.load(sys.stdin)
except Exception: raise SystemExit
s=d.get("statistics") or d.get("allSitesStats") or []
def pick(items):
    out=[]
    for it in items:
        if isinstance(it,dict):
            for k,v in it.items(): out.append((k,v))
    return out
rows=pick(s) if isinstance(s,list) else list(s.items()) if isinstance(s,dict) else []
for k,v in rows[:4]:
    print("%s\t%s" % (k,v))')"
        if [ -n "${stats}" ]; then
            fm star "Source" "stats/view/allSitesStats  (Insights draw from these)" focus
            while IFS=$'\t' read -r k v; do
                [ -z "${k}" ] && continue
                fm star "${k}" "${v}"
            done <<<"${stats}"
            pass "ZAP statistics (the basis of Insights) report scan effectiveness"
        else
            fail "no Insights or statistics were returned" \
                 "the report had no insights section and stats/view/allSitesStats was empty" \
                 "ask: 'ZAP Insights evidence is unavailable; confirm the insights add-on is installed in ZAP 2.17.0 and a scan has run'"
        fi
    fi
    return "${STEP_RC}"
}
