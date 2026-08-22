"""2016 chapter-one sampling exam and its detailed MathJax solution."""
from __future__ import annotations

import math


def _sampled_signal_svg() -> str:
    """Draw a continuous Sa signal and its impulse-sampling locations."""
    curve_points = []
    for index in range(321):
        time = -2.4 + index * 4.8 / 320
        amplitude = 1.0 if abs(time) < 1e-12 else math.sin(2 * time) / (2 * time)
        curve_points.append(f"{430 + 142 * time:.1f},{142 - 76 * amplitude:.1f}")

    stems = []
    for sample in range(-4, 5):
        time = sample * math.pi / 6
        amplitude = 1.0 if sample == 0 else math.sin(2 * time) / (2 * time)
        x = 430 + 142 * time
        y = 300 - 86 * amplitude
        stems.append(
            f'<line class="s16-stem" x1="{x:.1f}" y1="300" x2="{x:.1f}" y2="{y:.1f}"/>'
            f'<circle class="s16-dot" cx="{x:.1f}" cy="{y:.1f}" r="3.8"/>'
        )

    return fr'''<svg class="signal-svg" data-plot="2016-impulse-sampling-time" viewBox="0 0 860 380" role="img" aria-label="Sa 信号与冲激采样波形">
<style>.s16-axis{{fill:none;stroke:#174b73;stroke-width:2.2}}.s16-curve{{fill:none;stroke:#008d8c;stroke-width:2.5}}.s16-stem{{stroke:#008d8c;stroke-width:2.1}}.s16-dot{{fill:#bf6500}}.s16-title{{fill:#315d7c;font-size:18px;font-family:"Microsoft YaHei",sans-serif}}</style>
<defs><marker id="s16-time-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
<text class="s16-title" x="430" y="28" text-anchor="middle">原信号与冲激采样</text>
<path class="s16-axis" d="M58 142H807" marker-end="url(#s16-time-arrow)"/><path class="s16-axis" d="M430 206V48" marker-end="url(#s16-time-arrow)"/>
<polyline class="s16-curve" points="{' '.join(curve_points)}"/>
<foreignObject x="776" y="148" width="42" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(t\)</div></foreignObject><foreignObject x="442" y="48" width="85" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(f(t)\)</div></foreignObject>
<path class="s16-axis" d="M58 300H807" marker-end="url(#s16-time-arrow)"/><path class="s16-axis" d="M418 356V213" marker-end="url(#s16-time-arrow)"/>
{''.join(stems)}
<foreignObject x="776" y="306" width="42" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(t\)</div></foreignObject><foreignObject x="442" y="216" width="90" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(f_s(t)\)</div></foreignObject>
<foreignObject x="424" y="320" width="25" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(0\)</div></foreignObject><foreignObject x="491" y="320" width="90" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(T=\pi/6\)</div></foreignObject>
</svg>'''


def _sampled_spectrum_svg() -> str:
    """Draw non-overlapping rectangular spectrum copies at the sampled period."""
    copies = []
    for copy_index in range(-2, 3):
        center = 430 + 15 * 12 * copy_index
        left, right = center - 30, center + 30
        copies.append(f'<path class="s16-copy" d="M{left:.1f} 276V118H{right:.1f}V276"/>')

    return fr'''<svg class="signal-svg" data-plot="2016-impulse-sampling-spectrum" viewBox="0 0 860 340" role="img" aria-label="冲激采样后的周期频谱">
<style>.s16-axis{{fill:none;stroke:#174b73;stroke-width:2.2}}.s16-copy{{fill:none;stroke:#008d8c;stroke-width:2.8}}.s16-title{{fill:#315d7c;font-size:18px;font-family:"Microsoft YaHei",sans-serif}}</style>
<defs><marker id="s16-spectrum-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
<text class="s16-title" x="430" y="28" text-anchor="middle">冲激采样后的周期频谱</text>
<path class="s16-axis" d="M48 276H816" marker-end="url(#s16-spectrum-arrow)"/><path class="s16-axis" d="M430 304V62" marker-end="url(#s16-spectrum-arrow)"/>
{''.join(copies)}
<foreignObject x="804" y="284" width="42" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega\)</div></foreignObject><foreignObject x="438" y="64" width="105" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(F_s(\omega)\)</div></foreignObject>
<foreignObject x="365" y="284" width="45" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(-2\)</div></foreignObject><foreignObject x="426" y="284" width="25" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(0\)</div></foreignObject><foreignObject x="485" y="284" width="45" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(2\)</div></foreignObject>
<foreignObject x="606" y="284" width="90" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega_s\)</div></foreignObject>
</svg>'''


def training_html() -> str:
    """Return the source-faithful 2016 question, without solutions or additions."""
    return r'''<section class="exam-page"><h1>第一章 补充真题</h1>
<div class="exam-head"><span>2016 年真题</span><span>详解见 P.____</span></div>
<p>六、已知 \(f(t)=\operatorname{Sa}(2t)\)，用 \(\delta_T(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT)\) 进行取样：</p>
<p>（1）求麦奎斯特频率；</p>
<p>（2）如果 \(\omega_s=6\omega_m\)，求 \(f_s(t)=f(t)\delta_T(t)\)，并画出波形；</p>
<p>（3）若 \(F_s(\omega)=\mathcal{F}[f_s(t)]\)，画出其频谱图。</p>
</section>'''


def answers_html() -> str:
    """Return the full worked solution with numeric, non-overlapping diagrams."""
    return r'''<section class="answer-page"><h1>真题整理详解（续）</h1><h2>2016 年真题：冲激采样与频谱复制</h2>
<p>采用 \(\operatorname{Sa}(x)=\sin x/x\) 的定义，则 \(f(t)=\sin(2t)/(2t)\)。其频谱只在 \(|\omega|\leq2\) 内非零，因此最高角频率为：</p>
<div class="formula">\[\omega_m=2\,\mathrm{rad}\,\mathrm{s}^{-1},\qquad f_m=\frac{\omega_m}{2\pi}=\frac{1}{\pi}\,\mathrm{Hz}.\]</div>
<p>因此奈奎斯特频率为 \(f_m=1/\pi\,\mathrm{Hz}\)，相应的最小采样角频率为 \(\omega_{s,\min}=2\omega_m=4\,\mathrm{rad}\,\mathrm{s}^{-1}\)。</p>
<p>题设 \(\omega_s=6\omega_m\)，所以：</p>
<div class="formula">\[\omega_s=12\,\mathrm{rad}\,\mathrm{s}^{-1},\qquad T=\frac{2\pi}{\omega_s}=\frac{\pi}{6}\,\mathrm{s}.\]</div>
<p>于是冲激采样信号为：</p>
<div class="formula">\[f_s(t)=\sum_{n=-\infty}^{\infty}f\!\left(\frac{n\pi}{6}\right)\delta\!\left(t-\frac{n\pi}{6}\right).\]</div>
''' + _sampled_signal_svg() + r'''<p>原信号的连续时间傅里叶变换为：</p>
<div class="formula">\[F(\omega)=\frac{\pi}{2}\,\operatorname{rect}\!\left(\frac{\omega}{4}\right).\]</div>
<p>冲激采样使频谱以 \(\omega_s=12\,\mathrm{rad}\,\mathrm{s}^{-1}\) 周期复制：</p>
<div class="formula">\[F_s(\omega)=\frac{1}{T}\sum_{k=-\infty}^{\infty}F(\omega-k\omega_s)=\frac{1}{T}\sum_{k=-\infty}^{\infty}F(\omega-12k).\]</div>
<p>每个矩形副本宽度为 \(4\,\mathrm{rad}\,\mathrm{s}^{-1}\)，相邻副本中心间距为 \(12\,\mathrm{rad}\,\mathrm{s}^{-1}\)，故互不重叠。</p>
''' + _sampled_spectrum_svg() + r'''</section>'''
