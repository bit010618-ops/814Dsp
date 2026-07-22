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


MODEL_PATH = Path("full/source/chapter_01_training_component.json")
CHAPTER_NAME = "第一章 离散时间信号与系统"
BLUE = HexColor("#123B5D")
INK = HexColor("#1F2933")
BRASS = HexColor(style.ACCENT_BRASS)


def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))


def _start(page: canvas.Canvas, number: int) -> None:
    style.draw_header(page, CHAPTER_NAME)
    style.draw_footer(page, number)


def _heading(page: canvas.Canvas, title: str, year: int) -> float:
    page.setFillColor(BLUE)
    page.setFont(style.FONT_SANS, 18)
    page.drawString(62, 770, title)
    page.setFillColor(INK)
    page.setFont(style.FONT_SERIF, 10.5)
    page.drawString(62, 736, f"{year} 年真题")
    page.setFillColor(HexColor("#52616B"))
    page.drawRightString(A4[0] - 62, 736, "详解：真题整理详解")
    return 702


def _formula(page: canvas.Canvas, formula: str, y: float, *, size: float = 15) -> float:
    asset, width, height = style._math_metrics(formula, size)
    drawn_height = height * 72 / 300
    drawn_width = width * drawn_height / height
    page.drawImage(ImageReader(str(asset)), (A4[0] - drawn_width) / 2, y - drawn_height, drawn_width, drawn_height, mask="auto")
    return y - drawn_height - 12


def _math_label(page: canvas.Canvas, formula: str, x: float, y: float, *, size: float = 12) -> None:
    """Draw a compact mathematical label without relying on Unicode glyph coverage."""
    asset, width, height = style._math_metrics(formula, size)
    drawn_height = height * 72 / 300
    drawn_width = width * drawn_height / height
    page.drawImage(
        ImageReader(str(asset)),
        x - drawn_width / 2,
        y - drawn_height / 2,
        drawn_width,
        drawn_height,
        mask="auto",
    )


def _system_diagram(page: canvas.Canvas, y: float) -> float:
    page.setStrokeColor(BLUE)
    page.setFillColor(INK)
    page.setLineWidth(0.8)
    x0, mid_y = 115, y - 100
    page.setFont(style.FONT_SERIF, 10)
    page.drawString(x0 - 38, mid_y - 4, "x(n)")
    page.line(x0, mid_y, x0 + 58, mid_y)
    page.circle(x0 + 70, mid_y, 13, fill=0, stroke=1)
    page.drawCentredString(x0 + 70, mid_y - 4, "Σ")
    page.line(x0 + 83, mid_y, x0 + 130, mid_y)
    page.rect(x0 + 130, mid_y - 18, 42, 36, fill=0, stroke=1)
    _math_label(page, r"z^{-1}", x0 + 151, mid_y, size=12)
    page.line(x0 + 172, mid_y, x0 + 218, mid_y)
    page.circle(x0 + 230, mid_y, 13, fill=0, stroke=1)
    page.drawCentredString(x0 + 230, mid_y - 4, "Σ")
    page.line(x0 + 243, mid_y, x0 + 290, mid_y)
    page.rect(x0 + 290, mid_y - 18, 42, 36, fill=0, stroke=1)
    _math_label(page, r"z^{-1}", x0 + 311, mid_y, size=12)
    page.line(x0 + 332, mid_y, x0 + 384, mid_y)
    page.circle(x0 + 397, mid_y, 13, fill=0, stroke=1)
    page.drawCentredString(x0 + 397, mid_y - 4, "Σ")
    page.line(x0 + 410, mid_y, x0 + 445, mid_y)
    page.drawString(x0 + 450, mid_y - 4, "y(n)")
    page.setFillColor(HexColor("#52616B"))
    page.drawString(x0 + 84, mid_y - 18, "0.25")
    page.drawString(x0 + 333, mid_y - 18, "0.2")
    page.line(x0 + 18, mid_y, x0 + 18, mid_y + 54)
    page.line(x0 + 18, mid_y + 54, x0 + 397, mid_y + 54)
    page.line(x0 + 397, mid_y + 54, x0 + 397, mid_y + 13)
    page.drawString(x0 + 196, mid_y + 61, "0.5")
    page.line(x0 + 311, mid_y - 18, x0 + 311, mid_y - 74)
    page.line(x0 + 311, mid_y - 74, x0 + 70, mid_y - 74)
    page.line(x0 + 70, mid_y - 74, x0 + 70, mid_y - 13)
    page.drawString(x0 + 177, mid_y - 70, "0.4")
    page.line(x0 + 311, mid_y - 42, x0 + 230, mid_y - 42)
    page.line(x0 + 230, mid_y - 42, x0 + 230, mid_y - 13)
    page.drawString(x0 + 264, mid_y - 38, "0.3")
    return y - 205


def _stem(page: canvas.Canvas, x: float, y: float, values: dict[int, float], label_formula: str) -> None:
    page.setStrokeColor(BLUE); page.setFillColor(INK); page.setLineWidth(0.7)
    page.line(x, y, x + 190, y); page.line(x + 80, y - 55, x + 80, y + 75)
    page.setFont(style.FONT_SERIF, 10); page.drawString(x + 194, y - 4, "n")
    _math_label(page, label_formula, x + 96, y + 66, size=11)
    for n, value in values.items():
        px = x + 80 + n * 28
        py = y + value * 25
        page.setStrokeColor(HexColor("#B45309")); page.setFillColor(HexColor("#B45309"))
        page.line(px, y, px, py); page.circle(px, py, 1.6, fill=1, stroke=0)
        page.setFillColor(INK); page.setFont(style.FONT_SERIF, 8); page.drawCentredString(px, y - 13, str(n)); page.drawString(px + 3, py + (4 if value >= 0 else -10), str(int(value)))


def _training_2002(page: canvas.Canvas) -> None:
    _start(page, 1); y = _heading(page, "第一章 分章强化训练", 2002)
    y = style.draw_rich_paragraph(page, r"如图，{{f(t)=\mathrm{Sa}(1000\pi t)}}，{{p(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT)}}。{{f_s(t)}} 为 {{f(t)}} 与 {{p(t)}} 的乘积，经矩形滤波器 {{H(\Omega)}} 后得到 {{y(t)}}。", 62, y, A4[0] - 124)
    page.setStrokeColor(BLUE); page.setLineWidth(0.8); page.line(104, y - 48, 204, y - 48); page.line(204, y - 48, 248, y - 48); page.rect(248, y - 66, 70, 36, fill=0, stroke=1); page.drawCentredString(283, y - 53, "H(Ω)"); page.line(318, y - 48, 410, y - 48); page.setFont(style.FONT_SERIF, 10); page.drawString(65, y - 52, "f(t)"); page.drawString(172, y - 78, "p(t)"); page.drawString(417, y - 52, "y(t)"); page.drawCentredString(220, y - 48, "×"); page.line(172, y - 70, 220, y - 54)
    y -= 115
    y = style.draw_rich_paragraph(page, r"（1）要从 {{f_s(t)}} 中无失真地恢复 {{f(t)}}，求最大采样间隔 {{T_{\max}}}。" + "\n" + r"（2）若 {{T=0.0008\,\mathrm{s}}}，计算 {{f_s(t)}} 的频谱函数，并画出示意关系。" + "\n" + r"（3）设计矩形滤波器 {{H(\Omega)}}，使 {{y(t)}} 无失真地反映 {{f(t)}}。", 62, y, A4[0] - 124)
    page.showPage()


def _training_2006(page: canvas.Canvas) -> None:
    _start(page, 2); y = _heading(page, "第一章 分章强化训练", 2006)
    y = style.draw_rich_paragraph(page, "一离散系统结构如图所示。", 62, y, A4[0] - 124)
    y = _system_diagram(page, y)
    style.draw_rich_paragraph(page, "求：\n（1）系统的传递函数；\n（2）描述系统的差分方程；\n（3）系统的单位阶跃响应。", 62, y, A4[0] - 124)
    page.showPage()


def _training_2019(page: canvas.Canvas) -> None:
    _start(page, 3); y = _heading(page, "第一章 分章强化训练", 2019)
    y = style.draw_rich_paragraph(page, "已知 {{f_1(n)}} 和 {{f_2(n)}} 波形如下，求 {{f_1(n)}} 与 {{f_2(n)}} 的卷积。", 62, y, A4[0] - 124)
    _stem(page, 110, y - 100, {-2: 1, -1: 1, 0: 1, 1: 1, 2: 1}, r"f_1(n)")
    _stem(page, 110, y - 260, {-1: 1, 0: 2, 1: -1, 2: 2, 3: -1}, r"f_2(n)")
    page.showPage()


def _answer_2002(page: canvas.Canvas) -> None:
    _start(page, 1); y = style.draw_title(page, "真题整理详解", 770); y = style.draw_continuation_title(page, "2002 年真题：采样与恢复", y + 6)
    y = style.draw_rich_paragraph(page, r"{{\mathrm{Sa}(1000\pi t)}} 的最高角频率为 {{\Omega_h=1000\pi\,\mathrm{rad}\,\mathrm{s}^{-1}}}。由无混叠采样条件 {{\Omega_s\geq2\Omega_h}}，并使用 {{\Omega_s=\frac{2\pi}{T}}}，得到最大抽样间隔：", 62, y, A4[0] - 124)
    y = _formula(page, r"T_{\max}=\frac{\pi}{\Omega_h}=10^{-3}\,\mathrm{s}", y)
    y = style.draw_rich_paragraph(page, r"当 {{T=0.0008\,\mathrm{s}}} 时，{{\Omega_s=2500\pi\,\mathrm{rad}\,\mathrm{s}^{-1}}}。冲激采样使连续频谱以 {{\Omega_s}} 为周期复制：", 62, y, A4[0] - 124)
    y = _formula(page, r"F_s(j\Omega)=\frac{1}{T}\sum_{k=-\infty}^{\infty}F(j(\Omega-k\Omega_s))", y)
    y = style.draw_rich_paragraph(page, r"每个矩形谱副本的支撑区为 {{|\Omega-k\Omega_s|\leq1000\pi}}，相邻副本之间仍留有间隔，因此可用理想低通滤波器恢复。为补偿采样带来的 {{\frac{1}{T}}} 倍幅度，滤波器应取：", 62, y, A4[0] - 124)
    y = _formula(page, r"H(\Omega)=T,\quad |\Omega|\leq1000\pi", y)
    _formula(page, r"H(\Omega)=0,\quad |\Omega|>1000\pi", y, size=13)
    page.showPage()


def _answer_2006(page: canvas.Canvas) -> None:
    _start(page, 2); y = style.draw_title(page, "真题整理详解", 770); y = style.draw_continuation_title(page, "2006 年真题：系统结构", y + 6)
    y = style.draw_rich_paragraph(page, "设第二个延时器输出为 {{v(n)}}。由结构图逐节点列式，可得 {{v(n)}} 与输入的关系，再由 {{y(n)=0.2x(n)+0.2v(n)}} 消去中间变量。", 62, y, A4[0] - 124)
    y = _formula(page, r"v(n)=0.5x(n-1)+0.25x(n-2)+0.3v(n-1)+0.4v(n-2)", y)
    y = style.draw_rich_paragraph(page, "因此传递函数为：", 62, y, A4[0] - 124)
    y = _formula(page, r"H(z)=\frac{Y(z)}{X(z)}=\frac{0.2+0.04z^{-1}-0.03z^{-2}}{1-0.3z^{-1}-0.4z^{-2}}", y)
    y = style.draw_rich_paragraph(page, "将分母移到左侧，即得到描述系统的差分方程：", 62, y, A4[0] - 124)
    y = _formula(page, r"y(n)-0.3y(n-1)-0.4y(n-2)=0.2x(n)+0.04x(n-1)-0.03x(n-2)", y)
    y = style.draw_rich_paragraph(page, r"令输入为单位阶跃 {{u(n)}}。先将传递函数分解为 {{H(z)=0.075+\frac{0.125}{1-0.8z^{-1}}}}，再对冲激响应求累加，可得单位阶跃响应：", 62, y, A4[0] - 124)
    _formula(page, r"s(n)=(0.7-0.5\times0.8^n)u(n)", y)
    page.showPage()


def _answer_2019(page: canvas.Canvas) -> None:
    _start(page, 3); y = style.draw_title(page, "真题整理详解", 770); y = style.draw_continuation_title(page, "2019 年真题：图形卷积", y + 6)
    y = style.draw_rich_paragraph(page, r"先读出图中样值：{{f_1(n)=1}}，{{-2\leq n\leq2}}；{{f_2(-1)=1}}，{{f_2(0)=2}}，{{f_2(1)=-1}}，{{f_2(2)=2}}，{{f_2(3)=-1}}，其余样值为零。卷积的支撑区为 {{-3\leq n\leq5}}。", 62, y, A4[0] - 124)
    y = style.draw_rich_paragraph(page, "由于 {{f_1(n)}} 在连续五个整数点上均为 1，{{f_1(n)*f_2(n)}} 等于 {{f_2}} 在长度为五的滑动窗口中的样值和。逐点相加得到卷积结果：", 62, y, A4[0] - 124)
    y = _formula(page, r"(f_1*f_2)(n)=\{1,3,2,4,3,2,0,1,-1\},\quad -3\leq n\leq5", y)
    style.draw_rich_paragraph(page, "检查时可将每一项与 {{f_2}} 的支撑区对齐：最左端只保留 {{f_2(-1)}}；窗口逐步右移时依次加入或移出一个样值。由此既能避免漏项，也可核对卷积长度为 {{5+5-1=9}}。", 62, y, A4[0] - 124)
    page.showPage()


def _build(root: Path, output_path: Path | None, *, answers: bool) -> Path:
    style.register_fonts(); load_model(root)
    default = "full/outputs/chapter_01_answers_component.pdf" if answers else "full/outputs/chapter_01_training_component.pdf"
    output = output_path or root / default; output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    for draw in ((_answer_2002, _answer_2006, _answer_2019) if answers else (_training_2002, _training_2006, _training_2019)):
        draw(page)
    page.save(); return output


def build_training_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    return _build(root, output_path, answers=False)


def build_answers_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    return _build(root, output_path, answers=True)


if __name__ == "__main__":
    print(build_training_pdf()); print(build_answers_pdf())
