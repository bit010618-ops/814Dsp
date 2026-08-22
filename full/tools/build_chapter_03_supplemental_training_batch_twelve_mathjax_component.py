"""Twelfth verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><section class="exam-page"><h1>第三章 补充真题（第十二批）</h1>
<div class="exam-head"><span>2024 年真题（第七题第 1 问）</span><span>详解见 P.____</span></div>
<p>七、计算题：1. 计算序列 (x(n)=(-1)^n+1, 0\leq n\leq3) 的 4 点离散傅里叶变换 (X(k))，要求写出每一点的值以及 (X_{\mathrm{ep}}(k)) 的值。</p><div class="writing-space"></div></section></main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1><h2>2024 年真题（第七题第 1 问）</h2>
<p>先按 (n=0,1,2,3) 写出一个周期内的样值：</p>
<div class="formula">\[x(n)=\{2,0,2,0\}.\]</div>
<p>取 (W_4=e^{-j\frac{2\pi}{4}})。只有 (n=0,2) 两项非零，因此：</p>
<div class="formula">\[X(k)=\sum_{n=0}^{3}x(n)W_4^{nk}=2+2W_4^{2k}=2+2(-1)^k.\]</div>
<p>逐点代入 (k=0,1,2,3)，得到：</p>
<div class="formula">\[X(0)=4,\qquad X(1)=0,\qquad X(2)=4,\qquad X(3)=0.\]</div>
<p>偶对称分量可写为：</p>
<div class="formula">\[X_{\mathrm{ep}}(k)=\frac{1}{2}\left[X(k)+X^*\left((-k)\right)_4\right].\]</div>
<p>本题中 (X(k)) 为实偶序列，故 (X^*\left((-k)\right)_4=X(k))，从而：</p>
<div class="formula">\[X_{\mathrm{ep}}(k)=X(k)=\{4,0,4,0\},\qquad 0\leq k\leq3.\]</div></main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
