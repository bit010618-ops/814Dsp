from __future__ import annotations

import json
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sample.tools import build_sample as style


MODEL_PATH = Path("full/source/chapter_01_opening_component.json")
CHAPTER_NAME = "第一章 离散时间信号与系统"
BLUE = HexColor("#123B5D")
BRASS = HexColor(style.ACCENT_BRASS)
PALE = HexColor("#F4F7F8")
INK = HexColor("#1F2933")


def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))


def _draw_section(page: canvas.Canvas, number: int, title: str, x: float, y: float) -> None:
    page.setFillColor(PALE)
    page.roundRect(x, y - 70, 222, 70, 3, fill=1, stroke=0)
    page.setStrokeColor(BRASS)
    page.setLineWidth(0.65)
    page.line(x + 18, y - 16, x + 55, y - 16)
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 10)
    page.drawString(x + 18, y - 34, title.split(" ", 1)[0])
    page.setFillColor(INK)
    page.setFont(style.FONT_SANS, 13)
    page.drawString(x + 18, y - 55, title.split(" ", 1)[1])


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    model = load_model(root)
    output = output_path or root / "full/outputs/chapter_01_opening_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("数字信号处理讲义：第一章导览")

    style.draw_header(page, CHAPTER_NAME)
    style.draw_footer(page, 1)
    y = style.draw_title(page, CHAPTER_NAME, 752)
    page.setStrokeColor(BRASS)
    page.setLineWidth(1.1)
    page.line(62, y - 9, 186, y - 9)
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 12)
    page.drawString(62, y - 42, "本章结构")
    page.setFillColor(INK)
    page.setFont(style.FONT_SERIF, 11)
    page.drawString(62, y - 65, "从离散时间序列的表示与运算出发，依次建立系统分析、差分方程与采样的基础。")

    positions = [(62, y - 106), (311, y - 106), (62, y - 197), (311, y - 197)]
    for number, (title, (x, section_y)) in enumerate(zip(model["sections"], positions), start=1):
        _draw_section(page, number, title, x, section_y)

    page.setStrokeColor(BRASS)
    page.setLineWidth(0.55)
    page.line(62, 388, A4[0] - 62, 388)
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 11)
    page.drawString(62, 364, "学习主线")
    page.setFillColor(INK)
    page.setFont(style.FONT_SERIF, 11)
    page.drawString(62, 338, "序列的描述与运算 → 系统性质与时域求解 → 差分方程 → 连续时间信号的抽样与恢复")
    page.showPage()
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
