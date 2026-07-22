from __future__ import annotations

import io
import sys
from pathlib import Path

from pypdf import PageObject, PdfReader, PdfWriter, Transformation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sample.tools import build_sample as style


CHAPTER_NAME = "第一章 离散时间信号与系统"
OUTPUT_PATH = Path("full/outputs/chapter_01_handout.pdf")
PAGE_WIDTH, PAGE_HEIGHT = map(float, A4)
BODY_TOP = 780.0
BODY_BOTTOM = 70.0
CROP_TOP = 800.0
BLOCK_GAP = 12.0
COMPONENT_FILENAMES = (
    "chapter_01_opening_component.pdf",
    "chapter_01_origin_component.pdf",
    "chapter_01_representation_component.pdf",
    "chapter_01_operations_component.pdf",
    "chapter_01_typical_sequences_component.pdf",
    "chapter_01_periodicity_component.pdf",
    "chapter_01_linearity_component.pdf",
    "chapter_01_time_invariance_component.pdf",
    "chapter_01_convolution_basics_component.pdf",
    "chapter_01_convolution_properties_component.pdf",
    "chapter_01_causal_stable_component.pdf",
    "chapter_01_difference_equation_component.pdf",
    "chapter_01_sampling_theorem_component.pdf",
    "chapter_01_sampling_engineering_component.pdf",
    "chapter_01_sampling_recovery_component.pdf",
    "chapter_01_analog_digital_chain_component.pdf",
    "chapter_01_applications_close_component.pdf",
)


def load_component_paths(root: Path = ROOT) -> list[Path]:
    paths = [root / "full/outputs" / filename for filename in COMPONENT_FILENAMES]
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError("chapter one component PDFs are missing: " + ", ".join(missing))
    return paths


def _body_bounds(page: PageObject) -> tuple[float, float]:
    positions: list[float] = []

    def collect(text: str, _cm, tm, _font, _size) -> None:
        if text.strip() and BODY_BOTTOM <= float(tm[5]) <= CROP_TOP:
            positions.append(float(tm[5]))

    page.extract_text(visitor_text=collect)
    if not positions:
        return BODY_BOTTOM, CROP_TOP
    return max(BODY_BOTTOM, min(positions) - 42), min(CROP_TOP, max(positions) + 28)


def _overlay(page_count: int) -> PdfReader:
    style.register_fonts()
    buffer = io.BytesIO()
    layer = canvas.Canvas(buffer, pagesize=A4, pageCompression=1)
    for number in range(1, page_count + 1):
        style.draw_header(layer, CHAPTER_NAME)
        style.draw_footer(layer, number)
        layer.showPage()
    layer.save()
    buffer.seek(0)
    return PdfReader(buffer)


def _new_page(writer: PdfWriter) -> PageObject:
    return writer.add_blank_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    source_pages: list[tuple[PageObject, float, float]] = []
    for component_path in load_component_paths(root):
        reader = PdfReader(str(component_path))
        for page in reader.pages:
            bottom, top = _body_bounds(page)
            source_pages.append((page, bottom, top))

    writer = PdfWriter()
    target = _new_page(writer)
    cursor = BODY_TOP
    for source, bottom, top in source_pages:
        height = top - bottom
        if cursor - height < BODY_BOTTOM:
            target = _new_page(writer)
            cursor = BODY_TOP
        source.mediabox.lower_left = (0, bottom)
        source.mediabox.upper_right = (PAGE_WIDTH, top)
        source.cropbox.lower_left = (0, bottom)
        source.cropbox.upper_right = (PAGE_WIDTH, top)
        destination_bottom = cursor - height
        target.merge_transformed_page(source, Transformation().translate(0, destination_bottom - bottom))
        cursor = destination_bottom - BLOCK_GAP

    overlay = _overlay(len(writer.pages))
    for page, layer in zip(writer.pages, overlay.pages):
        page.merge_page(layer, over=True)

    output = output_path or root / OUTPUT_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    writer.write(str(output))
    return output


if __name__ == "__main__":
    print(build_pdf())
