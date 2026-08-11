"""Assemble chapter two's main body without training or answer modules."""
from __future__ import annotations

import sys
import tempfile
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools import (
    build_chapter_02_dtft_mathjax_component as dtft,
    build_chapter_02_foundations_mathjax_component as foundations,
    build_chapter_02_inverse_properties_mathjax_component as inverse_properties,
    build_chapter_02_special_filters_mathjax_component as special_filters,
    build_chapter_02_system_frequency_mathjax_component as system_frequency,
)
from full.tools.build_chapter_05_to_08_body import STYLE, _main_body
from full.tools.render_mathjax_formula import MATHJAX


COMPONENTS = (foundations, inverse_properties, dtft, system_frequency, special_filters)

CHAPTER_TITLE = "第二章 z 变换与 LSI 系统频域分析"
HEADING_STYLE = "<style>h4{break-after:avoid;color:#315d7c;font-size:11.5pt;font-weight:400;margin:10pt 0 3pt}</style>"


def _demote_component_headings(body: str) -> str:
    """Keep one chapter title while preserving component heading hierarchy."""
    def replace(match: re.Match[str]) -> str:
        closing, level = match.group(1), int(match.group(2))
        return f"<{closing}h{level + 1}>"

    return re.sub(r"<(/?)h([1-3])>", replace, body)


def _combined_body() -> str:
    with tempfile.TemporaryDirectory(prefix="dsp-chapter-02-body-") as directory:
        temporary = Path(directory)
        bodies = []
        for component in COMPONENTS:
            path = component.write_html(temporary / f"{component.__name__.split('.')[-1]}.html")
            bodies.append(_demote_component_headings(_main_body(path.read_text(encoding="utf-8"))))
    return "\n".join(bodies)


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = (
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<script>window.MathJax={tex:{packages:{"[+]": ["ams"]}}};</script>'
        f'<script defer src="{MATHJAX}"></script>{STYLE}{HEADING_STYLE}<body><main>'
        f"<h1>{CHAPTER_TITLE}</h1>{_combined_body()}</main></body></html>"
    )
    output.write_text(document, encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_html(ROOT / "full" / "outputs" / "chapter_02_body.html"))
