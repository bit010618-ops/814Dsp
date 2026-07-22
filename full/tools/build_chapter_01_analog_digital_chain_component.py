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


MODEL_PATH = Path("full/source/chapter_01_analog_digital_chain_component.json")
CHAPTER = "第一章 离散时间信号与系统"
PALE = HexColor("#F4F7F8")
BLUE = HexColor("#123B5D")
TEAL = HexColor("#0F8B8D")
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
        draw_height *= limit / draw_width
        draw_width = limit
    page.setFillColor(PALE)
    page.roundRect(62, y - height, A4[0] - 124, height, 3, fill=1, stroke=0)
    page.drawImage(ImageReader(str(asset)), (A4[0] - draw_width) / 2, y - height + (height - draw_height) / 2, draw_width, draw_height, mask="auto")
    return y - height - 12


def math_label(page: canvas.Canvas, formula: str, center_x: float, center_y: float, size: float = 9) -> None:
    asset, image_width, image_height = style._math_metrics(formula, size)
    draw_height = image_height * 72 / 300
    draw_width = image_width * draw_height / image_height
    page.drawImage(ImageReader(str(asset)), center_x - draw_width / 2, center_y - draw_height / 2, draw_width, draw_height, mask="auto")


def arrow(page: canvas.Canvas, x1: float, y1: float, x2: float, y2: float) -> None:
    page.setStrokeColor(BLUE)
    page.setLineWidth(0.8)
    page.line(x1, y1, x2, y2)
    page.line(x2, y2, x2 - 6, y2 + 3)
    page.line(x2, y2, x2 - 6, y2 - 3)


def process_box(page: canvas.Canvas, x: float, y: float, width: float, text: str) -> None:
    page.setFillColor(PALE)
    page.setStrokeColor(TEAL)
    page.setLineWidth(0.75)
    page.roundRect(x, y, width, 39, 3, fill=1, stroke=1)
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 8.6)
    lines = text.split("\n")
    for index, line in enumerate(lines):
        page.drawCentredString(x + width / 2, y + 22 - index * 11, line)


def process_chain(page: canvas.Canvas, y: float) -> float:
    boxes = [
        (63, 72, "前置预\n滤波器"),
        (151, 64, "模数\n转换"),
        (231, 78, "数字信号\n处理器"),
        (325, 64, "数模\n转换"),
        (405, 72, "模拟低通\n滤波器"),
    ]
    base = y - 40
    for x, width, label in boxes:
        process_box(page, x, base, width, label)
    for (x, width, _label), (next_x, _next_width, _next_label) in zip(boxes, boxes[1:]):
        arrow(page, x + width + 3, base + 19, next_x - 4, base + 19)
    math_label(page, r"x_a(t)", 48, base + 20, 10)
    arrow(page, 61, base + 19, 62, base + 19)
    math_label(page, r"x(n)", 222, base + 58, 10)
    math_label(page, r"y(n)", 315, base + 58, 10)
    math_label(page, r"y_a(t)", 497, base + 20, 10)
    arrow(page, 477, base + 19, 491, base + 19)
    page.setFillColor(BRASS)
    page.setFont(style.FONT_SANS, 8.4)
    page.drawCentredString(275, base - 17, "模拟域                              数字域                              模拟域")
    return base - 35


def zero_order_hold(page: canvas.Canvas, y: float) -> float:
    x, width, height = 95, 395, 85
    page.setStrokeColor(BLUE)
    page.setLineWidth(0.65)
    page.line(x, y, x + width, y)
    page.line(x, y - 25, x, y + height)
    math_label(page, r"t", x + width + 14, y - 2, 9)
    math_label(page, r"y_0(t)", x - 18, y + height + 5, 9)
    samples = [(0, 22), (1, 48), (2, 34), (3, 62), (4, 45)]
    step = width / 5
    page.setStrokeColor(TEAL)
    page.setLineWidth(1.15)
    for index, (_, level) in enumerate(samples):
        left = x + index * step
        right = x + (index + 1) * step
        page.line(left, y + level, right, y + level)
        if index < len(samples) - 1:
            page.line(right, y + level, right, y + samples[index + 1][1])
        page.setFillColor(TEAL)
        page.circle(left, y + level, 2.1, fill=1, stroke=0)
    page.setFillColor(TEAL)
    page.circle(x + len(samples) * step, y + samples[-1][1], 2.1, fill=1, stroke=0)
    for index, label in enumerate([r"0", r"T", r"2T", r"3T", r"4T"]):
        px = x + index * step
        page.setStrokeColor(BLUE)
        page.line(px, y - 3, px, y + 3)
        math_label(page, label, px, y - 16, 8.5)
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 8.8)
    page.drawCentredString(x + width / 2, y + height + 12, "零阶保持：每个样值保持到下一采样时刻")
    return y - 31


def page_one(page: canvas.Canvas) -> None:
    start(page, 1)
    y = title(page, "模拟信号的数字处理链路")
    y = paragraph(page, "模拟信号进入数字处理系统前，需要先限制其有效频带；经过模数转换后，信号成为可由数字系统处理的离散序列。处理结果再经数模转换与模拟低通滤波，恢复为连续时间输出。", y)
    y = section(page, "从模拟输入到模拟输出", y - 2)
    y = process_chain(page, y - 44)
    y = formula_box(page, r"x_a(t)\ \longrightarrow\ x(n)\ \longrightarrow\ y(n)\ \longrightarrow\ y_a(t)", y, 52)
    y = paragraph(page, "前置预滤波器先去除可能在采样后折叠到有效频带内的高频成分。若输入信号的最高角频率为 {{\\Omega_c}}，采样角频率需满足 {{\\Omega_s\\geq2\\Omega_c}}；这一条件保证后续数字处理建立在无混叠的离散表示上。", y)
    style.draw_note(page, "数字信号处理器可实现滤波、降噪、增强、变换、压缩和识别等任务。它处理的是离散序列，而不是直接对连续波形进行运算。", y - 3)
    page.showPage()


def page_two(page: canvas.Canvas) -> None:
    start(page, 2)
    y = title(page, "采样、量化与编码")
    y = paragraph(page, "模数转换把连续时间输入变成可存储、可计算的数字序列。它先在等间隔时刻取得样值，再把连续幅度映射到有限个量化等级，并用二进制码字表示量化后的结果。", y)
    y = section(page, "离散化的三个环节", y - 2)
    y = formula_box(page, r"x(n)=x_a(nT),\qquad q(n)=Q\left[x(n)\right]", y, 56)
    y = paragraph(page, "采样决定信号在时间轴上的离散位置；量化决定每个样值可取的幅度等级；编码则把量化等级写成数字系统可以传输、存储和运算的码字。三者共同完成从连续量到数字表示的转换。", y)
    y = section(page, "前置预滤波的作用", y - 2)
    y = paragraph(page, "实际输入往往含有目标频带之外的成分。前置预滤波器应在采样前抑制这些成分，以防它们在频谱复制时混入目标频带；这一环节不能由采样后的数字处理完全补救。", y)
    style.draw_note(page, "学习时应区分：采样频率决定频谱副本之间的间隔；量化等级决定幅度表示的精细程度。两者对应不同的失真来源。", y - 3)
    page.showPage()


def page_three(page: canvas.Canvas) -> None:
    start(page, 3)
    y = title(page, "数模转换与零阶保持")
    y = paragraph(page, "数字处理器的输出 {{y(n)}} 仍是离散序列。数模转换器把各个数值依次送入保持电路；最常见的零阶保持方式是在两个采样时刻之间维持前一个样值不变，因此得到阶梯状的连续时间波形。", y)
    y = section(page, "零阶保持输出", y - 2)
    y = zero_order_hold(page, y - 76)
    y = paragraph(page, "阶梯波形包含目标低频成分，也包含由保持过程带来的高频成分。理想数模恢复可用满足重构条件的低通滤波器直接得到连续输出；实际系统则在保持器之后配置模拟平滑滤波器，使输出波形更加连续。", y)
    y = formula_box(page, r"y(n)\ \longrightarrow\ y_0(t)\ \longrightarrow\ y_a(t)", y, 50)
    style.draw_note(page, "保持器负责把离散数值变为可供模拟电路处理的阶梯波形；平滑滤波器负责抑制不需要的高频分量。两者的功能不能混为一谈。", y - 3)
    page.showPage()


def page_four(page: canvas.Canvas) -> None:
    start(page, 4)
    y = title(page, "采样间隔与实际恢复")
    y = paragraph(page, "在相同的模拟低通滤波条件下，采样间隔 {{T}} 越小，零阶保持的每个台阶越短，阶梯波形对连续信号变化的跟随越细致。采样点更密并不替代重构滤波，但会降低实际恢复时的近似误差。", y)
    y = formula_box(page, r"T\downarrow\quad\Longrightarrow\quad f_s=\frac{1}{T}\uparrow", y, 54)
    y = section(page, "处理链的检查顺序", y - 2)
    y = paragraph(page, "先检查输入是否已带限、采样频率是否满足无混叠条件；再检查量化和编码是否形成正确的数字序列；最后检查数模转换、保持与平滑滤波是否按正确次序连接。任何一个环节失配，都会使最终模拟输出偏离希望得到的波形。", y)
    style.draw_note(page, "本节小结：数字处理并不是脱离模拟环节的独立过程。抗混叠、采样、量化编码、数字运算、数模转换和恢复滤波共同构成一条完整链路。让未来的你感谢曾经努力拼搏的自己。", y - 3)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    load_model(root)
    output = output_path or root / "full/outputs/chapter_01_analog_digital_chain_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4)
    page.setTitle("数字信号处理讲义：模拟信号的数字处理方法")
    page_one(page)
    page_two(page)
    page_three(page)
    page_four(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
