#!/bin/bash
# Shared step library for m2-c3 "Run authenticated ZAP scripts in GitHub
# Actions".
#
# Sourced by preflight_check.sh (author tooling). The clip's on-screen proof is
# the GitHub Actions job log; this library proves the SAME four beats LOCALLY by
# running the identical Automation Framework plan through ZAP's automation API,
# so you can validate against the objective before you push to CI:
#   1. Headless Automation Framework run   2. Authenticated context configuration
#   3. Authenticated script job result     4. Authenticated custom alert record
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
K="${ZAP_API_KEY:-}"

AF_PLAN_HOST="${DEMO_DIR}/ci/af-plan.yaml"
AF_PLAN_ZAP="/af/af-plan.yaml"
WORKFLOW_HOST="${REPO_ROOT}/.github/workflows/zap-authenticated-scan.yml"
ALERT_NAME="Globomantics unsafe reflection (custom rule)"

PASS=0; FAIL=0; STEP_RC=0
pass() { fm ok "$1"; PASS=$((PASS+1)); STEP_RC=0; }
fail() { fm fail "$1" "${2:-}" "${3:-}"; FAIL=$((FAIL+1)); STEP_RC=1; }
# A learner-authored deliverable is not written yet (expected on the -before branch, that IS the demo).
# Not a failure: friendly guidance on how to author it and where the finished reference lives.
need_author() { fm todo "$1" "${2:-}" "${3:-}" "$(author_try "${4:-}")"; STEP_RC=1; }
enc()  { python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=""))' "$1"; }

zap() { # <path> <query> -> body (asserts HTTP 200)
    local path="$1" query="${2:-}" code
    code="$(curl -s -o /tmp/.m2body -w '%{http_code}' "${ZAP}/JSON/${path}/?apikey=${K}&${query}")"
    [ "${code}" = "200" ] || { echo "  (ZAP API ${path} -> HTTP ${code})" >&2; return 1; }
    cat /tmp/.m2body
}

zap_container() { ( cd "${REPO_ROOT}" && docker compose ps -q zap 2>/dev/null ) | head -1; }

# The AF env registers the context's auth script by its FILE NAME
# (globomantics-auth.py) every time it creates the context. ZAP rejects a
# duplicate script name, so re-running the plan against the long-lived local ZAP
# aborts context creation ("A script with the same name already exists:
# globomantics-auth.py") before any job runs. Remove the demo scripts first so
# each run registers them cleanly, and make sure the report output dir exists and
# is writable. CI is unaffected, it runs a fresh ZAP per run, so the plan file
# itself is unchanged; this only makes the local re-runnable preflight reliable.
reset_plan_state() {
    local c; c="$(zap_container)"
    [ -n "${c}" ] && docker exec "${c}" sh -c 'mkdir -p /zap/wrk && chmod 0777 /zap/wrk' >/dev/null 2>&1 || true
    local s
    for s in "globomantics-auth.py" "globomantics-auth" "globomantics-active-rule" "globomantics-marker"; do
        zap script/action/remove "scriptName=$(enc "${s}")" >/dev/null 2>&1 || true
    done
}

PLAN_ID=""
run_plan() { # -> sets PLAN_ID
    reset_plan_state
    zap core/action/deleteAllAlerts >/dev/null || return 1   # every alert after this comes from this plan run
    local c; c="$(zap_container)"; [ -n "${c}" ] && docker exec "${c}" sh -c 'rm -f /tmp/globo-rule-trace.log' >/dev/null 2>&1
    PLAN_ID="$(zap automation/action/runPlan "filePath=$(enc "${AF_PLAN_ZAP}")" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("planId",""))
except Exception: print("")')"
    [ -n "${PLAN_ID}" ]
}
plan_progress() { zap automation/view/planProgress "planId=${PLAN_ID}"; }
plan_field() { # <jsonkey> -> count of entries in that list
    plan_progress | python3 -c 'import json,sys
try:
    values=json.load(sys.stdin)[sys.argv[1]]
    if not isinstance(values,list): raise ValueError("expected a plan progress list")
    print(len(values))
except Exception: print("?")' "$1"
}
plan_finished() { plan_progress | python3 "${REPO_ROOT}/runtime/scripts/zap_scan.py" plan-finished; }

# Poll a no-arg producer function until it prints something, or a timeout
# elapses. The AF plan can report "finished" a moment before the active scan's
# alerts are queryable, so Steps 3/4 wait for the evidence instead of checking
# once. Never weakens the check, it still requires the real alert.
wait_nonempty() { # <seconds> <fn> -> prints fn's first non-empty output
    local secs="$1" fn="$2" out i=0
    while [ "${i}" -lt "${secs}" ]; do
        out="$(${fn})"
        [ -n "${out}" ] && { printf '%s' "${out}"; return 0; }
        sleep 5; i=$((i+5))
    done
    printf ''
    return 1
}

custom_alert() {
    zap core/view/alerts "baseurl=$(enc "${APP_INTERNAL}/account/profile")" | python3 -c '
import json,sys
name=sys.argv[1]
try: data=json.load(sys.stdin)
except Exception: print(""); raise SystemExit
for a in data.get("alerts", []):
    if (a.get("alert") or a.get("name"))==name:
        print("%s|%s|%s" % (name, a.get("risk"), a.get("param"))); raise SystemExit
print("")' "${ALERT_NAME}"
}

ensure_ready() {
    [ -n "${K}" ] || { fail "ZAP_API_KEY is not set" "the .env file is missing or not loaded" "run from the repo so .env loads"; return 1; }
    zap core/view/version | grep -q '"version"' || {
        fail "ZAP API not reachable" "the stack may still be starting" "run scripts/lab-up.sh, wait for 'Up', then retry"; return 1; }
    [ -f "${AF_PLAN_HOST}" ] || {
        need_author "you have not written the Automation Framework plan yet" \
            "the m2-demo1-before branch ships without ci/af-plan.yaml on purpose; writing it IS this demo" \
            "author ci/af-plan.yaml (this demo's README, Step 1)" \
            "${AF_PLAN_HOST}"
        return 1; }
    # The workflow is shared course infrastructure (provided on every branch), NOT a file this demo
    # authors (the demo authors only ci/af-plan.yaml). If it is missing, that is a real problem.
    [ -f "${WORKFLOW_HOST}" ] || {
        fail "GitHub Actions workflow not found" \
            ".github/workflows/zap-authenticated-scan.yml is missing (it is shared infrastructure, not authored in this demo)" \
            "re-add it from the course repo (git checkout origin/main -- .github/workflows/zap-authenticated-scan.yml)"
        return 1; }
    zap automation/view/planProgress "planId=0" >/dev/null 2>&1 || zap core/view/version >/dev/null || true
    return 0
}

HOSTED_PATHS=(demos/module2-demos/m2-demo1-authenticated-zap-github-actions/ci demos/module1-demos/m1-demo2-javascript-http-sender/zap-scripts demos/module1-demos/m1-demo3-python-scanning-authentication/zap-scripts .github/workflows/zap-authenticated-scan.yml)
hosted() { python3 "${REPO_ROOT}/runtime/scripts/hosted_run.py" "${REPO_ROOT}" zap-authenticated-scan.yml m2-demo1-after "${HOSTED_PATHS[@]}" 2>/dev/null; }

# ===========================================================================
# STEP 1, Headless Automation Framework run (EO3a)  → "GitHub Actions job log"
# ===========================================================================
step1_headless_run() {
    fm header "ZAP runs headless from the Automation Framework plan" \
              "No GUI, no clicks, ZAP runs the whole scan from one config file. The GitHub Actions job log is the proof (EO3a)."
    if ! run_plan; then
        fail "the Automation Framework plan did not start" "automation/action/runPlan returned no plan id" \
             "check the automation add-on and the plan path /af/af-plan.yaml"
        return "${STEP_RC}"
    fi
    local i; for i in $(seq 1 120); do plan_finished && break; sleep 3; done
    local errs warns jobs; errs="$(plan_field error)"; warns="$(plan_field warn)"; jobs="$(plan_field info)"
    # The displayed value deliberately OMITS ZAP's Automation Framework plan id. ZAP mints and increments
    # that id on every runPlan (plan 0 on a fresh engine, a higher number as the engine is reused), so
    # printing it makes this line change run-to-run and unusable for a clean recording. The real
    # ${PLAN_ID} is still captured in run_plan() and drives every planProgress / plan_field / plan_finished
    # call for THIS run; only this human-facing line drops it. The stable, repeatable facts the learner
    # reads are: the plan finished, with zero errors and zero warnings (all still measured from the live run).
    fm star "Local plan run" "$(plan_finished && echo finished || echo NOT finished) · ${errs} errors · ${warns} warnings" focus
    local h id concl sha labels covers url steps
    h="$(hosted)"; IFS='|' read -r id concl sha labels covers url steps <<<"${h}"
    fm section "Hosted proof, GitHub Actions (read from the Actions API)"
    fm star "Workflow run" "${id:-none found} · ${concl:-?} · commit ${sha:-?}" focus
    fm star "Runner" "${labels:-?}"
    fm star "Headless ZAP step" "$(printf '%s' "${steps}" | tr ';' '\n' | grep -m1 '^Run ZAP headless' | cut -d= -f2 || echo '?')"
    fm star "Run covers this code" "${covers:-no}  ${url}"
    if plan_finished && [ "${errs}" = "0" ] && [ "${concl}" = "success" ] && [ "${covers}" = "yes" -o "${covers}" = "branch" ] \
       && [[ ",${labels}," == *",ubuntu-24.04,"* ]] && [[ "${steps}" == *"Run ZAP headless with the Automation Framework plan=success"* ]]; then
        pass "the plan ran headless with no errors, and the hosted ubuntu-24.04 job for this code succeeded"
    else
        fail "headless proof incomplete (local errors=${errs}; hosted=${concl:-none}, covers this code=${covers:-no})" \
             "the local plan failed, or no successful hosted run exists for the current scan files" \
             "fix the plan, or push / run the 'Globomantics authenticated ZAP scan' workflow on m2-demo1-after, then retry"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2, Authenticated context configuration (EO3a) → config artifact
# ===========================================================================
step2_context_config() {
    fm header "The authenticated context, declared as config, proven loaded by the hosted run" \
              "The plan binds scope, scripted login and user BEFORE scanning. The hosted job runs this exact plan and raises the custom alert on a login-only page, which only happens when ZAP loaded the context, user and scripted auth (EO3a)."
    local ctx auth engine user scope
    ctx="$(grep -A2 'contexts:' "${AF_PLAN_HOST}" | grep -m1 'name:' | sed 's/.*name: *//; s/"//g')"
    auth="$(awk '/authentication:/{f=1} f&&/method:/{print $2; exit}' "${AF_PLAN_HOST}" | tr -d '\"')"
    engine="$(grep -m1 'scriptEngine:' "${AF_PLAN_HOST}" | sed 's/.*scriptEngine: *//; s/\"//g')"
    user="$(awk '/users:/{f=1} f&&/name:/{print $3; exit}' "${AF_PLAN_HOST}" | tr -d '\"')"
    scope="$(grep -m1 'account/profile' "${AF_PLAN_HOST}" | sed 's/^ *- *//; s/\"//g')"
    local h id concl sha labels covers url steps assert
    h="$(hosted)"; IFS='|' read -r id concl sha labels covers url steps <<<"${h}"
    assert="$(printf '%s' "${steps}" | tr ';' '\n' | grep -m1 '^Assert the authenticated custom alert' | cut -d= -f2)"
    # Local supporting evidence: an authenticated (session-cookie) request reached the login-only page.
    local reached; reached="$(wait_nonempty 60 marker_on_auth_request)"
    fm star "Context · authentication · engine (ci/af-plan.yaml)" "${ctx} · ${auth} · ${engine}" focus
    fm star "User · scope" "${user} · ${scope}"
    fm star "Local: authenticated request reached the login-only page" "${reached:-none}"
    fm star "Hosted run proved it loaded (run ${id:-none})" "custom alert on login-only page: assert=${assert:-not found} · covers this code: ${covers:-no}" focus
    if [ "${ctx}" = "Globomantics" ] && [ "${auth}" = "script" ] && [ "${user}" = "alice" ] \
       && [[ "${scope}" == *account/profile* ]] && [ "${assert}" = "success" ] && { [ "${covers}" = "yes" ] || [ "${covers}" = "branch" ]; }; then
        pass "the plan declares the authenticated context and the hosted run proves ZAP loaded it (authenticated custom alert on a login-only page)"
    else
        fail "the authenticated context was not proven loaded (ctx=${ctx} auth=${auth} user=${user}; hosted assert=${assert:-none}, covers=${covers:-no})" \
             "the plan env block is incomplete, or no hosted run covers this code" \
             "check env.contexts in ci/af-plan.yaml; run the authenticated-scan workflow on m2-demo1-after"
    fi
    return "${STEP_RC}"
}

marker_on_auth_request() { # an authenticated scan request carrying the JS marker header
    zap core/view/messages "baseurl=$(enc "${APP_INTERNAL}/account/profile")&count=500" | python3 -c '
import json,sys
for m in reversed(json.load(sys.stdin).get("messages",[])):
    h=m.get("requestHeader","")
    if "X-Globomantics-Marker: GLOBO-DEMO" in h and "session=" in h.lower():
        print(h.splitlines()[0].strip()[:100]); break'
}

custom_alert_present() { # the custom Python rule's named alert on the authenticated page
    zap core/view/alerts "baseurl=$(enc "${APP_INTERNAL}/account/profile")" | python3 -c '
import json,sys
name=sys.argv[1]
for a in json.load(sys.stdin).get("alerts",[]):
    if (a.get("alert") or a.get("name"))==name:
        print("%s · %s/%s" % (a.get("pluginId"), a.get("risk"), a.get("confidence"))); break' "${ALERT_NAME}"
}

# ===========================================================================
# STEP 3, Authenticated script job result (EO3a) → "Authenticated script job result"
# ===========================================================================
step3_script_job() {
    fm header "The Module 1 scripts running during the authenticated plan" \
              "The JavaScript marker stamps the plan's requests, and the Python rule raises its alert on the login-only page, both from the same authenticated run (EO3a)."
    local js py h id concl sha labels covers url steps assert py_ok=""
    js="$(wait_nonempty 120 marker_on_auth_request)"
    py="$(wait_nonempty 120 custom_alert_present)"
    h="$(hosted)"; IFS='|' read -r id concl sha labels covers url steps <<<"${h}"
    assert="$(printf '%s' "${steps}" | tr ';' '\n' | grep -m1 '^Assert the authenticated custom alert' | cut -d= -f2)"
    { [ -n "${py}" ] || { [ "${assert}" = "success" ] && { [ "${covers}" = "yes" ] || [ "${covers}" = "branch" ]; }; }; } && py_ok=1
    fm star "JavaScript check (globomantics-marker)" "${js:+marker header on an authenticated request: }${js:-no marked authenticated request}" focus
    fm star "Python check (globomantics-active-rule)" "${py:+local custom alert }${py:-hosted report custom alert (assert=${assert:-none})}" focus
    if [ -n "${js}" ] && [ -n "${py_ok}" ]; then
        pass "both Module 1 scripts ran during the authenticated plan (JS stamped an authenticated request; the Python rule raised its alert on the login-only page)"
    else
        fail "a Module 1 script did not run (js=${js:+yes} python=${py_ok:+yes})" \
             "the script job did not load it, or the scan did not run as alice" \
             "run Step 1 first; check the script jobs and context user in ci/af-plan.yaml"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4, Authenticated custom alert record (EO3a) → "Authenticated custom alert record"
# ===========================================================================
step4_custom_alert() {
    fm header "The authenticated finding recorded by the pipeline" \
              "The custom rule's named alert on the login-only page, from this plan run locally, and from the hosted job's fail-closed report check (EO3a)."
    local rec n r p h id concl sha labels covers url steps
    rec="$(wait_nonempty 180 custom_alert)"
    IFS='|' read -r n r p <<<"${rec}"
    fm star "Alert (this plan run; store was cleared first)" "${n:-NOT RAISED}" focus
    fm star "Risk · parameter" "${r:-?} · ${p:-?}"
    h="$(hosted)"; IFS='|' read -r id concl sha labels covers url steps <<<"${h}"
    local assert; assert="$(printf '%s' "${steps}" | tr ';' '\n' | grep -m1 '^Assert the authenticated custom alert' | cut -d= -f2)"
    fm star "Hosted report check (run ${id:-none})" "${assert:-not found} · covers this code: ${covers:-no}" focus
    if [ -n "${rec}" ] && [ "${assert}" = "success" ] && [ "${covers}" = "yes" -o "${covers}" = "branch" ]; then
        pass "the custom alert was raised by this authenticated run, and the hosted job's report check passed for this code"
    else
        fail "authenticated custom alert not proven (local=${rec:+yes} hosted=${assert:-none} covers=${covers:-no})" \
             "the named custom alert is required; a built-in reflected-XSS finding does not substitute" \
             "run Step 1 first; for hosted proof run the workflow on m2-demo1-after"
    fi
    return "${STEP_RC}"
}
