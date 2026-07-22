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

MODEL_PATH = Path("full/source/chapter_01_time_invariance_component.json")
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

def title(page, text, y=774):
    return style.draw_title(page, text, y)

def section(page, text, y):
    return style.draw_continuation_title(page, text, y)

def page_one(page):
    start(page, 1)
    y = title(page, "离散时间系统的时不变性质")
    y = para(page, "若系统响应与激励作用于系统的时刻无关，则该系统为时不变系统，也称移不变系统。判断时必须比较两条完整路径。", y)
    y = section(page, "定义", y - 2)
    y = box(page, r"y(n)=T[x(n)]\quad\Longrightarrow\quad T[x(n-k)]=y(n-k),\qquad \forall k\in\mathbb{Z}", y, 54)
    y = para(page, "第一条路径是先让输入延迟 {{k}} 个样本，再通过系统；第二条路径是先通过系统，再将输出延迟 {{k}} 个样本。二者相等才是时不变。", y)
    y = section(page, "判别步骤", y - 2)
    y = para(page, "（1）由原输入 {{x(n)}} 写出 {{y(n)}}；（2）把输入替换为 {{x(n-k)}} 并求输出 {{T[x(n-k)]}}；（3）把原输出替换为 {{y(n-k)}}；（4）比较两式。", y)
    y = box(page, r"T[x(n-k)]=y(n-k)", y, 44)
    style.draw_note(page, "常见误区：不能只在某一个样点比较数值；时不变性要求等式对任意输入、任意整数移位 {{k}} 都成立。", y - 2)
    page.showPage()

def page_two(page):
    start(page, 2)
    y = title(page, "累加系统的时不变性")
    y = section(page, "例 1：从负无穷开始的累加器", y)
    y = box(page, r"y(n)=\sum_{m=-\infty}^{n}x(m)", y, 48)
    y = para(page, "对移位输入，有 {{T[x(n-k)]=\\sum_{m=-\\infty}^{n}x(m-k)}}。令 {{m'=m-k}}，下限仍为负无穷，得到下式。", y)
    y = box(page, r"T[x(n-k)]=\sum_{m'=-\infty}^{n-k}x(m')=y(n-k)", y, 50)
    y = para(page, "故从负无穷开始的累加器是时不变系统。", y)
    y = section(page, "例 2：从零开始的累加器", y - 2)
    y = box(page, r"y(n)=\sum_{m=0}^{n}x(m)", y, 48)
    y = para(page, "相同变量替换后，下限由 {{0}} 变为 {{-k}}，因此一般不能与 {{y(n-k)}} 的下限 {{0}} 一致。", y)
    y = box(page, r"T[x(n-k)]=\sum_{m'=-k}^{n-k}x(m')\ne\sum_{m=0}^{n-k}x(m')=y(n-k)", y, 54)
    style.draw_note(page, "结论：从零开始累加器的“起始时刻”固定在绝对时间原点，系统行为依赖于时刻，因此是时变系统。", y - 2)
    page.showPage()

def page_three(page):
    start(page, 3)
    y = title(page, "抽取与滑动平均系统")
    y = section(page, "例 3：抽取系统", y)
    y = para(page, "系统定义为 {{y(n)=x(2n)}}。先延迟输出得到 {{y(n-k)=x(2n-2k)}}；先延迟输入再通过系统则得到 {{T[x(n-k)]=x(2n-k)}}。两式一般不相等。", y)
    y = box(page, r"x(2n-2k)\ne x(2n-k)", y, 52)
    y = para(page, "例如取 {{x(n)=n}}、{{k=1}}、{{n=3}}：前者为 {{x(4)=4}}，后者为 {{x(5)=5}}，故可直接构成反例。", y)
    y = section(page, "线性时不变系统：滑动平均", y - 2)
    y = box(page, r"T[x(n)]=\frac{1}{M_2-M_1+1}\sum_{k=M_1}^{M_2}x(n-k)", y, 58)
    y = para(page, "当 {{M_1=0}}、{{M_2=3}} 时，{{y(n)=\\frac{1}{4}[x(n)+x(n-1)+x(n-2)+x(n-3)]}}。加权求和保持线性，固定的相对延迟保持时不变，因此它是线性时不变系统。", y)
    style.draw_note(page, "滑动平均通过对相邻样值求平均来平滑快速变化。它的核心判据不是“能否滤波”，而是系数和相对延迟均不随绝对时间 {{n}} 改变。", y - 3)
    page.showPage()

def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    load_model(root)
    out = output_path or root / "full/outputs/chapter_01_time_invariance_component.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(out), pagesize=A4)
    page.setTitle("数字信号处理讲义：第一章时不变性")
    page_one(page)
    page_two(page)
    page_three(page)
    page.save()
    return out

if __name__ == "__main__":
    print(build_pdf())
