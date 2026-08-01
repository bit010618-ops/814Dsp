"""First verified batch of chapter-two supplemental exam questions and answers."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}.indent{padding-left:1.7em;text-indent:-1.7em}
</style>"""


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题</h1>
<div class="exam-head"><span>2002 年真题</span><span>详解见 P.____</span></div>
<p>一、填空题</p>
<p>3.连续时间系统稳定要求系统函数 \(H(s)\) 的极点________，离散时间系统稳定要求其系统函数 \(H(z)\) 的收敛域________。</p></section>
<section class="exam-page"><div class="exam-head"><span>2003 年真题</span><span>详解见 P.____</span></div>
<p>八、已知时域离散线性非移变系统的系统函数 \(H(z)\)：</p>
<div class="formula">\[H(z)=\frac{1}{(z-a)(z-b)},\qquad a,b\text{ 为常数}.\]</div>
<p class="indent">（1）要求系统稳定，确定 \(a\) 和 \(b\) 的取值域；</p>
<p class="indent">（2）要求系统因果、稳定，确定 \(a\) 和 \(b\) 的取值域。</p>
<h2>2003 年真题（判断题第 2 小题）</h2>
<p>令 \(x(n)=a^{|n|}\)，\(0<|a|<1\)，\(-\infty\le n\le\infty\)，</p>
<div class="formula">\[X(z)=\sum_{n=-\infty}^{\infty}x(n)z^{-n}.\]</div>
<p>则 \(X(z)\) 的收敛域为 \(|a|<|z|<|a|^{-1}\)。</p><p>a）正确　　b）不正确</p></section>
<section class="exam-page"><div class="exam-head"><span>2004 年真题：梳状滤波器</span><span>详解见 P.____</span></div>
<p>九、四阶梳状滤波器的系统函数为：</p>
<div class="formula">\[H(z)=A\frac{1+z^{-4}}{1+0.3^4z^{-4}}.\]</div>
<p class="indent">（1）画出 \(H(z)\) 的零极点分布图；</p><p class="indent">（2）求使滤波器的增益等于 2 时的 \(A\) 值。</p></section>
<section class="exam-page"><div class="exam-head"><span>2004 年真题：频率响应</span><span>详解见 P.____</span></div>
<p>十二、什么类型的滤波器具有单位取样响应：</p>
<div class="formula">\[h(n)=\delta(n)-\frac{\sin(n\pi/3)}{n\pi}.\]</div><p>并画出该滤波器的频率响应幅度频谱。</p></section>
<section class="exam-page"><div class="exam-head"><span>2005 年真题</span><span>详解见 P.____</span></div>
<p>十一、设 \(x(n)\) 是一个实因果序列，它的离散时间傅里叶变换为：</p>
<div class="formula">\[X(e^{j\omega})=X_R(e^{j\omega})+jX_I(e^{j\omega}).\]</div>
<p>如果 \(X_R(e^{j\omega})=1+A\cos\omega\)，求 \(x(n)\)。</p></section>
<section class="exam-page"><div class="exam-head"><span>2006 年真题</span><span>详解见 P.____</span></div>
<p>10. 已知</p><div class="formula">\[F(z)=\frac{2z^2}{\left(z-\frac12\right)^2(z-1)},\]</div>
<p>求在 \(\frac12<|z|<1\) 时对应的原序列。</p></section>
<section class="exam-page"><div class="exam-head"><span>2007 年真题</span><span>详解见 P.____</span></div>
<p>2. 若信号 \(x(n)=k\)，\(k\) 为常数，求其离散时间傅里叶变换；</p>
<h2>2007 年真题（填空题第 3 小题）</h2><p>若某稳定系统的系统函数在单位圆外有极点，则系统一定是________系统。</p></section>'''


def answers_html() -> str:
    return r'''<section class="answer"><h2>2002 年真题：连续与离散系统稳定性</h2>
<p>连续时间有理系统稳定，当且仅当系统函数的全部极点严格位于 \(s\) 平面的左半平面。离散时间 LTI 系统稳定，当且仅当 \(H(z)\) 的收敛域包含单位圆：</p>
<div class="formula">\[\operatorname{Re}\{p_i\}<0,\qquad |z|=1\subset\operatorname{ROC}.\]</div>
<h2>2003 年真题：极点、收敛域、因果性与稳定性</h2>
<p>稳定性的必要且充分条件是收敛域包含单位圆，因而不能有极点落在单位圆上：</p>
<div class="formula">\[|a|\ne1,\qquad |b|\ne1,\qquad |z|=1\subset\operatorname{ROC}.\]</div>
<p>若还要求因果，ROC 必为最外极点之外，故全部极点均须严格位于单位圆内：</p>
<div class="formula">\[|a|<1,\qquad |b|<1.\]</div>
<p>对于 \(x(n)=a^{|n|}\)，右边部分给出 \(|z|>|a|\)，左边部分给出 \(|z|<|a|^{-1}\)，所以题中判断正确。</p>
<h2>2004 年真题：四阶梳状滤波器</h2>
<p>分子为零时 \(z^{-4}=-1\)，分母为零时 \(z^{-4}=-0.3^{-4}\)。四个零点在单位圆上；四个极点与它们同角度、半径为 \(0.3\)：</p>
<div class="formula">\[z_k=e^{j(2k+1)\pi/4},\qquad p_k=0.3e^{j(2k+1)\pi/4},\qquad k=0,1,2,3.\]</div>
<p>按直流增益为 2 的通常定义，令 \(H(e^{j0})=2\)，得到</p>
<div class="formula">\[2=A\frac{2}{1+0.3^4}\quad\Longrightarrow\quad A=1+0.3^4.\]</div>
<h2>2004 年真题：由单位取样响应判滤波器类型</h2>
<p>理想低通的冲激响应为 \(\sin(\omega_c n)/(\pi n)\)。题给冲激响应是单位冲激减去截止频率为 \(\omega_c=\pi/3\) 的理想低通，因此为理想高通滤波器：</p>
<div class="formula">\[|H(e^{j\omega})|=\begin{cases}0,&|\omega|<\pi/3,\\1,&\pi/3<|\omega|\le\pi.\end{cases}\]</div>
<h2>2005 年真题：由频谱实部恢复实因果序列</h2>
<p>频谱实部对应时域共轭对称分量。先反变换得到</p>
<div class="formula">\[x_e(n)=\delta(n)+\frac{A}{2}\bigl[\delta(n-1)+\delta(n+1)\bigr].\]</div>
<p>因 \(x(n)\) 为实因果序列，\(n>0\) 时有 \(x(n)=2x_e(n)\)，而 \(x(0)=x_e(0)\)。所以</p>
<div class="formula">\[x(n)=\delta(n)+A\delta(n-1).\]</div>
<h2>2006 年真题：指定 ROC 的反 \(z\) 变换</h2>
<p>令 \(q=z^{-1}\)，先作部分分式分解：</p>
<div class="formula">\[F(z)=\frac{8}{1-z^{-1}}-\frac{4}{1-\frac12z^{-1}}-\frac{4}{\left(1-\frac12z^{-1}\right)^2}.\]</div>
<p>ROC 为 \(\frac12<|z|<1\)：极点 \(z=1\) 对应左边序列，两个 \(z=\frac12\) 项对应右边序列。故</p>
<div class="formula">\[f(n)=-8u(-n-1)-4\left(\frac12\right)^nu(n)-4(n+1)\left(\frac12\right)^nu(n).\]</div>
<p>合并右边两项亦可写为</p>
<div class="formula">\[f(n)=-8u(-n-1)-4(n+2)\left(\frac12\right)^nu(n).\]</div>
<h2>2007 年真题：常数序列的 DTFT 与稳定系统的极点</h2>
<p>常数序列的 DTFT 为冲激列：</p>
<div class="formula">\[X(e^{j\omega})=2\pi k\sum_{m=-\infty}^{\infty}\delta(\omega-2\pi m).\]</div>
<p>稳定系统的 ROC 必含单位圆。若有极点在单位圆外，因果系统的 ROC 会位于最外极点之外而无法包含单位圆，所以该系统一定为<strong>非因果系统</strong>。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    """Return the browser DOM after MathJax has converted every formula."""
    completed = subprocess.run(
        [
            str(EDGE), "--headless=new", "--disable-gpu",
            "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri(),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout
