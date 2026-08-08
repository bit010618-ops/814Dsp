from __future__ import annotations

import io
import re
import sys
from collections import deque
from pathlib import Path

import pdfplumber
from pypdf import PageObject, PdfReader, PdfWriter, Transformation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sample.tools import build_sample as style


CHAPTER_NAME = "第一章 离散时间信号与系统"
OUTPUT_PATH = Path("full/outputs/chapter_01_handout.pdf")
PAGE_WIDTH, PAGE_HEIGHT = map(float, A4)
# The overlay header rule sits near 794 pt.  Keep the top of each reflowed
# content block below it so 18 pt section titles cannot touch the rule.
BODY_TOP = 766.0
BODY_BOTTOM = 35.0
CROP_TOP = 800.0
# Individual component pages already carry a conservative internal safety
# margin around every glyph, formula and figure.  A small inter-block gap is
# therefore enough and avoids creating artificial half-page whitespace.
BLOCK_GAP = 0.0
COMPONENT_FILENAMES = (
    "chapter_01_opening_component.pdf",
    "chapter_01_origin_component.pdf",
    "chapter_01_representation_mathjax_component.pdf",
    "chapter_01_operations_mathjax_component.pdf",
    "chapter_01_typical_sequences_mathjax_component.pdf",
    "chapter_01_periodicity_mathjax_component.pdf",
    "chapter_01_linearity_mathjax_component.pdf",
    "chapter_01_time_invariance_mathjax_component.pdf",
    "chapter_01_convolution_basics_mathjax_component.pdf",
    "chapter_01_convolution_properties_mathjax_component.pdf",
    "chapter_01_causal_stable_mathjax_component.pdf",
    "chapter_01_difference_equation_mathjax_component.pdf",
    "chapter_01_sampling_theorem_mathjax_component.pdf",
    "chapter_01_sampling_engineering_mathjax_component.pdf",
    "chapter_01_sampling_recovery_mathjax_component.pdf",
    "chapter_01_analog_digital_chain_mathjax_component.pdf",
    "chapter_01_applications_close_mathjax_component.pdf",
    "chapter_01_training_mathjax_component.pdf",
    "chapter_01_supplemental_mathjax_component.pdf",
    "chapter_01_training_answers_mathjax_component.pdf",
    "chapter_01_supplemental_answers_mathjax_component.pdf",
)
FULL_PAGE_VECTOR_COMPONENTS = frozenset({
    "chapter_01_representation_mathjax_component.pdf",
    "chapter_01_operations_mathjax_component.pdf",
    "chapter_01_typical_sequences_mathjax_component.pdf",
    "chapter_01_periodicity_mathjax_component.pdf",
    "chapter_01_linearity_mathjax_component.pdf",
    "chapter_01_time_invariance_mathjax_component.pdf",
    "chapter_01_convolution_basics_mathjax_component.pdf",
    "chapter_01_convolution_properties_mathjax_component.pdf",
    "chapter_01_causal_stable_mathjax_component.pdf",
    "chapter_01_difference_equation_mathjax_component.pdf",
    "chapter_01_sampling_theorem_mathjax_component.pdf",
    "chapter_01_sampling_engineering_mathjax_component.pdf",
    "chapter_01_sampling_recovery_mathjax_component.pdf",
    "chapter_01_analog_digital_chain_mathjax_component.pdf",
    "chapter_01_applications_close_mathjax_component.pdf",
    "chapter_01_training_mathjax_component.pdf",
    "chapter_01_supplemental_mathjax_component.pdf",
    "chapter_01_training_answers_mathjax_component.pdf",
    "chapter_01_supplemental_answers_mathjax_component.pdf",
})


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
    # Displayed formulas are raster XObjects and have no extractable text.  Keep
    # their transformation bounds in the crop calculation so their surrounding
    # formula box can never be split into a visible sliver at a reflow boundary.
    try:
        content = page.get_contents().get_data().decode("latin1")
    except Exception:
        content = ""
    number = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)"
    matrix = re.compile(
        rf"q\s+({number})\s+({number})\s+({number})\s+({number})\s+({number})\s+({number})\s+cm\s+/\S+\s+Do"
    )
    for match in matrix.finditer(content):
        _a, _b, _c, height, _x, bottom = map(float, match.groups())
        positions.extend((bottom, bottom + height))
    if not positions:
        return BODY_BOTTOM, CROP_TOP
    return max(BODY_BOTTOM, min(positions) - 34), min(CROP_TOP, max(positions) + 22)


def _vector_geometry_bounds(component_path: Path, page_index: int) -> tuple[float, float]:
    """Read actual HTML/SVG and MathJax vector marks, not just PDF text."""
    with pdfplumber.open(str(component_path)) as document:
        page = document.pages[page_index]
        objects = [
            item
            for group in page.objects.values()
            for item in group
            if "top" in item and "bottom" in item
        ]
        if not objects:
            return BODY_BOTTOM, CROP_TOP
        content_top = min(float(item["top"]) for item in objects)
        content_bottom = max(float(item["bottom"]) for item in objects)
        return (
            max(BODY_BOTTOM, float(page.height) - content_bottom - 25.0),
            min(CROP_TOP, float(page.height) - content_top + 20.0),
        )


def _component_page_bounds(
    component_path: Path, page: PageObject, *, page_index: int | None = None
) -> tuple[float, float]:
    """Use true vector geometry so the reflow engine never keeps blank page tails."""
    if component_path.name in FULL_PAGE_VECTOR_COMPONENTS and page_index is not None:
        return _vector_geometry_bounds(component_path, page_index)
    return _body_bounds(page)


def _safe_split_boundary(
    component_path: Path,
    page_index: int,
    *,
    bottom: float,
    top: float,
    max_height: float,
) -> float | None:
    """Return a whitespace cut line that fits the next normal-content fragment.

    Component PDFs are often taller than the remaining space on a handout page,
    even when their opening heading, prose and formula comfortably fit.  Use the
    real vector-object gaps as admissible cut lines so a chart or formula is
    never sheared just to eliminate a page tail.
    """
    minimum = top - max_height
    if minimum <= bottom or max_height < 96:
        return None

    with pdfplumber.open(str(component_path)) as document:
        page = document.pages[page_index]
        intervals: list[tuple[float, float]] = []
        for objects in page.objects.values():
            for item in objects:
                if "top" not in item or "bottom" not in item:
                    continue
                lower = max(bottom, float(page.height) - float(item["bottom"]))
                upper = min(top, float(page.height) - float(item["top"]))
                if upper > lower:
                    intervals.append((lower, upper))

    if not intervals:
        return None
    intervals.sort()
    merged: list[list[float]] = []
    for lower, upper in intervals:
        if not merged or lower > merged[-1][1] + 1.5:
            merged.append([lower, upper])
        else:
            merged[-1][1] = max(merged[-1][1], upper)

    # Select the lowest available gap: it fills the current page as much as
    # possible while retaining a generous buffer around adjacent content.
    candidates: list[float] = []
    for previous, following in zip(merged, merged[1:]):
        gap_bottom, gap_top = previous[1], following[0]
        if gap_top - gap_bottom < 16:
            continue
        cut = (gap_bottom + gap_top) / 2
        if minimum + 6 <= cut <= top - 48:
            candidates.append(cut)
    return min(candidates) if candidates else None


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
    source_pages: deque[tuple[Path, int, float, float, bool]] = deque()
    for component_path in load_component_paths(root):
        reader = PdfReader(str(component_path))
        # Chapter training is intentionally one exam question per printable
        # page.  Preserve that boundary for both priority and supplementary
        # sets when the otherwise-flowing body is assembled into the handout.
        keep_each_page = component_path.name in {
            "chapter_01_training_mathjax_component.pdf",
            "chapter_01_supplemental_mathjax_component.pdf",
        }
        for page_index, page in enumerate(reader.pages):
            bottom, top = _component_page_bounds(
                component_path, page, page_index=page_index
            )
            source_pages.append((component_path, page_index, bottom, top, keep_each_page))

    writer = PdfWriter()
    target = _new_page(writer)
    cursor = BODY_TOP
    while source_pages:
        component_path, page_index, bottom, top, keep_each_page = source_pages.popleft()
        height = top - bottom
        available = cursor - BODY_BOTTOM
        if not keep_each_page and height > available and cursor < BODY_TOP:
            split = _safe_split_boundary(
                component_path,
                page_index,
                bottom=bottom,
                top=top,
                max_height=available,
            )
            if split is not None:
                # Continue the lower fragment before later component pages.
                source_pages.appendleft((component_path, page_index, bottom, split, False))
                bottom = split
                height = top - bottom
        if cursor - height < BODY_BOTTOM:
            target = _new_page(writer)
            cursor = BODY_TOP
        # A fresh reader keeps crops of a preceding fragment from leaking into
        # the continuation fragment of the same source component page.
        source = PdfReader(str(component_path)).pages[page_index]
        source.mediabox.lower_left = (0, bottom)
        source.mediabox.upper_right = (PAGE_WIDTH, top)
        source.cropbox.lower_left = (0, bottom)
        source.cropbox.upper_right = (PAGE_WIDTH, top)
        destination_bottom = cursor - height
        target.merge_transformed_page(source, Transformation().translate(0, destination_bottom - bottom))
        cursor = BODY_BOTTOM if keep_each_page else destination_bottom - BLOCK_GAP

    overlay = _overlay(len(writer.pages))
    for page, layer in zip(writer.pages, overlay.pages):
        page.merge_page(layer, over=True)

    output = output_path or root / OUTPUT_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    writer.write(str(output))
    return output


if __name__ == "__main__":
    print(build_pdf())
