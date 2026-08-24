"""Supplemental chapter-one real exams and detailed answers in MathJax."""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 23mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933;margin:0}main{max-width:174mm;margin:auto}
.exam-page{page-break-after:always;break-after:page;min-height:244mm}.exam-page:last-child{page-break-after:auto}.answer-flow .exam-page{page-break-after:auto;break-after:auto;min-height:0}.answer-flow .exam-page:not(:first-child)>h1{display:none}.bridge-page{page-break-after:auto;break-after:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt;break-after:avoid}.exam-head{display:flex;justify-content:space-between;color:#485b69;margin-bottom:18pt}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.signal-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}.axis{fill:none;stroke:#174b73;stroke-width:2}.stem{stroke:#b45309;stroke-width:2}.dot{fill:#b45309}.tick{stroke:#174b73;stroke-width:1.3}.label{fill:#374c5b;font:16px "Microsoft YaHei",sans-serif}.conv-line{fill:none;stroke:#008f95;stroke-width:3}
</style>"""


def _document(content: str) -> str:
    return f'<!doctype html><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}'


def supplemental_spectrum_svg() -> str:
    """Discrete spectral impulses from the 2002 sampling answer."""
    positions = (145, 275, 385, 475, 585, 715)
    heights = (54, 94, 128, 128, 94, 54)
    labels = ("−5π", "−3π", "−2π", "2π", "3π", "5π")
    parts = []
    for x, h, label in zip(positions, heights, labels):
        parts.append(f'<path class="stem" d="M{x} 184V{184-h}"/><circle class="dot" cx="{x}" cy="{184-h}" r="4"/><text class="label" x="{x}" y="213" text-anchor="middle">{label}</text>')
    return """<!-- supplemental_spectrum_svg: data-defined line spectrum -->
<svg class="signal-svg" viewBox="0 0 860 260" role="img" aria-label="连续时间幅度谱">
 <defs><marker id="sarrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path class="axis" d="M45 184H814" marker-end="url(#sarrow)"/><path class="axis" d="M430 224V38" marker-end="url(#sarrow)"/>
 __STEMS__<text class="label" x="815" y="164">Ω</text><text class="label" x="440" y="46">|X(jΩ)|</text>
</svg>""".replace("__STEMS__", "".join(parts))


def self_convolution_waveform_svg() -> str:
    """Render the 2004 rectangle self-convolution from its exact breakpoints."""
    width, height = 860, 310
    left, right, top, bottom = 82, 792, 58, 238
    x_min, x_max, y_min, y_max = -0.5, 4.6, -0.25, 2.45
    x_map = lambda value: left + (value - x_min) * (right - left) / (x_max - x_min)
    y_map = lambda value: bottom - (value - y_min) * (bottom - top) / (y_max - y_min)
    points = ((0, 0), (2, 2), (4, 0))
    polyline = " ".join(f"{x_map(x):.2f},{y_map(y):.2f}" for x, y in points)
    ticks = "".join(
        f'<line class="tick" x1="{x_map(x):.2f}" y1="{y_map(0)-5:.2f}" x2="{x_map(x):.2f}" y2="{y_map(0)+5:.2f}"/>'
        f'<text class="label" x="{x_map(x):.2f}" y="{y_map(0)+27:.2f}" text-anchor="middle">{x}</text>'
        for x in (0, 2, 4)
    )
    return rf'''<!-- self_convolution_waveform_svg: y(t) is calculated from the overlap length -->
<svg class="signal-svg" data-plot="self-convolution" viewBox="0 0 {width} {height}" role="img" aria-label="矩形脉冲自卷积的三角波形">
 <defs><marker id="conv-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <text class="label" x="{width / 2:.2f}" y="30" text-anchor="middle">矩形脉冲的自卷积波形</text>
 <line class="axis" x1="{left-12}" y1="{y_map(0):.2f}" x2="{right+22}" y2="{y_map(0):.2f}" marker-end="url(#conv-arrow)"/>
 <line class="axis" x1="{x_map(0):.2f}" y1="{bottom+8}" x2="{x_map(0):.2f}" y2="{top-12}" marker-end="url(#conv-arrow)"/>
 {ticks}
 <line class="tick" x1="{x_map(0)-5:.2f}" y1="{y_map(2):.2f}" x2="{x_map(0)+5:.2f}" y2="{y_map(2):.2f}"/>
 <text class="label" x="{x_map(0)-13:.2f}" y="{y_map(2)+5:.2f}" text-anchor="end">2</text>
 <polyline class="conv-line" points="{polyline}"/>
 <circle class="dot" cx="{x_map(2):.2f}" cy="{y_map(2):.2f}" r="4"/>
 <foreignObject x="{right+25}" y="{y_map(0)-18:.2f}" width="34" height="30"><div>\(t\)</div></foreignObject>
 <foreignObject x="{x_map(0)+10:.2f}" y="{top-34:.2f}" width="84" height="30"><div>\((f*f)(t)\)</div></foreignObject>
</svg>'''


def system_structure_svg() -> str:
    """Render the 2006 source system with explicit, equation-backed signal paths."""
    return '''<!-- system_structure_svg: signal paths match the state equations in the detailed answer -->
<svg class="signal-svg" data-diagram="2006-system-structure" viewBox="0 0 1140 540" role="img" aria-label="2006 年离散系统结构图">
 <defs><marker id="sys-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <style>.wire{fill:none;stroke:#174b73;stroke-width:2.4;marker-end:url(#sys-arrow)}.plain{fill:none;stroke:#174b73;stroke-width:2.4}.sum{fill:#fff;stroke:#174b73;stroke-width:2.4}.block{fill:#fff;stroke:#174b73;stroke-width:2.2;rx:4}.node{fill:#174b73}.dlabel{fill:#263746;font:20px "Microsoft YaHei",sans-serif}.small{fill:#263746;font:17px "Microsoft YaHei",sans-serif}.sumlabel{fill:#174b73;font:25px serif}</style>
 <text class="dlabel" x="570" y="34" text-anchor="middle">离散系统结构图</text>
 <text class="dlabel" x="48" y="266">x[n]</text><path class="wire" d="M105 260H142"/><circle class="node" cx="142" cy="260" r="4"/>
 <path class="plain" d="M142 260V72H812"/><rect class="block" x="814" y="51" width="70" height="42"/><text class="small" x="849" y="78" text-anchor="middle">0.2</text><path class="wire" d="M884 72H930V398"/>
 <rect class="block" x="204" y="239" width="72" height="42"/><text class="small" x="240" y="266" text-anchor="middle">0.25</text><path class="wire" d="M142 260H204"/><path class="wire" d="M276 260H337"/>
 <circle class="sum" cx="360" cy="260" r="23"/><text class="sumlabel" x="360" y="269" text-anchor="middle">Σ</text><text class="small" x="329" y="249">+</text><text class="small" x="351" y="301">+</text>
 <rect class="block" x="458" y="239" width="76" height="42"/><text class="dlabel" x="496" y="266" text-anchor="middle">z⁻¹</text><path class="wire" d="M383 260H458"/><path class="wire" d="M534 260H647"/>
 <circle class="sum" cx="670" cy="260" r="23"/><text class="sumlabel" x="670" y="269" text-anchor="middle">Σ</text><text class="small" x="640" y="249">+</text><text class="small" x="662" y="228">+</text>
 <rect class="block" x="531" y="112" width="58" height="42"/><text class="small" x="560" y="139" text-anchor="middle">0.5</text><path class="wire" d="M560 72V112"/><path class="wire" d="M560 154V232"/>
 <path class="wire" d="M693 260H724"/><circle class="node" cx="724" cy="260" r="4"/>
 <rect class="block" x="686" y="322" width="76" height="42"/><text class="dlabel" x="724" y="349" text-anchor="middle">z⁻¹</text><path class="wire" d="M724 260V322"/><path class="plain" d="M724 364V432"/><circle class="node" cx="724" cy="432" r="4"/>
 <path class="wire" d="M724 432H578"/><rect class="block" x="516" y="411" width="62" height="42"/><text class="small" x="547" y="438" text-anchor="middle">0.4</text><path class="wire" d="M516 432H420V283H360"/>
 <path class="wire" d="M724 260H798V326"/><rect class="block" x="768" y="326" width="60" height="42"/><text class="small" x="798" y="353" text-anchor="middle">0.3</text><path class="wire" d="M798 368V420H937"/>
 <path class="wire" d="M724 432V462H826"/><rect class="block" x="826" y="441" width="60" height="42"/><text class="small" x="856" y="468" text-anchor="middle">0.2</text><path class="wire" d="M886 462H960V443"/>
 <circle class="sum" cx="960" cy="420" r="23"/><text class="sumlabel" x="960" y="429" text-anchor="middle">Σ</text><text class="small" x="932" y="409">+</text><text class="small" x="953" y="393">+</text><text class="small" x="953" y="455">+</text><path class="wire" d="M983 420H1082"/><text class="dlabel" x="1090" y="427">y[n]</text>
 <text class="small" x="454" y="488">反馈支路</text><text class="small" x="734" y="492">一拍延时状态</text><text class="small" x="874" y="118">输入直通支路</text>
</svg>'''


def system_structure_2007_svg() -> str:
    """Clean, equation-backed redraw of the 2007 discrete-system diagram."""
    return r'''<!-- 2007-system-structure: paths follow the original two-delay system -->
<svg class="signal-svg" data-diagram="2007-system-structure" viewBox="0 0 1180 430" role="img" aria-label="2007 年离散系统结构图">
 <defs><marker id="q07-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <style>.qwire{fill:none;stroke:#174b73;stroke-width:2.6;marker-end:url(#q07-arrow)}.qplain{fill:none;stroke:#174b73;stroke-width:2.6}.qsum{fill:#fff;stroke:#174b73;stroke-width:2.6}.qblock{fill:#fff;stroke:#174b73;stroke-width:2.3;rx:5}.qnode{fill:#174b73}.qsign{fill:#174b73;font:24px serif}.qnum{fill:#263746;font:20px "Microsoft YaHei",sans-serif}</style>
 <foreignObject x="26" y="190" width="70" height="36"><div>\(x[n]\)</div></foreignObject><path class="qwire" d="M92 206H142"/><circle class="qnode" cx="142" cy="206" r="4"/>
 <path class="qplain" d="M142 206V64H1008"/><path class="qplain" d="M142 206V352H286"/>
 <circle class="qsum" cx="182" cy="206" r="25"/><text class="qsign" x="169" y="198">+</text><text class="qsign" x="174" y="229">−</text><path class="qwire" d="M207 206H278"/>
 <rect class="qblock" x="280" y="176" width="86" height="60"/><foreignObject x="299" y="189" width="50" height="34"><div>\(z^{-1}\)</div></foreignObject><path class="qwire" d="M366 206H456"/><circle class="qnode" cx="410" cy="206" r="4"/>
 <foreignObject x="384" y="150" width="68" height="30"><div>\(g_1[n]\)</div></foreignObject>
 <rect class="qblock" x="286" y="320" width="82" height="52"/><text class="qnum" x="327" y="353" text-anchor="middle">0.5</text><path class="qwire" d="M410 206V346H368"/><path class="qwire" d="M286 346H182V231"/>
 <circle class="qsum" cx="486" cy="206" r="25"/><text class="qsign" x="473" y="198">+</text><text class="qsign" x="473" y="229">+</text><text class="qsign" x="497" y="229">+</text><path class="qwire" d="M456 206H461"/><path class="qwire" d="M486 64V181"/><path class="qwire" d="M511 206H582"/>
 <rect class="qblock" x="584" y="176" width="86" height="60"/><foreignObject x="603" y="189" width="50" height="34"><div>\(z^{-1}\)</div></foreignObject><path class="qwire" d="M670 206H768"/><circle class="qnode" cx="718" cy="206" r="4"/>
 <foreignObject x="690" y="150" width="68" height="30"><div>\(g_2[n]\)</div></foreignObject>
 <rect class="qblock" x="590" y="320" width="82" height="52"/><text class="qnum" x="631" y="353" text-anchor="middle">0.4</text><path class="qwire" d="M718 206V346H672"/><path class="qwire" d="M590 346H486V231"/>
 <rect class="qblock" x="784" y="176" width="76" height="60"/><text class="qnum" x="822" y="212" text-anchor="middle">0.2</text><path class="qwire" d="M768 206H784"/><path class="qwire" d="M860 206H926"/>
 <circle class="qsum" cx="956" cy="206" r="25"/><text class="qsign" x="943" y="198">+</text><text class="qsign" x="943" y="229">+</text><path class="qwire" d="M981 206H1060"/><foreignObject x="1066" y="190" width="80" height="36"><div>\(y[n]\)</div></foreignObject><path class="qwire" d="M956 64V181"/>
 <text class="qnum" x="590" y="406" text-anchor="middle">主信号流从左至右；反馈支路按原图的 0.5 与 0.4 系数连接。</text>
</svg>'''


def convolution_2016_svg(kind: str = "inputs") -> str:
    """Programmatic textbook stem plots for the 2016 discrete convolution question."""
    if kind == "inputs":
        panels = (
            ("f_1[n]", (-2, -1, 0, 1, 2), (1, 1, -1, 1, 1), 110),
            ("f_2[n]", (0, 1, 2, 3), (1, -1, 1, -1), 400),
        )
        title, height = "2016 年真题：卷积的两个输入序列", 320
    else:
        panels = (("f[n]", (-2, -1, 0, 1, 2, 3, 4, 5), (1, 0, -1, 2, -2, 1, 0, -1), 150),)
        title, height = "卷积结果", 320

    def panel(label: str, indices: tuple[int, ...], values: tuple[int, ...], left: int) -> str:
        base, top, bottom, step = 148, 48, 236, 52
        zero_x = left + (0 - indices[0]) * step
        axis_zero_x = zero_x
        axis_start, axis_end = left - 26, left + (indices[-1] - indices[0]) * step + 38
        ticks, stems = [], []
        for index, value in zip(indices, values):
            x, y = left + (index - indices[0]) * step, base - value * 55
            if index != 0:
                ticks.append(f'<line class="tick" data-index="{index}" x1="{x}" y1="{base-5}" x2="{x}" y2="{base+5}"/><text class="label" data-index="{index}" x="{x}" y="{base+27}" text-anchor="middle">{index}</text>')
            stems.append(f'<line class="stem" x1="{x}" y1="{base}" x2="{x}" y2="{y}"/><circle class="dot" cx="{x}" cy="{y}" r="4"/><text class="label" x="{x}" y="{y-10 if value > 0 else y+24}" text-anchor="middle">{value}</text>')
        return rf'''<g>
 <path class="axis" d="M{axis_start} {base}H{axis_end}" marker-end="url(#conv2016-arrow)"/>
 <path class="axis" data-origin-at-zero="true" d="M{axis_zero_x} {bottom}V{top}" marker-end="url(#conv2016-arrow)"/>
 {''.join(ticks)}{''.join(stems)}<text class="label" data-origin-label="true" x="{axis_zero_x+10}" y="{base+27}" text-anchor="start">0</text>
 <foreignObject x="{axis_end-2}" y="{base+13}" width="32" height="34"><div>\(n\)</div></foreignObject>
 <foreignObject x="{axis_zero_x+10}" y="{top-12}" width="90" height="34"><div>\({label}\)</div></foreignObject>
</g>'''

    body = ''.join(panel(*item) for item in panels)
    return f'''<!-- convolution_2016_svg: exact samples from the original exam figure, rendered with real SVG coordinates -->
<svg class="signal-svg" data-source-candidate-id="2016-qintro-01" data-plot="2016-discrete-convolution-{kind}" viewBox="0 0 760 {height}" role="img" aria-label="{title}">
 <defs><marker id="conv2016-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <text class="label" x="380" y="28" text-anchor="middle">{title}</text>
 {body}
</svg>'''


def convolution_2021_svg(kind: str = "inputs") -> str:
    """Programmatic textbook stem plots for the 2021 discrete convolution question."""
    if kind == "inputs":
        panels = (
            ("f_1[n]", range(-2, 3), {-2: 1, -1: 1, 1: 1, 2: 1}, 84, 48),
            ("f_2[n]", range(-1, 4), {-1: 1, 1: -1, 2: 2, 3: -1}, 444, 48),
        )
        title, height = "2021 年真题：卷积的两个输入序列", 330
    else:
        panels = (("f[n]", range(-3, 6), {-3: 1, -2: 1, -1: -1, 0: 1, 1: 1, 2: -2, 3: 1, 4: 1, 5: -1}, 82, 62),)
        title, height = "2021 年真题：离散卷积结果", 330

    def panel(label: str, tick_range: range, samples: dict[int, int], left: int, step: int) -> str:
        base, top, bottom = 182, 55, 276
        zero_x = left + (0 - tick_range.start) * step
        axis_zero_x = zero_x
        axis_start, axis_end = left - 28, left + (tick_range.stop - tick_range.start - 1) * step + 42
        ticks, stems = [], []
        for index in tick_range:
            x = left + (index - tick_range.start) * step
            if index != 0:
                ticks.append(f'<line class="tick" data-index="{index}" x1="{x}" y1="{base-5}" x2="{x}" y2="{base+5}"/><text class="label" data-index="{index}" x="{x}" y="{base+29}" text-anchor="middle">{index}</text>')
        for index, value in samples.items():
            x, y = left + (index - tick_range.start) * step, base - value * 48
            label_y = y - 10 if value > 0 else y + 25
            stems.append(f'<line class="stem" x1="{x}" y1="{base}" x2="{x}" y2="{y}"/><circle class="dot" cx="{x}" cy="{y}" r="4"/><text class="label" x="{x}" y="{label_y}" text-anchor="middle">{value}</text>')
        return rf'''<g>
 <path class="axis" d="M{axis_start} {base}H{axis_end}" marker-end="url(#conv2021-arrow)"/>
 <path class="axis" data-origin-at-zero="true" d="M{axis_zero_x} {bottom}V{top}" marker-end="url(#conv2021-arrow)"/>
 {''.join(ticks)}{''.join(stems)}<text class="label" data-origin-label="true" x="{axis_zero_x+10}" y="{base+29}" text-anchor="start">0</text>
 <foreignObject x="{axis_end-4}" y="{base+12}" width="32" height="34"><div>\(n\)</div></foreignObject>
 <foreignObject x="{axis_zero_x+10}" y="{top-14}" width="90" height="34"><div>\({label}\)</div></foreignObject>
</g>'''

    return f'''<!-- convolution_2021_svg: exact source samples rendered as true-coordinate textbook stem plots -->
<svg class="signal-svg" data-source-candidate-id="2021-qintro-01" data-plot="2021-discrete-convolution-{kind}" viewBox="0 0 760 {height}" role="img" aria-label="{title}">
 <defs><marker id="conv2021-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <text class="label" x="380" y="29" text-anchor="middle">{title}</text>
 {''.join(panel(*item) for item in panels)}
</svg>'''


def sampling_2019_svg(kind: str) -> str:
    """Data-driven textbook plots for the 2019 Sa(2t) sampling question."""
    marker = '<defs><marker id="s19-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>'
    if kind == "time":
        left, right, top_base, bottom_base = 58, 812, 126, 346
        x_min, x_max = -3.7, 3.7
        x = lambda t: left + (t - x_min) * (right - left) / (x_max - x_min)
        sa = lambda t: 1.0 if abs(t) < 1e-12 else math.sin(2 * t) / (2 * t)
        curve = " ".join(f"{x(t):.1f},{top_base-78*sa(t):.1f}" for t in (-3.5+i*0.025 for i in range(281)))
        samples = []
        for n in range(-7, 8):
            t, value, px = n * math.pi / 6, sa(n * math.pi / 6), x(n * math.pi / 6)
            py = bottom_base - 94 * value
            samples.append(f'<line class="stem" x1="{px:.1f}" y1="{bottom_base}" x2="{px:.1f}" y2="{py:.1f}" marker-end="url(#s19-arrow)"/>')
        ticks = "".join(
            f'<line class="tick" x1="{x(t):.1f}" y1="{bottom_base-5}" x2="{x(t):.1f}" y2="{bottom_base+5}"/><foreignObject x="{x(t)-26:.1f}" y="{bottom_base+12}" width="52" height="30"><div>\\({label}\\)</div></foreignObject>'
            for t, label in ((-math.pi/6, r"-T_s"), (0, "0"), (math.pi/6, r"T_s"))
        )
        return rf'''<!-- sampling_2019_svg: Sa(2t) curve and impulse samples use exact coordinates -->
<svg class="signal-svg" data-plot="2019-sa-sampling-time" viewBox="0 0 870 430" role="img" aria-label="Sa(2t) 与冲激采样序列">
 {marker}
 <text class="label" x="435" y="28" text-anchor="middle">原信号与冲激串采样</text>
 <path class="axis" d="M{left} {top_base}H{right}" marker-end="url(#s19-arrow)"/><path class="axis" d="M{x(0):.1f} {top_base+82}V42" marker-end="url(#s19-arrow)"/>
 <polyline class="conv-line" points="{curve}"/>
 <foreignObject x="{right-2}" y="{top_base+9}" width="32" height="28"><div>\(t\)</div></foreignObject><foreignObject x="{right-170}" y="42" width="148" height="32"><div>\(f(t)=\operatorname{{Sa}}(2t)\)</div></foreignObject>
 <path class="axis" d="M{left} {bottom_base}H{right}" marker-end="url(#s19-arrow)"/><path class="axis" d="M{x(0)-10:.1f} {bottom_base+60}V{bottom_base-116}" marker-end="url(#s19-arrow)"/>
 {''.join(samples)}{ticks}
 <foreignObject x="{right-2}" y="{bottom_base+9}" width="32" height="28"><div>\(t\)</div></foreignObject><foreignObject x="{right-124}" y="{bottom_base-112}" width="94" height="30"><div>\(f_s(t)\)</div></foreignObject>
</svg>'''
    left, right, base, top = 58, 812, 226, 70
    x_min, x_max = -27, 27
    x = lambda omega: left + (omega-x_min)*(right-left)/(x_max-x_min)
    bands = "".join(
        f'<rect x="{x(12*k-2):.1f}" y="106" width="{x(12*k+2)-x(12*k-2):.1f}" height="{base-106:.1f}" fill="#d9efed" stroke="#008f95" stroke-width="2"/>'
        for k in range(-2, 3)
    )
    ticks = "".join(
        f'<line class="tick" x1="{x(value):.1f}" y1="{base-5}" x2="{x(value):.1f}" y2="{base+5}"/><foreignObject x="{x(value)-32:.1f}" y="{base+11}" width="64" height="30"><div>\\({label}\\)</div></foreignObject>'
        for value, label in ((-12, r"-\omega_s"), (0, "0"), (12, r"\omega_s"))
    )
    return rf'''<!-- sampling_2019_svg: periodic replicas of F(j omega), with exact period omega_s=12 -->
<svg class="signal-svg" data-plot="2019-sa-sampling-spectrum" viewBox="0 0 870 300" role="img" aria-label="冲激采样后的周期频谱">
 {marker}
 <text class="label" x="435" y="28" text-anchor="middle">冲激采样后的周期频谱</text>
 {bands}
 <path class="axis" d="M{left} {base}H{right}" marker-end="url(#s19-arrow)"/><path class="axis" d="M{x(0):.1f} {base+40}V{top}" marker-end="url(#s19-arrow)"/>
 {ticks}
 <foreignObject x="{right-2}" y="{base+8}" width="42" height="28"><div>\(\omega\)</div></foreignObject><foreignObject x="{right-168}" y="60" width="128" height="34"><div>\(F_s(j\omega)\)</div></foreignObject>
</svg>'''


def ad_da_chain_svg() -> str:
    """Textbook-style A/D--digital filter--D/A chain and exact input triangle spectrum."""
    return '''<!-- ad_da_chain_svg: source sampling period and all signal paths are explicit -->
<svg class="signal-svg" data-source-candidate-id="2022-q七-01" data-diagram="2022-ad-da-chain" viewBox="0 0 900 390" role="img" aria-label="A/D、数字低通和 D/A 串联系统及输入频谱">
 <defs><marker id="ad-da-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <g fill="none" stroke="#174b73" stroke-width="3" marker-end="url(#ad-da-arrow)">
  <path d="M55 80H150"/><path d="M245 80H350"/><path d="M455 80H555"/><path d="M650 80H835"/>
 </g><g fill="#1f2933" font-size="24"><text x="72" y="55" font-style="italic">x(t)</text><text x="267" y="55" font-style="italic">x[n]</text><text x="473" y="55" font-style="italic">x₁[n]</text><text x="710" y="55" font-style="italic">yₐ(t)</text></g>
 <g fill="#fff" stroke="#174b73" stroke-width="2.5"><rect x="150" y="47" width="95" height="66" rx="4"/><rect x="350" y="47" width="105" height="66" rx="4"/><rect x="555" y="47" width="95" height="66" rx="4"/></g>
 <g fill="#1f2933" font-size="25" text-anchor="middle"><text x="197" y="89">A/D</text><text x="402" y="89" font-style="italic">h[n]</text><text x="602" y="89">D/A</text></g>
 <path d="M112 136V93" stroke="#174b73" stroke-width="3" marker-end="url(#ad-da-arrow)"/><text x="98" y="165" fill="#1f2933" font-size="23" font-style="italic">T</text>
 <g transform="translate(120 230)" fill="none" stroke="#174b73" stroke-width="2.5"><path d="M0 100H650" marker-end="url(#ad-da-arrow)"/><path d="M325 150V15" marker-end="url(#ad-da-arrow)"/><path d="M155 100L325 40L495 100" stroke="#0b8b8c" stroke-width="4"/></g>
 <g fill="#1f2933" font-size="22"><text x="780" y="335" font-style="italic">f (kHz)</text><text x="457" y="242" font-style="italic">X(jf)</text><text x="438" y="346">0</text><text x="265" y="346">−1</text><text x="605" y="346">1</text><text x="445" y="276">1</text></g>
</svg>'''


def ad_da_output_spectrum_svg(cutoff_khz: float) -> str:
    """Exact output spectrum after the discrete low-pass and ideal D/A conversion."""
    center, scale, baseline = 430, 260, 190
    half = cutoff_khz * scale
    peak_y, amplitude_px = 75, 115
    edge_y = baseline - amplitude_px * (1 - cutoff_khz)
    return f'''<!-- ad_da_output_spectrum_svg: cutoff={cutoff_khz} kHz controls triangle support -->
<svg class="signal-svg" data-plot="2022-ad-da-output-{cutoff_khz}" viewBox="0 0 860 270" role="img" aria-label="D/A 输出频谱">
 <defs><marker id="out-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path d="M90 {baseline}H780" stroke="#174b73" stroke-width="2.5" marker-end="url(#out-arrow)"/><path d="M{center} 225V35" stroke="#174b73" stroke-width="2.5" marker-end="url(#out-arrow)"/>
 <path d="M{center-half:.1f} {baseline}V{edge_y:.1f}L{center} {peak_y}L{center+half:.1f} {edge_y:.1f}V{baseline}" fill="none" stroke="#0b8b8c" stroke-width="4"/>
 <g fill="#1f2933" font-size="22"><text x="790" y="198" font-style="italic">f (kHz)</text><text x="444" y="48" font-style="italic">Yₐ(jf)</text><text x="{center-half-12:.1f}" y="220">−{cutoff_khz:g}</text><text x="{center-7}" y="220">0</text><text x="{center+half-5:.1f}" y="220">{cutoff_khz:g}</text><text x="{center+10}" y="88">1</text></g>
</svg>'''


def dtft_sampling_2023_svg(sample_rate: int) -> str:
    """True-coordinate discrete DTFT plot on [0, 2π] for the 2023 sampling question."""
    if sample_rate == 100:
        stems = [(430, "π", "2π")]
    elif sample_rate == 150:
        stems = [(323, "2π/3", "π"), (537, "4π/3", "π")]
    else:
        raise ValueError(f"unsupported sample rate: {sample_rate}")
    stem_svg = "".join(
        f'<path d="M{x} 190V82" stroke="#0b8b8c" stroke-width="4" marker-end="url(#dtft-arrow)"/>'
        f'<text x="{x-18}" y="222">{position}</text><text x="{x+10}" y="76">{amplitude}</text>'
        for x, position, amplitude in stems
    )
    return f'''<!-- dtft_sampling_2023_svg: discrete spectral impulses calculated from fs={sample_rate} Hz -->
<svg class="signal-svg" data-plot="2023-dtft-sampling-{sample_rate}" viewBox="0 0 860 270" role="img" aria-label="采样序列的 DTFT 离散频谱">
 <defs><marker id="dtft-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path d="M100 190H790" stroke="#174b73" stroke-width="2.5" marker-end="url(#dtft-arrow)"/><path d="M110 225V40" stroke="#174b73" stroke-width="2.5" marker-end="url(#dtft-arrow)"/>
 {stem_svg}<g fill="#1f2933" font-size="22"><text x="792" y="198" font-style="italic">ω</text><text x="118" y="52" font-style="italic">X(eʲω)</text><text x="102" y="220">0</text><text x="760" y="220">2π</text></g>
</svg>'''


def rectangular_pulse_2024_svg() -> str:
    """Exact source rectangle f(t)=1 on [-2, 2], redrawn with full axes."""
    return r'''<!-- rectangular_pulse_2024_svg: source breakpoints -2 and 2 rendered as true coordinates -->
<svg class="signal-svg" data-plot="2024-rectangular-pulse" viewBox="0 0 860 310" role="img" aria-label="2024 年矩形脉冲信号">
 <defs><marker id="rect2024-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path class="axis" d="M112 205H770" marker-end="url(#rect2024-arrow)"/><path class="axis" d="M430 253V45" marker-end="url(#rect2024-arrow)"/>
 <path d="M230 205V95H630V205" fill="none" stroke="#0b8b8c" stroke-width="4"/>
 <g class="tick"><path d="M230 200V210"/><path d="M430 200V210"/><path d="M630 200V210"/><path d="M425 95H435"/></g>
 <g class="label"><text x="230" y="234" text-anchor="middle">−2</text><text x="442" y="234">0</text><text x="630" y="234" text-anchor="middle">2</text><text x="444" y="102">1</text></g>
 <foreignObject x="774" y="186" width="34" height="32"><div>\(t\)</div></foreignObject>
 <foreignObject x="442" y="39" width="56" height="32"><div>\(f(t)\)</div></foreignObject>
</svg>'''


def pulse_sampling_2024_svg() -> str:
    """Centered 40-us rectangular sampling train, driven by T and pulse width."""
    centers = (-120, -60, 0, 60, 120)
    pulse_paths = "".join(f'<path d="M{430 + center - 10} 205V95H{430 + center + 10}V205" fill="none" stroke="#0b8b8c" stroke-width="3.5"/>' for center in centers)
    return rf'''<!-- pulse_sampling_2024_svg: T_s=40 us and tau=10 us determine each pulse coordinate -->
<svg class="signal-svg" data-plot="2024-pulse-sampling-train" viewBox="0 0 860 310" role="img" aria-label="周期矩形脉冲采样序列">
 <defs><marker id="pulse2024-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path class="axis" d="M135 205H760" marker-end="url(#pulse2024-arrow)"/><path class="axis" d="M430 252V45" marker-end="url(#pulse2024-arrow)"/>
 {pulse_paths}
 <g class="tick"><path d="M370 200V210"/><path d="M430 200V210"/><path d="M490 200V210"/><path d="M425 95H435"/></g>
 <g class="label"><text x="370" y="234" text-anchor="middle">−40</text><text x="442" y="234">0</text><text x="490" y="234" text-anchor="middle">40</text><text x="444" y="102">1</text><text x="430" y="274" text-anchor="middle">单位：μs</text></g>
 <foreignObject x="764" y="186" width="34" height="32"><div>\(t\)</div></foreignObject><foreignObject x="452" y="39" width="58" height="32"><div>\(s(t)\)</div></foreignObject>
</svg>'''


def pulse_spectrum_2024_svg(kind: str) -> str:
    """Frequency-domain rectangles for the original and sampled 2024 signal."""
    if kind == "baseband":
        bands = '<path d="M275 190V88H585V190" fill="#d9efed" fill-opacity="0.7" stroke="#008f95" stroke-width="3"/>'
        ticks = '<text class="label" x="275" y="220" text-anchor="middle">−5</text><text class="label" x="438" y="220">0</text><text class="label" x="585" y="220" text-anchor="middle">5</text><text class="label" x="444" y="97">1</text>'
        title, label = "原信号频谱", r"F(f)"
    elif kind == "sampled":
        bands = ''.join((
            '<path d="M115 190V111H205V190" fill="#d9efed" fill-opacity="0.7" stroke="#008f95" stroke-width="3"/>',
            '<path d="M385 190V98H475V190" fill="#d9efed" fill-opacity="0.7" stroke="#008f95" stroke-width="3"/>',
            '<path d="M655 190V111H745V190" fill="#d9efed" fill-opacity="0.7" stroke="#008f95" stroke-width="3"/>'
        ))
        ticks = '<text class="label" x="160" y="220" text-anchor="middle">−25</text><text class="label" x="438" y="220">0</text><text class="label" x="700" y="220" text-anchor="middle">25</text><text class="label" x="482" y="105">C₀</text><text class="label" x="750" y="119">C₁</text>'
        title, label = "脉冲采样后的频谱副本", r"F_s(f)"
    else:
        raise ValueError(f"unsupported pulse spectrum kind: {kind}")
    return rf'''<!-- pulse_spectrum_2024_svg: rectangles are centered at k f_s with source width 10 kHz -->
<svg class="signal-svg" data-plot="2024-pulse-spectrum-{kind}" viewBox="0 0 860 270" role="img" aria-label="{title}">
 <defs><marker id="pulsespec-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <text class="label" x="430" y="28" text-anchor="middle">{title}</text><path class="axis" d="M72 190H790" marker-end="url(#pulsespec-arrow)"/><path class="axis" d="M430 225V48" marker-end="url(#pulsespec-arrow)"/>
 {bands}<g class="label">{ticks}<text x="795" y="199" font-style="italic">f (kHz)</text></g><foreignObject x="442" y="44" width="88" height="34"><div>\({label}\)</div></foreignObject>
</svg>'''


def h1_bandpass_2024_svg() -> str:
    """Exact two-passband H1(f): [-37,-12] and [12,37] kHz."""
    return r'''<!-- h1_bandpass_2024_svg: passband edges are -37,-12,12,37 kHz from the source figure -->
<svg class="signal-svg" data-plot="2024-h1-bandpass" viewBox="0 0 860 290" role="img" aria-label="H1 的带通频率响应">
 <defs><marker id="h1-2024-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path class="axis" d="M58 205H798" marker-end="url(#h1-2024-arrow)"/><path class="axis" d="M430 238V45" marker-end="url(#h1-2024-arrow)"/>
 <path d="M88 205V105H318V205M542 205V105H772V205" fill="#d9efed" fill-opacity="0.7" stroke="#008f95" stroke-width="3"/>
 <g class="label"><text x="88" y="233" text-anchor="middle">−37</text><text x="318" y="233" text-anchor="middle">−12</text><text x="442" y="233">0</text><text x="542" y="233" text-anchor="middle">12</text><text x="772" y="233" text-anchor="middle">37</text><text x="442" y="114">1</text><text x="801" y="214" font-style="italic">f (kHz)</text></g>
 <foreignObject x="442" y="38" width="72" height="34"><div>\(H_1(f)\)</div></foreignObject>
</svg>'''


QUESTIONS = (
    (2002, 60, r"已知 \(x(t)=\cos(50t)\)，对其进行时域采样。要求能从采样信号中恢复原始信号，填空：奈奎斯特频率为______ \(\mathrm{Hz}\)；奈奎斯特采样周期为______ \(\mathrm{s}\)。"),
    (2003, 60, r"已知 \(x(t)=1+\cos(200t)+\sin(300t)\)，对其进行时域采样。要求能从采样信号中恢复原始信号，填空：奈奎斯特频率为______ \(\mathrm{Hz}\)；奈奎斯特采样周期为______ \(\mathrm{s}\)。"),
    (2004, "____", r"线性时不变系统的输入为：\(x(n)=u(n)\)，输出\(y(n)=\left[4\left(\frac{1}{2}\right)^n-3\left(-\frac{3}{4}\right)^n\right]u(n)\)<br>（1）求系统的单位冲激响应；<br>（2）判断系统的稳定性和因果性，并说明理由。"),
    (2005, "____", r"某离散系统可由二阶常系数线性差分方程描述，且已知该系统单位阶跃响应序列为\(y(n)=[2^n+3(5)^n+10]u(n)\)。<br>（1）求此二阶差分方程；<br>（2）若激励为\(f(n)=3u(n)+3u(n-7)\)，求响应\(y(n)\)。"),
    (2007, "____", r"已知\(x(t)=\cos(1000\pi t)\frac{\sin 400t}{\pi t}\)，对其进行时域抽样；"),
    (2007, "____", r"已知一离散系统如图所示：<br>（1）写出描述该系统的差分方程；<br>（2）求解该系统的单位冲激响应。"),
    (2007, "____", r"已知一个线性时不变系统的单位冲激响应除区间\(N_1&lt;n&lt;N_2\)之外皆为零，又已知输入序列\(x(n)\)除区间\(N_3&lt;n&lt;N_4\)之外皆为零，则该系统的输出除________区间之外皆为零。"),
    (2013, "____", r"已知信号\(x(t)\)是带限信号，其频谱函数的截止频率\(\omega_m=1500\pi\mathrm{rad}/\mathrm{s}\)，对信号\(y(t)=x(t)\cdot x(2t)\)进行时域采样，满足采样定理的最大采样间隔\(T_{\max}\)________。"),
    (2013, "____", r"设离散时间 LTI 系统的冲激响应\(h(n)=a^n u[n]\)，试判断系统的因果稳定性。"),
    (2014, 61, r"已知系统 \(y[n]=x[n]\{g[n]+g[n-1]\}\)，若 \(g[n]=1+(-1)^n\)，则系统是否为时变系统？______。"),
    (2014, "____", r"设\(f_1[n]=2^n\left\{u[n]-u[n-3]\right\}\)，\(f_2[n]=2\delta[n+1]+5\delta[n-1]\)，则\(f_1[n]\)和\(f_2[n]\)的卷积结果为________。"),
    (2014, "____", r"如果\(x(t)\)的最高频率\(\omega_m\)，若对\(x\left(\frac{t}{4}\right)\cdot x\left(\frac{t}{2}\right)\)采样，则频谱不混叠的最大采样时间间隔是________。"),
    (2015, 61, "对模拟信号进行采样，得到的是______信号。"),
    (2015, "____", "数字信号处理的三种基本运算是______、______、______。"),
    (2016, "____", r"系统如图所示，求\(f(n)=f_1(n)*f_2(n)\)；"),
    (2016, "____", r"\(\mathcal{T}\{u(n)\}=g(n)\)，那么\(x(n)=(n+1)R_3(n)\)，则\(y(n)=?\)"),
    (2017, "____", r"试判断下列各方程描述的系统的线性、时不变性、因果性。<br>\(y(n)=\sum_{m=0}^{n}x(m)\)；\(y(t)=\frac{\mathrm{d}}{\mathrm{d}t}f(t)\)；\(y(t)=\max\left(f_1(t),f_2(t),f_3(t)\ldots\right)\)。"),
    (2019, "____", r"设系统 \(y[n]=n x[n-1]+x[n-2]\)，判断该系统是否线性、时变、因果。"),
    (2019, "____", r"已知\(f(t)=\operatorname{Sa}(2t)\)，\(\delta_T(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT_s)\)：<br>（1）求奈奎斯特频率；<br>（2）若\(\omega_s=6\omega_m\)，求\(f_s(t)=f(t)\delta_T(t)\)，并画波形；<br>（3）设\(F_s(j\omega)\)是\(f_s(t)\)的傅里叶变换，画出\(f_s(t)\)的频谱图；<br>（4）用一采样保持器使其在输出端恢复原信号。"),
    (2020, 61, r"已知频带宽度有限信号 \(x(t)\)、\(y(t)\) 的最高频率分别为 \(f_1\) 和 \(f_2\)，其中 \(f_1&lt;f_2\)，则对信号 \(2x(t)+5y(t)\) 进行无失真抽样的采样频率为______。"),
    (2021, "____", r"已知 \(f_1[n]\) 和 \(f_2[n]\) 的波形如图所示，求 \(f_1[n]\) 和 \(f_2[n]\) 的卷积。"),
    (2022, "____", r"已知信号 \(f(t)=\mathrm{e}^{-5t}u(t)\)，其经过周期为 \(T\) 的理想采样信号采样后得到 \(f_s(t)\)，求采样后信号的拉氏变换 \(F_s(s)\)。"),
    (2022, "____", r"已知信号 \(x(t)=2+\sum_{k=1}^{4}\cos(k\omega_0t)\)，现对其进行采样，试回答以下问题：<br>（1）求出对该信号采样的奈奎斯特频率；<br>（2）当 \(\omega_0=\frac{\pi}{4}\) 时，采样周期为 \(1.2\,\mathrm{s}\)，求采样后信号的频谱函数；<br>（3）当 \(\omega_0=\frac{\pi}{4}\) 时，采样周期为 \(0.5\,\mathrm{s}\)，求采样后信号的频谱函数。"),
    (2016, "____", r"已知 \(x(n)=R_6(n)\)。<br>（1）求 \(x_e(n)\)；<br>（2）求 \(x_o(n)R_8(n)\)。"),
    (2021, "____", r"已知信号 \(x(t)=10\cos(20\pi t)\cos(200\pi t)\)，抽样频率 \(f_s=250\,\mathrm{Hz}\)：<br>（1）求抽样信号 \(x_s(t)\) 的频谱；<br>（2）要无失真恢复 \(x(t)\)，试求出对 \(x_s(t)\) 采用的低通滤波器的截止频率。"),
    (2022, "____", r"一连续信号 \(x(t)\)，经过 \(T\) 周期采样与 A/D 转换后得到离散信号 \(x[n]\)，再通过一理想低通滤波器 \(h[n]\)，其截止频率为 \(\omega_c=\frac{\pi}{4}\)，得到信号 \(x_1[n]\)，最后 D/A 转换得到信号 \(y_a(t)\)。已知 \(X(jf)\) 如图。<br>（1）当 \(T=0.05\,\mathrm{ms}\) 时，画出 \(y_a(t)\) 的频谱图；<br>（2）当 \(T=0.25\,\mathrm{ms}\) 时，画出 \(y_a(t)\) 的频谱图。"),
    (2023, "____", r"\(x(n)=\left(\frac{1}{2}\right)^n u(n)\)，系统的输出为 \(g(n)\)，求系统单位脉冲 \(h(n)\)。"),
    (2023, "____", r"对 \(x_c(t)=\cos(100\pi t)\) 进行理想采样，得到 \(x(n)\)，画出以下采样频率下的序列傅里叶变换 \(X(\mathrm{e}^{j\omega})\) 在 \(\omega\in[0,2\pi]\) 内的示意图。<br>（1）\(f_s=100\,\mathrm{Hz}\)；<br>（2）\(f_s=150\,\mathrm{Hz}\)。"),
    (2023, "____", r"已知信号 \(f(t)=A\sin(\omega_0t)\)，若对原信号 \(f(t)\) 进行采样传输，满足采样定理要求，试给出合理的采样频率和采样周期。"),
    (2024, "____", r"矩形脉冲信号 \(f(t)\) 如图所示，以采样角频率 \(\Omega_s=2\pi\,\mathrm{rad}\,\mathrm{s}^{-1}\) 对其采样，试说明采样后能否恢复原信号？计算以该采样率获得的离散时间序列的离散时间傅里叶变换。"),
    (2024, "____", r"已知信号 \(f(t)=10^4\operatorname{Sa}(10^4t)\)，采样序列 \(s(t)\) 周期为 \(T_s=40\,\mu\mathrm{s}\)，脉冲宽度为 \(10\,\mu\mathrm{s}\)，幅度为 \(1\,\mathrm{V}\)，波形如图。<br>（1）求 \(f(t)\) 的频谱并绘制出频谱图，计算该信号的带宽；<br>（2）试计算 \(f_s(t)\) 的频谱；<br>（3）若已知一系统 \(H_1(f)\) 的频率响应如图所示，试构造一个系统，使得与系统 \(H_1(f)\) 串联后的输出为 \(f(t)\)。"),
    (2025, "____", r"系统 \(y[n]=\sum_{i=-\infty}^{\infty}a^{n-i}x[i]\)，\(a\ne0\)，系统是否可逆，若可逆，求其逆系统。"),
    (2002, 62, r"有一信号 \(x(t)=3\cos(2\pi t)+2\sin(3\pi t)+\cos(5\pi t)\)，现以 \(\Omega_s=8\pi\) 的频率对其采样得到离散信号 \(x(n)\)。画出 \(x(t)\) 和 \(x(n)\) 的幅度谱，判断是否存在混叠；若存在，说明避免方法并画出不失真时的离散频谱。"),
    (2003, 62, r"信号经过理想冲激串采样后，再经过增益为 \(T\) 的理想低通滤波器。证明：当低通滤波器截止角频率为 \(\omega_c=\frac{\omega_s}{2}\) 时，对任意 \(T\)，重建信号与原信号在采样时刻始终相等。"),
    (2003, 61, r"已知系统差分方程为 \(r(n)-6r(n-1)+8r(n-2)=e(n-1)+2e(n-2)\)，求单位样值响应。"),
)


def write_questions_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    pages = []
    for index, (year, answer_page, prompt) in enumerate(QUESTIONS):
        title = "第一章 补充真题" if index == 0 else "第一章 补充真题（续）"
        if "描述该系统的差分方程" in prompt:
            figure = system_structure_2007_svg()
        elif "f_1(n)*f_2(n)" in prompt:
            figure = convolution_2016_svg()
        elif "f_1[n]" in prompt and "卷积" in prompt:
            figure = convolution_2021_svg()
        elif "A/D 转换后得到离散信号" in prompt:
            figure = ad_da_chain_svg()
        elif "序列傅里叶变换" in prompt:
            figure = dtft_sampling_2023_svg(100) + dtft_sampling_2023_svg(150)
        elif "矩形脉冲信号" in prompt:
            figure = rectangular_pulse_2024_svg()
        elif "采样序列" in prompt:
            figure = pulse_sampling_2024_svg() + h1_bandpass_2024_svg()
        else:
            figure = ""
        pages.append(f'<section class="exam-page"><h1>{title}</h1><div class="exam-head"><span>{year} 年真题</span><span>详解见 P.{answer_page}</span></div><p>{prompt}</p>{figure}</section>')
    output.write_text(_document("<main>" + "".join(pages) + "</main>"), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    spectrum = supplemental_spectrum_svg()
    sampling_time = sampling_2019_svg("time")
    sampling_spectrum = sampling_2019_svg("spectrum")
    content = r"""
<main class="answer-flow">
<section class="exam-page"><h1>真题整理详解</h1><h2>2002 年真题：单频正弦信号采样</h2><p>最高角频率为 \(\Omega_m=50\,\mathrm{rad}\,\mathrm{s}^{-1}\)。无混叠恢复要求 \(\Omega_s\geq2\Omega_m\)，换算为频率与采样周期：</p><div class="formula">\[f_{s,\min}=\frac{50}{\pi}\,\mathrm{Hz},\qquad T_{s,\max}=\frac{\pi}{50}\,\mathrm{s}\]</div><h2>2003 年真题：多频正弦信号采样</h2><p>常数项不增加频率上限，最高角频率为 \(\Omega_m=300\,\mathrm{rad}\,\mathrm{s}^{-1}\)。</p><div class="formula">\[f_{s,\min}=\frac{300}{\pi}\,\mathrm{Hz},\qquad T_{s,\max}=\frac{\pi}{300}\,\mathrm{s}\]</div><p>检查时必须先统一单位：50、200、300 均为角频率，不能直接当作 Hz。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2014 年真题：离散系统时变性判定</h2><p>代入 \(g[n]=1+(-1)^n\)，有 \(g[n-1]=1-(-1)^n\)，故 \(g[n]+g[n-1]=2\)。系统化为 \(y[n]=2x[n]\)，不显含时间索引，故不是时变系统。</p><h2>2014 年真题：有限长序列卷积</h2><p>利用冲激序列的移位性质 \(f[n]*\delta[n-n_0]=f[n-n_0]\)，有：</p><div class="formula">\[
\begin{aligned}
y[n]&=f_1[n]*f_2[n]\\
&=2f_1[n+1]+5f_1[n-1]\\
&=2^{n+2}\left\{u[n+1]-u[n-2]\right\}+5\cdot2^{n-1}\left\{u[n-1]-u[n-4]\right\}.
\end{aligned}
\]</div><p>逐个离散时刻合并同一索引的样值，等价地可写为：</p><div class="formula">\[
y[n]=2\delta[n+1]+4\delta[n]+13\delta[n-1]+10\delta[n-2]+20\delta[n-3].
\]</div><h2>2014 年真题：时扩信号乘积的抽样间隔</h2><p>时间伸缩 \(x(at)\) 会把最高角频率缩放为 \(\left|a\right|\omega_m\)。因此 \(x(t/4)\) 与 \(x(t/2)\) 的最高角频率分别为 \(\omega_m/4\) 与 \(\omega_m/2\)。</p><p>时间域相乘对应频域卷积，支撑区间相加，故乘积信号的最高角频率为：</p><div class="formula">\[
\Omega_{y,\max}=\frac{\omega_m}{4}+\frac{\omega_m}{2}=\frac{3}{4}\omega_m.
\]</div><p>不混叠抽样要求 \(\Omega_s\geq2\Omega_{y,\max}=3\omega_m/2\)。由 \(\Omega_s=2\pi/T\)，最大采样时间间隔为：</p><div class="formula">\[
T_{\max}=\frac{2\pi}{3\omega_m/2}=\frac{4\pi}{3\omega_m}.
\]</div><h2>2015 年真题：采样后信号的类型</h2><p>采样把连续时间自变量限制在离散采样时刻，得到离散时间信号。采样本身不等同于量化；只有幅值也离散化后才得到数字信号。</p><h2>2015 年真题：数字信号处理的基本运算</h2><p>数字信号处理系统由基本运算单元及其连接关系构成，三种基本运算为：加法、乘法与延时（单位延时）。</p><h2>2020 年真题：组合带限信号的抽样频率</h2><p>线性组合不产生高于原分量的频率；最高频率为 \(f_2\)。</p><div class="formula">\[f_{s,\min}=2f_2\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2003 年真题：差分方程求单位样值响应</h2><p>在零状态下作 \(z\) 变换并令 \(w=z^{-1}\)，得到：</p><div class="formula">\[H(z)=\frac{z^{-1}+2z^{-2}}{1-6z^{-1}+8z^{-2}}=\frac{1}{4}-\frac{1}{1-2z^{-1}}+\frac{3}{4(1-4z^{-1})}\]</div><p>对因果系统取收敛域 \(\left|z\right|>4\)，反变换得到：</p><div class="formula">\[h[n]=\frac{1}{4}\delta[n]-2^n u[n]+\frac{3}{4}\,4^n u[n]\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2002 年真题：采样后的离散频谱与混叠</h2><p>原信号含有 \(2\pi\)、\(3\pi\)、\(5\pi\) 三个正频率分量。给定 \(\Omega_s=8\pi\)，奈奎斯特角频率为 \(4\pi\)，因此 \(5\pi\) 分量越过奈奎斯特频率并折叠到 \(-3\pi\)，产生混叠。</p>__SPECTRUM__<p>避免混叠需满足 \(\Omega_s>2\Omega_{\max}=10\pi\)，提高采样角频率后各分量即可分离。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2004 年真题：由单位阶跃响应求冲激响应</h2><p>输入为单位阶跃 \(u[n]\)，题给输出即单位阶跃响应，记为 \(s[n]\)。因果 LTI 系统满足 \(s[n]=\sum_{k=-\infty}^{n}h[k]\)，所以：</p><div class="formula">\[
\begin{aligned}
h[n]&=s[n]-s[n-1]\\
&=\delta[n]-4\left(\frac{1}{2}\right)^n u[n-1]-7\left(-\frac{3}{4}\right)^n u[n-1].
\end{aligned}
\]</div><p>上式在 \(n<0\) 时为零，故系统因果。并且：</p><div class="formula">\[
\sum_{n=-\infty}^{\infty}\left|h[n]\right|
\leq1+4\sum_{n=1}^{\infty}\left(\frac{1}{2}\right)^n
+7\sum_{n=1}^{\infty}\left(\frac{3}{4}\right)^n
=26<\infty.
\]</div><p>因此冲激响应绝对可和，系统稳定。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2007 年真题：带通信号的时域抽样</h2><p>先把乘积中的两部分分开识别。令 \(g(t)=\sin(400t)/(\pi t)\)，则其频谱为：</p><div class="formula">\[
G(j\Omega)=
\begin{cases}
1, & \left|\Omega\right|&lt;400,\\
0, & \left|\Omega\right|&gt;400.
\end{cases}
\]</div><p>乘以 \(\cos(1000\pi t)\) 会把该低通信号的频谱平移到 \(\pm1000\pi\) 附近，因此：</p><div class="formula">\[
X(j\Omega)=\frac{1}{2}\left[G\bigl(j(\Omega-1000\pi)\bigr)+G\bigl(j(\Omega+1000\pi)\bigr)\right].
\]</div><p>采样周期为 \(T\)，采样角频率为 \(\Omega_s=\frac{2\pi}{T}\)。时域冲激串采样及其频域结果分别为：</p><div class="formula">\[
\begin{aligned}
x_p(t)&=\sum_{n=-\infty}^{\infty}x(nT)\delta(t-nT),\\
X_p(j\Omega)&=\frac{1}{T}\sum_{k=-\infty}^{\infty}X\bigl(j(\Omega-k\Omega_s)\bigr).
\end{aligned}
\]</div><p>原信号的最高角频率为 \(\Omega_m=1000\pi+400\)。若还要求可用通常的低通方式无失真恢复，需使频谱副本不重叠：</p><div class="formula">\[
\Omega_s\geq2\left(1000\pi+400\right),\qquad
f_s\geq1000+\frac{400}{\pi}\ \mathrm{Hz}.
\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2007 年真题：离散系统的差分方程与冲激响应</h2><p>按图中两级延时与反馈支路，记第一级、第二级延时输出分别为 \(g_1[n]\)、\(g_2[n]\)。各节点关系为：</p><div class="formula">\[
\begin{aligned}
v_1[n]&=x[n]-0.5g_1[n], & g_1[n]&=v_1[n-1],\\
v_2[n]&=x[n]+g_1[n]+0.4g_2[n], & g_2[n]&=v_2[n-1],\\
y[n]&=x[n]+0.2g_2[n].
\end{aligned}
\]</div><p>在零状态下作 \(z\) 变换，消去内部变量可得：</p><div class="formula">\[
H(z)=\frac{Y(z)}{X(z)}=\frac{1+0.3z^{-1}+0.1z^{-2}}{1+0.1z^{-1}-0.2z^{-2}}.
\]</div><p>因此差分方程为：</p><div class="formula">\[
y[n]+0.1y[n-1]-0.2y[n-2]=x[n]+0.3x[n-1]+0.1x[n-2].
\]</div><p>将系统函数分解为：</p><div class="formula">\[
H(z)=-\frac{1}{2}+\frac{19}{18}\frac{1}{1-0.4z^{-1}}+\frac{4}{9}\frac{1}{1+0.5z^{-1}}.
\]</div><p>取因果收敛域 \(\left|z\right|>0.5\)，单位冲激响应为：</p><div class="formula">\[
h[n]= -\frac{1}{2}\delta[n]+\frac{19}{18}\left(0.4\right)^n u[n]+\frac{4}{9}\left(-0.5\right)^n u[n].
\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2007 年真题：有限长卷积的支持区间</h2><p>离散 LTI 系统的输出为 \(y[n]=x[n]*h[n]\)。卷积中只有当 \(m\) 落在 \(x[m]\) 的非零区间且 \(n-m\) 落在 \(h[n-m]\) 的非零区间时，乘积项才可能非零。</p><div class="formula">\[
\begin{aligned}
N_3&lt;m&lt;N_4,\qquad N_1&lt;n-m&lt;N_2
\end{aligned}
\]</div><p>把第二个不等式与第一个相加，得到输出可能非零的范围：</p><div class="formula">\[
N_1+N_3&lt;n&lt;N_2+N_4.
\]</div><p>因此应填 \(N_1+N_3&lt;n&lt;N_2+N_4\)。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2013 年真题：带限信号乘积的抽样间隔</h2><p>已知 \(x(t)\) 的频谱只在 \(\left|\Omega\right|\leq1500\pi\) 内可能非零。时间尺度变换 \(x(2t)\) 会将频率轴扩展两倍，因此其最高角频率为 \(3000\pi\,\mathrm{rad}/\mathrm{s}\)。</p><p>时间域相乘对应频域卷积，两个频谱支撑区间相加，所以 \(y(t)\) 的最高角频率为：</p><div class="formula">\[
\Omega_{y,\max}=1500\pi+3000\pi=4500\pi\,\mathrm{rad}/\mathrm{s}.
\]</div><p>满足奈奎斯特条件需 \(\Omega_s\geq2\Omega_{y,\max}\)，故采样周期的最大值为：</p><div class="formula">\[
T_{\max}=\frac{\pi}{\Omega_{y,\max}}=\frac{1}{4500}\,\mathrm{s}.
\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2013 年真题：离散 LTI 系统的因果性与稳定性</h2><p>系统的单位冲激响应为 \(h[n]=a^n u[n]\)。由于 \(u[n]=0\)（\(n&lt;0\)），故 \(h[n]=0\)（\(n&lt;0\)），系统对任意 \(a\) 都是因果系统。</p><p>对离散 LTI 系统，BIBO 稳定的充要条件是单位冲激响应绝对可和：</p><div class="formula">\[
\sum_{n=-\infty}^{\infty}\left|h[n]\right|
=\sum_{n=0}^{\infty}\left|a\right|^n.
\]</div><p>上式为等比级数，故稳定条件为：</p><div class="formula">\[
\sum_{n=-\infty}^{\infty}\left|h[n]\right|&lt;\infty
\Longleftrightarrow \left|a\right|&lt;1.
\]</div><p>因此：系统恒为因果；当且仅当 \(\left|a\right|&lt;1\) 时稳定。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2016 年真题：由单位阶跃响应求有限序列输出</h2><p>矩形序列 \(R_3[n]\) 在 \(n=0,1,2\) 取一、其余时刻取零，因此：</p><div class="formula">\[
R_3[n]=u[n]-u[n-3].
\]</div><p>先将输入改写为单位阶跃的线性组合：</p><div class="formula">\[
\begin{aligned}
x[n]&=(n+1)R_3[n]\\
&=u[n]+u[n-1]+u[n-2]-3u[n-3].
\end{aligned}
\]</div><p>已知 \(\mathcal{T}\{u[n]\}=g[n]\)。由线性与时不变性，各个移位阶跃的响应依次为 \(g[n]\)、\(g[n-1]\)、\(g[n-2]\)、\(g[n-3]\)，故：</p><div class="formula">\[
y[n]=g[n]+g[n-1]+g[n-2]-3g[n-3].
\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2017 年真题：系统性质判定</h2><p>分别考察三个系统。对离散系统，令输入作平移后，可比较平移输入的输出：</p><div class="formula">\[
\begin{aligned}
\mathcal{T}\{x_0(n)\}&=\sum_{m=0}^{n}x(m-n_0)\\
&=\sum_{r=-n_0}^{n-n_0}x(r).
\end{aligned}
\]</div><p>由于求和下限固定为零，平移输入的输出一般不会等于原输出的平移。因此该系统线性、因果，但不是时不变系统。</p><p>微分满足叠加性，且输入平移后的输出与原输出的平移完全一致，因此微分系统线性、时不变、因果。</p><p>最后一个系统对时间平移保持不变，且当前时刻的输出只取决于各输入在同一时刻的值，故它时不变、因果；但一般有：</p><div class="formula">\[
\max\left(a_1+b_1,a_2+b_2\right)\ne\max\left(a_1,a_2\right)+\max\left(b_1,b_2\right),
\]</div><p>所以最大值运算不满足叠加性，是非线性系统。综上：三者依次为“线性、时变、因果”，“线性、时不变、因果”，“非线性、时不变、因果”。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2019 年真题：离散系统性质判定</h2><p>系统可写成线性算子 \(\mathcal{T}\{x\}[n]=n x[n-1]+x[n-2]\)。对任意输入 \(x_1[n]\)、\(x_2[n]\) 与常数 \(a,b\)，有：</p><div class="formula">\[
\begin{aligned}
\mathcal{T}\{a x_1+b x_2\}[n]
&=n\left[a x_1[n-1]+b x_2[n-1]\right]+a x_1[n-2]+b x_2[n-2]\\
&=a\mathcal{T}\{x_1\}[n]+b\mathcal{T}\{x_2\}[n].
\end{aligned}
\]</div><p>因此系统满足叠加性，是线性系统。再令输入延迟 \(n_0\)，则：</p><div class="formula">\[
\begin{aligned}
\mathcal{T}\{x[n-n_0]\}
&=n x[n-n_0-1]+x[n-n_0-2],\\
y[n-n_0]
&=(n-n_0)x[n-n_0-1]+x[n-n_0-2].
\end{aligned}
\]</div><p>两式一般不相等，故系统为时变系统。输出 \(y[n]\) 只依赖输入的 \(n-1\) 和 \(n-2\) 时刻样值，不依赖未来输入，故系统因果。结论：该系统线性、时变、因果。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2019 年真题：\(\operatorname{Sa}(2t)\) 的冲激采样与恢复</h2><p>采用 \(\operatorname{Sa}(x)=\sin x/x\) 的定义。由时间尺度变换，原信号频谱为：</p><div class="formula">\[
F(j\omega)=
\begin{cases}
\dfrac{\pi}{2}, & \left|\omega\right|<2,\\
0, & \left|\omega\right|>2.
\end{cases}
\]</div><p>所以最高角频率为 \(\omega_m=2\,\mathrm{rad}/\mathrm{s}\)，奈奎斯特采样角频率为：</p><div class="formula">\[
\omega_{s,\mathrm{N}}=2\omega_m=4\,\mathrm{rad}/\mathrm{s}.
\]</div><p>给定 \(\omega_s=6\omega_m=12\,\mathrm{rad}/\mathrm{s}\)，于是：</p><div class="formula">\[
T_s=\frac{2\pi}{\omega_s}=\frac{\pi}{6},\qquad
f_s(t)=\sum_{n=-\infty}^{\infty}\operatorname{Sa}\left(\frac{n\pi}{3}\right)\delta\left(t-\frac{n\pi}{6}\right).
\]</div>__SAMPLING_2019_TIME__<p>冲激串采样使频谱以 \(\omega_s=12\) 为周期复制，且每个副本的带宽仍为 \(2\omega_m=4\)：</p><div class="formula">\[
F_s(j\omega)=\frac{1}{T_s}\sum_{k=-\infty}^{\infty}F\bigl(j(\omega-k\omega_s)\bigr).
\]</div>__SAMPLING_2019_SPECTRUM__<p>由于 \(\omega_s>2\omega_m\)，各频谱副本互不重叠。若采用零阶采样保持器，每个样值被保持一个采样周期；其频率响应为：</p><div class="formula">\[
H_0(j\omega)=T_s\mathrm{e}^{-j\omega T_s/2}\operatorname{Sa}\left(\frac{\omega T_s}{2}\right).
\]</div><p>保持器会在通带内引入幅度下垂和 \(T_s/2\) 的延迟，故不能只把它当作理想低通。令恢复滤波器在基带内补偿保持器并滤除其余频谱副本：</p><div class="formula">\[
H_r(j\omega)=
\begin{cases}
\dfrac{\mathrm{e}^{j\omega T_s/2}}{T_s\operatorname{Sa}\left(\dfrac{\omega T_s}{2}\right)}, & \left|\omega\right|<2,\\
0, & \left|\omega\right|>2.
\end{cases}
\]</div><p>于是基带内 \(H_r(j\omega)H_0(j\omega)=1\)，输出端可恢复原信号。若保留保持器固有的 \(T_s/2\) 延迟而不作相位超前补偿，则输出为延迟 \(T_s/2\) 的原信号；将时基相应提前即可对齐。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2016 年真题：离散序列卷积</h2><p>由题图读出非零样值：</p><div class="formula">\[
\begin{aligned}
f_1[-2]&=1,&f_1[-1]&=1,&f_1[0]&=-1,&f_1[1]&=1,&f_1[2]&=1,\\
f_2[0]&=1,&f_2[1]&=-1,&f_2[2]&=1,&f_2[3]&=-1.
\end{aligned}
\]</div><p>卷积的支撑区间为 \(-2\leq n\leq5\)。逐点按 \(f[n]=\sum_m f_1[m]f_2[n-m]\) 求和，得到：</p><div class="formula">\[
\begin{aligned}
f[-2]&=1, & f[-1]&=0, & f[0]&=-1, & f[1]&=2,\\
f[2]&=-2, & f[3]&=1, & f[4]&=0, & f[5]&=-1.
\end{aligned}
\]</div>__CONVOLUTION_2016__<p>写成冲激序列形式为：</p><div class="formula">\[
f[n]=\delta[n+2]-\delta[n]-2\delta[n-1]+2\delta[n-2]+\delta[n-3]-\delta[n-5].
\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2005 年真题：由阶跃响应反求二阶差分方程</h2><p>为避免与本问的输出记号混淆，记给定的单位阶跃响应为 \(s[n]\)。单位阶跃的 \(z\) 变换为 \(U(z)=1/(1-z^{-1})\)，因此系统函数为：</p><div class="formula">\[
\begin{aligned}
S(z)&=\frac{1}{1-2z^{-1}}+\frac{3}{1-5z^{-1}}+\frac{10}{1-z^{-1}},\\
H(z)&=\left(1-z^{-1}\right)S(z)\\
&=\frac{14-85z^{-1}+111z^{-2}}{1-7z^{-1}+10z^{-2}}.
\end{aligned}
\]</div><p>两边同乘分母并作反变换，得到所求二阶常系数线性差分方程：</p><div class="formula">\[
y[n]-7y[n-1]+10y[n-2]
=14f[n]-85f[n-1]+111f[n-2].
\]</div><p>第二问中 \(f[n]=3u[n]+3u[n-7]\)。利用线性与时不变性，输出等于两项阶跃响应的加权和：</p><div class="formula">\[
\begin{aligned}
y[n]&=3s[n]+3s[n-7]\\
&=3\left[2^n+3\left(5\right)^n+10\right]u[n]\\
&\quad+3\left[2^{n-7}+3\left(5\right)^{n-7}+10\right]u[n-7].
\end{aligned}
\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2003 年真题：冲激采样后的低通重建</h2><p>采样信号为 \(f_p(t)=\sum_{n=-\infty}^{\infty}f(nT)\delta(t-nT)\)。理想低通重建输出为：</p><div class="formula">\[f_0(t)=\sum_{n=-\infty}^{\infty}f(nT)\,\operatorname{Sa}\left(\frac{t-nT}{T}\right)\]</div><p>令 \(t=mT\)。当 \(n\ne m\) 时，\(m-n\) 为非零整数，重建核为零；当 \(n=m\) 时重建核为一，因此：</p><div class="formula">\[f_0(mT)=f(mT)\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2021 年真题：离散序列卷积</h2><p>由题图可读出四个非零样值分别为：</p><div class="formula">\[
f_1[-2]=f_1[-1]=f_1[1]=f_1[2]=1,
\]
\[
f_2[-1]=1,\qquad f_2[1]=-1,\qquad f_2[2]=2,\qquad f_2[3]=-1.
\]</div><p>按离散卷积定义 \(f[n]=\sum_{k=-\infty}^{\infty}f_1[k]f_2[n-k]\) 逐点求和。其非零支撑范围为 \(-3\leq n\leq5\)，各点结果为：</p><div class="formula">\[
\begin{aligned}
f[-3]&=1,& f[-2]&=1,& f[-1]&=-1,\\
f[0]&=1,& f[1]&=1,& f[2]&=-2,\\
f[3]&=1,& f[4]&=1,& f[5]&=-1.
\end{aligned}
\]</div>__CONVOLUTION_2021__<p>例如 \(n=2\) 时，只有 \(k=-1,1\) 两项非零：</p><div class="formula">\[
f[2]=f_1[-1]f_2[3]+f_1[1]f_2[1]=-1-1=-2.
\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2022 年真题：周期理想采样的拉普拉斯变换</h2><p>周期为 \(T\) 的理想冲激串为 \(\delta_T(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT)\)。采样后信号为：</p><div class="formula">\[
\begin{aligned}
f_s(t)&=f(t)\delta_T(t)\\
&=\sum_{n=-\infty}^{\infty}f(nT)\delta(t-nT)\\
&=\sum_{n=0}^{\infty}\mathrm{e}^{-5nT}\delta(t-nT).
\end{aligned}
\]</div><p>对每个冲激项作拉普拉斯变换，并将结果写成等比级数：</p><div class="formula">\[
\begin{aligned}
F_s(s)&=\sum_{n=0}^{\infty}\mathrm{e}^{-5nT}\mathrm{e}^{-snT}\\
&=\sum_{n=0}^{\infty}\left[\mathrm{e}^{-(s+5)T}\right]^n\\
&=\frac{1}{1-\mathrm{e}^{-(s+5)T}}.
\end{aligned}
\]</div><p>级数收敛条件为 \(\left|\mathrm{e}^{-(s+5)T}\right|&lt;1\)，故收敛域为 \(\operatorname{Re}\{s\}&gt;-5\)。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2022 年真题：连续信号采样与采样频谱</h2><p>信号最高角频率为 \(\omega_m=4\omega_0\)，故无失真采样条件为：</p><div class="formula">\[
\omega_s\geq2\omega_m=8\omega_0.
\]</div><p>原信号频谱为：</p><div class="formula">\[
X(j\Omega)=4\pi\delta(\Omega)+\pi\sum_{k=1}^{4}\left[\delta(\Omega-k\omega_0)+\delta(\Omega+k\omega_0)\right].
\]</div><p>周期理想采样满足：</p><div class="formula">\[
X_s(j\Omega)=\frac{1}{T}\sum_{m=-\infty}^{\infty}X\left(j\left(\Omega-m\Omega_s\right)\right),\qquad\Omega_s=\frac{2\pi}{T}.
\]</div><p>（2）\(T=1.2\,\mathrm{s}\) 时，\(\Omega_s=5\pi/3\)，于是：</p><div class="formula">\[
X_s(j\Omega)=\frac{1}{1.2}\sum_{m=-\infty}^{\infty}X\left(j\left(\Omega-\frac{5m\pi}{3}\right)\right).
\]</div><p>因 \(5\pi/3&lt;2\pi\)，频谱副本发生混叠。</p><p>（3）\(T=0.5\,\mathrm{s}\) 时，\(\Omega_s=4\pi\)，于是：</p><div class="formula">\[
X_s(j\Omega)=2\sum_{m=-\infty}^{\infty}X\left(j\left(\Omega-4m\pi\right)\right).
\]</div><p>此时 \(4\pi&gt;2\pi\)，频谱副本不发生混叠。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2016 年真题：有限序列的偶、奇分解</h2><p>偶分量和奇分量由定义直接给出：</p><div class="formula">\[
\begin{aligned}
x_e[n]&=\frac{1}{2}\left(x[n]+x[-n]\right)=\frac{1}{2}\left(R_6[n]+R_6[-n]\right),\\
x_o[n]&=\frac{1}{2}\left(x[n]-x[-n]\right)=\frac{1}{2}\left(R_6[n]-R_6[-n]\right).
\end{aligned}
\]</div><p>因此第（1）问的结果为上述 \(x_e[n]\)。对第（2）问，\(R_8[n]\) 只保留 \(0\leq n\leq7\) 的部分；在该区间内，奇分量仅于 \(1\leq n\leq5\) 取 \(1/2\)。故：</p><div class="formula">\[
x_o[n]R_8[n]=\begin{cases}
\dfrac{1}{2}, & 1\leq n\leq5,\\
0, & \text{其他 }n.
\end{cases}
\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2021 年真题：抽样频谱与低通恢复</h2><p>先用积化和差公式分解输入信号：</p><div class="formula">\[
\begin{aligned}
x(t)&=5\cos(220\pi t)+5\cos(180\pi t),\\
X(j\Omega)&=5\pi\sum_{\sigma\in\{-1,1\}}\left[\delta\left(\Omega-\sigma220\pi\right)+\delta\left(\Omega-\sigma180\pi\right)\right].
\end{aligned}
\]</div><p>抽样频率为 \(f_s=250\,\mathrm{Hz}\)，故 \(T_s=1/250\)、\(\Omega_s=500\pi\)。理想冲激抽样后的频谱为：</p><div class="formula">\[
X_s(j\Omega)=1250\pi\sum_{m=-\infty}^{\infty}\sum_{\sigma\in\{-1,1\}}\left[\delta\left(\Omega-500m\pi-\sigma220\pi\right)+\delta\left(\Omega-500m\pi-\sigma180\pi\right)\right].
\]</div><p>原频谱最大角频率为 \(220\pi\)。最近的相邻副本从 \(500\pi-220\pi=280\pi\) 开始，因此恢复低通滤波器的截止频率应满足：</p><div class="formula">\[
220\pi\leq\Omega_c\leq280\pi.
\]</div><p>为补偿抽样带来的 \(1/T_s\) 幅度系数，通带增益取 \(T_s\)。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2022 年真题：A/D、数字低通与 D/A 串联</h2><p>图中输入频谱为以原点为峰、支撑区间为 \([-1,1],\mathrm{kHz}\) 的三角谱，即：</p><div class="formula">\[
X(jf)=
\begin{cases}
1-\left|f\right|/(1\,\mathrm{kHz}), & \left|f\right|\leq1\,\mathrm{kHz},\\
0, & \text{其他 }f.
\end{cases}
\]</div><p>数字低通的截止频率是归一化角频率 \(\omega_c=\pi/4\)。若采样频率为 \(f_s=1/T\)，它对应的模拟频率截止点为：</p><div class="formula">\[
f_c=\frac{\omega_c}{2\pi}f_s=\frac{f_s}{8}.
\]</div><p>（1）\(T=0.05\,\mathrm{ms}\) 时，\(f_s=20\,\mathrm{kHz}\)，奈奎斯特频率为 \(10\,\mathrm{kHz}\)，输入带宽远小于该值，采样不混叠；且 \(f_c=2.5\,\mathrm{kHz}\)，完整通过原频谱。D/A 输出为：</p><div class="formula">\[
Y_a(jf)=
\begin{cases}
1-\left|f\right|/(1\,\mathrm{kHz}), & \left|f\right|\leq1\,\mathrm{kHz},\\
0, & \text{其他 }f.
\end{cases}
\]</div>__AD_DA_FAST__<p>（2）\(T=0.25\,\mathrm{ms}\) 时，\(f_s=4\,\mathrm{kHz}\)，奈奎斯特频率为 \(2\,\mathrm{kHz}\)，采样同样不混叠；但此时 \(f_c=0.5\,\mathrm{kHz}\)，数字低通只留下三角谱的中心部分。因此：</p><div class="formula">\[
Y_a(jf)=
\begin{cases}
1-\left|f\right|/(1\,\mathrm{kHz}), & \left|f\right|\leq0.5\,\mathrm{kHz},\\
0, & \text{其他 }f.
\end{cases}
\]</div>__AD_DA_SLOW__<p>两种情形的区别来自同一个数字截止频率映射到不同的模拟频率；并非由采样混叠引起。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2023 年真题：由单位阶跃响应求单位脉冲响应</h2><p>题给 \(x[n]\) 是以 \(1/2\) 为比值的右边等比序列，因此它的 Z 变换为：</p><div class="formula">\[
X(z)=\sum_{n=0}^{\infty}\left(\frac{1}{2}\right)^n z^{-n}=\frac{1}{1-\frac{1}{2}z^{-1}}.
\]</div><p>对零状态 LTI 系统，\(G(z)=H(z)X(z)\)。故系统函数及其时域响应为：</p><div class="formula">\[
\begin{aligned}
H(z)&=\frac{G(z)}{X(z)}=\left(1-\frac{1}{2}z^{-1}\right)G(z),\\
h[n]&=g[n]-\frac{1}{2}g[n-1].
\end{aligned}
\]</div><p>即：对已知单位阶跃响应 \(g[n]\) 取后向差分，再减去其一半延时项，便得到单位脉冲响应。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2023 年真题：正弦采样序列的 DTFT</h2><p>理想采样后，离散时间角频率为 \(\omega_0=2\pi\cdot50/f_s\)，并有 \(x[n]=\cos(\omega_0n)\)。DTFT 的基本对为：</p><div class="formula">\[
\cos(\omega_0n)\longleftrightarrow\pi\sum_{k=-\infty}^{\infty}\left[\delta\left(\omega-\omega_0-2k\pi\right)+\delta\left(\omega+\omega_0-2k\pi\right)\right].
\]</div><p>（1）\(f_s=100\,\mathrm{Hz}\) 时，\(\omega_0=\pi\)。两组冲激在 \(\omega=\pi\) 重合，幅值相加：</p><div class="formula">\[
X\left(\mathrm{e}^{j\omega}\right)=2\pi\sum_{k=-\infty}^{\infty}\delta\left(\omega-\pi-2k\pi\right).
\]</div>__DTFT_2023_100__<p>（2）\(f_s=150\,\mathrm{Hz}\) 时，\(\omega_0=2\pi/3\)。在 \([0,2\pi]\) 内出现两根幅值均为 \(\pi\) 的谱线，位置为 \(2\pi/3\) 与 \(4\pi/3\)：</p><div class="formula">\[
X\left(\mathrm{e}^{j\omega}\right)=\pi\sum_{k=-\infty}^{\infty}\left[\delta\left(\omega-\frac{2\pi}{3}-2k\pi\right)+\delta\left(\omega+\frac{2\pi}{3}-2k\pi\right)\right].
\]</div>__DTFT_2023_150__</section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2023 年真题：正弦信号的采样频率与周期</h2><p>正弦信号的最高普通频率和最高角频率分别为：</p><div class="formula">\[
f_m=\frac{\omega_0}{2\pi},\qquad \Omega_m=\omega_0.
\]</div><p>采样定理可用普通频率或角频率表达；两种写法必须使用同一单位：</p><div class="formula">\[
\begin{aligned}
f_s&\geq2f_m=\frac{\omega_0}{\pi},\\
\Omega_s&\geq2\Omega_m=2\omega_0.
\end{aligned}
\]</div><p>因而可选择任何 \(f_s\geq\omega_0/\pi\) 的采样频率；相应采样周期须满足：</p><div class="formula">\[
T_s=\frac{1}{f_s}\leq\frac{\pi}{\omega_0}.
\]</div><p>实际系统通常在临界值之外留出余量，以减小实际滤波器过渡带造成的风险。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2024 年真题：矩形脉冲的采样与 DTFT</h2><p>题给采样角频率为 \(\Omega_s=2\pi\,\mathrm{rad}\,\mathrm{s}^{-1}\)，故采样周期为：</p><div class="formula">\[
T_s=\frac{2\pi}{\Omega_s}=1\,\mathrm{s}.
\]</div><p>图中的矩形脉冲在 \(-2\leq t\leq2\) 内取值为 \(1\)。因此采样后得到有限长离散序列：</p><div class="formula">\[
x[n]=\begin{cases}
1, & -2\leq n\leq2,\\
0, & \text{其他 }n.
\end{cases}
\]</div><p>该矩形脉冲不是带限信号；其连续时间频谱延伸到无穷高频。给定的有限采样角频率不能使频谱副本完全分离，因此不能由这些样本无失真恢复原连续时间信号。</p><p>离散序列的 DTFT 直接由五个非零样本求和：</p><div class="formula">\[
\begin{aligned}
X\left(\mathrm{e}^{j\omega}\right)
&=\sum_{n=-2}^{2}\mathrm{e}^{-j\omega n}\\
&=\mathrm{e}^{2j\omega}+\mathrm{e}^{j\omega}+1+\mathrm{e}^{-j\omega}+\mathrm{e}^{-2j\omega}\\
&=1+2\cos\omega+2\cos(2\omega)\\
&=\frac{\sin\left(5\omega/2\right)}{\sin\left(\omega/2\right)}.
\end{aligned}
\]</div><p>最后一式在 \(\omega=2k\pi\) 处按极限取值为 \(5\)，并且该 DTFT 以 \(2\pi\) 为周期。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2024 年真题：非理想脉冲采样与恢复</h2><p>采用普通频率 \(f\) 表示频谱。令 \(\operatorname{Sa}(x)=\sin(\pi x)/(\pi x)\)，则题给信号的频谱为：</p><div class="formula">\[
F(f)=\begin{cases}
1, & \left|f\right|\leq5\,\mathrm{kHz},\\
0, & \left|f\right|>5\,\mathrm{kHz}.
\end{cases}
\]</div>__PULSE_2024_BASEBAND__<p>因此按最高频率计的单边带宽为 \(B=5\,\mathrm{kHz}\)；双边频谱的总占用宽度为 \(10\,\mathrm{kHz}\)。</p><p>矩形脉冲串的周期、脉冲宽度与占空比为：</p><div class="formula">\[
f_s=\frac{1}{T_s}=25\,\mathrm{kHz},\qquad \tau=10\,\mu\mathrm{s},\qquad \frac{\tau}{T_s}=\frac14.
\]</div><p>以脉冲中心为零时，采样序列的傅里叶级数系数为：</p><div class="formula">\[
C_k=\frac{\tau}{T_s}\operatorname{Sa}\left(\frac{k\tau}{T_s}\right)=\frac{1}{4}\operatorname{Sa}\left(\frac{k}{4}\right).
\]</div><p>时间相乘对应频域卷积，故采样信号频谱为：</p><div class="formula">\[
F_s(f)=\sum_{k=-\infty}^{\infty}C_kF\left(f-kf_s\right).
\]</div>__PULSE_2024_SAMPLED__<p>图中只画出了 \(k=-1,0,1\) 的副本；所有副本的中心间隔为 \(25\,\mathrm{kHz}\)，每个副本的带宽仍为 \(5\,\mathrm{kHz}\)。</p><p>给定的 \(H_1(f)\) 恰好只通过 \(k=\pm1\) 的两份副本，因此其输出频谱为：</p><div class="formula">\[
Y_1(f)=C_1\left[F\left(f-f_s\right)+F\left(f+f_s\right)\right],\qquad C_1=\frac14\operatorname{Sa}\left(\frac14\right).
\]</div><p>在 \(H_1(f)\) 后串接“与 \(2\cos(2\pi f_st)\) 相乘 \(\to\) 截止频率为 \(5\,\mathrm{kHz}\) 的理想低通 \(\to\) 增益”即可完成恢复。调制后的低频项为 \(2C_1F(f)\)，故低通通带内取：</p><div class="formula">\[
G=\frac{1}{2C_1}=\frac{2}{\operatorname{Sa}(1/4)}.
\]</div><p>该级联会滤除搬移到 \(\pm2f_s\) 附近的高频项，最终输出频谱为 \(F(f)\)，从而输出为 \(f(t)\)。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2025 年真题：离散系统可逆性</h2><p>该系统可看作以 \(h[n]=a^n\) 为核的线性卷积算子。检验可逆性时，只要找到一个非零输入也映射为零输出，即可说明系统不是一一对应的。</p><p>取非零序列：</p><div class="formula">\[
x_0[n]=\delta[n]-a\delta[n-1].
\]</div><p>代入题给系统，利用冲激序列的抽样性质可得：</p><div class="formula">\[
\begin{aligned}
\mathcal{T}\{x_0\}[n]
&=\sum_{i=-\infty}^{\infty}a^{n-i}\left(\delta[i]-a\delta[i-1]\right)\\
&=a^n-a\cdot a^{n-1}=0.
\end{aligned}
\]</div><p>零输入同样输出零，而 \(x_0[n]\ne0\) 也输出零，因此不同输入对应同一输出。该系统不可逆，故不存在逆系统。</p></section>
</main>""".replace("__SPECTRUM__", spectrum).replace("__CONVOLUTION_2016__", convolution_2016_svg("output")).replace("__CONVOLUTION_2021__", convolution_2021_svg("output")).replace("__SAMPLING_2019_TIME__", sampling_time).replace("__SAMPLING_2019_SPECTRUM__", sampling_spectrum).replace("__AD_DA_FAST__", ad_da_output_spectrum_svg(1.0)).replace("__AD_DA_SLOW__", ad_da_output_spectrum_svg(0.5)).replace("__DTFT_2023_100__", dtft_sampling_2023_svg(100)).replace("__DTFT_2023_150__", dtft_sampling_2023_svg(150)).replace("__PULSE_2024_BASEBAND__", pulse_spectrum_2024_svg("baseband")).replace("__PULSE_2024_SAMPLED__", pulse_spectrum_2024_svg("sampled"))
    output.write_text(_document(content), encoding="utf-8")
    return output


def _render(writer, output: Path) -> Path:
    html = writer(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


def render_questions_pdf(output: Path) -> Path:
    return _render(write_questions_html, output)


def render_answers_pdf(output: Path) -> Path:
    return _render(write_answers_html, output)


if __name__ == "__main__":
    print(render_questions_pdf(ROOT / "full/outputs/chapter_01_supplemental_mathjax_component.pdf"))
    print(render_answers_pdf(ROOT / "full/outputs/chapter_01_supplemental_answers_mathjax_component.pdf"))
