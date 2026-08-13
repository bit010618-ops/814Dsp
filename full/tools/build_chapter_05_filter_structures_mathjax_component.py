"""Chapter-five digital-filter structure body, without training material."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}
h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}
p{margin:5pt 0 8pt;orphans:3;widows:3}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt}.table th,.table td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:left;vertical-align:top}.table th{color:#315d7c;font-weight:500;background:#f4f7f8}
.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}
.structure-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.structure-svg .wire{fill:none;stroke:#174b73;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}.structure-svg .block{fill:#f4f7f8;stroke:#0d8794;stroke-width:2}.structure-svg .sum{fill:#fff;stroke:#174b73;stroke-width:2.4}.structure-svg .branch{fill:#174b73}.structure-svg .label{fill:#315d7c;font:16px "Microsoft YaHei",sans-serif}.structure-svg .math-label div{height:100%;display:flex;align-items:center;justify-content:center;color:#172b3a;font-size:17px;white-space:nowrap;overflow:visible}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.table{font-size:9.5pt}}
</style>"""


def _math(x: float, y: float, width: float, text: str) -> str:
    if text in {"h(N-2)", "h(N-1)"}:
        x -= 11
        width = 80
    return f'<foreignObject class="math-label" x="{x}" y="{y}" width="{width}" height="34"><div xmlns="http://www.w3.org/1999/xhtml">\\({text}\\)</div></foreignObject>'


def iir_direct_form_svg() -> str:
    """Formal direct-I layout: two complete delay chains and a standard summer."""
    return f'''<svg class="structure-svg" data-diagram="iir-direct-form-i" viewBox="0 0 900 340" role="img" aria-label="IIR 直接 I 型结构图"><defs><marker id="d1" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs><text class="label" x="450" y="34" text-anchor="middle">直接 I 型：前向延时链与反馈延时链</text><path class="wire" marker-end="url(#d1)" d="M55 112H150"/><path class="wire" marker-end="url(#d1)" d="M150 112H245"/><path class="wire" marker-end="url(#d1)" d="M245 112H340"/><path class="wire" marker-end="url(#d1)" d="M340 112H540"/><path class="wire" marker-end="url(#d1)" d="M610 112H830"/><circle class="sum" cx="575" cy="112" r="35"/><text class="label" x="575" y="119" text-anchor="middle">Σ</text><circle class="branch" cx="150" cy="112" r="4"/><circle class="branch" cx="245" cy="112" r="4"/><circle class="branch" cx="340" cy="112" r="4"/><path class="wire" d="M150 112V184H540"/><path class="wire" d="M245 112V210H540"/><path class="wire" d="M340 112V236H540"/><path class="wire" marker-end="url(#d1)" d="M745 112V280H475"/><path class="wire" marker-end="url(#d1)" d="M475 280V147H548"/><path class="wire" marker-end="url(#d1)" d="M665 112V305H410"/><path class="wire" marker-end="url(#d1)" d="M410 305V138H544"/><rect class="block" x="173" y="165" width="56" height="38" rx="4"/><rect class="block" x="268" y="191" width="56" height="38" rx="4"/><rect class="block" x="363" y="217" width="56" height="38" rx="4"/><rect class="block" x="475" y="261" width="72" height="38" rx="4"/><rect class="block" x="410" y="286" width="72" height="38" rx="4"/>{_math(34,77,50,'x(n)')}{_math(817,77,55,'y(n)')}{_math(120,76,60,'z^{-1}')}{_math(215,76,60,'z^{-1}')}{_math(310,76,60,'z^{-1}')}{_math(174,166,54,'b_1')}{_math(269,192,54,'b_2')}{_math(364,218,54,'b_M')}{_math(483,262,58,'-a_1')}{_math(418,287,58,'-a_N')}</svg>'''


def iir_cascade_svg() -> str:
    """Formal cascade realization: identical second-order blocks in a left-to-right chain."""
    return f'''<svg class="structure-svg" data-diagram="iir-cascade-form" viewBox="0 0 900 250" role="img" aria-label="IIR 二阶节级联结构图"><defs><marker id="cascade-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs><text class="label" x="450" y="34" text-anchor="middle">IIR 二阶节级联结构</text><path class="wire" marker-end="url(#cascade-arrow)" d="M55 130H165"/><rect class="block" x="165" y="84" width="155" height="92" rx="6"/><path class="wire" marker-end="url(#cascade-arrow)" d="M320 130H382"/><rect class="block" x="382" y="84" width="155" height="92" rx="6"/><path class="wire" marker-end="url(#cascade-arrow)" d="M537 130H599"/><rect class="block" x="599" y="84" width="155" height="92" rx="6"/><path class="wire" marker-end="url(#cascade-arrow)" d="M754 130H846"/><text class="label" x="351" y="137" text-anchor="middle">⋯</text>{_math(22,95,70,'x(n)')}{_math(185,102,115,'H_1(z)')}{_math(402,102,115,'H_2(z)')}{_math(619,102,115,'H_R(z)')}{_math(808,95,68,'y(n)')}<text class="label" x="242" y="160" text-anchor="middle">二阶节</text><text class="label" x="459" y="160" text-anchor="middle">二阶节</text><text class="label" x="676" y="160" text-anchor="middle">二阶节</text></svg>'''


def fir_direct_form_svg() -> str:
    """Complete transversal FIR: delay line, taps, gains, and the final summer."""
    return f'''<svg class="structure-svg" data-diagram="fir-direct-form" viewBox="0 0 900 360" role="img" aria-label="FIR 抽头延迟线直接型结构图"><defs><marker id="fir-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs><text class="label" x="450" y="34" text-anchor="middle">FIR 抽头延迟线直接型结构</text><path class="wire" marker-end="url(#fir-arrow)" d="M52 100H170"/><path class="wire" marker-end="url(#fir-arrow)" d="M170 100H300"/><path class="wire" marker-end="url(#fir-arrow)" d="M300 100H430"/><path class="wire" marker-end="url(#fir-arrow)" d="M430 100H560"/><path class="wire" marker-end="url(#fir-arrow)" d="M560 100H690"/><circle class="branch" cx="82" cy="100" r="4"/><circle class="branch" cx="170" cy="100" r="4"/><circle class="branch" cx="300" cy="100" r="4"/><circle class="branch" cx="430" cy="100" r="4"/><circle class="branch" cx="560" cy="100" r="4"/><circle class="branch" cx="690" cy="100" r="4"/><rect class="block" x="184" y="74" width="74" height="52" rx="5"/><rect class="block" x="314" y="74" width="74" height="52" rx="5"/><rect class="block" x="574" y="74" width="74" height="52" rx="5"/><path class="wire" d="M82 100V170"/><path class="wire" d="M170 100V170"/><path class="wire" d="M300 100V170"/><path class="wire" d="M430 100V170"/><path class="wire" d="M560 100V170"/><path class="wire" d="M690 100V170"/><rect class="block" x="55" y="170" width="56" height="42" rx="4"/><rect class="block" x="143" y="170" width="56" height="42" rx="4"/><rect class="block" x="273" y="170" width="56" height="42" rx="4"/><rect class="block" x="403" y="170" width="56" height="42" rx="4"/><rect class="block" x="533" y="170" width="56" height="42" rx="4"/><rect class="block" x="663" y="170" width="56" height="42" rx="4"/><path class="wire" d="M83 212V262H754"/><path class="wire" d="M171 212V262"/><path class="wire" d="M301 212V262"/><path class="wire" d="M431 212V262"/><path class="wire" d="M561 212V262"/><path class="wire" d="M691 212V262"/><circle class="sum" cx="790" cy="262" r="32"/><text class="label" x="790" y="270" text-anchor="middle">Σ</text><path class="wire" marker-end="url(#fir-arrow)" d="M822 262H858"/>{_math(20,65,60,'x(n)')}{_math(190,82,62,'z^{-1}')}{_math(320,82,62,'z^{-1}')}{_math(580,82,62,'z^{-1}')}{_math(54,174,58,'h(0)')}{_math(142,174,58,'h(1)')}{_math(272,174,58,'h(2)')}{_math(402,174,58,'h(m)')}{_math(532,174,58,'h(N-2)')}{_math(662,174,58,'h(N-1)')}{_math(835,228,58,'y(n)')}<text class="label" x="490" y="105" text-anchor="middle">⋯</text><text class="label" x="490" y="198" text-anchor="middle">⋯</text></svg>'''


def dtmf_parallel_svg() -> str:
    return f'''<svg class="structure-svg" data-diagram="dtmf-parallel-form" viewBox="0 0 900 330" role="img" aria-label="双音多频并联谐振器结构图"><defs><marker id="d2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs><text class="label" x="450" y="34" text-anchor="middle">双音多频信号的两支路并联谐振器</text><path class="wire" marker-end="url(#d2)" d="M58 165H150V98H240"/><path class="wire" marker-end="url(#d2)" d="M150 165V232H240"/><circle class="branch" cx="150" cy="165" r="5"/><rect class="block" x="240" y="65" width="180" height="66" rx="6"/><rect class="block" x="240" y="199" width="180" height="66" rx="6"/><path class="wire" marker-end="url(#d2)" d="M420 98H555V145H562"/><path class="wire" marker-end="url(#d2)" d="M420 232H555V185H562"/><circle class="sum" cx="595" cy="165" r="33"/><text class="label" x="595" y="172" text-anchor="middle">Σ</text><path class="wire" marker-end="url(#d2)" d="M628 165H838"/><text class="label" x="330" y="92" text-anchor="middle">谐振支路 1</text><text class="label" x="330" y="226" text-anchor="middle">谐振支路 2</text>{_math(0,130,120,'x(n)=\\delta(n)')}{_math(255,94,150,'H_1(z)')}{_math(255,228,150,'H_2(z)')}{_math(800,130,68,'y(n)')}{_math(438,67,100,'\\omega_1')}{_math(438,240,100,'\\omega_2')}</svg>'''


def fir_cascade_svg() -> str:
    return f'''<svg class="structure-svg" data-diagram="fir-cascade-form" viewBox="0 0 900 230" role="img" aria-label="FIR 二阶节级联型结构图"><defs><marker id="d3" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs><text class="label" x="450" y="32" text-anchor="middle">FIR 二阶节级联型结构</text><path class="wire" marker-end="url(#d3)" d="M60 120H170"/><rect class="block" x="170" y="75" width="150" height="90" rx="6"/><path class="wire" marker-end="url(#d3)" d="M320 120H385"/><rect class="block" x="385" y="75" width="150" height="90" rx="6"/><path class="wire" marker-end="url(#d3)" d="M535 120H600"/><rect class="block" x="600" y="75" width="150" height="90" rx="6"/><path class="wire" marker-end="url(#d3)" d="M750 120H842"/><text class="label" x="353" y="128" text-anchor="middle">⋯</text>{_math(25,85,65,'x(n)')}{_math(195,100,100,'H_1(z)')}{_math(410,100,100,'H_2(z)')}{_math(625,100,100,'H_{N/2}(z)')}{_math(808,85,65,'y(n)')}</svg>'''


def frequency_sampling_svg() -> str:
    return f'''<svg class="structure-svg" data-diagram="frequency-sampling-form" viewBox="0 0 900 270" role="img" aria-label="频率采样型 FIR 插值结构图"><defs><marker id="d4" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs><text class="label" x="450" y="32" text-anchor="middle">频率采样型 FIR 的梳状滤波器与谐振器柜</text><path class="wire" marker-end="url(#d4)" d="M55 140H185"/><rect class="block" x="185" y="102" width="155" height="76" rx="6"/><path class="wire" marker-end="url(#d4)" d="M340 140H440"/><rect class="block" x="440" y="78" width="220" height="124" rx="6"/><path class="wire" marker-end="url(#d4)" d="M660 140H842"/><text class="label" x="262" y="132" text-anchor="middle">梳状滤波器</text><text class="label" x="550" y="121" text-anchor="middle">N 个一阶谐振器</text><text class="label" x="550" y="157" text-anchor="middle">并联组成谐振器柜</text>{_math(20,106,70,'x(n)')}{_math(202,145,120,'H_1(z)=1-z^{-N}')}{_math(458,172,185,'\\frac{1}{N}\\sum_{k=0}^{N-1}H_k(z)')}{_math(800,106,70,'y(n)')}</svg>'''


def fast_convolution_svg() -> str:
    return f'''<svg class="structure-svg" data-diagram="fast-convolution-form" viewBox="0 0 900 310" role="img" aria-label="快速卷积型 FIR 结构框图"><defs><marker id="d5" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs><text class="label" x="450" y="30" text-anchor="middle">FFT 快速卷积结构</text><path class="wire" marker-end="url(#d5)" d="M58 98H135"/><rect class="block" x="135" y="65" width="130" height="66" rx="5"/><path class="wire" marker-end="url(#d5)" d="M265 98H350"/><rect class="block" x="350" y="65" width="120" height="66" rx="5"/><path class="wire" marker-end="url(#d5)" d="M470 98H565V132H615"/><path class="wire" marker-end="url(#d5)" d="M58 214H135"/><rect class="block" x="135" y="181" width="130" height="66" rx="5"/><path class="wire" marker-end="url(#d5)" d="M265 214H350"/><rect class="block" x="350" y="181" width="120" height="66" rx="5"/><path class="wire" marker-end="url(#d5)" d="M470 214H565V158H615"/><circle class="sum" cx="650" cy="145" r="28"/><text class="label" x="650" y="152" text-anchor="middle">×</text><path class="wire" marker-end="url(#d5)" d="M678 145H730"/><rect class="block" x="730" y="112" width="105" height="66" rx="5"/><path class="wire" marker-end="url(#d5)" d="M835 145H880"/><text class="label" x="200" y="104" text-anchor="middle">补零至 L 点</text><text class="label" x="410" y="104" text-anchor="middle">L 点 FFT</text><text class="label" x="200" y="220" text-anchor="middle">补零至 L 点</text><text class="label" x="410" y="220" text-anchor="middle">L 点 FFT</text><text class="label" x="782" y="151" text-anchor="middle">L 点 IFFT</text>{_math(15,63,70,'x(n)')}{_math(15,180,70,'h(n)')}{_math(848,110,52,'y(n)')}</svg>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>第五章 数字滤波器结构</h1>

<h2>5.1 数字滤波器概述</h2>
<p>数字滤波器是由差分方程描述的一类特殊离散时间系统。它以输入序列为对象，经确定的运算关系得到输出序列；不同的运算安排决定不同的实现结构。对线性时不变系统，时域卷积与频域相乘分别给出滤波的两种等价描述：</p>
<div class="formula">\[
\begin{aligned}
y(n)&=x(n)*h(n),\\
Y\!\left(e^{j\omega}\right)&=H\!\left(e^{j\omega}\right)X\!\left(e^{j\omega}\right).
\end{aligned}
\]</div>
<p>设计指标通常在频域给出：需要保留的频段应使 [[\left|H(e^{j\omega})\right|]] 接近所要求增益，需要抑制的频段则应使其足够小。实际结构不能只看理想频响，还要同时考虑运算量、存储量、有限字长误差、稳定性、参数控制能力与模块化实现的便利性。</p>

<h3>结构表示与基本运算单元</h3>
<p>滤波器可用方框图或信号流图表示。所有基本结构均由三种运算组合而成：相加、乘以常数和单位延时。离散系统中单位延时器的系统函数为 [[z^{-1}]]；连成延时链后，每一个抽头对应不同的历史样本。</p>
<table class="table"><thead><tr><th>单元</th><th>作用</th><th>书写约定</th></tr></thead><tbody>
<tr><td>加法器</td><td>汇总多条信号支路</td><td>输入端的正负号必须明确。</td></tr>
<tr><td>乘法器</td><td>施加系数或增益</td><td>系数与所属支路一一对应。</td></tr>
<tr><td>单位延时器</td><td>将序列延迟一个采样间隔</td><td>使用 [[z^{-1}]] 表示。</td></tr>
</tbody></table>

<h3>研究结构的意义</h3>
<p>FIR 与 IIR 的冲激响应特性决定了它们具有不同的实现结构；同一传输函数的不同结构所需的存储单元和乘法次数不同，因而影响复杂度与运算速度。有限字长条件下，各种结构的量化误差、溢出敏感性和稳定性也不同。好的结构还应便于性能控制、模块化实现和时分复用。</p>

<h2>5.2 IIR 数字滤波器结构</h2>
<p>IIR 滤波器的单位冲激响应为无限长序列，有限 [[z]] 平面内存在极点；因果稳定实现要求所有极点位于单位圆内。由于输出的历史样本参与当前计算，IIR 结构具有反馈，是递归结构。</p>
<div class="formula">\[
H(z)=\frac{\sum_{m=0}^{M}b_m z^{-m}}{1+\sum_{n=1}^{N}a_n z^{-n}},
\qquad
y(n)=\sum_{m=0}^{M}b_m x(n-m)-\sum_{n=1}^{N}a_n y(n-n).
\]</div>

<h3>直接 I 型与直接 II 型</h3>
<p>直接 I 型按差分方程直接实现：输入 [[x(n)]] 经 [[M]] 节延时链形成横向前向网络，输出 [[y(n)]] 经 [[N]] 节延时链形成反馈网络。它的信号意义最直观，但需要两条延时链。</p>
<figure>
__IIR_DIRECT_FORM__
<figcaption>图 5-1 IIR 直接 I 型结构</figcaption>
</figure>
<p>直接 II 型把两条延时链合并为共享状态延时链，因此在通常的 [[M=N]] 情形下延时单元数可由 [[M+N]] 降至 [[\max(M,N)]]。合并虽节省存储，却使内部状态的动态范围和有限字长效应更值得注意。</p>
<p>令共享延时链的输出为内部状态 [[w(n)]]，直接 II 型的两步计算为：</p>
<div class="formula">\[
\begin{aligned}
w(n)&=x(n)-\sum_{r=1}^{N}a_r w(n-r),\\
y(n)&=\sum_{m=0}^{M}b_m w(n-m).
\end{aligned}
\]</div>
<p>这两式表明直接 II 型并没有改变原系统函数；它只是把输入历史和输出历史所需的两条延时链，改写为同一条状态延时链。</p>

<table class="table"><thead><tr><th>直接型</th><th>延时单元</th><th>特点</th></tr></thead><tbody>
<tr><td>直接 I 型</td><td>[[M+N]]</td><td>前向横向网络和反馈网络各保留一条延时链，信号意义直观。</td></tr>
<tr><td>直接 II 型</td><td>[[\max(M,N)]]</td><td>共享延时链，延时数最少，故称典范型；内部状态动态范围需要特别检查。</td></tr>
</tbody></table>
<p>直接型由差分方程直接得到，便于理解，但系数不直接对应单个零极点，极点又可能对系数变化敏感。因此在高阶或窄带系统中，不能仅因为“直接型最简单”就忽略有限字长下的性能风险。</p>

<h3>级联型、并联型与转置型 IIR 结构</h3>
<p>级联型将系统函数按实系数一阶或二阶因子分解，每个二阶节承担一对实根或共轭复根，主信号从左到右顺次通过各节：</p>
<div class="formula">\[
H(z)=A\prod_{r=1}^{R}
\frac{1+\beta_{1r}z^{-1}+\beta_{2r}z^{-2}}
{1+\alpha_{1r}z^{-1}+\alpha_{2r}z^{-2}}.
\]</div>
<p>这种安排便于按零极点控制各节特性，也便于对每节单独缩放。并联型则对部分分式展开，把同一输入分到若干支路，支路输出在求和节点汇总；它特别适合由若干谐振节叠加构造频率选择性。转置型来自实系数 LSI 流图：将所有支路方向反转、支路增益不变，并交换输入输出位置，传输函数保持不变。</p>
<p>选择 IIR 结构时，不能只看“实现了同一个 [[H(z)]]”。同一系统函数的不同结构在溢出敏感度、量化误差、极限环、内部状态幅度与调试便利性上都可能不同。</p>
<figure>
__IIR_CASCADE__
<figcaption>图 5-2 IIR 二阶节级联结构</figcaption>
</figure>

<h3>应用：双音多频信号</h3>
<p>电话按键的双音多频（DTMF）信号由一个低频组和一个高频组中的两个正弦分量叠加而成。并联型结构可把单位冲激输入分别送入两个二阶谐振支路，再在求和节点合成输出；各支路的极点位置直接决定所选频率。该例说明并联型便于控制极点，适合谐振器叠加，但不适合需要精确控制传输零点的陷波或窄带带阻滤波器。</p>
<figure>
__DTMF_PARALLEL__
<figcaption>图 5-3 并联型结构示例：双音多频信号</figcaption>
</figure>

<h2>5.3 FIR 数字滤波器结构</h2>
<p>FIR 滤波器的单位冲激响应只在有限个样点非零。因果 FIR 的 [[H(z)]] 只含有限次 [[z^{-1}]] 多项式，极点全部位于 [[z=0]]，因此本身稳定；常见直接实现没有输出到输入的反馈。</p>
<div class="formula">\[
H(z)=\sum_{n=0}^{N-1}h(n)z^{-n},
\qquad
y(n)=\sum_{m=0}^{N-1}h(m)x(n-m).
\]</div>

<h3>抽头延迟线直接型</h3>
<p>直接型又称横向滤波器或抽头延迟线结构：输入依次通过 [[z^{-1}]] 延时链，每个抽头乘以 [[h(m)]] 后相加。优点是简单、直观、运算速度快，且系数就是冲激响应样值；不足是不能直接把零点以分节方式控制。</p>
<figure>
__FIR_DIRECT_FORM__
<figcaption>图 5-4 FIR 抽头延迟线直接型结构</figcaption>
</figure>

<h3>FIR 级联型、频率抽样型与谐振器型</h3>
<p>当需要控制传输零点时，可将 [[H(z)]] 分解为实系数一阶或二阶因子并级联实现。与直接型相比，级联型通常需要更多系数和乘法，但零点控制更方便。频率抽样型从有限个频率样值出发构造系统，适合频率取样设计；谐振器型可由多个谐振单元并联形成，梳状滤波器中的零点与各谐振支路极点之间的抵消关系必须逐项检查。</p>
<figure>
__FIR_CASCADE__
<figcaption>图 5-5 FIR 二阶节级联型结构</figcaption>
</figure>

<h3>频率采样型的插值结构</h3>
<p>对单位圆上的 [[N]] 个频率样值 [[H(k)]]，频率采样型可直接写成下列插值形式：</p>
<div class="formula">\[
H(z)=\left(1-z^{-N}\right)\frac{1}{N}
\sum_{k=0}^{N-1}\frac{H(k)}{1-W_N^{-k}z^{-1}}.
\]</div>
<div class="formula">\[
H(z)=H_1(z)\frac{1}{N}\sum_{k=0}^{N-1}H_k(z),
\qquad
H_1(z)=1-z^{-N},
\qquad
H_k(z)=\frac{H(k)}{1-W_N^{-k}z^{-1}}.
\]</div>
<p>其中 [[H_1(z)]] 是梳状滤波器，后级为由 [[N]] 个一阶谐振器组成的谐振器柜；梳状滤波器的每个单位圆零点会与对应谐振支路的极点相抵消，从而实现所给的频率样值。</p>
<figure>
__FREQUENCY_SAMPLING__
<figcaption>图 5-6 频率采样型 FIR 滤波器的插值结构</figcaption>
</figure>

<p>频率采样结构由梳状滤波器和谐振器柜级联组成。对 [[N]] 个频率采样值 [[H(k)]]，可用 IDFT 关系构造有限长冲激响应：</p>
<div class="formula">\[
h(n)=\frac{1}{N}\sum_{k=0}^{N-1}H(k)e^{j2\pi kn/N}.
\]</div>
<p>该结构特别适合只有少数 [[H(k)]] 非零的窄带滤波器。其缺点是谐振器支路系数通常为复数，并且有限字长会使单位圆上的极点偏离，从而带来稳定性风险。修正方法是把梳状滤波器零点与谐振器极点同时移到半径 [[r\leq1]]、且接近单位圆的圆上，以换取稳健性。</p>
<p>修正后在半径 [[r]] 的圆上取样，系统函数与谐振器极点分别为：</p>
<div class="formula">\[
H_r(z)=\left(1-r^N z^{-N}\right)\frac{1}{N}
\sum_{k=0}^{N-1}\frac{H_r(k)}{1-rW_N^{-k}z^{-1}},
\qquad
z_k=re^{j2\pi k/N}.
\]</div>
<p>当 [[r]] 足够接近 [[1]] 时，修正圆上的频率样值 [[H_r(k)]] 近似原来的 [[H(k)]]；而全部谐振器极点已落在单位圆内，有限字长实现的稳定性更可靠。</p>

<h3>快速卷积型结构</h3>
<p>若输入的非零长度为 [[M]]、FIR 冲激响应的非零长度为 [[N]]，线性卷积输出长度为：</p>
<div class="formula">\[
L=M+N-1.
\]</div>
<p>将两个序列分别补零到 [[L]] 点后进行 [[L]] 点 FFT，相乘并作 [[L]] 点 IFFT，即可用圆周卷积等价地得到线性卷积。长序列处理中还应结合重叠相加法或重叠保留法分块，保证每一块的 FFT 长度避免循环混叠。</p>
<figure>
__FAST_CONVOLUTION__
<figcaption>图 5-7 快速卷积型 FIR 滤波器结构</figcaption>
</figure>

<h3>线性相位型结构</h3>
<p>线性相位 FIR 的冲激响应关于中心点满足偶对称或奇对称：</p>
<div class="formula">\[
\begin{cases}
h(n)=h(N-1-n), & \text{偶对称},\\
h(n)=-h(N-1-n), & \text{奇对称},
\end{cases}
\qquad 0\leq n\leq N-1.
\]</div>
<p>对称性允许将关于中心成对的抽头先相加或相减，再乘共同系数，从而减少乘法次数。[[N]] 为奇数和偶数时中心抽头的处理不同；偶对称对应加法组合，奇对称对应减法组合。线性相位（及广义线性相位）系统具有常数群延迟，能在不过度扭曲波形形状的前提下完成频率选择。</p>
<p>令 [[N=2L+1]]。除中心抽头外，成对样本的实现可统一为：</p>
<div class="formula">\[
\begin{aligned}
y(n)={}&\sum_{m=0}^{L-1}h(m)\left[x(n-m)\pm x(n-2L+m)\right]\\
&+h(L)x(n-L).
\end{aligned}
\]</div>
<p>其中偶对称取加号；奇对称取减号，且奇对称时 [[h(L)=0]]，所以中心支路不参与输出。令 [[N=2L]] 时没有中心抽头，全部项均为成对组合：</p>
<div class="formula">\[
y(n)=\sum_{m=0}^{L-1}h(m)\left[x(n-m)\pm x(n-2L+1+m)\right].
\]</div>
<p>两种长度下都先完成对称样本的加法或减法，再乘以一组独立系数；这正是线性相位 FIR 结构能够减少乘法器数量的原因。</p>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    content = (content
        .replace("__IIR_DIRECT_FORM__", iir_direct_form_svg())
        .replace("__IIR_CASCADE__", iir_cascade_svg())
        .replace("__FIR_DIRECT_FORM__", fir_direct_form_svg())
        .replace("__DTMF_PARALLEL__", dtmf_parallel_svg())
        .replace("__FIR_CASCADE__", fir_cascade_svg())
        .replace("__FREQUENCY_SAMPLING__", frequency_sampling_svg())
        .replace("__FAST_CONVOLUTION__", fast_convolution_svg()))
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
