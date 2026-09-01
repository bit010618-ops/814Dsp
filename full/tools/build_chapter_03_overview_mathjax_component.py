"""Chapter-three conceptual bridge from FS and FT to DTFT and DFS."""
from __future__ import annotations

import math
from pathlib import Path

from full.tools.normalize_mathjax_inline import normalize_legacy_inline_math
from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.mapping{border-collapse:collapse;width:100%;margin:10pt 0 12pt}.mapping th,.mapping td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:left}.mapping th{color:#315d7c;font-weight:500;background:#f4f7f8}.fourier-family-map{break-inside:avoid;margin:12pt 0 13pt}.fourier-family-map svg{display:block;width:100%;height:auto;border:1px solid #d6dde2;border-radius:5pt;background:#fff}.fourier-family-map figcaption{margin-top:4pt;color:#52616d;text-align:center;font-size:9.5pt}@media(max-width:560px){body{font-size:10.5pt}.mapping{font-size:9.5pt}.formula{padding:7pt 8pt}}
</style>"""


def fourier_family_map_svg() -> str:
    """Return an editable redraw of the unique five-stage map on source page 527."""
    axis = 'fill="none" stroke="#174b73" stroke-width="1.8" stroke-linecap="round"'
    signal = 'fill="none" stroke="#0d8794" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
    stem = 'stroke="#0d8794" stroke-width="2" stroke-linecap="round"'
    dot = 'fill="#c77613" stroke="#c77613"'
    label_style = 'height:100%;display:flex;align-items:center;justify-content:center;color:#172b3a;font-size:13px'

    def math(x: int, y: int, width: int, expression: str) -> str:
        return (
            f'<foreignObject x="{x}" y="{y}" width="{width}" height="27">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" style="{label_style}">\\({expression}\\)</div>'
            '</foreignObject>'
        )

    rows: list[str] = []
    tops = [50, 143, 236, 329, 422]
    left_labels = [r"x_a(t)", r"x(n)", r"x(n)w(n)", r"\widetilde{x}_N(n)", r"x_N(n)"]
    right_labels = [r"X_a(j\Omega)", r"X(e^{j\omega})", r"X_w(e^{j\omega})", r"\widetilde{X}_N(k)", r"X_N(k)"]
    transforms = ["FT", "DTFT", "DTFT", "DFS", "DFT"]
    for top, left, right, transform in zip(tops, left_labels, right_labels, transforms):
        baseline = top + 55
        rows.extend((
            f'<line x1="48" y1="{baseline}" x2="332" y2="{baseline}" {axis} marker-end="url(#ch3-family-arrow)"/>',
            f'<line x1="190" y1="{top+12}" x2="190" y2="{baseline+12}" {axis}/>',
            f'<line x1="643" y1="{baseline}" x2="930" y2="{baseline}" {axis} marker-end="url(#ch3-family-arrow)"/>',
            f'<line x1="785" y1="{top+12}" x2="785" y2="{baseline+12}" {axis}/>',
            f'<line x1="392" y1="{baseline}" x2="574" y2="{baseline}" {axis} marker-end="url(#ch3-family-arrow)"/>',
            f'<text x="476" y="{baseline-9}" text-anchor="middle" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="13">{transform}</text>',
            math(55, top + 3, 112, left),
            math(805, top + 3, 120, right),
        ))

    def stems(points: list[tuple[int, int]], baseline: int) -> str:
        return ''.join(
            f'<line x1="{x}" y1="{baseline}" x2="{x}" y2="{y}" {stem}/>'
            f'<circle cx="{x}" cy="{y}" r="3" {dot}/>'
            for x, y in points
        )

    rows.extend((
        f'<path d="M60 105 C95 104,105 66,132 69 S170 101,190 105 S232 104,272 104 S305 104,325 104" {signal}/>',
        f'<path d="M652 105 C678 104,690 72,719 70 S753 99,785 105 S824 104,861 104 S905 104,923 104" {signal}/>',
        stems([(114,181), (151,166), (190,176), (229,157), (266,183)], 198),
        stems([(678,182), (716,166), (754,178), (785,157), (824,178), (861,166), (900,182)], 198),
        '<rect x="115" y="251" width="151" height="73" fill="none" stroke="#b56b2e" stroke-width="1.4" stroke-dasharray="4 4"/>',
        stems([(132,280), (166,262), (199,270), (232,255), (260,284)], 291),
        f'<path d="M653 291 C686 291,693 257,722 257 S755 288,785 291 S820 291,850 291 S883 257,910 257" {signal}/>',
        '<line x1="112" y1="344" x2="112" y2="402" stroke="#b56b2e" stroke-width="1.2" stroke-dasharray="3 3"/>',
        '<line x1="269" y1="344" x2="269" y2="402" stroke="#b56b2e" stroke-width="1.2" stroke-dasharray="3 3"/>',
        stems([(125,371), (155,356), (190,366), (225,350), (255,374)], 384),
        stems([(678,371), (716,356), (754,366), (785,350), (824,366), (861,356), (900,371)], 384),
        '<line x1="112" y1="477" x2="112" y2="495" stroke="#b56b2e" stroke-width="1.2"/>',
        '<line x1="269" y1="477" x2="269" y2="495" stroke="#b56b2e" stroke-width="1.2"/>',
        stems([(120,462), (150,448), (190,457), (230,442), (260,466)], 477),
        stems([(690,462), (730,450), (770,442), (812,457), (852,448), (892,466)], 477),
        '<text x="53" y="27" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="14">时域描述</text>',
        '<text x="676" y="27" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="14">频域描述</text>',
        math(274, 104, 35, "t"), math(873, 104, 44, "\\Omega"),
        math(274, 197, 35, "n"), math(873, 197, 42, "\\omega"),
        math(274, 290, 35, "n"), math(873, 290, 42, "\\omega"),
        math(274, 383, 35, "n"), math(873, 383, 35, "k"),
        math(274, 476, 35, "n"), math(873, 476, 35, "k"),
    ))
    return f'''<figure class="fourier-family-map" id="fourier-family-map">
<svg viewBox="0 0 980 515" role="img" aria-labelledby="fourier-family-map-title">
<title id="fourier-family-map-title">连续、离散、截断与周期延拓的频谱对应关系</title>
<defs><marker id="ch3-family-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#174b73"/></marker></defs>
{''.join(rows)}
</svg>
<figcaption>图 3-1　连续、离散、截断与周期延拓的频谱对应关系</figcaption>
</figure>'''


def fourier_series_partial_sum_svg() -> str:
    """Render calculated rectangular-pulse Fourier partial sums from their coefficients."""

    width, height = 980, 360
    panels = ((42, 4.0, 11), (515, 8.0, 21))

    def partial_sum(t: float, period: float, terms: int) -> float:
        omega0 = 2.0 * math.pi / period
        pulse_width = 2.0
        value = pulse_width / period
        for k in range(1, terms + 1):
            argument = k * omega0 * pulse_width / 2.0
            coefficient = pulse_width / period * math.sin(argument) / argument
            value += 2.0 * coefficient * math.cos(k * omega0 * t)
        return value

    def path_for(values: list[tuple[float, float]], x0: int, x1: int, y0: int, y1: int) -> str:
        x_min, x_max, y_min, y_max = -8.0, 8.0, -0.35, 1.35
        coords = []
        for x, y in values:
            px = x0 + (x - x_min) / (x_max - x_min) * (x1 - x0)
            py = y1 - (y - y_min) / (y_max - y_min) * (y1 - y0)
            coords.append(f"{px:.2f},{py:.2f}")
        return "M" + " L".join(coords)

    fragments: list[str] = []
    for index, (left, period, terms) in enumerate(panels):
        x0, x1, y0, y1 = left + 24, left + 421, 82, 286
        x_axis = y1 - (0.0 + 0.35) / 1.7 * (y1 - y0)
        y_axis = x0 + 0.5 * (x1 - x0)
        samples = [(-8.0 + 16.0 * i / 800.0, partial_sum(-8.0 + 16.0 * i / 800.0, period, terms)) for i in range(801)]
        exact = [(-8.0 + 16.0 * i / 800.0, 1.0 if abs(((-8.0 + 16.0 * i / 800.0 + period / 2.0) % period) - period / 2.0) <= 1.0 else 0.0) for i in range(801)]
        fragments.extend((
            f'<rect x="{left}" y="36" width="445" height="282" rx="8" fill="#ffffff" stroke="#d6dde2"/>',
            f'<line x1="{x0}" y1="{x_axis:.2f}" x2="{x1}" y2="{x_axis:.2f}" fill="none" stroke="#174b73" stroke-width="1.7" marker-end="url(#ch3-fs-arrow)"/>',
            f'<line x1="{y_axis:.2f}" y1="{y1}" x2="{y_axis:.2f}" y2="{y0}" fill="none" stroke="#174b73" stroke-width="1.7" marker-end="url(#ch3-fs-arrow)"/>',
            f'<path d="{path_for(exact, x0, x1, y0, y1)}" fill="none" stroke="#7e8d99" stroke-width="1.5" stroke-dasharray="5 4"/>',
            f'<path d="{path_for(samples, x0, x1, y0, y1)}" fill="none" stroke="#0d8794" stroke-width="2.2" stroke-linejoin="round"/>',
            f'<text x="{left+222}" y="61" text-anchor="middle" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="14">矩形脉冲列的有限谐波逼近</text>',
            f'<text x="{left+222}" y="307" text-anchor="middle" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="12">周期 T₀ = {period:g}，保留 {terms} 个正谐波</text>',
            f'<foreignObject x="{x1-8}" y="{x_axis+6:.2f}" width="30" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px">\\(t\\)</div></foreignObject>',
            f'<foreignObject x="{y_axis+7:.2f}" y="{y0-4}" width="38" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px">\\(x(t)\\)</div></foreignObject>',
        ))
        if index == 0:
            fragments.append(f'<text x="{left+58}" y="73" fill="#7e8d99" font-family="Microsoft YaHei, sans-serif" font-size="11">虚线：原矩形脉冲列</text>')
    return f'''<figure class="fourier-family-map" data-plot="fourier-series-partial-sums">
<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="fourier-series-partial-sums-title">
<title id="fourier-series-partial-sums-title">有限谐波数逼近的实际效果</title>
<defs><marker id="ch3-fs-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#174b73"/></marker></defs>
{''.join(fragments)}
</svg>
<figcaption>图 3-2　有限谐波数逼近的实际效果：实线由傅里叶级数系数直接计算，虚线为原矩形脉冲列。</figcaption>
</figure>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>第三章 离散傅里叶变换</h1>
<p>傅里叶分析的核心是把信号放在适合观察或计算的频域中描述。本章把前面已经见过的傅里叶级数、傅里叶变换和序列傅里叶变换连接起来，再建立离散傅里叶级数与离散傅里叶变换的计算框架。</p>

<h2>四类傅里叶描述的坐标关系</h2>
<table class="mapping"><thead><tr><th>时域</th><th>频域</th><th>对应工具</th></tr></thead><tbody>
<tr><td>连续时间</td><td>连续频率</td><td>傅里叶变换 FT</td></tr>
<tr><td>连续时间</td><td>离散频率</td><td>傅里叶级数 FS</td></tr>
<tr><td>离散时间</td><td>连续频率</td><td>序列傅里叶变换 DTFT</td></tr>
<tr><td>离散时间</td><td>离散频率</td><td>离散傅里叶级数 DFS</td></tr>
</tbody></table>
<p>时域周期性会导致频域离散性；频域周期性会导致时域离散性。DFS 恰好位于“离散时间、离散频率”的一格，因此它在两个域内都带有周期结构。</p>

""" + fourier_family_map_svg() + r"""
<p>上图按“连续、离散、截断、周期延拓与有限主值区间”展示实际频谱分析的链条：连续信号经采样形成序列；有限记录相当于乘窗，会在频域引入展宽；把有限主值区间周期延拓后得到 DFS 的双周期描述；DFT 则只保留一个长度为 [[N]] 的主值区间用于计算。该图用于区分采样、截断和周期延拓各自造成的频域变化。</p>

<h2>从傅里叶级数到傅里叶变换</h2>
<p>对周期为 [[T_0]] 的连续时间信号，基本角频率为 [[\Omega_0=2\pi/T_0]]。其频谱只出现在谐波频点 [[k\Omega_0]] 上，频点间隔由 [[T_0]] 决定：</p>
<div class="formula">\[
T_0\uparrow\quad\Longrightarrow\quad\Omega_0=\frac{2\pi}{T_0}\downarrow.
\]</div>
<p>当 (T_0) 无限增大时，频谱取样间隔趋于零，离散的傅里叶级数频谱过渡为连续的傅里叶变换频谱。同一序号 [[k]] 的系数数值可相同，但在不同记录周期下，物理频率仍由 [[k\Omega_0]] 给出；不能只比较系数数值而忽略频率坐标。</p>

<h3>连续时间傅里叶级数变换对</h3>
<p>以下变换对用于从一个周期内的连续时间波形计算各次谐波系数，并以直流项和所有正、负谐波重新构造原周期信号：</p>
<div class="formula">\[
\widetilde{x}(t)=\sum_{k=-\infty}^{\infty}X(jk\Omega_0)e^{jk\Omega_0t},\qquad
X(jk\Omega_0)=\frac{1}{T_0}\int_{-T_0/2}^{T_0/2}\widetilde{x}(t)e^{-jk\Omega_0t}\,\mathrm{d}t.
\]</div>

<h3>矩形脉冲列的谐波系数</h3>
<p>对幅度为 1、宽度为 [[\tau]]、周期为 [[T_0]] 的实偶矩形脉冲列，下式给出每一个谐波频点的傅里叶级数系数；它说明脉冲宽度与周期之比决定直流分量和谱线包络：</p>
<div class="formula">\[
X(jk\Omega_0)=\frac{1}{T_0}\int_{-\tau/2}^{\tau/2}e^{-jk\Omega_0t}\,\mathrm{d}t
=\frac{\tau}{T_0}\operatorname{Sa}\left(\frac{k\Omega_0\tau}{2}\right),
\qquad \operatorname{Sa}(u)=\frac{\sin u}{u}.
\]</div>
<p>对于实偶的周期信号，负、正谐波系数相等且为实数，因此级数可合并成直流项与余弦谐波项。该式直接说明频域各离散谱线如何重构时域波形：</p>
<div class="formula">\[
\widetilde{x}(t)=X(j0)+\sum_{k=1}^{\infty}2X(jk\Omega_0)\cos(k\Omega_0t).
\]</div>
<p>有限谐波和用于近似实际波形。增加保留的谐波数会改善跳变附近以外的逼近，但在跳变点附近仍会出现局部振铃；下图的曲线由上述系数逐项相加得到。</p>
""" + fourier_series_partial_sum_svg() + r"""

<h2>从连续时间频谱到 DTFT</h2>
<p>连续信号以采样间隔 [[T]] 变为序列后，模拟角频率 [[\Omega]] 与数字角频率 [[\omega]] 的关系为：</p>
<div class="formula">\[
\omega=\Omega T,\qquad \Omega=\frac{\omega}{T}.
\]</div>
<p>采样会使离散时间序列的频谱以 [[2\pi]] 为周期重复。若原模拟频谱在折叠频率以内，[[X(e^{j\omega})]] 可理解为 [[X(j\Omega)]] 在数字频率轴上的周期延拓，并带有与采样间隔相关的幅度缩放。减小 [[T]] 会提高采样频率、扩大可无混叠观察的频率范围。</p>

<h2>本章的计算视角</h2>
<p>频域把时域卷积化为乘积，因此常将复杂的时域计算转换到频域完成，再经反变换回到时域。离散形式允许使用有限个样本和快速算法完成计算；但使用任何有限点变换前，必须区分清楚线性卷积、循环卷积、记录长度与频率取样间隔。</p>
</main>
"""
    content = normalize_legacy_inline_math(
        content.replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    )
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
