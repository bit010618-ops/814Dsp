"""Chapter-six IIR transformation training and consolidated answer components."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:20pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.exam-page{break-before:page;min-height:230mm}.exam-page:first-child{break-before:auto}.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:0 0 10pt}.writing-space{min-height:172mm}.answer-step{break-inside:avoid;margin:8pt 0}.answer-step strong{color:#315d7c}.formula{break-inside:avoid;padding:7pt 4pt;margin:8pt 0;text-align:center;overflow-x:auto}@media(max-width:560px){body{font-size:10.5pt}.writing-space{min-height:145mm}}
</style>"""


def _document(content: str) -> str:
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第六章 分章强化训练</h1>
<div class="exam-head"><span>2007 年真题</span><span>详解见 P.____</span></div>
<p>八、证明：时间连续的稳定系统经双线性变换后得到的离散系统仍然是稳定系统；反之亦真。（设定双线性变换为 \(s=\frac{2}{T}\frac{z-1}{z+1}\)）</p>
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
<h2>2007 年真题</h2>
<p>八、证明：时间连续的稳定系统经双线性变换后得到的离散系统仍然是稳定系统；反之亦真。（设定双线性变换为 \(s=\frac{2}{T}\frac{z-1}{z+1}\)）</p>
<div class="answer-step"><strong>第 1 步：写出实部。</strong>双线性变换把 \(z\) 平面映射到 \(s\) 平面。将分子分母同乘 \(z^*+1\)，得到：</div>
<div class="formula">\[
\begin{aligned}
\operatorname{Re}\{s\}&=\frac{2}{T}\operatorname{Re}\left\{\frac{z-1}{z+1}\right\}\\
&=\frac{2}{T}\frac{\left|z\right|^2-1}{\left|z+1\right|^2}.
\end{aligned}
\]</div>
<div class="answer-step"><strong>第 2 步：比较稳定区域。</strong>采样周期 \(T>0\)，且对有限 \(z\ne-1\)，分母 \(\left|z+1\right|^2>0\)。因此实部的符号只由 \(\left|z\right|^2-1\) 决定：</div>
<div class="formula">\[
\operatorname{Re}\{s\}<0
\quad\Longleftrightarrow\quad
\left|z\right|<1.
\]</div>
<p>也就是说，连续时间系统的左半平面一一映射到离散系统的单位圆内；虚轴 \(\operatorname{Re}\{s\}=0\) 映射到单位圆 \(\left|z\right|=1\)。</p>
<div class="answer-step"><strong>第 3 步：由极点位置得出结论。</strong>连续时间有理系统稳定当且仅当全部极点位于左半平面。经上述映射后，这些极点全部落在单位圆内，因而所得离散系统稳定。反过来，若离散系统稳定，其全部极点在单位圆内，逆双线性变换把它们映射到左半平面，所以对应连续时间系统也稳定。故双线性变换保持稳定性，反之亦真。</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
