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
# is writable. CI is unaffected — it runs a fresh ZAP per run — so the plan file
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
    PLAN_ID="$(zap automation/action/runPlan "filePath=$(enc "${AF_PLAN_ZAP}")" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("planId",""))
except Exception: print("")')"
    [ -n "${PLAN_ID}" ]
}
plan_progress() { zap automation/view/planProgress "planId=${PLAN_ID}"; }
plan_field() { # <jsonkey> -> count of entries in that list
    plan_progress | python3 -c 'import json,sys
try: print(len(json.load(sys.stdin).get(sys.argv[1],[])))
except Exception: print("0")' "$1"
}
plan_finished() { plan_progress | grep -q '"finished"[^,]*[0-9T:-]'; }

# Poll a no-arg producer function until it prints something, or a timeout
# elapses. The AF plan can report "finished" a moment before the active scan's
# alerts are queryable, so Steps 3/4 wait for the evidence instead of checking
# once. Never weakens the check — it still requires the real alert.
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

reflection_reached() {
    zap core/view/alerts "baseurl=$(enc "${APP_INTERNAL}/account/profile")" | python3 -c '
import json,sys
try: data=json.load(sys.stdin)
except Exception: print(""); raise SystemExit
for a in data.get("alerts", []):
    nm=(a.get("alert") or a.get("name") or "")
    if "Cross Site Scripting (Reflected)" in nm:
        print("%s | param=%s" % (nm, a.get("param"))); raise SystemExit
print("")'
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
        fail "ZAP API not reachable" "the stack may still be starting" "run scripts/demo_up.sh, wait for 'Up', then retry"; return 1; }
    [ -f "${AF_PLAN_HOST}" ] || {
        fail "Automation Framework plan not found" "ci/af-plan.yaml is missing" "restore the file from the repo"; return 1; }
    [ -f "${WORKFLOW_HOST}" ] || {
        fail "GitHub Actions workflow not found" ".github/workflows/zap-authenticated-scan.yml is missing" "restore the file from the repo"; return 1; }
    zap automation/view/planProgress "planId=0" >/dev/null 2>&1 || zap core/view/version >/dev/null || true
    return 0
}

# ===========================================================================
# STEP 1 — Headless Automation Framework run (EO3a)  → "GitHub Actions job log"
# ===========================================================================
step1_headless_run() {
    fm header "ZAP runs headless from the Automation Framework plan" \
              "No GUI, no clicks — ZAP runs the whole scan from one config file, exactly as the GitHub Actions job does (EO3a)."
    fm star "Runner (CI)" "ubuntu-24.04 · ghcr.io/zaproxy/zaproxy:stable" focus
    fm star "Command" "zap.sh -cmd -autorun /zap/wrk/af-plan.yaml  (headless)"
    if ! run_plan; then
        fail "the Automation Framework plan did not start" "automation/action/runPlan returned no plan id" \
             "ask: 'the ZAP Automation Framework could not run /af/af-plan.yaml; check the automation add-on and the plan path'"
        return "${STEP_RC}"
    fi
    local i
    for i in $(seq 1 120); do
        plan_finished && break
        sleep 3
    done
    local errs; errs="$(plan_field error)"
    if plan_finished && [ "${errs}" = "0" ]; then
        pass "the plan ran headless to completion with no errors"
    else
        fail "the headless plan did not finish cleanly" "it is still running, or it reported ${errs} error(s)" \
             "ask: 'the ZAP AF plan reported errors; read automation/view/planProgress and fix the plan'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2 — Authenticated context configuration (EO3a) → config artifact
# ===========================================================================
step2_context_config() {
    fm header "The authenticated context, declared as config" \
              "The plan binds the target scope, the scripted login, and the user BEFORE scanning — the config a pipeline runs unattended (EO3a)."
    local ok=1
    grep -q 'Globomantics' "${AF_PLAN_HOST}" || ok=0
    grep -q 'globomantics-auth' "${AF_PLAN_HOST}" || ok=0
    grep -q 'alice' "${AF_PLAN_HOST}" || ok=0
    grep -q 'app:8000' "${AF_PLAN_HOST}" || ok=0
    fm star "Context" "Globomantics" focus
    fm star "Authentication" "script-based → globomantics-auth (Login URL: /login)"
    fm star "User" "alice"
    fm star "Target scope" "http://app:8000 (profile + greet paths)"
    if [ "${ok}" = 1 ]; then
        pass "the plan binds context + scripted auth + user + scope before scanning"
    else
        fail "the authenticated context configuration is incomplete" \
             "the plan is missing the context, auth script, user, or scope" \
             "ask: 'the af-plan.yaml context/auth/user/scope block is incomplete; restore it'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3 — Authenticated script job result (EO3a) → "Authenticated script job result"
# ===========================================================================
step3_script_job() {
    fm header "The Module 1 scripts running under the authenticated scope" \
              "The same JavaScript and Python checks you wrote in Module 1 now run unattended, logged in as alice (EO3a)."
    fm star "Loaded by the plan" "globomantics-marker (JS) · globomantics-active-rule (Py) · globomantics-auth (Py)" focus
    local refl; refl="$(wait_nonempty 180 reflection_reached)"
    if [ -n "${refl}" ]; then
        fm star "Ran authenticated against" "/account/profile — reflection reached while logged in"
        pass "the scripts executed against the authenticated scope"
    else
        fail "the scripts did not run against the authenticated scope" \
             "the active scan did not reach the logged-in page" \
             "ask: 'the AF plan scan did not run authenticated; check the context user and scripted auth'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4 — Authenticated custom alert record (EO3a) → "Authenticated custom alert record"
# ===========================================================================
step4_custom_alert() {
    fm header "The authenticated finding recorded by the pipeline" \
              "The headless run records the custom rule's named alert on the login-only page, logged in as alice — the result a quality gate can later gate on (EO3a)."
    local rec; rec="$(wait_nonempty 180 custom_alert)"
    if [ -n "${rec}" ]; then
        IFS='|' read -r n r p <<<"${rec}"
        fm star "Alert" "${n}" focus
        fm star "Risk" "${r}"
        fm star "Parameter" "${p}"
        pass "the custom rule raised its named alert under the authenticated AF run (serialized in the headless report)"
    else
        # The required proof is the NAMED custom alert. A built-in reflected-XSS
        # finding is NOT an acceptable substitute, so a missing custom alert is a
        # hard failure. Any reflection found is shown only as a diagnostic.
        local refl; refl="$(reflection_reached)"
        fail "the authenticated AF run did not record the custom alert '${ALERT_NAME}'" \
             "the named custom alert is required here; a built-in reflected-XSS finding${refl:+ (present: ${refl})} does not substitute for it" \
             "ask: 'the authenticated AF scan did not raise ${ALERT_NAME} on /account/profile as alice; check the context auth and the custom rule'"
    fi
    return "${STEP_RC}"
}
