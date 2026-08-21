"""Sixth verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第六批）</h1>
<div class="exam-head"><span>2024 年真题（DSP 第 3 小题）</span><span>详解见 P.____</span></div>
<p>七、计算题。3．序列 \(x(n)\) 在 \(0\leq n\leq N-1\) 以外为零，且 \(x(n)=x(N-1-n)\)，\(n=0,1,2,\ldots,N-1\)，\(N\) 是偶数，其 \(N\) 点 DFT 是 \(X(k)\)，则 \(X\left(\frac{N}{2}\right)\) 值是多少。</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2024 年真题（DSP 第 3 小题）</h2>
<p>在 \(k=N/2\) 处，DFT 基函数为 \(e^{-j\pi n}=(-1)^n\)，故：</p>
<div class="formula">\[
X\left(\frac{N}{2}\right)=\sum_{n=0}^{N-1}x(n)(-1)^n.
\]</div>
<p>把第 \(n\) 项与第 \(N-1-n\) 项配对。由题设 \(x(N-1-n)=x(n)\)，且 \(N\) 为偶数，有：</p>
<div class="formula">\[
(-1)^{N-1-n}=-(-1)^n.
\]</div>
<p>每一对样本的贡献相消，因此：</p>
<div class="formula">\[
X\left(\frac{N}{2}\right)=0.
\]</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
