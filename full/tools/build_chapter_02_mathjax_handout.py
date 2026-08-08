"""Assemble migrated chapter-two blocks into one naturally reflowed A4 document."""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from io import BytesIO
from pathlib import Path

from pypdf import PageObject, PdfReader, PdfWriter
from pypdf.generic import ArrayObject, BooleanObject, DecodedStreamObject, DictionaryObject, FloatObject, NameObject, NumberObject
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
    build_chapter_02_supplemental_training_batch_three_mathjax_component as supplemental_training_batch_three,
    build_chapter_02_supplemental_training_batch_four_mathjax_component as supplemental_training_batch_four,
    build_chapter_02_supplemental_training_batch_five_mathjax_component as supplemental_training_batch_five,
    build_chapter_02_supplemental_training_batch_six_mathjax_component as supplemental_training_batch_six,
    build_chapter_02_supplemental_training_batch_seven_mathjax_component as supplemental_training_batch_seven,
    build_chapter_02_supplemental_training_batch_eight_mathjax_component as supplemental_training_batch_eight,
    build_chapter_02_supplemental_training_batch_nine_mathjax_component as supplemental_training_batch_nine,
    build_chapter_02_supplemental_training_batch_ten_mathjax_component as supplemental_training_batch_ten,
    build_chapter_02_supplemental_training_batch_eleven_mathjax_component as supplemental_training_batch_eleven,
    build_chapter_02_supplemental_training_batch_twelve_mathjax_component as supplemental_training_batch_twelve,
    build_chapter_02_supplemental_training_batch_thirteen_mathjax_component as supplemental_training_batch_thirteen,
    build_chapter_02_supplemental_training_batch_fourteen_mathjax_component as supplemental_training_batch_fourteen,
    build_chapter_02_supplemental_training_batch_sixteen_mathjax_component as supplemental_training_batch_sixteen,
    build_chapter_02_supplemental_training_batch_seventeen_mathjax_component as supplemental_training_batch_seventeen,
    build_chapter_02_supplemental_training_batch_eighteen_mathjax_component as supplemental_training_batch_eighteen,
    build_chapter_02_supplemental_training_batch_nineteen_mathjax_component as supplemental_training_batch_nineteen,
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
    supplemental_training_batch_three,
    supplemental_training_batch_four,
    supplemental_training_batch_five,
    supplemental_training_batch_six,
    supplemental_training_batch_seven,
    supplemental_training_batch_eight,
    supplemental_training_batch_nine,
    supplemental_training_batch_ten,
    supplemental_training_batch_eleven,
    supplemental_training_batch_twelve,
    supplemental_training_batch_thirteen,
    supplemental_training_batch_fourteen,
    supplemental_training_batch_sixteen,
    supplemental_training_batch_seventeen,
    supplemental_training_batch_eighteen,
    supplemental_training_batch_nineteen,
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
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<body><main>{body}</main></body></html>'''
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


def _page_as_form_xobject(writer: PdfWriter, page: PageObject, *, isolated: bool = False):
    """Embed a PDF page as a self-contained Form XObject.

    Chromium occasionally leaves a malformed graphics-state stack in a page
    stream.  Invoking that page as a Form confines the defect to the form, so
    it cannot clip or otherwise mask the independent header/footer layer.
    """
    form = DecodedStreamObject()
    contents = page.get_contents()
    form.set_data(contents.get_data() if contents is not None else b"")
    form[NameObject("/Type")] = NameObject("/XObject")
    form[NameObject("/Subtype")] = NameObject("/Form")
    form[NameObject("/FormType")] = NumberObject(1)
    form[NameObject("/BBox")] = ArrayObject(
        [
            FloatObject(float(page.mediabox.left)),
            FloatObject(float(page.mediabox.bottom)),
            FloatObject(float(page.mediabox.right)),
            FloatObject(float(page.mediabox.top)),
        ]
    )
    resources = page.get("/Resources")
    form[NameObject("/Resources")] = (
        resources.clone(writer) if resources is not None else DictionaryObject()
    )
    if isolated:
        form[NameObject("/Group")] = DictionaryObject(
            {
                NameObject("/S"): NameObject("/Transparency"),
                NameObject("/I"): BooleanObject(True),
                NameObject("/K"): BooleanObject(False),
            }
        )
    return writer._add_object(form)


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
        header_page = PdfReader(overlay).pages[0]
        source_form = _page_as_form_xobject(writer, page, isolated=True)
        header_form = _page_as_form_xobject(writer, header_page)
        finished_page = writer.add_blank_page(width=A4[0], height=A4[1])
        finished_page[NameObject("/Resources")] = DictionaryObject(
            {
                NameObject("/XObject"): DictionaryObject(
                    {
                        NameObject("/Source"): source_form,
                        NameObject("/Header"): header_form,
                    }
                )
            }
        )
        stream = DecodedStreamObject()
        stream.set_data(b"q\n/Source Do\nQ\nq\n/Header Do\nQ\n")
        finished_page.replace_contents(stream)
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
