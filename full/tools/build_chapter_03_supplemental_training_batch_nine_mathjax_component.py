"""Ninth verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第九批）</h1>
<div class="exam-head"><span>2025 年真题（第七题第 2 小题）</span><span>详解见 P.____</span></div>
<p>七、简答题。2．已知 \(x(n)=\left(\frac{1}{2}\right)^n u(n)\)，其傅里叶变换为 \(X(e^{j\omega})\)，另外一个长度为 4 的有限长序列 \(y(n)\)，\(0\leq n\leq3\)，其 4 点 DFT 为 \(Y(k)=X(e^{j\omega})\big|_{\omega=\frac{\pi}{2}k}\)，\(0\leq n\leq3\)，求 \(y(n)\) 的表达式。</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2025 年真题（第七题第 2 小题）</h2>
<p>把 DTFT 在 \(N=4\) 个等间隔频率点上采样，再作 4 点 IDFT，时域得到原序列以 4 为周期的叠加：</p>
<div class="formula">\[
y(n)=\sum_{r=-\infty}^{\infty}x(n-4r),\qquad 0\leq n\leq3.
\]</div>
<p>由于 \(x(n)\) 是右边序列，\(0\leq n\leq3\) 时只有 \(r\leq0\) 的项非零。令 \(m=-r\)，得到：</p>
<div class="formula">\[
\begin{aligned}
y(n)&=\sum_{m=0}^{\infty}\left(\frac{1}{2}\right)^{n+4m}\\
&=\left(\frac{1}{2}\right)^n\sum_{m=0}^{\infty}\left(\frac{1}{16}\right)^m\\
&=\frac{16}{15}\left(\frac{1}{2}\right)^n,\qquad 0\leq n\leq3.
\end{aligned}
\]</div>
<p>因此 4 点主值序列为：</p>
<div class="formula">\[
y(0)=\frac{16}{15},\qquad y(1)=\frac{8}{15},\qquad y(2)=\frac{4}{15},\qquad y(3)=\frac{2}{15}.
\]</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
