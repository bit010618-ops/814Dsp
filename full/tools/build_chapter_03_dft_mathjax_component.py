"""Chapter-three §3.2 DFT definition and properties in a MathJax component."""
from __future__ import annotations

from pathlib import Path

from full.tools.normalize_mathjax_inline import normalize_legacy_inline_math
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


def circular_shift_cycle_svg() -> str:
    """Draw the circular-shift construction from real eight-point sample values."""

    rows = (
        (r"x(n)", (1, 2, 3, 4, 0, 0, 0, 0), "先在一个主值区间内补零"),
        (r"x\left((n+2)\right)_8", (3, 4, 0, 0, 0, 0, 1, 2), "按 8 周期向左循环移位 2 点"),
        (r"x\left((n+2)\right)_8R_8(n)", (3, 4, 0, 0, 0, 0, 1, 2), "在主值区间截取输出"),
    )
    fragments: list[str] = []
    for row, (label, sequence, explanation) in enumerate(rows):
        top = 44 + row * 126
        axis_y = top + 68
        x_axis_start, x_axis_end, y_axis = 70, 900, 118
        x_step = 74
        fragments.extend((
            f'<line x1="{x_axis_start}" y1="{axis_y}" x2="{x_axis_end}" y2="{axis_y}" stroke="#174b73" stroke-width="1.7" marker-end="url(#ch3-shift-arrow)"/>',
            f'<line x1="{y_axis}" y1="{axis_y+28}" x2="{y_axis}" y2="{top+18}" stroke="#174b73" stroke-width="1.5" marker-end="url(#ch3-shift-arrow)"/>',
            f'<line x1="{y_axis+8}" y1="{top+12}" x2="{y_axis+8*x_step+18}" y2="{top+12}" stroke="#b56b2e" stroke-width="1.2" stroke-dasharray="4 3"/>',
            f'<line x1="{y_axis+8}" y1="{top+12}" x2="{y_axis+8}" y2="{axis_y+15}" stroke="#b56b2e" stroke-width="1.2" stroke-dasharray="4 3"/>',
            f'<line x1="{y_axis+8*x_step+18}" y1="{top+12}" x2="{y_axis+8*x_step+18}" y2="{axis_y+15}" stroke="#b56b2e" stroke-width="1.2" stroke-dasharray="4 3"/>',
            f'<foreignObject x="130" y="{top-26}" width="220" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\({label}\\)</div></foreignObject>',
            f'<text x="390" y="{top-12}" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="12">{explanation}</text>',
            f'<foreignObject x="{x_axis_end-2}" y="{axis_y+3}" width="26" height="22"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px">\\(n\\)</div></foreignObject>',
            f'<text x="{y_axis+4}" y="{axis_y+22}" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="11">0</text>',
            f'<text x="{y_axis+8*x_step+5}" y="{axis_y+22}" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="11">7</text>',
        ))
        for n, value in enumerate(sequence):
            x = y_axis + 20 + n * x_step
            y = axis_y - value * 12
            fragments.append(f'<line x1="{x}" y1="{axis_y}" x2="{x}" y2="{y}" stroke="#0d8794" stroke-width="2"/>')
            fragments.append(f'<circle cx="{x}" cy="{y}" r="3.8" fill="#c77613"/>')
            if value:
                fragments.append(f'<text x="{x}" y="{y-8}" text-anchor="middle" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="11">{value}</text>')
    return f'''<figure data-plot="circular-shift-cycle" style="break-inside:avoid;margin:12pt 0 13pt">
<svg viewBox="0 0 980 430" role="img" aria-labelledby="circular-shift-cycle-title" style="display:block;width:100%;height:auto;border:1px solid #d6dde2;border-radius:5pt;background:#fff">
<title id="circular-shift-cycle-title">周期延拓、移位与主值区间截取</title>
<defs><marker id="ch3-shift-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#174b73"/></marker></defs>
{''.join(fragments)}
</svg>
<figcaption style="margin-top:4pt;color:#52616d;text-align:center;font-size:9.5pt">图 3-3　周期延拓、移位与主值区间截取：圆周移位的折回来自周期性，而非在区间端点补零。</figcaption>
</figure>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>3.2 离散傅里叶变换的定义及性质</h1>
<p>DFT 面向有限长序列。把长度为 [[N]] 的主值序列视作一个 [[N]] 周期序列的一个周期，DFS 的变换对就限制为有限个样值，从而得到 DFT 与 IDFT。</p>

<h2>有限长序列的周期延拓</h2>
<p>设 [[x(n)]] 仅在 [[0\leq n\leq N-1]] 给定。其周期延拓可写为 [[\widetilde{x}(n)=x((n))_N]]；[[x(n)]] 称为主值序列，区间 [[0\leq n\leq N-1]] 称为主值区间。DFT 的每一步都隐含这一周期性，不能把越界下标当作普通的零值而忽略折回。</p>

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
x\left((n-n_0)\right)_N
\quad\longleftrightarrow\quad
W_N^{k n_0}X(k).
\]</div>
<p>频域循环移位对应时域调制：</p>
<div class="formula">\[
W_N^{-n k_0}x(n)
\quad\longleftrightarrow\quad
X\left((k-k_0)\right)_N.
\]</div>
<p>下图用一个真实 8 点序列展示“周期延拓—移位—截取”的顺序；它用于避免把圆周移位误画成区间端点的普通补零移位。</p>
""" + circular_shift_cycle_svg() + r"""
<h3>例题：8 点圆周移位与反褶</h3>
<p>已知序列 (x(n)=\{1,2,3,4\})，其中第一个样值对应 (n=0)。将它补零为 8 点主值序列后，分别求下列圆周运算的主值序列。</p>
<div class="formula">\[
\begin{aligned}
x\left((n)\right)_8R_8(n)&=\{1,2,3,4,0,0,0,0\},\\
x\left((n+2)\right)_8R_8(n)&=\{3,4,0,0,0,0,1,2\},\\
x\left((n-2)\right)_8R_8(n)&=\{0,0,1,2,3,4,0,0\},\\
x\left((-n)\right)_8R_8(n)&=\{1,0,0,0,0,4,3,2\},\\
x\left((-n+2)\right)_8R_8(n)&=\{3,2,1,0,0,0,0,4\},\\
x\left((-n-2)\right)_8R_8(n)&=\{0,0,0,4,3,2,1,0\}.
\end{aligned}
\]</div>
<p>例如对最后一式取 (n=3)，有：</p>
<div class="formula">\[
x\left((-3-2)\right)_8=x\left((-5)\right)_8=x(3)=4.
\]</div>
<p>这个检验说明圆周反褶不是把有限长列表直接倒写：应先完成 8 周期延拓，再按 8 周期下标取值。</p>
<h3>例题：由频域相位因子恢复圆周移位序列</h3>
<p>若 (X(k)) 是序列 (x(n)=\left\{1,\frac{3}{4},\frac{2}{4},\frac{1}{4}\right\}) 的 4 点 DFT，第一个样值对应 (n=0)。若 (Y(k)) 是 (y(n)) 的 4 点 DFT，且：</p>
<div class="formula">\[
Y(k)=W_4^{3k}X(k),
\]</div>
<p>根据时域圆周移位性质，先保留 4 周期性，再在主值区间取值：</p>
<div class="formula">\[
\begin{aligned}
y(n)&=x\left((n-3)\right)_4R_4(n)\\
&=x\left((n+1)\right)_4R_4(n)\\
&=\left\{\frac{3}{4},\frac{2}{4},\frac{1}{4},1\right\},\qquad 0\leq n\leq3.
\end{aligned}
\]</div>

<h2>循环共轭对称与循环卷积</h2>
<p>DFT 的周期性使共轭对称也必须按 [[N]] 周期理解。任一 [[N]] 点主值序列可分解为循环共轭对称分量与循环共轭反对称分量：</p>
<div class="formula">\[
\begin{aligned}
x_{\mathrm{ep}}(n)&=\frac{1}{2}\left[x(n)+x^*\left((N-n)\right)_N\right],\\
x_{\mathrm{op}}(n)&=\frac{1}{2}\left[x(n)-x^*\left((N-n)\right)_N\right].
\end{aligned}
\]</div>
<p>它们分别对应频域的实部与虚部。特别地，实序列的 DFT 满足循环共轭对称关系：</p>
<div class="formula">\[
X(k)=X^*\left((N-k)\right)_N,\qquad 0\leq k\leq N-1.
\]</div>
<p>计算实序列 DFT 时，只需直接计算约半数频点，其余频点可由该关系复核。</p>
<p>两个 [[N]] 点序列的循环卷积定义为：</p>
<div class="formula">\[
y(n)=x_1(n)\mathbin{\circledast}_N x_2(n)
=\sum_{m=0}^{N-1}x_1(m)x_2\left((n-m)\right)_N.
\]</div>
<p>它与频域逐点相乘相对应：</p>
<div class="formula">\[
Y(k)=X_1(k)X_2(k),\qquad
y(n)=\operatorname{IDFT}\left\{X_1(k)X_2(k)\right\}.
\]</div>
  <p>手算循环卷积时依次执行：补零到 [[N]] 点、周期延拓、反褶、循环移位、逐点相乘后求和。要由循环卷积得到线性卷积，须取 [[N\geq N_1+N_2-1]]，否则首尾项会发生时域混叠。</p>
  <h3>例题：6 点圆周卷积</h3>
  <p>求下面两序列的 6 点圆周卷积：</p>
  <div class="formula">\[
  x_1(n)=R_5(n),\qquad
  x_2(n)=n+1,\quad 0\leq n\leq2.
  \]</div>
  <p>先把两列都补至 6 点主值区间。于是 [[x_1(n)=\{1,1,1,1,1,0\}]]、[[x_2(n)=\{1,2,3,0,0,0\}]]；再按循环卷积定义逐点求和：</p>
  <div class="formula">\[
  \begin{aligned}
  y(n)&=x_1(n)\mathbin{\circledast}_6 x_2(n)\\
      &=\sum_{m=0}^{5}x_1(m)x_2\left((n-m)\right)_6\\
      &=\{4,3,6,6,6,5\},\qquad 0\leq n\leq5.
  \end{aligned}
  \]</div>
<p>这里的首尾折回正是圆周卷积与线性卷积不同的地方；[[N=6]] 固定后，每个下标都按 6 周期取值。</p>

<h2>基本序列的 DFT 对</h2>
<p>下列基本变换对用于快速核对冲激、常数序列和旋转因子序列的 DFT；所有式子都在同一个 [[N]] 点主值区间内理解：</p>
<div class="formula">\[
\delta(n)R_N(n)\quad\longleftrightarrow\quad 1,\qquad
\delta(n-m)R_N(n)\quad\longleftrightarrow\quad W_N^{mk}.
\]</div>
<div class="formula">\[
R_N(n)\quad\longleftrightarrow\quad N\delta(k)R_N(k),\qquad
e^{j\frac{2\pi}{N}mn}R_N(n)\quad\longleftrightarrow\quad N\delta(k-m)R_N(k).
\]</div>
<p>其中第一组用于定位时域冲激在频域中的相位因子，第二组用于识别直流和单一 DFT 栅栏频点；它们也可作为更复杂 DFT 运算的代入检查。</p>

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
    content = normalize_legacy_inline_math(content)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
