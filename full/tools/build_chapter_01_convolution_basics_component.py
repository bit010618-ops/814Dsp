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

MODEL_PATH = Path("full/source/chapter_01_convolution_basics_component.json")
CHAPTER = "第一章 离散时间信号与系统"
PALE = HexColor("#F4F7F8")
NAVY = HexColor("#264866")
RED = HexColor("#A43B35")


def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))


def start(page, number):
    style.draw_header(page, CHAPTER)
    style.draw_footer(page, number)


def box(page, formula, y, h=50):
    asset, iw, ih = style._math_metrics(formula, style.DISPLAY_FORMULA_SIZE)
    dh = min(h - 12, ih * 72 / 300)
    dw = iw * dh / ih
    limit = A4[0] - 148
    if dw > limit:
        dw, dh = limit, dh * limit / dw
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


def stems(page, values, x, y, width, height, label):
    page.setStrokeColor(NAVY); page.setFillColor(NAVY); page.setLineWidth(0.8)
    base = y - height * 0.38
    page.line(x, base, x + width, base)
    page.line(x + 14, y - height + 8, x + 14, y - 6)
    page.setFont("Times-Italic", 11); page.drawString(x + 2, y - 4, label)
    scale = (height * .42) / max(values)
    gap = (width - 42) / max(1, len(values) - 1)
    for n, value in enumerate(values):
        px = x + 14 + n * gap
        page.setStrokeColor(RED); page.setFillColor(RED); page.setLineWidth(1.3)
        page.line(px, base, px, base + value * scale)
        page.circle(px, base + value * scale, 2.2, fill=1, stroke=0)
        page.setFillColor(NAVY); page.setFont("Helvetica", 7.5); page.drawCentredString(px, base - 11, str(n))
        page.setFillColor(RED); page.setFont("Helvetica", 7.5); page.drawCentredString(px, base + value * scale + 5, str(value))


def page_one(page):
    start(page, 1); y = title(page, "LSI 系统的时域求解：线性卷积")
    y = para(page, "同时满足线性和时不变性的离散时间系统称为 {{LSI}} 系统。其单位脉冲响应定义为 {{h(n)=T[\\delta(n)]}}；只要知道输入 {{x(n)}} 与 {{h(n)}}，就能由卷积和求得输出。", y)
    y = section(page, "卷积和定义", y - 2)
    y = box(page, r"y(n)=x(n)*h(n)=\sum_{m=-\infty}^{\infty}x(m)h(n-m)", y, 58)
    y = para(page, "符号 {{*}} 表示线性卷积。求和变量 {{m}} 遍历全部整数；固定 {{n}} 后，对每个相同 {{m}} 的样值相乘并累加，得到该时刻的输出 {{y(n)}}。", y)
    y = section(page, "从单位脉冲分解到卷积和", y - 2)
    y = box(page, r"x(n)=\sum_{m=-\infty}^{\infty}x(m)\delta(n-m)", y, 54)
    y = para(page, "利用线性性可把响应逐项相加；再利用移不变性，有 {{T[\\delta(n-m)]=h(n-m)}}，因此可直接得到下式。", y)
    y = box(page, r"T[x(n)]=\sum_{m=-\infty}^{\infty}x(m)h(n-m)", y, 52)
    style.draw_note(page, "关键：卷积不是普通逐项相乘。它体现的是“每一个输入脉冲在系统中产生的移位响应之和”。", y - 3)
    page.showPage()


def page_two(page):
    start(page, 2); y = title(page, "图解计算法：反褶、移位、相乘、相加")
    y = para(page, "图解法始终将 {{x(m)}} 固定，把 {{h(m)}} 看成关于变量 {{m}} 的序列。按如下顺序操作，可以逐个求出每一个 {{y(n)}}。", y)
    for heading, body in [
        ("1. 反褶", "以 {{m=0}} 为对称轴，将 {{h(m)}} 反褶为 {{h(-m)}}。"),
        ("2. 移位", "将 {{h(-m)}} 沿 {{m}} 轴平移 {{n}}，得到 {{h(n-m)}}；{{n>0}} 时向右移，{{n<0}} 时向左移。"),
        ("3. 相乘", "将 {{x(m)}} 与 {{h(n-m)}} 在相同 {{m}} 处的样值逐点相乘。"),
        ("4. 相加", "把所有乘积相加，得到该固定 {{n}} 下的输出值 {{y(n)}}。"),
    ]:
        y = section(page, heading, y - 1); y = para(page, body, y)
    y = section(page, "支持区间检查", y - 2)
    y = para(page, "只有两个序列在横轴上发生重叠的样点才会对结果有贡献。有限长序列卷积的长度为 {{L_x+L_h-1}}，这可用于检查是否漏算首尾项。", y)
    y = box(page, r"x(n)*\delta(n-n_0)=x(n-n_0)", y, 50)
    style.draw_note(page, "上式说明：与移位单位脉冲卷积只会使序列延时 {{n_0}}；这也是检查卷积方向与下标的简便方法。", y - 3)
    page.showPage()


def page_three(page):
    start(page, 3); y = title(page, "例题：两个有限长序列的线性卷积")
    y = para(page, "已知 {{x(n)=\\delta(n)+2\\delta(n-1)}}，{{h(n)=3\\delta(n)+2\\delta(n-1)+\\delta(n-2)}}，求 {{y(n)=x(n)*h(n)}}。", y)
    y = box(page, r"x=[1,2],\qquad h=[3,2,1]", y, 46)
    stems(page, [1, 2], 72, y, 190, 106, "x(m)"); stems(page, [3, 2, 1], 330, y, 190, 106, "h(m)"); y -= 122
    y = section(page, "逐步计算", y)
    y = para(page, "{{n=0}} 时仅 {{m=0}} 重叠：{{y(0)=1\\cdot3=3}}。{{n=1}} 时有两项重叠：{{y(1)=1\\cdot2+2\\cdot3=8}}。", y)
    y = para(page, "{{n=2}} 时：{{y(2)=1\\cdot1+2\\cdot2=5}}；{{n=3}} 时仅 {{m=1}} 重叠：{{y(3)=2\\cdot1=2}}。", y)
    y = box(page, r"y(n)=3\delta(n)+8\delta(n-1)+5\delta(n-2)+2\delta(n-3)", y, 56)
    stems(page, [3, 8, 5, 2], 120, y, 355, 120, "y(n)"); y -= 137
    style.draw_note(page, "核对：输入长度为 2、响应长度为 3，因此输出长度应为 {{2+3-1=4}}，与结果一致。", y - 2)
    page.showPage()


def page_four(page):
    start(page, 4); y = title(page, "例题详解：由脉冲响应直接求输出")
    y = para(page, "同一例题也可用脉冲分解直接计算。先把输入写成两项加权移位单位脉冲，再分别写出每一项的系统响应。", y)
    y = box(page, r"x(n)=\delta(n)+2\delta(n-1)", y, 46)
    y = para(page, "输入 {{\\delta(n)}} 的响应为 {{h(n)}}；输入 {{2\\delta(n-1)}} 的响应为 {{2h(n-1)}}。由线性性相加即可。", y)
    y = box(page, r"y(n)=h(n)+2h(n-1)", y, 46)
    y = para(page, "代入 {{h(n)=3\\delta(n)+2\\delta(n-1)+\\delta(n-2)}} 并合并同类项：", y)
    y = box(page, r"y(n)=3\delta(n)+8\delta(n-1)+5\delta(n-2)+2\delta(n-3)", y, 56)
    y = section(page, "本节小结", y - 2)
    y = para(page, "卷积和是 LSI 系统输出的时域表达式。图解法强调反褶—移位—相乘—相加；脉冲分解法强调线性性与移不变性。两种方法必须给出同一结果。", y)
    style.draw_note(page, "常见错误：把 {{h(n-m)}} 错写成 {{h(m-n)}}；忘记反褶；遗漏首尾仅一项重叠的输出值；把卷积误作等长逐项乘积。", y - 4)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts(); load_model(root)
    out = output_path or root / "full/outputs/chapter_01_convolution_basics_component.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(out), pagesize=A4); page.setTitle("数字信号处理讲义：线性卷积基础")
    page_one(page); page_two(page); page_three(page); page_four(page); page.save()
    return out


if __name__ == "__main__":
    print(build_pdf())
