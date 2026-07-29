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


def formula(page, latex, y, height=54):
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


def begin(page, number, heading):
    style.draw_header(page, CHAPTER)
    style.draw_footer(page, number)
    return style.draw_title(page, heading, 746)


def sub(page, text, y):
    return style.draw_continuation_title(page, text, y)


def page_one(page):
    y = begin(page, 1, "共轭对称与共轭反对称分量")
    y = para(page, r"共轭对称序列的实部为偶函数、虚部为奇函数；共轭反对称序列的实部为奇函数、虚部为偶函数。它们分别满足：", y)
    y = formula(page, r"x_e(n)=x_e^*(-n),\qquad x_o(n)=-x_o^*(-n)", y, 54)
    y = para(page, r"任意序列都可唯一分解为这两个分量之和。由 {{x(n)}} 直接求分量时，使用：", y)
    y = formula(page, r"x_e(n)=\frac{1}{2}[x(n)+x^*(-n)],\qquad x_o(n)=\frac{1}{2}[x(n)-x^*(-n)]", y, 58)
    y = para(page, "先作时间反转并取共轭，再与原序列相加或相减，即可得到相应分量。这一分解不改变原序列：{{x(n)=x_e(n)+x_o(n)}}。", y)
    y = sub(page, "频域函数的对应分量", y - 6)
    y = para(page, r"若 {{X(e^{j\omega})}} 是 {{x(n)}} 的 DTFT，则频域同样可分为共轭对称与共轭反对称两部分。", y)
    y = formula(page, r"X_e(e^{j\omega})=\frac{1}{2}[X(e^{j\omega})+X^*(e^{-j\omega})],\quad X_o(e^{j\omega})=\frac{1}{2}[X(e^{j\omega})-X^*(e^{-j\omega})]", y, 58)
    y = sub(page, "时域与频域的共轭对称对应", y - 6)
    y = para(page, r"频域函数的共轭对称分量与共轭反对称分量分别满足：", y)
    formula(page, r"X_e(e^{j\omega})=X_e^*(e^{-j\omega}),\qquad X_o(e^{j\omega})=-X_o^*(e^{-j\omega})", y, 54)
    page.showPage()


def page_two(page):
    y = begin(page, 2, "时域与频域的共轭对称对应（续）")
    y = para(page, r"序列实部的 DTFT 等于频域的共轭对称分量；序列虚部乘以 {{j}} 后的 DTFT 等于频域的共轭反对称分量：", y)
    y = formula(page, r"\mathcal{F}\{\mathrm{Re}[x(n)]\}=X_e(e^{j\omega}),\qquad \mathcal{F}\{j\,\mathrm{Im}[x(n)]\}=X_o(e^{j\omega})", y, 58)
    y = sub(page, "实序列的特殊情况", y - 6)
    y = para(page, r"当 {{x(n)}} 为实序列时，频域只剩下共轭对称分量。因此实部为偶函数、虚部为奇函数；幅度为偶函数，相位为奇函数：", y)
    y = formula(page, r"X(e^{j\omega})=X^*(e^{-j\omega}),\quad \mathrm{Re}[X(e^{j\omega})]=\mathrm{Re}[X(e^{-j\omega})],\quad \mathrm{Im}[X(e^{j\omega})]=-\mathrm{Im}[X(e^{-j\omega})]", y, 60)
    y = formula(page, r"|X(e^{j\omega})|=|X(e^{-j\omega})|,\qquad \arg X(e^{j\omega})=-\arg X(e^{-j\omega})", y, 54)
    y = para(page, "这些对称性可用于减少频谱计算量，并用于从已知实部或虚部恢复另一个分量。", y)
    y = sub(page, "例题：由实部恢复实因果序列", y - 6)
    para(page, r"例题：设 {{h(n)}} 为实因果序列，且 {{H_R(e^{j\omega})=1+\cos\omega}}，求 {{h(n)}} 和 {{H(e^{j\omega})}}。", y)
    page.showPage()


def page_three(page):
    y = begin(page, 3, "例题：由实部恢复实因果序列（续）")
    y = sub(page, "解", y)
    y = para(page, r"因为 {{h(n)}} 为实序列，{{H(e^{j\omega})}} 具有共轭对称性。已知实部 {{H_R(e^{j\omega})}}，其对应的共轭对称时域分量为：", y)
    y = formula(page, r"h_e(n)=\delta(n)+\frac{1}{2}\delta(n-1)+\frac{1}{2}\delta(n+1)", y, 58)
    y = para(page, r"因 {{h(n)}} 为因果序列，{{n<0}} 时 {{h(n)=0}}。在 {{n=-1}} 处，{{h_e(-1)=\frac{1}{2}}}，故为抵消该负时刻值，必须有 {{h_o(-1)=-\frac{1}{2}}}。又 {{h_o(n)}} 为奇函数，因此：", y)
    y = formula(page, r"h_o(0)=0,\qquad h_o(1)=\frac{1}{2}", y, 54)
    y = para(page, "将两个分量相加可得最终因果序列：", y)
    y = formula(page, r"h(n)=h_e(n)+h_o(n)=\delta(n)+\delta(n-1)", y, 56)
    y = para(page, r"因此 {{H(e^{j\omega})=1+e^{-j\omega}}}。检验其实部为 {{1+\cos\omega}}，虚部为 {{-\sin\omega}}，符合实序列频谱的共轭对称性。", y)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    output = output_path or root / "full" / "outputs" / "chapter_02_dtft_conjugate_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("数字信号处理讲义：第二章 DTFT 共轭对称性质")
    for draw in (page_one, page_two, page_three):
        draw(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
