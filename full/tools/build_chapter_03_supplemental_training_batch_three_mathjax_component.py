"""Third verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第三批）</h1>
<div class="exam-head"><span>2017 年真题（第六题第 1 小题）</span><span>详解见 P.____</span></div>
<p>六、已知一个有限长序列 \(x(n)=\delta(n)+2\delta(n-5)\)。若序列 \(y(n)\) 的 10 点离散傅里叶变换为 \(Y(k)=W_{10}^{2k}X(k)\)，求序列 \(y(n)\)；若 \(M(k)=X(k)Y(k)\)，求序列 \(m(n)\)。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2017 年真题（第六题第 2 小题）</span><span>详解见 P.____</span></div>
<p>已知 \(x(n)=\left\{1,2,3\right\}\)，\(k=0,1,2\)；\(h(n)=\left\{1,0,1,-1,0\right\}\)，\(k=0,1,2,3,4\)，求 \(x(n)\) 和 \(h(n)\) 的 5 点循环卷积。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2017 年真题（第六题第 3 小题）</span><span>详解见 P.____</span></div>
<p>一频谱分析信号处理器，抽样点数必须为 2 的整数幂，假定没有任何特殊数据处理措施，要求频率分辨率 \(F_0\leq10\,\mathrm{Hz}\)。如果采样时间间隔为 \(T=0.1\,\mathrm{ms}\)，试确定：（1）最小记录时间；（2）所允许处理的最高频率；（3）在一个记录中的最少点数。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2019 年真题（第三题）</span><span>详解见 P.____</span></div>
<p>三、简述栅栏效应的原因及解决方法。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2020 年真题（简答题第 1 小题）</span><span>详解见 P.____</span></div>
<p>二、简答题。1．什么是栅栏效应？</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2017 年真题（第六题第 1 小题）</h2>
<p>采用 DFT 的时移性质。令 \(W_N=e^{-j2\pi/N}\)，频域乘上 \(W_{10}^{2k}\) 对应时域循环右移 2 点，因此：</p>
<div class="formula">\[
y(n)=x\left((n-2)\right)_{10}=\delta(n-2)+2\delta(n-7).
\]</div>
<p>又 \(M(k)=X(k)Y(k)\)，故 \(m(n)\) 是 \(x(n)\) 与 \(y(n)\) 的 10 点循环卷积。非零样本分别位于 \(0,5\) 与 \(2,7\)，逐项相加并按长度 10 回绕：</p>
<div class="formula">\[
m(n)=5\delta(n-2)+4\delta(n-7).
\]</div>
<h2>2017 年真题（第六题第 2 小题）</h2>
<p>先将 \(x(n)\) 补零到 5 点，再作循环卷积。逐点计算：</p>
<div class="formula">\[
(x\circledast_5 h)(n)=\sum_{m=0}^{4}x(m)h\left((n-m)\right)_5.
\]</div>
<p>得到一个周期内的结果为：</p>
<div class="formula">\[
(x\circledast_5 h)(n)=\left\{-2,2,4,1,1\right\},\qquad n=0,1,2,3,4.
\]</div>
<h2>2017 年真题（第六题第 3 小题）</h2>
<p>采样频率与频率间隔为：</p>
<div class="formula">\[
f_s=\frac{1}{T}=10\,\mathrm{kHz},\qquad F_0=\frac{f_s}{N}=\frac{1}{NT}.
\]</div>
<p>由 \(F_0\leq10\,\mathrm{Hz}\) 得 \(N\geq1000\)。又 \(N\) 必须为 2 的整数幂，故取最小值 \(N=1024\)。于是：</p>
<div class="formula">\[
T_0=NT=102.4\,\mathrm{ms},\qquad
f_{\max}=\frac{f_s}{2}=5\,\mathrm{kHz},\qquad
F_0=\frac{1}{NT}=9.765625\,\mathrm{Hz}.
\]</div>
<h2>2019 年真题（第三题）</h2>
<p>有限长记录的 DFT 只在离散频率栅栏上取样。若信号实际频率没有恰好落在某个 DFT 栅栏频点，主瓣能量会分散到相邻频点，导致谱峰幅值偏低、峰值位置只能落到临近栅栏，这就是栅栏效应。</p>
<p>可通过延长有效记录时间、增大 \(N\) 以减小频率间隔，并尽量采用相干采样来减轻影响；合适的窗函数可降低泄漏。零填充只能加密显示的频率采样点，不能提高本质频率分辨率。</p>
<h2>2020 年真题（简答题第 1 小题）</h2>
<p>栅栏效应是指 DFT 只能在等间隔离散频点上给出频谱值，当真实谱线位于两个频点之间时，频谱峰值会被相邻频点分摊，因而出现频率和幅值估计偏差的现象。</p>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
