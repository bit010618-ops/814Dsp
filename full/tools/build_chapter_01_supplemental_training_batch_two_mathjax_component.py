"""2007 sampling-spectrum exam question and detailed textbook solution."""
from __future__ import annotations


def _sampling_system_svg() -> str:
    """Return the clean source-faithful sampling system without source watermark."""
    return r'''<svg class="signal-svg" data-diagram="2007-sampling-system" viewBox="0 0 860 300" role="img" aria-label="模拟采样与序列生成系统">
<style>.s07-line{fill:none;stroke:#174b73;stroke-width:2.4}.s07-block{fill:#f5f8f9;stroke:#008d8c;stroke-width:2.1}.s07-text{fill:#315d7c;font-size:18px;font-family:"Microsoft YaHei",sans-serif}</style>
<defs><marker id="s07-arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0L9 4.5L0 9Z" fill="#174b73"/></marker></defs>
<text class="s07-text" x="430" y="32" text-anchor="middle">模拟采样与序列生成</text>
<path class="s07-line" d="M75 135H332" marker-end="url(#s07-arrow)"/><text x="90" y="117" class="s07-text">x(t)</text>
<circle cx="350" cy="135" r="30" fill="#fff" stroke="#174b73" stroke-width="2.4"/><path class="s07-line" d="M332 117L368 153M332 153L368 117"/>
<path class="s07-line" d="M350 235V166" marker-end="url(#s07-arrow)"/><text x="375" y="214" class="s07-text">p(t)</text>
<path class="s07-line" d="M380 135H460" marker-end="url(#s07-arrow)"/><text x="390" y="117" class="s07-text">x<tspan baseline-shift="sub" font-size="12">p</tspan>(t)</text>
<rect class="s07-block" x="470" y="93" width="190" height="84" rx="8"/><text x="565" y="144" class="s07-text" text-anchor="middle">序列生成</text>
<path class="s07-line" d="M660 135H786" marker-end="url(#s07-arrow)"/><text x="734" y="117" class="s07-text">x(n)</text>
<foreignObject x="257" y="235" width="250" height="42"><div xmlns="http://www.w3.org/1999/xhtml">\(p(t)=\sum_{k=-\infty}^{\infty}\delta(t-kT)\)</div></foreignObject>
</svg>'''


def _frequency_relations_svg() -> str:
    """Draw original, impulse-sampled and discrete-time triangular spectra."""
    return r'''<svg class="signal-svg" data-plot="2007-sampling-frequency-relations" viewBox="0 0 900 780" role="img" aria-label="连续频谱、采样频谱与离散时间频谱">
<style>.s07-axis{fill:none;stroke:#174b73;stroke-width:2.1}.s07-spectrum{fill:none;stroke:#008d8c;stroke-width:2.7}.s07-title{fill:#315d7c;font-size:18px;font-family:"Microsoft YaHei",sans-serif}</style>
<defs><marker id="s07-freq-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
<text x="450" y="30" class="s07-title" text-anchor="middle">采样前后的频谱关系</text>
<text x="80" y="88" class="s07-title">原连续时间频谱</text>
<path class="s07-axis" d="M80 220H825" marker-end="url(#s07-freq-arrow)"/><path class="s07-axis" d="M450 244V102" marker-end="url(#s07-freq-arrow)"/><path class="s07-spectrum" d="M270 220L450 122L630 220"/>
<foreignObject x="808" y="225" width="52" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega\)</div></foreignObject><foreignObject x="458" y="103" width="105" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(X(\omega)\)</div></foreignObject><foreignObject x="224" y="227" width="100" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(-2\pi\times10^3\)</div></foreignObject><foreignObject x="431" y="227" width="28" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(0\)</div></foreignObject><foreignObject x="595" y="227" width="100" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(2\pi\times10^3\)</div></foreignObject>
<text x="80" y="312" class="s07-title">冲激采样后的周期频谱</text>
<path class="s07-axis" d="M80 452H825" marker-end="url(#s07-freq-arrow)"/><path class="s07-axis" d="M450 476V326" marker-end="url(#s07-freq-arrow)"/>
<path class="s07-spectrum" d="M85 452L90 450L95 452M270 452L450 352L630 452M805 452L810 450L815 452"/>
<foreignObject x="808" y="457" width="52" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega\)</div></foreignObject><foreignObject x="458" y="327" width="125" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(X_p(\omega)\)</div></foreignObject><foreignObject x="421" y="459" width="60" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(0\)</div></foreignObject><foreignObject x="592" y="459" width="110" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega_s=4\pi\times10^3\)</div></foreignObject>
<text x="80" y="546" class="s07-title">离散序列的 DTFT（以 \(2\pi\) 为周期）</text>
<path class="s07-axis" d="M80 690H825" marker-end="url(#s07-freq-arrow)"/><path class="s07-axis" d="M450 720V560" marker-end="url(#s07-freq-arrow)"/><path class="s07-spectrum" d="M270 690L450 590L630 690"/>
<foreignObject x="808" y="695" width="70" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\Omega\)</div></foreignObject><foreignObject x="458" y="561" width="155" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(X(e^{j\Omega})\)</div></foreignObject><foreignObject x="258" y="697" width="50" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(-\pi\)</div></foreignObject><foreignObject x="435" y="697" width="30" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(0\)</div></foreignObject><foreignObject x="617" y="697" width="45" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\pi\)</div></foreignObject>
</svg>'''


def training_html() -> str:
    """Return the 2007 question with the original wording and clean system graphic."""
    return r'''<section class="exam-page"><h1>第一章 补充真题</h1>
<div class="exam-head"><span>2007 年真题</span><span>详解见 P.____</span></div>
<p>五、图示系统，\(x(t)=\dfrac{\sin^2\!\left(\pi\times10^3t\right)}{\left(\pi\times10^3t\right)^2}\)，\(T=0.5\times10^{-3}\,\mathrm{s}\)，</p>
''' + _sampling_system_svg() + r'''<p>（1）计算 \(x(t)\)、\(x_p(t)\)、\(x(n)\) 所对应的频谱 \(X(j\omega)\)、\(X_p(j\omega)\)、\(X(e^{j\Omega})\)，并画出频谱图。</p>
<p>（2）\(\displaystyle\int_{-\infty}^{\infty}x(t)\,\mathrm{d}t\) 和 \(\displaystyle\sum_{n=-\infty}^{\infty}x(n)\)。</p>
</section>'''


def answers_html() -> str:
    """Return the full Fourier-domain derivation and the two requested sums."""
    return r'''<section class="answer-page"><h1>真题整理详解（续）</h1><h2>2007 年真题：模拟采样与离散序列频谱</h2>
<p>记 \(a=\pi\times10^3\)。由 \(x(t)=\operatorname{Sa}^2(at)\) 及“时域相乘对应频域卷积”，原连续时间频谱为：</p>
<div class="formula">\[X(\omega)=\begin{cases}10^{-3}\!\left(1-\dfrac{|\omega|}{2\pi\times10^3}\right),&|\omega|\leq2\pi\times10^3,\\[4pt]0,&|\omega|>2\pi\times10^3.\end{cases}\]</div>
<p>采样周期为 \(T=0.5\times10^{-3}\,\mathrm{s}\)，故 \(\omega_s=2\pi/T=4\pi\times10^3\,\mathrm{rad}\,\mathrm{s}^{-1}\)。冲激采样后：</p>
<div class="formula">\[X_p(\omega)=\frac{1}{T}\sum_{k=-\infty}^{\infty}X(\omega-k\omega_s).\]</div>
<p>相邻三角形副本在零点处相接，没有重叠。序列生成后的离散样值为：</p>
<div class="formula">\[x(n)=\begin{cases}1,&n=0,\\[2pt]\dfrac{4}{\pi^2n^2},&n\text{ 为奇数},\\[6pt]0,&n\ne0\text{ 且 }n\text{ 为偶数}.\end{cases}\]</div>
<p>其 DTFT 是以 \(2\pi\) 为周期的三角谱；在主值区间 \(-\pi\leq\Omega\leq\pi\) 内：</p>
<div class="formula">\[X\!\left(e^{j\Omega}\right)=2\left(1-\frac{|\Omega|}{\pi}\right).\]</div>
''' + _frequency_relations_svg() + r'''<p>最后，连续信号积分等于零频率处的谱值，离散序列求和等于 DTFT 在 \(\Omega=0\) 处的值，因此：</p>
<div class="formula">\[\int_{-\infty}^{\infty}x(t)\,\mathrm{d}t=X(0)=10^{-3},\qquad\sum_{n=-\infty}^{\infty}x(n)=X\!\left(e^{j0}\right)=2.\]</div>
</section>'''
