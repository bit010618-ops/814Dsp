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
    y = begin(page, 1, "离散时间信号傅里叶变换")
    y = para(page, "一个离散时间非周期信号及其频谱的关系，可用离散时间信号（序列）的傅里叶变换表示。DTFT 把离散序列映射为关于连续频率变量的周期函数。", y)
    y = sub(page, "正变换", y - 4)
    y = para(page, "序列 {{x(n)}} 的离散时间傅里叶变换定义为：", y)
    y = formula(page, r"X(e^{j\omega})=\sum_{n=-\infty}^{\infty}x(n)e^{-j\omega n}", y, 56)
    y = para(page, r"它也可由 z 变换得到：当 z 落在单位圆上，即 {{z=e^{j\omega}}}，z 变换便给出 DTFT。", y)
    y = sub(page, "反变换", y - 6)
    y = para(page, r"由频域函数恢复时域序列时，在任意一个长度为 {{2\pi}} 的频率区间上积分即可：", y)
    y = formula(page, r"x(n)=\frac{1}{2\pi}\int_{-\pi}^{\pi}X(e^{j\omega})e^{j\omega n}\,d\omega", y, 58)
    y = para(page, "正、反变换成对使用：正变换描述频谱，反变换从完整频谱恢复原序列。", y)
    y = sub(page, "正变换的收敛条件", y - 6)
    y = para(page, "若序列 {{x(n)}} 绝对可和，则其傅里叶变换存在且连续：", y)
    formula(page, r"\sum_{n=-\infty}^{\infty}|x(n)|<\infty", y, 54)
    page.showPage()


def page_two(page: canvas.Canvas) -> None:
    y = begin(page, 2, "DTFT 的收敛条件与周期性（续）")
    y = para(page, "绝对可和是保证正变换逐项求和有意义的常用充分条件。对具体序列，还应结合其 z 变换的收敛域判断单位圆是否包含在收敛域中。", y)
    y = sub(page, "频域的周期性", y - 6)
    y = para(page, r"由于时域变量 {{n}} 为整数，频率增加 {{2\pi}} 后复指数的取值不变，因此 DTFT 在频域呈现周期性：", y)
    y = formula(page, r"X(e^{j(\omega+2\pi k)})=X(e^{j\omega}),\qquad k\in\mathbb{Z}", y, 56)
    y = para(page, r"这与连续时间傅里叶变换不同：离散时间导致频域周期延拓。分析频谱时通常只需观察任一主值区间，例如 {{-\pi\leq\omega<\pi}}。", y)
    y = sub(page, "与 z 变换的关系", y - 6)
    y = para(page, r"DTFT 是 z 变换在单位圆上的特例；只有当 z 变换的收敛域包含单位圆时，才可以把 z 直接代为 {{e^{j\omega}}}。", y)
    y = sub(page, "DTFT 正变换和反变换的由来", y - 6)
    y = para(page, r"从 z 变换定义出发，将 {{z=re^{j\omega}}} 写成极坐标形式。若收敛域覆盖单位圆，令 {{r=1}}，便得到 DTFT 的正变换。", y)
    y = formula(page, r"X(z)=\sum_{n=-\infty}^{\infty}x(n)z^{-n}\quad\Longrightarrow\quad X(e^{j\omega})", y, 58)
    y = sub(page, "DTFT 正变换和反变换的由来（续）", y - 6)
    para(page, r"反变换来自 z 反变换沿收敛域内闭合路径的积分。选择单位圆作为积分路径后，复变量积分化为一个 {{2\pi}} 周期内的频率积分。", y)
    page.showPage()


def page_three(page: canvas.Canvas) -> None:
    y = begin(page, 3, "DTFT 正变换和反变换的由来（续）")
    y = formula(page, r"x(n)=\frac{1}{2\pi}\int_{-\pi}^{\pi}X(e^{j\omega})e^{j\omega n}\,d\omega", y, 58)
    y = sub(page, "使用时的检查顺序", y - 6)
    y = para(page, r"先确认序列的 z 变换收敛域是否包含单位圆；再写正变换或反变换；最后利用频域的 {{2\pi}} 周期性选择合适的观察区间。若单位圆不在收敛域内，不能把相应 z 变换当作 DTFT。", y)
    y = sub(page, "本节结论", y - 6)
    y = para(page, r"DTFT 用连续而周期的频率变量描述离散时间序列。单位圆、收敛条件和 {{2\pi}} 周期性是后续讨论共轭对称、系统函数与频率响应的基础。", y)
    y = sub(page, "DTFT 的共轭对称性质", y - 6)
    y = para(page, "共轭表示一对按规律相配的复数。若两个复数实部相等、虚部互为相反数，则它们互为共轭复数：", y)
    y = formula(page, r"z=a+jb\qquad\Longrightarrow\qquad z^*=a-jb", y, 54)
    y = para(page, "DTFT 的共轭对称性质把时域序列的对称性与频域函数的实部、虚部结构联系起来。若序列满足 {{x(n)=x^*(-n)}}，称为共轭对称；若满足 {{x(n)=-x^*(-n)}}，称为共轭反对称。", y)
    y = para(page, "一般序列可写成共轭对称分量与共轭反对称分量之和。下一部分将据此说明频域函数的对应分量。", y)
    formula(page, r"x_e(n)=\frac{1}{2}[x(n)+x^*(-n)],\qquad x_o(n)=\frac{1}{2}[x(n)-x^*(-n)]", y, 54)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    output = output_path or root / "full" / "outputs" / "chapter_02_dtft_basics_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("数字信号处理讲义：第二章 DTFT 基础")
    for draw in (page_one, page_two, page_three):
        draw(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
