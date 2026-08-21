"""Eighth verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第八批）</h1>
<div class="exam-head"><span>2025 年真题（第七题第 1 小题）</span><span>详解见 P.____</span></div>
<p>七、简答题。1．\(x(n)=4\delta(n)+\delta(n-1)+\delta(n-2)+\delta(n-3)\)，求：（1）\(x(n)\) 的 4 点离散傅里叶变换 \(X(k)\)，要求写出 \(X(k)\) 每个点的值；（2）写出（1）中 \(X(k)\) 的共轭对称分量 \(X_{\mathrm{ep}}(k)\) 和共轭反对称分量 \(X_{\mathrm{op}}(k)\) 的值。</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2025 年真题（第七题第 1 小题）</h2>
<p>在一个 4 点主值序列内，\(x(0)=4\)，其余三个样本均为 \(1\)。按 4 点 DFT 定义：</p>
<div class="formula">\[
X(k)=4+e^{-j\frac{\pi}{2}k}+e^{-j\pi k}+e^{-j\frac{3\pi}{2}k},\qquad k=0,1,2,3.
\]</div>
<p>逐点代入可得：</p>
<div class="formula">\[
X(0)=7,\qquad X(1)=X(2)=X(3)=3.
\]</div>
<p>共轭对称与共轭反对称分量定义为：</p>
<div class="formula">\[
\begin{aligned}
X_{\mathrm{ep}}(k)&=\frac{1}{2}\left[X(k)+X^*\left((-k)\right)_4\right],\\
X_{\mathrm{op}}(k)&=\frac{1}{2}\left[X(k)-X^*\left((-k)\right)_4\right].
\end{aligned}
\]</div>
<p>本题各 \(X(k)\) 均为实数，且 \(X^*\left((-k)\right)_4=X(k)\)。因此：</p>
<div class="formula">\[
X_{\mathrm{ep}}(0)=7,\qquad X_{\mathrm{ep}}(1)=X_{\mathrm{ep}}(2)=X_{\mathrm{ep}}(3)=3,
\]</div>
<div class="formula">\[
X_{\mathrm{op}}(k)=0,\qquad k=0,1,2,3.
\]</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
