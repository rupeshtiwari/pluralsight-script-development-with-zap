#!/bin/bash
# One-shot diagnostic for the m2-demo1 authenticated AF run.
# Prints exactly what ZAP saw so we can pinpoint why the authenticated
# reflection is not reached. Paste the whole output back.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${HERE}/../../.." && pwd)"
# shellcheck disable=SC1091
[ -f "${REPO_ROOT}/.env" ] && source "${REPO_ROOT}/.env"
ZAP="http://localhost:8090"
K="${ZAP_API_KEY:-}"
APP="http://app:8000"
enc() { python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=""))' "$1"; }
j() { python3 -m json.tool 2>/dev/null || cat; }

echo "============================================================"
echo "1. PLAN PROGRESS (info / warn / error from a FRESH AF run)"
echo "============================================================"
# Run a fresh plan and capture ITS id. ZAP increments the plan id per run,
# so we must read back the id runPlan returns, not a hardcoded one.
PID="$(curl -s "${ZAP}/JSON/automation/action/runPlan/?apikey=${K}&filePath=$(enc "/af/af-plan.yaml")" \
  | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("planId",""))
except Exception: print("")')"
echo "  planId: ${PID:-<none>}"
# Wait for it to finish (up to ~4 min).
for _ in $(seq 1 80); do
  done="$(curl -s "${ZAP}/JSON/automation/view/planProgress/?apikey=${K}&planId=${PID}" \
    | python3 -c 'import json,sys
try: print(1 if (json.load(sys.stdin).get("finished") or "").strip() else 0)
except Exception: print(0)')"
  [ "${done}" = "1" ] && break
  sleep 3
done
curl -s "${ZAP}/JSON/automation/view/planProgress/?apikey=${K}&planId=${PID}" | python3 -c '
import json,sys
try: d=json.load(sys.stdin)
except Exception as e: print("  (no plan progress:", e, ")"); raise SystemExit
for k in ("started","finished","error","warn","info"):
    v=d.get(k)
    if isinstance(v,list):
        print("  %-8s (%d):" % (k, len(v)))
        for m in v: print("      -", m)
    else:
        print("  %-8s: %s" % (k, v))'

echo
echo "============================================================"
echo "2. SITES TREE — is the authenticated profile node present?"
echo "============================================================"
curl -s "${ZAP}/JSON/core/view/urls/?apikey=${K}&baseurl=$(enc "${APP}")" | python3 -c '
import json,sys
try: urls=json.load(sys.stdin).get("urls",[])
except Exception: urls=[]
prof=[u for u in urls if "/account/profile" in u]
print("  total urls in tree:", len(urls))
print("  profile nodes:")
for u in prof: print("      -", u)
if not prof: print("      (none — the active scan had no profile node to attack)")'

echo
echo "============================================================"
echo "3. ALERTS recorded on /account/profile"
echo "============================================================"
curl -s "${ZAP}/JSON/core/view/alerts/?apikey=${K}&baseurl=$(enc "${APP}/account/profile")" | python3 -c '
import json,sys
try: al=json.load(sys.stdin).get("alerts",[])
except Exception: al=[]
if not al: print("  (no alerts on /account/profile)")
for a in al: print("      - %s | param=%s | risk=%s" % (a.get("alert") or a.get("name"), a.get("param"), a.get("risk")))'

echo
echo "============================================================"
echo "3b. CUSTOM ALERT present in ZAP's store? (what the GUI shows)"
echo "    Unfiltered, matched by name across ALL urls."
echo "============================================================"
curl -s "${ZAP}/JSON/core/view/alerts/?apikey=${K}" | python3 -c '
import json,sys
try: al=json.load(sys.stdin).get("alerts",[])
except Exception: al=[]
names=[(a.get("alert") or a.get("name") or "") for a in al]
print("  total alerts in store:", len(names))
hits=[(a.get("alert") or a.get("name"), a.get("url"), a.get("param")) for a in al if "Globomantics" in ((a.get("alert") or a.get("name")) or "")]
if hits:
    print("  CUSTOM ALERT FOUND (GUI Alerts tab will show it):")
    for n,u,p in hits: print("      >> %s | url=%s | param=%s" % (n,u,p))
else:
    print("  CUSTOM ALERT: NOT in the store (GUI Alerts tab would be empty for it).")
    print("  distinct alert names present:")
    for n in sorted(set(names)): print("      -", n)'

echo
echo "============================================================"
echo "4. DIRECT AUTH TEST (host -> app, bypassing ZAP) — does"
echo "   login + note reflect? Confirms the app itself is fine."
echo "============================================================"
CID="$(docker ps --format '{{.Names}}' | grep -E 'zap' | head -1)"
if [ -n "${CID}" ]; then
  echo "  running from inside the ZAP container (${CID}) so app:8000 resolves:"
  docker exec "${CID}" sh -c '
    C=$(curl -s -i -X POST http://app:8000/login --data "username=alice" | grep -i "^set-cookie:" | sed -E "s/.*session=([^;]+).*/\1/I" | tr -d "\r" | head -1)
    echo "    login cookie: ${C:-<none>}"
    echo "    no-cookie  /account/profile?note=seed -> HTTP $(curl -s -o /dev/null -w "%{http_code}" "http://app:8000/account/profile?note=seed")"
    echo "    with-cookie profile body (Note line):"
    curl -s -b "session=$C" "http://app:8000/account/profile?note=XSSPROBE123" | grep -i "note:" | sed "s/^/      /"
  '
else
  echo "  (no ZAP container found; is the stack up?)"
fi
echo "============================================================"
echo "Done. Paste everything above."
