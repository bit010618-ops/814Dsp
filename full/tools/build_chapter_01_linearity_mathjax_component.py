"""Linearity material rendered through complete MathJax formulas only."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main class="chapter">
  <header><h1>离散时间系统的线性性质</h1></header>
  <section>
    <p>线性系统满足叠加原理：可加性与比例性必须同时成立。设 \(y_1(n)=T[x_1(n)]\)、\(y_2(n)=T[x_2(n)]\)。</p>
    <h2>可加性与比例性</h2>
    <div class="formula">\[T[x_1(n)+x_2(n)]=T[x_1(n)]+T[x_2(n)]\]</div>
    <div class="formula">\[T[a x_1(n)]=aT[x_1(n)]\]</div>
    <h2>叠加原理</h2>
    <div class="formula">\[T[a x_1(n)+b x_2(n)]=a y_1(n)+b y_2(n)\]</div>
    <p>更一般地，若 \(y_i(n)=T[x_i(n)]\)，则对任意有限组输入和系数，线性系统均有：</p>
    <div class="formula">\[T\left[\sum_{i=1}^{N}a_i x_i(n)\right]=\sum_{i=1}^{N}a_i y_i(n)\]</div>
  </section>
  <section>
    <h3>例：验证下面的系统是否为线性系统</h3>
    <div class="formula">\[y(n)=x^2(n)\]</div>
    <p>系统定义为 \(y(n)=x^2(n)\)。虽然零输入产生零输出，但仍需检验叠加原理：</p>
    <div class="formula">\[
T[a x_1+b x_2]=(a x_1+b x_2)^2
=a^2x_1^2+b^2x_2^2+2abx_1x_2
\]</div>
    <div class="formula">\[T[a x_1+b x_2]\ne aT[x_1]+bT[x_2]\]</div>
    <p>交叉项 \(2abx_1x_2\) 一般不为零，故平方系统不是线性系统。</p>
    <h3>例：验证下面的系统是否为线性系统</h3>
    <div class="formula">\[y(n)=x(-n)\]</div>
    <p>系统定义为 \(y(n)=x(-n)\)，于是：</p>
    <div class="formula">\[T[a x_1(n)+b x_2(n)]=a x_1(-n)+b x_2(-n)=a y_1(n)+b y_2(n)\]</div>
    <p>等式对任意输入与任意系数都成立，因此时间反褶系统是线性系统。线性与时不变是不同性质；该例的时不变性将单独讨论。</p>
  </section>
  <section>
    <h3>例：验证下面的 3 点中值滤波器是否是线性系统</h3>
    <div class="formula">\[y(n)=\operatorname{Mid}\{x(k)\},\qquad n-1\leq k\leq n+1\]</div>
    <p>三点中值滤波器定义为：对 \(n-1\leq k\leq n+1\) 的三个样值取中间值。它能保留中值而抑制异常点，但不满足叠加原理。</p>
    <h3>反例</h3>
    <p>取 \(a=b=1\)，并在同一三个样点上令 \(x_1=\{1,2,1\}\)、\(x_2=\{2,1,1\}\)。</p>
    <div class="formula">\[T[x_1]=1,\qquad T[x_2]=1,\qquad T[x_1]+T[x_2]=2\]</div>
    <div class="formula">\[x_1+x_2=\{3,3,2\},\qquad T[x_1+x_2]=3\]</div>
    <div class="formula">\[T[x_1+x_2]\ne T[x_1]+T[x_2]\]</div>
    <p>因此，三点中值滤波器为非线性系统。这个例子说明：系统具有实际滤波作用，并不意味着它必定线性。</p>
  </section>
</main>
"""
    template = r"""<!doctype html>
<html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>数字信号处理讲义：离散时间系统的线性性质</title>
<script>window.MathJax={tex:{packages:{'[+]':['ams']}},chtml:{scale:1}};</script>
<script defer src="__MATHJAX__"></script>
<style>
@page { size:A4; margin:18mm 18mm 20mm; }
* { box-sizing:border-box; }
body { margin:0; color:#1f2933; font-family:"Noto Serif CJK SC","Microsoft YaHei",serif; font-size:11pt; line-height:1.75; }
.chapter { max-width:174mm; margin:0 auto; }
h1 { color:#1e4f79; font-size:22pt; font-weight:400; line-height:1.3; border-bottom:1.4pt solid #b56b2e; padding-bottom:8pt; margin:0 0 15pt; }
h2 { color:#1e4f79; font-size:15pt; font-weight:400; border-bottom:.8pt solid #c59d6e; padding-bottom:4pt; margin:20pt 0 8pt; }
h3 { color:#315d7c; font-size:12.5pt; font-weight:400; margin:16pt 0 6pt; }
p { margin:0 0 9pt; }
.formula { background:#f4f7f8; border-radius:5pt; padding:9pt 14pt; margin:10pt 0 13pt; overflow-x:auto; overflow-y:hidden; text-align:center; }
.formula mjx-container[display="true"] { margin:0 !important; }
@media screen and (max-width:560px) { body { font-size:10.5pt; } .chapter { width:100%; max-width:100%; } }
</style>__CONTENT__</html>"""
    output.write_text(template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", content), encoding="utf-8")
    return output


def render_pdf(output: Path, *, wait_ms: int = 10000) -> Path:
    if not EDGE.exists():
        raise FileNotFoundError(f"Microsoft Edge is required: {EDGE}")
    html = write_html(output.with_suffix(".html"))
    subprocess.run(
        [str(EDGE), "--headless=new", "--disable-gpu", "--no-first-run",
         "--no-pdf-header-footer", f"--virtual-time-budget={wait_ms}",
         f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()],
        check=True,
    )
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_01_linearity_mathjax_component.pdf"))
