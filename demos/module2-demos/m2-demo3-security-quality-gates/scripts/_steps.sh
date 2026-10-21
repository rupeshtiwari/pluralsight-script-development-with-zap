#!/bin/bash
# Shared step library for m2-c5 "Enforce ZAP quality gates in GitHub Actions".
#
# Sourced by preflight_check.sh and demo_step.sh. This demo is about the GATE:
# an alertFilter marks a benign finding as a False Positive BEFORE scanning, then
# exitStatus turns the remaining alert risks into a process exit code a pipeline
# blocks on (EO3c).
#   1. False Positive alert filter    2. Automation Framework job order
#   3. Gate JSON report and exit code  4. Filtered alert report
#
# Every request targets ONLY the local Globomantics app on the compose network.

HERE_STEPS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO_DIR="$(cd "${HERE_STEPS}/.." && pwd)"
REPO_ROOT="$(cd "${DEMO_DIR}/../../.." && pwd)"
# shellcheck disable=SC1091
source "${REPO_ROOT}/runtime/scripts/lib.sh"
FMT="${REPO_ROOT}/runtime/scripts/fmt.py"
fm() { python3 "${FMT}" "$@"; }

GATE_PLAN_HOST="${DEMO_DIR}/ci/gate-plan.yaml"
GATE_PLAN_ZAP="/zap/wrk/gate-plan.yaml"
GATE_DIR="${DEMO_DIR}/logs/.gate"
GATE_REPORT="${GATE_DIR}/globo-gate-report.json"
GATE_EXIT_FILE="${GATE_DIR}/exit"
FP_RULE="10021"                 # X-Content-Type-Options Header Missing (benign)
XSS_RULE="40012"                # Cross Site Scripting (Reflected) (the real risk)
ZAP_IMAGE_D="${ZAP_IMAGE:-ghcr.io/zaproxy/zaproxy:stable}"

PASS=0; FAIL=0; STEP_RC=0
pass() { fm ok "$1"; PASS=$((PASS+1)); STEP_RC=0; }
fail() { fm fail "$1" "${2:-}" "${3:-}"; FAIL=$((FAIL+1)); STEP_RC=1; }
# A learner-authored deliverable is not written yet (expected on the -before branch, that IS the demo).
# Not a failure: friendly guidance on how to author it and where the finished reference lives.
need_author() { fm todo "$1" "${2:-}" "${3:-}" "$(author_try "${4:-}")"; STEP_RC=1; }
jq_py() { python3 -c "$1"; }

# Select the ZAP SERVICE container specifically. The compose project name
# contains "zap", so a plain `grep zap` matches every service (app, mongo,
# postgres, zap). `docker compose ps -q zap` resolves the zap service only
# (same approach as m2-c3 / m2-c4).
zap_container() { ( cd "${REPO_ROOT}" && docker compose ps -q zap 2>/dev/null ) | head -1; }
compose_net() {
    local cid; cid="$(zap_container)"
    [ -n "${cid}" ] || { echo ""; return; }
    docker inspect -f '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}' "${cid}" 2>/dev/null | awk '{print $1}'
}

# Run the gate plan HEADLESS, exactly as CI does, and capture its exit code.
run_gate() {
    local net img; net="$(compose_net)"; img="${ZAP_IMAGE_D}"
    [ -n "${net}" ] || { fail "could not find the ZAP container network" "is the stack up?" "run scripts/demo_up.sh and retry"; return 1; }
    mkdir -p "${GATE_DIR}"; rm -f "${GATE_REPORT}"
    cp "${GATE_PLAN_HOST}" "${GATE_DIR}/gate-plan.yaml"
    chmod -R 0777 "${GATE_DIR}"
    docker run --rm --network "${net}" -v "${GATE_DIR}:/zap/wrk:rw" \
        -v "${REPO_ROOT}/demos/module1-demos/m1-demo2-javascript-http-sender/zap-scripts:/zap-scripts:ro" "${img}" \
        zap.sh -cmd -autorun "${GATE_PLAN_ZAP}" >"${GATE_DIR}/run.log" 2>&1
    local code=$?
    echo "${code}" > "${GATE_EXIT_FILE}"
    [ -f "${GATE_REPORT}" ]
}

ensure_gate() { # reuse the last gate run, or run it once
    [ -f "${GATE_REPORT}" ] && [ -f "${GATE_EXIT_FILE}" ] && return 0
    fm note "Priming: no gate run in this session yet, running the gate plan headless once so this step has a report and an exit code."
    run_gate
}

ensure_ready() {
    command -v docker >/dev/null 2>&1 || { fail "docker is not available" "the demo runs the gate in a container" "install/start Docker (Colima) and retry"; return 1; }
    [ -n "$(zap_container)" ] || { fail "the ZAP stack is not running" "no zap container found" "run scripts/demo_up.sh, wait for 'Up', then retry"; return 1; }
    [ -f "${GATE_PLAN_HOST}" ] || {
        need_author "you have not written the quality-gate plan yet" \
            "the m2-demo3-before branch ships without ci/gate-plan.yaml on purpose; writing it IS this demo" \
            "author ci/gate-plan.yaml (this demo's README, Step 1); the finished reference is on the m2-demo3-after branch" \
            "${GATE_PLAN_HOST}"
        return 1; }
    # Gate execution belongs to named Step 3, not hidden readiness.
    return 0
}

OUTLINE_ORDER="passiveScan-config alertFilter script spider passiveScan-wait activeScan-policy activeScan passiveScan-wait report exitStatus"
plan_jobs() { python3 -c 'import re,sys
t=open(sys.argv[1]).read()
print(" ".join(re.findall(r"^\s*-\s*type:\s*([\w-]+)", t, re.M)))' "${GATE_PLAN_HOST}"; }
plan_value() { python3 -c 'import re,sys
m=re.search(sys.argv[2]+r":\s*\"?([^\"\n#]+?)\"?\s*(?:#.*)?$", open(sys.argv[1]).read(), re.M)
print(m.group(1).strip() if m else "")' "${GATE_PLAN_HOST}" "$1"; }
HOSTED_PATHS=(demos/module2-demos/m2-demo3-security-quality-gates/ci .github/workflows/zap-quality-gate.yml runtime/app)
hosted() { python3 "${REPO_ROOT}/runtime/scripts/hosted_run.py" "${REPO_ROOT}" zap-quality-gate.yml m2-demo3-after "${HOSTED_PATHS[@]}" 2>/dev/null; }

# ===========================================================================
# STEP 1, False Positive alert filter (EO3c)  -> "False Positive alert filter"
# ===========================================================================
step1_fp_filter() {
    fm header "A known benign finding is marked False Positive, by config" \
              "A quality gate must ignore noise it has already judged benign. The alertFilter job records that decision once, in the plan, so every run applies it (EO3c)."
    local rid risk url
    rid="$(plan_value ruleId)"; risk="$(plan_value newRisk)"; url="$(plan_value url)"
    fm star "Filtered rule  (ruleId)" "${rid:-<none>}  (X-Content-Type-Options Header Missing)" focus
    fm star "New disposition  (newRisk)" "${risk:-<none>}" focus
    fm star "Scope  (url)" "${url:-<none>}"
    if [ "${rid}" = "${FP_RULE}" ] && [ "${risk}" = "False Positive" ] && [ -n "${url}" ]; then
        pass "the plan marks rule ${FP_RULE} as a False Positive, scoped to ${url}"
    else
        fail "the alertFilter config is missing or wrong (ruleId=${rid:-none}, newRisk=${risk:-none})" \
             "expected ruleId ${FP_RULE} with newRisk \"False Positive\" and a url scope in ci/gate-plan.yaml" \
             "restore the alertFilter job for rule ${FP_RULE}"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2, Automation Framework job order (EO3c)  -> "Automation Framework job order"
# ===========================================================================
step2_job_order() {
    fm header "Order matters: filter BEFORE scan, gate LAST" \
              "A filter applied after scanning would be too late. The plan follows the architecture's job order, so the disposition applies to every alert and the gate runs last (EO3c)."
    local jobs; jobs="$(plan_jobs)"
    fm star "Job order (ci/gate-plan.yaml)" "$(echo "${jobs}" | sed 's/ / → /g')" focus
    fm star "Architecture order (Module 2)" "$(echo "${OUTLINE_ORDER}" | sed 's/ / → /g')"
    # Collapse repeated script jobs (add + enable) before comparing.
    local cmp; cmp="$(echo "${jobs}" | tr ' ' '\n' | awk 'NR==1||$0!=p{print}{p=$0}' | tr '\n' ' ' | sed 's/ $//')"
    if [ "${cmp}" = "${OUTLINE_ORDER}" ]; then
        fm star "alertFilter before activeScan · exitStatus last" "yes · yes"
        pass "the plan follows the architecture job order: filter before scanning, gate last"
    else
        fail "the job order does not follow the architecture order" \
             "got: ${cmp}" "reorder ci/gate-plan.yaml to: ${OUTLINE_ORDER}"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3, Gate JSON report and exit code (EO3c)  -> "Gate JSON report and exit code"
# ===========================================================================
step3_gate_exit() {
    fm header "The gate turns alert risk into a build decision" \
              "exitStatus compares the remaining alerts against warnLevel/errorLevel and sets the process exit code, the signal a pipeline blocks on (EO3c)."
    run_gate || { fail "the gate run did not produce a report" "zap.sh -cmd -autorun failed" "read logs/.gate/run.log and fix gate-plan.yaml"; return "${STEP_RC}"; }
    local code; code="$(cat "${GATE_EXIT_FILE}" 2>/dev/null)"
    local highs; highs="$(jq_py 'import json
d=json.load(open("'"${GATE_REPORT}"'"))
print(sum(1 for s in d.get("site",[]) for a in s.get("alerts",[]) if str(a.get("riskcode"))=="3"))')"
    local el wl; el="$(plan_value errorLevel)"; wl="$(plan_value warnLevel)"
    fm star "Gate thresholds from the plan  (errorLevel · warnLevel)" "${el:-?} · ${wl:-?}" focus
    fm star "High-risk alerts after filtering (report)" "${highs}"
    fm star "Process exit code  (echo \$?)" "${code}" focus
    local h id concl sha labels covers url steps gstep
    h="$(hosted)"; IFS='|' read -r id concl sha labels covers url steps <<<"${h}"
    gstep="$(printf '%s' "${steps}" | tr ';' '\n' | grep -m1 '^Run the ZAP quality gate' | cut -d= -f2)"
    fm star "Hosted gate run (GitHub Actions)" "${id:-none found} · gate step ${gstep:-?} · commit ${sha:-?} · covers this code: ${covers:-no}"
    if [ "${code}" = "1" ] && [[ "${highs}" =~ ^[0-9]+$ ]] && [ "${highs}" -gt 0 ] && [ "${el}" = "HIGH" ] \
       && [ "${gstep}" = "failure" ] && [ "${covers}" = "yes" -o "${covers}" = "branch" ]; then
        pass "the gate exited 1 for a real High-risk alert, and the hosted gate job blocked the build for this code"
    elif [ "${code}" = "1" ] && [ "${highs:-0}" -gt 0 ]; then
        fail "local gate blocked correctly, but no hosted gate run covers this code" \
             "the GitHub Actions gate run is part of this demo's proof" \
             "run the 'Globomantics ZAP quality gate' workflow on m2-demo3-after (Actions → Run workflow), then retry"
    else
        fail "the gate did not prove the expected exit=1 High-risk decision (exit=${code:-?}, highs=${highs:-?})" \
             "expected exit 1 with at least one High finding" "read logs/.gate/run.log"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4, Filtered alert report (EO3c)  -> "Filtered alert report"
# ===========================================================================
step4_filtered_report() {
    fm header "The report proves the filter held and the gate was right" \
              "The benign finding now carries the False Positive disposition, while the real High finding remains, exactly why the gate blocked (EO3c)."
    ensure_gate || { return "${STEP_RC}"; }
    local row; row="$(jq_py 'import json
d=json.load(open("'"${GATE_REPORT}"'"))
fp=xs=("","")
for s in d.get("site",[]):
    for a in s.get("alerts",[]):
        if str(a.get("pluginid"))=="'"${FP_RULE}"'": fp=(a.get("name") or a.get("alert",""), a.get("riskdesc",""))
        if str(a.get("pluginid"))=="'"${XSS_RULE}"'": xs=(a.get("name") or a.get("alert",""), a.get("riskdesc",""))
print("|".join(fp+xs))')"
    IFS='|' read -r fpn fpr xn xr <<<"${row}"
    local code; code="$(cat "${GATE_EXIT_FILE}" 2>/dev/null)"
    fm star "Benign finding  (rule ${FP_RULE})" "${fpn:-not present}, ${fpr:-not present}" focus
    fm star "Real finding  (rule ${XSS_RULE})" "${xn:-not present}, ${xr:-not present}" focus
    fm star "Gate outcome (from this run)" "exit ${code:-?} → $([ "${code}" = 1 ] && echo 'build blocked' || echo 'build NOT blocked')"
    if [ -n "${fpn}" ] && [[ "${fpr}" == *"False Positive"* ]] && [ -n "${xn}" ] && [[ "${xr}" == High* ]] && [ "${code}" = 1 ]; then
        pass "the filtered report shows the benign finding as False Positive and the High kept, the reason the gate blocked"
    else
        fail "the report did not prove both the False Positive and the remaining High-risk alert" \
             "expected rule ${FP_RULE} False Positive and rule ${XSS_RULE} High from the same run that exited 1" \
             "run Step 3 first; confirm the scan reached /greet"
    fi
    return "${STEP_RC}"
}
