"""Chapter-three §3.3 LSI output methods in a MathJax component."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}</style>"""


def six_point_circular_convolution_svg() -> str:
    """Show real six-point samples through the circular-convolution construction."""

    panels = (
        (44, r"x_1(n)=R_5(n)", (1, 1, 1, 1, 1, 0), "补零到 6 点主值区间"),
        (164, r"x_2(n)", (1, 2, 3, 0, 0, 0), "第二个序列补零"),
        (284, r"x_2\left((-n)\right)_6", (1, 0, 0, 0, 3, 2), "反褶后按 6 周期折回"),
        (404, r"y(n)", (4, 3, 6, 6, 6, 5), "逐次循环移位、相乘求和的输出"),
    )

    def panel(top: int, label: str, values: tuple[int, ...], note: str, output: bool) -> str:
        y_axis, baseline, step = 115, top + 72, 100
        parts = [
            f'<line x1="70" y1="{baseline}" x2="870" y2="{baseline}" stroke="#174b73" stroke-width="1.7" marker-end="url(#ch3-conv-arrow)"/>',
            f'<line x1="{y_axis}" y1="{baseline+25}" x2="{y_axis}" y2="{top+22}" stroke="#174b73" stroke-width="1.5" marker-end="url(#ch3-conv-arrow)"/>',
            f'<foreignObject x="132" y="{top-8}" width="170" height="25"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px">\\({label}\\)</div></foreignObject>',
            f'<text x="360" y="{top+7}" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="12">{note}</text>',
            f'<foreignObject x="878" y="{baseline+2}" width="24" height="22"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:13px">\\(n\\)</div></foreignObject>',
        ]
        for n, value in enumerate(values):
            x = y_axis + 24 + n * step
            y = baseline - value * (8 if output else 13)
            parts.append(f'<line x1="{x}" y1="{baseline}" x2="{x}" y2="{y}" stroke="#0d8794" stroke-width="2"/>')
            parts.append(f'<circle cx="{x}" cy="{y}" r="3.8" fill="#c77613"/>')
            if value:
                parts.append(f'<text x="{x}" y="{y-8}" text-anchor="middle" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="11">{value}</text>')
        return ''.join(parts)

    return f'''<figure data-plot="six-point-circular-convolution" style="break-inside:avoid;margin:12pt 0 13pt">
<svg viewBox="0 0 980 515" role="img" aria-labelledby="six-point-circular-convolution-title" style="display:block;width:100%;height:auto;border:1px solid #d6dde2;border-radius:5pt;background:#fff">
<title id="six-point-circular-convolution-title">补零、周期延拓、反褶与循环移位</title>
<defs><marker id="ch3-conv-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#174b73"/></marker></defs>
{panel(*panels[0], False)}{panel(*panels[1], False)}{panel(*panels[2], False)}{panel(*panels[3], True)}
</svg>
<figcaption style="margin-top:4pt;color:#52616d;text-align:center;font-size:9.5pt">图 3-4　补零、周期延拓、反褶与循环移位：最后一行给出六个循环卷积输出样本。</figcaption>
</figure>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>3.3 用 DFT 求解 LSI 系统输出</h1>
<p>对有限长输入 [[x(n)]] 和有限长单位脉冲响应 [[h(n)]]，线性卷积可转化为 DFT 域的逐点相乘。关键不是“做一次 DFT”本身，而是选择足够的变换长度以避免循环混叠。</p>
<h2>DFT 求线性卷积</h2>
<p>若 [[x(n)]] 长度为 [[N_1]]、[[h(n)]] 长度为 [[N_2]]，线性卷积长度为 [[N_1+N_2-1]]。两序列均补零到 [[N]] 点后，作 [[N]] 点 DFT：</p>
<div class="formula">\[
X(k)=\operatorname{DFT}_N\{x(n)\},\quad H(k)=\operatorname{DFT}_N\{h(n)\},\quad Y(k)=X(k)H(k).
\]</div>
<p>再作 [[N]] 点 IDFT 得到循环卷积。只有满足：</p>
<div class="formula">\[
N\geq N_1+N_2-1
\]</div>
<p>时，主值区间内的循环卷积才与线性卷积完全相同；当 [[N]] 不足时，线性卷积尾部会折回并叠加到前部。</p>
<div class="formula">\[
y(n)=\operatorname{IDFT}_N\{X(k)H(k)\}=y_l\left((n)\right)_N.
\]</div>

<h2>例题：不同长度的圆周卷积</h2>
<p>求下面两序列的线性卷积和 4 点、5 点、6 点、7 点圆周卷积。</p>
<div class="formula">\[
x_1(n)=R_5(n),\qquad x_2(n)=n+1,\quad 0\leq n\leq2.
\]</div>
<p>将两个序列写成主值区间内的有限长序列，分别为 [[\{1,1,1,1,1\}]] 与 [[\{1,2,3\}]]。线性卷积是后续比较的基准：</p>
<div class="formula">\[
y_l(n)=x_1(n)*x_2(n)=\{1,3,6,6,6,5,3\},\qquad 0\leq n\leq6.
\]</div>
<p>圆周卷积的结果由该线性卷积以相应长度作周期延拓后，在主值区间逐项相加得到：</p>
<div class="formula">\[
\begin{aligned}
y_4(n)&=\{7,8,9,6\}, &&0\leq n\leq3,\\
y_5(n)&=\{6,6,6,6,6\}, &&0\leq n\leq4,\\
y_6(n)&=\{4,3,6,6,6,5\}, &&0\leq n\leq5,\\
y_7(n)&=\{1,3,6,6,6,5,3\}, &&0\leq n\leq6.
\end{aligned}
\]</div>
<p>下图将补零、反褶和循环移位的关键样本放在同一坐标体系中；它用于解释首尾为何按周期折回并得到各个输出样值。</p>
""" + six_point_circular_convolution_svg() + r"""
<p>前 3 种长度均小于线性卷积长度 [[7]]，末尾样本会折回并造成时域混叠；当 [[N=7=N_1+N_2-1]] 时，7 点圆周卷积恰与线性卷积一致。</p>

<h2>例题：4 点 DFT 的自卷积</h2>
<p>序列 [[x(n)=\delta(n)+2\delta(n-2)+\delta(n-3)]]，试求：（A）序列 [[x(n)]] 的 4 点 DFT；（B）若 [[y(n)]] 是 [[x(n)]] 与它本身的 4 点圆周卷积，求 [[y(n)]] 及其 4 点 DFT。</p>
<p>先把序列按 4 点主值区间写为 [[\{1,0,2,1\}]]。其 4 点 DFT 是下式；它给出频域逐点相乘所需的谱值：</p>
<div class="formula">\[
\begin{aligned}
X(k)&=\sum_{n=0}^{3}x(n)W_4^{nk}=1+2W_4^{2k}+W_4^{3k},\\
X(0)&=4,\qquad X(1)=-1+j,\qquad X(2)=2,\qquad X(3)=-1-j.
\end{aligned}
\]</div>
<p>时域直接求 4 点圆周卷积，得到：</p>
<div class="formula">\[
y(n)=x(n)\circledast_4x(n)=\{5,4,5,2\},\qquad 0\leq n\leq3.
\]</div>
<p>也可在频域平方后反变换。这个式子说明“时域圆周卷积”与“频域逐点相乘”完全对应：</p>
<div class="formula">\[
Y(k)=X(k)X(k),\qquad y(n)=\operatorname{IDFT}_4\{Y(k)\}.
\]</div>

<h2>计算路线的选择</h2>
<p>短序列可直接在时域逐项求和；已知解析频谱时可在频域相乘后反变换；当序列较长且滤波器为有限长时，采用 DFT/FFT 分块算法更有效。三种路线的数学结果一致，区别在于计算量与中间组织方式。</p>

<h2>重叠相加法</h2>
<p>设输入被分成长度 [[M]] 的互不重叠分段 [[x_i(n)]]，滤波器长度为 [[N_2]]。每一段的线性卷积长度为 [[M+N_2-1]]，取 DFT 长度 [[L\geq M+N_2-1]] 后不会在本段内产生循环混叠。</p>
<ol class="steps">
<li>将 [[h(n)]] 补零到 [[L]] 点，预先求 [[H(k)]]。</li>
<li>每一段 [[x_i(n)]] 补零到 [[L]] 点，求 [[X_i(k)]]。</li>
<li>计算 [[Y_i(k)=X_i(k)H(k)]]，再作 [[L]] 点 IDFT 得 [[y_i(n)]]。</li>
<li>把相邻分段输出的重叠部分相加，形成总输出。</li>
</ol>
<div class="formula">\[
y(n)=\sum_i y_i(n-iM),\qquad L\geq M+N_2-1.
\]</div>
<p>重叠相加法中没有丢弃样本；重叠区的各段贡献必须相加。</p>

<h3>例题：重叠相加法验证</h3>
<p>求下面两序列的线性卷积，并用重叠相加法验证。</p>
<div class="formula">\[
x(n)=(n+1)R_8(n),\qquad h(n)=R_3(n).
\]</div>
<p>下面的参数式给出分块长度与所取 DFT 长度；把 [[x(n)]] 分成两段 [[\{1,2,3,4\}]]、[[\{5,6,7,8\}]] 后，每段的 6 点计算结果就是该段的线性卷积：</p>
<div class="formula">\[
M=4,\qquad N_2=3,\qquad L_0=M+N_2-1=6.
\]</div>
<div class="formula">\[
\begin{aligned}
y_0(n)&=\{1,3,6,9,7,4\},\\
y_1(n)&=\{5,11,18,21,15,8\}.
\end{aligned}
\]</div>
<p>第二段输出右移 [[M=4]] 点后与第一段相加；下式给出重叠相加的最终线性卷积结果：</p>
<div class="formula">\[
y(n)=y_0(n)+y_1(n-4)=\{1,3,6,9,12,15,18,21,15,8\}.
\]</div>

<h2>重叠保留法</h2>
<p>重叠保留法的输入分段包含前一段末尾的 [[N_2-1]] 个样本。每段新增 [[M]] 个样本，因此输入块长度为：</p>
<div class="formula">\[
L_0=M+N_2-1.
\]</div>
<ol class="steps">
<li>每段保留前 [[N_2-1]] 个历史样本，并接入 [[M]] 个新样本。</li>
<li>取 [[L\geq L_0]]，对输入块和 [[h(n)]] 补零后作 DFT，相乘并 IDFT。</li>
<li>每段输出的前 [[N_2-1]] 点含有循环混叠，全部舍去；保留后 [[M]] 点并依次拼接。</li>
</ol>
<p>“重叠保留”中的保留指输入的重叠样本，而输出中恰恰要舍弃混叠的前 [[N_2-1]] 点。两种方法都以线性卷积长度为尺度选取 DFT 长度。</p>

<h3>例题：重叠保留法验证</h3>
<p>仍求 [[x(n)=(n+1)R_8(n)]] 与 [[h(n)=R_3(n)]] 的线性卷积。取 [[M=4]]、[[N_2=3]]，输入块长度为 [[L_0=6]]；相邻输入块保留 2 个历史样本。</p>
<div class="formula">\[
\begin{aligned}
x_0&=\{0,0,1,2,3,4\}, & y_0&=\{7,4,\underline{1,3,6,9}\},\\
x_1&=\{3,4,5,6,7,8\}, & y_1&=\{18,15,\underline{12,15,18,21}\},\\
x_2&=\{7,8,0,0,0,0\}, & y_2&=\{7,15,\underline{15,8,0,0}\}.
\end{aligned}
\]</div>
<p>每块输出前 2 点带有循环混叠，不能使用；下划线标出每块后 4 个保留点。最后一块的补零部分只用于结束计算，因此只取其中对应原输入的 [[15,8]]。按块拼接后得到：</p>
<div class="formula">\[
y(n)=\{1,3,6,9,12,15,18,21,15,8\}.
\]</div>

<h2>例题：循环卷积长度的判定</h2>
<p>对长度分别为 [[N_1=7]] 和 [[N_2=3]] 的两个序列，其线性卷积长度为 [[9]]。若取 [[N=8]]，结果会有尾部样本折回到主值区间而产生混叠；取 [[N=9]] 或更长时，[[N]] 点循环卷积与线性卷积一致。</p>
<div class="formula">\[
7+3-1=9,\qquad N\geq9.
\]</div>
<h2>例题：DFT 卷积的无混叠区间</h2>
<p>对 50 点长序列 [[x(n)]], [[0\leq n\leq49]] 和 20 点长序列 [[h(n)]], [[0\leq n\leq19]] 分别做 50 点的 DFT，得到 [[X(k)]] 和 [[H(k)]]，令 [[Y(k)=X(k)H(k)]], [[0\leq k\leq49]]，[[y(n)]] 是 [[Y(k)]] 的 50 点 IDFT 的值，则 [[n]] 在______范围内时，[[y(n)]] 的结果与 [[x(n)]] 和 [[h(n)]] 线性卷积的结果一致。</p>
<p>（A）[[19\leq n\leq48]]　（B）[[19\leq n\leq49]]　（C）[[20\leq n\leq49]]　（D）[[20\leq n\leq68]]。</p>
<p>解：线性卷积长度为 [[50+20-1=69]]，而 50 点圆周卷积把末尾的 19 个样本折回主值区间前端。因此前 [[19]] 个样本发生时域混叠，[[19\leq n\leq49]] 的 31 个样本未受折回项影响，故选择（B）。</p>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    html = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(html, encoding="utf-8")
    return output
