"""Sixteenth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


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
.indent{padding-left:1.7em;text-indent:-1.7em}
figure{break-inside:avoid;margin:12pt auto;text-align:center}
.diagram{display:block;width:min(100%,450pt);height:auto;margin:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
figcaption{color:#315d7c;font-size:9.5pt;margin-top:4pt}
</style>"""


def _math_label(x: float, y: float, width: float, height: float, latex: str, *, size: int = 16) -> str:
    """Place one complete MathJax expression in an SVG label region."""
    return (
        f'<foreignObject x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}">'
        '<div xmlns="http://www.w3.org/1999/xhtml" '
        f'style="height:100%;display:flex;align-items:center;justify-content:center;font-size:{size}px">'
        f'\\({latex}\\)</div></foreignObject>'
    )


def pole_zero_svg() -> str:
    """A correctly scaled z-plane: zero at the origin and the two real poles."""
    center_x, center_y, unit = 335, 208, 92
    phi_x = center_x + 1.618 * unit
    psi_x = center_x - 0.618 * unit
    return r'''<svg class="diagram" viewBox="0 0 720 360" role="img" aria-label="2017 年第十题的零极点图">
<defs><marker id="arrow-b16-pz" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<path fill="none" stroke="#174b73" stroke-width="2.2" marker-end="url(#arrow-b16-pz)" d="M82 208H664"/>
<path fill="none" stroke="#174b73" stroke-width="2.2" marker-end="url(#arrow-b16-pz)" d="M335 342V48"/>
<circle data-role="unit-circle" cx="335" cy="208" r="92" fill="none" stroke="#9aa8b3" stroke-width="1.8" stroke-dasharray="6 5"/>
<path fill="none" stroke="#667784" stroke-width="1.2" d="M243 201V215M427 201V215"/>
<text x="237" y="236" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="15">−1</text>
<text x="422" y="236" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="15">1</text>
<text x="345" y="236" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="15">0</text>
<circle data-role="zero" cx="335" cy="208" r="10" fill="#fff" stroke="#0f8b8d" stroke-width="4"/>
<path data-role="pole-negative" d="M''' + f'{psi_x - 10:.1f} 198L{psi_x + 10:.1f} 218M{psi_x + 10:.1f} 198L{psi_x - 10:.1f} 218' + r'''" fill="none" stroke="#b56b2e" stroke-width="4"/>
<path data-role="pole-positive" d="M''' + f'{phi_x - 10:.1f} 198L{phi_x + 10:.1f} 218M{phi_x + 10:.1f} 198L{phi_x - 10:.1f} 218' + r'''" fill="none" stroke="#b56b2e" stroke-width="4"/>
<text x="670" y="214" fill="#1f2933" font-family="Georgia, serif" font-size="20">Re(z)</text>
<text x="348" y="55" fill="#1f2933" font-family="Georgia, serif" font-size="20">Im(z)</text>
<text x="204" y="99" fill="#667784" font-family="Microsoft YaHei, sans-serif" font-size="14">单位圆</text>
<text x="305" y="184" fill="#0f8b8d" font-family="Microsoft YaHei, sans-serif" font-size="14">零点</text>
<text x="'''+f'{psi_x - 48:.1f}'+r'''" y="170" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="14">极点</text>
<text x="'''+f'{phi_x - 12:.1f}'+r'''" y="252" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="14">极点</text>
''' + _math_label(204, 245, 162, 34, r'-\frac{\sqrt5-1}{2}', size=15) + _math_label(445, 245, 150, 34, r'\frac{1+\sqrt5}{2}', size=15) + r'''</svg>'''


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 分章强化训练（续）</h1>
<div class="exam-head"><span>2017 年真题</span><span>详解见 P.____</span></div>
<p>十、某因果线性时不变系统，其输入 \(x(n)\) 和输出 \(y(n)\) 满足差分方程：</p>
<div class="formula">\[y(n)=y(n-1)+y(n-2)+x(n-1).\]</div>
<p class="indent">1．求系统函数，画出零极图；</p>
<p class="indent">2．求系统的单位样值响应；</p>
<p class="indent">3．判断系统是否稳定，若稳定，求一个满足该方程的稳定的单位样值响应。</p>
</section>'''


def answers_html() -> str:
    return r'''<section class="answer"><h1>真题整理详解（续）</h1>
<h2>2017 年真题：差分方程、收敛域与稳定性</h2>
<p>在零初始条件下对差分方程作 \(z\) 变换，先将输入与输出分别提出：</p>
<div class="formula">\[\begin{aligned}
Y(z)&=z^{-1}Y(z)+z^{-2}Y(z)+z^{-1}X(z).
\end{aligned}\]</div>
<p>整理并取输出与输入之比，系统函数为：</p>
<div class="formula">\[H(z)=\frac{z^{-1}}{1-z^{-1}-z^{-2}}=\frac{z}{z^2-z-1}.\]</div>
<p>分母的两个根就是极点，分子给出原点处的零点：</p>
<div class="formula">\[z_0=0,\qquad
z=\frac{1+\sqrt5}{2},\qquad
z=\frac{1-\sqrt5}{2}=-\frac{\sqrt5-1}{2}.\]</div>
<figure>''' + pole_zero_svg() + r'''<figcaption>零点位于原点；两个实极点分别位于 \(p_1\) 与 \(p_2\)。虚线为单位圆。</figcaption></figure>
<p>题设指定系统为因果系统，因此收敛域在最外极点之外：</p>
<div class="formula">\[\operatorname{ROC}:\left|z\right|>\frac{1+\sqrt5}{2}.\]</div>
<p>将系统函数展开为便于反变换的部分分式：</p>
<div class="formula">\[H(z)=\frac{1}{\sqrt5}\left(
\frac{1}{1-\frac{1+\sqrt5}{2}z^{-1}}
-\frac{1}{1-\frac{1-\sqrt5}{2}z^{-1}}
\right).\]</div>
<p>取两个右边序列，得到题设因果系统的单位样值响应：</p>
<div class="formula">\[h_{\mathrm c}[n]=\frac{1}{\sqrt5}\left[
\left(\frac{1+\sqrt5}{2}\right)^n
-\left(\frac{1-\sqrt5}{2}\right)^n
\right]u[n].\]</div>
<p>该因果收敛域不包含单位圆，故因果系统不稳定。若要求同一差分方程具有稳定的单位样值响应，收敛域必须夹在两个极点之间：</p>
<div class="formula">\[\operatorname{ROC}:\frac{\sqrt5-1}{2}<\left|z\right|<\frac{1+\sqrt5}{2}.\]</div>
<p>此时大模极点对应左边序列，小模极点对应右边序列，因此稳定解为：</p>
<div class="formula">\[h_{\mathrm s}[n]=-\frac{1}{\sqrt5}\left[
\left(\frac{1+\sqrt5}{2}\right)^n u[-n-1]
+\left(\frac{1-\sqrt5}{2}\right)^n u[n]
\right].\]</div>
<p>这个稳定解是双边序列：它满足原差分方程并且收敛域包含单位圆，但不再是因果系统。</p>
</section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output
