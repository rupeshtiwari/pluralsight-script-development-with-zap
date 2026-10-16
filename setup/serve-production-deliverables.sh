#!/usr/bin/env bash
# Local-only, dependency-free viewer. Runs in the foreground; Ctrl+C stops it.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$HERE"
if [[ $# -gt 0 && -d "$1" ]]; then ROOT="$(cd "$1" && pwd)"; shift; fi
PORT="${1:-8765}"
if [[ ! "$PORT" =~ ^[0-9]{1,5}$ ]] || (( PORT < 1024 || PORT > 65535 )); then
  echo 'Usage: ./serve.sh [PORT 1024-65535] OR ./setup/serve-production-deliverables.sh BATCH_FOLDER [PORT]' >&2
  exit 2
fi
if [[ ! -f "$ROOT/index.html" || ! -f "$ROOT/manifest.json" ]]; then
  echo "Missing real batch index.html or manifest.json in: $ROOT" >&2
  echo 'Run ./setup/run-all-demo-preflights.sh on the recording Mac first.' >&2
  exit 1
fi
# The batch ZIP is portable: refresh uses bundled Python source and author notes.
# A newer narration-final.json becomes visible on each server launch.
if [[ -x "$ROOT/refresh.sh" ]]; then
  "$ROOT/refresh.sh"
fi
URL="http://127.0.0.1:${PORT}/index.html"
printf 'Serving local production proof only on %s\nSource folder: %s\nPress Ctrl+C to stop.\n' "$URL" "$ROOT"
( sleep 1; if command -v open >/dev/null 2>&1; then open "$URL" >/dev/null 2>&1 || true;
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL" >/dev/null 2>&1 || true; fi ) &
exec python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$ROOT"
