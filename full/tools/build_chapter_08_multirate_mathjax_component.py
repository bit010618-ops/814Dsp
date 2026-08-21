"""Chapter-eight multirate DSP body, excluding source-code exercises."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt;orphans:3;widows:3}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt}.table th,.table td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:left;vertical-align:top}.table th{color:#315d7c;font-weight:500;background:#f4f7f8}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.table{font-size:9.5pt}}</style>"""


DIAGRAM_STYLE = r'''<style>
.multirate-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.multirate-svg .wire{fill:none;stroke:#174b73;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
.multirate-svg .block{fill:#f4f7f8;stroke:#0d8794;stroke-width:2}.multirate-svg .label{fill:#315d7c;font:17px "Microsoft YaHei",sans-serif}.multirate-svg .annotation{fill:#587083;font:14px "Microsoft YaHei",sans-serif}.multirate-svg .axis{fill:none;stroke:#315d7c;stroke-width:1.7;stroke-linecap:round}.multirate-svg .spectrum-a{fill:none;stroke:#0d8794;stroke-width:2.4;stroke-linejoin:round}.multirate-svg .spectrum-b{fill:none;stroke:#b56b2e;stroke-width:2.4;stroke-linejoin:round}.multirate-svg .panel{fill:#fff;stroke:#d8e0e5;stroke-width:1.2}.multirate-svg .math-label div{height:100%;display:flex;align-items:center;justify-content:center;color:#172b3a;font-size:17px;white-space:nowrap;overflow:visible}
</style>'''


def _math(x: float, y: float, width: float, text: str, height: float = 32) -> str:
    return f'<foreignObject class="math-label" x="{x}" y="{y}" width="{width}" height="{height}"><div xmlns="http://www.w3.org/1999/xhtml">\\({text}\\)</div></foreignObject>'


def _arrow(marker: str) -> str:
    return f'<defs><marker id="{marker}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs>'


def decimation_spectrum_svg() -> str:
    """Clean four-stage frequency-domain relationship for twofold decimation."""
    return f'''<svg class="multirate-svg" id="decimation-spectrum-transform" viewBox="0 0 900 510" role="img" aria-label="二倍抽取的频谱移位、求和、降幅和拉伸关系">{_arrow('dec-spectrum-arrow')}
<text class="label" x="450" y="32" text-anchor="middle">二倍抽取的频谱变换过程</text>
<rect class="panel" x="48" y="66" width="340" height="160" rx="5"/><rect class="panel" x="512" y="66" width="340" height="160" rx="5"/><rect class="panel" x="512" y="282" width="340" height="160" rx="5"/><rect class="panel" x="48" y="282" width="340" height="160" rx="5"/>
<text class="annotation" x="218" y="91" text-anchor="middle">原频谱</text><text class="annotation" x="682" y="91" text-anchor="middle">移位并求和</text><text class="annotation" x="682" y="307" text-anchor="middle">幅度缩小为一半</text><text class="annotation" x="218" y="307" text-anchor="middle">拉伸后频谱</text>
<path class="axis" marker-end="url(#dec-spectrum-arrow)" d="M82 195H352"/><path class="axis" marker-end="url(#dec-spectrum-arrow)" d="M546 195H816"/><path class="axis" marker-end="url(#dec-spectrum-arrow)" d="M546 411H816"/><path class="axis" marker-end="url(#dec-spectrum-arrow)" d="M82 411H352"/>
<path class="axis" marker-end="url(#dec-spectrum-arrow)" d="M96 195V112"/><path class="axis" marker-end="url(#dec-spectrum-arrow)" d="M560 195V112"/><path class="axis" marker-end="url(#dec-spectrum-arrow)" d="M560 411V328"/><path class="axis" marker-end="url(#dec-spectrum-arrow)" d="M96 411V328"/>
<text class="annotation" x="102" y="126">幅度</text><text class="annotation" x="566" y="126">幅度</text><text class="annotation" x="566" y="342">幅度</text><text class="annotation" x="102" y="342">幅度</text>
<path class="spectrum-a" d="M96 195L130 142L164 195M190 195L220 119L250 195M276 195L310 142L344 195"/>
<path class="spectrum-a" d="M560 195L590 142L620 195M668 195L698 142L728 195M776 195L806 142L836 195"/><path class="spectrum-b" d="M614 195L644 142L674 195M722 195L752 142L782 195"/>
<path class="spectrum-a" d="M560 411L590 359L620 411M668 411L698 359L728 411M776 411L806 359L836 411"/><path class="spectrum-b" d="M614 411L644 359L674 411M722 411L752 359L782 411"/>
<path class="spectrum-a" d="M96 411L130 359L164 411M190 411L220 335L250 411M276 411L310 359L344 411"/>
<path class="wire" marker-end="url(#dec-spectrum-arrow)" d="M405 145H493"/><text class="annotation" x="449" y="132" text-anchor="middle">移位、求和</text><path class="wire" marker-end="url(#dec-spectrum-arrow)" d="M682 237V268"/><text class="annotation" x="697" y="257">降幅</text><path class="wire" marker-end="url(#dec-spectrum-arrow)" d="M495 362H405"/><text class="annotation" x="450" y="349" text-anchor="middle">拉伸</text>
{_math(95,198,250,'-2\\pi\\quad -\\pi\\quad 0\\quad \\pi\\quad 2\\pi')}{_math(562,198,250,'-2\\pi\\quad -\\pi\\quad 0\\quad \\pi\\quad 2\\pi')}{_math(562,414,250,'-2\\pi\\quad -\\pi\\quad 0\\quad \\pi\\quad 2\\pi')}{_math(95,414,250,'-2\\pi\\quad -\\pi\\quad 0\\quad \\pi\\quad 2\\pi')}
</svg>'''


def decimator_svg() -> str:
    return f'''<svg class="multirate-svg" id="decimator-cascade" viewBox="0 0 900 260" role="img" aria-label="抗混叠滤波器与M倍抽取器级联结构">{_arrow('decimator-arrow')}
<text class="label" x="450" y="34" text-anchor="middle">抗混叠滤波与抽取器的级联结构</text><path class="wire" marker-end="url(#decimator-arrow)" d="M70 132H212"/><rect class="block" x="212" y="87" width="180" height="90" rx="6"/><path class="wire" marker-end="url(#decimator-arrow)" d="M392 132H493"/><rect class="block" x="493" y="87" width="104" height="90" rx="45"/><path class="wire" marker-end="url(#decimator-arrow)" d="M597 132H828"/>
{_math(26,91,95,'x(n)')}{_math(233,103,138,'h_d(n)')}{_math(507,103,75,'\\downarrow M')}{_math(780,91,88,'x_d(n)')}<text class="annotation" x="72" y="174">采样率：f_s</text><text class="annotation" x="236" y="201">抗混叠低通滤波器</text><text class="annotation" x="725" y="174">采样率：f_s/M</text></svg>'''


def interpolator_svg() -> str:
    return f'''<svg class="multirate-svg" id="interpolator-cascade" viewBox="0 0 900 260" role="img" aria-label="L倍上采样器与抗镜像滤波器级联结构">{_arrow('interpolator-arrow')}
<text class="label" x="450" y="34" text-anchor="middle">插零与插值低通滤波器的级联结构</text><path class="wire" marker-end="url(#interpolator-arrow)" d="M70 132H210"/><rect class="block" x="210" y="87" width="104" height="90" rx="45"/><path class="wire" marker-end="url(#interpolator-arrow)" d="M314 132H418"/><rect class="block" x="418" y="87" width="190" height="90" rx="6"/><path class="wire" marker-end="url(#interpolator-arrow)" d="M608 132H828"/>
{_math(26,91,95,'x(n)')}{_math(224,103,75,'\\uparrow L')}{_math(444,103,138,'h_i(n)')}{_math(781,91,88,'x_i(n)')}<text class="annotation" x="72" y="174">采样率：f_s</text><text class="annotation" x="438" y="201">抗镜像插值低通滤波器</text><text class="annotation" x="722" y="174">采样率：L f_s</text></svg>'''


def rational_converter_svg() -> str:
    return f'''<svg class="multirate-svg" id="rational-rate-converter" viewBox="0 0 900 300" role="img" aria-label="L比M有理数倍采样率转换及多级分解结构">{_arrow('rational-arrow')}
<text class="label" x="450" y="34" text-anchor="middle">有理数倍采样率变换的标准结构</text><path class="wire" marker-end="url(#rational-arrow)" d="M60 142H178"/><rect class="block" x="178" y="96" width="100" height="92" rx="46"/><path class="wire" marker-end="url(#rational-arrow)" d="M278 142H380"/><rect class="block" x="380" y="96" width="170" height="92" rx="6"/><path class="wire" marker-end="url(#rational-arrow)" d="M550 142H650"/><rect class="block" x="650" y="96" width="100" height="92" rx="46"/><path class="wire" marker-end="url(#rational-arrow)" d="M750 142H844"/>
{_math(18,101,90,'x(n)')}{_math(191,112,74,'\\uparrow L')}{_math(400,111,130,'H(z)')}{_math(664,112,74,'\\downarrow M')}{_math(802,101,85,'x_d(n)')}<text class="annotation" x="465" y="219" text-anchor="middle">低通滤波器同时负责抗镜像与抗混叠</text>{_math(332,242,240,'f_s^\\prime=\\frac{L}{M}f_s')}</svg>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>第八章 多采样率数字信号处理</h1>
<p>多采样率处理研究同一系统中不同采样率信号的表示、变换和实现。它用于降低传输或运算速率、实现窄带滤波器、完成子带分解与重构，以及连接采样率不同的处理模块。核心原则是：任何改变采样率的操作都要同时检查频谱压缩、镜像、混叠和抗混叠滤波。</p>

<h2>多采样率处理的必要性</h2>
<p>数字传输系统需要能够传输多种采样率的信号，并自动完成采样率转换。音频处理中同时存在多种常用采样率，例如立体声音频常用 48 kHz、CD 音频使用 44.1 kHz、数字音频广播可使用 32 kHz。当数字信号在具有独立时钟的两个数字系统之间传递时，也必须按时钟差异转换采样率。</p>
<p>另一方面，采用不同频带的低通、带通和高通滤波器进行子带分解后，可以对各子带分别转换采样率并提取特征，以减少数据量、实现压缩；若原采样率过高，也应在满足带宽条件下适当降低采样率，消除冗余。因此，多采样率处理是采样率转换理论及其系统实现的统一基础。</p>

<h2>8.1 信号的整数倍抽取</h2>
<p>[[M]] 倍抽取使采样率降低为原来的 [[1/M]]，每隔 [[M]] 个样本取一个样本：</p>
<div class="formula">\[
y(n)=x(Mn),\qquad F_s'=\frac{F_s}{M}.
\]</div>
<p>时域抽取会使频谱在数字频率轴上压缩并叠加：</p>
<div class="formula">\[
Y\!\left(e^{j\omega}\right)=\frac{1}{M}
\sum_{r=0}^{M-1}X\!\left(e^{j(\omega-2\pi r)/M}\right).
\]</div>
<div class="formula">\[
X_d\!\left(e^{j\omega}\right)=\frac{1}{M}
\sum_{r=0}^{M-1}X\!\left(e^{j(\omega/M-2\pi r/M)}\right).
\]</div>
<div class="formula">\[
X_d\!\left(e^{j\omega}\right)=
\frac{1}{2}X\!\left(e^{j\omega/2}\right)+
\frac{1}{2}X\!\left(e^{j(\omega/2-\pi)}\right).
\]</div>
<figure class="source-figure compact"><img src="../assets/source-figures/ch08-decimation-spectrum.png" alt="二倍抽取时的频谱移位、求和与拉伸"><figcaption>图 8-1　二倍抽取的频谱变换过程</figcaption></figure>
<p>上式可看作将原频谱按 [[M]] 段分解、移位并相加后再缩放。故抽取后表现为频谱拉伸、移位、求和与幅度缩小。为避免相加后的谱副本重叠，必须满足</p>
<div class="formula">\[
X\!\left(e^{j\omega}\right)=0,\qquad \frac{\pi}{M}\leq\left|\omega\right|\leq\pi.
\]</div>
<div class="formula">\[
\begin{aligned}
H_d\!\left(e^{j\omega}\right)&=
\begin{cases}
1, & 0\leq\left|\omega\right|<\pi/M,\\
0, & \pi/M\leq\left|\omega\right|\leq\pi,
\end{cases}\\
w(n)&=\sum_{k=-\infty}^{\infty}h_d(k)x(n-k),\\
x_d(n)&=w(Mn).
\end{aligned}
\]</div>
<p>因此若原信号带宽未限制在 [[\pi/M]] 以内，抽取后会产生不可逆混叠。正确结构是先用抗混叠低通滤波器限制带宽，再接 [[\downarrow M]] 抽取器；不能把低通滤波器放在抽取之后当作补救。</p>
<figure class="source-figure compact"><img src="../assets/source-figures/ch08-decimator-structure.png" alt="抗混叠滤波器与抽取器级联结构"><figcaption>图 8-2　抗混叠滤波与抽取器的级联结构</figcaption></figure>

<h3>例题</h3>
<p>已知信号 [[x(n)]] 的取样频率 [[f_s=2f_h]]，[[f_h]] 为信号最高频率。设计一个将取样率降低到 [[1/8]] 的抽取器系统。</p>
<p>（1）画出系统框图，并注明系统中各信号的取样频率；（2）写出抗混叠滤波器的理想幅度响应；（3）用窗函数法设计一个 40 阶的抗混叠滤波器，采用汉宁窗；（4）写出系统的差分方程。</p>
<p>解：抽取因子为 [[M=8]]。系统按“抗混叠数字低通滤波器 [[\longrightarrow\downarrow 8]]”连接；输入采样率为 [[2f_h]]，输出采样率为 [[f_h/4]]。为保证抽取前的离散频谱不发生混叠，理想低通滤波器的截止角频率取</p>
<div class="formula">\[
\omega_c=\frac{\pi}{8},\qquad
\left|H_d\!\left(e^{j\omega}\right)\right|=
\begin{cases}
1, & \left|\omega\right|\leq\pi/8,\\
0, & \pi/8<\left|\omega\right|\leq\pi.
\end{cases}
\]</div>
<p>采用 40 阶汉宁窗设计时，先以该理想幅频响应求得长度为 41 的低通 FIR 单位脉冲响应 [[h_d(k)]]，再乘以同长度汉宁窗 [[w(k)]]，得到 [[h(k)=h_d(k)w(k)]]。滤波器输出与抽取输出依次为</p>
<div class="formula">\[
v(n)=\sum_{k=0}^{40}h(k)x(n-k),\qquad y(n)=v(8n).
\]</div>
<div class="formula">\[
\begin{aligned}
w(n)&=\frac{1}{2}\left[1-\cos\!\left(\frac{\pi n}{20}\right)\right]R_{41}(n),\\
h(n)&=\frac{\sin\!\left[\frac{\pi}{8}(n-20)\right]}{\pi(n-20)}
\cdot\frac{1}{2}\left[1-\cos\!\left(\frac{\pi n}{20}\right)\right]R_{41}(n),\\
x_d(n)&=\sum_{k=0}^{40}h(k)x(8n-k).
\end{aligned}
\]</div>

<h2>8.2 信号的整数倍内插</h2>
<p>[[L]] 倍内插使采样率提高 [[L]] 倍。第一步在相邻原样本间插入 [[L-1]] 个零：</p>
<div class="formula">\[
\begin{aligned}
y(n)&=\sum_{k=-\infty}^{\infty}x(k)\delta(n-kL),\\
x_p(n)&=\begin{cases}
x(n/L), & n=0,\ \pm L,\ \pm2L,\ldots,\\
0, & \text{其他 } n,
\end{cases}\\
F_s'&=LF_s.
\end{aligned}
\]</div>
<p>零插入不会自动产生新的平滑样本，而是在频域形成镜像谱：</p>
<div class="formula">\[
Y\!\left(e^{j\omega}\right)=X\!\left(e^{j\omega L}\right).
\]</div>
<div class="formula">\[
\begin{aligned}
H_i\!\left(e^{j\omega}\right)&=\begin{cases}
L, & 0\leq\left|\omega\right|<\pi/L,\\
0, & \pi/L\leq\left|\omega\right|\leq\pi,
\end{cases}\\
h_i(n)&=\frac{\sin(\pi n/L)}{\pi n/L}.
\end{aligned}
\]</div>
<p>随后必须使用插值低通滤波器去除镜像，并补偿增益。理想插值器在 [[|\omega|\leq\pi/L]] 内增益为 [[L]]，其他频段为零；这样可保留原谱并获得较高采样率序列。</p>
<p>将插零序列通过插值滤波器后，时域关系为卷积：</p>
<div class="formula">\[
x_i(n)=\sum_{k=-\infty}^{\infty}x(k)
\frac{\sin\!\left[\pi(n-kL)/L\right]}{\pi(n-kL)/L}.
\]</div>
<figure class="source-figure compact"><img src="../assets/source-figures/ch08-interpolator-structure.png" alt="上采样与插值低通滤波器的级联结构"><figcaption>图 8-3　插零与插值低通滤波器的级联结构</figcaption></figure>
<p>其中 [[h_i(n)]] 是抗影像滤波器的单位脉冲响应。插零本身并未完成平滑重构；只有低通滤波器去除额外的 [[L-1]] 个影像频谱后，内插后的样值才对应于所需的较高采样率信号。</p>

<h2>8.3 抽取与内插的频域关系</h2>
<p>抽取前的低通滤波器防止谱副本叠加，内插后的低通滤波器去除零插入产生的镜像。二者都是低通滤波器，但所处位置、目的和增益要求不同：前者的截止频率受抽取倍数限制，后者的截止频率受内插倍数限制并需补偿 [[L]] 倍幅度。</p>
<table class="table"><thead><tr><th>操作</th><th>时域效果</th><th>频域风险与滤波目的</th></tr></thead><tbody><tr><td>抽取 [[\downarrow M]]</td><td>按间隔取样，长度/采样率下降</td><td>频谱压缩并叠加；先低通以防混叠。</td></tr><tr><td>内插 [[\uparrow L]]</td><td>插零，采样率上升</td><td>频谱压缩后周期镜像；后低通以消除镜像并补偿增益。</td></tr></tbody></table>

<h2>8.4 有理数倍采样率变换与多相结构</h2>
<p>以先 [[L]] 倍内插、再 [[M]] 倍抽取实现 [[L/M]] 倍采样率变换，输入输出采样率满足：</p>
<div class="formula">\[
F_s'=\frac{L}{M}F_s.
\]</div>
<p>为避免不必要的运算，可把低通滤波器拆成多相分量。对抽取因子 [[M]]，多相展开写为：</p>
<div class="formula">\[
H(z)=\sum_{r=0}^{M-1}z^{-r}E_r\!\left(z^M\right).
\]</div>
<p>多相结构把原来会在抽取后丢弃的中间运算移除，并允许滤波器和采样率变换器交换位置或合并。实现时仍需逐项核对：上采样/下采样倍数、滤波器位置、各相位支路和输出采样率必须一致；任何一处颠倒都会改变频谱并造成混叠或镜像残留。</p>
<figure class="source-figure compact"><img src="../assets/source-figures/ch08-rational-converter.png" alt="L比M有理数倍采样率变换结构"><figcaption>图 8-4　有理数倍采样率变换的标准结构</figcaption></figure>

<h3>单级与多级采样频率变换</h3>
<p>单级有理数倍变换采用“[[\uparrow L]] [[\longrightarrow]] 低通滤波 [[\longrightarrow]] [[\downarrow M]]”的结构。低通滤波器同时承担抗影像和抗混叠任务；当 [[L]] 或 [[M]] 很大时，所需截止频率很低，滤波器阶数和计算量会显著增大。</p>
<div class="formula">\[
H\!\left(e^{j\omega}\right)=
\begin{cases}
L, & 0\leq\left|\omega\right|<\omega_c,\\
0, & \omega_c\leq\left|\omega\right|\leq\pi,
\end{cases}
\qquad
\omega_c=\min\!\left(\frac{\pi}{L},\frac{\pi}{M}\right).
\]</div>
<p>此时应把 [[L/M]] 分解为若干较小因子的乘积，构成多级采样率变换系统。各级在较宽的过渡带内工作，能显著降低每一级滤波器的设计代价；各级的倍率乘积必须仍等于总变换比。</p>
<div class="formula">\[
\frac{147}{160}=\frac{7}{8}\cdot\frac{7}{5}\cdot\frac{3}{4}.
\]</div>

<h2>8.5 多采样率系统的应用</h2>
<h3>语音系统中的采样率转换</h3>
<p>在语音系统中，可先以较高采样率完成 A/D 变换，再利用数字低通滤波器和抽取器降低处理采样率；输出端则通过内插、低通滤波和 D/A 变换恢复到所需的模拟输出采样率。这样可把难以实现的高选择性模拟抗混叠滤波任务，转移为较易精确设计的数字滤波任务。</p>
<h3>时分复用与频分复用</h3>
<p>时分复用将多个序列按时间交织成一路数据流，接收端再按时隙分离各路序列；频分复用则把不同信号安排在不同频带，经低通、带通或高通滤波器分离。多采样率结构能使各子带按其实际带宽选用合适采样率，从而减少总传输量和计算量。</p>
<div class="formula">\[
\begin{aligned}
y(n)&=\left\{\ldots,x_1(0),x_2(0),x_3(0),x_1(1),x_2(1),x_3(1),\ldots\right\},\\
y(n)&=y_1(n)+y_2(n)+y_3(n).
\end{aligned}
\]</div>
<h3>频分复用</h3>
<p>频分复用先把各路基带信号分别上采样，再用低通、带通和高通滤波器把它们安排到互不重叠的频带，最后相加传输。接收端按相同的频带分离，再恢复各支路；滤波器带宽与采样率必须共同保证各子带不发生混叠。</p>
<div class="formula">\[
\begin{aligned}
X_i\!\left(e^{j3\omega}\right)&=X_i\!\left(e^{j\omega}\right)\big|_{\omega\mapsto3\omega},\qquad i=1,2,3,\\
y(n)&=G_1(z)x_1^{\uparrow3}(n)+G_2(z)x_2^{\uparrow3}(n)+G_3(z)x_3^{\uparrow3}(n),\\
G_1(z),\ G_2(z),\ G_3(z)&\text{ 分别为低通、带通和高通滤波器。}
\end{aligned}
\]</div>
<h3>音频采样率转换</h3>
<p>常见音频系统同时使用 44.1 kHz、48 kHz、32 kHz、96 kHz 和 192 kHz 等采样率。若制作链路与播放标准不同，需要使用采样率转换器进行有理数倍重采样；当兼容 CD 音频时，还应注意采样率转换与位深转换是两个独立环节，不能混为一谈。</p>
<p>44.1 kHz 源于早期 PCM 录制设备与视频扫描体制的匹配：在 PAL 与 NTSC 两种体制下，分别有</p>
<div class="formula">\[
44100=294\cdot50\cdot3,\qquad 44056=245\cdot59.94\cdot3.
\]</div>
<p>实际录制与播放中，应尽量选择整数倍采样率的转换链路；若必须在 44.1 kHz 与 48 kHz 系列之间转换，则需要通过有理数倍采样率转换器完成重采样。位深降低属于量化格式转换，不能把它当成采样率转换的一部分。</p>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    content = (
        content
        .replace('<figure class="source-figure compact"><img src="../assets/source-figures/ch08-decimation-spectrum.png" alt="二倍抽取时的频谱移位、求和与拉伸"><figcaption>图 8-1　二倍抽取的频谱变换过程</figcaption></figure>', f'<figure>{decimation_spectrum_svg()}<figcaption>图 8-1　二倍抽取的频谱变换过程</figcaption></figure>')
        .replace('<figure class="source-figure compact"><img src="../assets/source-figures/ch08-decimator-structure.png" alt="抗混叠滤波器与抽取器级联结构"><figcaption>图 8-2　抗混叠滤波与抽取器的级联结构</figcaption></figure>', f'<figure>{decimator_svg()}<figcaption>图 8-2　抗混叠滤波与抽取器的级联结构</figcaption></figure>')
        .replace('<figure class="source-figure compact"><img src="../assets/source-figures/ch08-interpolator-structure.png" alt="上采样与插值低通滤波器的级联结构"><figcaption>图 8-3　插零与插值低通滤波器的级联结构</figcaption></figure>', f'<figure>{interpolator_svg()}<figcaption>图 8-3　插零与插值低通滤波器的级联结构</figcaption></figure>')
        .replace('<figure class="source-figure compact"><img src="../assets/source-figures/ch08-rational-converter.png" alt="L比M有理数倍采样率变换结构"><figcaption>图 8-4　有理数倍采样率变换的标准结构</figcaption></figure>', f'<figure>{rational_converter_svg()}<figcaption>图 8-4　有理数倍采样率变换的标准结构</figcaption></figure>')
    )
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{DIAGRAM_STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
