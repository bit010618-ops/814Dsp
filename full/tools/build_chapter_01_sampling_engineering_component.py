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


MODEL_PATH = Path("full/source/chapter_01_sampling_engineering_component.json")
CHAPTER = "第一章 离散时间信号与系统"
PALE = HexColor("#F4F7F8")
BLUE = HexColor("#123B5D")
TEAL = HexColor("#0F8B8D")
RED = HexColor("#B13A3A")
BRASS = HexColor("#B08D57")


def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))


def start(page: canvas.Canvas, number: int) -> None:
    style.draw_header(page, CHAPTER)
    style.draw_footer(page, number)


def title(page: canvas.Canvas, text: str, y: float = 774) -> float:
    return style.draw_title(page, text, y)


def section(page: canvas.Canvas, text: str, y: float) -> float:
    return style.draw_continuation_title(page, text, y)


def paragraph(page: canvas.Canvas, text: str, y: float) -> float:
    return style.draw_rich_paragraph(page, text, 62, y, A4[0] - 124)


def formula_box(page: canvas.Canvas, formula: str, y: float, height: float = 50) -> float:
    asset, image_width, image_height = style._math_metrics(formula, style.DISPLAY_FORMULA_SIZE)
    draw_height = min(height - 12, image_height * 72 / 300)
    draw_width = image_width * draw_height / image_height
    limit = A4[0] - 148
    if draw_width > limit:
        draw_height = draw_height * limit / draw_width
        draw_width = limit
    page.setFillColor(PALE)
    page.roundRect(62, y - height, A4[0] - 124, height, 3, fill=1, stroke=0)
    page.drawImage(
        ImageReader(str(asset)),
        (A4[0] - draw_width) / 2,
        y - height + (height - draw_height) / 2,
        draw_width,
        draw_height,
        mask="auto",
    )
    return y - height - 12


def math_label(page: canvas.Canvas, formula: str, center_x: float, baseline_y: float, size: float = 9) -> None:
    asset, image_width, image_height = style._math_metrics(formula, size)
    draw_height = image_height * 72 / 300
    draw_width = image_width * draw_height / image_height
    page.drawImage(
        ImageReader(str(asset)),
        center_x - draw_width / 2,
        baseline_y - draw_height / 2,
        draw_width,
        draw_height,
        mask="auto",
    )


def arrow(page: canvas.Canvas, x1: float, y1: float, x2: float, y2: float) -> None:
    page.setStrokeColor(BLUE)
    page.setLineWidth(0.8)
    page.line(x1, y1, x2, y2)
    page.line(x2, y2, x2 - 6, y2 + 3)
    page.line(x2, y2, x2 - 6, y2 - 3)


def process_chain(page: canvas.Canvas, y: float) -> float:
    labels = ["模拟输入", "抗混叠滤波", "模数转换", "离散序列"]
    x0, width, height, gap = 68, 103, 42, 27
    page.setFont(style.FONT_SANS, 10)
    for index, label in enumerate(labels):
        x = x0 + index * (width + gap)
        page.setStrokeColor(BRASS)
        page.setFillColor(PALE)
        page.roundRect(x, y - height, width, height, 3, fill=1, stroke=1)
        page.setFillColor(BLUE)
        page.drawCentredString(x + width / 2, y - 25, label)
        if index < len(labels) - 1:
            arrow(page, x + width + 4, y - height / 2, x + width + gap - 4, y - height / 2)
    return y - height - 18


def spectrum_axis(page: canvas.Canvas, x: float, y: float, width: float, label: str) -> None:
    page.setStrokeColor(BLUE)
    page.setLineWidth(0.65)
    page.line(x, y, x + width, y)
    page.line(x + width, y, x + width - 6, y + 3)
    page.line(x + width, y, x + width - 6, y - 3)
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SERIF, 9)
    page.drawString(x + width + 7, y - 4, label)


def tent(page: canvas.Canvas, x: float, y: float, half_width: float, height: float, color) -> None:
    page.setStrokeColor(color)
    page.setLineWidth(1.15)
    page.line(x - half_width, y, x, y + height)
    page.line(x, y + height, x + half_width, y)


def anti_alias_spectrum(page: canvas.Canvas, y: float) -> float:
    x, width = 90, 404
    spectrum_axis(page, x, y, width, "f")
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 9)
    page.drawString(x, y + 61, "带宽未限制：频谱副本相交")
    for center in [x + 104, x + 202, x + 300]:
        tent(page, center, y, 79, 41, RED)
    page.setFillColor(RED)
    page.drawCentredString(x + 202, y + 48, "混叠")
    lower = y - 102
    spectrum_axis(page, x, lower, width, "f")
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 9)
    page.drawString(x, lower + 61, "先限制输入带宽：频谱副本分离")
    for center in [x + 82, x + 202, x + 322]:
        tent(page, center, lower, 42, 41, TEAL)
    page.setFillColor(TEAL)
    page.drawCentredString(x + 202, lower + 48, "可恢复")
    return lower - 23


def bandpass_spectrum(page: canvas.Canvas, y: float) -> float:
    x, width = 92, 400
    spectrum_axis(page, x, y, width, "f")
    left, right = x + 230, x + 332
    page.setStrokeColor(TEAL)
    page.setFillColor(HexColor("#DCEFF0"))
    page.rect(left, y, right - left, 44, fill=1, stroke=1)
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SERIF, 9)
    page.drawCentredString((left + right) / 2, y + 49, "带通频带")
    page.setStrokeColor(BRASS)
    page.line(left, y - 7, right, y - 7)
    page.line(left, y - 7, left + 4, y - 4)
    page.line(left, y - 7, left + 4, y - 10)
    page.line(right, y - 7, right - 4, y - 4)
    page.line(right, y - 7, right - 4, y - 10)
    math_label(page, r"\Delta f_0", (left + right) / 2, y - 17, 9)
    math_label(page, r"f_h-\Delta f_0", left, y - 34, 9)
    math_label(page, r"f_h", right, y - 34, 9)
    math_label(page, r"f_0", (left + right) / 2, y - 51, 9)
    return y - 68


def page_one(page: canvas.Canvas) -> None:
    start(page, 1)
    y = title(page, "抗混叠滤波")
    y = paragraph(page, "实际的模拟信号在进入模数转换器之前，通常先经过抗混叠滤波器。它的任务是限制输入带宽，使采样后的频谱副本彼此分离，从而避免不可逆的混叠。", y)
    y = process_chain(page, y - 12)
    y = section(page, "采样前的带宽约束", y - 2)
    y = paragraph(page, "若滤波后的模拟输入最高频率为 {{f_h}}，则选择采样频率时应满足采样定理。工程上，滤波器还需要留出过渡带，因此截止频率通常应低于折叠频率，而不应刚好压在临界位置。", y)
    y = formula_box(page, r"f_h\leq\frac{f_s}{2}\qquad\Longleftrightarrow\qquad \Omega_h\leq\frac{\Omega_s}{2}", y, 50)
    style.draw_note(page, "抗混叠滤波器位于采样之前；采样后再滤除混叠，已经无法恢复被重叠的频谱成分。", y - 3)
    page.showPage()


def page_two(page: canvas.Canvas) -> None:
    start(page, 2)
    y = title(page, "抗混叠滤波的频域作用")
    y = paragraph(page, "采样会使模拟频谱按 {{f_s}} 为间隔重复出现。若原信号带宽过宽，相邻副本会相交；先用低通滤波器限制输入带宽后，副本之间保留空隙，才可用重构滤波器取回所需频带。", y)
    y = section(page, "频谱副本的分离", y - 2)
    y = anti_alias_spectrum(page, y - 70)
    y = paragraph(page, "上图的差别不在于采样操作本身，而在于采样前是否已经满足带宽条件。混叠一旦发生，重叠区域来自哪些原始频率成分便不再能够唯一判定。", y)
    style.draw_note(page, "判断顺序：先看输入最高频率，再比较 {{f_h}} 与 {{\\frac{f_s}{2}}}；若不满足，先设计前置滤波而不是事后补救。", y - 3)
    page.showPage()


def page_three(page: canvas.Canvas) -> None:
    start(page, 3)
    y = title(page, "带通信号的采样参数")
    y = paragraph(page, "带通信号的频谱只占据某一段非零频率附近的区间，而不是从零频率开始。记最高频率为 {{f_h}}、频带宽度为 {{\\Delta f_0}}，则频带中心频率由右端点与带宽共同确定。", y)
    y = formula_box(page, r"f_0=f_h-\frac{\Delta f_0}{2}", y, 48)
    y = section(page, "频带位置与带宽", y - 2)
    y = bandpass_spectrum(page, y - 66)
    y = paragraph(page, "带通采样的关键不只在于最高频率 {{f_h}}，还在于有效带宽 {{\\Delta f_0}} 与频带所在位置。合理选择采样频率时，可让重复后的频带交错排列而不发生重叠。", y)
    style.draw_note(page, "带通信号的采样率可以与带宽相关，但仍必须保证所有频谱副本之间没有相交。", y - 3)
    page.showPage()


def page_four(page: canvas.Canvas) -> None:
    start(page, 4)
    y = title(page, "带通信号的无混叠采样")
    y = paragraph(page, "当带通信号的最高频率恰好是带宽的整数倍时，可以直接选用两倍带宽作为采样频率。采样后的频谱副本不重叠，并可由适当的带通滤波器恢复原信号。", y)
    y = formula_box(page, r"f_h=r\Delta f_0,\quad r\in\mathbb{Z}\qquad\Longrightarrow\qquad f_s=2\Delta f_0", y, 52)
    y = section(page, "非整数情形", y - 2)
    y = paragraph(page, "若 {{\\frac{f_h}{\\Delta f_0}}} 不是整数，则将频带下端向低频方向延伸，构造一个不小于原带宽的 {{\\Delta f_0'}}，使最高频率成为该扩展带宽的整数倍；随后按相同方法选择采样频率。", y)
    y = formula_box(page, r"\Delta f_0'=\frac{f_h}{r}\geq\Delta f_0,\qquad r\in\mathbb{Z},\qquad f_s=2\Delta f_0'", y, 54)
    y = paragraph(page, "这里的扩展只用于确定可行的采样频率和滤波器通带，并不表示原信号新增了频率成分。恢复时仍使用与原频带相匹配的带通滤波器选出所需部分。", y)
    style.draw_note(page, "做带通采样题时，先写清 {{f_h}}、{{\\Delta f_0}} 和 {{f_0}}；再检查整数倍条件，最后说明采样后用带通滤波器恢复。", y - 3)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    load_model(root)
    output = output_path or root / "full/outputs/chapter_01_sampling_engineering_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4)
    page.setTitle("数字信号处理讲义：抗混叠滤波与带通信号采样")
    page_one(page)
    page_two(page)
    page_three(page)
    page_four(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
