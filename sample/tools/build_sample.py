from __future__ import annotations

import json
import hashlib
import os
import re
from pathlib import Path

from PIL import Image
os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / "artifacts" / ".matplotlib"))
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[1]
FONT_SERIF = "NotoSerifSC"
FONT_SANS = "NotoSansSC"
MATH_CACHE = ROOT / "artifacts" / "formula_cache"
DISPLAY_FORMULA_SIZE = 11
# 正文文字之间的行内公式：统一使用 17.5 pt 实际绘制高度。
INLINE_MATH_DRAWN_HEIGHT = 17.5
# 相对正文基线下移 3 pt，使行内数学符号与文字中线对齐。
INLINE_MATH_BASELINE_OFFSET = -5.5
# 传统教材风的低饱和黄铜金，仅用于细线点缀，不承担正文信息。
ACCENT_BRASS = "#B08D57"

matplotlib.rcParams.update({"mathtext.fontset": "stix"})


def register_fonts() -> None:
    if FONT_SERIF not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(
            TTFont(FONT_SERIF, r"C:\Windows\Fonts\NotoSerifSC-VF.ttf")
        )
    if FONT_SANS not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(
            TTFont(FONT_SANS, r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
        )


def wrap_text(text: str, font: str, size: float, width: float) -> list[str]:
    lines: list[str] = []
    current = ""
    for character in text:
        candidate = current + character
        if current and pdfmetrics.stringWidth(candidate, font, size) > width:
            lines.append(current)
            current = character
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def validate_formula_source(source: str) -> str | None:
    if "/" in source:
        return "solidus division is forbidden; use \\frac{numerator}{denominator}"
    return None


def math_asset(source: str, cache_dir: Path = MATH_CACHE, font_size: float = 15) -> Path:
    error = validate_formula_source(source)
    if error:
        raise ValueError(error)
    cache_dir.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(f"{source}|{font_size}".encode("utf-8")).hexdigest()[:16]
    output = cache_dir / f"math-{digest}.png"
    if output.exists():
        return output

    figure = plt.figure(figsize=(4, 1), dpi=300)
    figure.patch.set_alpha(0)
    figure.text(0.5, 0.5, f"${source}$", ha="center", va="center", fontsize=font_size, color="#1F2933")
    figure.savefig(output, dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.05)
    plt.close(figure)
    return output


def _math_metrics(source: str, size: float = 11) -> tuple[Path, float, float]:
    asset = math_asset(source, font_size=size)
    with Image.open(asset) as image:
        return asset, float(image.width), float(image.height)


def _rich_atoms(text: str) -> list[tuple[str, str]]:
    atoms: list[tuple[str, str]] = []
    position = 0
    while True:
        start = text.find("{{", position)
        if start < 0:
            break
        atoms.extend(("text", character) for character in text[position:start])
        end = text.find("}}", start + 2)
        if end < 0:
            atoms.extend(("text", character) for character in text[start:])
            return atoms
        while end + 2 < len(text) and text[end + 2] == "}":
            end += 1
        atoms.append(("math", text[start + 2:end]))
        position = end + 2
    atoms.extend(("text", character) for character in text[position:])
    return atoms


def draw_rich_paragraph(
    page: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    font: str = FONT_SERIF,
    size: float = 10.5,
    leading: float = 18,
) -> float:
    page.setFillColor(HexColor("#1F2933"))
    page.setFont(font, size)
    cursor = x
    atoms = _rich_atoms(text)
    for index, (kind, value) in enumerate(atoms):
        if kind == "text":
            if value == "\n":
                y -= leading
                cursor = x
                continue
            atom_width = pdfmetrics.stringWidth(value, font, size)
            if (
                cursor > x
                and cursor + atom_width > x + width
                and value not in "，。；：、）"
            ):
                y -= leading
                cursor = x
            page.drawString(cursor, y, value)
            cursor += atom_width
            continue

        asset, image_width, image_height = _math_metrics(value, size + 2.8)
        drawn_height = min(leading - 2, INLINE_MATH_DRAWN_HEIGHT)
        drawn_width = image_width * drawn_height / image_height
        trailing_width = 0.0
        if index + 1 < len(atoms):
            next_kind, next_value = atoms[index + 1]
            if next_kind == "text" and next_value in "，。；：、）":
                trailing_width = pdfmetrics.stringWidth(next_value, font, size)
        if cursor > x and cursor + drawn_width + trailing_width > x + width:
            y -= leading
            cursor = x
        page.drawImage(
            ImageReader(str(asset)),
            cursor,
            y + INLINE_MATH_BASELINE_OFFSET,
            drawn_width,
            drawn_height,
            mask="auto",
        )
        cursor += drawn_width
    return y - leading


def draw_header(page: canvas.Canvas, chapter: str) -> None:
    width, height = A4
    page.setStrokeColor(HexColor(ACCENT_BRASS))
    page.setLineWidth(0.45)
    page.line(50, height - 46, width - 50, height - 46)
    page.setFillColor(HexColor("#123B5D"))
    page.setFont(FONT_SANS, 8.6)
    page.drawString(50, height - 35, "数字信号处理讲义")
    page.setFillColor(HexColor("#52616B"))
    page.setFont(FONT_SERIF, 8.2)
    page.drawRightString(width - 50, height - 35, chapter)


def draw_footer(page: canvas.Canvas, page_number: int) -> None:
    width, _ = A4
    page.setFillColor(HexColor("#52616B"))
    page.setFont("Times-Roman", 9)
    page.drawCentredString(width / 2, 31, str(page_number))


def draw_title(page: canvas.Canvas, title: str, y: float, title_right: str = "") -> float:
    page.setFillColor(HexColor("#123B5D"))
    page.setFont(FONT_SANS, 18)
    page.drawString(62, y, title)
    if title_right:
        title_width = pdfmetrics.stringWidth(title, FONT_SANS, 18)
        page.setFillColor(HexColor("#52616B"))
        page.setFont(FONT_SERIF, 9.5)
        page.drawString(62 + title_width + 22, y + 2, title_right)
    page.setStrokeColor(HexColor(ACCENT_BRASS))
    page.setLineWidth(0.9)
    page.line(62, y - 12, 230, y - 12)
    return y - 38


def draw_continuation_title(page: canvas.Canvas, title: str, y: float, size: float = 13) -> float:
    page.setFillColor(HexColor("#123B5D"))
    page.setFont(FONT_SANS, size)
    page.drawString(62, y, title)
    page.setStrokeColor(HexColor(ACCENT_BRASS))
    page.setLineWidth(0.7)
    page.line(62, y - 10, 230 if size >= 18 else 190, y - 10)
    return y - (38 if size >= 18 else 28)


def draw_body_lines(page: canvas.Canvas, lines: list[str], y: float) -> float:
    usable_width = A4[0] - 124
    for text in lines:
        y = draw_rich_paragraph(page, text, 62, y, usable_width)
    return y


def draw_note(page: canvas.Canvas, note: str, y: float) -> float:
    page.setFillColor(HexColor("#F4F7F8"))
    page.roundRect(62, y - 58, A4[0] - 124, 58, 3, fill=1, stroke=0)
    page.setFillColor(HexColor("#123B5D"))
    page.setFont(FONT_SANS, 9.5)
    page.drawString(76, y - 20, "复习提示")
    y = draw_rich_paragraph(page, note, 76, y - 40, A4[0] - 152, size=10)
    return y - 18


def draw_formula(page: canvas.Canvas, formula: str, y: float) -> float:
    error = validate_formula_source(formula)
    if error:
        raise ValueError(error)
    asset, image_width, image_height = _math_metrics(formula, DISPLAY_FORMULA_SIZE)
    drawn_width = image_width * 72 / 300
    drawn_height = image_height * 72 / 300
    max_width = A4[0] - 150
    if drawn_width > max_width:
        scale = max_width / drawn_width
        drawn_width *= scale
        drawn_height *= scale
    box_height = max(36, drawn_height + 16)
    box_bottom = y - box_height + 8
    page.setFillColor(HexColor("#F4F7F8"))
    page.roundRect(62, box_bottom, A4[0] - 124, box_height, 3, fill=1, stroke=0)
    page.drawImage(
        ImageReader(str(asset)),
        (A4[0] - drawn_width) / 2,
        box_bottom + (box_height - drawn_height) / 2,
        drawn_width,
        drawn_height,
        mask="auto",
    )
    return box_bottom - 16


def draw_exercise_box(page: canvas.Canvas, question: str, y: float, height: float) -> float:
    width = A4[0] - 124
    page.setFillColor(HexColor("#FFF9E8"))
    page.setStrokeColor(HexColor("#D9B356"))
    page.roundRect(62, y - height, width, height, 4, fill=1, stroke=1)
    page.setFillColor(HexColor("#9D2B2B"))
    page.setFont(FONT_SANS, 10.5)
    page.drawString(78, y - 22, "练习")
    question_y = draw_rich_paragraph(page, question, 78, y - 48, width - 32)
    page.setStrokeColor(HexColor("#B8C3CA"))
    line_y = question_y - 12
    while line_y > y - height + 22:
        page.line(78, line_y, 62 + width - 16, line_y)
        line_y -= 22
    return y - height - 20


def draw_figure(
    page: canvas.Canvas,
    figure_path: str,
    caption: str,
    y: float,
    figure_title: str = "",
    crop: dict | None = None,
    max_height: float = 420,
) -> float:
    path = Path(figure_path)
    if not path.is_absolute():
        path = ROOT / path
    with Image.open(path) as source:
        image_width, image_height = source.size
    if figure_title:
        page.setFillColor(HexColor("#123B5D"))
        page.setFont(FONT_SANS, 10.5)
        page.drawCentredString(A4[0] / 2, y, figure_title)
        y -= 24
    crop = crop or {}
    left = int(crop.get("left_px", 0))
    top = int(crop.get("top_px", 0))
    right = int(crop.get("right_px", 0))
    bottom = int(crop.get("bottom_px", 0))
    cropped_width = image_width - left - right
    cropped_height = image_height - top - bottom
    if cropped_width <= 0 or cropped_height <= 0:
        raise ValueError("invalid figure crop")
    max_width = A4[0] - 124
    scale = min(max_width / cropped_width, max_height / cropped_height)
    drawn_width = cropped_width * scale
    drawn_height = cropped_height * scale
    x = (A4[0] - drawn_width) / 2
    crop_bottom_y = y - drawn_height
    page.saveState()
    clip = page.beginPath()
    clip.rect(x, crop_bottom_y, drawn_width, drawn_height)
    page.clipPath(clip, stroke=0, fill=0)
    page.drawImage(
        ImageReader(str(path)),
        x - left * scale,
        crop_bottom_y - bottom * scale,
        image_width * scale,
        image_height * scale,
        mask="auto",
    )
    page.restoreState()
    if not caption:
        return y - drawn_height - 18
    page.setFillColor(HexColor("#52616B"))
    page.setFont(FONT_SERIF, 9)
    page.drawCentredString(A4[0] / 2, y - drawn_height - 16, caption)
    return y - drawn_height - 34


def draw_page(page: canvas.Canvas, item: dict, chapter: str, page_number: int) -> None:
    draw_header(page, item.get("chapter", chapter))
    y = draw_title(page, item["title"], A4[1] - 82, item.get("title_right", ""))
    if item.get("lead"):
        y = draw_body_lines(page, [item["lead"]], y)
        y -= 8
    formulae = item.get("formulae") or ([item["formula"]] if item.get("formula") else [])
    for formula in formulae:
        y = draw_formula(page, formula, y)
    if item.get("body"):
        y = draw_body_lines(page, item["body"], y)
    if item.get("plain_question"):
        y = draw_body_lines(page, [item["plain_question"]], y)
    if item.get("figure_path"):
        y = draw_figure(
            page,
            item["figure_path"],
            item.get("caption", ""),
            y,
            item.get("figure_title", ""),
            item.get("figure_crop"),
            float(item.get("figure_max_height", 420)),
        )
    if item.get("note"):
        y = draw_note(page, item["note"], y)
    for continuation in item.get("continuations", []):
        y -= 4
        y = draw_continuation_title(
            page,
            continuation["title"],
            y,
            float(continuation.get("title_size", 13)),
        )
        if continuation.get("lead"):
            y = draw_body_lines(page, [continuation["lead"]], y)
            y -= 8
        formulae = continuation.get("formulae") or (
            [continuation["formula"]] if continuation.get("formula") else []
        )
        for formula in formulae:
            y = draw_formula(page, formula, y)
        if continuation.get("body"):
            y = draw_body_lines(page, continuation["body"], y)
        if continuation.get("note"):
            y = draw_note(page, continuation["note"], y)
    if item.get("exercise"):
        draw_exercise_box(
            page,
            item["exercise"],
            y,
            float(item.get("exercise_height", 160)),
        )
    draw_footer(page, page_number)
    page.showPage()


def build_sample(content_path: Path, output_path: Path) -> Path:
    register_fonts()
    content = json.loads(content_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output_path), pagesize=A4, pageCompression=1)
    for number, item in enumerate(content["pages"], start=1):
        draw_page(page, item, content["chapter"], number)
    page.save()
    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--content", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    build_sample(args.content, args.output)
