"""First verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第一批）</h1>
<div class="exam-head"><span>2003 年真题（判断题第 1 小题）</span><span>详解见 P.____</span></div>
<p>十、判断下列各题是否正确。</p>
<p>（1）如果 \(X(k)=\operatorname{DFT}[x(n)]\)，\(k=0,1,\ldots,7\)；\(y(n)=x\left((n+5)\right)_8R_8(n)\)，则 \(Y(k)=\operatorname{DFT}[y(n)]\)，\(k=0,1,\ldots,7\)，且 \(\left|Y(k)\right|=\left|X(k)\right|\)，\(k=0,1,\ldots,7\)。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2003 年真题（判断题第 3 小题）</span><span>详解见 P.____</span></div>
<p>十、判断下列各题是否正确。</p>
<p>（3）设一个稳定 IIR 滤波器的系统函数和脉冲响应分别用 \(H(z)\) 和 \(h(n)\) 表示。令 \(H(k)=H(z)\left|_{z=e^{-j2\pi k/N}}\right.\)，\(k=0,1,\ldots,N-1\)，则 \(h_N(n)=\operatorname{IDFT}[H(k)]\)，\(h(n)=h_N(n)\)。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2006 年真题（第九题）</span><span>详解见 P.____</span></div>
<p>九、一有限长序列为：\(x(n)=\delta(n)+2\delta(n-5)\)。</p>
<p>（1）求序列 \(x(n)\) 的 10 点离散傅里叶变换 DFT。</p>
<p>（2）若序列 \(y(n)\) 的 DFT 为 \(Y(k)=e^{j2k\pi/10}X(k)\)，其中 \(X(k)\) 是 \(x(n)\) 的 10 点 DFT，求序列 \(y(n)\)。</p>
<p>（3）若 10 点序列 \(y(n)\) 的 DFT 为 \(Y(k)=X(k)W(k)\)，其中 \(X(k)\) 是 \(x(n)\) 的 10 点 DFT，\(W(k)\) 是 \(w(n)\) 的 10 点 DFT，\(w(n)=\begin{cases}1,&0\leq n\leq6,\\0,&\text{其他},\end{cases}\) 求序列 \(y(n)\)。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2006 年真题（第十二题）</span><span>详解见 P.____</span></div>
<p>十二、假设以 \(8\,\mathrm{kHz}\) 速率对一段长为 \(10\,\mathrm{s}\) 的语音信号采样，现用一长度为 \(L=64\) 的 FIR 滤波器 \(h(n)\) 对其进行滤波，若采用 DFT 为 1024 点的重叠保留法，那么共需多少次 DFT 变换和多少次 IDFT 变换来进行卷积？</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2007 年真题（填空题第 2 小题）</span><span>详解见 P.____</span></div>
<p>九、填空题。（2）序列 \(x(n)\) 为 100 点有限长的序列，除 \(z\) 变换 \(X(z)\) 在单位圆上至少进行________点取样，才能通过同样点数的 IDFT 恢复出原序列。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2007 年真题（简答题第 2 小题）</span><span>详解见 P.____</span></div>
<p>十、简答题。（2）频谱泄露产生的主要原因是什么？可以用什么方法加以改善？</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2003 年真题（判断题第 1 小题）</h2>
<p><strong>结论：正确。</strong>对 8 点序列，\(y(n)=x\left((n+5)\right)_8\) 是循环时移。DFT 时移性质给出：</p>
<div class="formula">\[
Y(k)=e^{j2\pi k\cdot5/8}X(k).
\]</div>
<p>相乘因子的模恒为 1，因此：</p><div class="formula">\[
\left|Y(k)\right|=\left|X(k)\right|,\qquad k=0,1,\ldots,7.
\]</div>
<h2>2003 年真题（判断题第 3 小题）</h2>
<p><strong>结论：不正确。</strong>将稳定 IIR 的 \(H(z)\) 在单位圆等间隔取 \(N\) 点并作 IDFT，得到的是其单位脉冲响应的 \(N\) 点周期叠加，而不是一般意义上的原响应：</p>
<div class="formula">\[
h_N(n)=\sum_{r=-\infty}^{\infty}h(n-rN).
\]</div>
<p>稳定只保证该叠加收敛；IIR 的 \(h(n)\) 通常无限长，故周期叠加项一般不为零，不能断言 \(h(n)=h_N(n)\)。</p>
<h2>2006 年真题（第九题）</h2>
<div class="answer-step"><strong>（1）10 点 DFT。</strong>利用冲激的时移性质：</div>
<div class="formula">\[
X(k)=1+2e^{-j2\pi k\cdot5/10}=1+2e^{-j\pi k}=1+2(-1)^k,\qquad k=0,1,\ldots,9.
\]</div>
<div class="answer-step"><strong>（2）循环时移。</strong>正指数因子对应将时域序列向左循环移位 2 点：</div>
<div class="formula">\[
y(n)=x\left((n+2)\right)_{10}.
\]</div>
<p>故一个周期内 \(y(3)=2\)、\(y(8)=1\)，其余样值为零。</p>
<div class="answer-step"><strong>（3）循环卷积。</strong>频域相乘对应 10 点循环卷积：</div>
<div class="formula">\[
y(n)=x(n)\mathbin{\circledast}_{10}w(n)=w(n)+2w\left((n-5)\right)_{10}.
\]</div>
<p>逐个 \(n=0,1,\ldots,9\) 计算：</p>
<div class="formula">\[
y(n)=\left\{3,3,1,1,1,3,3,2,2,2\right\},\qquad 0\leq n\leq9.
\]</div>
<h2>2006 年真题（第十二题）</h2>
<p>语音样本总数为：</p><div class="formula">\[
N_x=8\times10^3\times10=80000.
\]</div>
<p>重叠保留法中，1024 点 DFT、长度 64 的 FIR 每段可保留的有效输出长度为：</p>
<div class="formula">\[
L_b=1024-64+1=961.
\]</div>
<p>需要的数据块数为：</p><div class="formula">\[
B=\left\lceil\frac{80000}{961}\right\rceil=84.
\]</div>
<p>滤波器频响 \(H(k)\) 预先计算一次，之后每块各作一次输入 DFT 与一次 IDFT。因此共需 \(85\) 次 DFT（含预先计算 \(H(k)\)）和 \(84\) 次 IDFT；若题目约定 \(H(k)\) 已预先给定，则在线卷积阶段为 84 次 DFT、84 次 IDFT。</p>
<h2>2007 年真题（填空题第 2 小题）</h2>
<p>长度为 100 的有限长序列以 \(N\) 点单位圆采样后作 \(N\) 点 IDFT，会形成 \(N\) 点周期叠加。为避免样值折叠，必须有：</p>
<div class="formula">\[
N\geq100.
\]</div>
<p>填：<strong>100</strong> 点。</p>
<h2>2007 年真题（简答题第 2 小题）</h2>
<p>频谱泄露的直接原因是有限长记录相当于把原信号乘以一个时间窗。频域中于是发生卷积：原本集中在某一频点的谱，会因窗函数的主瓣和旁瓣扩散到相邻频点；当观察时间不是信号周期的整数倍时，泄露尤为明显。</p>
<p>改善方法是：加长有效记录时间以减小主瓣宽度；使采样记录尽可能包含整数个周期；并在允许的幅度精度／分辨率权衡下选用旁瓣较低的窗函数。后补零只能使显示的频率取样更密，不能替代加长有效记录时间。</p>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
