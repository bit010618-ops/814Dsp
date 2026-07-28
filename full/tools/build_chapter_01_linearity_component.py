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

MODEL_PATH = Path("full/source/chapter_01_linearity_component.json")
CHAPTER = "第一章 离散时间信号与系统"
PALE = HexColor("#F4F7F8")

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

def title(page, text, y=730):
    return style.draw_title(page, text, y)

def section(page, text, y):
    return style.draw_continuation_title(page, text, y)

def page_one(page):
    start(page, 1)
    y = title(page, "离散时间系统的线性性质")
    y = para(page, "线性系统满足叠加原理：可加性与比例性必须同时成立。设 {{y_1(n)=T[x_1(n)]}}、{{y_2(n)=T[x_2(n)]}}。", y)
    y = section(page, "可加性与比例性", y - 2)
    y = box(page, r"T[x_1(n)+x_2(n)]=T[x_1(n)]+T[x_2(n)]", y)
    y = box(page, r"T[a x_1(n)]=aT[x_1(n)]", y, 44)
    y = section(page, "叠加原理", y - 2)
    y = box(page, r"T[a x_1(n)+b x_2(n)]=a y_1(n)+b y_2(n)", y, 50)
    y = para(page, "更一般地，若 {{y_i(n)=T[x_i(n)]}}，则对任意有限组输入和系数，线性系统均有下式。", y)
    y = box(page, r"T[\sum_{i=1}^{N}a_i x_i(n)]=\sum_{i=1}^{N}a_i y_i(n)", y, 50)
    # This intact title/formula block belongs in the available lower area of
    # the definition page; its derivation continues on the next page.
    y = section(page, "例：验证下面的系统是否为线性系统：", y - 2)
    y = box(page, r"y(n)=x^2(n)", y, 46)
    y = section(page, "例（续）", y - 2)
    y = para(page, "（零输入产生零输出）", y)
    para(page, "系统定义为 {{y(n)=x^2(n)}}。虽然零输入产生零输出，但仍需检验叠加原理。", y)
    page.showPage()

def page_two(page):
    start(page, 2)
    y = section(page, "例（续）：叠加检验", 752)
    y = box(page, r"T[a x_1+b x_2]=(a x_1+b x_2)^2=a^2x_1^2+b^2x_2^2+2abx_1x_2", y, 58)
    y = box(page, r"T[a x_1+b x_2]\ne aT[x_1]+bT[x_2]", y, 48)
    y = para(page, "交叉项 {{2abx_1x_2}} 一般不为零，故平方系统不是线性系统。", y)
    y = section(page, "例：验证下面的系统是否为线性系统：", y - 2)
    y = box(page, r"y(n)=x(-n)", y, 46)
    y = para(page, "系统定义为 {{y(n)=x(-n)}}，于是", y)
    y = box(page, r"T[a x_1(n)+b x_2(n)]=a x_1(-n)+b x_2(-n)=a y_1(n)+b y_2(n)", y, 54)
    y = para(page, "等式对任意输入与任意系数都成立，因此时间反褶系统是线性系统。线性与时不变是不同性质；该例的时不变性将单独讨论。", y)
    # Page 2 still has room for the next complete example heading/formula.
    y = section(page, "例：验证下面的3点中值滤波器是否是线性系统：", y - 4)
    box(page, r"y(n)=\operatorname{Mid}\{x(k)\},\qquad n-1\leq k\leq n+1", y, 52)
    page.showPage()

def page_three(page):
    start(page, 3)
    y = section(page, "例（续）", 774)
    y = para(page, "三点中值滤波器定义为：对 {{n-1\\leq k\\leq n+1}} 的三个样值取中间值。它能保留中值而抑制异常点，但不满足叠加原理。", y)
    y = section(page, "反例", y - 2)
    y = para(page, "取 {{a=b=1}}，并在同一三个样点上令 {{x_1=\\{1,2,1\\}}}、{{x_2=\\{2,1,1\\}}}。", y)
    y = box(page, r"T[x_1]=1,\qquad T[x_2]=1,\qquad T[x_1]+T[x_2]=2", y, 48)
    y = box(page, r"x_1+x_2=\{3,3,2\},\qquad T[x_1+x_2]=3", y, 48)
    y = para(page, "因此 {{T[x_1+x_2]\\ne T[x_1]+T[x_2]}}，三点中值滤波器为非线性系统。这个例子说明：系统具有实际滤波作用，并不意味着它必定线性。", y)
    page.showPage()

def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    load_model(root)
    out = output_path or root / "full/outputs/chapter_01_linearity_component.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(out), pagesize=A4)
    page.setTitle("数字信号处理讲义：第一章线性系统")
    page_one(page)
    page_two(page)
    page_three(page)
    page.save()
    return out

if __name__ == "__main__":
    print(build_pdf())
