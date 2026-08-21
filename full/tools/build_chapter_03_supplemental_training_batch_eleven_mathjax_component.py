"""Eleventh verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><section class="exam-page"><h1>第三章 补充真题（第十一批）</h1>
<div class="exam-head"><span>2007 年真题（第十三题第 1 问）</span><span>详解见 P.____</span></div>
<p>十三、对一个连续时间信号 \(x(t)\) 进行采样，采样频率为 \(8192\,\mathrm{Hz}\)，共采样 500 点，得到一有限长序列 \(x(n)\)。（1）通过 DFT 方法来分析序列在 \(800\,\mathrm{Hz}\) 频率处的频率特性，应如何做？</p><div class="writing-space"></div></section></main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1><h2>2007 年真题（第十三题第 1 问）</h2>
<p>将 500 点序列在末尾补 12 个零，取 \(N=512\) 点 DFT。此时频率间隔为：</p>
<div class="formula">\[\Delta f=\frac{8192}{512}=16\,\mathrm{Hz}.\]</div>
<p>目标频率恰好落在 DFT 栅格上：</p>
<div class="formula">\[k_0=\frac{800}{16}=50.\]</div>
<p>因此计算补零后序列的 512 点 DFT \(X(k)\)，取 \(X(50)\) 即得到 \(800\,\mathrm{Hz}\) 处的复频率特性；其模和相角分别给出幅度和相位。</p></main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
