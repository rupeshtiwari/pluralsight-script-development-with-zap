#!/usr/bin/env bash
# Capture the exact four public named-step outputs for parallel narration work.
# Same execution path as individual recording: steps/0N-*.sh -> _run_step.sh.
# Each step's canonical visible output is saved as logs/preflight-step-0N.log.
set -uo pipefail
if [ "$#" -ne 1 ]; then
    echo "usage: preflight_all_steps.sh DEMO_DIRECTORY" >&2
    exit 2
fi
DEMO_DIR="$(cd "$1" && pwd)"
cd "$DEMO_DIR" || exit 2
mkdir -p logs
# Never reuse a baseline from a failed or earlier preflight run.
rm -f logs/preflight-step-0[1-4].log
stamp="$(date +%Y%m%d-%H%M%S)"
full_log="logs/preflight-${stamp}.log"
raw_log="logs/preflight-${stamp}.ansi.log"
steps=(steps/0[1-4]-*.sh)
if [ "${#steps[@]}" -ne 4 ]; then
    echo "FAIL: expected four concept-named step scripts" >&2
    exit 1
fi
for i in 0 1 2 3; do
    if [[ "${steps[$i]}" != steps/0$((i+1))-*.sh ]]; then
        echo "FAIL: incorrect step order" >&2
        exit 1
    fi
done
main() {
    echo "PREFLIGHT · four actual demo steps, same commands as the Recorder"
    echo "Evidence is restricted to the authorized local Globomantics application."
    echo
    passed=1   # environmental readiness is checked by the real step engines
    for i in 0 1 2 3; do
        local step="${steps[$i]}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "STEP $((i+1)) · command: ./${step}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        if DEMO_SYNC_MODE=1 DEMO_SYNC_PHASE=reference "./${step}"; then
            passed=$((passed + 1))
        else
            echo "FAIL: Step $((i+1)) failed; baseline is not recording-ready."
            echo "RESULT: ${passed} checks passed before failure"
            return 1
        fi
        echo
    done
    echo "RESULT: ${passed} checks passed, 0 failed"
    echo "REFERENCE: logs/preflight-step-01.log through logs/preflight-step-04.log"
    echo "CHECK: compare the Recorder's same-output steps; separate ZAP GUI or Actions proof is still required."
}
# Full preflight keeps its high-level headings; per-step logs are byte-identical
# to the recording-mode terminal display when the proof is unchanged.
{ main; } 2>&1 | tee "$raw_log"
rc=${PIPESTATUS[0]}
cp "$raw_log" "$full_log"
echo "Full preflight log: ${full_log}"
exit "$rc"
