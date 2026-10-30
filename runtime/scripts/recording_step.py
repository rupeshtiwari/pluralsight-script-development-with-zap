#!/usr/bin/env python3
"""Record a freshly executed demo step and fail on presentation-output drift.

Reference and filmed executions always run the SAME named-step engine. The raw
output is retained unchanged; only run-unique identifiers and telemetry counts
are normalized on the terminal and in the narration transcript. Security facts,
alert risk, HTTP codes, process exit and PASS/FAIL are never replaced.
"""
from __future__ import annotations
import difflib
import os
from pathlib import Path
import re
import subprocess
import sys
from terminal_paths import display_command, display_text

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
MARKER = re.compile(r"(?<=marker-)[0-9A-Za-z._-]{5,}")
TIMESTAMP = re.compile(r"\b20\d\d-\d\d-\d\d[T ][0-9:.+Z-]+\b")
SCAN_ID = re.compile(r"\bid=\d+\b")
# These metrics are recorded exactly in the raw audit log, but are intentionally
# not safe for narrator scripts because a fresh scan can yield a different count.
LIVE_COUNTER = re.compile(
    r"((?:Requests the scan sent|Probe requests the scan sent)(?::\s*|\s+│\s*))\d+"
)
INSIGHT_STAT = re.compile(r"(Statistic · meaning(?::\s*|\s+│\s*))\d+(?=\s|$)")


def canonical(line: str) -> str:
    # Native formatter already shortens artifact fields. Preserve runnable repair
    # commands (notably their demos/ git paths) while hiding personal homes.
    line = display_command(ANSI.sub("", line))
    # Initial plan priming depends on whether this session has scan state.
    # It is still recorded byte-for-byte in the raw audit output.
    if line.lstrip().startswith("Priming:"):
        return ""
    line = MARKER.sub("<live-request-id>", line)
    line = TIMESTAMP.sub("<live-timestamp>", line)
    line = SCAN_ID.sub("id=<live-scan-id>", line)
    line = LIVE_COUNTER.sub(r"\g<1><live-count-in-raw-log>", line)
    line = INSIGHT_STAT.sub(r"\g<1><live-value-in-raw-log>", line)
    return line


def main() -> int:
    if len(sys.argv) < 5:
        print("usage: recording_step.py DEMO_DIR STEP NATIVE_RUNNER NUMBER", file=sys.stderr)
        return 2
    demo = Path(sys.argv[1]).resolve()
    step = sys.argv[2]
    cmd = sys.argv[3:]
    if step not in {"1", "2", "3", "4"} or not (demo / "scripts").is_dir():
        print("ERROR: invalid demo directory or step", file=sys.stderr)
        return 2
    phase = os.getenv("DEMO_SYNC_PHASE", "compare")
    if phase not in {"reference", "compare"}:
        print("ERROR: DEMO_SYNC_PHASE must be reference or compare", file=sys.stderr)
        return 2

    logs = demo / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    proof = logs / ".producer"
    proof.mkdir(exist_ok=True)
    stem = "step-%02d" % int(step)
    reference = logs / ("preflight-" + stem + ".log")
    display_file = (proof / ("reference-" + stem + "-candidate.log")) if phase == "reference" else (logs / ("recorded-" + stem + ".log"))
    raw_file = proof / (("reference-" if phase == "reference" else "recorded-") + stem + ".raw.log")
    if phase == "compare" and not reference.is_file():
        print(display_text("SYNC HOLD: no preflight baseline at %s" % reference), file=sys.stderr)
        print("Run the complete preflight on the matching completed source state, "
              "then share the four preflight-step logs with the recorder.", file=sys.stderr)
        return 1

    env = os.environ.copy()
    env.pop("DEMO_SYNC_MODE", None)
    env.pop("DEMO_SYNC_PHASE", None)
    env["FORCE_COLOR"] = "0"
    rendered: list[str] = []
    with raw_file.open("w", encoding="utf-8") as raw:
        child = subprocess.Popen(
            cmd, cwd=demo, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, errors="replace", bufsize=1,
        )
        assert child.stdout is not None
        for line in child.stdout:
            raw.write(line)
            normalized = canonical(line)
            rendered.append(normalized)
            sys.stdout.write(normalized)
            sys.stdout.flush()
        status = child.wait()
    data = "".join(rendered)
    display_file.write_text(data, encoding="utf-8")
    if status != 0 or "✔ PASS" not in data or "✘ FAIL" in data:
        print(display_text("SYNC HOLD: underlying step failed or did not prove PASS; raw output: %s" % raw_file), file=sys.stderr)
        return status or 1
    if phase == "reference":
        # A narration reference exists only after actual successful execution.
        reference.write_text(data, encoding="utf-8")
        return 0

    expected = reference.read_text(encoding="utf-8")
    if data != expected:
        diff = list(difflib.unified_diff(
            expected.splitlines(), data.splitlines(),
            fromfile="preflight/"+stem, tofile="recording/"+stem, lineterm=""
        ))
        mismatch = proof / (stem + "-mismatch.diff")
        mismatch.write_text("\n".join(diff) + "\n", encoding="utf-8")
        print("SYNC MISMATCH: recording output differs from the verified preflight.", file=sys.stderr)
        print(display_text("Compare %s with %s; see %s" % (reference, display_file, mismatch)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
