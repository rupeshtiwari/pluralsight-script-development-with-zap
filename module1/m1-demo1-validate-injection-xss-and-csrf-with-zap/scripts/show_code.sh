#!/bin/bash
# OPTIONAL reference — NOT a recorded demo step.
#
# Shows the exact vulnerable line(s) in app/main.py behind a finding, so a
# beginner can see *why* it is exploitable. Snippets are read live from the
# source, so they can never drift from the running app.
#
#   ./scripts/show_code.sh sqli     # SQL injection (product search)
#   ./scripts/show_code.sh nosql    # NoSQL injection (account lookup)
#   ./scripts/show_code.sh cmd      # command injection (admin ping)
#   ./scripts/show_code.sh xss      # reflected XSS (greeting)
#   ./scripts/show_code.sh csrf     # CSRF (email change)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${HERE}/../../.." && pwd)"
SRC="${REPO_ROOT}/app/main.py"
FMT="${REPO_ROOT}/scripts/fmt.py"
fm() { python3 "${FMT}" "$@"; }

case "${1:-}" in
    sqli)  ANCHOR="VULNERABLE: query built by string concatenation."; N=5; TITLE="SQL injection · product search";;
    nosql) ANCHOR="VULNERABLE: the query string is parsed qs-style";  N=15; TITLE="NoSQL injection · account lookup";;
    cmd)   ANCHOR="VULNERABLE: host interpolated into a shell command"; N=5; TITLE="Command injection · admin ping";;
    xss)   ANCHOR="VULNERABLE: raw reflection into HTML body";        N=4; TITLE="Reflected XSS · greeting";;
    csrf)  ANCHOR="VULNERABLE: token presence/validity is checked";   N=4; TITLE="CSRF · email change";;
    *) echo "usage: show_code.sh {sqli|nosql|cmd|xss|csrf}"; exit 2;;
esac

fm header "Vulnerable code — ${TITLE}" \
          "The line(s) that make the app exploitable — this is why ZAP's alert fired."
echo
# Line numbers so you can jump straight to it in the editor (VS Code: Ctrl+G).
awk -v a="${ANCHOR}" -v n="${N}" '
    index($0, a) { printf "  %4d  %s\n", NR, $0;
                   c = n; while (c-- > 0) { if (getline <= 0) break; printf "  %4d  %s\n", NR, $0 } exit }
' "${SRC}"
echo
fm note "Source: app/main.py  ·  in VS Code: Cmd+P -> main.py, then Ctrl+G -> the line above."
fm note "The remediated build fixes exactly these lines."
