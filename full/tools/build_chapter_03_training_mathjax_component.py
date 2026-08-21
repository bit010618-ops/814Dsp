"""Reusable chapter-three training and final-answer components."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:20pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.exam-page{break-before:page;min-height:230mm}.exam-page:first-child{break-before:auto}.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:0 0 10pt}.formula{break-inside:avoid;padding:7pt 4pt;margin:8pt 0;text-align:center;overflow-x:auto}.writing-space{min-height:105mm}.answer-step{break-inside:avoid;margin:8pt 0}.answer-step strong{color:#315d7c}@media(max-width:560px){body{font-size:10.5pt}}</style>"""


def _document(content: str) -> str:
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 分章强化训练</h1>
<div class="exam-head"><span>2003 年真题</span><span>详解见 P.____</span></div>
<p>七、用 DFT 对模拟信号进行谱分析，设模拟信号 \(x_a(t)\) 的最高频率为 200 Hz，以 Nyquist 频率采样得到时域离散序列 \(x(n)=x_a(nT)\)，要求频率分辨率为 10 Hz，求序列 \(x(n)\) 的离散傅里叶变换 \(X(k)\) 各 \(k\) 点对应的数字频率 \(\omega_k\)（弧）和模拟频率 \(f_k\)（Hz）的值。</p>
<div class="writing-space"></div></section>
<section class="exam-page">
<div class="exam-head"><span>2002 年真题</span><span>详解见 P.____</span></div>
<p>九、已知 \(x_1(n)=\left(\frac{1}{2}\right)^n,\ 0\leq n\leq4\)，\(x_2(n)=1,\ 0\leq n\leq2\)，且 \(X_1(K)=\operatorname{DFT}[x_1(n)]\)，\(X_2(K)=\operatorname{DFT}[x_2(n)]\)，求 \(x_3(n)=\operatorname{IDFT}\left[X_1(K)X_2(K)\right]\)。</p>
<div class="writing-space"></div></section>
<section class="exam-page">
<div class="exam-head"><span>2002 年真题（第十题）</span><span>详解见 P.____</span></div>
<p>十、已知序列 \(h(n)\) 是 \(h(t)\) 的 9 点取样 \(0\leq n\leq8\)，取样间隔 \(T=0.15\,\mathrm{s}\)，问如何用 DFT 计算其频谱，使频谱分辨率高于 \(2\,\mathrm{rad/s}\)？</p>
<div class="writing-space"></div></section>
<section class="exam-page">
<div class="exam-head"><span>2005 年真题</span><span>详解见 P.____</span></div>
<p>九、已知两个序列：\(x(n)=\delta(n)+3\delta(n-1)+3\delta(n-2)+2\delta(n-5)\)，\(h(n)=\delta(n)+\delta(n-1)+\delta(n-2)+\delta(n-3)\)。其中 \(X(K)\) 和 \(H(K)\) 分别是 \(x(n)\) 和 \(h(n)\) 的 5 点 DFT，对 \(Y(K)=X(K)H(K)\) 做 IDFT，得到序列 \(y(n)\)，求 \(y(n)\)。</p>
<div class="writing-space"></div></section>
<section class="exam-page">
<div class="exam-head"><span>2004 年真题</span><span>详解见 P.____</span></div>
<p>十、设 \(x(t)\) 的最高频率 \(f_h\) 不超过 3 Hz，现用 \(f_s=100\,\mathrm{Hz}\) 对 \(x(t)\) 取样 256 点，得到 \(x(n)\)。</p>
<p>（1）对 \(x(n)\) 做 DFT 时，所能得到的最大频率分辨率是多少？</p>
<p>（2）如果信号由三个正弦组成，其频率分别是 \(f_1=2\,\mathrm{Hz}\)，\(f_2=2.02\,\mathrm{Hz}\)，\(f_3=2.07\,\mathrm{Hz}\)，即 \(x(t)=\sin(2\pi f_1t)+\sin(2\pi f_2t)+\sin(2\pi f_3t)\)，求取样后的 \(x(n)\) 的 DFT 简图。</p>
<div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>真题整理详解</h1>
<h2>2003 年真题</h2>
<p>用 DFT 对模拟信号进行谱分析。</p>
<div class="answer-step"><strong>第 1 步：确定采样频率。</strong>题目规定按 Nyquist 频率采样，最高频率为 \(200\,\mathrm{Hz}\)，故：</div>
<div class="formula">\[
f_s=2\times200=400\,\mathrm{Hz}.
\]</div>
<div class="answer-step"><strong>第 2 步：由频率分辨率确定 DFT 点数。</strong>DFT 的频率间隔为 \(F_0=f_s/N\)。由 \(F_0=10\,\mathrm{Hz}\) 得：</div>
<div class="formula">\[
N=\frac{f_s}{F_0}=40.
\]</div>
<div class="answer-step"><strong>第 3 步：写出第 \(k\) 个频点的数字频率。</strong>对 \(N=40\) 点 DFT，频率取样点为：</div>
<div class="formula">\[
\omega_k=\frac{2\pi k}{N}=\frac{2\pi k}{40}=\frac{\pi k}{20}\ \mathrm{rad},
\qquad k=0,1,\ldots,39.
\]</div>
<div class="answer-step"><strong>第 4 步：写出对应的模拟频率。</strong>每个频点间隔为 \(10\,\mathrm{Hz}\)，因此：</div>
<div class="formula">\[
f_k=kF_0=10k\,\mathrm{Hz},
\qquad k=0,1,\ldots,39.
\]</div>
<p>因此，\(k=0\) 对应直流，\(k=20\) 对应 Nyquist 频率 \(200\,\mathrm{Hz}\)。在 DFT 的一个周期内，\(k=21,\ldots,39\) 也可按负频率解释为 \(f_k=(k-40)\times10\,\mathrm{Hz}\)。</p>
<h2>2002 年真题</h2>
<p>已知 \(x_1(n)=\left(\frac{1}{2}\right)^n,\ 0\leq n\leq4\)，\(x_2(n)=1,\ 0\leq n\leq2\)，且 \(X_1(K)=\operatorname{DFT}[x_1(n)]\)，\(X_2(K)=\operatorname{DFT}[x_2(n)]\)，求 \(x_3(n)=\operatorname{IDFT}\left[X_1(K)X_2(K)\right]\)。</p>
<div class="answer-step"><strong>第 1 步：识别 DFT 域乘法。</strong>由 DFT 的循环卷积性质：</div>
<div class="formula">\[
x_3(n)=x_1(n)\mathbin{\circledast}_N x_2(n).
\]</div>
<p>原题没有给出 DFT 点数 \(N\)，故不能把答案擅自写成唯一的固定数列；一般答案应按所用 \(N\) 点的循环卷积理解。</p>
<div class="answer-step"><strong>第 2 步：给出无混叠的常用情形。</strong>两序列长度分别为 5 与 3。若希望结果等于线性卷积，必须满足：</div>
<div class="formula">\[
N\geq5+3-1=7.
\]</div>
<p>此时逐项相加得到：</p>
<div class="formula">\[
x_3(n)=\left\{1,\frac{3}{2},\frac{7}{4},\frac{7}{8},\frac{7}{16},\frac{3}{16},\frac{1}{16}\right\},
\qquad 0\leq n\leq6.
\]</div>
<p>若实际 DFT 点数小于 7，应将这七个线性卷积样值按该 \(N\) 点周期折回相加，得到相应的循环卷积结果。</p>
<h2>2002 年真题（第十题）</h2>
<p>已知序列 \(h(n)\) 是 \(h(t)\) 的 9 点取样 \(0\leq n\leq8\)，取样间隔 \(T=0.15\,\mathrm{s}\)，问如何用 DFT 计算其频谱，使频谱分辨率高于 \(2\,\mathrm{rad/s}\)？</p>
<div class="answer-step"><strong>第 1 步：写出 DFT 的角频率间隔。</strong>对 \(N\) 点 DFT，模拟角频率的取样间隔为：</div>
<div class="formula">\[
\Delta\Omega=\frac{2\pi}{NT}.
\]</div>
<div class="answer-step"><strong>第 2 步：由分辨率要求确定点数。</strong>“高于 \(2\,\mathrm{rad/s}\)”即要求频率间隔小于 \(2\,\mathrm{rad/s}\)，故：</div>
<div class="formula">\[
\frac{2\pi}{N\times0.15}<2
\quad\Longrightarrow\quad
N>\frac{2\pi}{2\times0.15}\approx20.94.
\]</div>
<p>因此取 \(N\geq21\)。为了使用常用的基 2 FFT，可将原有 9 点样值后补零，取 \(N=32\) 点 DFT。此时：</p>
<div class="formula">\[
\Delta\Omega=\frac{2\pi}{32\times0.15}\approx1.309\,\mathrm{rad/s}<2\,\mathrm{rad/s}.
\]</div>
<p>零填充使频域取样点更密，便于观察频谱；原始有效记录仍为 9 个样本，应同时保留这一点以区分频谱显示加密与记录长度带来的本征分辨能力。</p>
<h2>2005 年真题</h2>
<p>已知两个序列：\(x(n)=\delta(n)+3\delta(n-1)+3\delta(n-2)+2\delta(n-5)\)，\(h(n)=\delta(n)+\delta(n-1)+\delta(n-2)+\delta(n-3)\)。其中 \(X(K)\) 和 \(H(K)\) 分别是 \(x(n)\) 和 \(h(n)\) 的 5 点 DFT，对 \(Y(K)=X(K)H(K)\) 做 IDFT，得到序列 \(y(n)\)，求 \(y(n)\)。</p>
<div class="answer-step"><strong>第 1 步：按 5 点 DFT 的周期处理序列。</strong>频域相乘再作 5 点 IDFT，对应 5 点循环卷积。由于 \(\delta(n-5)\) 与 \(\delta(n)\) 在 5 点周期内重合，先把一个周期写为：</div>
<div class="formula">\[
x_5(n)=\{3,3,3,0,0\},\qquad h_5(n)=\{1,1,1,1,0\},\qquad 0\leq n\leq4.
\]</div>
<div class="answer-step"><strong>第 2 步：计算 5 点循环卷积。</strong>由 DFT 的卷积定理：</div>
<div class="formula">\[
y(n)=x_5(n)\mathbin{\circledast}_5h_5(n).
\]</div>
<p>逐个循环索引相加，可得：</p>
<div class="formula">\[
\begin{aligned}
y(0)&=3+3=6, & y(1)&=3+3=6,\\
y(2)&=3+3+3=9, & y(3)&=3+3+3=9,\\
y(4)&=3+3=6.
\end{aligned}
\]</div>
<p>因此，一个周期内的结果为：</p>
<div class="formula">\[
y(n)=\{6,6,9,9,6\},\qquad 0\leq n\leq4,
\]</div>
<p>并按 5 为周期延拓。此题的关键是不能把 \(\delta(n-5)\) 当作普通线性卷积中的新位置；题目已明确使用 5 点 DFT，它应先折回到 \(n=0\)。</p>
<h2>2004 年真题</h2>
<p>设 \(x(t)\) 的最高频率 \(f_h\) 不超过 3 Hz，现用 \(f_s=100\,\mathrm{Hz}\) 对 \(x(t)\) 取样 256 点，得到 \(x(n)\)。</p>
<div class="answer-step"><strong>（1）频谱间隔。</strong>DFT 的频率分辨率（频谱间隔）为：</div>
<div class="formula">\[
F_0=\frac{f_s}{N}=\frac{100}{256}=0.390625\,\mathrm{Hz}.
\]</div>
<div class="answer-step"><strong>（2）三正弦的 DFT 观察结果。</strong>三条谱线都位于 2 Hz 附近；最大频差为：</div>
<div class="formula">\[
\left|f_3-f_1\right|=0.07\,\mathrm{Hz}&lt;F_0.
\]</div>
<p>因此在该 256 点记录下，三条正弦分量不能作为三条独立谱线分辨。正频率一侧的主要能量集中在最接近 2 Hz 的 DFT 栅栏 \(k\approx2/F_0=5.12\) 附近，负频率一侧出现相应的共轭对称能量；由于频率没有恰落在栅栏上，会伴随谱泄漏。简图应画成 \(k\approx5\) 附近的一团相邻谱线及其负频率对称部分，而不是三根可分开的谱线。</p>
<p>若要分辨这些分量，必须延长有效记录时间以减小 \(F_0\)，而非仅把已有 256 点后面补零。</p>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
