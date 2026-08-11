"""Assemble the completed chapter 5--8 main-body components only.

Training and answer components are intentionally absent: their classification
and final placement begin only after the complete handout body is stable.
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools import (
    build_chapter_05_filter_structures_mathjax_component as chapter_five,
    build_chapter_06_iir_design_mathjax_component as chapter_six,
    build_chapter_07_fir_design_mathjax_component as chapter_seven,
    build_chapter_08_multirate_mathjax_component as chapter_eight,
)
from full.tools.render_mathjax_formula import MATHJAX


COMPONENTS = (chapter_five, chapter_six, chapter_seven, chapter_eight)

STYLE = r"""
<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
h1{break-before:page;break-after:avoid;color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}
h1:first-child{break-before:auto}
h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}
p{margin:5pt 0 8pt}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
figure{break-inside:avoid;margin:12pt auto;text-align:center}
svg{max-width:100%;height:auto}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>
"""


def _main_body(html: str) -> str:
    match = re.search(r"<main(?:\s[^>]*)?>(.*)</main>", html, flags=re.DOTALL)
    if not match:
        raise ValueError("chapter body component is missing a main container")
    return match.group(1)


def _combined_body() -> str:
    with tempfile.TemporaryDirectory(prefix="dsp-chapter-05-to-08-") as directory:
        root = Path(directory)
        bodies = []
        for component in COMPONENTS:
            html = component.write_html(root / f"{component.__name__.split('.')[-1]}.html")
            bodies.append(_main_body(html.read_text(encoding="utf-8")))
    return "\n".join(bodies)


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = (
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<script>window.MathJax={tex:{packages:{"[+]": ["ams"]}}};</script>'
        f'<script defer src="{MATHJAX}"></script>{STYLE}<body><main>'
        f"{_combined_body()}</main></body></html>"
    )
    output.write_text(document, encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_html(ROOT / "full" / "outputs" / "chapter_05_to_08_body.html"))
