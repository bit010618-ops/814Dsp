"""Assemble migrated chapter-two blocks into one naturally reflowed A4 document."""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools.render_mathjax_formula import EDGE, MATHJAX
from sample.tools import build_sample as page_style
from full.tools import (
    build_chapter_02_dtft_mathjax_component as dtft,
    build_chapter_02_foundations_mathjax_component as foundations,
    build_chapter_02_inverse_properties_mathjax_component as inverse_properties,
    build_chapter_02_special_filters_mathjax_component as special_filters,
    build_chapter_02_supplemental_training_mathjax_component as supplemental_training,
    build_chapter_02_supplemental_training_batch_two_mathjax_component as supplemental_training_batch_two,
    build_chapter_02_system_frequency_mathjax_component as system_frequency,
    build_chapter_02_training_mathjax_component as training,
)


COMPONENTS = (
    foundations,
    inverse_properties,
    dtft,
    system_frequency,
    special_filters,
    training,
    supplemental_training,
    supplemental_training_batch_two,
)

STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{break-after:avoid;color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}figure{break-inside:avoid;margin:12pt auto;text-align:center}svg{width:min(100%,470pt);height:auto}figcaption{color:#315d7c;font-size:9.5pt;margin-top:4pt}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}.indent{padding-left:1.7em;text-indent:-1.7em}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>"""


def _main_body(html: str) -> str:
    match = re.search(r"<main>(.*)</main>", html, flags=re.DOTALL)
    if not match:
        raise ValueError("component HTML is missing its main content block")
    return match.group(1)


def _combined_content() -> str:
    with tempfile.TemporaryDirectory(prefix="dsp-chapter-02-") as directory:
        temp = Path(directory)
        bodies = []
        for module in COMPONENTS:
            path = module.write_html(temp / f"{module.__name__.split('.')[-1]}.html")
            bodies.append(_main_body(path.read_text(encoding="utf-8")))
    return "\n".join(bodies)


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    body = _combined_content()
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{body}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    """Return the assembled document only after MathJax has typeset every formula."""
    completed = subprocess.run(
        [
            str(EDGE), "--headless=new", "--disable-gpu",
            "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri(),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout


def assert_mathjax_ready(dom: str) -> None:
    """Prevent PDF export from silently leaking raw TeX source notation."""
    if "<mjx-container" not in dom:
        raise RuntimeError("MathJax did not produce any rendered formula containers")
    raw_delimiters = (r"\(", r"\)", r"\[", r"\]")
    remaining = [delimiter for delimiter in raw_delimiters if delimiter in dom]
    if remaining:
        raise RuntimeError(
            "MathJax left unprocessed formula delimiters in the document: "
            + ", ".join(remaining)
        )


def stamp_headers_and_folios(source: Path, output: Path) -> Path:
    """Place verified static page furniture in reserved PDF margins."""
    page_style.register_fonts()
    reader = PdfReader(str(source))
    writer = PdfWriter()
    chapter = "第二章 z 变换与 LSI 系统频域分析"
    for number, page in enumerate(reader.pages, start=1):
        overlay = BytesIO()
        layer = canvas.Canvas(overlay, pagesize=A4)
        page_style.draw_header(layer, chapter)
        page_style.draw_footer(layer, number)
        layer.save()
        overlay.seek(0)
        page.merge_page(PdfReader(overlay).pages[0])
        writer.add_page(page)
    with output.open("wb") as stream:
        writer.write(stream)
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    assert_mathjax_ready(rendered_dom(html))
    with tempfile.TemporaryDirectory(prefix="dsp-chapter-02-pdf-") as directory:
        raw_pdf = Path(directory) / "raw.pdf"
        subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={raw_pdf.resolve()}", html.resolve().as_uri()], check=True)
        return stamp_headers_and_folios(raw_pdf, output)


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_02_mathjax_handout.pdf"))
