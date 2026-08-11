"""Reusable chapter-three training and final-answer components."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:20pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:0 0 10pt}.formula{break-inside:avoid;padding:7pt 4pt;margin:8pt 0;text-align:center;overflow-x:auto}.writing-space{min-height:105mm}.answer-step{break-inside:avoid;margin:8pt 0}.answer-step strong{color:#315d7c}@media(max-width:560px){body{font-size:10.5pt}}</style>"""


def _document(content: str) -> str:
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>第三章 分章强化训练</h1>
<div class="exam-head"><span>2003 年真题</span><span>详解见 P.____</span></div>
<p>七、用 DFT 对模拟信号进行谱分析，设模拟信号 \(x_a(t)\) 的最高频率为 200 Hz，以 Nyquist 频率采样得到时域离散序列 \(x(n)=x_a(nT)\)，要求频率分辨率为 10 Hz，求序列 \(x(n)\) 的离散傅里叶变换 \(X(k)\) 各 \(k\) 点对应的数字频率 \(\omega_k\)（弧）和模拟频率 \(f_k\)（Hz）的值。</p>
<div class="writing-space"></div>
<div class="exam-head"><span>2002 年真题</span><span>详解见 P.____</span></div>
<p>九、已知 \(x_1(n)=\left(\frac{1}{2}\right)^n,\ 0\leq n\leq4\)，\(x_2(n)=1,\ 0\leq n\leq2\)，且 \(X_1(K)=\operatorname{DFT}[x_1(n)]\)，\(X_2(K)=\operatorname{DFT}[x_2(n)]\)，求 \(x_3(n)=\operatorname{IDFT}\left[X_1(K)X_2(K)\right]\)。</p>
<div class="writing-space"></div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>真题整理详解</h1>
<h2>2003 年真题</h2>
<p>用 DFT 对模拟信号进行谱分析。</p>
<div class="answer-step"><strong>第 1 步：确定采样频率。</strong>题目规定按 Nyquist 频率采样，最高频率为 \(200\,\mathrm{Hz}\)，故：</div>
<div class="formula">\[
f_s=2\times200=400\,\mathrm{Hz}.
\]</div>
<div class="answer-step"><strong>第 2 步：由频率分辨率确定 DFT 点数。</strong>DFT 的频率间隔为 \(F_0=f_s/N\)。由 \(F_0=10\,\mathrm{Hz}\) 得：</div>
<div class="formula">\[
N=\frac{f_s}{F_0}=40.
\]</div>
<div class="answer-step"><strong>第 3 步：写出第 \(k\) 个频点的数字频率。</strong>对 \(N=40\) 点 DFT，频率取样点为：</div>
<div class="formula">\[
\omega_k=\frac{2\pi k}{N}=\frac{2\pi k}{40}=\frac{\pi k}{20}\ \mathrm{rad},
\qquad k=0,1,\ldots,39.
\]</div>
<div class="answer-step"><strong>第 4 步：写出对应的模拟频率。</strong>每个频点间隔为 \(10\,\mathrm{Hz}\)，因此：</div>
<div class="formula">\[
f_k=kF_0=10k\,\mathrm{Hz},
\qquad k=0,1,\ldots,39.
\]</div>
<p>因此，\(k=0\) 对应直流，\(k=20\) 对应 Nyquist 频率 \(200\,\mathrm{Hz}\)。在 DFT 的一个周期内，\(k=21,\ldots,39\) 也可按负频率解释为 \(f_k=(k-40)\times10\,\mathrm{Hz}\)。</p>
<h2>2002 年真题</h2>
<p>已知 \(x_1(n)=\left(\frac{1}{2}\right)^n,\ 0\leq n\leq4\)，\(x_2(n)=1,\ 0\leq n\leq2\)，且 \(X_1(K)=\operatorname{DFT}[x_1(n)]\)，\(X_2(K)=\operatorname{DFT}[x_2(n)]\)，求 \(x_3(n)=\operatorname{IDFT}\left[X_1(K)X_2(K)\right]\)。</p>
<div class="answer-step"><strong>第 1 步：识别 DFT 域乘法。</strong>由 DFT 的循环卷积性质：</div>
<div class="formula">\[
x_3(n)=x_1(n)\mathbin{\circledast}_N x_2(n).
\]</div>
<p>原题没有给出 DFT 点数 \(N\)，故不能把答案擅自写成唯一的固定数列；一般答案应按所用 \(N\) 点的循环卷积理解。</p>
<div class="answer-step"><strong>第 2 步：给出无混叠的常用情形。</strong>两序列长度分别为 5 与 3。若希望结果等于线性卷积，必须满足：</div>
<div class="formula">\[
N\geq5+3-1=7.
\]</div>
<p>此时逐项相加得到：</p>
<div class="formula">\[
x_3(n)=\left\{1,\frac{3}{2},\frac{7}{4},\frac{7}{8},\frac{7}{16},\frac{3}{16},\frac{1}{16}\right\},
\qquad 0\leq n\leq6.
\]</div>
<p>若实际 DFT 点数小于 7，应将这七个线性卷积样值按该 \(N\) 点周期折回相加，得到相应的循环卷积结果。</p>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
