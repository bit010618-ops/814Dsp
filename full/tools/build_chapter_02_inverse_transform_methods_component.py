from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sample.tools import build_sample as style

CHAPTER = "第二章 z 变换与 LSI 系统频域分析"
PALE = HexColor("#F4F7F8")


def para(page: canvas.Canvas, text: str, y: float) -> float:
    return style.draw_rich_paragraph(page, text, 62, y, A4[0] - 124)


def formula(page: canvas.Canvas, latex: str, y: float, height: float = 54) -> float:
    asset, width, image_height = style._math_metrics(latex, style.DISPLAY_FORMULA_SIZE)
    draw_h = min(height - 12, image_height * 72 / 300)
    draw_w = width * draw_h / image_height
    limit = A4[0] - 148
    if draw_w > limit:
        draw_h *= limit / draw_w
        draw_w = limit
    page.setFillColor(PALE)
    page.roundRect(62, y - height, A4[0] - 124, height, 3, fill=1, stroke=0)
    page.drawImage(ImageReader(str(asset)), (A4[0] - draw_w) / 2, y - height + (height - draw_h) / 2, draw_w, draw_h, mask="auto")
    return y - height - 12


def begin(page: canvas.Canvas, page_no: int, heading: str) -> float:
    style.draw_header(page, CHAPTER)
    style.draw_footer(page, page_no)
    return style.draw_title(page, heading, 746)


def sub(page: canvas.Canvas, text: str, y: float) -> float:
    return style.draw_continuation_title(page, text, y)


def page_one(page: canvas.Canvas) -> None:
    y = begin(page, 1, "z 反变换：部分分式展开法")
    y = para(page, "部分分式展开法适用于能够因式分解的有理型 {{X(z)}}。先将代数式分解为若干简单分式，再依据每一项的收敛域选择右边或左边序列，最后叠加各项反变换。", y)
    y = sub(page, "展开的一般形式", y - 4)
    y = formula(page, r"X(z)=\sum_k\frac{A_k}{1-p_kz^{-1}}+\sum_{m=0}^{M}B_mz^{-m}", y, 58)
    y = para(page, "若极点互异，可用代入极点或系数比较求出各 {{A_k}}；若有重极点，则需保留相应的高阶分式。ROC 不包含极点，且决定同一简单分式应对应哪一侧序列。", y)
    y = sub(page, "系数比较", y - 4)
    y = formula(page, r"\frac{z}{(z-a)(z-b)}=\frac{A}{z-a}+\frac{B}{z-b}", y, 54)
    y = para(page, "将两边同乘分母后比较各次幂系数，或令 {{z=a}}、{{z=b}}，即可得到 A、B。此步骤只求代数系数；时域方向仍须由 ROC 判定。", y)
    y = sub(page, "例：部分分式展开求 z 反变换", y - 6)
    y = para(page, r"例：设 {{X(z)=\frac{z^2}{(z-2)(z-0.5)}}}，收敛域为 {{|z|>2}}，求 {{x(n)}}。收敛域位于模最大极点之外，因此结果应为右边序列。", y)
    y = formula(page, r"X(z)=\frac{A_1z}{z-2}+\frac{A_2z}{z-0.5}", y, 54)
    y = para(page, r"令 {{z=2}} 得 {{A_1=\frac{4}{3}}}；令 {{z=0.5}} 得 {{A_2=-\frac{1}{3}}}。因此：", y)
    formula(page, r"X(z)=\frac{4}{3}\frac{z}{z-2}-\frac{1}{3}\frac{z}{z-0.5}", y, 54)
    page.showPage()


def page_two(page: canvas.Canvas) -> None:
    y = begin(page, 2, "例：部分分式展开求 z 反变换（续）")
    y = para(page, "对 {{|z|>2}}，两项均取右边序列的反变换，得到：", y)
    y = formula(page, r"x(n)=\frac{4}{3}2^nu(n)-\frac{1}{3}(0.5)^nu(n),\qquad |z|>2", y, 58)
    y = sub(page, "z 反变换：幂级数展开法", y - 6)
    y = para(page, "幂级数展开法（长除法）直接把 {{X(z)}} 展开为 {{z^{-1}}} 或 {{z}} 的幂级数，再读取 {{z^{-n}}} 的系数。它尤其适合不便因式分解，或只需要若干时域样值的情形。", y)
    y = formula(page, r"X(z)=\sum_{n=-\infty}^{\infty}x(n)z^{-n}", y, 50)
    y = para(page, "当 ROC 在最外极点之外时，按 {{z^{-1}}} 的降幂展开，得到因果（右边）序列；当 ROC 在最内极点之内时，按 {{z}} 的升幂展开，得到反因果（左边）序列。", y)
    y = sub(page, "例：长除法", y - 6)
    y = para(page, "例：设下式的收敛域为 |z|>3，求 x(n)。由 ROC 知应按 z 的降幂方向展开。", y)
    y = formula(page, r"X(z)=\frac{3z^{-1}}{(1-3z^{-1})^2},\qquad |z|>3", y, 54)
    y = formula(page, r"X(z)=3z^{-1}+18z^{-2}+81z^{-3}+\cdots", y, 54)
    formula(page, r"x(n)=n3^nu(n-1),\qquad |z|>3", y, 54)
    page.showPage()


def page_three(page: canvas.Canvas) -> None:
    y = begin(page, 3, "幂级数展开与方法比较")
    y = sub(page, "反变换方法比较", y - 6)
    y = para(page, "围线积分法给出 z 反变换的理论定义；部分分式展开法适合有理式且可分解的情形；幂级数展开法则直接给出序列样值，并可在工程中用于近似或逐项计算。三种方法都不能脱离 ROC 单独使用。", y)
    y = sub(page, "选择方法的顺序", y - 4)
    y = para(page, "先写清 {{X(z)}} 与 ROC；若分母能方便因式分解，优先采用部分分式展开；若希望直接得到展开系数，或只需有限项样值，则采用长除法。每一步都应检查得到的序列方向是否与 ROC 一致。", y)
    y = sub(page, "本节小结", y - 4)
    y = formula(page, r"X(z)+\mathrm{ROC}\quad\Longrightarrow\quad x(n)", y, 54)
    y = para(page, "同一代数式配不同 ROC 可对应不同的 {{x(n)}}。因此“写出 ROC、找极点、确定展开方向、再求反变换”是本节所有计算题的固定主线。", y)
    y = sub(page, "z 变换的性质", y - 6)
    y = para(page, "在进入下一节前，先固定一条原则：线性组合、移位和卷积后的 ROC 以原收敛域为基础判定；若零极点相消，收敛域可能扩大。", y)
    y = sub(page, "线性性质", y - 6)
    y = formula(page, r"\mathcal{Z}\{ax(n)+by(n)\}=aX(z)+bY(z)", y, 50)
    para(page, "若 {{X(z)}} 与 {{Y(z)}} 的 ROC 分别为 {{R_x}}、{{R_y}}，线性组合的 ROC 至少包含两者的重叠部分；当零极点抵消时，实际 ROC 可以比重叠部分更大。", y)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    output = output_path or root / "full" / "outputs" / "chapter_02_inverse_transform_methods_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("数字信号处理讲义：第二章 z 反变换方法")
    for draw in (page_one, page_two, page_three):
        draw(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
