"""Chapter-three §3.3 LSI output methods in a MathJax component."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}</style>"""


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
y(n)=\operatorname{IDFT}_N\{X(k)H(k)\}=y_l\left((n)\bmod N\right).
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
