"""Chapter-three §3.5 analog-signal spectrum analysis with DFT."""
from __future__ import annotations

import math
from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}</style>"""


def analog_dft_spectrum_chain_svg() -> str:
    """Render the actual analog-to-DFT spectrum-analysis chain."""
    return '''<figure data-diagram="analog-dft-spectrum-chain" style="break-inside:avoid;margin:12pt 0 13pt"><svg viewBox="0 0 980 180" role="img" aria-labelledby="analog-dft-spectrum-chain-title" style="display:block;width:100%;height:auto;border:1px solid #d6dde2;border-radius:5pt;background:#fff"><title id="analog-dft-spectrum-chain-title">模拟信号经采样、截断和 DFT 的频谱分析流程</title><defs><marker id="analog-dft-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#174b73"/></marker></defs><text x="35" y="35" fill="#174b73" font-family="Microsoft YaHei, sans-serif" font-size="18" font-weight="700">模拟信号的 DFT 频谱分析链路</text><rect x="55" y="72" width="150" height="55" rx="6" fill="#f4f7f8" stroke="#0d8794" stroke-width="1.5"/><rect x="300" y="72" width="150" height="55" rx="6" fill="#f4f7f8" stroke="#0d8794" stroke-width="1.5"/><rect x="545" y="72" width="150" height="55" rx="6" fill="#fff8e8" stroke="#b56b2e" stroke-width="1.5"/><rect x="790" y="72" width="150" height="55" rx="6" fill="#eef7f1" stroke="#16866d" stroke-width="1.5"/><text x="130" y="105" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="17">模拟信号 xₐ(t)</text><text x="375" y="105" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="17">采样序列 x(n)</text><text x="620" y="105" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="17">有限记录 x(n)w(n)</text><text x="865" y="105" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="17">DFT 样值 X(k)</text><line x1="205" y1="99" x2="300" y2="99" stroke="#174b73" stroke-width="2" marker-end="url(#analog-dft-arrow)"/><line x1="450" y1="99" x2="545" y2="99" stroke="#174b73" stroke-width="2" marker-end="url(#analog-dft-arrow)"/><line x1="695" y1="99" x2="790" y2="99" stroke="#174b73" stroke-width="2" marker-end="url(#analog-dft-arrow)"/><text x="235" y="70" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">采样</text><text x="475" y="70" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">截断／加窗</text><text x="725" y="70" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">N 点 DFT</text><text x="58" y="160" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">采样率决定混叠；记录与窗函数决定泄漏和分辨率；零填充仅加密观察频点。</text></svg><figcaption style="margin-top:4pt;color:#52616d;text-align:center;font-size:9.5pt">图 3-8　模拟信号作 DFT 频谱分析的处理链。</figcaption></figure>'''


def _stems(values: list[float], *, x0: float, width: float, baseline: float, height: float, color: str) -> str:
    """Generate a stem row from samples instead of manually placing graphic rods."""
    step = width / max(1, len(values) - 1)
    parts: list[str] = []
    for index, value in enumerate(values):
        x = x0 + index * step
        y = baseline - value * height
        parts.append(f'<line x1="{x:.1f}" y1="{baseline:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="1.8"/><circle cx="{x:.1f}" cy="{y:.1f}" r="3.0" fill="{color}"/>')
    return "".join(parts)


def _curve(*, x0: float, width: float, baseline: float, height: float, fn) -> str:
    """Generate a continuous curve from its analytical sample function."""
    points = []
    for index in range(81):
        u = index / 80
        points.append(f'{x0 + u * width:.1f},{baseline - fn(u) * height:.1f}')
    return "M" + " L".join(points)


def analog_dft_spectrum_correspondence_svg() -> str:
    """Show the five data-driven time/frequency views used by DFT analysis."""
    samples = [1.0, 0.82, 0.67, 0.55, 0.45, 0.37, 0.30, 0.25, 0.20, 0.16]
    finite = samples[:7]
    periodic = samples[:5] + samples + samples[:5]
    spectrum = [0.25, 0.45, 0.68, 0.47, 0.31, 0.24, 0.31, 0.47, 0.68, 0.45, 0.25]
    axes = []
    for baseline in (83, 163, 243, 323, 403):
        axes.append(f'<line x1="40" y1="{baseline}" x2="420" y2="{baseline}" stroke="#174b73" stroke-width="1.4" marker-end="url(#spectrum-correspondence-arrow)"/><line x1="105" y1="{baseline + 24}" x2="105" y2="{baseline - 56}" stroke="#174b73" stroke-width="1.4" marker-end="url(#spectrum-correspondence-arrow)"/>')
        axes.append(f'<line x1="555" y1="{baseline}" x2="935" y2="{baseline}" stroke="#174b73" stroke-width="1.4" marker-end="url(#spectrum-correspondence-arrow)"/><line x1="620" y1="{baseline + 24}" x2="620" y2="{baseline - 56}" stroke="#174b73" stroke-width="1.4" marker-end="url(#spectrum-correspondence-arrow)"/>')
    analog_time = _curve(x0=105, width=190, baseline=83, height=46, fn=lambda u: math.exp(-3.0 * u))
    analog_freq = _curve(x0=620, width=190, baseline=83, height=46, fn=lambda u: math.exp(-7.5 * abs(2 * u - 1)))
    dtft = _curve(x0=620, width=190, baseline=163, height=43, fn=lambda u: 0.18 + 0.72 * abs(math.cos(2 * math.pi * u)) ** 7)
    broadened = _curve(x0=620, width=190, baseline=243, height=43, fn=lambda u: 0.22 + 0.50 * abs(math.cos(2 * math.pi * u)) ** 3 + 0.06 * abs(math.sin(18 * math.pi * u)))
    return f'''<figure data-diagram="analog-dft-spectrum-correspondence" style="break-inside:avoid;margin:10pt 0 13pt"><svg viewBox="0 0 980 455" role="img" aria-labelledby="analog-dft-spectrum-correspondence-title" style="display:block;width:100%;height:auto;border:1px solid #d6dde2;border-radius:5pt;background:#fff"><title id="analog-dft-spectrum-correspondence-title">模拟信号作 DFT 频谱分析的五层时频对应关系</title><defs><marker id="spectrum-correspondence-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#174b73"/></marker></defs><text x="32" y="28" fill="#174b73" font-family="Microsoft YaHei, sans-serif" font-size="18" font-weight="700">有限记录的频域展宽与 DFT 栅栏取样</text>{''.join(axes)}<path d="{analog_time}" fill="none" stroke="#d44c45" stroke-width="2.2"/><path d="{analog_freq}" fill="none" stroke="#d44c45" stroke-width="2.2"/>{_stems(samples, x0=105, width=190, baseline=163, height=42, color='#0d8794')}<path d="{dtft}" fill="none" stroke="#315fbd" stroke-width="2.2"/>{_stems(finite, x0=115, width=130, baseline=243, height=42, color='#0d8794')}<rect x="105" y="188" width="165" height="55" fill="none" stroke="#315fbd" stroke-dasharray="5 4" stroke-width="1.3"/><path d="{broadened}" fill="none" stroke="#0d8794" stroke-width="2.2"/>{_stems(periodic, x0=48, width=330, baseline=323, height=40, color='#0d8794')}{_stems(spectrum + spectrum[:4], x0=548, width=335, baseline=323, height=40, color='#7e168d')}{_stems(finite, x0=115, width=130, baseline=403, height=42, color='#0d8794')}{_stems(spectrum, x0=620, width=190, baseline=403, height=42, color='#7e168d')}<line x1="438" y1="83" x2="535" y2="83" stroke="#b56b2e" stroke-width="1.8" marker-end="url(#spectrum-correspondence-arrow)"/><line x1="438" y1="163" x2="535" y2="163" stroke="#b56b2e" stroke-width="1.8" marker-end="url(#spectrum-correspondence-arrow)"/><line x1="438" y1="243" x2="535" y2="243" stroke="#b56b2e" stroke-width="1.8" marker-end="url(#spectrum-correspondence-arrow)"/><line x1="438" y1="323" x2="535" y2="323" stroke="#b56b2e" stroke-width="1.8" marker-end="url(#spectrum-correspondence-arrow)"/><line x1="438" y1="403" x2="535" y2="403" stroke="#b56b2e" stroke-width="1.8" marker-end="url(#spectrum-correspondence-arrow)"/><text x="474" y="73" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="15" font-weight="700">FT</text><text x="462" y="153" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="15" font-weight="700">DTFT</text><text x="462" y="233" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="15" font-weight="700">DTFT</text><text x="468" y="313" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="15" font-weight="700">DFS</text><text x="470" y="393" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="15" font-weight="700">DFT</text><foreignObject x="116" y="34" width="115" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\(x_a(t)\\)</div></foreignObject><foreignObject x="632" y="34" width="140" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\(X_a(j\\Omega)\\)</div></foreignObject><foreignObject x="116" y="114" width="105" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\(x(n)\\)</div></foreignObject><foreignObject x="632" y="114" width="145" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\(X(e^{{j\\omega}})\\)</div></foreignObject><foreignObject x="116" y="194" width="150" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\(x(n)w(n)\\)</div></foreignObject><foreignObject x="632" y="194" width="190" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\(X(e^{{j\\omega}})*W(e^{{j\\omega}})\\)</div></foreignObject><foreignObject x="116" y="274" width="135" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\(\\widetilde{{x}}_N(n)\\)</div></foreignObject><foreignObject x="632" y="274" width="135" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\(\\widetilde{{X}}_N(k)\\)</div></foreignObject><foreignObject x="116" y="354" width="110" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\(x_N(n)\\)</div></foreignObject><foreignObject x="632" y="354" width="115" height="28"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\(X_N(k)\\)</div></foreignObject><text x="300" y="97" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="13">连续时间</text><text x="300" y="177" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="13">时域采样</text><text x="300" y="257" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="13">有限记录</text><text x="300" y="337" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="13">周期延拓</text><text x="300" y="417" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="13">有限样点</text><text x="875" y="97" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="13">连续频谱</text><text x="875" y="177" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="13">周期频谱</text><text x="875" y="257" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="13">展宽频谱</text><text x="875" y="337" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="13">周期谱样点</text><text x="875" y="417" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="13">有限谱样点</text></svg><figcaption style="margin-top:4pt;color:#52616d;text-align:center;font-size:9.5pt">图 3-9　模拟信号的有限记录、频域展宽与 DFT 栅栏取样之间的对应关系。</figcaption></figure>'''


def anti_aliasing_sampling_svg() -> str:
    """Plot spectrum copies before and after an anti-aliasing low-pass filter."""
    X = "{X}"  # Preserve the LaTeX group in the f-string below.
    core = _curve(x0=420, width=150, baseline=118, height=58, fn=lambda u: math.exp(-8 * abs(2 * u - 1)))
    left = _curve(x0=192, width=90, baseline=118, height=38, fn=lambda u: math.exp(-7 * abs(2 * u - 1)))
    right = _curve(x0=708, width=90, baseline=118, height=38, fn=lambda u: math.exp(-7 * abs(2 * u - 1)))
    safe_core = _curve(x0=420, width=150, baseline=235, height=58, fn=lambda u: math.exp(-10 * abs(2 * u - 1)))
    safe_left = _curve(x0=192, width=90, baseline=235, height=13, fn=lambda u: math.exp(-10 * abs(2 * u - 1)))
    safe_right = _curve(x0=708, width=90, baseline=235, height=13, fn=lambda u: math.exp(-10 * abs(2 * u - 1)))
    return rf'''<figure data-diagram="anti-aliasing-sampling" style="break-inside:avoid;margin:10pt 0 13pt"><svg viewBox="0 0 980 285" role="img" aria-labelledby="anti-aliasing-title" style="display:block;width:100%;height:auto;border:1px solid #d6dde2;border-radius:5pt;background:#fff"><title id="anti-aliasing-title">抗混叠滤波前后的采样频谱副本</title><defs><marker id="anti-alias-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#174b73"/></marker></defs><text x="34" y="28" fill="#174b73" font-family="Microsoft YaHei, sans-serif" font-size="18" font-weight="700">采样频谱副本与抗混叠滤波</text><line x1="105" y1="118" x2="905" y2="118" stroke="#174b73" stroke-width="1.5" marker-end="url(#anti-alias-arrow)"/><line x1="495" y1="156" x2="495" y2="55" stroke="#174b73" stroke-width="1.5" marker-end="url(#anti-alias-arrow)"/><path d="{left}" fill="none" stroke="#d44c45" stroke-width="2.2"/><path d="{core}" fill="none" stroke="#0d8794" stroke-width="2.4"/><path d="{right}" fill="none" stroke="#315fbd" stroke-width="2.2"/><line x1="345" y1="72" x2="345" y2="132" stroke="#b56b2e" stroke-dasharray="4 3"/><line x1="645" y1="72" x2="645" y2="132" stroke="#b56b2e" stroke-dasharray="4 3"/><text x="105" y="70" fill="#b83a30" font-family="Microsoft YaHei, sans-serif" font-size="15" font-weight="700">采样率不足：频谱副本重叠</text><line x1="105" y1="235" x2="905" y2="235" stroke="#174b73" stroke-width="1.5" marker-end="url(#anti-alias-arrow)"/><line x1="495" y1="273" x2="495" y2="172" stroke="#174b73" stroke-width="1.5" marker-end="url(#anti-alias-arrow)"/><path d="{safe_left}" fill="none" stroke="#d44c45" stroke-width="2.2"/><path d="{safe_core}" fill="none" stroke="#0d8794" stroke-width="2.4"/><path d="{safe_right}" fill="none" stroke="#315fbd" stroke-width="2.2"/><line x1="345" y1="190" x2="345" y2="248" stroke="#16866d" stroke-dasharray="4 3"/><line x1="645" y1="190" x2="645" y2="248" stroke="#16866d" stroke-dasharray="4 3"/><text x="105" y="187" fill="#16866d" font-family="Microsoft YaHei, sans-serif" font-size="15" font-weight="700">抗混叠低通后：副本之间保留保护带</text><foreignObject x="474" y="35" width="120" height="26"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px">\\(\widehat{{X}}_a(j\\Omega)\\)</div></foreignObject><foreignObject x="907" y="118" width="45" height="26"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px">\\(f\\)</div></foreignObject><foreignObject x="322" y="125" width="55" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:12px">\\(-f_h\\)</div></foreignObject><foreignObject x="627" y="125" width="55" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:12px">\\(f_h\\)</div></foreignObject></svg><figcaption style="margin-top:4pt;color:#52616d;text-align:center;font-size:9.5pt">图 3-10　抗混叠滤波把有效带宽限制在相邻采样频谱副本不重叠的范围内。</figcaption></figure>'''


def window_leakage_padding_svg() -> str:
    """Compare calculated window spectra and zero-padded DFT observation points."""
    rect = _curve(x0=75, width=350, baseline=125, height=54, fn=lambda u: abs(math.sin(15 * math.pi * u) / (15 * math.pi * u + 1e-6)))
    tri = _curve(x0=75, width=350, baseline=245, height=54, fn=lambda u: abs(math.sin(15 * math.pi * u) / (15 * math.pi * u + 1e-6)) ** 2)
    coarse = [1.0, 0.55, 0.18, 0.1, 0.16, 0.52, 1.0]
    fine = [abs(math.cos(i * math.pi / 15)) ** 2 for i in range(16)]
    return f'''<figure data-diagram="window-leakage-and-padding" style="break-inside:avoid;margin:10pt 0 13pt"><svg viewBox="0 0 980 305" role="img" aria-labelledby="window-padding-title" style="display:block;width:100%;height:auto;border:1px solid #d6dde2;border-radius:5pt;background:#fff"><title id="window-padding-title">窗口泄漏与零填充的频谱观察效果</title><defs><marker id="window-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#174b73"/></marker></defs><text x="34" y="28" fill="#174b73" font-family="Microsoft YaHei, sans-serif" font-size="18" font-weight="700">窗函数的泄漏权衡与零填充的观察加密</text><line x1="62" y1="125" x2="440" y2="125" stroke="#174b73" stroke-width="1.4" marker-end="url(#window-arrow)"/><line x1="75" y1="153" x2="75" y2="65" stroke="#174b73" stroke-width="1.4" marker-end="url(#window-arrow)"/><path d="{rect}" fill="none" stroke="#b56b2e" stroke-width="2.1"/><text x="85" y="63" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">矩形窗：主瓣窄、旁瓣高</text><line x1="62" y1="245" x2="440" y2="245" stroke="#174b73" stroke-width="1.4" marker-end="url(#window-arrow)"/><line x1="75" y1="273" x2="75" y2="185" stroke="#174b73" stroke-width="1.4" marker-end="url(#window-arrow)"/><path d="{tri}" fill="none" stroke="#16866d" stroke-width="2.1"/><text x="85" y="183" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">三角窗：旁瓣低、主瓣宽</text><line x1="530" y1="125" x2="920" y2="125" stroke="#174b73" stroke-width="1.4" marker-end="url(#window-arrow)"/><line x1="550" y1="153" x2="550" y2="65" stroke="#174b73" stroke-width="1.4" marker-end="url(#window-arrow)"/>{_stems(coarse, x0=570, width=270, baseline=125, height=48, color='#7e168d')}<text x="570" y="63" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">原记录的 8 点 DFT 栅栏</text><line x1="530" y1="245" x2="920" y2="245" stroke="#174b73" stroke-width="1.4" marker-end="url(#window-arrow)"/><line x1="550" y1="273" x2="550" y2="185" stroke="#174b73" stroke-width="1.4" marker-end="url(#window-arrow)"/>{_stems(fine, x0=570, width=300, baseline=245, height=48, color='#0d8794')}<text x="570" y="183" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">同一记录零填充后的 32 点观察栅栏</text><foreignObject x="422" y="125" width="34" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:12px">\\(\\omega\\)</div></foreignObject><foreignObject x="900" y="245" width="34" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:12px">\\(k\\)</div></foreignObject></svg><figcaption style="margin-top:4pt;color:#52616d;text-align:center;font-size:9.5pt">图 3-11　窗函数改变主瓣/旁瓣权衡；零填充增加频率样点而不改变由记录长度决定的本征分辨率。</figcaption></figure>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>3.5 用 DFT 对模拟信号作频谱分析</h1>
<p>将模拟信号的有限时段记录采样后作 DFT，得到的是连续频谱的离散观察。分析结果同时受时域采样、记录长度、截断和频域取样影响，因此必须区分采样频率与频率分辨率。</p>
<p><strong>时频对应图：</strong>下图把连续时间信号、采样序列、有限记录、周期延拓和有限 DFT 样点并列，用于辨认截断导致的频域展宽，以及 DFT 只在离散栅栏上观察频谱这一事实。</p>
""" + analog_dft_spectrum_correspondence_svg() + r"""
<h2>采样参数与频率分辨率</h2>
<div class="formula">\[
T_0=NT,\qquad f_s=\frac{1}{T},\qquad F_0=\frac{1}{T_0},\qquad f_s=NF_0.
\]</div>
<p>其中 [[T]] 为采样间隔，[[f_s]] 为采样频率，[[T_0]] 为记录长度，[[F_0]] 为频率分辨率（频谱间隔），[[N]] 为采样点数。为避免时域采样造成的频域混叠，应满足：</p>
<div class="formula">\[
f_s\geq2f_h.
\]</div>
<p>提高 [[f_s]] 扩大可观察的最高频率；增大记录长度 [[T_0]] 才能减小 [[F_0]]、提高频率分辨率。两者由不同参数控制，不能混为一谈。</p>
<h2>频谱分析的三个典型问题</h2>
<p><strong>频域混叠：</strong>时域采样率不足时，原连续频谱的周期副本相互重叠。处理方法是选择足够的 [[f_s]]，并在 A/D 前使用抗混叠低通滤波器。</p>
<p><strong>采样频谱副本公式：</strong>这个公式说明时域按间隔 [[T]] 采样后，模拟频谱会以采样角频率为间隔重复；它用于判断相邻副本是否发生重叠：</p>
<div class="formula">\[
\widehat{X}_a(j\Omega)=\frac{1}{T}\sum_{m=-\infty}^{\infty}X_a\left(j(\Omega-m\Omega_s)\right),
\qquad \Omega_s=\frac{2\pi}{T}.
\]</div>
""" + anti_aliasing_sampling_svg() + r"""
<p><strong>频谱泄漏：</strong>有限时间记录等价于时域乘窗，频域则与窗函数频谱卷积；非整周期截断会使原本集中的谱线扩展到相邻频率。选择合适的窗函数形状、增加窗长可改善泄漏表现。</p>
<p><strong>栅栏效应：</strong>DFT 只在离散频点上取样，真实谱峰若落在两个 DFT 栅栏之间，观察到的峰值与位置都会受限。时域零填充能加密频域样点，使观察更细致，但不改变由 [[T_0]] 决定的本征分辨率。</p>
<h2>窗函数与记录长度</h2>
<p>矩形窗主瓣较窄但旁瓣较高；三角窗和升余弦类窗可降低旁瓣、缓解泄漏，但主瓣会变宽。窗的形状决定主瓣与旁瓣的权衡，窗长 [[N]] 增大则通常使过渡带变窄。选择窗函数时应根据相邻谱线间隔与强弱差异综合判断。</p>
<h2>矩形窗的频谱展宽</h2>
<p><strong>矩形窗频谱公式：</strong>长度为 [[N]] 的矩形窗在频域中的响应为：</p>
<div class="formula">\[
W_R\left(e^{j\omega}\right)
=e^{-j\frac{N-1}{2}\omega}
\frac{\sin\left(\frac{N\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}.
\]</div>
<p>这个公式用来判断有限记录对单根谱线的展宽方式。其幅度主瓣的两侧第一个零点间隔约为 [[4\pi/N]]；因此增大 [[N]] 能使主瓣变窄、过渡带变窄。仅仅增大记录长度并不会使矩形窗旁瓣的相对起伏消失，强谱线附近仍可能掩盖较弱谱线。</p>
<h2>观察实例：窗口长度与泄漏</h2>
<p><strong>单一余弦的记录长度比较：</strong>令 [[x(n)=\cos\left(\frac{\pi}{4}n\right)]]，分别记录 [[y_1(n)=x(n)R_{32}(n)]] 与 [[y_2(n)=x(n)R_{64}(n)]]。这两个记录使用同一种矩形窗；较长的 [[R_{64}(n)]] 使主瓣更窄，从而使频率位置的观察更精细。</p>
<p><strong>强弱相邻分量的记录长度比较：</strong>令</p>
<div class="formula">\[
x(n)=\cos\left(\frac{\pi}{4}n\right)+0.2\cos\left(\frac{\pi}{5}n\right).
\]</div>
<p>分别采用 [[R_{40}(n)]] 和 [[R_{320}(n)]] 截取记录。短记录时，较强分量的泄漏可能覆盖弱分量；延长为 [[R_{320}(n)]] 后主瓣变窄，弱分量更容易分辨。三角窗通常具有更低旁瓣、但更宽主瓣：若窗口长度不变，它未必更利于分开很接近的两条谱线。</p>
""" + window_leakage_padding_svg() + r"""
<h2>零填充的作用</h2>
<p><strong>零填充序列：</strong>把已有的 [[N]] 点记录补到 [[L]] 点，可写成：</p>
<div class="formula">\[
x_L(n)=
\begin{cases}
x(n),&0\leq n\leq N-1,\\
0,&N\leq n\leq L-1.
\end{cases}
\]</div>
<p>此操作用于加密 DFT 的频率观察网格：频点间隔由 [[2\pi/N]] 变为 [[2\pi/L]]。它不会延长真实记录 [[T_0]]，也不会改变本征频率分辨率 [[F_0=1/T_0]]；零填充只能帮助更细地观察已有频谱形状。</p>
<h2>工程处理流程</h2>
<ol class="steps">
<li>由最高频率 [[f_h]] 选定采样率，满足 [[f_s\geq2f_h]] 并留出模拟滤波过渡带。</li>
<li>由所需频率间隔 [[F_0]] 确定最小记录长度 [[T_0\geq1/F_0]]。</li>
<li>计算 [[N=T_0/T]]；若处理器要求 2 的整数幂，可向上选取合适 [[N]]。</li>
<li>根据泄漏要求选窗；需要更密显示时可零填充后再作 DFT。</li>
</ol>
<h2>例题：参数选取</h2>
<p>某 FFT 处理器要求采样点数为 2 的整数幂。若频率分辨率要求为 [[F_0\leq10\,\mathrm{Hz}]]，信号最高频率不超过 [[4\,\mathrm{kHz}]]，则先取 [[T_0\geq0.1\,\mathrm{s}]]，再取 [[f_s\geq8\,\mathrm{kHz}]]。相应点数 [[N=T_0f_s\geq800]]，向上取 1024 点；此时 [[T=1/8000\,\mathrm{s}]]，[[T_0=1024T=0.128\,\mathrm{s}]]，实际频率间隔为 [[F_0=7.8125\,\mathrm{Hz}]]。</p>
<h3>例题题干</h3>
<p>有一频谱分析用的 FFT 处理器，其抽样点数必须是 2 的整数幂，假设没有采用任何数据处理的措施，已给条件为：（a）对频率分辨率的要求是 [[F_0\leq10\text{ Hz}]]；（b）信号频率不超过 [[4\text{ kHz}]]。试确定以下参量：（A）最小记录长度 [[T_0]]；（B）抽样点间的最大时间间隔 [[T]]（即最小抽样频率）；（C）在一个记录中最少点数 [[N]]。</p>
<p>解：[[T_0\geq1/F_0=0.1\text{ s}]]；为满足采样定理，[[f_s\geq2\times4\text{ kHz}=8\text{ kHz}]]，所以 [[T\leq0.125\text{ ms}]]。由 [[N\geq T_0f_s=800]] 且 [[N]] 必须为 2 的整数幂，取 [[N=1024]]。此时 [[T_0=1024\times0.125\text{ ms}=0.128\text{ s}]]，实际频率分辨率为 [[F_0=1/T_0=7.8125\text{ Hz}]]，满足要求。</p>

<h2>多音信号的谱线组成</h2>
<p><strong>两音信号展开式：</strong>这个公式把带相位的两个余弦分量写成四个复指数项，用于确定 DFT 频谱中正、负频率谱线的位置和相位：</p>
<div class="formula">\[
\begin{aligned}
x(n)&=A_0\cos(\omega_0 n+\theta_0)+A_1\cos(\omega_1 n+\theta_1)\\
&=\frac{A_0}{2}e^{j\theta_0}e^{j\omega_0n}+\frac{A_0}{2}e^{-j\theta_0}e^{-j\omega_0n}\\
&\quad+\frac{A_1}{2}e^{j\theta_1}e^{j\omega_1n}+\frac{A_1}{2}e^{-j\theta_1}e^{-j\omega_1n}.
\end{aligned}
\]</div>
<p><strong>对应的 DTFT 冲激谱：</strong>每个余弦分量在 [[\omega=\pm\omega_i]] 处各产生一条冲激谱线；相位由复权重 [[e^{\pm j\theta_i}]] 给出：</p>
<div class="formula">\[
X(e^{j\omega})=\pi\sum_{i=0}^{1}A_i\bigl[
e^{j\theta_i}\delta(\omega-\omega_i)
+e^{-j\theta_i}\delta(\omega+\omega_i)
\bigr].
\]</div>

<h2>傅里叶的故事</h2>
<p>傅里叶分析得名于法国数学家让·巴普蒂斯·约瑟夫·傅里叶（1768—1830）。在他之前，人们已经知道可用三角函数描述周期现象；欧拉研究声波传播时进一步使用正弦分解，拉格朗日也将相关思想用于天体轨道的观察与预测。</p>
<p>1807 年，傅里叶提交有关热传播的论文，主张周期信号可以由适当的正弦分量组合表示。这一观点当时引起争议，特别是对于不连续信号能否分解的问题。后来他在《热的解析理论》（1822）中系统阐述了这些思想；狄利克雷等数学家给出了相应的严格条件，通常称为狄利克雷条件。</p>
<p>这一历史提醒我们：频谱图不是只为“看见峰值”，还要结合采样、截断、加窗和变换条件解释峰值为什么出现、为什么展宽，以及所得结论的适用范围。</p>
</main>
"""
    content = content.replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    html = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(html, encoding="utf-8")
    return output
