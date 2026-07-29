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


def begin(page: canvas.Canvas, number: int, heading: str) -> float:
    style.draw_header(page, CHAPTER)
    style.draw_footer(page, number)
    return style.draw_title(page, heading, 746)


def sub(page: canvas.Canvas, text: str, y: float) -> float:
    return style.draw_continuation_title(page, text, y)


def page_one(page: canvas.Canvas) -> None:
    y = begin(page, 1, "z 变换的线性性质")
    y = para(page, "若两个序列的 z 变换存在，则它们的线性组合的 z 变换等于相应 z 变换的线性组合。收敛域至少是原收敛域的重叠部分；当组合后零极点相消时，实际收敛域可能扩大。", y)
    y = formula(page, r"\mathcal{Z}\{ax(n)+by(n)\}=aX(z)+bY(z)", y, 54)
    y = para(page, r"若 {{R_x^-<|z|<R_x^+}}、{{R_y^-<|z|<R_y^+}}，则重叠区域满足 {{\max(R_x^-,R_y^-)<|z|<\min(R_x^+,R_y^+)}}。", y)
    y = sub(page, "例：余弦右边序列", y - 4)
    y = para(page, r"例：已知 {{x(n)=\cos(\omega_0n)u(n)}}，求它的 z 变换，收敛域为 {{|z|>1}}。", y)
    y = para(page, "将余弦写成两项复指数之和，再分别对右边指数序列取 z 变换并相加：", y)
    y = formula(page, r"\cos(\omega_0n)u(n)=\frac{1}{2}e^{j\omega_0n}u(n)+\frac{1}{2}e^{-j\omega_0n}u(n)", y, 58)
    y = formula(page, r"X(z)=\frac{1-\cos\omega_0z^{-1}}{1-2\cos\omega_0z^{-1}+z^{-2}},\qquad |z|>1", y, 58)
    y = sub(page, "z 变换的移位性质", y - 6)
    para(page, "序列的时间移位在 z 域对应乘以 z 的幂。移位会改变零点位于原点或无穷远处的情形，因此 ROC 需结合移位后的序列实际支持范围重新判断。", y)
    page.showPage()


def page_two(page: canvas.Canvas) -> None:
    y = begin(page, 2, "z 变换的移位性质（续）")
    y = formula(page, r"\mathcal{Z}\{x(n-m)\}=z^{-m}X(z)", y, 54)
    y = sub(page, "例：有限长矩形序列", y - 4)
    y = para(page, "例：求序列 x(n)=u(n)-u(n-3) 的 z 变换及收敛域。", y)
    y = para(page, "不能只把两项的 ROC 机械相交。先在时域相减，可见该序列是有限长序列：", y)
    y = formula(page, r"x(n)=\delta(n)+\delta(n-1)+\delta(n-2)", y, 54)
    y = formula(page, r"X(z)=1+z^{-1}+z^{-2}", y, 54)
    y = para(page, "因 {{x(n)}} 在 n=0、1、2 三点取非零值，z=0 使 {{z^{-1}}} 不存在；其余有限 z 均可收敛。因此 ROC 为 {{|z|>0}}。这也说明相减后的有限长序列使收敛域扩大。", y)
    y = sub(page, "判定要点", y - 4)
    y = para(page, "先观察相减或相加后的最终时域序列，再判定 ROC；不能只从运算前的单边序列 ROC 直接推出结果。", y)
    y = sub(page, "z 变换的卷积和性质", y - 6)
    y = para(page, "设 y(n) 为 x(n) 与 h(n) 的卷积和。时域卷积对应 z 域相乘；一般情况下，Y(z) 的 ROC 为 X(z) 与 H(z) 的重叠部分，但边界上的零极点相消会使 ROC 扩大。", y)
    formula(page, r"y(n)=x(n)*h(n)\qquad\Longleftrightarrow\qquad Y(z)=X(z)H(z)", y, 54)
    page.showPage()


def page_three(page: canvas.Canvas) -> None:
    y = begin(page, 3, "z 变换的卷积和性质（续）")
    y = sub(page, "例：零极点相消", y - 4)
    y = para(page, "例：设 {{x(n)=a^nu(n)}}，{{h(n)=b^nu(n)-ab^{n-1}u(n-1)}}，求 {{x(n)*h(n)}}。", y)
    y = formula(page, r"X(z)=\frac{1}{1-az^{-1}},\qquad H(z)=\frac{1-az^{-1}}{1-bz^{-1}}", y, 56)
    y = para(page, "相乘后，X(z) 在 z=a 的极点与 H(z) 的零点相消：", y)
    y = formula(page, r"Y(z)=\frac{1}{1-bz^{-1}}\qquad\Longrightarrow\qquad y(n)=b^nu(n)", y, 56)
    y = para(page, "若 {{|b|<|a|}}，相消后收敛域由原先重叠所受的 |a| 限制扩大为 {{|z|>|b|}}。计算中必须先写出乘积，再检查是否存在零极点相消。", y)
    y = sub(page, "性质使用顺序", y - 4)
    y = para(page, "先列出每个序列及其 ROC；再进行线性、移位或卷积运算；最后根据化简后的表达式与时域支持范围重新确定最终 ROC。", y)
    y = sub(page, "其他常用性质", y - 6)
    y = para(page, "时间反转对应自变量互逆；乘以指数序列对应 z 域自变量缩放；z 域微分可得到带 n 的时域序列；共轭序列也有对应的共轭关系。使用这些性质时同样应重新检查 ROC。", y)
    y = formula(page, r"\mathcal{Z}\{x(-n)\}=X(z^{-1}),\qquad \mathcal{Z}\{a^nx(n)\}=X(a^{-1}z)", y, 52)
    formula(page, r"\mathcal{Z}\{nx(n)\}=-z\frac{dX(z)}{dz}", y, 52)
    para(page, "以上性质与线性、移位和卷积性质共同构成 z 域运算表；其公式、序列形式和收敛域必须成对核对。", y)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    output = output_path or root / "full" / "outputs" / "chapter_02_z_transform_properties_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("数字信号处理讲义：第二章 z 变换性质")
    for draw in (page_one, page_two, page_three):
        draw(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
