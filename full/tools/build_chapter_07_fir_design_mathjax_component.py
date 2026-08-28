"""Chapter-seven FIR design body, excluding source-code demonstrations."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt;orphans:3;widows:3}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt;break-inside:avoid}.table th,.table td{border:.45pt solid #b9c6cf;padding:6pt 7pt;text-align:left;vertical-align:top}.table th{color:#315d7c;font-weight:600;background:#f4f7f8}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.table{font-size:9.5pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>第七章 FIR 数字滤波器设计</h1>
<h2>7.1 线性相位 FIR 数字滤波器的条件和特点</h2>
<p>FIR 滤波器可严格实现线性相位。若长度为 [[N]] 的实序列冲激响应满足关于 [[(N-1)/2]] 的偶对称或奇对称，则相位可写成线性项加常数，群延迟为常数。其充要对称条件为：</p>
<p>理想延时说明了线性相位的含义：所有频率分量只经历同一延时 [[\tau]]，不会因相对时移不同而改变波形形状。</p>
<div class="formula">\[
\begin{aligned}
h(n)&=\delta(n-\tau),& y(n)&=x(n-\tau),\\
H\!\left(e^{j\omega}\right)&=e^{-j\tau\omega},&
\tau_g(\omega)&=-\frac{\mathrm{d}\theta(\omega)}{\mathrm{d}\omega}=\tau.
\end{aligned}
\]</div>
<p>一般线性相位频率响应可分成振幅响应与相位响应两部分。第一类的相位只有延时项；第二类除延时项外，还带有恒定的四分之一圆周相位偏置：</p>
<div class="formula">\[
\begin{aligned}
H\!\left(e^{j\omega}\right)&=\pm\left|H\!\left(e^{j\omega}\right)\right|e^{j\theta(\omega)},\\
\theta(\omega)&=-\tau\omega &&\text{（第一类线性相位）},\\
\theta(\omega)&=\beta_0-\tau\omega,& \beta_0&=\pm\frac{\pi}{2} &&\text{（第二类线性相位）}.
\end{aligned}
\]</div>
<p>对第一类线性相位，把频率响应分别按实部和虚部比较，可得到便于推导单位脉冲响应对称性的两条关系：</p>
<div class="formula">\[
\begin{aligned}
H(\omega)\cos(\omega\tau)&=\sum_{n=0}^{N-1}h(n)\cos(\omega n),\\
H(\omega)\sin(\omega\tau)&=\sum_{n=0}^{N-1}h(n)\sin(\omega n).
\end{aligned}
\]</div>
<p>两式消去振幅响应，得到对任意 \(\omega\) 都成立的条件：</p>
<div class="formula">\[
\sum_{n=0}^{N-1}h(n)\sin\!\left[(n-\tau)\omega\right]=0.
\]</div>
<p>当有限长序列的支撑区间为 \(0\leq n\leq N-1\) 时，对称中心为 \(\tau=(N-1)/2\)。第一类线性相位要求 \(h(n)\) 关于该中心偶对称，因此：</p>
<div class="formula">\[
\tau=\frac{N-1}{2},
\qquad
h(n)=h(N-1-n),
\qquad 0\leq n\leq N-1.
\]</div>
<p>第二类线性相位含有 \(\beta_0=\pm\pi/2\) 的常数相位偏置。相同的实虚部比较给出：</p>
<div class="formula">\[
\sum_{n=0}^{N-1}h(n)\sin\!\left[\beta_0+(n-\tau)\omega\right]=0,
\qquad
h(n)=-h(N-1-n).
\]</div>
<div class="formula">\[
h(n)=\pm h(N-1-n),\qquad 0\leq n\leq N-1.
\]</div>
<p>偶对称属于第一类线性相位，奇对称属于第二类线性相位。长度奇偶与对称类型共同决定 [[H(0)]]、[[H(\pi)]] 是否必为零，进而决定能否实现低通、高通、带通或带阻。实系数线性相位 FIR 的零点同时满足共轭成对与关于单位圆镜像对称；全部极点位于原点，系统稳定。</p>
<div class="formula">\[
H(z)=\sum_{n=0}^{N-1}h(n)z^{-n},
\qquad
z_i\text{ 为零点 }\Longrightarrow z_i^*,\ \frac{1}{z_i},\ \frac{1}{z_i^*}\text{ 也按重数出现。}
\]</div>
<figure class="diagram"><figcaption>FIR 滤波的时域与频域对应关系</figcaption>
<svg class="fir-flow-svg" viewBox="0 0 920 310" role="img" aria-label="FIR 时域卷积与频域相乘对应关系图">
<defs><marker id="fir-flow-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6z" fill="#174b73"/></marker></defs>
<rect class="box" x="64" y="42" width="210" height="68" rx="8"/><foreignObject class="math-foreign" x="94" y="54" width="150" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(h(n)\)</div></foreignObject><text class="caption" x="169" y="101" text-anchor="middle">有限长冲激响应</text>
<path class="arrow" d="M18 144H360"/><foreignObject class="math-foreign" x="20" y="112" width="60" height="25"><div xmlns="http://www.w3.org/1999/xhtml">\(x(n)\)</div></foreignObject><rect class="box" x="360" y="115" width="190" height="58" rx="8"/><text class="label" x="455" y="151" text-anchor="middle">时域卷积</text><path class="arrow" d="M550 144H886"/><foreignObject class="math-foreign" x="690" y="112" width="190" height="25"><div xmlns="http://www.w3.org/1999/xhtml">\(y(n)=x(n)*h(n)\)</div></foreignObject>
<path class="arrow" d="M169 112V220"/><text class="label" x="183" y="185">DTFT</text><path class="arrow" d="M454 174V220"/><text class="label" x="468" y="199">DTFT</text>
<rect class="freq-box" x="64" y="230" width="210" height="60" rx="8"/><foreignObject class="math-foreign" x="80" y="245" width="178" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(H(e^{j\omega})\)</div></foreignObject>
<rect class="freq-box" x="360" y="230" width="190" height="60" rx="8"/><text class="label" x="455" y="267" text-anchor="middle">频域相乘</text>
<rect class="freq-box" x="660" y="230" width="210" height="60" rx="8"/><foreignObject class="math-foreign" x="666" y="245" width="198" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(Y(e^{j\omega})=X(e^{j\omega})H(e^{j\omega})\)</div></foreignObject>
<path class="arrow" d="M274 260H356"/><path class="arrow" d="M550 260H656"/>
</svg></figure>
<figure class="diagram"><figcaption>FIR 幅频响应决定频率成分的去留</figcaption>
<svg class="fir-spectrum-selection-svg" viewBox="0 0 920 350" role="img" aria-label="输入频谱、FIR 幅频响应与输出频谱关系图">
<defs><marker id="fir-select-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6z" fill="#174b73"/></marker></defs>
<text class="label" x="155" y="32" text-anchor="middle">输入频谱</text><text class="label" x="460" y="32" text-anchor="middle">低通 FIR 幅频响应</text><text class="label" x="765" y="32" text-anchor="middle">输出频谱</text>
<path class="axis" d="M42 276H275" marker-end="url(#fir-select-arrow)"/><path class="axis" d="M70 292V60" marker-end="url(#fir-select-arrow)"/>
<path class="input-spectrum" d="M78 276L112 245L138 156L165 245L194 276M194 276L215 258L237 205L258 258L272 276"/>
<text class="caption" x="36" y="78">幅度</text><foreignObject class="math-foreign" x="255" y="282" width="28" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega\)</div></foreignObject><text class="caption" x="138" y="323" text-anchor="middle">低频与高频均存在</text>
<path class="axis" d="M347 276H580" marker-end="url(#fir-select-arrow)"/><path class="axis" d="M375 292V60" marker-end="url(#fir-select-arrow)"/>
<path class="passband" d="M392 276V114H510V276Z"/><path class="filter-response" d="M382 276H392V114H510V276H570"/>
<path class="cutoff" d="M392 114V276M510 114V276"/><foreignObject class="math-foreign" x="366" y="282" width="52" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(-\omega_c\)</div></foreignObject><foreignObject class="math-foreign" x="492" y="282" width="36" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega_c\)</div></foreignObject><foreignObject class="math-foreign" x="329" y="60" width="40" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\left|H\right|\)</div></foreignObject><foreignObject class="math-foreign" x="560" y="282" width="28" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega\)</div></foreignObject><text class="caption" x="451" y="323" text-anchor="middle">仅保留通带频率成分</text>
<path class="axis" d="M652 276H885" marker-end="url(#fir-select-arrow)"/><path class="axis" d="M680 292V60" marker-end="url(#fir-select-arrow)"/>
<path class="output-spectrum" d="M688 276L720 250L748 156L775 250L802 276"/><text class="caption" x="646" y="78">幅度</text><foreignObject class="math-foreign" x="865" y="282" width="28" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\(\omega\)</div></foreignObject><text class="caption" x="765" y="323" text-anchor="middle">高频分量被抑制</text>
</svg></figure>
<p>由关于中心的偶对称或奇对称直接换元，可得系统函数的倒数对称关系：</p>
<div class="formula">\[
H(z)=\pm z^{-(N-1)}H\!\left(z^{-1}\right).
\]</div>
<p>令 \(z=e^{j\omega}\) 后，可把与延时有关的线性相位提出，余下的 \(H_0(\omega)\) 决定幅度响应：</p>
<div class="formula">\[
\begin{aligned}
H\!\left(e^{j\omega}\right)&=e^{-j\frac{N-1}{2}\omega}H_0(\omega),\\
H_0(\omega)&=\sum_{n=0}^{N-1}h(n)\cos\!\left[\left(\frac{N-1}{2}-n\right)\omega\right]
&&\text{（偶对称）},\\
H_0(\omega)&=j\sum_{n=0}^{N-1}h(n)\sin\!\left[\left(\frac{N-1}{2}-n\right)\omega\right]
&&\text{（奇对称）}.
\end{aligned}
\]</div>
<h3>例题</h3>
<p>设某线性相位 FIR 数字滤波器的 \(h(n)\) 为实序列，它的三个零点是 \(z=-1,\quad z=0.5,\quad z=0.5e^{j\pi/4}\)。试确定该滤波器可能存在的其余零点，并求最低阶数及最小群延迟。</p>
<p>解：实序列零点先按共轭成对，再按单位圆镜像成对。因此其余零点为 \(0.5e^{-j\pi/4}\)、\(2\)、\(2e^{j\pi/4}\)、\(2e^{-j\pi/4}\)。连同已知零点共七个，故：</p>
<div class="formula">\[
N-1=7,\qquad \tau=\frac{N-1}{2}=3.5.
\]</div>
<figure class="diagram"><figcaption>FIR 系统函数的零极点结构</figcaption>
<svg class="fir-pz-svg" viewBox="0 0 720 320" role="img" aria-label="FIR 零极点图">
<defs><marker id="fir-pz-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6z" fill="#174b73"/></marker></defs>
<path class="axis" d="M70 160H380" marker-end="url(#fir-pz-arrow)"/><path class="axis" d="M225 295V28" marker-end="url(#fir-pz-arrow)"/><circle class="unit" cx="225" cy="160" r="105"/>
<text class="label" x="390" y="181">Re[z]</text><text class="label" x="240" y="41">Im[z]</text><text class="caption" x="225" y="312" text-anchor="middle">单位圆</text>
<circle class="zero" cx="120" cy="160" r="8"/><circle class="zero" cx="277" cy="160" r="8"/><circle class="zero" cx="262" cy="123" r="8"/><circle class="zero" cx="262" cy="197" r="8"/><circle class="zero" cx="330" cy="86" r="8"/><circle class="zero" cx="330" cy="234" r="8"/>
<path class="pole" d="M216 151L234 169M234 151L216 169"/><text class="caption" x="238" y="151">原点极点 N−1 重</text>
<text class="caption" x="78" y="184">−1</text><text class="caption" x="268" y="184">0.5</text><text class="caption" x="337" y="78">镜像零点</text><text class="caption" x="337" y="252">镜像零点</text>
<text class="label" x="470" y="100">实系数：零点成共轭对</text><text class="label" x="470" y="142">线性相位：关于单位圆镜像</text><text class="label" x="470" y="184">FIR：全部极点在原点</text><text class="label" x="470" y="226">因此系统必稳定</text>
</svg></figure>

<figure class="diagram"><figcaption>有限长冲激响应的对称中心</figcaption>
<svg class="fir-symmetry-svg" viewBox="0 0 920 270" role="img" aria-label="奇偶长度 FIR 冲激响应对称示意图">
<text class="label" x="230" y="26" text-anchor="middle">偶对称，N 为奇数，τ=5</text><text class="label" x="690" y="26" text-anchor="middle">偶对称，N 为偶数，τ=4.5</text>
<path class="axis" d="M50 180H410"/><path class="axis" d="M510 180H870"/><path class="mirror" d="M230 45V225"/><path class="mirror" d="M690 45V225"/>
<g class="stem"><path d="M80 180V145M115 180V160M150 180V130M195 180V155M230 180V110M265 180V155M310 180V130M345 180V160M380 180V145"/><path d="M540 180V145M575 180V160M610 180V130M655 180V155M725 180V155M770 180V130M805 180V160M840 180V145"/></g>
<g class="dot"><circle cx="80" cy="145" r="4"/><circle cx="115" cy="160" r="4"/><circle cx="150" cy="130" r="4"/><circle cx="195" cy="155" r="4"/><circle cx="230" cy="110" r="4"/><circle cx="265" cy="155" r="4"/><circle cx="310" cy="130" r="4"/><circle cx="345" cy="160" r="4"/><circle cx="380" cy="145" r="4"/><circle cx="540" cy="145" r="4"/><circle cx="575" cy="160" r="4"/><circle cx="610" cy="130" r="4"/><circle cx="655" cy="155" r="4"/><circle cx="725" cy="155" r="4"/><circle cx="770" cy="130" r="4"/><circle cx="805" cy="160" r="4"/><circle cx="840" cy="145" r="4"/></g>
<text class="caption" x="230" y="250" text-anchor="middle">样值相对于整数对称中心成对出现</text><text class="caption" x="690" y="250" text-anchor="middle">对称中心位于两个样本之间</text>
</svg></figure>

<h3>四种线性相位类型</h3>
<table class="table"><thead><tr><th>类型</th><th>对称性与长度</th><th>端点约束</th><th>可实现的典型响应</th></tr></thead><tbody>
<tr><td>I</td><td>偶对称，[[N]] 为奇数</td><td>无强制端点零值</td><td>低通、高通、带通、带阻</td></tr>
<tr><td>II</td><td>偶对称，[[N]] 为偶数</td><td>[[H(\pi)=0]]</td><td>低通、带通；不能作高通、带阻</td></tr>
<tr><td>III</td><td>奇对称，[[N]] 为奇数</td><td>[[H(0)=H(\pi)=0]]</td><td>带通及需要奇对称响应的场合</td></tr>
<tr><td>IV</td><td>奇对称，[[N]] 为偶数</td><td>[[H(0)=0]]</td><td>高通、带通</td></tr>
</tbody></table>
<h3>四类结构的幅度函数</h3>
<p>利用成对的抽头可把四类结构分别写成余弦级数或正弦级数。下式中的 \(H_{\mathrm{I}}\) 至 \(H_{\mathrm{IV}}\) 表示提出线性相位因子之后的实值幅度函数：</p>
<div class="formula">\[
\begin{aligned}
N=2M+1:\qquad
H_{\mathrm{I}}(\omega)&=h(M)+2\sum_{m=1}^{M}h(M-m)\cos(m\omega),\\
H_{\mathrm{III}}(\omega)&=2\sum_{m=1}^{M}h(M-m)\sin(m\omega),\\
N=2M:\qquad
H_{\mathrm{II}}(\omega)&=2\sum_{m=1}^{M}h(M-m)\cos\!\left[\left(m-\frac{1}{2}\right)\omega\right],\\
H_{\mathrm{IV}}(\omega)&=2\sum_{m=1}^{M}h(M-m)\sin\!\left[\left(m-\frac{1}{2}\right)\omega\right].
\end{aligned}
\]</div>
<p>四种类型的区别来自对称性及长度奇偶性。设计前必须先核对通带是否包含 [[\omega=0]] 或 [[\omega=\pi]]；若结构在该端点被强制为零，就不能用来实现端点处要求非零增益的理想响应。</p>

<h2>7.2 利用窗函数法设计 FIR 滤波器</h2>
<p>窗函数法先由理想频响 [[H_d(e^{j\omega})]] 作 IDTFT 得到通常无限长的 [[h_d(n)]]，再用有限长度窗截断为可实现序列：</p>
<div class="formula">\[
h(n)=h_d(n)w(n).
\]</div>
<p>取长度为 [[N]] 的矩形窗时，截断序列与其频率响应分别为：</p>
<div class="formula">\[
R_N(n)=
\begin{cases}
1, & 0\le n\le N-1,\\
0, & \text{其他}.
\end{cases}
\qquad
W_R\!\left(e^{j\omega}\right)
=\frac{1-e^{-j\omega N}}{1-e^{-j\omega}}
=e^{-j\omega\frac{N-1}{2}}\frac{\sin(N\omega/2)}{\sin(\omega/2)}.
\]</div>
<p>常用窗函数都在 [[0\le n\le N-1]] 内定义；它们以更宽的主瓣换取更低的旁瓣。三角窗、汉宁窗、海明窗和布莱克曼窗可统一写为：</p>
<div class="formula">\[
w_{\mathrm{tri}}(n)=
\begin{cases}
\dfrac{2n}{N-1}, & 0\le n\le\dfrac{N-1}{2},\\
2-\dfrac{2n}{N-1}, & \dfrac{N-1}{2}&lt;n\le N-1.
\end{cases}
\]</div>
<div class="formula formula-wide">\[
\begin{aligned}
w_{\mathrm{Han}}(n)&=\frac{1}{2}\left[1-\cos\!\left(\frac{2\pi n}{N-1}\right)\right]R_N(n),\\
w_{\mathrm{Ham}}(n)&=\left[0.54-0.46\cos\!\left(\frac{2\pi n}{N-1}\right)\right]R_N(n),\\
w_{\mathrm{Blk}}(n)&=\left[0.42-0.5\cos\!\left(\frac{2\pi n}{N-1}\right)+0.08\cos\!\left(\frac{4\pi n}{N-1}\right)\right]R_N(n).
\end{aligned}
\]</div>
<p>时域相乘对应频域卷积，因此加窗会形成过渡带并产生振荡起伏。增加 [[N]] 会缩窄主瓣、减小过渡带宽，但同一窗形的主旁瓣能量比例并不因此改变；选窗则主要控制阻带衰减。矩形、三角、汉宁、海明和布莱克曼窗的典型阻带衰减依次增强，而对应过渡带通常变宽。</p>
<p>矩形窗频谱主瓣的第一零点间隔约为 [[4\pi/N]]，因此理想截止频率 [[\omega_c]] 附近会被展宽为过渡带，典型范围可写为：</p>
<div class="formula">\[
\omega_c-\frac{2\pi}{N}\lesssim\omega\lesssim\omega_c+\frac{2\pi}{N}.
\]</div>
<p>设计步骤是：由通/阻带边界取理想截止频率；写出 [[h_d(n)]]；按阻带衰减选择窗型；由过渡带宽确定 [[N]]；计算 [[h(n)]] 并复核频响。线性相位高通与带阻设计通常要求 [[N]] 为奇数，避免结构固有的端点零值与指标冲突。</p>

<table class="table"><thead><tr><th>窗函数</th><th>主瓣宽度</th><th>旁瓣峰值</th><th>典型过渡带宽</th><th>典型阻带最小衰减</th></tr></thead><tbody>
<tr><td>矩形窗</td><td>[[4\pi/N]]</td><td>-13 dB</td><td>[[1.8\pi/N]]</td><td>-21 dB</td></tr>
<tr><td>三角窗</td><td>[[8\pi/N]]</td><td>-25 dB</td><td>[[6.1\pi/N]]</td><td>-25 dB</td></tr>
<tr><td>汉宁窗</td><td>[[8\pi/N]]</td><td>-31 dB</td><td>[[6.2\pi/N]]</td><td>-44 dB</td></tr>
<tr><td>海明窗</td><td>[[8\pi/N]]</td><td>-41 dB</td><td>[[6.6\pi/N]]</td><td>-53 dB</td></tr>
<tr><td>布莱克曼窗</td><td>[[12\pi/N]]</td><td>-57 dB</td><td>[[11\pi/N]]</td><td>-74 dB</td></tr>
</tbody></table>
<h3>例题</h3>
<p>请设计一个线性相位 FIR 低通滤波器，技术指标如下：（1）抽样频率为 [[f_s=15\text{ kHz}]]；（2）通带截止频率为 [[f_p=1.5\text{ kHz}]]；（3）阻带截止频率为 [[f_{st}=3\text{ kHz}]]；（4）阻带衰减不小于 50 dB。</p>
<p>解：先把模拟频率换为数字角频率，并取通、阻带边界的中心作为理想截止频率：</p>
<div class="formula">\[
\begin{aligned}
\omega_p&=2\pi\frac{f_p}{f_s}=0.2\pi, & \omega_{st}&=2\pi\frac{f_{st}}{f_s}=0.4\pi,\\
\omega_c&=\frac{\omega_p+\omega_{st}}{2}=0.3\pi, & \Delta\omega&=\left|\omega_{st}-\omega_p\right|=0.2\pi.
\end{aligned}
\]</div>
<p>阻带指标为 50 dB，应选择典型阻带衰减约为 53 dB 的海明窗。由海明窗的过渡带宽近似关系可定出长度和群延迟：</p>
<div class="formula">\[
N=\frac{6.6\pi}{\Delta\omega}=\frac{6.6\pi}{0.2\pi}=33,
\qquad
\tau=\frac{N-1}{2}=16.
\]</div>
<div class="formula">\[
h_d(n)=
\begin{cases}
\dfrac{\sin\left[\omega_c(n-\tau)\right]}{\pi(n-\tau)}, & n\ne\tau,\\
\dfrac{\omega_c}{\pi}, & n=\tau,
\end{cases}
\qquad h(n)=h_d(n)w_{\mathrm{Ham}}(n).
\]</div>
<p>代入本题的截止频率、长度及海明窗，可得实际 FIR 系数：</p>
<div class="formula">\[
h(n)=
\begin{cases}
\dfrac{\sin\!\left[0.3\pi(n-16)\right]}{\pi(n-16)}, & n\ne16,\\
0.3, & n=16,
\end{cases}
\left[0.54-0.46\cos\!\left(\frac{n\pi}{16}\right)\right]R_{33}(n).
\]</div>
<p>最后必须复核实际幅频响应的通带、阻带和过渡带；若不满足指标，应改变长度或窗形重新设计。</p>
<h3>高通、带通与带阻的理想单位抽样响应</h3>
<p>高通和带阻的线性相位设计通常取 [[N]] 为奇数。它们可以由全通、低通响应直接相减或相加；带通则由两个低通响应相减得到。令 [[\tau=(N-1)/2]]，三类理想单位抽样响应为：</p>
<div class="formula">\[
\begin{aligned}
h_{\mathrm{hp}}(n)&=\frac{\sin\!\left[\pi(n-\tau)\right]-\sin\!\left[\omega_c(n-\tau)\right]}{\pi(n-\tau)},\\
h_{\mathrm{bp}}(n)&=\frac{\sin\!\left[\omega_2(n-\tau)\right]-\sin\!\left[\omega_1(n-\tau)\right]}{\pi(n-\tau)},\\
h_{\mathrm{bs}}(n)&=\frac{\sin\!\left[\pi(n-\tau)\right]+\sin\!\left[\omega_1(n-\tau)\right]-\sin\!\left[\omega_2(n-\tau)\right]}{\pi(n-\tau)}.
\end{aligned}
\]</div>
<p>在 [[n=\tau]] 处各式应取极限值，再乘所选窗函数。带通设计的过渡带宽取两侧过渡带宽中的较小值；带阻可理解为高通与低通响应之和。</p>

<h2>7.3 利用频率采样法设计 FIR 滤波器</h2>
<p>频率采样法对理想频率响应作等间隔采样，并将采样值作为实际 FIR 数字滤波器频率特性的抽样值。由这 [[N]] 个频域样值可唯一确定一个长度为 [[N]] 的单位脉冲响应：</p>
<div class="formula">\[
\begin{aligned}
H(k)&=H_d(k)=H_d\!\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi}{N}k},\\
\omega_k&=\frac{2\pi}{N}k,\qquad k=0,1,\ldots,N-1,\\
h(n)&=\frac{1}{N}\sum_{k=0}^{N-1}H(k)W_N^{-nk},\qquad n=0,1,\ldots,N-1.
\end{aligned}
\]</div>
<p>若要求线性相位，频域采样值的幅度和相位也必须满足冲激响应对称性的约束。设 [[\tau=(N-1)/2]]，四类情形的采样值关系如下：</p>
<div class="formula formula-wide">\[
\begin{aligned}
h(n)=h(N-1-n),\ N\text{ 为奇数}:&\qquad H_k=H_{N-k},\quad H(\omega)\text{ 以 }0,\pi,2\pi\text{ 呈偶对称},\\
h(n)=h(N-1-n),\ N\text{ 为偶数}:&\qquad H_k=-H_{N-k},\quad H(\omega)\text{ 以 }\pi\text{ 呈奇对称},\quad H(\pi)=0,\\
h(n)=-h(N-1-n),\ N\text{ 为奇数}:&\qquad H_k=-H_{N-k},\quad H(\omega)\text{ 以 }0,\pi,2\pi\text{ 呈奇对称},\quad H(0)=H(\pi)=0,\\
h(n)=-h(N-1-n),\ N\text{ 为偶数}:&\qquad H_k=H_{N-k},\quad H(\omega)\text{ 以 }\pi\text{ 呈偶对称},\quad H(0)=0.
\end{aligned}
\]</div>
<p>偶对称时，采样相位为 [[\theta_k=-\frac{N-1}{N}\pi k]]；奇对称时，采样相位为 [[\theta_k=\pm\frac{\pi}{2}-\frac{N-1}{N}\pi k]]。低通示例中，[[N=33]] 为奇数且直流处需有非零增益，故应选 I 型线性相位；奇对称情形会强制 [[H(0)=H(\pi)=0]]，不适合一般低通。</p>
<p>频率采样点之间并非直线连接，而是由内插函数叠加恢复：</p>
<div class="formula">\[
\begin{aligned}
H\!\left(e^{j\omega}\right)&=\sum_{k=0}^{N-1}H(k)\Phi\!\left(\omega-\frac{2\pi}{N}k\right),\\
\Phi(\omega)&=\frac{\sin(\omega N/2)}{N\sin(\omega/2)}e^{-j\omega(N-1)/2}.
\end{aligned}
\]</div>
<figure class="diagram"><figcaption>频率采样点与过渡带起伏</figcaption>
<svg class="fir-sampling-svg" viewBox="0 0 920 320" role="img" aria-label="频率采样法低通 FIR 响应与过渡带图">
<defs><marker id="fir-sampling-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6z" fill="#174b73"/></marker></defs>
<path class="transition" d="M465 36H520V270H465z"/><path class="axis" d="M58 270H876" marker-end="url(#fir-sampling-arrow)"/><path class="axis" d="M58 270V34" marker-end="url(#fir-sampling-arrow)"/><text class="label" x="884" y="291">ω</text><text class="label" x="29" y="49">H(ω)</text>
<path class="ideal" d="M75 72H470V270H855"/><path class="response" d="M75 72 C145 65 175 81 230 70 S322 88 370 67 S430 90 466 72 C485 92 492 220 525 252 S565 222 598 258 S648 235 684 264 S733 242 770 265 S820 247 855 264"/>
<g class="stem"><path d="M75 270V72M122 270V72M169 270V72M216 270V72M263 270V72M310 270V72M357 270V72M404 270V72M451 270V72M498 270V270M545 270V270M592 270V270M639 270V270M686 270V270M733 270V270M780 270V270M827 270V270"/></g>
<g class="dot"><circle cx="75" cy="72" r="4"/><circle cx="122" cy="72" r="4"/><circle cx="169" cy="72" r="4"/><circle cx="216" cy="72" r="4"/><circle cx="263" cy="72" r="4"/><circle cx="310" cy="72" r="4"/><circle cx="357" cy="72" r="4"/><circle cx="404" cy="72" r="4"/><circle cx="451" cy="72" r="4"/><circle cx="498" cy="270" r="4"/><circle cx="545" cy="270" r="4"/><circle cx="592" cy="270" r="4"/><circle cx="639" cy="270" r="4"/><circle cx="686" cy="270" r="4"/><circle cx="733" cy="270" r="4"/><circle cx="780" cy="270" r="4"/><circle cx="827" cy="270" r="4"/></g>
<text class="caption" x="270" y="54" text-anchor="middle">通带取样值</text><text class="caption" x="492" y="302" text-anchor="middle">过渡带：无取样点</text><text class="caption" x="690" y="242" text-anchor="middle">内插引起的阻带起伏</text><text class="caption" x="470" y="291">0.5π</text><text class="caption" x="848" y="291">π</text>
</svg></figure>
<p>理想频响变化越陡，不连续点附近的肩峰和起伏越明显。若过渡带没有采样点，通带会产生波动，阻带衰减也会较差；增加采样点或在过渡带安排非零的过渡采样值可显著改善结果。设计时不可只让通带、阻带采样点“对上”，还应检查采样点之间由内插得到的真实频响。</p>

<h3>例题</h3>
<p>利用频率采样法，设计一个线性相位低通 FIR 数字滤波器，其理想幅频特性如下：已知 [[\omega_c=0.5\pi]]，采样点数为奇数 [[N=33]]。试求各采样点的幅值 [[H_k]] 及相位 [[\theta_k]]，也即求频域采样值 [[H(k)]]。</p>
<p>解：[[N=33]] 为奇数。低通响应在直流处必须有非零增益，因此排除奇对称情形，选择 I 型线性相位，群延迟为 [[\tau=16]]。在 [[\omega_k=2\pi k/33]] 上，低通通带对应 [[k=0,1,\ldots,8]] 与 [[k=25,\ldots,32]]，其余采样点取零；相位按 [[\theta_k=-16\omega_k]] 给出。该取样在过渡带没有采样点，故采样点之间的内插会造成较明显的阻带起伏。</p>
<p>减小误差的一种直接方式是在过渡带增加采样点。经验结果是：不加过渡采样点时阻带衰减约为 20 dB；加入一个值约为 0.3904 的过渡采样点时约为 44--54 dB；加入两个值约为 0.5886、0.1065 的过渡采样点时约为 65--75 dB。</p>

<h2>7.4 利用等波纹逼近法设计 FIR 滤波器</h2>
<p>等波纹最佳逼近是一种优化设计方法：在给定滤波器长度与线性相位约束下，使逼近区域内加权误差的最大值最小，且极大误差在整个逼近频段近似均匀分布。设 [[H_d(\omega)]] 为理想广义幅度、[[H_g(\omega)]] 为实际设计的广义幅度，则：</p>
<div class="formula">\[
\begin{aligned}
E(\omega)&=W(\omega)\left|H_d(\omega)-H_g(\omega)\right|,\\
\mathop{\min}_{\vphantom{\omega}}\ \max_{\omega\in\mathcal{B}}\left|E(\omega)\right|.&
\end{aligned}
\]</div>
<p>加权函数 [[W(\omega)]] 越大，对应频段的逼近精度越高。通带和阻带是逼近区域，过渡带是不要求精确逼近的无关区域；无关区域的宽度不能为零。Remez 多重交换迭代以加权切比雪夫准则求取 [[h(n)]]，可分别控制通带和阻带的波纹幅度，通常比窗函数法和基本频率采样法以更短长度达到同一指标。</p>
<p>给定通带波纹 [[\alpha_p]] 与阻带衰减 [[\alpha_s]] 时，常先将指标换算为线性容限：</p>
<div class="formula">\[
\begin{aligned}
\delta_p&=\frac{10^{\alpha_p/20}-1}{10^{\alpha_p/20}+1},\\
\delta_s&=10^{-\alpha_s/20}.
\end{aligned}
\]</div>
<table class="table"><thead><tr><th>方法</th><th>直接控制量</th><th>主要特征</th></tr></thead><tbody><tr><td>窗函数法</td><td>窗型与长度</td><td>过程直观；过渡带与旁瓣受窗函数制约。</td></tr><tr><td>频率采样法</td><td>离散频响样值</td><td>便于指定关键频点；需处理采样点间插误差。</td></tr><tr><td>等波纹逼近</td><td>误差权重与长度</td><td>在给定长度下最大加权误差最小；通、阻带可独立加权。</td></tr></tbody></table>
<h3>例题</h3>
<p>用窗函数法和等波纹最佳逼近法分别设计一个线性相位 FIR 带阻滤波器。指标如下：通带下截止频率 [[\omega_{lp}=0.2\pi]]，阻带下截止频率 [[\omega_{ls}=0.35\pi]]；阻带上截止频率 [[\omega_{us}=0.65\pi]]，通带上截止频率 [[\omega_{up}=0.8\pi]]，[[\alpha_p=1\text{ dB}]]，[[\alpha_s=60\text{ dB}]]。</p>
<p>解题比较时，窗函数法先由最窄过渡带估算长度，并选择满足阻带衰减的窗；等波纹法则把两个通带和中间阻带分别作为逼近区域，依据通带、阻带容限构造权重。两种方法的频率边界相同，但等波纹法可通过加权误差分配，在相近技术指标下使用更短的滤波器长度。</p>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    # Keep all SVG paint local to each primitive: the static PDF exporter does
    # not reliably inherit outer stylesheet rules for inline SVG.
    for source, rendered in {
        'class="box"': 'class="box" fill="#f4f7f8" stroke="#0d8794" stroke-width="2"',
        'class="freq-box"': 'class="freq-box" fill="#f4f7f8" stroke="#0d8794" stroke-width="2"',
        'class="axis"': 'class="axis" fill="none" stroke="#174b73" stroke-width="2"',
        'class="arrow"': 'class="arrow" fill="none" stroke="#174b73" stroke-width="2.5"',
        'class="mirror"': 'class="mirror" fill="none" stroke="#b56b2e" stroke-width="1.8" stroke-dasharray="5 4"',
        'class="unit"': 'class="unit" fill="none" stroke="#7f929f" stroke-width="1.8"',
        'class="input-spectrum"': 'class="input-spectrum" fill="#5b9bbf" fill-opacity="0.58" stroke="#174b73" stroke-width="2"',
        'class="output-spectrum"': 'class="output-spectrum" fill="#5b9bbf" fill-opacity="0.58" stroke="#174b73" stroke-width="2"',
        'class="filter-response"': 'class="filter-response" fill="#dceef4" stroke="#0d8794" stroke-width="2"',
        'class="transition"': 'class="transition" fill="#fff1cf" fill-opacity="0.75" stroke="none"',
        'class="response"': 'class="response" fill="none" stroke="#0d8794" stroke-width="2.5"',
        'class="ideal"': 'class="ideal" fill="none" stroke="#b56b2e" stroke-width="2" stroke-dasharray="6 4"',
        'class="stem"': 'class="stem" fill="none" stroke="#0d8794" stroke-width="2"',
        'class="dot"': 'class="dot" fill="#c97806"',
        'class="zero"': 'class="zero" fill="#ffffff" stroke="#0d8794" stroke-width="2.4"',
        'class="pole"': 'class="pole" fill="none" stroke="#b56b2e" stroke-width="2.4"',
        'class="label"': 'class="label" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16"',
        'class="caption"': 'class="caption" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14"',
    }.items():
        content = content.replace(source, rendered)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
