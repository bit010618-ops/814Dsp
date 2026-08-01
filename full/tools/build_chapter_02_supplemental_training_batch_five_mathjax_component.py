"""Fifth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}
h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
p{margin:5pt 0 8pt}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.exam-page{break-before:page;min-height:230mm}
.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
</style>"""


def training_html() -> str:
    """Preserve the original 2013 calculation-question wording."""
    return r'''<section class="exam-page">
<h1>第二章补充真题（续）</h1>
<div class="exam-head"><span>2013 年真题</span><span>详解见 P.____</span></div>
<p>五、已知 \(\displaystyle x[n]=\left(\frac13\right)^n u[n]+\left(\frac12\right)^n u[-n-1]\)，求 \(x[n]\) 的 \(z\) 变换 \(X(z)\)。</p>
</section>'''


def answers_html() -> str:
    """Give the two-sided z-transform and ROC derivation in full."""
    return r'''<section>
<h1>真题整理详解（续）</h1>
<h2>2013 年真题：双边序列的 \(z\) 变换</h2>
<p>将序列按右边序列与左边序列分开处理：</p>
<div class="formula">\[
x[n]=x_1[n]+x_2[n],\qquad
x_1[n]=\left(\frac13\right)^n u[n],\qquad
x_2[n]=\left(\frac12\right)^n u[-n-1].
\]</div>
<p>对右边序列，有</p>
<div class="formula">\[
X_1(z)=\sum_{n=0}^{\infty}\left(\frac13\right)^n z^{-n}
=\frac{1}{1-\frac13z^{-1}},\qquad
\operatorname{ROC}:\left|z\right|>\frac13.
\]</div>
<p>对左边序列，求和区间为 \(n\le -1\)。令 \(m=-n\)，则 \(m\ge1\)，因此</p>
<div class="formula">\[
\begin{aligned}
X_2(z)
&=\sum_{n=-\infty}^{-1}\left(\frac12\right)^n z^{-n}\\
&=\sum_{m=1}^{\infty}(2z)^m
=\frac{2z}{1-2z}
=-\frac{1}{1-\frac12z^{-1}},
\qquad \operatorname{ROC}:\left|z\right|<\frac12.
\end{aligned}
\]</div>
<p>两项相加，并取两个收敛域的交集，得到</p>
<div class="formula">\[
X(z)=\frac{1}{1-\frac13z^{-1}}-\frac{1}{1-\frac12z^{-1}},
\qquad
\operatorname{ROC}:\frac13<\left|z\right|<\frac12.
\]</div>
<p>该 ROC 位于两个极点之间，和题目给出的“右边项 + 左边项”的双边序列形式一致。</p>
</section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    completed = subprocess.run(
        [str(EDGE), "--headless=new", "--disable-gpu", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout
