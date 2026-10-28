"""Display local paths from the module folder; never change filesystem paths."""
from pathlib import Path
import re

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def display_text(text: str) -> str:
    """Shorten checkout paths BEFORE wrapping terminal fields.

    /checkout/demos/module2-demos/demo/logs/report.json becomes
    module2-demos/demo/logs/report.json. Other checkout files remain relative
    to the repository root. The operation is idempotent so CLI arguments and
    JSON field values can pass through the same shared formatter safely.
    """
    text = str(text)
    root = re.escape(str(REPOSITORY_ROOT))
    # The module folder is the display root for every current and future demo.
    text = re.sub(r'(?<![\w/])' + root + r'/(?:demos/)?', '', text)
    text = re.sub(r'(?<![\w/])demos/(?=(?:module[^/\s]*|m\d+)[/\\])', '', text)
    # Outside this checkout, hide only the personal home prefix. URLs and
    # container paths such as /tmp/report.json are not local checkout paths.
    text = re.sub(r'(?<![\w/])/(?:Users|home)/[^/\s]+(?=/|$)', '~', text)
    return text
