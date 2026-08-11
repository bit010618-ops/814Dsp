"""Chapter-six IIR filter-design body, excluding source-code exercises."""
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
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.table{font-size:9.5pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>第六章 IIR 数字滤波器设计</h1>

<h2>6.1 数字滤波器设计方法概述</h2>
<p>数字滤波器的目标是在给定的通带、阻带、过渡带和允许衰减条件下，构造一个因果稳定的离散 LSI 系统。按功能可分为低通、高通、带通、带阻；按冲激响应可分为 FIR 与 IIR。本章聚焦 IIR：先设计成熟的模拟原型，再把 [[s]] 平面系统映射为 [[z]] 平面系统。</p>
<p>设计过程分为三步：先由任务确定频率与衰减指标；再用因果稳定 [[H(z)]] 逼近这些指标；最后选择运算结构和有限字长。对于数字频响 [[H(e^{j\omega})]]，幅频特性描述各频率分量的衰减，相频特性描述相对延时。通带最大衰减与阻带最小衰减通常以 dB 表示：</p>
<div class="formula">\[
\alpha_p=-20\log_{10}\left|H\!\left(e^{j\omega_p}\right)\right|,
\qquad
\alpha_s=-20\log_{10}\left|H\!\left(e^{j\omega_s}\right)\right|.
\]</div>
<p>设计规格越接近理想矩形频响，阶数与实现复杂度通常越高。IIR 设计的关键不是机械套公式，而是始终检查稳定性、频率映射关系及最终数字频响是否仍满足原指标。</p>

<h3>经典滤波与现代滤波</h3>
<p>经典滤波器假定有用信号和待去除成分占据不同频带，利用选频特性实现分离；若信号和噪声频谱重叠，单纯的经典滤波通常无法完成分离。现代滤波则从含噪记录中估计信号或其特征，代表方法包括维纳滤波、卡尔曼滤波、线性预测和自适应滤波。本章讨论的是按频带指标设计的经典 IIR 数字滤波器。</p>
<h3>设计指标与实现步骤</h3>
<p>实际设计先确定通带、阻带和过渡带的边界及容限；再以因果稳定的离散 LSI 系统 [[H(z)]] 逼近指标；最后选择实现结构和有限字长。[[\alpha_p=-3\text{ dB}]] 时，[[|H(e^{j\omega_p})|\approx0.707]]，该点通常称为 3 dB 截止频率。</p>

<h2>6.2 模拟滤波器的设计</h2>
<p>模拟滤波器理论成熟，典型原型包括巴特沃斯、切比雪夫、椭圆和贝塞尔滤波器。实际设计通常先完成归一化低通原型，再通过频率变换得到高通、带通或带阻系统。</p>

<h3>巴特沃斯低通原型</h3>
<p>[[N]] 阶巴特沃斯低通的幅度平方函数为：</p>
<div class="formula">\[
\left|H_a(j\Omega)\right|^2=
\frac{1}{1+\left(\frac{\Omega}{\Omega_c}\right)^{2N}}.
\]</div>
<p>在 [[\Omega=\Omega_c]] 处幅度为 [[1/\sqrt2]]，即 3 dB 截止点。阶数越大，通带到阻带的过渡越陡，但结构越复杂。为了构成因果稳定滤波器，应从幅度平方函数的 [[2N]] 个极点中选取 [[s]] 平面左半平面的 [[N]] 个极点。</p>
<div class="formula">\[
\begin{aligned}
H_a(s)H_a(-s)&=\frac{1}{1+\left(\frac{s}{j\Omega_c}\right)^{2N}},\\
s_k&=\Omega_c e^{j\pi\left(\frac12+\frac{2k+1}{2N}\right)},
\qquad k=0,1,\ldots,2N-1,\\
H_a(s)&=\frac{\Omega_c^N}{\prod_{k=0}^{N-1}(s-s_k)},
\qquad \operatorname{Re}(s_k)<0.
\end{aligned}
\]</div>
<p>以 [[p=s/\Omega_c]] 作频率归一化后，先由通带 [[\Omega_p,\alpha_p]] 与阻带 [[\Omega_s,\alpha_s]] 求阶数：</p>
<div class="formula">\[
N\geq
\frac{\log_{10}\!\left(\dfrac{10^{\alpha_s/10}-1}{10^{\alpha_p/10}-1}\right)}
{2\log_{10}(\Omega_s/\Omega_p)}.
\]</div>
<p>计算所得 [[N]] 若非整数，取不小于它的最小整数；再由通带或阻带约束求 [[\Omega_c]] 并用另一条约束复核。随后查归一化极点或多项式系数，最后作去归一化。</p>

<h3>例题</h3>
<p>已知通带截止频率 [[f_p=5\text{ kHz}]]，通带最大衰减 [[\alpha_p=2\text{ dB}]]，截止频率 [[f_s=12\text{ kHz}]]，阻带最小衰减 [[\alpha_s=30\text{ dB}]]，按照以上技术指标设计巴特沃斯低通滤波器。</p>
<p>解：先将频率换为角频率 [[\Omega_p=2\pi f_p]]、[[\Omega_s=2\pi f_s]]，代入巴特沃斯阶数不等式，取不小于计算值的最小整数，得到 [[N=5]]。随后选取左半 [[s]] 平面的五个归一化极点：</p>
<div class="formula">\[
-0.3090\pm j0.9511,\qquad -0.8090\pm j0.5878,\qquad -1.0000.
\]</div>
<p>由这些极点构成归一化五阶原型，再用由通带或阻带约束求得的 [[\Omega_c]] 去归一化。最后必须把实际 [[H_a(j\Omega)]] 代回 [[\Omega_p]]、[[\Omega_s]] 复核衰减，而不能只因阶数取整就默认指标成立。</p>

<h3>频带变换</h3>
<p>高通、带通和带阻设计都可转化为归一化低通原型。高通可使用倒频映射；带通和带阻需要引入中心频率与带宽。对带通，令 [[B=\Omega_u-\Omega_l]]、[[\Omega_0^2=\Omega_l\Omega_u]]，则低通原型变量与带通变量满足：</p>
<div class="formula">\[
p=\frac{s^2+\Omega_0^2}{Bs}.
\]</div>
<p>带阻对应的低通变换为 [[p=Bs/(s^2+\Omega_0^2)]]。频带变换后必须重新检查两个阻带边界，选择更严格的一侧作为原型低通的阻带指标。</p>

<h3>例题</h3>
<p>设计模拟带通滤波器，通带带宽 [[B=2\pi\times200\text{ rad/s}]]，中心频率 [[\Omega_0=2\pi\times1000\text{ rad/s}]]，通带内最大衰减 [[\alpha_p=3\text{ dB}]]，阻带 [[\Omega_{s1}=2\pi\times830\text{ rad/s}]]、[[\Omega_{s2}=2\pi\times1200\text{ rad/s}]]，阻带最小衰减 [[\alpha_s=15\text{ dB}]]。</p>
<p>解：先归一化，[[\eta_0=\Omega_0/B=5]]，并把两侧阻带边界分别映射到低通原型频率。取绝对值较小者作为原型阻带边界，得到 [[\lambda_s=1.833]]；由巴特沃斯阶数公式得 [[N=3]]。设计三阶归一化低通原型后，代入</p>
<div class="formula">\[
p=\frac{s^2+\Omega_0^2}{Bs}
\]</div>
<p>即可得到带通 [[H_a(s)]]。这种“先选更严格阻带、后作低通到带通变换”的顺序同样适用于带阻设计。</p>

<h2>6.3 脉冲响应不变法</h2>
<p>脉冲响应不变法先将模拟 [[H_a(s)]] 作拉普拉斯反变换得到 [[h_a(t)]]，再以采样间隔 [[T]] 对其取样，构造数字冲激响应。若采用本章的增益约定，核心对应可写为：</p>
<div class="formula">\[
h(n)=T h_a(nT),
\qquad
H_a(s)=H(z)\big|_{z=e^{sT}}.
\]</div>
<p>映射 [[z=e^{sT}]] 将 [[s]] 平面左半平面映射到 [[z]] 平面单位圆内，因此稳定性得到保持；模拟虚轴映射为数字单位圆。模拟角频率与数字角频率在主值范围内呈线性关系：</p>
<div class="formula">\[
\omega=\Omega T.
\]</div>
<p>但时域取样必然导致频域周期延拓，数字频响是模拟频响的周期叠加，因此高频会折叠到主值频带而产生混叠。它适合衰减很快的低通或带通模拟原型；对高通和带阻，由于高频不充分衰减，通常不宜采用此法。</p>

<h3>例题</h3>
<p>已知一 RC 低通滤波电路，设 [[RC=1]]：（1）请求解该模拟滤波器的传递函数 [[H(s)]]，分析其滤波特性；（2）用脉冲响应不变法将该模拟滤波器转换为数字滤波器 [[H(z)]]，需保证数字滤波器 [[H(z)]] 的滤波特性与模拟滤波器相近。</p>
<p>解：RC 低通的传递函数为 [[H_a(s)=1/(s+1)]]，单位冲激响应为 [[h_a(t)=e^{-t}u(t)]]。按脉冲响应不变法取样，得到</p>
<div class="formula">\[
h(n)=T e^{-nT}u(n),\qquad
H(z)=\frac{T}{1-e^{-T}z^{-1}}.
\]</div>
<p>采样间隔 [[T]] 不能只按截止频率勉强选取，应为模拟阻带衰减留有余量；[[T]] 过大时，模拟高频尾部会周期折叠到数字主值频带，造成明显混叠。</p>

<h2>6.4 双线性变换法</h2>
<p>双线性变换通过非线性映射把整个模拟频率轴压缩到 [[-\pi/T]] 到 [[\pi/T]]，从而消除频谱混叠。标准变换为：</p>
<div class="formula">\[
s=\frac{2}{T}\frac{1-z^{-1}}{1+z^{-1}},
\qquad
z=\frac{1+sT/2}{1-sT/2}.
\]</div>
<p>左半 [[s]] 平面一一映射到单位圆内，虚轴一一映射到单位圆上，因而模拟因果稳定系统转换后仍因果稳定。代入 [[z=e^{j\omega}]] 可得频率关系：</p>
<div class="formula">\[
\Omega=\frac{2}{T}\tan\frac{\omega}{2},
\qquad
\omega=2\arctan\frac{\Omega T}{2}.
\]</div>
<p>该映射无混叠，但频率不再线性对应，故需要预畸变：将数字指标频率先转换为模拟频率，再设计模拟原型。低频近似下 [[\tan(\omega/2)\approx\omega/2]]，对应较接近线性；频率越高，畸变越不能忽略。</p>

<h2>6.5 IIR 数字滤波器设计方法小结</h2>
<h3>例题：两种变换法的比较</h3>
<p>设计低通数字滤波器，要求在通带内频率低于 [[0.2\pi\text{ rad}]] 时，容许幅度误差在 1 dB 以内；在频率 [[0.3\pi]] 到 [[\pi]] 之间的阻带衰减大于 15 dB。指定模拟滤波器采用巴特沃斯低通滤波器，试分别用脉冲响应不变法和双线性变换法设计滤波器。</p>
<p>解题时，两种方法都先使用相同的数字指标，但模拟原型指标不同：脉冲响应不变法可按 [[T=1\text{ s}]] 使用 [[\Omega=\omega/T]] 的线性对应；双线性变换法则必须对 [[0.2\pi]] 和 [[0.3\pi]] 分别预畸变为 [[\Omega=2\tan(\omega/2)/T]]。两者均可求得六阶巴特沃斯原型，但对应的 [[\Omega_c]] 与最终 [[H(z)]] 不同，原因正是频率映射不同。比较最终响应时，前者需额外检查混叠，后者需检查预畸变点是否准确对齐。</p>

<table class="table"><thead><tr><th>方法</th><th>保持的主要性质</th><th>主要限制</th></tr></thead><tbody>
<tr><td>脉冲响应不变法</td><td>时域冲激响应取样；频率线性对应。</td><td>存在频率混叠，宜用于高频衰减快的低通或带通原型。</td></tr>
<tr><td>双线性变换法</td><td>稳定性保持；频率一一映射，无混叠。</td><td>频率非线性，需要按关键频率预畸变。</td></tr>
</tbody></table>
<p>完整设计路线应当是：给出数字指标，按所选映射得到模拟指标；完成模拟低通原型与频带变换；将 [[H_a(s)]] 变为 [[H(z)]]；最后计算系数并复核幅频、相频、稳定性和有限字长实现条件。两种方法得到不同的数字系统并不表示谁“算错了”，而是它们保持的近似性质不同。</p>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
