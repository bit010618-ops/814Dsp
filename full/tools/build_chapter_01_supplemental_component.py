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


MODEL_PATH = Path("full/source/chapter_01_supplemental_component.json")
CHAPTER_NAME = "第一章 离散时间信号与系统"
INK = HexColor("#1F2933")
MUTED = HexColor("#52616B")


def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))


def _start(page: canvas.Canvas, number: int) -> None:
    style.draw_header(page, CHAPTER_NAME)
    style.draw_footer(page, number)


def _formula(page: canvas.Canvas, formula: str, y: float, *, size: float = 15) -> float:
    asset, width, height = style._math_metrics(formula, size)
    drawn_height = height * 72 / 300
    drawn_width = width * drawn_height / height
    page.drawImage(
        ImageReader(str(asset)),
        (A4[0] - drawn_width) / 2,
        y - drawn_height,
        drawn_width,
        drawn_height,
        mask="auto",
    )
    return y - drawn_height - 12


def _question_heading(page: canvas.Canvas, year: int, y: float, *, first: bool) -> float:
    if first:
        page.setFillColor(HexColor("#123B5D"))
        page.setFont(style.FONT_SANS, 18)
        page.drawString(62, y, "第一章 补充真题")
        y -= 34
    page.setFillColor(INK)
    page.setFont(style.FONT_SERIF, 10.5)
    page.drawString(62, y, f"{year} 年真题")
    page.setFillColor(MUTED)
    page.drawRightString(A4[0] - 62, y, "详解：真题整理详解")
    return y - 31


def _training(page: canvas.Canvas) -> None:
    _start(page, 1)
    y = _question_heading(page, 2002, 770, first=True)
    y = style.draw_rich_paragraph(
        page,
        r"已知 {{x(t)=\cos(50t)}}，对其进行时域采样。要求能从采样信号中恢复原始信号，填空：奈奎斯特频率为______ {{\mathrm{Hz}}}；奈奎斯特采样周期为______ {{\mathrm{s}}}。",
        62,
        y,
        A4[0] - 124,
    )
    y -= 46
    y = _question_heading(page, 2003, y, first=False)
    style.draw_rich_paragraph(
        page,
        r"已知 {{x(t)=1+\cos(200t)+\sin(300t)}}，对其进行时域采样。要求能从采样信号中恢复原始信号，填空：奈奎斯特频率为______ {{\mathrm{Hz}}}；奈奎斯特采样周期为______ {{\mathrm{s}}}。",
        62,
        y,
        A4[0] - 124,
    )
    y -= 32
    y = _question_heading(page, 2014, y, first=False)
    y = style.draw_rich_paragraph(
        page,
        r"已知系统 {{y[n]=x[n]\{g[n]+g[n-1]\}}}，若 {{g[n]=1+(-1)^n}}，则系统是否为时变系统？______。",
        62,
        y,
        A4[0] - 124,
    )
    y -= 32
    y = _question_heading(page, 2015, y, first=False)
    y = style.draw_rich_paragraph(
        page,
        "对模拟信号进行采样，得到的是______信号。",
        62,
        y,
        A4[0] - 124,
    )
    y -= 40
    y = _question_heading(page, 2020, y, first=False)
    style.draw_rich_paragraph(
        page,
        r"已知频带宽度有限信号 {{x(t)}}、{{y(t)}} 的最高频率分别为 {{f_1}} 和 {{f_2}}，其中 {{f_1<f_2}}，则对信号 {{2x(t)+5y(t)}} 进行无失真抽样的采样频率为______。",
        62,
        y,
        A4[0] - 124,
    )
    page.showPage()
    _start(page, 2)
    y = _question_heading(page, 2003, 770, first=True)
    style.draw_rich_paragraph(
        page,
        r"已知系统差分方程为 {{r(n)-6r(n-1)+8r(n-2)=e(n-1)+2e(n-2)}}，求单位样值响应。",
        62,
        y,
        A4[0] - 124,
    )
    page.showPage()


def _answers(page: canvas.Canvas) -> None:
    _start(page, 1)
    y = style.draw_title(page, "真题整理详解", 770)
    y = style.draw_continuation_title(page, "2002 年真题：单频正弦信号采样", y + 6)
    y = style.draw_rich_paragraph(
        page,
        r"信号 {{x(t)=\cos(50t)}} 的最高角频率为 {{\Omega_m=50\,\mathrm{rad}\,\mathrm{s}^{-1}}}。无混叠恢复要求最小采样角频率满足 {{\Omega_s=2\Omega_m}}。再用 {{f_s=\frac{\Omega_s}{2\pi}}} 和 {{T_s=\frac{1}{f_s}}} 换算，得到：",
        62,
        y,
        A4[0] - 124,
    )
    y = _formula(page, r"f_{s,\min}=\frac{50}{\pi}\,\mathrm{Hz},\qquad T_{s,\max}=\frac{\pi}{50}\,\mathrm{s}", y)
    # 展示公式已自行回收高度；再下移小节标题，确保上一题结果先完整读完。
    y = style.draw_continuation_title(page, "2003 年真题：多频正弦信号采样", y - 14)
    y = style.draw_rich_paragraph(
        page,
        r"常数项不增加频率上限；两项正弦分量的角频率分别为 {{200\,\mathrm{rad}\,\mathrm{s}^{-1}}} 与 {{300\,\mathrm{rad}\,\mathrm{s}^{-1}}}，故最高角频率为 {{\Omega_m=300\,\mathrm{rad}\,\mathrm{s}^{-1}}}。同样按最小采样频率 {{\Omega_s=2\Omega_m}} 换算：",
        62,
        y,
        A4[0] - 124,
    )
    y = _formula(page, r"f_{s,\min}=\frac{300}{\pi}\,\mathrm{Hz},\qquad T_{s,\max}=\frac{\pi}{300}\,\mathrm{s}", y)
    style.draw_rich_paragraph(
        page,
        "检查时要先统一频率单位：题目给出的 50、200、300 均为角频率，不能直接把它们当作 Hz。",
        62,
        y,
        A4[0] - 124,
    )
    page.showPage()
    _start(page, 2)
    y = style.draw_title(page, "真题整理详解（续）", 770)
    y = style.draw_continuation_title(page, "2014 年真题：离散系统时变性判定", y + 6)
    y = style.draw_rich_paragraph(
        page,
        r"代入 {{g[n]=1+(-1)^n}} 可得 {{g[n-1]=1-(-1)^n}}，因此 {{g[n]+g[n-1]=2}}。系统化为 {{y[n]=2x[n]}}，不显含时间索引，故不是时变系统。",
        62,
        y,
        A4[0] - 124,
    )
    y -= 18
    y = style.draw_continuation_title(page, "2015 年真题：采样后信号的类型", y + 6)
    y = style.draw_rich_paragraph(
        page,
        "采样把连续时间自变量限制在离散的采样时刻，因此得到离散时间信号。采样本身不等同于量化；若还对幅值作离散化，才会得到数字信号。",
        62,
        y,
        A4[0] - 124,
    )
    y -= 18
    y = style.draw_continuation_title(page, "2020 年真题：组合带限信号的抽样频率", y)
    y = style.draw_rich_paragraph(
        page,
        r"线性组合 {{2x(t)+5y(t)}} 不产生高于原分量的频率。因为 {{f_2}} 是两个分量中的最高频率，无失真抽样频率应满足 {{f_s\geq 2f_2}}；取临界值时，最小采样频率为：",
        62,
        y,
        A4[0] - 124,
    )
    _formula(page, r"f_{s,\min}=2f_2", y)
    page.showPage()
    _start(page, 3)
    y = style.draw_title(page, "真题整理详解（续）", 770)
    y = style.draw_continuation_title(page, "2003 年真题：差分方程求单位样值响应", y + 6)
    y = style.draw_rich_paragraph(
        page,
        r"在零状态条件下，对差分方程作 {{z}} 变换，得到系统函数 {{H(z)=\frac{R(z)}{E(z)}}}。令 {{w=z^{-1}}}，并作部分分式展开：",
        62,
        y,
        A4[0] - 124,
    )
    y = _formula(page, r"H(z)=\frac{z^{-1}+2z^{-2}}{1-6z^{-1}+8z^{-2}}=\frac{1}{4}-\frac{1}{1-2z^{-1}}+\frac{3}{4(1-4z^{-1})}", y)
    y = style.draw_rich_paragraph(
        page,
        r"取因果系统的收敛域 {{|z|>4}}，再利用因果指数序列的 {{z}} 反变换对，可得单位样值响应：",
        62,
        y,
        A4[0] - 124,
    )
    _formula(page, r"h[n]=\frac{1}{4}\delta[n]-2^n u[n]+\frac{3}{4}\,4^n u[n]", y)
    page.showPage()


def _build(root: Path, output_path: Path | None, *, answers: bool) -> Path:
    style.register_fonts()
    load_model(root)
    default = "full/outputs/chapter_01_supplemental_answers_component.pdf" if answers else "full/outputs/chapter_01_supplemental_component.pdf"
    output = output_path or root / default
    output.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    (_answers if answers else _training)(page)
    page.save()
    return output


def build_training_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    return _build(root, output_path, answers=False)


def build_answers_pdf(root: Path = ROOT, output_path: Path | None = None) -> Path:
    return _build(root, output_path, answers=True)


if __name__ == "__main__":
    print(build_training_pdf())
    print(build_answers_pdf())
