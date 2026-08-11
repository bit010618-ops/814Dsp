"""Assemble reusable chapter-three body, training, and answer components."""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

from full.tools import build_chapter_03_dfs_mathjax_component as dfs
from full.tools import build_chapter_03_dft_mathjax_component as dft
from full.tools import build_chapter_03_frequency_sampling_mathjax_component as frequency_sampling
from full.tools import build_chapter_03_lsi_output_mathjax_component as lsi
from full.tools import build_chapter_03_spectrum_analysis_mathjax_component as spectrum_analysis
from full.tools import build_chapter_03_training_mathjax_component as training
from full.tools.render_mathjax_formula import MATHJAX


BODY_COMPONENTS = (dfs, dft, lsi, frequency_sampling, spectrum_analysis)

STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt;break-after:avoid}
h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}
p{margin:5pt 0 8pt;orphans:3;widows:3}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.note{color:#52616b;margin:4pt 0 8pt}
.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:15pt 0 10pt;break-after:avoid}
.writing-space{min-height:105mm}
.answer-step{break-inside:avoid;margin:8pt 0}.answer-step strong{color:#315d7c}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.exam-head{gap:8pt}}
</style>"""


def _main_body(document: str) -> str:
    match = re.search(r"<main>(.*)</main>", document, flags=re.DOTALL)
    if match is None:
        raise ValueError("component does not contain a main element")
    return match.group(1).strip()


def _document(content: str) -> str:
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{content}</main></html>'''


def _write_component(component: object, directory: Path, name: str, method: str = "write_html") -> str:
    output = directory / f"{name}.html"
    writer = getattr(component, method)
    return _main_body(writer(output).read_text(encoding="utf-8"))


def write_html(output: Path) -> Path:
    """Write the chapter body followed by its reusable question component."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="chapter-03-components-") as temporary:
        directory = Path(temporary)
        parts = [
            _write_component(component, directory, f"body-{index}")
            for index, component in enumerate(BODY_COMPONENTS, start=1)
        ]
        parts.append(_write_component(training, directory, "training", "write_training_html"))
    output.write_text(_document("\n\n".join(parts)), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    """Write only the book-end answer component for later total-book assembly."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="chapter-03-answers-") as temporary:
        content = _write_component(training, Path(temporary), "answers", "write_answers_html")
    output.write_text(_document(content), encoding="utf-8")
    return output
