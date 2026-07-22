from __future__ import annotations

import json
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sample.tools import build_sample as style


MODEL_PATH = Path("full/source/chapter_01_direct_rewrites.json")
CHAPTER_NAME = "第一章 离散时间信号与系统"
INK = HexColor("#1F2933")
BLUE = HexColor("#123B5D")
BRASS = HexColor(style.ACCENT_BRASS)
PALE = HexColor("#F4F7F8")


def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))


def _start_page(page: canvas.Canvas, number: int) -> None:
    style.draw_header(page, CHAPTER_NAME)
    style.draw_footer(page, number)


def _finish_page(page: canvas.Canvas) -> None:
    page.showPage()


def _math_box(page: canvas.Canvas, source: str, x: float, y_top: float, width: float, *, height: float = 38, size: float = 11) -> float:
    asset, image_width, image_height = style._math_metrics(source, size)
    drawn_height = min(height - 12, image_height * 72 / 300)
    drawn_width = image_width * drawn_height / image_height
    if drawn_width > width - 16:
        scale = (width - 16) / drawn_width
        drawn_width *= scale
        drawn_height *= scale
    bottom = y_top - height
    page.setFillColor(PALE)
    page.roundRect(x, bottom, width, height, 3, fill=1, stroke=0)
    page.drawImage(ImageReader(str(asset)), x + (width - drawn_width) / 2, bottom + (height - drawn_height) / 2, drawn_width, drawn_height, mask="auto")
    return bottom


def _draw_stem(page: canvas.Canvas, x: float, y: float, width: float, height: float, title: str, series: list[list[int]], n_min: int, n_max: int, subtitle: str) -> None:
    left, right, base = x + 20, x + width - 10, y + 26
    page.setStrokeColor(BLUE)
    page.setFillColor(INK)
    page.setLineWidth(0.7)
    page.line(left, base, right, base)
    page.line(left + 6, y + 10, left + 6, y + height - 12)
    page.setFont(style.FONT_SERIF, 10)
    page.drawString(x + 6, y + height - 3, title)
    page.setFont(style.FONT_SANS, 8.2)
    page.setFillColor(HexColor("#52616B"))
    page.drawCentredString(x + width / 2, y + 1, subtitle)
    scale_x = (right - (left + 6)) / (n_max - n_min)
    for n in range(n_min, n_max + 1):
        px = left + 6 + (n - n_min) * scale_x
        page.setStrokeColor(BLUE)
        page.line(px, base - 3, px, base + 3)
        page.setFillColor(INK)
        page.setFont(style.FONT_SANS, 7.2)
        page.drawCentredString(px, base - 13, str(n))
    for n, value in series:
        px = left + 6 + (n - n_min) * scale_x
        top = base + value * 20
        page.setStrokeColor(HexColor("#0E7490"))
        page.setLineWidth(1.25)
        page.line(px, base, px, top)
        page.setFillColor(HexColor("#0E7490"))
        page.circle(px, top, 2.2, fill=1, stroke=0)
        page.setFillColor(INK)
        page.setFont(style.FONT_SANS, 7.5)
        page.drawCentredString(px, top + 5, str(value))


def _draw_code(page: canvas.Canvas, code: str, x: float, y_top: float, width: float) -> float:
    lines = code.splitlines()
    leading = 12.2
    height = len(lines) * leading + 22
    bottom = y_top - height
    page.setFillColor(HexColor("#F7F8F8"))
    page.setStrokeColor(HexColor("#D8DEE2"))
    page.roundRect(x, bottom, width, height, 3, fill=1, stroke=1)
    page.setFillColor(INK)
    page.setFont(style.FONT_SANS, 8.6)
    y = y_top - 15
    for line in lines:
        page.drawString(x + 12, y, line)
        y -= leading
    return bottom


def _draw_signal_chain(page: canvas.Canvas, labels: list[str]) -> None:
    width, _ = A4
    x0, y0, box_w, box_h, gap = 54, 390, 91, 118, 10
    centers = []
    for index, label in enumerate(labels):
        x = x0 + index * (box_w + gap)
        centers.append((x, x + box_w))
        page.setFillColor(HexColor("#FBFAF5"))
        page.setStrokeColor(BLUE)
        page.setLineWidth(1.0)
        page.roundRect(x, y0, box_w, box_h, 3, fill=1, stroke=1)
        page.setFillColor(INK)
        page.setFont(style.FONT_SANS, 11.5)
        pieces = label.replace(" ", "").replace("数字信号处理器", "数字\n信号\n处理器").replace("前置预滤波器", "前置\n预滤波器").replace("模拟低通滤波器", "模拟\n低通\n滤波器").replace("转换器", "\n转换器")
        line_y = y0 + box_h / 2 + (pieces.count("\n") * 7)
        for piece in pieces.splitlines():
            page.drawCentredString(x + box_w / 2, line_y, piece)
            line_y -= 18
        if index < len(labels) - 1:
            page.setStrokeColor(BRASS)
            page.setFillColor(BRASS)
            page.setLineWidth(1.2)
            start = x + box_w
            end = x + box_w + gap
            page.line(start, y0 + box_h / 2, end, y0 + box_h / 2)
            page.line(end, y0 + box_h / 2, end - 4, y0 + box_h / 2 + 3)
            page.line(end, y0 + box_h / 2, end - 4, y0 + box_h / 2 - 3)
    page.setFillColor(INK)
    page.setFont("Times-Italic", 11)
    page.drawString(31, y0 + box_h / 2 + 7, r"x_a(t)")
    page.drawCentredString((centers[1][1] + centers[2][0]) / 2, y0 + box_h / 2 + 18, "x(n)")
    page.drawCentredString((centers[2][1] + centers[3][0]) / 2, y0 + box_h / 2 + 18, "y(n)")
    page.drawString(width - 47, y0 + box_h / 2 + 7, r"y_a(t)")


def _page_shift(page: canvas.Canvas, model: dict) -> None:
    _start_page(page, 1)
    y = style.draw_title(page, "序列的移位", 774)
    y = style.draw_rich_paragraph(page, "设有一序列 {{x(n)}}。当 {{m>0}} 时，{{x(n-m)}} 表示 {{x(n)}} 逐项右移 {{m}} 位后得到的序列；{{x(n+m)}} 表示 {{x(n)}} 逐项左移 {{m}} 位后得到的序列。", 62, y, A4[0] - 124)
    y = _math_box(page, r"y(n)=x(n\pm m)", 62, y - 3, A4[0] - 124)
    y -= 18
    diagram = model["blocks"][0]["diagram"]
    _draw_stem(page, 48, 315, 160, 165, "x(n)", diagram["series"], -1, 4, "原序列")
    _draw_stem(page, 218, 315, 160, 165, "x(n-1)", diagram["right_shift"], 0, 5, "右移一位：滞后／延时")
    _draw_stem(page, 388, 315, 160, 165, "x(n+1)", diagram["left_shift"], -3, 3, "左移一位：超前")
    style.draw_rich_paragraph(page, "例如 {{n=3}} 时，{{x(n-1)=x(2)=3}}。判断移位方向时，应始终以自变量中 {{n}} 的变化为准：减去正数是延时，加上正数是超前。", 62, 274, A4[0] - 124)
    _finish_page(page)


def _page_difference(page: canvas.Canvas) -> None:
    _start_page(page, 2)
    y = style.draw_title(page, "线性常系数差分方程的迭代求解", 774)
    y = style.draw_rich_paragraph(page, "考虑系统差分方程 {{y(n)-ay(n-1)=x(n)}}，令 {{x(n)=\\delta(n)}}，分别在两种边界条件下用迭代法求单位抽样响应。", 62, y, A4[0] - 124)
    y = _math_box(page, r"y(n)-ay(n-1)=x(n)", 62, y - 2, A4[0] - 124)
    left, right, top, column_w = 62, 310, y - 10, 223
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 12.5)
    page.drawString(left, top, "因果系统")
    page.drawString(right, top, "非因果系统")
    page.setStrokeColor(BRASS)
    page.setLineWidth(0.7)
    page.line(left, top - 8, left + 118, top - 8)
    page.line(right, top - 8, right + 128, top - 8)
    style.draw_rich_paragraph(page, "边界条件：{{n<0}} 时，{{h(n)=0}}。", left, top - 34, column_w, size=9.4, leading=15)
    style.draw_rich_paragraph(page, "边界条件：{{n>0}} 时，{{h(n)=0}}。", right, top - 34, column_w, size=9.4, leading=15)
    ly = _math_box(page, r"h(0)=ah(-1)+\delta(0)=1", left, top - 68, column_w, height=31, size=9)
    ly = _math_box(page, r"h(1)=ah(0)+\delta(1)=a", left, ly - 7, column_w, height=31, size=9)
    ly = _math_box(page, r"h(2)=ah(1)+\delta(2)=a^2", left, ly - 7, column_w, height=31, size=9)
    ly = _math_box(page, r"h(n)=a^n,\quad n\geq0", left, ly - 7, column_w, height=31, size=9)
    ry = _math_box(page, r"h(0)=a^{-1}[h(1)-\delta(1)]=0", right, top - 68, column_w, height=31, size=8.7)
    ry = _math_box(page, r"h(-1)=a^{-1}[h(0)-\delta(0)]=-a^{-1}", right, ry - 7, column_w, height=31, size=8.3)
    ry = _math_box(page, r"h(-2)=a^{-1}h(-1)=-a^{-2}", right, ry - 7, column_w, height=31, size=8.8)
    ry = _math_box(page, r"h(-n)=-a^{-n},\quad n\geq1", right, ry - 7, column_w, height=31, size=8.5)
    ly = _math_box(page, r"h(n)=a^n u(n)", left, ly - 20, column_w, height=38, size=10)
    ry = _math_box(page, r"h(n)=-a^n u(-n-1)", right, ry - 20, column_w, height=38, size=9.5)
    style.draw_rich_paragraph(page, "该响应显然因果；当 {{|a|<1}} 时，还是稳定系统。", left, ly - 22, column_w, size=9.4, leading=15)
    style.draw_rich_paragraph(page, "该响应显然非因果，但差分方程与左栏完全相同。", right, ry - 22, column_w, size=9.4, leading=15)
    style.draw_rich_paragraph(page, "同一常系数线性差分方程并不自动限定因果性；必须同时给出边界条件或系统初始条件。", 62, 207, A4[0] - 124, size=9.8, leading=16)
    _finish_page(page)


def _page_signal_chain(page: canvas.Canvas, model: dict) -> None:
    _start_page(page, 3)
    y = style.draw_title(page, "模拟信号的数字处理方法", 774)
    y = style.draw_rich_paragraph(page, "模拟输入 {{x_a(t)}} 依次经过前置预滤波、A/D 转换、数字处理、D/A 转换和模拟低通滤波，得到模拟输出 {{y_a(t)}}。其中数字信号处理器接收 {{x(n)}} 并输出 {{y(n)}}。", 62, y, A4[0] - 124)
    _draw_signal_chain(page, model["blocks"][3]["signal_chain"]["blocks"])
    y = style.draw_rich_paragraph(page, "数字信号处理器可对输入信号 {{x(n)}} 进行滤波、降噪、增强、变换、压缩和识别等处理，最终形成输出 {{y(n)}}。前置预滤波器用于在 A/D 转换前限制带宽；输出端的模拟低通滤波器用于平滑恢复后的连续信号。", 62, 330, A4[0] - 124)
    style.draw_note(page, "阅读信号处理链时，先区分连续时间信号 {{x_a(t)}}、{{y_a(t)}} 与离散时间序列 {{x(n)}}、{{y(n)}}；A/D 与 D/A 两侧的信号表示及滤波职责不能混淆。", y - 12)
    _finish_page(page)


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    model = load_model(root)
    output = output_path or root / "full" / "outputs" / "chapter_01_direct_rewrites.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4)
    page.setTitle("数字信号处理讲义：第一章直接转写块")
    _page_shift(page, model)
    _page_difference(page)
    _page_signal_chain(page, model)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
