"""2003 z-domain stability question."""
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
h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}
p{margin:5pt 0 8pt}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.exam-page{break-before:page;min-height:230mm}
.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
.indent{padding-left:1.7em;text-indent:-1.7em}
</style>"""


def training_html() -> str:
    """Return the source-faithful 2003 prompt."""
    return r'''<section class="exam-page">
<h1>第二章 补充真题（续）</h1>
<div class="exam-head"><span>2003 年真题</span><span>详解见 P.____</span></div>
<p>八、已知时域离散线性非移变系统的系统函数\(H(z)\)：</p>
<div class="formula">\[H(z)=\frac{1}{(z-a)(z-b)}\]</div>
<p>\(a,b\)为常数</p>
<p class="indent">（1）要求系统稳定，确定\(a\)和\(b\)的取值域</p>
<p class="indent">（2）要求系统因果、稳定，确定\(a\)和\(b\)的取值域</p>
</section>'''


def answers_html() -> str:
    """Explain stability by ROC first, then impose causality."""
    return r'''<section>
<h1>真题整理详解（续）</h1>
<h2>2003 年真题：极点、ROC 与稳定性</h2>
<p>系统函数的两个极点为 \(z=a\) 与 \(z=b\)。对于离散时间 LTI 系统，BIBO 稳定的充要条件是收敛域包含单位圆：</p>
<div class="formula">\[\left|z\right|=1\subset\operatorname{ROC}.\]</div>
<h3>（1）仅要求稳定</h3>
<p>极点不能落在单位圆上，否则无论收敛域取在极点内侧、外侧还是两极点之间，均无法包含该极点处的单位圆。因此稳定系统要求</p>
<div class="formula">\[\left|a\right|\ne1,\qquad \left|b\right|\ne1.\]</div>
<p>当两极点同在单位圆内时，取外侧 ROC；同在单位圆外时，取内侧 ROC；一个在内、一个在外时，取两极点之间的环形 ROC。三种情形均使 \(\left|z\right|=1\) 落入收敛域。</p>
<h3>（2）同时要求因果和稳定</h3>
<p>因果有理系统的 ROC 必须在最外层极点之外；要使该 ROC 同时包含单位圆，两个极点都必须严格位于单位圆内。因此</p>
<div class="formula">\[\boxed{\left|a\right|<1,\qquad \left|b\right|<1.}\]</div>
<p>此时收敛域为 \(\left|z\right|>\max\{\left|a\right|,\left|b\right|\}\)，它既符合因果性，也包含单位圆，故系统稳定。</p>
</section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script>
<script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>''',
        encoding="utf-8",
    )
    return output


def rendered_dom(html: Path) -> str:
    return subprocess.run(
        [str(EDGE), "--headless=new", "--disable-gpu", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
