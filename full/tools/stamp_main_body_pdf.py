"""Stamp stable page furniture onto the browser-rendered main-body PDF."""
from __future__ import annotations

import re
from io import BytesIO
from pathlib import Path

from pypdf import PageObject, PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    BooleanObject,
    DecodedStreamObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from sample.tools import build_sample as page_style


CHAPTER_TITLES = (
    "第一章 离散时间信号与系统",
    "第二章 z 变换与 LSI 系统频域分析",
    "第三章 离散傅里叶变换",
    "第四章 快速傅里叶变换",
    "第五章 数字滤波器结构",
    "第六章 IIR 数字滤波器设计",
    "第七章 FIR 数字滤波器设计",
    "第八章 多采样率数字信号处理",
)


def _normalise(text: str) -> str:
    return re.sub(r"\s+", "", text)


def chapter_for_pages(page_texts: list[str]) -> list[str]:
    """Infer each page's chapter from the first chapter title seen so far."""
    current = CHAPTER_TITLES[0]
    result: list[str] = []
    for text in page_texts:
        compact = _normalise(text)
        for title in CHAPTER_TITLES:
            if _normalise(title) in compact:
                current = title
                break
        result.append(current)
    return result


def _page_as_form_xobject(writer: PdfWriter, page: PageObject, *, isolated: bool = False):
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
    """Overlay chapter-aware headers and real folios inside reserved margins."""
    page_style.register_fonts()
    reader = PdfReader(str(source))
    chapters = chapter_for_pages([(page.extract_text() or "") for page in reader.pages])
    writer = PdfWriter()
    for number, (page, chapter) in enumerate(zip(reader.pages, chapters), start=1):
        overlay = BytesIO()
        layer = canvas.Canvas(overlay, pagesize=A4, pageCompression=1)
        page_style.draw_header(layer, chapter)
        page_style.draw_footer(layer, number)
        layer.save()
        overlay.seek(0)
        header_page = PdfReader(overlay).pages[0]
        source_form = _page_as_form_xobject(writer, page, isolated=True)
        furniture_form = _page_as_form_xobject(writer, header_page)
        finished = writer.add_blank_page(width=A4[0], height=A4[1])
        finished[NameObject("/Resources")] = DictionaryObject(
            {
                NameObject("/XObject"): DictionaryObject(
                    {
                        NameObject("/Source"): source_form,
                        NameObject("/Furniture"): furniture_form,
                    }
                )
            }
        )
        stream = DecodedStreamObject()
        stream.set_data(b"q\n/Source Do\nQ\nq\n/Furniture Do\nQ\n")
        finished.replace_contents(stream)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as target:
        writer.write(target)
    return output
