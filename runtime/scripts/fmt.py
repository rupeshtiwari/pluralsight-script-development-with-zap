#!/usr/bin/env python3
"""Colored output formatter for the Globomantics ZAP demos.

Every demo script prints through this one module so that all on-screen output
shares one look: boxed headers that say *what* you are seeing and *why*, the
"star" line format (one highlighted line, one blank line), and consistent
PASS / FAIL / FIX styling.

------------------------------------------------------------------------------
COLOR PALETTE  --  official Pluralsight brand colors (24-bit true color).
------------------------------------------------------------------------------
macOS Terminal supports 24-bit (true) color, so each role is rendered with the
exact brand hex rather than an approximate 256-color code. Change a role's color
by re-pointing it in PALETTE to a BRAND key; nothing else in any script changes.

Hex values are the official Pluralsight palette verified against Keynote Template
2026.07.b. Stop red is reserved strictly for a failed check (never decorative).
"""
import json
import os
import sys

# --- Official Pluralsight brand palette (R, G, B), verified against the ------
#     Keynote Template 2026.07.b style guide.
BRAND = {
    "pink":        (255, 22, 117),   # #FF1675 Transform Pink (primary)
    "inky":        (19, 15, 37),     # #130F25 Inky Blue (primary dark)
    "blue":        (0, 163, 255),    # #00A3FF Blue
    "purple":      (119, 14, 247),   # #770EF7 Purple
    "yellow":      (255, 201, 66),   # #FFC942 Yellow
    "orange":      (255, 123, 1),    # #FF7B01 Orange
    "green":       (2, 224, 136),    # #02E088 Green
    "gray_dark":   (27, 24, 52),     # #1B1834 Gray (dark)
    "gray_medium": (88, 95, 162),    # #585FA2 Gray (medium)
    "gray_light":  (235, 239, 245),  # #EBEFF5 Gray (light)
    "red":         (185, 0, 75),     # #B9004B Stop Red (failed check only)
}

# --- Role -> brand color (None = default terminal text) ---------------------
PALETTE = {
    "header":   "blue",         # box borders + WHAT title
    "label":    "purple",       # the label part of a star line (names / identifiers)
    "value":    None,           # the value part of a star line (default text, high contrast)
    "focus":    "yellow",       # the ONE field we want the audience to read
    "pass":     "green",        # a check that passed
    "fail":     "red",          # a check that failed (stop red; never decorative)
    "fix":      "orange",       # the suggested fix / prompt
    "muted":    "gray_medium",  # secondary text (the WHY line, notes, reasons)
    "emphasis": "pink",         # reserved for important emphasis (used sparingly)
}
_USE_COLOR = sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1"


def _w(name: str, text: str) -> str:
    """Render text in the brand color bound to a role (true color)."""
    if not _USE_COLOR:
        return text
    key = PALETTE.get(name)
    if key is None:
        return text
    r, g, b = BRAND[key]
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


# --- Public helpers ---------------------------------------------------------
def header(what: str, why: str = "", width: int = 74) -> None:
    """A boxed header: WHAT we are showing and WHY we are showing it."""
    line = "─" * (width - 2)
    print(_w("header", f"┌{line}┐"))
    for row in _wrap(f"WHAT:  {what}", width - 4):
        print(_w("header", "│ ") + row.ljust(width - 4) + _w("header", " │"))
    if why:
        for row in _wrap(f"WHY:   {why}", width - 4):
            print(_w("header", "│ ") + _w("muted", row.ljust(width - 4)) + _w("header", " │"))
    print(_w("header", f"└{line}┘"))


def star(label: str, value: str, focus: bool = False) -> None:
    """A single highlighted line in the mandated star format.

    Prints:  ★ <label>: <value>   followed by one blank line.
    When focus=True the value is drawn in the focus color (the field the
    author reads aloud). Values are never truncated.
    """
    bullet = _w("focus" if focus else "header", "★")
    lab = _w("label", f"{label}:")
    val = _w("focus" if focus else "value", value)
    print(f"  {bullet} {lab} {val}")
    print()


def section(title: str) -> None:
    print(_w("header", f"{title}:"))
    print()


def item(text: str, focus: bool = False) -> None:
    bullet = _w("focus" if focus else "header", "★")
    body = _w("focus" if focus else "value", text)
    print(f"  {bullet} {body}")
    print()


def ok(msg: str) -> None:
    print(f"{_w('pass', '✔ PASS')}  {msg}")


def bad(msg: str, reason: str = "", fix: str = "") -> None:
    print(f"{_w('fail', '✘ FAIL')}  {msg}")
    if reason:
        print(f"        {_w('muted', 'why: ')}{reason}")
    if fix:
        print(f"        {_w('fix', 'fix: ')}{_w('fix', fix)}")


def note(text: str) -> None:
    print(_w("muted", text))


def _wrap(text: str, width: int):
    words, line, out = text.split(), "", []
    for word in words:
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    out.append(line)
    return out or [""]


# --- CLI so bash scripts can call the same formatter ------------------------
def _main(argv) -> int:
    if not argv:
        print("usage: fmt.py {header|star|section|item|ok|fail|note|json} ...", file=sys.stderr)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "header":
        header(args[0], args[1] if len(args) > 1 else "")
    elif cmd == "star":
        star(args[0], args[1], focus=(len(args) > 2 and args[2] == "focus"))
    elif cmd == "section":
        section(args[0])
    elif cmd == "item":
        item(args[0], focus=(len(args) > 1 and args[1] == "focus"))
    elif cmd == "ok":
        ok(args[0])
    elif cmd == "fail":
        bad(args[0], args[1] if len(args) > 1 else "", args[2] if len(args) > 2 else "")
    elif cmd == "note":
        note(args[0])
    elif cmd == "json":
        # json <focus_key,focus_key,...>  -- reads JSON on stdin, prints each
        # requested field as a star line; focus keys use the focus color.
        focus_keys = set(args[0].split(",")) if args else set()
        keys = args[1].split(",") if len(args) > 1 else None
        data = json.load(sys.stdin)
        rows = data if isinstance(data, list) else [data]
        for row in rows:
            for key, val in row.items():
                if keys and key not in keys:
                    continue
                star(key, json.dumps(val) if isinstance(val, (dict, list)) else str(val),
                     focus=(key in focus_keys))
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    try:
        _rc = _main(sys.argv[1:])
    except BrokenPipeError:
        # A downstream reader (e.g. `| head`) closed the pipe. Exit quietly
        # instead of dumping a traceback.
        try:
            sys.stdout.close()
        except Exception:
            pass
        _rc = 0
    raise SystemExit(_rc)
