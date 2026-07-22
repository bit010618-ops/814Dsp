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


MODEL_PATH = Path("full/source/chapter_01_operations_component.json")
CHAPTER_NAME = "第一章 离散时间信号与系统"
INK = HexColor("#1F2933")
BLUE = HexColor("#123B5D")
BRASS = HexColor(style.ACCENT_BRASS)
TEAL = HexColor("#0F766E")
ORANGE = HexColor("#B45309")
PALE = HexColor("#F4F7F8")
TICK_OFFSET = 4


def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))


def _start(page: canvas.Canvas, number: int) -> None:
    style.draw_header(page, CHAPTER_NAME)
    style.draw_footer(page, number)


def _formula_box(page: canvas.Canvas, formula: str, y: float, *, height: float = 42, size: float = style.DISPLAY_FORMULA_SIZE) -> float:
    asset, image_width, image_height = style._math_metrics(formula, size)
    drawn_height = min(height - 12, image_height * 72 / 300)
    drawn_width = image_width * drawn_height / image_height
    maximum = A4[0] - 148
    if drawn_width > maximum:
        ratio = maximum / drawn_width
        drawn_width *= ratio
        drawn_height *= ratio
    bottom = y - height
    page.setFillColor(PALE)
    page.roundRect(62, bottom, A4[0] - 124, height, 3, fill=1, stroke=0)
    page.drawImage(ImageReader(str(asset)), (A4[0] - drawn_width) / 2, bottom + (height - drawn_height) / 2, drawn_width, drawn_height, mask="auto")
    return bottom - 14


def _draw_math(page: canvas.Canvas, formula: str, x: float, y: float, *, height: float = 14) -> float:
    asset, image_width, image_height = style._math_metrics(formula, style.DISPLAY_FORMULA_SIZE)
    drawn_width = image_width * height / image_height
    page.drawImage(ImageReader(str(asset)), x, y, drawn_width, height, mask="auto")
    return drawn_width


def _draw_stems(page: canvas.Canvas, x: float, y: float, width: float, height: float, series: list[list[int]], *, n_min: int = 0, n_max: int = 4, label: str = "x(n)") -> None:
    left, right, base = x + 18, x + width - 14, y + height * 0.38
    zero_x = left + (0 - n_min) * (right - left) / (n_max - n_min)
    page.setStrokeColor(BLUE)
    page.setLineWidth(0.7)
    page.line(left, base, right, base)
    page.line(zero_x, y + 9, zero_x, y + height - 9)
    _draw_math(page, label, zero_x + 5, y + height - 20, height=13)
    page.setFont("Times-Italic", 10)
    page.setFillColor(INK)
    page.drawString(right + 8, base - 14, "n")
    for n in range(n_min, n_max + 1):
        px = left + (n - n_min) * (right - left) / (n_max - n_min)
        page.setStrokeColor(BLUE)
        page.line(px, base - 3, px, base + 3)
        page.setFillColor(HexColor("#52616B"))
        page.setFont(style.FONT_SANS, 7.2)
        page.drawCentredString(px + TICK_OFFSET, base - 13, str(n))
    maximum = max(1, max(abs(value) for _, value in series))
    scale_y = min((height * 0.45) / maximum, 21)
    for n, value in series:
        px = left + (n - n_min) * (right - left) / (n_max - n_min)
        top = base + value * scale_y
        page.setStrokeColor(ORANGE)
        page.setFillColor(ORANGE)
        page.setLineWidth(1.1)
        page.line(px, base, px, top)
        page.circle(px, top, 1.8, fill=1, stroke=0)
        page.setFillColor(INK)
        page.setFont(style.FONT_SANS, 7.6)
        page.drawCentredString(px + TICK_OFFSET, top + (6 if value >= 0 else -11), str(value))


def _operation_heading(page: canvas.Canvas, title: str, y: float) -> float:
    return style.draw_continuation_title(page, title, y)


def _page_overview_sum_product(page: canvas.Canvas, model: dict) -> None:
    _start(page, 1)
    y = style.draw_title(page, "离散时间信号的基本运算", 774)
    y = style.draw_rich_paragraph(page, "本节的基本运算包括：序列的和（积）、移位、反褶、累加和、差分、时间尺度（比例）变换、能量和平均功率。它们均以离散时间索引 {{n}} 为自变量，并按相同索引处的样值定义。", 62, y, A4[0] - 124)
    y = _operation_heading(page, "序列的和与积", y - 1)
    y = style.draw_rich_paragraph(page, "两序列在同一索引 {{n}} 处的样值可逐项相加或逐项相乘，分别构成新序列：", 62, y, A4[0] - 124)
    y = _formula_box(page, r"y(n)=x_1(n)+x_2(n),\qquad y(n)=x_1(n)x_2(n)", y - 3)
    example = model["sections"][0]["example"]
    positions = [(62, 422, "x_1(n)", example["x1"]), (311, 422, "x_2(n)", example["x2"]), (62, 264, "x_1(n)+x_2(n)", example["sum"]), (311, 264, "x_1(n)x_2(n)", example["product"])]
    for x, graph_y, label, series in positions:
        _draw_stems(page, x, graph_y, 220, 122, series, label=label)
    page.setFillColor(HexColor("#52616B"))
    page.setFont(style.FONT_SANS, 8.3)
    page.drawCentredString(172, 407, "输入序列 1")
    page.drawCentredString(421, 407, "输入序列 2")
    page.drawCentredString(172, 249, "逐项相加的结果")
    page.drawCentredString(421, 249, "逐项相乘的结果")
    style.draw_note(page, "逐项运算的前提是两个序列使用同一索引 {{n}}。先对齐索引，再做加法或乘法；不能把图上的相邻样点错当为同一时刻。", 218)
    page.showPage()


def _page_echo(page: canvas.Canvas, model: dict) -> None:
    _start(page, 2)
    y = style.draw_title(page, "移位的应用：回声", 774)
    y = style.draw_rich_paragraph(page, "回声由原始声音的延时、衰减副本叠加而成。延时 {{R}} 个采样点意味着使用 {{x(n-R)}}；当 {{0<\\alpha<1}} 时，系数 {{\\alpha}} 表示回声的衰减。", 62, y, A4[0] - 124)
    y = _operation_heading(page, "单次回声", y - 2)
    y = _formula_box(page, r"y(n)=x(n)+\alpha x(n-R),\qquad 0<\alpha<1", y - 3)
    y = style.draw_rich_paragraph(page, "当前输出由当前原始样值和 {{R}} 个采样点之前的样值共同决定；{{R}} 越大，听感上的回声间隔越长。", 62, y, A4[0] - 124)
    y = _operation_heading(page, "多次回声", y - 2)
    y = _formula_box(page, r"y(n)=x(n)+\alpha x(n-R)+\alpha^2x(n-2R)+\cdots+\alpha^{N-1}x(n-(N-1)R)", y - 3, height=48)
    y = style.draw_rich_paragraph(page, "第 {{k}} 次回声相对原声延时 {{kR}}，幅度乘以 {{\\alpha^k}}；因此在 {{0<\\alpha<1}} 时，后续回声会逐次减弱。", 62, y, A4[0] - 124)
    y = _operation_heading(page, "课件中的参数示例", y - 2)
    y = style.draw_rich_paragraph(page, r"原始声音后分别叠加两路回声：回声 1 取 {{\alpha=0.3,\ R=6000}}；回声 2 取 {{\alpha=0.3,\ R=10000}}。两路延时不同，因此同一原声会在不同时间间隔后再次出现。", 62, y, A4[0] - 124)
    style.draw_note(page, "从公式判断“延时”时，注意 {{x(n-R)}} 中的负号：{{R>0}} 表示向右移，即使用更早的输入样值。", y - 4)
    page.showPage()


def _page_reversal(page: canvas.Canvas) -> None:
    _start(page, 3)
    y = style.draw_title(page, "序列的反褶", 774)
    y = style.draw_rich_paragraph(page, "序列 {{x(n)}} 的反褶序列定义为 {{y(n)=x(-n)}}。它相当于把横轴索引的正负号互换，因此以 {{n=0}} 为对称轴；{{x(0)}} 在反褶后保持不变。", 62, y, A4[0] - 124)
    y = _formula_box(page, r"y(n)=x(-n)", y - 3)
    _draw_stems(page, 72, 410, 200, 130, [[0, 1], [1, 2], [2, 3]], n_min=-3, n_max=3, label="x(n)")
    _draw_stems(page, 325, 410, 200, 130, [[-2, 3], [-1, 2], [0, 1]], n_min=-3, n_max=3, label="x(-n)")
    page.setFillColor(HexColor("#52616B"))
    page.setFont(style.FONT_SANS, 8.4)
    page.drawCentredString(172, 395, "原序列：样值索引为 0、1、2")
    page.drawCentredString(425, 395, "反褶后：索引变为 0、−1、−2")
    y = _operation_heading(page, "周期序列与反褶后的移位", 368)
    y = style.draw_rich_paragraph(page, "对于周期序列，应在每个周期内围绕该周期的局部 {{n=0}} 反褶，得到的周期排列仍须保持周期性；不能只对整条图形做一次全局镜像而破坏周期结构。", 62, y, A4[0] - 124)
    y = _formula_box(page, r"x(-n+1),\qquad x(-n-1)", y - 3)
    style.draw_note(page, "处理复合变换时可先反褶，再按 {{n}} 的表达式判断移位方向：{{x(-n+1)}} 是反褶结果 {{x(-n)}} 的右移 1 位；{{x(-n-1)}} 是 {{x(-n)}} 的左移 1 位。", y - 3)
    page.showPage()


def _page_accumulation_difference(page: canvas.Canvas) -> None:
    _start(page, 4)
    y = style.draw_title(page, "累加和与差分", 774)
    y = style.draw_rich_paragraph(page, "累加和把从负无穷到当前索引的全部样值累积起来。将相邻两个累加和相减，恰好留下当前样值，因此累加和可写成递推形式。", 62, y, A4[0] - 124)
    y = _formula_box(page, r"y(n)=\sum_{k=-\infty}^{n}x(k),\qquad y(n)-y(n-1)=x(n),\qquad y(n)=y(n-1)+x(n)", y - 3, height=48)
    y = _operation_heading(page, "前向差分与后向差分", y - 1)
    y = style.draw_rich_paragraph(page, "差分反映序列样值随索引的变化。前向差分比较当前样值和下一样值；后向差分比较当前样值和前一样值：", 62, y, A4[0] - 124)
    y = _formula_box(page, r"\nabla x(n)=x(n+1)-x(n),\qquad \Delta x(n)=x(n)-x(n-1)", y - 3)
    y = _operation_heading(page, "例：矩形序列的后向差分", y - 2)
    y = style.draw_rich_paragraph(page, r"令 {{x(n)=R_{10}(n)}}，即 {{n=0,1,\ldots,9}} 时取 1，其他时刻取 0。{{x(n)}} 与 {{x(n-1)}} 在内部区间相同，只有进入和离开矩形序列时发生变化：", 62, y, A4[0] - 124)
    y = _formula_box(page, r"\Delta R_{10}(n)=R_{10}(n)-R_{10}(n-1)=\{1,0,0,0,0,0,0,0,0,0,-1\}", y - 3, height=46, size=10)
    style.draw_note(page, "后向差分在 {{n=0}} 产生正脉冲，在 {{n=10}} 产生负脉冲；它突出的是序列的突变位置，而不是平坦区间内恒定的样值。", y - 4)
    page.showPage()


def _page_scale_energy_power(page: canvas.Canvas) -> None:
    _start(page, 5)
    y = style.draw_title(page, "时间尺度、能量与平均功率", 774)
    y = _operation_heading(page, "时间尺度（比例）变换", y)
    y = style.draw_rich_paragraph(page, r"当 {{m>1}} 为正整数时，{{x(mn)}} 为抽取（下采样）序列，只保留原序列每隔 {{m}} 个索引的样值；{{x(\frac{n}{m})}} 为插值（上采样）序列。", 62, y, A4[0] - 124)
    y = _formula_box(page, r"x(n)=\{0,1,2,3,4,5,6\}\ \Longrightarrow\ x(2n)=\{0,2,4,6\}", y - 3)
    y = _operation_heading(page, "序列的能量", y - 1)
    y = _formula_box(page, r"E_x=\sum_{n=-\infty}^{\infty}|x(n)|^2=\sum_{n=-\infty}^{\infty}x(n)x^*(n)", y - 3)
    y = style.draw_rich_paragraph(page, r"若 {{E_x=A<\infty}}，则 {{x(n)}} 称为能量有限信号（简称能量信号）。有限长序列以及绝对可和的无限长序列都是能量信号；{{x^*(n)}} 表示 {{x(n)}} 的复共轭。", 62, y, A4[0] - 124)
    y = _operation_heading(page, "序列的平均功率", y - 2)
    y = _formula_box(page, r"P_x=\lim_{N\to\infty}\frac{1}{2N+1}\sum_{n=-N}^{N}|x(n)|^2", y - 3)
    y = style.draw_rich_paragraph(page, r"若 {{P_x=C<\infty}}，则 {{x(n)}} 称为功率有限信号（简称功率信号）。周期信号和随机信号通常在无限时间内存在，因此通常不是能量信号而是功率信号。", 62, y, A4[0] - 124)
    y = style.draw_rich_paragraph(page, "若 {{x(n)}} 的周期为 {{N}}，只需取一个周期内的样值计算平均功率：", 62, y - 2, A4[0] - 124)
    y = _formula_box(page, r"P_x=\frac{1}{N}\sum_{n=0}^{N-1}|x(n)|^2", y - 3)
    style.draw_note(page, "本节八项基本运算构成后续系统分析的共同语言：先确认索引的变换，再处理样值的叠加、差分、能量或功率。", y - 4)
    page.showPage()


def build_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    style.register_fonts()
    model = load_model(root)
    output = output_path or root / "full" / "outputs" / "chapter_01_operations_component.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("数字信号处理讲义：第一章基本运算组件")
    _page_overview_sum_product(page, model)
    _page_echo(page, model)
    _page_reversal(page)
    _page_accumulation_difference(page)
    _page_scale_energy_power(page)
    page.save()
    return output


if __name__ == "__main__":
    print(build_pdf())
