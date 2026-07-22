from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sample.tools import build_sample as style


MODEL_PATH = Path("full/source/chapter_01_origin_component.json")
CHAPTER_NAME = "第一章 离散时间信号与系统"
INK = HexColor("#1F2933")
BLUE = HexColor("#123B5D")
BRASS = HexColor(style.ACCENT_BRASS)
PALE = HexColor("#F4F7F8")
TEAL = HexColor("#0F766E")
HORIZONTAL_TICK_LABEL_OFFSET = 4
WAVEFORM_LEFT_LABEL_CLEARANCE = 24


def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))


def _start(page: canvas.Canvas, page_number: int) -> None:
    style.draw_header(page, CHAPTER_NAME)
    style.draw_footer(page, page_number)


def _formula_box(page: canvas.Canvas, formula: str, y: float, *, height: float = 42) -> float:
    asset, width, image_height = style._math_metrics(formula, style.DISPLAY_FORMULA_SIZE)
    drawn_height = min(height - 12, image_height * 72 / 300)
    drawn_width = width * drawn_height / image_height
    max_width = A4[0] - 146
    if drawn_width > max_width:
        ratio = max_width / drawn_width
        drawn_width *= ratio
        drawn_height *= ratio
    bottom = y - height
    page.setFillColor(PALE)
    page.roundRect(62, bottom, A4[0] - 124, height, 3, fill=1, stroke=0)
    page.drawImage(
        ImageReader(str(asset)), (A4[0] - drawn_width) / 2,
        bottom + (height - drawn_height) / 2, drawn_width, drawn_height, mask="auto"
    )
    return bottom - 15


def _signal_value(t: float) -> float:
    return 0.42 * math.sin(2 * math.pi * 8 * t) + 0.22 * math.sin(2 * math.pi * 24 * t) + 0.12 * math.sin(2 * math.pi * 47 * t)


def _draw_waveform_comparison(page: canvas.Canvas, y_top: float, *, compact: bool = False) -> float:
    """Clean redraw of the four sampling-rate comparisons on source page 5."""
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 11)
    page.drawCentredString(A4[0] / 2, y_top, "不同采样频率下钢琴乐曲的赏析")
    y_top -= 12
    # Reserve a dedicated left label column: formula labels must never intrude
    # into the waveform plotting area, especially the wide f_s=44100 Hz label.
    x, width = 138, A4[0] - 200
    row_height, gap = (34, 5) if compact else (53, 9)
    labels = [r"f_s=44100\,\mathrm{Hz}", r"\frac{f_s}{4}", r"\frac{f_s}{8}", r"\frac{f_s}{16}"]
    sample_counts = [100, 28, 14, 8]
    for row, (label, count) in enumerate(zip(labels, sample_counts)):
        top = y_top - row * (row_height + gap)
        bottom = top - row_height
        middle = (top + bottom) / 2
        page.setStrokeColor(HexColor("#AAB6BD"))
        page.setLineWidth(0.35)
        page.rect(x, bottom, width, row_height, fill=0, stroke=1)
        page.line(x, middle, x + width, middle)
        page.setFillColor(INK)
        page.setFont(style.FONT_SERIF, 8)
        page.drawRightString(x - 12, middle - 3, "0")
        asset, asset_width, asset_height = style._math_metrics(label, 9.6)
        label_height = 12 if compact else 15
        label_width = asset_width * label_height / asset_height
        page.drawImage(ImageReader(str(asset)), 62, middle - label_height / 2, label_width, label_height, mask="auto")
        page.setStrokeColor(TEAL)
        page.setFillColor(TEAL)
        page.setLineWidth(0.65)
        previous = None
        for index in range(count):
            t = index / (count - 1)
            px = x + t * width
            py = middle + _signal_value(t) * row_height * 0.73
            if previous is not None:
                page.line(previous[0], previous[1], px, py)
            page.line(px, middle, px, py)
            page.circle(px, py, 0.95 if row == 0 else 1.35, fill=1, stroke=0)
            previous = (px, py)
    bottom = y_top - 4 * row_height - 3 * gap
    page.setFillColor(HexColor("#52616B"))
    page.setFont(style.FONT_SERIF, 7.8 if compact else 8.6)
    page.drawCentredString(A4[0] / 2, bottom - 12, "同一段信号在采样频率逐步降低时的离散取样比较")
    return bottom - (24 if compact else 30)


def _draw_sampling_representation(page: canvas.Canvas, y_top: float) -> float:
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 11)
    page.drawCentredString(A4[0] / 2, y_top, "连续时间信号与离散时间序列的对应")
    x, width, graph_height, gap = 86, A4[0] - 172, 104, 27
    top_graph_bottom = y_top - 123
    lower_graph_bottom = top_graph_bottom - graph_height - gap
    for base, label, axis_label in [(top_graph_bottom, "x(t)", "t"), (lower_graph_bottom, "x(n)", "n")]:
        mid = base + graph_height / 2
        page.setStrokeColor(BLUE)
        page.setLineWidth(0.55)
        page.line(x, mid, x + width, mid)
        page.line(x + 12, base + 6, x + 12, base + graph_height - 3)
        page.setFillColor(INK)
        page.setFont("Times-Italic", 10)
        page.drawString(x + 15, base + graph_height - 5, label)
        page.drawRightString(x + width, mid - 14, axis_label)
    page.setStrokeColor(TEAL)
    page.setLineWidth(1.0)
    previous = None
    for index in range(180):
        t = index / 179
        px = x + 12 + t * (width - 26)
        py = top_graph_bottom + graph_height / 2 + _signal_value(t) * graph_height * 0.70
        if previous:
            page.line(previous[0], previous[1], px, py)
        previous = (px, py)
    page.setLineWidth(0.7)
    for n in range(10):
        t = n / 9
        px = x + 12 + t * (width - 26)
        continuous_y = top_graph_bottom + graph_height / 2 + _signal_value(t) * graph_height * 0.70
        discrete_y = lower_graph_bottom + graph_height / 2 + _signal_value(t) * graph_height * 0.70
        page.setStrokeColor(HexColor("#B45309"))
        page.line(px, top_graph_bottom + graph_height / 2, px, continuous_y)
        page.line(px, lower_graph_bottom + graph_height / 2, px, discrete_y)
        page.setFillColor(HexColor("#B45309"))
        page.circle(px, continuous_y, 1.7, fill=1, stroke=0)
        page.circle(px, discrete_y, 1.7, fill=1, stroke=0)
        page.setFillColor(INK)
        page.setFont(style.FONT_SANS, 7.6)
        # Keep every horizontal tick label clear of the vertical axis or stem line.
        # The offset changes only the label position, never the sample coordinate.
        page.drawCentredString(px + HORIZONTAL_TICK_LABEL_OFFSET, lower_graph_bottom + graph_height / 2 - 14, str(n))
    x_t = x + 12 + (width - 26) / 9
    page.setStrokeColor(BRASS)
    page.setLineWidth(0.8)
    page.line(x + 12, lower_graph_bottom + graph_height - 13, x_t, lower_graph_bottom + graph_height - 13)
    page.setFillColor(BRASS)
    page.setFont("Times-Italic", 10)
    page.drawCentredString((x + 12 + x_t) / 2, lower_graph_bottom + graph_height - 9, "T")
    return lower_graph_bottom - 21


def _page_origin(page: canvas.Canvas) -> None:
    _start(page, 1)
    y = style.draw_title(page, "1.1 离散时间信号——序列", 774)
    y = style.draw_continuation_title(page, "离散时间信号的由来", y + 7)
    y = style.draw_rich_paragraph(
        page,
        "通过对连续时间信号进行时域采样，可以得到离散时间信号。这样做的直接目的，是便于用计算机对采样数据进行处理；与此同时，面对不同的连续时间信号，还必须回答如何选择采样频率。",
        62, y, A4[0] - 124
    )
    y -= 4
    y = style.draw_rich_paragraph(
        page,
        "离散时间信号（又称序列）是连续时间信号以时间 {{T}} 等间隔采样得到的，{{T}} 称为采样周期或采样间隔。采样频率记为 {{f_s}}，二者满足：",
        62, y, A4[0] - 124
    )
    y = _formula_box(page, r"T=\frac{1}{f_s}", y - 3)
    y = style.draw_rich_paragraph(
        page,
        "采样频率与信号变化的快慢有关。为了从采样值中不失真地保留带限信号的变化细节，采样频率至少应达到信号最高频率分量 {{f_h}} 的两倍：",
        62, y, A4[0] - 124
    )
    y = _formula_box(page, r"f_s\geq 2f_h", y - 3)
    y = style.draw_continuation_title(page, "采样频率与信号细节", y - 4)
    y = style.draw_rich_paragraph(
        page,
        "钢琴音频的谐音成分通常会到几千赫兹。当采样频率选择过小时，钢琴音频中一些原有的高频细节成分不能被保留下来，也就不能保证原有的音质和音效，乐曲听上去会感觉有失真。",
        62, y, A4[0] - 124
    )
    _draw_waveform_comparison(page, y - 3, compact=True)
    page.showPage()


def _page_representation(page: canvas.Canvas) -> None:
    _start(page, 2)
    y = style.draw_title(page, "离散时间信号的表达", 774)
    y = style.draw_rich_paragraph(
        page,
        "一般，采样间隔是均匀的，用 {{x(nT)}} 表示信号在 {{nT}} 点上的值，{{n}} 为整数。由于 {{x(nT)}} 顺序存放在计算机存储器中，我们通常用 {{x(n)}} 表示离散时间信号的序列值。",
        62, y, A4[0] - 124
    )
    y = _draw_sampling_representation(page, y - 7)
    y = style.draw_rich_paragraph(
        page,
        "因此，{{T}} 不只是图上的相邻样点距离：它把序列索引 {{n}} 与实际物理时间联系起来。后续分析中，{{x(n)}} 是以整数 {{n}} 为自变量的离散时间序列，而 {{x(nT)}} 则强调其来自连续时间信号在各采样时刻的取值。",
        62, y, A4[0] - 124
    )
    style.draw_note(page, "记号检查：{{x(t)}} 是连续时间信号；{{x(nT)}} 是采样时刻的取值；{{x(n)}} 是将这些取值按整数序号记录后的离散时间序列。", y - 3)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    output = output_path or root / "full" / "outputs" / "chapter_01_origin_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("数字信号处理讲义：第一章采样导入组件")
    _page_origin(page)
    _page_representation(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
