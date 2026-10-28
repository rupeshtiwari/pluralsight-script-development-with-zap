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

from terminal_paths import display_text, display_command

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
    "focus":    "pink",         # primary Transform Pink: one precise on-screen value
    "pass":     "green",        # a check that passed
    "fail":     "red",          # a check that failed (stop red; never decorative)
    "todo":     "yellow",       # a learner-authored deliverable not written yet (NOT a failure)
    "fix":      "orange",       # the suggested fix / prompt
    "muted":    "gray_medium",  # secondary text (the WHY line, notes, reasons)
    "emphasis": "pink",         # reserved for important emphasis (used sparingly)
}
_USE_COLOR = sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1"

# Fixed, deterministic table geometry so the terminal render and the README render match exactly,
# and so a long value WRAPS onto aligned continuation lines instead of being truncated or overflowing.
# The editor boxes values, so each row is followed by one blank line of padding to box into.
LABEL_WIDTH = 40
VALUE_WIDTH = 60


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
    print(_w("header", "  ★ │ " + "OBSERVED FIELD".ljust(40) + " │ " + "ACTUAL VALUE"))


def _wrap_value(value: str, width: int):
    """Word-wrap a value to `width`, hard-breaking any single token longer than the column
    (HTML and payloads have no spaces), so nothing is ever truncated."""
    out, line = [], ""
    for word in value.split(" "):
        while len(word) > width:
            if line:
                out.append(line)
                line = ""
            out.append(word[:width])
            word = word[width:]
        if not line:
            line = word
        elif len(line) + 1 + len(word) <= width:
            line += " " + word
        else:
            out.append(line)
            line = word
    out.append(line)
    return out or [""]


def star(label: str, value: str, focus: bool = False) -> None:
    """Aligned field/value row that shows the FULL value, with the `│` separator ALWAYS at the same
    column so the table never misaligns, whatever the label or value length.

    BOTH columns wrap: a label longer than LABEL_WIDTH and a value longer than VALUE_WIDTH each flow
    onto continuation lines within their own column, so the separator stays put and nothing is
    truncated. One blank padding line follows the row so the editor can box a value cleanly. The
    geometry is fixed (LABEL_WIDTH / VALUE_WIDTH) so the terminal and the README match. Continuation
    lines keep both gutters, so the evidence parser can rejoin label and value.
    """
    label, value = display_text(label).strip(), display_text(value)
    color = "focus" if focus else "value"
    sep = _w("header", " │ ")
    lab_chunks = _wrap_value(label, LABEL_WIDTH)
    val_chunks = _wrap_value(value, VALUE_WIDTH)
    for i in range(max(len(lab_chunks), len(val_chunks))):
        lab = lab_chunks[i] if i < len(lab_chunks) else ""
        val = val_chunks[i] if i < len(val_chunks) else ""
        mark = "  ★ │ " if i == 0 else "    │ "
        print(_w("header", mark) + _w("label", f"{lab:<{LABEL_WIDTH}}") + sep + _w(color, val))
    print()  # one blank line of padding, so the editor can box the value without touching the next row


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


def todo(msg: str, reason: str = "", fix: str = "", try_cmd: str = "") -> None:
    """A learner-authored deliverable has not been written yet. This is the demo's own work on the
    `-before` branch, NOT a broken repo, so it is a teaching moment, rendered in brand yellow and never
    in Stop Red (which is reserved strictly for a real failed check). The banner says plainly that this
    is expected, teaches why it appears, and gives the next action: author it (the README step shows the
    code), or bring the whole file in with the one-line `try_cmd` copy, which stays on THIS branch (it
    does not switch branches). Then re-run the same step and it passes."""
    print(f"{_w('todo', '✍️  AUTHOR THIS FIRST')}  {msg}")
    print(f"        {_w('todo', '✅ this is EXPECTED on the -before branch, not an error')} "
          f"{_w('muted', '— writing this file is the demo itself.')}")
    if reason:
        print(f"        {_w('muted', '💡 why you see it: ')}{reason}")
    if fix:
        print(f"        {_w('fix', '✍️  how to author it (you learn it): ')}{_w('fix', fix)}")
    if try_cmd:
        print(f"        {_w('header', '⚡ or bring the whole file in with one command (stays on this branch):')}")
        print(f"        {_w('header', try_cmd)}")
        print(f"        {_w('muted', '↻ then run this SAME step again, and it passes.')}")


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
        print("usage: fmt.py {header|star|section|item|ok|fail|todo|note|json} ...", file=sys.stderr)
        return 2
    cmd, args = argv[0], [display_text(arg) for arg in argv[1:]]
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
    elif cmd == "todo":
        # The 4th arg is a RUNNABLE copy command; keep its full repo-relative path (demos/...) so it
        # works when pasted. Only hide a home prefix (owner rule F); never shorten the path itself.
        try_cmd = display_command(argv[4]) if len(argv) > 4 else ""
        todo(args[0], args[1] if len(args) > 1 else "", args[2] if len(args) > 2 else "", try_cmd)
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
