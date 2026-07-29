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
BLUE = HexColor("#123B5D")
TEAL = HexColor("#0F8B8D")


def start(page: canvas.Canvas, n: int) -> None:
    style.draw_header(page, CHAPTER)
    style.draw_footer(page, n)


def title(page: canvas.Canvas, text: str, y: float = 746) -> float:
    return style.draw_title(page, text, y)


def section(page: canvas.Canvas, text: str, y: float) -> float:
    return style.draw_continuation_title(page, text, y)


def para(page: canvas.Canvas, text: str, y: float) -> float:
    return style.draw_rich_paragraph(page, text, 62, y, A4[0] - 124)


def formula(page: canvas.Canvas, latex: str, y: float, h: float = 52) -> float:
    image, width, height = style._math_metrics(latex, style.DISPLAY_FORMULA_SIZE)
    draw_h = min(h - 12, height * 72 / 300)
    draw_w = width * draw_h / height
    limit = A4[0] - 148
    if draw_w > limit:
        draw_h *= limit / draw_w
        draw_w = limit
    page.setFillColor(PALE)
    page.roundRect(62, y - h, A4[0] - 124, h, 3, fill=1, stroke=0)
    page.drawImage(ImageReader(str(image)), (A4[0] - draw_w) / 2, y - h + (h - draw_h) / 2, draw_w, draw_h, mask="auto")
    return y - h - 12


def z_plane(page: canvas.Canvas, x: float, y: float, radius: float, label: str) -> None:
    page.setStrokeColor(BLUE); page.setLineWidth(.7)
    page.line(x-radius-12, y, x+radius+18, y); page.line(x, y-radius-12, x, y+radius+18)
    page.circle(x, y, radius, stroke=1, fill=0)
    page.setFillColor(BLUE); page.setFont(style.FONT_SERIF, 9)
    page.drawString(x+radius+20, y-3, "Re{z}"); page.drawString(x+4, y+radius+22, "Im{z}")
    page.setFillColor(TEAL); page.setFont(style.FONT_SANS, 10); page.drawCentredString(x, y-radius-30, label)


def page_one(page: canvas.Canvas) -> None:
    start(page, 1); y = title(page, "2.1 z 变换的基本概念")
    y = para(page, "z 变换把离散时间序列表示为复变量 {{z}} 的函数，是分析离散 LSI 系统、收敛域、系统函数和频率响应的统一工具。本节依次建立定义、收敛域与反变换方法。", y)
    y = section(page, "z 变换的由来", y - 2)
    y = para(page, r"将连续时间拉普拉斯变换中的 {{s=\sigma+j\Omega}} 与采样间隔 {{T}} 联系起来，令 {{z=e^{sT}}}，就得到从 s 平面到 z 平面的映射。该映射把连续系统的指数因子转换为离散系统中的幂次因子。", y)
    y = formula(page, r"z=e^{sT}=e^{\sigma T}e^{j\Omega T}", y, 56)
    y = title(page, "z 变换的定义", y - 18)
    y = para(page, "序列 {{x(n)}} 的双边 z 变换定义为对所有整数时刻的加权求和；只有该级数绝对收敛的复变量 {{z}} 才属于收敛域。", y)
    y = formula(page, r"X(z)=\sum_{n=-\infty}^{\infty}x(n)z^{-n}", y, 58)
    y = section(page, "LSI 系统的系统函数", y - 4)
    y = para(page, r"离散 LSI 系统的单位脉冲响应为 {{h(n)}} 时，其 z 变换称为系统函数。系统函数与输入、输出的 z 变换满足相乘关系；该关系成立的 ROC 是相应收敛域的公共部分。", y)
    formula(page, r"H(z)=\mathcal{Z}\{h(n)\},\qquad Y(z)=H(z)X(z)", y, 54); page.showPage()


def page_two(page: canvas.Canvas) -> None:
    start(page, 2); y = title(page, "s 平面与 z 平面的映射")
    y = para(page, r"若 {{s=\sigma+j\Omega}}，则 {{|z|=e^{\sigma T}}}、{{\arg z=\Omega T}}。因此 s 平面中的竖直线映射为 z 平面中的圆，虚轴 {{\sigma=0}} 映射为单位圆。频率 {{\Omega}} 相差 {{\frac{2\pi}{T}}} 的点在 z 平面重合，这正是离散时间频域周期性的几何来源。", y)
    z_plane(page, 190, 420, 96, "s 平面：虚轴对应 σ=0")
    z_plane(page, 406, 420, 96, "z 平面：单位圆 |z|=1")
    y = section(page, "单位圆与频率响应", 270)
    y = para(page, r"对稳定的离散 LSI 系统，频率响应由 {{H(z)}} 在单位圆上的取值给出，即以 {{z=e^{j\omega}}} 代入系统函数。单位圆是否落在 ROC 内，是频率响应是否存在的必要条件。", y)
    formula(page, r"H(e^{j\omega})=H(z)|_{z=e^{j\omega}},\qquad \omega=\Omega T", y, 52); page.showPage()


def page_three(page: canvas.Canvas) -> None:
    start(page, 3); y = title(page, "z 变换及其收敛域")
    y = para(page, "同一个代数式 {{X(z)}} 在不同 ROC 下可以对应不同的时间序列；因此求反变换或判断系统时，必须同时给出表达式与收敛域。ROC 内不能包含极点。", y)
    y = section(page, "典型序列的收敛域", y - 2)
    y = formula(page, r"a^n u(n)\ \longleftrightarrow\ \frac{1}{1-az^{-1}},\quad |z|>|a|", y, 54)
    y = formula(page, r"-a^n u(-n-1)\ \longleftrightarrow\ \frac{1}{1-az^{-1}},\quad |z|<|a|", y, 54)
    y = para(page, "右边序列的 ROC 位于最外极点之外；左边序列的 ROC 位于最内极点之内；双边序列的 ROC 是两个极点圆之间的环域。有限长序列的 ROC 通常为整个 z 平面，是否包含零点或无穷远点取决于时间支持范围。", y)
    source_figure = ROOT / "full" / "source" / "chapter_02_figures" / "source-0194.png"
    image = ImageReader(str(source_figure))
    page.drawImage(image, 62, 74, A4[0] - 124, 262, mask="auto")
    page.showPage()


def page_four(page: canvas.Canvas) -> None:
    start(page, 4); y = title(page, "z 反变换")
    y = para(page, "由 {{X(z)}} 求 {{x(n)}} 称为 z 反变换。本质上是根据 ROC 将 {{X(z)}} 展开成合适方向的幂级数，再读取 {{z^{-n}}} 的系数。常用方法包括围线积分、部分分式展开和幂级数展开。", y)
    y = formula(page, r"x(n)=\frac{1}{2\pi j}\oint_C X(z)z^{n-1}\,dz", y, 56)
    y = section(page, "部分分式展开法", y - 2)
    y = para(page, "将有理函数按极点分解为简单分式，再依据每一项的 ROC 查表反变换。重复极点对应高阶分式；多项式部分对应有限长冲激组合。", y)
    y = formula(page, r"X(z)=\sum_k\frac{A_k}{1-p_kz^{-1}}\quad\Rightarrow\quad x(n)=\sum_k A_kp_k^n u(n)\ \ (|z|>\max|p_k|)", y, 64)
    y = title(page, "幂级数展开法", y - 18)
    y = para(page, "若 ROC 在最外极点之外，按 {{z^{-1}}} 的降幂展开，得到右边序列；若 ROC 在最内极点之内，按 {{z}} 的升幂展开，得到左边序列。展开方向由 ROC 决定，而不是由代数式外观决定。", y)
    y = section(page, "极点与收敛域", y - 4)
    y = para(page, "ROC 中不包含极点。对有理型系统函数，因果系统的 ROC 位于模最大有限极点的外侧；稳定系统还必须使单位圆落在 ROC 内。", y)
    y = formula(page, r"|z|>\max_k|p_k|,\qquad |z|=1\in \mathrm{ROC}", y, 54)
    y = section(page, "判定顺序", y - 4)
    para(page, "先由系统函数找出有限极点；再由序列的右边、左边或双边性质确定 ROC 所在区域；最后检查单位圆是否在该区域内，以判断稳定性和频率响应是否存在。", y); page.showPage()


def page_five(page: canvas.Canvas) -> None:
    start(page, 5); y = title(page, "例题：同一 X(z) 与不同收敛域")
    y = para(page, r"设 {{X(z)=\frac{1}{1-az^{-1}}}}。分别给出两种 ROC 下对应的序列，并解释差异。", y)
    y = section(page, "解答", y - 2)
    y = para(page, r"当 {{|z|>|a|}} 时，按 {{z^{-1}}} 的降幂展开：{{X(z)=1+az^{-1}+a^2z^{-2}+\cdots}}，因此得到因果右边序列。", y)
    y = formula(page, r"x(n)=a^n u(n),\qquad |z|>|a|", y, 52)
    y = para(page, "当 {{|z|<|a|}} 时，将式子改写为关于 {{z}} 的升幂级数，得到反因果左边序列。两种序列的代数式相同，但 ROC 不同，所以时间支持范围不同。", y)
    y = formula(page, r"x(n)=-a^n u(-n-1),\qquad |z|<|a|", y, 52)
    y = title(page, "本节结论", y - 18)
    y = para(page, "z 变换必须与 ROC 成对使用：ROC 决定序列是右边、左边还是双边，也决定系统的因果性、稳定性与单位圆上的频率响应是否存在。", y)
    y = section(page, "有限长序列的收敛域", y - 4)
    y = para(page, "有限长右边序列的 ROC 包含无穷远点；有限长左边序列的 ROC 包含零点。若序列在正、负时刻均有限长且包含 {{n=0}}，则 ROC 为整个有限 z 平面。", y)
    formula(page, r"x(n)=\delta(n)\quad\Longrightarrow\quad X(z)=1,\qquad \text{ROC：全 z 平面}", y, 54); page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    output = output_path or root / "full" / "outputs" / "chapter_02_z_transform_foundations_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("数字信号处理讲义：第二章 z 变换的基本概念")
    for draw in (page_one, page_two, page_three, page_four, page_five):
        draw(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
