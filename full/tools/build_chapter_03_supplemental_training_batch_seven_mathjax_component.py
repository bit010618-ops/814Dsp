"""Seventh verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第七批）</h1>
<div class="exam-head"><span>2003 年真题</span><span>详解见 P.____</span></div>
<p>七、用 DFT 对模拟信号进行谱分析，设模拟信号 \(x_a(t)\) 的最高频率为 \(200\,\mathrm{Hz}\)，以 Nyquist 频率采样得到时域离散序列 \(x(n)=x_a(nT)\)，要求频率分辨率为 \(10\,\mathrm{Hz}\)，求序列 \(x(n)\) 的离散傅里叶变换 \(X(k)\) 各 \(k\) 点对应的数字频率 \(\omega_k\)（弧）和模拟频率 \(f_k\)（Hz）的值。</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2003 年真题</h2>
<p>最高模拟频率为 \(200\,\mathrm{Hz}\)，按 Nyquist 频率采样，采样频率与采样周期为：</p>
<div class="formula">\[
f_s=400\,\mathrm{Hz}=2\times200\,\mathrm{Hz},\qquad T=\frac{1}{400}\,\mathrm{s}.
\]</div>
<p>频率分辨率就是相邻 DFT 频率采样点的间隔，故 DFT 长度为：</p>
<div class="formula">\[
F_0=\frac{f_s}{N}=10\,\mathrm{Hz},\qquad N=\frac{400}{10}=40.
\]</div>
<p>对 \(N=40\) 点 DFT，\(k=0,1,\ldots,39\) 对应的数字频率为：</p>
<div class="formula">\[
\omega_k=\frac{2\pi k}{40}=\frac{k\pi}{20}\quad\text{（弧）}.
\]</div>
<p>模拟频率按 DFT 的通常频率标记分为正频率和负频率两段：</p>
<div class="formula">\[
f_k=
\begin{cases}
k\times10\,\mathrm{Hz}, & k=0,1,\ldots,20,\\
(k-40)\times10\,\mathrm{Hz}, & k=21,22,\ldots,39.
\end{cases}
\]</div>
<p>因此 \(k=0\) 对应直流，\(k=1\) 至 \(20\) 依次对应 \(10\) 至 \(200\,\mathrm{Hz}\)，而 \(k=21\) 至 \(39\) 依次对应 \(-190\) 至 \(-10\,\mathrm{Hz}\)。</p>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
