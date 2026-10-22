#!/usr/bin/env bash
# Whole-course preflight: run EVERY module's EVERY demo, step by step, in the exact order and the
# exact output format a recorder would see, so you confirm the entire course in one command instead
# of testing each demo by hand.
#
#   ./lab preflight --all            (from the repo root; same as calling this script)
#   runtime/scripts/preflight_course.sh [REPO_ROOT]
#
# What it writes (at the repo root, so you can hand them straight back):
#   course-evidence.txt      one text file with every demo's four steps and their real output,
#                            grouped module by module, demo by demo. This is the evidence a student
#                            or recorder reads before starting: if it is all PASS, the course runs.
#   FAIL-<module>-<demo>.log a separate log written ONLY for a demo that failed, named so you can see
#                            at a glance which module and demo broke. It holds that demo's full output
#                            and the failing step, and it is exactly what to hand back to fix the step.
#
# Exit code is non-zero if any demo failed, so CI (and a student) can treat "course did not pass" as a
# hard stop: if this fails, do not start recording. A demo whose taught file is not authored on the
# current branch is reported as SKIPPED (author it, or run on the integration branch), never a failure.
set -uo pipefail

ROOT="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$ROOT" || exit 2

EVIDENCE="$ROOT/course-evidence.txt"
runner="$ROOT/runtime/scripts/preflight_all_steps.sh"
[ -x "$runner" ] || { echo "cannot find preflight_all_steps.sh" >&2; exit 2; }

# Start clean: one evidence file per course run, and no stale FAIL logs from an earlier run.
rm -f "$ROOT"/FAIL-*.log
: > "$EVIDENCE"
{
  echo "COURSE PREFLIGHT · every module, every demo, every step, in recorder order"
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "Evidence is restricted to the authorized local Globomantics application."
  echo
} >> "$EVIDENCE"

total=0; passed=0; failed=0; skipped=0; course_rc=0

# demos/module1-demos/m1-demo1-... before module2, m1-demo1 before m1-demo2: plain sort is the right order.
while IFS= read -r stepsdir; do
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

  # Capture the demo's full preflight output once; tee into the evidence file and keep it for a FAIL log.
  out="$("$runner" "$demo_dir" 2>&1)"; rc=$?
  printf '%s\n\n' "$out" >> "$EVIDENCE"

  if printf '%s' "$out" | grep -q "AUTHOR THIS FIRST"; then
    skipped=$((skipped+1))
    echo "  ⏭️  SKIPPED (${demo}: a taught file is not authored on this branch; run on the integration branch)"
    { echo "RESULT for ${demo}: SKIPPED (taught file not authored on this branch)"; echo; } >> "$EVIDENCE"
  elif [ "$rc" -eq 0 ]; then
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
      echo "Failing step(s): $(printf '%s' "$out" | grep -oE 'STEP [0-9]+ · command: [^ ]+' | tail -0; printf '%s' "$out" | awk '/^STEP [0-9]/{s=$0} /✘ FAIL/{print s}')"
      echo "────────────────────────────────────────────────────────────────"
      printf '%s\n' "$out"
    } > "$faillog"
    echo "  ✘ FAIL (${demo})  →  wrote ${faillog#"$ROOT"/}"
    { echo "RESULT for ${demo}: FAIL (see FAIL-${module}-${demo}.log)"; echo; } >> "$EVIDENCE"
  fi
  echo
done < <(find "$ROOT"/demos -type d -name steps | sort)

summary="COURSE PREFLIGHT SUMMARY · ${total} demo(s): ${passed} passed, ${failed} failed, ${skipped} skipped"
echo "$summary"
{ echo "────────────────────────────────────────────────────────────────"; echo "$summary"; } >> "$EVIDENCE"
echo "Evidence written to: ${EVIDENCE#"$ROOT"/}"
if [ "$failed" -gt 0 ]; then
  echo "Course preflight did NOT pass. A student must not start: fix the demos named in the FAIL-*.log files, then re-run."
  echo "Per-failure logs:"; for f in "$ROOT"/FAIL-*.log; do [ -f "$f" ] && echo "    ${f#"$ROOT"/}"; done
else
  echo "Course preflight PASSED. Every authored demo runs end to end; the course is safe to start."
fi
exit "$course_rc"
