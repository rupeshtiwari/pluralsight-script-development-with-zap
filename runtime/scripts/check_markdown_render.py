#!/usr/bin/env python3
"""Find Markdown that GitHub will show as literal text because it sits inside an HTML block.

GitHub (CommonMark/GFM) starts an HTML block at a line that opens with a block tag
such as <details>, </details>, <table> or <div>, and keeps everything up to the next
BLANK line as raw HTML. A heading, list, table row, bold text or code fence placed
directly under such a line (for example "</details>" then "## Step 2") renders as
plain text like "## Step 2". Fix: put a blank line between them.

    python3 check_markdown_render.py FILE_OR_DIR [...]      # exit 1 when any issue is found
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BLOCK_TAGS = ('address|article|aside|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|'
              'fieldset|figcaption|figure|footer|form|h[1-6]|head|header|hr|html|legend|li|link|main|menu|nav|ol|'
              'p|section|summary|table|tbody|td|tfoot|th|thead|title|tr|ul')
OPENS_BLOCK = re.compile(r'^ {0,3}</?(?:' + BLOCK_TAGS + r')(?:[\s/>]|$)', re.I)
ONLY_TAGS = re.compile(r'^ {0,3}(?:</?[A-Za-z][A-Za-z0-9-]*(?:\s[^<>]*)?/?>\s*)+$')
MARKDOWN = re.compile(r'^ {0,3}(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|\||\*\*|```|~~~|>\s)')
FENCE = re.compile(r'^ {0,3}(```|~~~)')


def issues(text: str):
    found, in_html, fence, prev = [], False, None, ''
    for number, line in enumerate(text.splitlines(), 1):
        if fence:
            if line.strip().startswith(fence):
                fence = None
            prev = line
            continue
        if not line.strip():
            in_html = False
        elif in_html and MARKDOWN.match(line):
            found.append((number, line.strip(), prev.strip()))
            in_html = False
        elif not in_html and (OPENS_BLOCK.match(line) or (ONLY_TAGS.match(line) and not prev.strip())):
            in_html = True
        if not in_html:
            match = FENCE.match(line)
            if match:
                fence = match.group(1)
        prev = line
    return found


def main(argv) -> int:
    total = 0
    for arg in argv or ['.']:
        root = Path(arg)
        files = [root] if root.is_file() else sorted(p for p in root.rglob('*.md') if '.git' not in p.parts)
        for path in files:
            for number, line, prev in issues(path.read_text(encoding='utf-8')):
                total += 1
                print(f'{path}:{number}: renders as literal text after HTML line {prev[:40]!r}: {line[:80]}')
    print(('FAIL' if total else 'PASS') + f': {total} Markdown line(s) trapped inside HTML blocks')
    return 1 if total else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
