"""Thirteenth verified batch of supplemental chapter-three DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><section class="exam-page"><h1>第三章 补充真题（第十三批）</h1>
<div class="exam-head"><span>2021 年真题（第七题）</span><span>详解见 P.____</span></div>
<p>七、DFT 变换</p>
<p>1. 已知 (x(n)=(n+1)R_6(n))，(X(k)) 是 (x(n)) 的 6 点 DFT，求 (X(k))；</p>
<p>2. 又已知 (h(n)=\{1,1,1,1\})，(Y(k)=X(k)\cdot H(K)R_{10}(K))，求 (y(n)=\operatorname{IDFT}(Y(K)))；</p>
<p>3. 已知 (x(n)=a^nR_8(n))，(x(n)) 的 (z) 变换在单位圆上采样 6 个点，(X(k)=\left.X(z)\right|_{z=e^{j\frac{2\pi}{6}k}},\ k=0,1,2,3,4,5)，求其 6 点 DFT 反变换 (x(n))；</p>
<p>4. 什么是频谱泄露，怎么抑制？</p><div class="writing-space"></div></section></main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1><h2>2021 年真题（第七题）</h2>
<h3>第 1 问：6 点 DFT</h3><p>一个周期内 (x(n)=\{1,2,3,4,5,6\})。令 (W_6=e^{-j\frac{2\pi}{6}})，则：</p>
<div class="formula">\[X(k)=\sum_{n=0}^{5}(n+1)W_6^{nk}=\begin{cases}21,&k=0,\\-\frac{6}{1-W_6^k},&k=1,2,3,4,5.\end{cases}\]</div>
<p>逐点写为：</p><div class="formula">\[\begin{aligned}X(0)&=21, &X(1)&=-3+j3\sqrt{3}, &X(2)&=-3+j\sqrt{3},\\X(3)&=-3, &X(4)&=-3-j\sqrt{3}, &X(5)&=-3-j3\sqrt{3}.\end{aligned}\]</div>
<h3>第 2 问：10 点频率栅格上的乘积</h3><p>乘积中出现 (R_{10}(K))，故以 (L=10) 为 DFT 长度，将 (x(n)) 和 (h(n)) 均补零至 10 点，分别得到 (X_{10}(K)) 与 (H_{10}(K))。频域相乘后作 10 点 IDFT 等于两序列的线性卷积；其长度为 (6+4-1=9<10)，不会发生循环混叠：</p>
<div class="formula">\[y(n)=x(n)*h(n)=\{1,3,6,10,14,18,15,11,6\},\qquad 0\leq n\leq8.\]</div>
<h3>第 3 问：单位圆六点取样后的 IDFT</h3><p>频域等间隔取样后作 6 点 IDFT，对应时域以 6 为周期的叠加：</p>
<div class="formula">\[\widetilde{x}(n)=\sum_{r=-\infty}^{\infty}x(n-6r),\qquad 0\leq n\leq5.\]</div>
<p>由于原序列只在 (0\leq n\leq7) 非零，前两个主值点还各叠加了一个后续样值：</p>
<div class="formula">\[\widetilde{x}(n)=\{1+a^6,\ a+a^7,\ a^2,\ a^3,\ a^4,\ a^5\},\qquad 0\leq n\leq5.\]</div>
<h3>第 4 问：频谱泄露</h3><p>频谱泄露是指对有限长记录作 DFT 时，有限观察窗会使原本集中在某些频点的频谱扩散到相邻频点，表现为主瓣展宽和旁瓣出现。抑制方法包括：延长记录长度以减小频率间隔；使记录长度覆盖整数个周期以避免非相干截断；以及按需求选用汉宁窗、海明窗、布莱克曼窗等窗函数降低旁瓣。补零只能加密频率取样，不能从根本上消除泄露。</p></main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
