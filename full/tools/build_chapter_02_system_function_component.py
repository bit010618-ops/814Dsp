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


def para(page, text, y):
    return style.draw_rich_paragraph(page, text, 62, y, A4[0] - 124)


def sub(page, text, y):
    return style.draw_continuation_title(page, text, y)


def begin(page, number, title):
    style.draw_header(page, CHAPTER)
    style.draw_footer(page, number)
    return style.draw_title(page, title, 746)


def box(page, latex, y, height=54):
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


def page_one(page):
    y = begin(page, 1, "系统函数与系统性质")
    y = para(page, r"对 LSI 系统，输出是输入与单位脉冲响应 {{h(n)}} 的卷积；z 域中卷积化为相乘。因此系统函数定义为单位脉冲响应的 z 变换：", y)
    y = box(page, r"y(n)=x(n)*h(n)\qquad\Longleftrightarrow\qquad Y(z)=X(z)H(z)", y, 56)
    y = box(page, r"H(z)=\mathcal{Z}\{h(n)\}=\frac{Y(z)}{X(z)}", y, 54)
    y = sub(page, "由收敛域判断因果性", y - 6)
    y = para(page, r"一般系统在时刻 {{n=n_0}} 的输出只依赖 {{n\leq n_0}} 的输入时为因果。对 LSI 系统，这等价于单位脉冲响应在负时刻为零：", y)
    y = box(page, r"h(n)=0\quad(n<0)", y, 52)
    y = para(page, "在 z 域，因果序列的收敛域位于最外极点之外，也就是 ROC 向外延伸至无穷远。", y)
    y = sub(page, "由收敛域判断稳定性", y - 6)
    y = para(page, r"LSI 系统稳定的充分必要条件是 {{h(n)}} 绝对可和。在 z 域中，等价条件是单位圆 {{|z|=1}} 位于收敛域内。", y)
    box(page, r"\sum_{n=-\infty}^{\infty}|h(n)|<\infty\qquad\Longleftrightarrow\qquad |z|=1\in\mathrm{ROC}", y, 56)
    page.showPage()


def page_two(page):
    y = begin(page, 2, "因果稳定系统的极点判据")
    y = para(page, r"系统同时因果且稳定时，ROC 必须既在最外极点之外，又包含单位圆。因此所有极点都应落在单位圆内：", y)
    y = box(page, r"\mathrm{ROC}: |z|>R_{\max},\qquad R_{\max}<1", y, 54)
    y = para(page, "判断顺序：先由极点位置确定候选收敛域；再结合“因果”选择外侧 ROC；最后检查单位圆是否包含在 ROC 内。不能只看代数表达式而忽略 ROC。", y)
    y = sub(page, "非因果但稳定的情形", y - 6)
    y = para(page, r"若单位脉冲响应含有负时刻非零项，则系统非因果；但只要其绝对可和，仍可稳定。因果性和稳定性是两项独立性质。", y)
    y = sub(page, "将系统改造成因果稳定系统", y - 6)
    y = para(page, r"例如对三点平均，{{y(n)=\frac{x(n)+x(n-1)+x(n-2)}{3}}} 只依赖当前和过去输入，因此因果；有限长单位脉冲响应绝对可和，因此稳定。", y)
    y = box(page, r"H(z)=\frac{1+z^{-1}+z^{-2}}{3},\qquad \mathrm{ROC}:|z|>0", y, 54)
    para(page, r"相反，含 {{x(n+1)}} 的平均式会使用未来输入，不能视为因果。将索引整体延迟即可转化为因果实现。", y)
    page.showPage()


def page_three(page):
    y = begin(page, 3, "例题：差分方程的系统函数")
    y = para(page, r"例题：已知线性移不变因果系统的差分方程为 {{y(n)+0.2y(n-1)-0.24y(n-2)=x(n)+x(n-1)}}。求系统函数和收敛域；判别系统的稳定性；求单位取样响应。", y)
    y = sub(page, "解", y - 6)
    y = para(page, "对零初始条件取 z 变换，并整理输出与输入之比：", y)
    y = box(page, r"H(z)=\frac{1+z^{-1}}{1+0.2z^{-1}-0.24z^{-2}}=\frac{1+z^{-1}}{(1-0.4z^{-1})(1+0.6z^{-1})}", y, 60)
    y = para(page, r"因系统因果，ROC 选择最外极点之外，即 {{|z|>0.6}}。单位圆在该收敛域内，所以系统稳定。", y)
    y = para(page, "作部分分式展开并按右边序列反变换：", y)
    y = box(page, r"H(z)=\frac{7}{5}\frac{1}{1-0.4z^{-1}}-\frac{2}{5}\frac{1}{1+0.6z^{-1}}", y, 58)
    y = box(page, r"h(n)=\left[\frac{7}{5}(0.4)^n-\frac{2}{5}(-0.6)^n\right]u(n)", y, 58)
    para(page, "结果同时满足因果性和绝对可和条件，因而与收敛域判定一致。", y)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    output = output_path or root / "full" / "outputs" / "chapter_02_system_function_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("数字信号处理讲义：第二章系统函数")
    for draw in (page_one, page_two, page_three):
        draw(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
