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

MODEL_PATH = Path("full/source/chapter_01_periodicity_component.json")
CHAPTER = "第一章 离散时间信号与系统"
INK, PALE = HexColor("#1F2933"), HexColor("#F4F7F8")

def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))

def start(page, number):
    style.draw_header(page, CHAPTER)
    style.draw_footer(page, number)

def box(page, formula, y, h=48):
    asset, iw, ih = style._math_metrics(formula, style.DISPLAY_FORMULA_SIZE)
    dh = min(h - 12, ih * 72 / 300)
    dw = iw * dh / ih
    limit = A4[0] - 148
    if dw > limit:
        ratio = limit / dw
        dw, dh = limit, dh * ratio
    page.setFillColor(PALE)
    page.roundRect(62, y - h, A4[0] - 124, h, 3, fill=1, stroke=0)
    page.drawImage(ImageReader(str(asset)), (A4[0] - dw) / 2, y - h + (h - dh) / 2, dw, dh, mask="auto")
    return y - h - 12

def para(page, text, y):
    return style.draw_rich_paragraph(page, text, 62, y, A4[0] - 124)

def title(page, text, y=774):
    return style.draw_title(page, text, y)

def section(page, text, y):
    return style.draw_continuation_title(page, text, y)

def page_one(page, m):
    start(page, 1)
    y = title(page, "离散时间序列的周期性")
    y = para(page, "本节先给出周期序列的定义，再说明正弦序列何时为周期序列，并建立从数字角频率求最小正周期的统一方法。", y)
    y = section(page, "周期序列的定义", y - 2)
    y = box(page, m["sections"][0]["formula"], y)
    y = para(page, "若存在满足上式的最小正整数 {{N}}，则 {{x(n)}} 为周期序列，{{N}} 称为它的基本周期。定义必须对所有整数 {{n}} 成立。", y)
    y = section(page, "正弦序列的周期性", y - 2)
    y = box(page, m["sections"][1]["formula"], y)
    y = para(page, "由 {{x(n+N)=A\\sin[(n+N)\\omega+\\varphi]}} 可知，只有当 {{N\\omega}} 是 {{2\\pi}} 的整数倍时，相移才不改变每一个样值。", y)
    y = box(page, r"N=\frac{2\pi k}{\omega},\qquad k\in\mathbb{Z}_{+}", y, 44)
    style.draw_note(page, "判定要点：离散正弦序列是否周期，取决于数字角频率与 {{2\\pi}} 的比值是否为有理数；连续时间正弦信号必周期这一结论不能直接照搬。", y - 2)
    page.showPage()

def page_two(page, m):
    start(page, 2)
    y = title(page, "由频率求基本周期")
    y = section(page, "有理性判据", y)
    y = box(page, m["sections"][2]["formula"], y, 52)
    y = para(page, "当 {{\\frac{2\\pi}{\\omega}}} 为整数时，基本周期就是该整数；当它是既约分数 {{\\frac{N}{k}}} 时，基本周期为分子 {{N}}；若它是无理数，序列无周期。", y)
    y = section(page, "例 1：余弦序列的基本周期", y - 2)
    y = box(page, r"x(n)=A\cos(\frac{13\pi}{4}n),\qquad \frac{2\pi}{\omega}=\frac{8}{13},\qquad N=8", y, 48)
    y = para(page, "{{8}} 与 {{13}} 互素，故既约分数的分子为基本周期，即 {{N=8}}。从采样观点看，{{13}} 个连续正弦周期内取到 {{8}} 个离散样值周期。", y)
    y = section(page, "例 2：复指数序列是否周期", y - 2)
    y = box(page, r"x(n)=e^{j\frac{n}{6}},\qquad \omega=\frac{1}{6},\qquad \frac{2\pi}{\omega}=12\pi\notin\mathbb{Q}", y, 48)
    style.draw_note(page, "结论：{{12\\pi}} 为无理数，不存在整数 {{N}} 使 {{N\\omega=2k\\pi}}，所以该复指数序列不是周期序列。", y - 2)
    page.showPage()

def page_three(page, m):
    start(page, 3)
    y = title(page, "周期求解方法与调幅序列")
    y = section(page, "组合序列的处理", y)
    y = para(page, "先找出每个含 {{n}} 的正弦、余弦或复指数分量的数字角频率，再分别求基本周期。对 {{\\sin(\\omega_1n)+\\sin(\\omega_2n)}}，总周期为 {{\\operatorname{lcm}(N_1,N_2)}}。", y)
    y = para(page, "对 {{\\sin(\\omega_1n)\\sin(\\omega_2n)}}，先利用积化和差公式得到 {{\\omega_a=|\\omega_1+\\omega_2|}} 与 {{\\omega_b=|\\omega_1-\\omega_2|}}，再取各周期的最小公倍数。含 {{n}} 的系数或非零实指数包络会破坏周期性。", y)
    y = section(page, "调幅序列的频率成分", y - 2)
    y = box(page, m["sections"][3]["formula"], y)
    y = para(page, "该式可写成载波分量和两个边带分量，数字角频率分别为 {{\\omega_H}}、{{\\omega_H+\\omega_L}}、{{\\omega_H-\\omega_L}}。因此应分别检查三个分量的周期，再取最小公倍数。", y)
    y = section(page, "参数的周期结论", y - 2)
    y = box(page, r"\omega_L=0.01\pi,\quad \omega_H=0.2\pi,\quad N_1=10,\quad N_2=N_3=200", y, 50)
    y = para(page, "三项频率为 {{0.2\\pi}}、{{0.21\\pi}}、{{0.19\\pi}}，相应基本周期为 {{10}}、{{200}}、{{200}}；故调幅序列的基本周期为 {{\\operatorname{lcm}(10,200,200)=200}}。", y)
    style.draw_note(page, "方法小结：先确认各分量自身有周期，再把每个基本周期化为整数，最后取最小公倍数；不要把连续信号周期 {{T_0}} 与离散样值周期 {{N}} 混为一谈。", y - 3)
    page.showPage()

def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    model = load_model(root)
    out = output_path or root / "full/outputs/chapter_01_periodicity_component.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(out), pagesize=A4)
    page.setTitle("数字信号处理讲义：第一章周期性")
    page_one(page, model)
    page_two(page, model)
    page_three(page, model)
    page.save()
    return out

if __name__ == "__main__":
    print(build_pdf())
