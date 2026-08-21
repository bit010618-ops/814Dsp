"""Chapter-five IIR structure training and consolidated answer components."""
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
<section class="exam-page"><h1>第五章 分章强化训练</h1>
<div class="exam-head"><span>2020 年真题</span><span>详解见 P.____</span></div>
<p>2.IIR 滤波器的级联型和并联型结构特点；</p>
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
<h2>2020 年真题</h2>
<p>2.IIR 滤波器的级联型和并联型结构特点；</p>
<div class="answer-step"><strong>级联型。</strong>先把系统函数作因式分解，把高阶系统写成若干个一阶或二阶节的乘积：</div>
<div class="formula">\[
H(z)=\prod_{r=1}^{R}H_r(z).
\]</div>
<p>主信号从左到右依次通过各个子系统，前一节的输出就是后一节的输入。因此它一眼表现为“串接关系”。实现时通常把共轭极点、零点配成二阶节，以减小有限字长下的系数量化敏感性；各节的排列还可用来控制中间节点的动态范围。</p>
<div class="answer-step"><strong>并联型。</strong>先把系统函数作部分分式展开，把它写成若干支路传递函数之和：</div>
<div class="formula">\[
H(z)=\sum_{r=1}^{R}H_r(z).
\]</div>
<p>输入先在分支点复制到各条并行支路，各支路分别完成自己的滤波，最后在标准求和点相加得到输出。因此它一眼表现为“分路—汇总关系”。并联型便于直接对应各个极点项或模态分量；当系统适合部分分式展开时，分析和局部调节较直观。</p>
<div class="answer-step"><strong>共同点与选择。</strong>两种结构实现的是同一个 (H(z))，理论频率响应相同；差别在于系统函数的分解方式和内部信号流。级联型强调因式分解后的逐节串接，并联型强调部分分式展开后的多路相加。实际实现应根据零极点分布、系数动态范围和量化误差综合选择，不能只按画图便利性判断。</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
