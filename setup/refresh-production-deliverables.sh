#!/usr/bin/env bash
# Rebuild HTML after a separate narration skill returns narration-final.json.
# No network calls and NO change to logs/manifests/recording artifacts.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[[ -f "$ROOT/manifest.json" ]] || { echo 'Missing real batch manifest.json' >&2; exit 1; }
[[ -f "$ROOT/tools/production_dashboard.py" && -d "$ROOT/author-playbooks" ]] || {
  echo 'Missing portable dashboard tools or bundled author playbooks' >&2
  exit 1
}
exec python3 "$ROOT/tools/production_dashboard.py" "$ROOT" --authors "$ROOT/author-playbooks"
