#!/usr/bin/env bash
# Whole-course preflight: run EVERY module's EVERY demo, step by step, in the exact order and the
# exact output format you would see, so you confirm the entire course in one command instead
# of testing each demo by hand.
#
#   ./preflight-check                (from the repo root; the whole course — same as calling this script)
#   ./preflight-check --m1           (scope to one module; --m1d1 scopes to one demo)
#   runtime/scripts/preflight_course.sh [REPO_ROOT] [FILTER] [SCOPE_LABEL]
#
# What it writes (at the repo root, so you can hand them straight back):
#   course-evidence.txt      one text file with every demo's four steps and their real output,
#                            grouped module by module, demo by demo. This is the evidence a student
#                            reads before starting: if it is all PASS, the course runs.
#   FAIL-<module>-<demo>.log a separate log written ONLY for a demo that failed, named so you can see
#                            at a glance which module and demo broke. It holds that demo's full output
#                            and the failing step, and it is exactly what to hand back to fix the step.
#
# Exit code is non-zero if any demo failed, so CI (and a student) can treat "course did not pass" as a
# hard stop: if this fails, do not start. The per-demo runner temporarily supplies missing
# reference sources. The scope transaction restores owned files only after total success.
set -uo pipefail

ROOT="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
# Optional scope: $2 is a grep -E pattern matched against each demo's repo-relative path (empty = the
# whole course); $3 is a human label for the header. The ./preflight-check front door translates
# --m1 / --m1d1 into these, so this engine stays one simple, filterable loop.
FILTER="${2:-}"
SCOPE_LABEL="${3:-every module, every demo, every step, in order}"
cd "$ROOT" || exit 2

# Validate the selector before potentially starting a large local stack.
selected=()
while IFS= read -r stepsdir; do
  selected+=("$stepsdir")
done < <(find "$ROOT"/demos -type d -name steps | sort | { if [ -n "$FILTER" ]; then grep -E "$FILTER"; else cat; fi; })
if [ "${#selected[@]}" -eq 0 ]; then
  echo "No demo matched the requested scope${FILTER:+ (filter: $FILTER)}."
  exit 2
fi

# One transaction spans every selected demo; no cleanup after an early success.
if [ "${PREFLIGHT_WORKSPACE_ACTIVE:-}" != "$ROOT/.preflight-workspace" ]; then
  exec python3 "$ROOT/runtime/scripts/preflight_workspace.py" run "$ROOT" "$FILTER" "$SCOPE_LABEL"
fi

EVIDENCE="$ROOT/course-evidence.txt"
runner="$ROOT/runtime/scripts/preflight_all_steps.sh"
[ -x "$runner" ] || { echo "cannot find preflight_all_steps.sh" >&2; exit 2; }

# Start clean: one evidence file per run, and no stale FAIL logs from an earlier run.
rm -f "$ROOT"/FAIL-*.log
: > "$EVIDENCE"
{
  echo "PREFLIGHT CHECK · ${SCOPE_LABEL}"
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "Evidence is restricted to the authorized local Globomantics application."
  echo
} >> "$EVIDENCE"

# Keep the runner PID so cancelling this front door also waits for source cleanup.
runner_pid=""; tee_pid=""; capture=""; fifo=""
cleanup_capture() {
  if [ -n "$runner_pid" ]; then
    kill -TERM "$runner_pid" 2>/dev/null || true
    wait "$runner_pid" 2>/dev/null || true
  fi
  if [ -n "$tee_pid" ]; then
    kill -TERM "$tee_pid" 2>/dev/null || true
    wait "$tee_pid" 2>/dev/null || true
  fi
  [ -z "$capture" ] || rm -f "$capture"
  [ -z "$fifo" ] || rm -f "$fifo"
}
cancel_preflight() {
  local code="$1"
  trap '' INT TERM HUP
  if [ -n "$runner_pid" ]; then
    kill -TERM "$runner_pid" 2>/dev/null || true
    wait "$runner_pid" 2>/dev/null || true
    runner_pid=""
  fi
  if [ -n "$tee_pid" ]; then
    wait "$tee_pid" 2>/dev/null || true
    tee_pid=""
  fi
  echo "Course preflight INTERRUPTED; no further demos were run. Evidence: ${EVIDENCE#"$ROOT"/}" | tee -a "$EVIDENCE"
  exit "$code"
}
trap cleanup_capture EXIT
trap 'cancel_preflight 130' INT
trap 'cancel_preflight 143' TERM
trap 'cancel_preflight 129' HUP

# FIFO + separate tee PID preserves the runner exit status, streams progress on
# macOS Bash 3.2 and Linux, and lets cancellation wait for source restoration.
run_logged() {
  local status tee_status
  capture="$(mktemp "$ROOT/.preflight-output.XXXXXX")" || return 1
  fifo="${capture}.pipe"
  mkfifo "$fifo" || return 1
  tee -a "$capture" "$EVIDENCE" < "$fifo" & tee_pid=$!
  "$@" > "$fifo" 2>&1 & runner_pid=$!
  wait "$runner_pid"; status=$?
  runner_pid=""
  wait "$tee_pid"; tee_status=$?
  tee_pid=""
  out="$(cat "$capture")"
  printf '\n' >> "$EVIDENCE"
  rm -f "$capture" "$fifo"; capture=""; fifo=""
  [ "$status" -ne 0 ] || status="$tee_status"
  return "$status"
}


out=""
if run_logged "$ROOT/runtime/scripts/preflight_runtime.sh"; then
  :
else
  status=$?
  printf '%s\n' "$out" > "$ROOT/FAIL-setup.log"
  echo "PREFLIGHT SETUP FAILED · no demo steps executed. See FAIL-setup.log and the error above." | tee -a "$EVIDENCE"
  run_logged "$ROOT/runtime/scripts/preflight_diagnose.sh" || true
  exit "$status"
fi

total=0; passed=0; failed=0; course_rc=0; diagnosed=0

# demos/module1-demos/m1-demo1-... before module2, m1-demo1 before m1-demo2: plain sort is the right order.
for stepsdir in "${selected[@]}"; do
  demo_dir="$(dirname "$stepsdir")"
  rel="${demo_dir#"$ROOT"/}"                       # e.g. demos/module1-demos/m1-demo1-...
  module="$(printf '%s' "$rel" | sed -E 's#demos/(module[0-9]+)-demos/.*#\1#')"
  demo="$(basename "$demo_dir")"
  total=$((total+1))

  banner="════════════════════════════════════════════════════════════════
  ${module} · ${demo}
════════════════════════════════════════════════════════════════"
  echo "$banner"
  { echo "$banner"; } >> "$EVIDENCE"

  run_logged "$runner" "$demo_dir"; rc=$?

  # A missing-source gate is incomplete validation, never a skipped success.
  if [ "$rc" -eq 0 ] && [[ "$out" != *"AUTHOR THIS FIRST"* ]]; then
    passed=$((passed+1))
    echo "  ✅ PASS (${demo})"
    { echo "RESULT for ${demo}: PASS"; echo; } >> "$EVIDENCE"
  else
    failed=$((failed+1)); course_rc=1
    faillog="$ROOT/FAIL-${module}-${demo}.log"
    {
      echo "FAILED DEMO: ${module} / ${demo}"
      echo "Demo folder: ${rel}"
      echo "Hand this file back to fix the step. The failing step is the one whose block ends in ✘ FAIL below."
      echo "Failing step(s): $(printf '%s' "$out" | awk '/^STEP [0-9]/{s=$0} /✘ FAIL|FAIL:/{if(s) print s; else print "Preparation or setup"}')"
      echo "────────────────────────────────────────────────────────────────"
      printf '%s\n' "$out"
    } > "$faillog"
    echo "  ✘ FAIL (${demo})  →  wrote ${faillog#"$ROOT"/}"
    { echo "RESULT for ${demo}: FAIL (see FAIL-${module}-${demo}.log)"; echo; } >> "$EVIDENCE"
    if [ "$diagnosed" -eq 0 ]; then
      run_logged "$ROOT/runtime/scripts/preflight_diagnose.sh" || true
      diagnosed=1
    fi
  fi
  if [ "$rc" -ge 128 ]; then
    echo "Course preflight interrupted; remaining demos were not run."
    exit "$rc"
  fi
  echo
done

if [ "$total" -eq 0 ]; then
  echo "No demo matched the requested scope${FILTER:+ (filter: $FILTER)}."
  { echo "No demo matched the requested scope."; } >> "$EVIDENCE"
  exit 2
fi

summary="COURSE PREFLIGHT SUMMARY · ${total} demo(s): ${passed} passed, ${failed} failed"
echo "$summary"
{ echo "────────────────────────────────────────────────────────────────"; echo "$summary"; } >> "$EVIDENCE"
echo "Run evidence: ${EVIDENCE#"$ROOT"/} (retained on failure; removed/restored after total success)"
if [ "$failed" -gt 0 ]; then
  echo "Course preflight did NOT pass. A student must not start: fix the demos named in the FAIL-*.log files, then re-run."
  echo "Per-failure logs:"; for f in "$ROOT"/FAIL-*.log; do [ -f "$f" ] && echo "    ${f#"$ROOT"/}"; done
else
  echo "Course preflight PASSED. Every selected demo completed all four checks; recording cleanup follows only after this complete scope succeeds."
fi
exit "$course_rc"
