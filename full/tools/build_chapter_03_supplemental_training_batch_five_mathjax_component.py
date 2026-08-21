"""Fifth verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第五批）</h1>
<div class="exam-head"><span>2023 年真题（DSP 第 4 小题）</span><span>详解见 P.____</span></div>
<p>七、DSP 简答题。4．对 80 点长序列 \(x(n)\)，\(0\leq n\leq79\)，以及长度为 3 的序列 \(h(n)\)，\(0\leq n\leq2\)，用重叠保留法计算线性卷积，设每段长度为 5，且长度包含重叠保留部分（重叠保留部分长度为 2）。（1）计算出全部的线性卷积结果，需要多少段？（2）写出首段和末段的内容（用 \(x(n)\) 表示，\(n\) 中填序号）。</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2023 年真题（DSP 第 4 小题）</h2>
<p>滤波器长度为 \(L_h=3\)，每段长度 \(N=5\)，因此每段丢弃前 \(L_h-1=2\) 个受循环卷积影响的样本，每段保留的新输出数为：</p>
<div class="formula">\[
M=N-(L_h-1)=5-2=3.
\]</div>
<p>线性卷积总长度为 \(L_x+L_h-1=80+3-1=82\)。为得到尾部的两个非零卷积样本，需要在输入末尾补两个零；故所需段数为：</p>
<div class="formula">\[
B=\left\lceil\frac{L_x+L_h-1}{M}\right\rceil
=\left\lceil\frac{82}{3}\right\rceil=28.
\]</div>
<p>首段在输入前补两个零，末段保留末尾两个有效输入样本并在后面补零。因此首段和末段分别为：</p>
<div class="formula">\[
\text{首段}=\left\{0,0,x(0),x(1),x(2)\right\},
\qquad
\text{末段}=\left\{x(77),x(78),x(79),0,0\right\}.
\]</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
