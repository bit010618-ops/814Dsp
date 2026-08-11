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
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.table{font-size:9.5pt}}
</style>"""


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

<h3>应用：双音多频信号</h3>
<p>电话按键的双音多频（DTMF）信号由一个低频组和一个高频组中的两个正弦分量叠加而成。并联型结构可把单位冲激输入分别送入两个二阶谐振支路，再在求和节点合成输出；各支路的极点位置直接决定所选频率。该例说明并联型便于控制极点，适合谐振器叠加，但不适合需要精确控制传输零点的陷波或窄带带阻滤波器。</p>

<h2>5.3 FIR 数字滤波器结构</h2>
<p>FIR 滤波器的单位冲激响应只在有限个样点非零。因果 FIR 的 [[H(z)]] 只含有限次 [[z^{-1}]] 多项式，极点全部位于 [[z=0]]，因此本身稳定；常见直接实现没有输出到输入的反馈。</p>
<div class="formula">\[
H(z)=\sum_{n=0}^{N-1}h(n)z^{-n},
\qquad
y(n)=\sum_{m=0}^{N-1}h(m)x(n-m).
\]</div>

<h3>抽头延迟线直接型</h3>
<p>直接型又称横向滤波器或抽头延迟线结构：输入依次通过 [[z^{-1}]] 延时链，每个抽头乘以 [[h(m)]] 后相加。优点是简单、直观、运算速度快，且系数就是冲激响应样值；不足是不能直接把零点以分节方式控制。</p>

<h3>FIR 级联型、频率抽样型与谐振器型</h3>
<p>当需要控制传输零点时，可将 [[H(z)]] 分解为实系数一阶或二阶因子并级联实现。与直接型相比，级联型通常需要更多系数和乘法，但零点控制更方便。频率抽样型从有限个频率样值出发构造系统，适合频率取样设计；谐振器型可由多个谐振单元并联形成，梳状滤波器中的零点与各谐振支路极点之间的抵消关系必须逐项检查。</p>

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

<p>频率采样结构由梳状滤波器和谐振器柜级联组成。对 [[N]] 个频率采样值 [[H(k)]]，可用 IDFT 关系构造有限长冲激响应：</p>
<div class="formula">\[
h(n)=\frac{1}{N}\sum_{k=0}^{N-1}H(k)e^{j2\pi kn/N}.
\]</div>
<p>该结构特别适合只有少数 [[H(k)]] 非零的窄带滤波器。其缺点是谐振器支路系数通常为复数，并且有限字长会使单位圆上的极点偏离，从而带来稳定性风险。修正方法是把梳状滤波器零点与谐振器极点同时移到半径 [[r\leq1]]、且接近单位圆的圆上，以换取稳健性。</p>

<h3>快速卷积型结构</h3>
<p>若输入的非零长度为 [[M]]、FIR 冲激响应的非零长度为 [[N]]，线性卷积输出长度为：</p>
<div class="formula">\[
L=M+N-1.
\]</div>
<p>将两个序列分别补零到 [[L]] 点后进行 [[L]] 点 FFT，相乘并作 [[L]] 点 IFFT，即可用圆周卷积等价地得到线性卷积。长序列处理中还应结合重叠相加法或重叠保留法分块，保证每一块的 FFT 长度避免循环混叠。</p>

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
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
