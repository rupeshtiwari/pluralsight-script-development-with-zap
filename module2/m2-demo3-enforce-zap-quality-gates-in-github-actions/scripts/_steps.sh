#!/bin/bash
# Shared step library for m2-demo3 "Enforce ZAP quality gates in GitHub Actions".
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
REPO_ROOT="$(cd "${DEMO_DIR}/../.." && pwd)"
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/lib.sh"
FMT="${REPO_ROOT}/scripts/fmt.py"
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
jq_py() { python3 -c "$1"; }

zap_container() { docker ps --format '{{.Names}}' 2>/dev/null | grep -E 'zap' | head -1; }
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
    docker run --rm --network "${net}" -v "${GATE_DIR}:/zap/wrk:rw" "${img}" \
        zap.sh -cmd -autorun "${GATE_PLAN_ZAP}" >"${GATE_DIR}/run.log" 2>&1
    local code=$?
    echo "${code}" > "${GATE_EXIT_FILE}"
    [ -f "${GATE_REPORT}" ]
}

ensure_gate() { # reuse the last gate run, or run it once
    [ -f "${GATE_REPORT}" ] && [ -f "${GATE_EXIT_FILE}" ] && return 0
    fm note "Priming: no gate run in this session yet — running the gate plan headless once so this step has a report and an exit code."
    run_gate
}

ensure_ready() {
    command -v docker >/dev/null 2>&1 || { fail "docker is not available" "the demo runs the gate in a container" "install/start Docker (Colima) and retry"; return 1; }
    [ -n "$(zap_container)" ] || { fail "the ZAP stack is not running" "no zap container found" "run scripts/demo_up.sh, wait for 'Up', then retry"; return 1; }
    [ -f "${GATE_PLAN_HOST}" ] || { fail "gate plan not found" "ci/gate-plan.yaml is missing" "restore the file from the repo"; return 1; }
    ensure_gate || return 1
    return 0
}

# ===========================================================================
# STEP 1 — False Positive alert filter (EO3c)  -> "False Positive alert filter"
# ===========================================================================
step1_fp_filter() {
    fm header "A known benign finding is marked False Positive — by config" \
              "A quality gate must ignore noise it has already judged benign. The alertFilter job records that decision once, in the plan, so every run applies it (EO3c)."
    local blk; blk="$(jq_py 'import re,sys
t=open("'"${GATE_PLAN_HOST}"'").read()
rid=re.search(r"ruleId:\s*([0-9]+)",t)
risk=re.search(r"newRisk:\s*\"([^\"]+)\"",t)
url=re.search(r"url:\s*\"([^\"]+)\"",t)
print("%s|%s|%s" % (rid.group(1) if rid else "", risk.group(1) if risk else "", url.group(1) if url else ""))')"
    IFS='|' read -r rid risk url <<<"${blk}"
    if [ "${rid}" = "${FP_RULE}" ] && [ -n "${risk}" ]; then
        fm star "Filtered rule  (ruleId)" "${rid}  (X-Content-Type-Options Header Missing)" focus
        fm star "New disposition  (newRisk)" "${risk}"
        fm star "Scope  (url)" "${url}"
        pass "the plan marks the benign finding as a False Positive"
    else
        fail "the alertFilter config is missing or wrong" \
             "expected ruleId ${FP_RULE} with newRisk in ci/gate-plan.yaml" \
             "ask: 'the alertFilter job in gate-plan.yaml is incomplete; restore the False Positive filter for rule ${FP_RULE}'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 2 — Automation Framework job order (EO3c)  -> "Automation Framework job order"
# ===========================================================================
step2_job_order() {
    fm header "Order matters: filter BEFORE scan, gate LAST" \
              "A filter applied after scanning would be too late. The plan's job order makes the disposition apply to every alert, and the gate run last (EO3c)."
    local order; order="$(jq_py 'import re,sys
t=open("'"${GATE_PLAN_HOST}"'").read()
jobs=re.findall(r"-\s*type:\s*(\w+)",t)
print(" -> ".join(jobs))')"
    fm star "Job order (ci/gate-plan.yaml)" "${order}" focus
    # alertFilter must come before activeScan, and exitStatus must be last.
    local ok; ok="$(jq_py 'import re
t=open("'"${GATE_PLAN_HOST}"'").read()
jobs=re.findall(r"-\s*type:\s*(\w+)",t)
af=jobs.index("alertFilter") if "alertFilter" in jobs else -1
asc=jobs.index("activeScan") if "activeScan" in jobs else -1
ok = af>=0 and asc>=0 and af<asc and jobs and jobs[-1]=="exitStatus"
print("yes" if ok else "no")')"
    if [ "${ok}" = "yes" ]; then
        fm star "alertFilter before activeScan" "yes — later alerts inherit the disposition"
        fm star "exitStatus runs last" "yes — the gate decides on the final alert set"
        pass "the job order applies the filter before scanning and gates last"
    else
        fail "the job order is wrong" \
             "alertFilter must precede activeScan and exitStatus must be last" \
             "ask: 'reorder gate-plan.yaml jobs so alertFilter runs before activeScan and exitStatus is last'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 3 — Gate JSON report and exit code (EO3c)  -> "Gate JSON report and exit code"
# ===========================================================================
step3_gate_exit() {
    fm header "The gate turns alert risk into a build decision" \
              "exitStatus compares the remaining alerts against warnLevel/errorLevel and sets the process exit code — the signal a pipeline blocks on (EO3c)."
    run_gate || { fail "the gate run did not produce a report" "zap.sh -cmd -autorun failed" "ask: 'the headless gate run failed; read logs/.gate/run.log and fix gate-plan.yaml'"; return "${STEP_RC}"; }
    local code; code="$(cat "${GATE_EXIT_FILE}" 2>/dev/null)"
    local highs; highs="$(jq_py 'import json
try: d=json.load(open("'"${GATE_REPORT}"'"))
except Exception: print(0); raise SystemExit
n=0
for s in d.get("site",[]):
    for a in s.get("alerts",[]):
        if str(a.get("riskcode"))=="3": n+=1
print(n)')"
    fm star "Gate thresholds  (errorLevel · warnLevel)" "HIGH · MEDIUM" focus
    fm star "High-risk alerts after filtering" "${highs}"
    fm star "Process exit code  (echo \$?)" "${code}"
    local verdict; verdict="BLOCKED"; [ "${code}" = "0" ] && verdict="passed"
    fm star "Build decision" "exit ${code} → the gate ${verdict} the build"
    if [ -n "${code}" ] && [ "${code}" != "0" ]; then
        pass "the gate blocked the build (non-zero exit) on the High-risk alert"
    elif [ "${code}" = "0" ]; then
        fail "the gate did not block the build" \
             "exit code was 0 though a High-risk alert was expected (highs=${highs})" \
             "ask: 'the gate exited 0; confirm /greet still has the reflected-XSS High and errorLevel=HIGH in gate-plan.yaml'"
    else
        fail "no exit code was captured from the gate run" \
             "the headless run did not return a process result" \
             "ask: 'the gate run produced no exit code; read logs/.gate/run.log'"
    fi
    return "${STEP_RC}"
}

# ===========================================================================
# STEP 4 — Filtered alert report (EO3c)  -> "Filtered alert report"
# ===========================================================================
step4_filtered_report() {
    fm header "The report proves the filter held and the gate was right" \
              "The benign finding now carries the False Positive disposition, while the real High finding remains — exactly why the gate blocked (EO3c)."
    ensure_gate || { return "${STEP_RC}"; }
    local fp; fp="$(jq_py 'import json
try: d=json.load(open("'"${GATE_REPORT}"'"))
except Exception: print("|"); raise SystemExit
for s in d.get("site",[]):
    for a in s.get("alerts",[]):
        if str(a.get("pluginid"))=="'"${FP_RULE}"'":
            print("%s|%s" % (a.get("name") or a.get("alert"), a.get("riskdesc","")))
            raise SystemExit
print("|")')"
    local xss; xss="$(jq_py 'import json
try: d=json.load(open("'"${GATE_REPORT}"'"))
except Exception: print("|"); raise SystemExit
for s in d.get("site",[]):
    for a in s.get("alerts",[]):
        if str(a.get("pluginid"))=="'"${XSS_RULE}"'":
            print("%s|%s" % (a.get("name") or a.get("alert"), a.get("riskdesc","")))
            raise SystemExit
print("|")')"
    IFS='|' read -r fpn fpr <<<"${fp}"
    IFS='|' read -r xn xr <<<"${xss}"
    fm star "Benign finding  (rule ${FP_RULE})" "${fpn:-not present} — ${fpr:-filtered to False Positive}" focus
    fm star "Real finding  (rule ${XSS_RULE})" "${xn:-Cross Site Scripting (Reflected)} — ${xr:-High}"
    fm star "Gate outcome" "benign filtered out, High kept → build blocked"
    if [ -n "${xn}" ] || [ -n "${xr}" ]; then
        pass "the filtered report shows the benign finding disposed and the High kept"
    else
        fail "the report did not show the expected findings" \
             "neither the filtered benign finding nor the High was found" \
             "ask: 'the gate report is missing expected alerts; confirm the scan reached /greet and the filter rule id'"
    fi
    return "${STEP_RC}"
}
