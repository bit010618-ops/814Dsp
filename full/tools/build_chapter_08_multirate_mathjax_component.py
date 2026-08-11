"""Chapter-eight multirate DSP body, excluding source-code exercises."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt;orphans:3;widows:3}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt}.table th,.table td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:left;vertical-align:top}.table th{color:#315d7c;font-weight:500;background:#f4f7f8}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.table{font-size:9.5pt}}</style>"""


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
<p>上式可看作将原频谱按 [[M]] 段分解、移位并相加后再缩放。故抽取后表现为频谱拉伸、移位、求和与幅度缩小。为避免相加后的谱副本重叠，必须满足</p>
<div class="formula">\[
X\!\left(e^{j\omega}\right)=0,\qquad \frac{\pi}{M}\leq\left|\omega\right|\leq\pi.
\]</div>
<p>因此若原信号带宽未限制在 [[\pi/M]] 以内，抽取后会产生不可逆混叠。正确结构是先用抗混叠低通滤波器限制带宽，再接 [[\downarrow M]] 抽取器；不能把低通滤波器放在抽取之后当作补救。</p>

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

<h2>8.2 信号的整数倍内插</h2>
<p>[[L]] 倍内插使采样率提高 [[L]] 倍。第一步在相邻原样本间插入 [[L-1]] 个零：</p>
<div class="formula">\[
y(n)=\sum_{k=-\infty}^{\infty}x(k)\delta(n-kL),
\qquad F_s'=LF_s.
\]</div>
<p>零插入不会自动产生新的平滑样本，而是在频域形成镜像谱：</p>
<div class="formula">\[
Y\!\left(e^{j\omega}\right)=X\!\left(e^{j\omega L}\right).
\]</div>
<p>随后必须使用插值低通滤波器去除镜像，并补偿增益。理想插值器在 [[|\omega|\leq\pi/L]] 内增益为 [[L]]，其他频段为零；这样可保留原谱并获得较高采样率序列。</p>
<p>将插零序列通过插值滤波器后，时域关系为卷积：</p>
<div class="formula">\[
x_i(n)=\sum_{k=-\infty}^{\infty}y(k)h_i(n-k).
\]</div>
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

<h3>单级与多级采样频率变换</h3>
<p>单级有理数倍变换采用“[[\uparrow L]] [[\longrightarrow]] 低通滤波 [[\longrightarrow]] [[\downarrow M]]”的结构。低通滤波器同时承担抗影像和抗混叠任务；当 [[L]] 或 [[M]] 很大时，所需截止频率很低，滤波器阶数和计算量会显著增大。</p>
<p>此时应把 [[L/M]] 分解为若干较小因子的乘积，构成多级采样率变换系统。各级在较宽的过渡带内工作，能显著降低每一级滤波器的设计代价；各级的倍率乘积必须仍等于总变换比。</p>

<h2>8.5 多采样率系统的应用</h2>
<h3>语音系统中的采样率转换</h3>
<p>在语音系统中，可先以较高采样率完成 A/D 变换，再利用数字低通滤波器和抽取器降低处理采样率；输出端则通过内插、低通滤波和 D/A 变换恢复到所需的模拟输出采样率。这样可把难以实现的高选择性模拟抗混叠滤波任务，转移为较易精确设计的数字滤波任务。</p>
<h3>时分复用与频分复用</h3>
<p>时分复用将多个序列按时间交织成一路数据流，接收端再按时隙分离各路序列；频分复用则把不同信号安排在不同频带，经低通、带通或高通滤波器分离。多采样率结构能使各子带按其实际带宽选用合适采样率，从而减少总传输量和计算量。</p>
<h3>音频采样率转换</h3>
<p>常见音频系统同时使用 44.1 kHz、48 kHz、32 kHz、96 kHz 和 192 kHz 等采样率。若制作链路与播放标准不同，需要使用采样率转换器进行有理数倍重采样；当兼容 CD 音频时，还应注意采样率转换与位深转换是两个独立环节，不能混为一谈。</p>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
