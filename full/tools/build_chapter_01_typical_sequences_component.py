from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from sample.tools import build_sample as style

MODEL_PATH = Path("full/source/chapter_01_typical_sequences_component.json")
CHAPTER = "第一章 离散时间信号与系统"
INK, BLUE, PALE = HexColor("#1F2933"), HexColor("#123B5D"), HexColor("#F4F7F8")

def load_model(root: Path = ROOT) -> dict:
    return json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))

def start(page, number):
    style.draw_header(page, CHAPTER); style.draw_footer(page, number)

def box(page, formula, y, h=48):
    asset, iw, ih = style._math_metrics(formula, style.DISPLAY_FORMULA_SIZE)
    dh = min(h-12, ih*72/300); dw = iw*dh/ih; limit=A4[0]-148
    if dw>limit: dw,dh=limit,dh*limit/dw
    page.setFillColor(PALE); page.roundRect(62,y-h,A4[0]-124,h,3,fill=1,stroke=0)
    page.drawImage(ImageReader(str(asset)),(A4[0]-dw)/2,y-h+(h-dh)/2,dw,dh,mask="auto")
    return y-h-12

def para(page, text, y): return style.draw_rich_paragraph(page,text,62,y,A4[0]-124)
def title(page, text, y=774): return style.draw_title(page,text,y)

def section(page, text, y): return style.draw_continuation_title(page,text,y)

def draw_stem_plot(page, values, x, top, width, height, label, signed=True):
    """Draw a compact, print-safe discrete-time stem plot without label collisions."""
    page.setFillColor(HexColor("#FFFFFF")); page.setStrokeColor(HexColor("#CBD5DE"))
    page.roundRect(x, top-height, width, height, 2, fill=1, stroke=1)
    left, right = x+32, x+width-14
    baseline = top-height/2 if signed else top-height+17
    page.setStrokeColor(BLUE); page.setLineWidth(0.45)
    page.line(left, baseline, right, baseline)
    page.setFillColor(INK); page.setFont(style.FONT_SERIF, 8.2)
    page.drawString(x+7, top-13, label)
    page.setFont(style.FONT_SERIF, 7.2); page.setFillColor(HexColor("#64748B"))
    page.drawRightString(left-5, baseline-2, "0")
    maximum = max(1.0, max(abs(v) for v in values))
    scale = (height/2-15)/maximum if signed else (height-30)/maximum
    step = (right-left)/(len(values)-1)
    page.setStrokeColor(HexColor("#0F8B8D")); page.setFillColor(HexColor("#B45309")); page.setLineWidth(0.7)
    for n, value in enumerate(values):
        px, py = left+n*step, baseline+value*scale if signed else baseline+value*scale
        page.line(px, baseline, px, py)
        page.circle(px, py, 1.55, fill=1, stroke=0)
    page.setFillColor(HexColor("#64748B")); page.setFont(style.FONT_SERIF, 7.2)
    page.drawCentredString(left, top-height+5, "0")
    page.drawCentredString(right, top-height+5, str(len(values)-1))
    page.drawRightString(right+8, baseline-2, "n")
    return top-height-9

def draw_sine_example(page, y):
    values = [math.sin(0.2*math.pi*n) for n in range(10)]
    y = draw_stem_plot(page, values, 62, y, A4[0]-124, 132, "x(n)=sin(0.2πn)：10 个采样点构成一个周期", signed=True)
    return y

def draw_complex_example(page, y):
    values = [2*math.exp(-n/12) for n in range(13)]
    y = draw_stem_plot(page, [v*math.cos(math.pi*n/6) for n,v in enumerate(values)], 62, y, A4[0]-124, 72, "实部 Re{x(n)}", signed=True)
    y = draw_stem_plot(page, [v*math.sin(math.pi*n/6) for n,v in enumerate(values)], 62, y, A4[0]-124, 72, "虚部 Im{x(n)}", signed=True)
    return draw_stem_plot(page, values, 62, y, A4[0]-124, 72, "模 |x(n)|", signed=False)

def page_one(page, m):
    start(page,1); y=title(page,"几种常用的典型序列")
    y=para(page,"本节依原课件顺序介绍单位抽样、单位阶跃、矩形、实指数、正弦和复指数序列；以下保留各序列的基础定义、关系与性质。",y)
    y=section(page,"单位抽样序列",y-3); y=box(page,m['sections'][0]['formula'],y)
    y=para(page,"{{\\delta(n)}} 是脉冲幅度为 1 的离散现实序列，也称单位脉冲序列或时域离散冲激；它不同于连续时间的 {{\\delta(t)}} 数学极限。",y)
    y=section(page,"单位阶跃序列",y-3)
    for f in m['sections'][1]['formulae']: y=box(page,f,y,42)
    style.draw_note(page,"要点：{{\\delta(n)}} 是相邻两个阶跃序列之差；{{u(n)}} 可看作从负无穷到 n 的单位抽样序列累加。",y)
    page.showPage()

def page_two(page,m):
    start(page,2); y=title(page,"矩形序列与实指数序列")
    y=section(page,"矩形序列",y)
    for f in m['sections'][2]['formulae']: y=box(page,f,y,44)
    y=para(page,"矩形序列在索引 0 至 N−1 取 1，其余索引取 0；可等价地由两个阶跃序列相减，或由 N 个移位单位抽样序列求和得到。",y)
    y=section(page,"实指数序列",y-3); y=box(page,m['sections'][3]['formula'],y)
    y=para(page,"当 {{|a|<1}} 时，样值随 n 增大而衰减；当 {{|a|\\geq1}} 时发散。若 {{a<0}}，样值符号交替，呈摇动特征。",y)
    style.draw_note(page,"判断实指数序列时，应同时观察幅度 {{|a|}} 与符号 {{a}}：前者决定收敛或发散，后者决定是否正负交替。",y-4)
    page.showPage()

def page_three(page,m):
    start(page,3); y=title(page,"正弦序列")
    for f in m['sections'][4]['formulae']: y=box(page,f,y,50)
    y=para(page,"连续时间正弦信号经等间隔 {{T}} 采样后得到正弦序列。{{\\omega}} 为数字角频率（rad），{{\\Omega}} 为模拟角频率（单位：弧度每秒），二者通过 {{\\omega=\\Omega T}} 联系。",y)
    y=section(page,"数字角频率的含义",y-3)
    y=para(page,"{{\\omega=0.2\\pi}} 表示相邻样值的相位差为 {{0.2\\pi}} rad，因此一个完整周期包含 {{\\frac{2\\pi}{0.2\\pi}=10}} 个采样点。数字角频率是相对频率，而非模拟角频率的单位。",y)
    y=draw_sine_example(page,y-10)
    style.draw_note(page,"复习提示：采样频率为 {{f_s}}、连续信号频率为 {{f_0}} 时，先用 {{\\omega=2\\pi\\frac{f_0}{f_s}}} 换算，再讨论离散序列。",y-2)
    page.showPage()

def page_four(page,m):
    start(page,4); y=title(page,"复指数序列")
    for f in m['sections'][5]['formulae']: y=box(page,f,y,48)
    y=para(page,"复指数序列的实部与虚部分别是同一数字角频率的余弦和正弦序列；指数因子 {{e^{\\sigma n}}} 决定其包络。",y)
    y=section(page,"实部、虚部与模",y-3)
    y=box(page,r"\Re\{x(n)\}=e^{\sigma n}\cos(\omega n),\quad \Im\{x(n)\}=e^{\sigma n}\sin(\omega n),\quad |x(n)|=e^{\sigma n}",y,54)
    y=para(page,"例如，对 {{x(n)=2e^{(-\\frac{1}{12}+j\\frac{\\pi}{6})n}}}，实部与虚部为衰减振荡，而模值按指数规律衰减，如下图所示。",y)
    y=draw_complex_example(page,y-8)
    style.draw_note(page,"欧拉公式把复指数和正弦、余弦联系起来；后续 DTFT、DFT 与频率响应分析都会反复使用这一表示。",y-1)
    page.showPage()

def build_pdf(root: Path=ROOT, output_path: Path|None=None) -> Path:
    style.register_fonts(); m=load_model(root); out=output_path or root/'full/outputs/chapter_01_typical_sequences_component.pdf'; out.parent.mkdir(parents=True,exist_ok=True)
    page=canvas.Canvas(str(out),pagesize=A4); page.setTitle("数字信号处理讲义：第一章典型序列")
    page_one(page,m); page_two(page,m); page_three(page,m); page_four(page,m); page.save(); return out

if __name__=='__main__': print(build_pdf())
