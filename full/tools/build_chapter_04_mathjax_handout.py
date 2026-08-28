"""Assemble the chapter-four main handout body in original source order."""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

from full.tools import build_chapter_04_dif_ifft_optimization_mathjax_component as dif_ifft
from full.tools import build_chapter_04_dft_efficiency_mathjax_component as efficiency
from full.tools import build_chapter_04_dit_fft_mathjax_component as dit
from full.tools.render_mathjax_formula import MATHJAX


BODY_COMPONENTS = (efficiency, dit, dif_ifft)

STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt;break-after:avoid}
h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}
p{margin:5pt 0 8pt;orphans:3;widows:3}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.counts,.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt}
.counts th,.counts td,.table th,.table td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:center}
.counts th,.table th{color:#315d7c;font-weight:500;background:#f4f7f8}
.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}
.source-figure{break-inside:avoid;margin:12pt auto;text-align:center}.source-figure img{display:block;max-width:100%;height:auto;margin:0 auto}.source-figure figcaption{margin-top:4pt;color:#52616b;font-size:9.5pt}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.counts,.table{font-size:9.5pt}}
</style>"""


def _main_body(document: str) -> str:
    match = re.search(r"<main>(.*)</main>", document, flags=re.DOTALL)
    if match is None:
        raise ValueError("component does not contain a main element")
    return match.group(1).strip()


def _document(content: str) -> str:
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{content}</main></html>'''


def write_html(output: Path) -> Path:
    """Write chapter four's body only; question material remains frozen for later."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="chapter-04-components-") as temporary:
        directory = Path(temporary)
        parts = []
        for index, component in enumerate(BODY_COMPONENTS, start=1):
            intermediate = directory / f"body-{index}.html"
            document = component.write_html(intermediate).read_text(encoding="utf-8")
            parts.append(_main_body(document))
    output.write_text(_document("\n\n".join(parts)), encoding="utf-8")
    return output
