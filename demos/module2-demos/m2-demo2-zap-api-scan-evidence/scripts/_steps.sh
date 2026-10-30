#!/bin/bash
# Shared step library for m2-c4 "Query the ZAP API and inspect scan evidence".
#
# Sourced by preflight_check.sh and demo_step.sh. Each step drives ZAP ONLY
# through its HTTP API (localhost:8090), the point of this lab: inspecting a
# finished scan's evidence programmatically, not from the GUI (EO3b).
#   1. ZAP API status response     2. ZAP API alert response
#   3. ZAP JSON report             4. ZAP Insights evidence
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
PROFILE="${APP_INTERNAL}/account/profile"
ZAP="http://localhost:8090"
K="${ZAP_API_KEY:-}"
# The authenticated plan from the previous lab generates the evidence this lab
# inspects; we reuse the same plan mounted into the ZAP container at /af.
AF_PLAN_ZAP="/af/af-plan.yaml"
# The script-generated alert this lab inspects (the Module 1 custom Python rule).
# The outline's "script-generated alert" is this named alert, NOT a built-in rule.
CUSTOM_NAME="Globomantics unsafe reflection (custom rule)"

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

# Select the ZAP SERVICE container specifically. The compose project name
# contains "zap", so a plain `grep zap` matches every service (app, mongo,
# postgres, zap) and can return the wrong container, which made the report
# read happen in the app container's /tmp. `docker compose ps -q zap` resolves
# the zap service only (same approach as m2-c3).
zap_container() { ( cd "${REPO_ROOT}" && docker compose ps -q zap 2>/dev/null ) | head -1; }

# --- priming: make sure a finished scan exists to inspect --------------------
# The AF env re-registers the context auth script by its file name every run;
# ZAP rejects the duplicate, aborting context creation on a re-run against the
# long-lived local ZAP. Remove the demo scripts first and ensure the report dir
# exists so the plan runs cleanly. (CI uses a fresh ZAP, so the plan is unchanged.)
reset_plan_state() {
    local c; c="$(zap_container)"
    [ -n "${c}" ] && docker exec "${c}" sh -c 'mkdir -p /zap/wrk && chmod 0777 /zap/wrk' >/dev/null 2>&1 || true
    local s
    for s in "globomantics-auth.py" "globomantics-auth" "globomantics-active-rule" "globomantics-marker"; do
        zap script/action/remove "scriptName=$(enc "${s}")" >/dev/null 2>&1 || true
    done
}
run_plan() { reset_plan_state; PLAN_ID="$(zap automation/action/runPlan "filePath=$(enc "${AF_PLAN_ZAP}")" | jq_py 'import json,sys
try: print(json.load(sys.stdin).get("planId",""))
except Exception: print("")')"; [ -n "${PLAN_ID:-}" ]; }
plan_finished() { zap automation/view/planProgress "planId=${PLAN_ID}" | grep -q '"finished"[^,]*[0-9T:-]'; }
SCAN_ID=""
scan_finished() { # Read THIS plan's scan; old completed scans cannot satisfy the wait.
    [ -n "${SCAN_ID}" ] || return 1
    local record
    record="$(zap ascan/view/scans | python3 "${REPO_ROOT}/runtime/scripts/zap_scan.py" record "${SCAN_ID}")" || return 1
    local id progress state requests
    IFS='|' read -r id progress state requests <<<"${record}"
    [ "${progress}" = "100" ] && [ "${state}" = "FINISHED" ] || return 1
    printf yes
}

custom_present() {
    zap core/view/alerts "baseurl=$(enc "${PROFILE}")" | python3 -c 'import json,sys
name=sys.argv[1]
try: d=json.load(sys.stdin)
except Exception: raise SystemExit
for a in d.get("alerts",[]):
    if (a.get("alert") or a.get("name"))==name:
        print("yes"); break' "${CUSTOM_NAME}"
}

STATE="${DEMO_DIR}/logs/.m2demo2-state"   # Step 1 plan + Step 2 API values, read by Steps 3-4
mkdir -p "${DEMO_DIR}/logs"

ensure_scan() { # Steps 2-4: the authenticated run from Step 1 must exist in this ZAP session
    SCAN_ID="$(sed -n 's/^scan=//p' "${STATE}" 2>/dev/null)"
    { [ -n "$(custom_present)" ] && [ -n "$(scan_finished)" ]; } && return 0
    fail "no finished authenticated scan in this ZAP session" "Step 1 runs the authenticated plan" "run Step 1 first"
    return 1
}

run_authenticated_plan() { # Step 1: fresh alerts, run the authenticated plan, wait for the scan
    # A failed new run must not leave an earlier scan identity usable.
    rm -f "${STATE}" || { fail "could not invalidate the previous scan state" "the state file is not writable" "check logs/.m2demo2-state permissions"; return 1; }
    local previous
    previous="$(zap ascan/view/scans | python3 "${REPO_ROOT}/runtime/scripts/zap_scan.py" ids)" || {
        fail "could not read active scans before starting the plan" "scan identity could not be established" "check the ZAP API"; return 1;
    }
    zap core/action/deleteAllAlerts >/dev/null || {
        fail "could not clear old alert evidence" "the ZAP API rejected deleteAllAlerts" "check the ZAP API"; return 1;
    }
    run_plan || { fail "could not start the plan to generate evidence" "automation/action/runPlan returned no plan id" "ask: 'the AF plan did not run; check the automation add-on and /af/af-plan.yaml'"; return 1; }
    local i; for i in $(seq 1 160); do plan_finished && break; sleep 3; done
    plan_finished || { fail "the authenticated plan did not finish in time" "planProgress never reported finished" "check the ZAP container log"; return 1; }
    SCAN_ID="$(zap ascan/view/scans | python3 "${REPO_ROOT}/runtime/scripts/zap_scan.py" new "${previous}")" || {
        fail "could not identify the active scan created by this plan" "expected exactly one new scan ID" "check planProgress and ascan/view/scans; do not reuse an earlier scan"; return 1;
    }
    # Bounded wait for the active scan to fully complete so Step 1 observes
    # progress=100 and the JSON report in Steps 3-4 is generated from a finished
    # scan. If it never reaches 100% within the timeout, fail with a nonzero exit.
    local k; for k in $(seq 1 80); do [ -n "$(scan_finished)" ] && break; sleep 3; done
    if [ -z "$(scan_finished)" ]; then
        fail "the authenticated scan did not complete" \
             "ascan/view/scans never reported progress=100 within the timeout" \
             "ask: 'the AF plan scan did not finish; check ZAP and the plan maxScanDurationInMins'"
        return 1
    fi
    # The scan can finish a moment before its alerts are queryable, so wait for
    # the script-generated alert rather than checking once. The named custom
    # alert is REQUIRED, a missing alert fails with a nonzero exit.
    local j; for j in $(seq 1 36); do [ -n "$(custom_present)" ] && return 0; sleep 5; done
    fail "the script-generated custom alert did not appear after the scan" \
         "core/view/alerts has no '${CUSTOM_NAME}' on ${PROFILE} after a completed scan" \
         "ask: 'the authenticated scan finished but did not raise the custom rule alert; check the custom rule and the context user'"
    return 1
}

ensure_ready() {
    [ -n "${K}" ] || { fail "ZAP_API_KEY is not set" "the .env file is missing or not loaded" "run from the repo so .env loads"; return 1; }
    zap core/view/version | grep -q '"version"' || {
        fail "ZAP API not reachable" "the stack may still be starting" "run scripts/lab-up.sh, wait for 'Up', then retry"; return 1; }
    return 0
}

# The report path that steps 3 and 4 display and save for inspection.
# new_report_path() MUST be called by the step DIRECTLY (never inside a
# rep="$(...)" capture). The report JSON is read through command substitution,
# which runs in a SUBSHELL, so any variable generate_report sets in there is
# discarded the moment the subshell exits. That lost subshell assignment is
# exactly why the "Report file" line used to print blank. Setting the paths in
# the step's own shell keeps them visible to the fm star line and the host save.
REPORT_CONTAINER_PATH=""
REPORT_HOST_PATH=""
new_report_path() { # set a fresh container + host report path in THIS shell
    local name; name="globo-api-report-$(date +%s)-${RANDOM}.json"
    REPORT_CONTAINER_PATH="/tmp/${name}"
    REPORT_HOST_PATH="${DEMO_DIR}/logs/${name}"
}
generate_report() { # generate the report at REPORT_CONTAINER_PATH; echoes its JSON
    local cid; cid="$(zap_container)"
    [ -n "${cid}" ] || return 1
    [ -n "${REPORT_CONTAINER_PATH}" ] || return 1
    zap reports/action/generate \
        "title=$(enc 'Globomantics API evidence')&template=traditional-json&reportDir=/tmp&reportFileName=$(basename "${REPORT_CONTAINER_PATH}")&display=false" \
        >/dev/null || return 1
    docker exec "${cid}" cat "${REPORT_CONTAINER_PATH}" 2>/dev/null
}
# Save the captured report JSON to the host so the learner can open the real
# file (logs/*.json is gitignored, so this is a local runtime artifact only).
save_report_host_copy() { # <json-body> -> writes REPORT_HOST_PATH (best effort)
    [ -n "${REPORT_HOST_PATH}" ] || return 0
    printf '%s' "$1" > "${REPORT_HOST_PATH}" 2>/dev/null || true
}

# ===========================================================================
# STEP 1, ZAP API status response (EO3b)  -> "ZAP API status response"
# ===========================================================================
step1_api_status() {
    fm header "The ZAP API answers: what engine, and is the authenticated scan done?" \
              "You drive ZAP over HTTP, not the GUI, start the authenticated plan, then ask the engine its version and whether the scan has finished (EO3b)."
    fm note "running the authenticated Automation Framework plan through the API (fresh alert store)..."
    run_authenticated_plan || return 1
    local ver prog user errs
    ver="$(zap core/view/version | jq_py 'import json,sys
try: print(json.load(sys.stdin).get("version",""))
except Exception: print("")')"
    prog="$(zap automation/view/planProgress "planId=${PLAN_ID}")"
    errs="$(printf '%s' "${prog}" | python3 -c 'import json,sys
try: print(len(json.load(sys.stdin).get("error",[])))
except Exception: print("?")')"
    user="$(zap users/view/usersList "contextId=$(zap context/view/context "contextName=Globomantics" | python3 -c 'import json,sys;print(json.load(sys.stdin)["context"]["id"])' 2>/dev/null)" 2>/dev/null | python3 -c 'import json,sys
try: print(" ".join(u["name"] for u in json.load(sys.stdin)["usersList"]))
except Exception: print("")')"
    local scan; scan="$(zap ascan/view/scans | python3 "${REPO_ROOT}/runtime/scripts/zap_scan.py" record "${SCAN_ID}")" || return 1
    IFS='|' read -r sid sprog sstate sreq <<<"${scan}"
    fm star "ZAP runtime  (GET core/view/version)" "${ver:-unknown}" focus
    fm star "Authenticated plan  (automation/view/planProgress)" "plan ${PLAN_ID} · finished · ${errs} errors · scanning as ${user:-?}"
    fm star "Active scan  (GET ascan/view/scans)" "id=${sid:-?} · progress=${sprog:-?}% · state=${sstate:-?}" focus
    fm star "Requests the scan sent" "${sreq:-?}"
    if [ -n "${ver}" ] && [ "${sprog}" = "100" ] && [ "${sstate}" = "FINISHED" ] && [ "${errs}" = "0" ] && [[ " ${user} " == *" alice "* ]]; then
        printf 'plan=%s\nscan=%s\n' "${PLAN_ID}" "${sid}" > "${STATE}" || {
            fail "could not save the validated scan identity" "the state file is not writable" "check logs/.m2demo2-state permissions"; return 1;
        }
        pass "the API reports the ZAP runtime and a finished authenticated scan"
    else
        fail "the API did not report a finished authenticated scan (version='${ver}', progress='${sprog}', plan errors=${errs}, user='${user}')" \
             "the authenticated plan failed or the scan did not finish" \
             "check ci/af-plan.yaml (mounted at /af) and the ZAP container log"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2, ZAP API alert response (EO3b)  -> "ZAP API alert response"
# ===========================================================================
step2_api_alert() {
    fm header "The ZAP API answers: what did your script find, and how is it rated?" \
              "Ask the API for the script-generated custom alert, its rule identity and its disposition (risk + confidence), the data a pipeline reads to decide (EO3b)."
    ensure_scan || return "${STEP_RC}"
    local rec; rec="$(zap core/view/alerts "baseurl=$(enc "${PROFILE}")" | python3 -c 'import json,sys
name=sys.argv[1]
for a in json.load(sys.stdin).get("alerts",[]):
    if (a.get("alert") or a.get("name"))==name:
        print("|".join(str(a.get(k,"")) for k in ("pluginId","alertRef","alert","risk","confidence","param","id"))); break' "${CUSTOM_NAME}")"
    IFS='|' read -r pid aref name risk conf param aid <<<"${rec}"
    if [ -n "${name}" ]; then
        fm star "Rule identity  (pluginId · alertRef)" "${pid} · ${aref}" focus
        fm star "Alert" "${name}  (alert id ${aid})"
        fm star "Disposition  (risk · confidence)" "${risk} · ${conf}" focus
        fm star "Parameter" "${param}"
        printf 'pid=%s\nrisk=%s\nconf=%s\nparam=%s\n' "${pid}" "${risk}" "${conf}" "${param}" >> "${STATE}"
        pass "the API returns the script-generated alert's rule identity and disposition"
    else
        fail "the API returned no script-generated custom alert for the authenticated page" \
             "core/view/alerts had no '${CUSTOM_NAME}' entry on /account/profile" \
             "run Step 1 again; confirm the Module 1 Python rule ran as alice"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3, ZAP JSON report (EO3b)  -> "ZAP JSON report"
# ===========================================================================
step3_json_report() {
    fm header "The official JSON report reconciles with the API" \
              "Generate ZAP's own JSON report through the API and compare its alert field by field with the Step 2 API response (EO3b)."
    ensure_scan || return "${STEP_RC}"
    new_report_path                 # set the paths in THIS shell, before the subshell capture below
    local rep; rep="$(generate_report)"
    if [ -z "${rep}" ]; then
        fail "could not generate or read the JSON report" "reports/action/generate failed" "check the reports add-on and docker access to the ZAP container"
        return "${STEP_RC}"
    fi
    save_report_host_copy "${rep}"  # write the real report to logs/ so it can be opened
    local line; line="$(printf '%s' "${rep}" | python3 -c 'import json,sys
name=sys.argv[1]
d=json.load(sys.stdin)
for site in d.get("site",[]):
    for a in site.get("alerts",[]):
        if (a.get("alert") or a.get("name"))==name:
            inst=(a.get("instances") or [{}])[0]
            print("|".join([a.get("pluginid",""), a.get("riskdesc",""), inst.get("param","")])); raise SystemExit' "${CUSTOM_NAME}")"
    IFS='|' read -r rpid riskdesc rparam <<<"${line}"
    local arec apid arisk aconf aparam
    arec="$(zap core/view/alerts "baseurl=$(enc "${PROFILE}")" | python3 -c '
import json,sys
name=sys.argv[1]
for a in json.load(sys.stdin).get("alerts",[]):
    if (a.get("alert") or a.get("name"))==name:
        print("|".join(str(a.get(k,"")) for k in ("pluginId","risk","confidence","param"))); break' "${CUSTOM_NAME}")"
    IFS='|' read -r apid arisk aconf aparam <<<"${arec}"
    fm star "Report file  (in ZAP container)" "${REPORT_CONTAINER_PATH}"
    fm star "Saved for inspection (on your Mac)" "${REPORT_HOST_PATH}" focus
    fm star "Report  pluginid · riskdesc · param" "${rpid:-?} · ${riskdesc:-?} · ${rparam:-?}" focus
    fm star "API (Step 2)  pluginId · risk (confidence) · param" "${apid:-?} · ${arisk:-?} (${aconf:-?}) · ${aparam:-?}" focus
    local m=0
    [ -n "${rpid}" ] && [ "${rpid}" = "${apid}" ] && m=$((m+1))
    [ -n "${riskdesc}" ] && [ "${riskdesc}" = "${arisk} (${aconf})" ] && m=$((m+1))
    [ -n "${rparam}" ] && [ "${rparam}" = "${aparam}" ] && m=$((m+1))
    fm star "Fields that match" "${m} of 3"
    if [ "${m}" = 3 ]; then
        pass "the official JSON report matches the API alert on rule ID, risk/confidence and parameter"
    else
        fail "the JSON report and the API disagree (${m}/3 fields match)" \
             "run Step 2 first in this session, or the report was generated from different scan data" \
             "re-run Steps 1-3; investigate any mismatch, never assume freshness"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4, ZAP Insights evidence (EO3b)  -> "ZAP Insights evidence"
# ===========================================================================
step4_insights() {
    fm header "ZAP 2.17.0 Insights assess scan effectiveness, not just findings" \
              "Read the report's Insights, signals about how well the scan ran and any operational issues, so you trust the result, not just the alert list (EO3b)."
    ensure_scan || return "${STEP_RC}"
    new_report_path                 # set the paths in THIS shell, before the subshell capture below
    local rep; rep="$(generate_report)"
    if [ -z "${rep}" ]; then
        fail "could not generate or read the JSON report for Insights" "reports/action/generate failed" "check the reports add-on"
        return "${STEP_RC}"
    fi
    save_report_host_copy "${rep}"  # write the real report to logs/ so it can be opened
    local ins; ins="$(printf '%s' "${rep}" | jq_py 'import json,sys
d=json.load(sys.stdin)
for it in (d.get("insights") or [])[:3]:
    print("%s\t%s\t%s\t%s" % (it.get("level",""), it.get("key",""), it.get("statistic",""), (it.get("description") or it.get("reason") or "")))')"
    if [ -z "${ins}" ]; then
        fm star "Top-level report keys" "$(printf '%s' "${rep}" | python3 -c 'import json,sys;print(" ".join(sorted(json.load(sys.stdin).keys())))')"
        fail "the report contained no ZAP Insights entries" \
             "ZAP 2.17.0 Insights are required here; generic statistics do not substitute" \
             "confirm the report keys above contain insights before recording"
        return "${STEP_RC}"
    fi
    local first=1
    while IFS=$'\t' read -r lvl key stat desc; do
        [ -z "${lvl}${key}${stat}${desc}" ] && continue
        if [ "${first}" = 1 ]; then fm star "Insight  (level · key)" "${lvl} · ${key}" focus; first=0
        else fm star "Insight  (level · key)" "${lvl} · ${key}"; fi
        fm star "Statistic · meaning" "${stat} · ${desc}"
    done <<<"${ins}"
    fm star "Report file  (in ZAP container)" "${REPORT_CONTAINER_PATH}"
    fm star "Saved for inspection (on your Mac)" "${REPORT_HOST_PATH}" focus
    fm note "Insights describe scan health, not application safety. Review the actual values alongside zap.log and request evidence. Logged errors and warnings may include setup activity; check their timing and cause before deciding their impact. A completed scan and a matching custom alert do not prove complete coverage or validate every finding. Investigate affected requests before treating network failures as harmless. This step retrieves and interprets evidence; it does not require repairing network failures to zero."
    pass "Insights retrieved successfully; scan health requires interpretation"
    return "${STEP_RC}"
}
