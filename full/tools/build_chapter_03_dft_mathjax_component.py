"""Chapter-three §3.2 DFT definition and properties in a MathJax component."""
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
p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.note{color:#52616b;margin:4pt 0 8pt}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>3.2 离散傅里叶变换的定义及性质</h1>
<p>DFT 面向有限长序列。把长度为 [[N]] 的主值序列视作一个 [[N]] 周期序列的一个周期，DFS 的变换对就限制为有限个样值，从而得到 DFT 与 IDFT。</p>

<h2>有限长序列的周期延拓</h2>
<p>设 [[x(n)]] 仅在 [[0\leq n\leq N-1]] 给定。其周期延拓可写为 [[\widetilde{x}(n)=x((n)\bmod N)]]；[[x(n)]] 称为主值序列，区间 [[0\leq n\leq N-1]] 称为主值区间。DFT 的每一步都隐含这一周期性，不能把越界下标当作普通的零值而忽略折回。</p>

<h2>DFT 与 IDFT</h2>
<p>令 [[W_N=e^{-j2\pi/N}]]，[[x(n)]] 的 [[N]] 点 DFT 定义为：</p>
<div class="formula">\[
X(k)=\sum_{n=0}^{N-1}x(n)W_N^{nk},\qquad 0\leq k\leq N-1.
\]</div>
<p>反变换为：</p>
<div class="formula">\[
x(n)=\frac{1}{N}\sum_{k=0}^{N-1}X(k)W_N^{-nk},\qquad 0\leq n\leq N-1.
\]</div>
<p>主值序列之外的取值按周期延拓理解，因此：</p>
<div class="formula">\[
x(n+N)=x(n),\qquad X(k+N)=X(k).
\]</div>
<p class="note">[[N]] 点 DFT 的时域和频域都只有 [[N]] 个独立值；DFT 与 IDFT 的信息量相同。</p>

<h2>与 DTFT 的关系</h2>
<p>有限长序列的 DTFT 是连续频率函数，[[N]] 点 DFT 则是在单位圆上等间隔取 [[N]] 个频率样值：</p>
<div class="formula">\[
X(k)=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{N}},\qquad k=0,1,\ldots,N-1.
\]</div>
<p>增加 DFT 点数相当于在同一条 DTFT 曲线上取得更密的频率样点；若仅在时域末尾补零，原始记录长度未增加，不能改变由记录长度决定的本征分辨能力。</p>

<h2>线性与循环移位</h2>
<p>对相同长度的序列，DFT 满足线性性质；长度不同时应先以零补到共同的 DFT 长度：</p>
<div class="formula">\[
a x_1(n)+b x_2(n)
\quad\longleftrightarrow\quad
aX_1(k)+bX_2(k).
\]</div>
<p>循环移位的正确顺序是：先把有限长序列作 [[N]] 周期延拓，再移位，最后在主值区间取值。时域循环移位与频域线性相位因子对应：</p>
<div class="formula">\[
x\left((n-n_0)\bmod N\right)
\quad\longleftrightarrow\quad
W_N^{k n_0}X(k).
\]</div>
<p>频域循环移位对应时域调制：</p>
<div class="formula">\[
W_N^{-n k_0}x(n)
\quad\longleftrightarrow\quad
X\left((k-k_0)\bmod N\right).
\]</div>
<h3>例题：8 点圆周移位与反褶</h3>
<p>已知序列 (x(n)=\{1,2,3,4\})，其中第一个样值对应 (n=0)。将它补零为 8 点主值序列后，分别求下列圆周运算的主值序列。</p>
<div class="formula">\[
\begin{aligned}
x\left((n)\bmod8\right)R_8(n)&=\{1,2,3,4,0,0,0,0\},\\
x\left((n+2)\bmod8\right)R_8(n)&=\{3,4,0,0,0,0,1,2\},\\
x\left((n-2)\bmod8\right)R_8(n)&=\{0,0,1,2,3,4,0,0\},\\
x\left((-n)\bmod8\right)R_8(n)&=\{1,0,0,0,0,4,3,2\},\\
x\left((-n+2)\bmod8\right)R_8(n)&=\{3,2,1,0,0,0,0,4\},\\
x\left((-n-2)\bmod8\right)R_8(n)&=\{0,0,0,4,3,2,1,0\}.
\end{aligned}
\]</div>
<p>例如对最后一式取 (n=3)，有：</p>
<div class="formula">\[
x\left((-3-2)\bmod8\right)=x\left((-5)\bmod8\right)=x(3)=4.
\]</div>
<p>这个检验说明圆周反褶不是把有限长列表直接倒写：应先完成 8 周期延拓，再按模 8 的下标取值。</p>

<h2>循环共轭对称与循环卷积</h2>
<p>实序列的 DFT 满足循环共轭对称关系 [[X(k)=X^*((-k)\bmod N)]]。计算实序列 DFT 时，只需直接计算约半数频点，其余频点可由该关系复核。</p>
<p>两个 [[N]] 点序列的循环卷积定义为：</p>
<div class="formula">\[
y(n)=x_1(n)\mathbin{\circledast}_N x_2(n)
=\sum_{m=0}^{N-1}x_1(m)x_2\left((n-m)\bmod N\right).
\]</div>
<p>它与频域逐点相乘相对应：</p>
<div class="formula">\[
Y(k)=X_1(k)X_2(k),\qquad
y(n)=\operatorname{IDFT}\left\{X_1(k)X_2(k)\right\}.
\]</div>
<p>手算循环卷积时依次执行：补零到 [[N]] 点、周期延拓、反褶、循环移位、逐点相乘后求和。要由循环卷积得到线性卷积，须取 [[N\geq N_1+N_2-1]]，否则首尾项会发生时域混叠。</p>

<h2>例题：序列 R_4(n) 的 DTFT、8 点 DFT 与 16 点 DFT</h2>
<p>已知 [[x(n)=R_4(n)]]，求 [[x(n)]] 的 DTFT，以及其 8 点和 16 点 DFT。</p>
<h3>解</h3>
<p>该序列在 [[n=0,1,2,3]] 为 1，其余为 0。因此：</p>
<div class="formula">\[
\begin{aligned}
X\left(e^{j\omega}\right)
&=\sum_{n=0}^{3}e^{-j\omega n}\\
&=e^{-j\frac{3\omega}{2}}\frac{\sin(2\omega)}{\sin(\omega/2)}.
\end{aligned}
\]</div>
<p>8 点 DFT 是在 [[\omega_k=2\pi k/8]] 处的 8 个样值，16 点 DFT 是在 [[\omega_k=2\pi k/16]] 处的 16 个样值：</p>
<div class="formula">\[
X_8(k)=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{8}},\qquad
X_{16}(k)=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{16}}.
\]</div>
<p>两者采样自同一条 DTFT。16 点 DFT 的谱线更密，但并未因补零而改变原四点记录的频率分辨能力。</p>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
