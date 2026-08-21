"""Tenth verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第十批）</h1>
<div class="exam-head"><span>2025 年真题（第七题第 3 小题）</span><span>详解见 P.____</span></div>
<p>七、简答题。3．序列 \(x(n)\) 在 \(0\leq n\leq N-1\) 以外为零，\(N\) 为偶数，\(x(n)\) 的 \(N\) 点 DFT 是 \(X(k)\)，求：（1）若 \(x(n)=x(N-1-n)\)，请给出 \(X\left(\frac{N}{2}\right)\) 的值；（2）若 \(x(n)=-x(N-1-n)\)，请给出 \(X(0)\) 的值。</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2025 年真题（第七题第 3 小题）</h2>
<p>（1）在 \(k=N/2\) 处，DFT 的基函数为 \(e^{-j\pi n}=(-1)^n\)，所以：</p>
<div class="formula">\[
X\left(\frac{N}{2}\right)=\sum_{n=0}^{N-1}x(n)(-1)^n.
\]</div>
<p>将第 \(n\) 项与第 \(N-1-n\) 项配对。题设给出 \(x(N-1-n)=x(n)\)，且 \(N\) 为偶数，因此：</p>
<div class="formula">\[
(-1)^{N-1-n}=-(-1)^n.
\]</div>
<p>每一对的贡献相消，故：</p>
<div class="formula">\[
X\left(\frac{N}{2}\right)=0.
\]</div>
<p>（2）在 \(k=0\) 处，DFT 值等于一个主值周期内样本之和：</p>
<div class="formula">\[
X(0)=\sum_{n=0}^{N-1}x(n).
\]</div>
<p>由 \(x(N-1-n)=-x(n)\)，第 \(n\) 项与第 \(N-1-n\) 项的和为零。由于 \(N\) 为偶数，不存在与自身配对的中间样本，故全部样本两两相消：</p>
<div class="formula">\[
X(0)=0.
\]</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
