"""Seventh verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第七批）</h1>
<div class="exam-head"><span>2007 年真题（填空题第 4 小题）</span><span>详解见 P.____</span></div>
<p>九、填空题。（4）设序列 \(x(n)=R_{100}(n)\)，\(h(n)=R_{10}(n)\)，\(y(n)=x(n)\mathbin{\circledast}_{80}h(n)\)，问 \(y(n)\) 在哪些点上的值等于 \(x(n)\) 和 \(h(n)\) 线性卷积的结果？答________。</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2007 年真题（填空题第 4 小题）</h2>
<p>两个矩形序列的线性卷积长度为 \(100+10-1=109\)，其非零支撑为 \(0\le n\le108\)。</p>
<p class="formula-name">循环卷积的周期折回关系（用于判断折回叠加）</p>
<div class="formula">\[
y_{80}[n]=\sum_{r=-\infty}^{\infty}y_{\mathrm{lin}}[n-80r].
\]</div>
<p>当 \(0\le n\le28\) 时，有后段 \(y_{\mathrm{lin}}[n+80]\) 折回并叠加。</p>
<p class="formula-name">低索引区的折回叠加式（用于计算发生混叠的卷积样点）</p>
<div class="formula">\[
y_{80}[n]=y_{\mathrm{lin}}[n]+y_{\mathrm{lin}}[n+80],\qquad 0\le n\le28.
\]</div>
<p>当 \(80\le n\le108\) 时，有前段 \(y_{\mathrm{lin}}[n-80]\) 叠加。因此只有中间不发生折叠的样点与线性卷积一致：</p>
<p class="formula-name">未折回区间判据（用于确定与线性卷积一致的样点）</p>
<div class="formula">\[
y_{80}[n]=y_{\mathrm{lin}}[n],\qquad 29\le n\le79.
\]</div>
<p>填：\(29\le n\le79\)。</p>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
