from __future__ import annotations

import json
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sample.tools import build_sample as style


MODEL_PATH = Path("full/source/chapter_01_representation_component.json")
CHAPTER_NAME = "第一章 离散时间信号与系统"
INK = HexColor("#1F2933")
BLUE = HexColor("#123B5D")
BRASS = HexColor(style.ACCENT_BRASS)
TEAL = HexColor("#0F766E")
ORANGE = HexColor("#B45309")
PALE = HexColor("#F4F7F8")
TICK_OFFSET = 4


def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))


def _start(page: canvas.Canvas, number: int) -> None:
    style.draw_header(page, CHAPTER_NAME)
    style.draw_footer(page, number)


def _formula_box(page: canvas.Canvas, formula: str, y: float, *, height: float = 42) -> float:
    asset, image_width, image_height = style._math_metrics(formula, style.DISPLAY_FORMULA_SIZE)
    drawn_height = min(height - 12, image_height * 72 / 300)
    drawn_width = image_width * drawn_height / image_height
    maximum = A4[0] - 148
    if drawn_width > maximum:
        ratio = maximum / drawn_width
        drawn_width *= ratio
        drawn_height *= ratio
    bottom = y - height
    page.setFillColor(PALE)
    page.roundRect(62, bottom, A4[0] - 124, height, 3, fill=1, stroke=0)
    page.drawImage(ImageReader(str(asset)), (A4[0] - drawn_width) / 2, bottom + (height - drawn_height) / 2, drawn_width, drawn_height, mask="auto")
    return bottom - 15


def _draw_math(page: canvas.Canvas, formula: str, x: float, y: float, *, height: float = 14) -> float:
    """Draw a mathtext asset and return its displayed width.

    ReportLab's built-in Times font does not contain every mathematical glyph
    needed here (notably delta and the not-equal sign), so all symbolic graph
    labels and the piecewise definition use the same rendered math path as the
    display equations.
    """
    asset, image_width, image_height = style._math_metrics(formula, style.DISPLAY_FORMULA_SIZE)
    drawn_width = image_width * height / image_height
    page.drawImage(ImageReader(str(asset)), x, y, drawn_width, height, mask="auto")
    return drawn_width


def _draw_axis(page: canvas.Canvas, x: float, y: float, width: float, height: float, *, n_min: int, n_max: int, label: str = "x(n)") -> tuple[float, float, float]:
    base = y + height * 0.5
    left = x + 18
    right = x + width - 12
    zero_x = left + (0 - n_min) * (right - left) / (n_max - n_min)
    page.setStrokeColor(BLUE)
    page.setLineWidth(0.7)
    page.line(left, base, right, base)
    page.line(zero_x, y + 9, zero_x, y + height - 6)
    page.setFillColor(INK)
    _draw_math(page, label, zero_x + 4, y + height - 17, height=13)
    # Keep the horizontal-axis name outside the rightmost tick-number column.
    page.setFont("Times-Italic", 10.5)
    page.drawString(right + 10, base - 15, "n")
    page.setFont(style.FONT_SANS, 7.3)
    for n in range(n_min, n_max + 1):
        px = left + (n - n_min) * (right - left) / (n_max - n_min)
        page.setStrokeColor(BLUE)
        page.line(px, base - 3, px, base + 3)
        page.setFillColor(HexColor("#52616B"))
        page.drawCentredString(px + TICK_OFFSET, base - 13, str(n))
    return left, right, base


def _draw_stems(page: canvas.Canvas, x: float, y: float, width: float, height: float, values: dict[int, int], *, n_min: int, n_max: int, show_values: bool = True, label: str = "x(n)") -> None:
    left, right, base = _draw_axis(page, x, y, width, height, n_min=n_min, n_max=n_max, label=label)
    scale_x = (right - left) / (n_max - n_min)
    scale_y = min((height * 0.42) / max(1, max(abs(value) for value in values.values())), 22)
    for n, value in values.items():
        px = left + (n - n_min) * scale_x
        top = base + value * scale_y
        page.setStrokeColor(ORANGE)
        page.setFillColor(ORANGE)
        page.setLineWidth(1.1)
        page.line(px, base, px, top)
        page.circle(px, top, 1.8, fill=1, stroke=0)
        if show_values:
            page.setFillColor(INK)
            page.setFont(style.FONT_SANS, 8)
            page.drawCentredString(px + TICK_OFFSET, top + (7 if value >= 0 else -11), str(value))


def _case_definition(page: canvas.Canvas, x: float, y_top: float, width: float) -> float:
    height = 83
    bottom = y_top - height
    page.setFillColor(PALE)
    page.roundRect(x, bottom, width, height, 3, fill=1, stroke=0)
    page.setFillColor(INK)
    _draw_math(page, r"\delta(n)=", x + 54, bottom + 34, height=18)
    page.setFont("Times-Roman", 40)
    page.drawString(x + 132, bottom + 22, "{")
    _draw_math(page, r"1", x + 162, bottom + 49, height=15)
    _draw_math(page, r"n=0", x + 202, bottom + 49, height=15)
    _draw_math(page, r"0", x + 162, bottom + 22, height=15)
    _draw_math(page, r"n\ne0", x + 202, bottom + 22, height=15)
    return bottom - 14


def _page_methods(page: canvas.Canvas) -> None:
    _start(page, 1)
    y = style.draw_title(page, "离散时间信号的表示方法", 774)
    y = style.draw_rich_paragraph(page, "离散时间信号可用数列、函数、图形和单位抽样序列四种方式表示。它们描述的是同一个以整数 {{n}} 为自变量的序列，应能相互对应。", 62, y, A4[0] - 124)
    y = style.draw_continuation_title(page, "用数列与函数表示", y - 2)
    y = style.draw_rich_paragraph(page, "用数列表示时，下划线标出 {{n=0}} 在序列中的位置。例如：", 62, y, A4[0] - 124)
    y = _formula_box(page, r"x_1(n)=\{\underline{1},2,3,4,5\},\quad x_2(n)=\{1,2,\underline{3},4,5\},\quad x_3(n)=\{\underline{0},0,1,2,3,4,5\}", y - 4, height=44)
    y = style.draw_rich_paragraph(page, r"三组数值相同的数列并不一定代表同一序列：必须用下划线明确 {{n=0}} 对应的项。用函数表示时，{{n}} 只取整数，因此条件 {{n<0}} 与 {{n\leq-1}} 对离散序列是等价的。", 62, y, A4[0] - 124)
    y = _formula_box(page, r"x_4(n)=A\sin(\omega n+\varphi),\quad n\in(-\infty,\infty)", y - 3)
    y = _case_definition(page, 62, y, A4[0] - 124)
    style.draw_note(page, "读数列时先找 {{n=0}} 的位置，再向两侧确定各样点的时间索引；不能只按数字的排列顺序判断序列。", y - 3)
    page.showPage()


def _page_graph_and_impulse(page: canvas.Canvas, model: dict) -> None:
    _start(page, 2)
    y = style.draw_title(page, "用图形表示离散时间信号", 774)
    y = style.draw_rich_paragraph(page, "图形的横坐标 {{n}} 表示离散时间坐标，仅在 {{n}} 为整数时有意义；纵坐标表示各信号点的值。下图给出同一序列的 stem 图表示。", 62, y, A4[0] - 124)
    values = {int(key): value for key, value in model["sample_plot"]["values"].items()}
    _draw_stems(page, 74, 390, A4[0] - 148, 210, values, n_min=-1, n_max=11)
    y = 365
    y = style.draw_continuation_title(page, "用单位抽样序列表示", y)
    y = style.draw_rich_paragraph(page, r"单位抽样序列 {{\delta(n)}} 是脉冲幅度为 1 的离散序列。它只有在 {{n=0}} 时取 1，在其他整数时刻均取 0：", 62, y, A4[0] - 124)
    _case_definition(page, 62, y - 4, 250)
    _draw_stems(page, 350, y - 92, 175, 100, {0: 1}, n_min=-4, n_max=6, show_values=True, label="δ(n)")
    page.showPage()


def _page_expansion_example(page: canvas.Canvas) -> None:
    _start(page, 3)
    y = style.draw_title(page, "单位抽样序列的移位加权和", 774)
    y = style.draw_rich_paragraph(page, r"任何序列都可以表示为单位抽样序列的移位加权和：{{x(m)}} 给出第 {{m}} 个样点的值，{{\delta(n-m)}} 给出该样点所在的位置。", 62, y, A4[0] - 124)
    y = _formula_box(page, r"x(n)=\sum_{m=-\infty}^{\infty}x(m)\delta(n-m)", y - 3)
    y = style.draw_continuation_title(page, "例：用单位抽样序列表示 x(n)={1,2,3}", y - 3)
    y = style.draw_rich_paragraph(page, "数列中第一项为 {{n=0}}，因此 {{x(0)=1}}、{{x(1)=2}}、{{x(2)=3}}。将三个样点分别平移到 0、1、2 处并按幅值加权：", 62, y, A4[0] - 124)
    _draw_stems(page, 66, 390, 212, 105, {0: 1}, n_min=-2, n_max=4, show_values=True, label="δ(n)")
    _draw_stems(page, 310, 390, 212, 105, {1: 2}, n_min=-2, n_max=4, show_values=True, label="2δ(n-1)")
    _draw_stems(page, 66, 260, 212, 105, {2: 3}, n_min=-2, n_max=4, show_values=True, label="3δ(n-2)")
    _draw_stems(page, 310, 260, 212, 105, {0: 1, 1: 2, 2: 3}, n_min=-2, n_max=4, show_values=True, label="x(n)")
    y = _formula_box(page, r"x(n)=\delta(n)+2\delta(n-1)+3\delta(n-2)=\sum_{m=0}^{2}x(m)\delta(n-m)", 229, height=47)
    style.draw_note(page, r"展开时，“值”写在 {{x(m)}} 前，“位置”由 {{\delta(n-m)}} 决定。检查时逐项代入 {{n=0,1,2}}，应分别得到 1、2、3。", y - 4)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    model = load_model(root)
    output = output_path or root / "full" / "outputs" / "chapter_01_representation_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("数字信号处理讲义：第一章表示方法组件")
    _page_methods(page)
    _page_graph_and_impulse(page, model)
    _page_expansion_example(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
