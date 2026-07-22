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


MODEL_PATH = Path("full/source/chapter_01_sampling_recovery_component.json")
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


def math_label(page: canvas.Canvas, formula: str, center_x: float, center_y: float, size: float = 9) -> None:
    asset, image_width, image_height = style._math_metrics(formula, size)
    draw_height = image_height * 72 / 300
    draw_width = image_width * draw_height / image_height
    page.drawImage(
        ImageReader(str(asset)),
        center_x - draw_width / 2,
        center_y - draw_height / 2,
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


def recovery_spectrum(page: canvas.Canvas, y: float) -> float:
    x, width = 105, 382
    page.setStrokeColor(BLUE)
    page.setLineWidth(0.65)
    page.line(x, y, x + width, y)
    page.line(x + width, y, x + width - 6, y + 3)
    page.line(x + width, y, x + width - 6, y - 3)
    math_label(page, r"\Omega", x + width + 19, y - 2, 10)
    for center in [x + 55, x + 191, x + 327]:
        page.setStrokeColor(TEAL)
        page.setLineWidth(1.1)
        page.line(center - 37, y, center, y + 40)
        page.line(center, y + 40, center + 37, y)
    page.setStrokeColor(BRASS)
    page.setLineWidth(0.9)
    left, right = x + 154, x + 228
    page.line(left, y + 54, left, y + 17)
    page.line(left, y + 54, right, y + 54)
    page.line(right, y + 54, right, y + 17)
    page.setFillColor(BRASS)
    page.setFont(style.FONT_SANS, 9)
    page.drawCentredString((left + right) / 2, y + 62, "重构低通通带")
    math_label(page, r"-\frac{\Omega_s}{2}", left, y - 18, 10)
    math_label(page, r"\frac{\Omega_s}{2}", right, y - 18, 10)
    return y - 30


def sinc_value(value: float) -> float:
    if abs(value) < 1e-8:
        return 1.0
    return math.sin(math.pi * value) / (math.pi * value)


def interpolation_diagram(page: canvas.Canvas, y: float) -> float:
    x, width, height = 90, 414, 76
    page.setStrokeColor(BLUE)
    page.setLineWidth(0.65)
    page.line(x, y, x + width, y)
    page.line(x, y - 8, x, y + height)
    math_label(page, r"t", x + width + 16, y - 2, 9)
    math_label(page, r"g", x - 18, y + height + 4, 9)
    scale_x = width / 6
    scale_y = 51
    page.setStrokeColor(TEAL)
    page.setLineWidth(1.0)
    for shift, opacity in [(-1, HexColor("#77BFC0")), (0, TEAL), (1, HexColor("#77BFC0"))]:
        page.setStrokeColor(opacity)
        previous = None
        for step in range(241):
            value = -3 + 6 * step / 240
            px = x + (value + 3) * scale_x
            py = y + sinc_value(value - shift) * scale_y
            if previous is not None:
                page.line(previous[0], previous[1], px, py)
            previous = (px, py)
    for value, label in [(-1, r"-T"), (0, r"0"), (1, r"T")]:
        px = x + (value + 3) * scale_x
        page.line(px, y - 3, px, y + 3)
        math_label(page, label, px, y - 17, 9)
    page.setFillColor(TEAL)
    page.circle(x + 3 * scale_x, y + scale_y, 2.3, fill=1, stroke=0)
    page.setFillColor(BLUE)
    page.drawCentredString(x + 3 * scale_x, y + height + 13, "以一个采样点为中心的内插函数")
    return y - 27


def page_one(page: canvas.Canvas) -> None:
    start(page, 1)
    y = title(page, "时域采样信号的恢复")
    y = paragraph(page, "当模拟信号满足采样定理、采样后的频谱副本彼此不重叠时，原模拟信号可由采样值唯一恢复。频域中，恢复的核心是保留中央频谱副本并抑制其他重复副本。", y)
    y = section(page, "理想低通重构", y - 2)
    y = recovery_spectrum(page, y - 68)
    y = paragraph(page, "理想重构滤波器的截止角频率取为 {{\\frac{\\Omega_s}{2}}}。实际滤波器不能做到理想的垂直截止，但可在允许误差范围内逼近该通带并实现恢复。", y)
    y = formula_box(page, r"H_r(j\Omega)=T,\quad |\Omega|\leq\frac{\Omega_s}{2}\qquad H_r(j\Omega)=0,\quad |\Omega|>\frac{\Omega_s}{2}", y, 52)
    style.draw_note(page, "恢复的前提是采样前没有产生混叠；重构滤波器只能取出已经分离的频谱副本，不能分开已重叠的成分。", y - 3)
    page.showPage()


def page_two(page: canvas.Canvas) -> None:
    start(page, 2)
    y = title(page, "重构的时域表达")
    y = paragraph(page, "频域中将采样频谱乘以重构滤波器，对应到时域就是将采样信号与滤波器的冲激响应卷积。理想低通滤波器的冲激响应给出了恢复所需的基本波形。", y)
    y = formula_box(page, r"h_r(t)=\frac{T\sin\!\left(\frac{\Omega_s}{2}t\right)}{\pi t}", y, 56)
    y = section(page, "卷积与恢复", y - 2)
    y = formula_box(page, r"y_a(t)=x_s(t)*h_r(t)", y, 48)
    y = paragraph(page, "若 {{y_a(t)}} 与原模拟信号 {{x_a(t)}} 相同，便完成恢复。将采样冲激串代入卷积式，可把恢复过程进一步写成各个样值的加权叠加，这正是内插恢复的形式。", y)
    y = formula_box(page, r"y_a(t)=\sum_{m=-\infty}^{\infty}x_a(mT)\,g(t-mT)", y, 56)
    style.draw_note(page, "这里 {{g(t)}} 是内插函数。每一个样值决定一条移位后的内插曲线，所有曲线相加得到连续时间输出。", y - 3)
    page.showPage()


def page_three(page: canvas.Canvas) -> None:
    start(page, 3)
    y = title(page, "内插函数")
    y = paragraph(page, "把理想低通重构的冲激响应乘以 {{T}}，可得到标准内插函数。它以某个采样点为中心，在其他整数倍采样时刻取零，因此不会改变相邻样值。", y)
    y = formula_box(page, r"g(t)=T h_r(t)=\frac{\sin\!\left(\frac{\pi t}{T}\right)}{\frac{\pi t}{T}}", y, 56)
    y = section(page, "移位内插波形", y - 2)
    y = interpolation_diagram(page, y - 78)
    y = paragraph(page, "对每个 {{m}}，函数 {{g(t-mT)}} 以 {{mT}} 为中心。对应样值 {{x_a(mT)}} 只改变该曲线的幅度；所有移位、加权后的曲线叠加，便在采样点之间补出连续波形。", y)
    style.draw_note(page, "内插不是任意连线，而是由重构滤波器确定的严格函数叠加。", y - 3)
    page.showPage()


def page_four(page: canvas.Canvas) -> None:
    start(page, 4)
    y = title(page, "采样点处的严格插值")
    y = paragraph(page, "内插函数在自身中心采样点的值为一，在其他整数倍采样点的值为零。因此，在任意采样时刻，求和式中只有与该时刻对应的一项保留，其余项全部消失。", y)
    y = formula_box(page, r"g(0)=1,\qquad g(kT)=0\quad(k\in\mathbb{Z},\ k\ne0)", y, 52)
    y = section(page, "样值不变性", y - 2)
    y = formula_box(page, r"y_a(mT)=x_a(mT)", y, 48)
    y = paragraph(page, "这说明恢复后的连续信号准确穿过每一个采样值；而采样点之间的波形由全部加权内插函数的延伸和叠加决定。该性质既解释了“恢复”的含义，也为检查重构公式提供了直接依据。", y)
    style.draw_note(page, "检查恢复式：把 {{t=mT}} 代入，结果必须化为 {{y_a(mT)=x_a(mT)}}；若不能满足，内插函数或比例系数存在错误。", y - 3)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    load_model(root)
    output = output_path or root / "full/outputs/chapter_01_sampling_recovery_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4)
    page.setTitle("数字信号处理讲义：时域采样信号的恢复")
    page_one(page)
    page_two(page)
    page_three(page)
    page_four(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
