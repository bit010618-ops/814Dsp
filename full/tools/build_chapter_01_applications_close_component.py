from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from sample.tools import build_sample as style
from full.tools.build_chapter_01_analog_digital_chain_component import formula_box


MODEL_PATH = Path("full/source/chapter_01_applications_close_component.json")
CHAPTER = "第一章 离散时间信号与系统"
BLUE = HexColor("#123B5D")
TEAL = HexColor("#0F8B8D")
BRASS = HexColor("#B08D57")
PALE = HexColor("#F4F7F8")


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


def wheel(page: canvas.Canvas, cx: float, cy: float, radius: float, marker_angle: float) -> None:
    page.setStrokeColor(HexColor("#B6342D"))
    page.setLineWidth(2.3)
    page.circle(cx, cy, radius, stroke=1, fill=0)
    page.setStrokeColor(TEAL)
    page.setLineWidth(1.25)
    for index in range(8):
        angle = math.radians(index * 45)
        page.line(cx, cy, cx + radius * 0.83 * math.cos(angle), cy + radius * 0.83 * math.sin(angle))
    page.setFillColor(PALE)
    page.setStrokeColor(HexColor("#B6342D"))
    page.setLineWidth(1.6)
    page.circle(cx, cy, radius * 0.36, stroke=1, fill=1)
    angle = math.radians(marker_angle)
    mx, my = cx + radius * 0.67 * math.cos(angle), cy + radius * 0.67 * math.sin(angle)
    page.setFillColor(BLUE)
    page.setStrokeColor(BLUE)
    page.circle(mx, my, radius * 0.09, stroke=0, fill=1)


def page_one(page: canvas.Canvas) -> None:
    start(page, 1)
    y = title(page, "从采样定理到信息论")
    y = paragraph(page, "采样问题的核心在于：在满足条件时，离散样值足以恢复连续信号；不满足条件时，不同连续信号可能留下同一组样值。这个结论奠定了数字信号处理对连续世界进行离散表示的基础。", y)
    y = section(page, "奈奎斯特的采样思想", y - 2)
    y = paragraph(page, "哈利·奈奎斯特（1889—1976）在 1927 年提出：对带宽有限的模拟信号进行采样，若要由样值准确恢复原信号，采样频率至少应为原信号最高频率的两倍。采样频率的一半称为奈奎斯特频率。", y)
    y = formula_box(page, r"f_s\geq2f_h,\qquad f_N=\frac{f_s}{2}", y, 54)
    y = section(page, "香农的推广", y - 2)
    y = paragraph(page, "克劳德·香农（1916—2001）建立现代信息论，并在带宽、噪声和信息传输速率的研究中发展了相关理论。采样定理通常也称为奈奎斯特—香农采样定理。", y)
    style.draw_note(page, "记忆主线：奈奎斯特给出采样恢复的频率条件；香农将信号、带宽、噪声与信息传输的理论框架系统化。", y - 3)
    page.showPage()


def page_two(page: canvas.Canvas) -> None:
    start(page, 2)
    y = title(page, "同一组样值未必对应唯一连续信号")
    y = paragraph(page, "设离散序列 {{x(n)=sin(0.1\\pi n)}} 来自在 {{f_s=1000\\,Hz}} 下对某个连续正弦信号的采样。虽然样值的变化规律已经确定，但若不额外限制连续信号的频带，仅凭这些样值仍无法唯一判断原连续信号。", y)
    y = formula_box(page, r"x(n)=\sin(0.1\pi n),\qquad T=\frac{1}{f_s}=1\ \mathrm{ms}", y, 56)
    y = section(page, "两个给出相同样值的连续信号", y - 2)
    y = formula_box(page, r"\left.\sin(100\pi t)\right|_{t=nT}=\sin(0.1\pi n)", y, 48)
    y = formula_box(page, r"\left.\sin(2100\pi t)\right|_{t=nT}=\sin(2.1\pi n)=\sin(0.1\pi n)", y, 54)
    y = paragraph(page, "前者的频率为 {{50\\,Hz}}，后者的频率为 {{1050\\,Hz}}；在该采样频率下，它们的样值完全相同。这正是频谱复制造成的歧义：连续信号必须先满足带限条件，才能从样值中唯一恢复。", y)
    style.draw_note(page, "结论：离散序列本身不自动携带“原连续信号唯一”的保证；唯一性来自带限假设与足够高的采样频率。", y - 3)
    page.showPage()


def page_three(page: canvas.Canvas) -> None:
    start(page, 3)
    y = title(page, "车轮现象：视觉中的混叠")
    y = paragraph(page, "摄像机以固定帧率记录转动的车轮，相邻帧之间只能看到有限次状态。当车轮在一帧间隔内转过接近一个辐条间距时，下一帧的图案会与上一帧十分相似，于是视觉上可能出现车轮静止或反向转动。", y)
    y = section(page, "离散观察下的不同表象", y - 2)
    wheel(page, 180, y - 122, 78, 90)
    wheel(page, 420, y - 122, 78, 45)
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 11)
    page.drawCentredString(180, y - 220, "帧间转过一个辐条间距：看起来近似静止")
    page.drawCentredString(420, y - 220, "帧间略少转一些：看起来反向转动")
    y -= 257
    y = paragraph(page, "该现象与信号采样中的混叠本质相同：连续变化被离散时刻观察后，原本不同的变化过程可能映射为难以区分的离散序列。提高观察频率或限制原信号带宽，才能消除这种歧义。", y)
    style.draw_note(page, "车轮不是“真的倒转”，而是离散观察带来的别名现象。分析时应回到采样条件，而不是只依据看到的表象判断。", y - 3)
    page.showPage()


def page_four(page: canvas.Canvas) -> None:
    start(page, 4)
    y = title(page, "透过现象看本质")
    y = paragraph(page, "我们通过感官或测量来认识世界时，常常只接触到事物的局部表象。采样、量化、观察帧率等过程会进一步改变表象与原始连续过程之间的对应关系，因此需要用明确的模型和条件去判断结论是否可靠。", y)
    y = section(page, "第一章小结", y - 2)
    y = paragraph(page, "本章从离散时间信号的表示、运算与典型序列出发，讨论了系统性质、线性卷积、差分方程，以及采样、恢复和模拟—数字处理链。贯穿全章的判断原则是：先明确对象与条件，再使用相应的数学表示和系统关系。", y)
    style.draw_note(page, "表象可以是局部的、片面的，甚至可能被采样过程扭曲；严谨的信号处理学习应不断追问条件、结构与本质。", y - 3)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    load_model(root)
    output = output_path or root / "full/outputs/chapter_01_applications_close_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4)
    page.setTitle("数字信号处理讲义：采样认知案例与本章收束")
    page_one(page)
    page_two(page)
    page_three(page)
    page_four(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
