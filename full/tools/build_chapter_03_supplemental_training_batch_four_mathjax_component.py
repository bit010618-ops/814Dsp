"""Fourth verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第四批）</h1>
<div class="exam-head"><span>2020 年真题（第三题）</span><span>详解见 P.____</span></div>
<p>三、已知 \(x[n]=4\delta[n]+7\delta[n-1]+3\delta[n-2]+\delta[n-3]+2\delta[n-4]\)，其 6 点 DFT 是 \(X(k)\)，\(Y(k)=X(3k)\)，\(k=0,1\)，求 \(Y(k)\) 的 2 点 IDFT。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2020 年真题（第五题）</span><span>详解见 P.____</span></div>
<p>五、已知序列 \(x[n]=4\delta[n]+3\delta[n-1]+2\delta[n-2]+\delta[n-3]\)，其 6 点离散傅里叶变换（DFT）用 \(X(k)\) 表示，试解下列问题：（1）若序列 \(y[n]\) 的长度为 6，其 6 点离散傅里叶变换为 \(Y(k)=W_6^{4k}X(k)\)，求 \(y[n]\)；（2）求 \(x[n]*x[n]\)。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2023 年真题（DSP 第 3 小题）</span><span>详解见 P.____</span></div>
<p>七、DSP 简答题。3．\(x(n)=nR_6(n)\)，\(X(k)\) 是 \(x(n)\) 的 10 点 DFT，设序列 \(y(n)\) 的 10 点 DFT 为 \(Y(k)\)，假设有 \(Y(k)=X(k)\cos\left(\frac{2\pi}{5}k\right)\)，求 \(y(n)\)。</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2020 年真题（第三题）</h2>
<p>对 6 点频谱以 3 为间隔抽取，得到的 2 点 IDFT 是原序列按间隔 2 的周期叠加：</p>
<div class="formula">\[
y(n)=x(n)+x(n+2)+x(n+4),\qquad n=0,1.
\]</div>
<p>因此：</p>
<div class="formula">\[
y(0)=4+3+2=9,\qquad y(1)=7+1=8.
\]</div>
<h2>2020 年真题（第五题）</h2>
<p>频域乘以 \(W_6^{4k}\) 对应长度 6 的时域循环右移 4 点：</p>
<div class="formula">\[
y(n)=x\left((n-4)\right)_6
=2\delta(n)+\delta(n-1)+4\delta(n-4)+3\delta(n-5).
\]</div>
<p>第二问为 6 点循环卷积。先计算线性卷积，再把第 6 点的尾项回绕到第 0 点，故一个周期内为：</p>
<div class="formula">\[
(x\circledast_6x)(n)=\left\{17,24,25,20,10,4\right\},\qquad n=0,1,\ldots,5.
\]</div>
<h2>2023 年真题（DSP 第 3 小题）</h2>
<p>将余弦分解为两个复指数，并采用 DFT 时移性质：</p>
<div class="formula">\[
\cos\left(\frac{2\pi}{5}k\right)
=\frac{1}{2}\left(W_{10}^{2k}+W_{10}^{-2k}\right).
\]</div>
<p>所以：</p>
<div class="formula">\[
y(n)=\frac{1}{2}\left[x\left((n-2)\right)_{10}+x\left((n+2)\right)_{10}\right].
\]</div>
<p>由 \(x(n)=nR_6(n)\)，一个 10 点周期内 \(x(n)=\left\{0,1,2,3,4,5,0,0,0,0\right\}\)，从而：</p>
<div class="formula">\[
y(n)=\left\{1,\frac{3}{2},2,3,1,\frac{3}{2},2,\frac{5}{2},0,\frac{1}{2}\right\},
\qquad n=0,1,\ldots,9.
\]</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
