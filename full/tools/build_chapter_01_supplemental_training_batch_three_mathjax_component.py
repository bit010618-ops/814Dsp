"""2025 finite-width and ideal-impulse sampling question with full solution."""
from __future__ import annotations


def _bipolar_square_wave_svg() -> str:
    """Draw the original bipolar square wave using exact period and amplitude geometry."""
    return r'''<svg class="signal-svg" data-plot="2025-bipolar-square-wave" viewBox="0 0 860 350" role="img" aria-label="幅度为正负五伏的周期方波">
<style>.s25-axis{fill:none;stroke:#174b73;stroke-width:2.2}.s25-wave{fill:none;stroke:#008d8c;stroke-width:2.8}.s25-title{fill:#315d7c;font-size:18px;font-family:"Microsoft YaHei",sans-serif}</style>
<defs><marker id="s25-wave-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
<text x="430" y="28" class="s25-title" text-anchor="middle">题设双极性周期方波</text>
<path class="s25-axis" d="M58 176H807" marker-end="url(#s25-wave-arrow)"/><path class="s25-axis" d="M430 304V55" marker-end="url(#s25-wave-arrow)"/>
<path class="s25-wave" d="M90 78H185V274H280V78H375V274H470V78H565V274H660V78H755"/>
<foreignObject x="795" y="182" width="35" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(t\)</div></foreignObject><foreignObject x="438" y="56" width="75" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(x(t)\)</div></foreignObject>
<foreignObject x="440" y="80" width="38" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(5\)</div></foreignObject><foreignObject x="440" y="252" width="45" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(-5\)</div></foreignObject>
<path class="s25-axis" d="M470 318H565"/><path class="s25-axis" d="M470 311V325M565 311V325"/><foreignObject x="484" y="316" width="85" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(T_0/2\)</div></foreignObject>
<foreignObject x="100" y="292" width="250" height="32"><div xmlns="http://www.w3.org/1999/xhtml">\(T_0=0.1\,\mathrm{s}\)</div></foreignObject>
</svg>'''


def _pulse_sampling_spectrum_svg() -> str:
    """Show line spectrum, finite-pulse envelope and ideal-impulse replica contrast."""
    return r'''<svg class="signal-svg" data-plot="2025-pulse-sampling-spectrum" viewBox="0 0 900 720" role="img" aria-label="有限宽周期脉冲采样与理想冲激采样频谱对比">
<style>.s25-axis{fill:none;stroke:#174b73;stroke-width:2.1}.s25-stem{stroke:#008d8c;stroke-width:2.4}.s25-ideal{stroke:#bf6500;stroke-width:2.4}.s25-env{fill:none;stroke:#8a6277;stroke-width:2;stroke-dasharray:6 4}.s25-title{fill:#315d7c;font-size:18px;font-family:"Microsoft YaHei",sans-serif}</style>
<defs><marker id="s25-freq-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
<text x="450" y="30" class="s25-title" text-anchor="middle">方波与两种采样方式的频谱关系</text>
<text x="70" y="88" class="s25-title">方波的谐波线谱（示意）</text><path class="s25-axis" d="M70 220H830" marker-end="url(#s25-freq-arrow)"/><path class="s25-axis" d="M450 242V112" marker-end="url(#s25-freq-arrow)"/>
<path class="s25-stem" d="M330 220V180M370 220V152M410 220V98M490 220V98M530 220V152M570 220V180"/>
<foreignObject x="810" y="225" width="42" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega\)</div></foreignObject><foreignObject x="455" y="113" width="95" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(X(\omega)\)</div></foreignObject><foreignObject x="416" y="225" width="70" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega_0\)</div></foreignObject>
<text x="70" y="300" class="s25-title">有限宽脉冲采样：副本受 \(\operatorname{Sa}\) 包络加权</text><path class="s25-axis" d="M70 450H830" marker-end="url(#s25-freq-arrow)"/><path class="s25-axis" d="M450 472V330" marker-end="url(#s25-freq-arrow)"/>
<path class="s25-env" d="M90 438Q250 350 450 338Q650 350 810 438"/><path class="s25-stem" d="M180 450V420M240 450V400M300 450V382M360 450V368M420 450V356M480 450V356M540 450V368M600 450V382M660 450V400M720 450V420"/>
<foreignObject x="810" y="455" width="42" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega\)</div></foreignObject><foreignObject x="456" y="331" width="110" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(X_s(\omega)\)</div></foreignObject><foreignObject x="392" y="455" width="120" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(k\omega_s\)</div></foreignObject>
<text x="70" y="534" class="s25-title">理想冲激采样：各频谱副本等幅复制</text><path class="s25-axis" d="M70 674H830" marker-end="url(#s25-freq-arrow)"/><path class="s25-axis" d="M450 698V564" marker-end="url(#s25-freq-arrow)"/>
<path class="s25-ideal" d="M180 674V620M240 674V620M300 674V620M360 674V620M420 674V620M480 674V620M540 674V620M600 674V620M660 674V620M720 674V620"/>
<foreignObject x="810" y="679" width="42" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega\)</div></foreignObject><foreignObject x="456" y="565" width="135" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\(X_{s,\delta}(\omega)\)</div></foreignObject>
</svg>'''


def training_html() -> str:
    """Return the question with its source parameters and the repaired clean wave plot."""
    return r'''<section class="exam-page"><h1>第一章 补充真题</h1>
<div class="exam-head"><span>2025 年真题</span><span>详解见 P.____</span></div>
<p>六、如图一方波信号 \(x(t)\) 幅度为 \(-5\,\mathrm{V}\sim5\,\mathrm{V}\)，周期为 \(0.1\,\mathrm{s}\)，脉冲为 \(0.05\,\mathrm{s}\)，被一幅度为 \(1\,\mathrm{V}\)，脉冲为 \(\tau\) 秒，采样周期为 \(T_s=10^{-2}\,\mathrm{s}\) 的周期脉冲信号 \(s(t)\) 进行采样，获得采样信号 \(x_s(t)\)，其中 \(\tau\ll T_s\)。</p>
''' + _bipolar_square_wave_svg() + r'''<p>（1）是否满足采样定理。</p>
<p>（2）计算 \(x(t)\)、\(s(t)\)、\(x_s(t)\) 的频谱表达式，并画出频谱图。</p>
<p>（3）若 \(s(t)\) 为理想冲激脉冲序列，计算采样信号 \(x_s(t)\) 的频谱，并与（2）进行对比分析。</p>
</section>'''


def answers_html() -> str:
    """Return the finite-pulse and ideal-impulse frequency-domain comparison."""
    return r'''<section class="answer-page"><h1>真题整理详解（续）</h1><h2>2025 年真题：周期脉冲采样与频谱对比</h2>
<p>方波周期为 \(T_0=0.1\,\mathrm{s}\)，故 \(\omega_0=2\pi/T_0=20\pi\,\mathrm{rad}\,\mathrm{s}^{-1}\)。以题图中心的正半周为对称中心，可写为：</p>
<div class="formula">\[x(t)=\frac{20}{\pi}\sum_{r=0}^{\infty}\frac{(-1)^r}{2r+1}\cos\!\left((2r+1)\omega_0t\right).\]</div>
<p>因此它含有无穷多个奇次谐波，并非带限信号。尽管 \(\omega_s=\frac{2\pi}{T_s}=200\pi\,\mathrm{rad}\,\mathrm{s}^{-1}\)，仍不能满足对完整方波无失真恢复所需的采样定理。</p>
<p>有限宽周期脉冲列可表示为 \(s(t)=\sum_k\operatorname{rect}((t-kT_s)/\tau)\)。其频谱及采样后频谱分别为：</p>
<div class="formula">\[S(\omega)=2\pi\frac{\tau}{T_s}\sum_{k=-\infty}^{\infty}\operatorname{Sa}\!\left(\frac{k\omega_s\tau}{2}\right)\delta(\omega-k\omega_s),\]</div>
<div class="formula">\[X_s(\omega)=\frac{\tau}{T_s}\sum_{k=-\infty}^{\infty}\operatorname{Sa}\!\left(\frac{k\omega_s\tau}{2}\right)X(\omega-k\omega_s).\]</div>
<p>可见有限宽采样会使各频谱副本乘上 \(\operatorname{Sa}\) 型权重：副本越远，幅度一般越受脉冲宽度的影响。</p>
''' + _pulse_sampling_spectrum_svg() + r'''<p>若采样信号改为理想冲激序列 \(s_\delta(t)=\sum_k\delta(t-kT_s)\)，则：</p>
<div class="formula">\[S_\delta(\omega)=\frac{2\pi}{T_s}\sum_{k=-\infty}^{\infty}\delta(\omega-k\omega_s),\qquad X_{s,\delta}(\omega)=\frac{1}{T_s}\sum_{k=-\infty}^{\infty}X(\omega-k\omega_s).\]</div>
<p>与有限宽脉冲采样相比，理想冲激采样的各副本不带 \(\operatorname{Sa}\) 包络；二者都会因原方波的无限谐波而发生频谱重叠，故均不能据此无失真恢复完整方波。</p>
</section>'''
