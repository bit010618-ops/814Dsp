"""Chapter-four FFT training and consolidated detailed-answer components."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:20pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.exam-page{break-before:page;min-height:230mm}.exam-page:first-child{break-before:auto}.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:0 0 10pt}.formula{break-inside:avoid;padding:7pt 4pt;margin:8pt 0;text-align:center;overflow-x:auto}.writing-space{min-height:172mm}.answer-step{break-inside:avoid;margin:8pt 0}.answer-step strong{color:#315d7c}.fft-flow{break-inside:avoid;margin:12pt 0}.fft-flow img{display:block;width:100%;height:auto;border:.5pt solid #d6dde2;background:#fff}.fft-flow figcaption{color:#52616b;text-align:center;margin-top:5pt;font-size:9.5pt}@media(max-width:560px){body{font-size:10.5pt}.writing-space{min-height:145mm}}
</style>"""


def _document(content: str) -> str:
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第四章 分章强化训练</h1>
<div class="exam-head"><span>2017 年真题</span><span>详解见 P.____</span></div>
<p>5.画出 8 点按时间抽样的基-2FFT 算法的流程运动图。</p>
<div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>真题整理详解</h1>
<h2>2017 年真题</h2>
<p>题目要求给出 8 点按时间抽取的基-2 FFT 算法流图。对 \(N=8=2^3\)，算法共有 3 级；按时间抽取时，输入为码位倒序，输出为自然顺序。</p>
<div class="answer-step"><strong>第 1 步：确定递归分解。</strong>把 8 点序列按偶、奇时间下标分为两组 4 点序列。设这两组的 4 点 DFT 为 \(X_1(k)\)、\(X_2(k)\)，则每个 \(k=0,1,2,3\) 对应的一对输出为：</div>
<div class="formula">\[
\begin{aligned}
X(k)&=X_1(k)+W_8^kX_2(k),\\
X\left(k+4\right)&=X_1(k)-W_8^kX_2(k),\\
W_8&=e^{-j\frac{2\pi}{8}}.
\end{aligned}
\]</div>
<div class="answer-step"><strong>第 2 步：确定输入、输出顺序。</strong>3 位二进制码倒序后，输入顺序应为 \(x(0),x(4),x(2),x(6),x(1),x(5),x(3),x(7)\)；经过 3 级蝶形后，输出恢复为自然顺序 \(X(0),X(1),\ldots,X(7)\)。</div>
<figure class="fft-flow" data-diagram="dit-radix-2-eight-point-flow">
<img src="../assets/source-figures/ch04-dit-fft-n8-flow.png" alt="8 点按时间抽取基 2 FFT 流图：三列各含四个蝶形，输入为码位倒序，输出为自然顺序">
<figcaption>8 点按时间抽取的基-2 FFT 算法流程图</figcaption>
</figure>
<div class="answer-step"><strong>第 3 步：读图检查。</strong>图中的三列从左到右依次为第 1 级、第 2 级、第 3 级，每一级均有 \(N/2=4\) 个蝶形。旋转因子标在对应的差分支路上；最后一级分别使用 \(W_8^0,W_8^1,W_8^2,W_8^3\)。因此该图满足基-2 DIT-FFT 的输入倒序、输出正序和三级递归结构。</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
