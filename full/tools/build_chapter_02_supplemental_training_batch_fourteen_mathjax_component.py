"""Fourteenth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

from pathlib import Path
from full.tools.render_mathjax_formula import MATHJAX

STYLE = r'''<style>@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;color:#52616b;margin:0 0 10pt}figure{margin:12pt auto;text-align:center}.diagram{width:min(100%,400pt);height:auto}</style>'''

def pole_zero_svg() -> str:
    return r'''<svg class="diagram" viewBox="0 0 620 340" role="img" aria-label="2015 年第七题的零极点图"><defs><marker id="a14" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0 0L0 6L8 3z" fill="#174b73"/></marker></defs><path d="M78 180H550M250 300V45" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#a14)"/><circle cx="250" cy="180" r="105" fill="none" stroke="#8798a5" stroke-width="2" stroke-dasharray="5 4"/><circle data-role="zero" cx="250" cy="180" r="10" fill="white" stroke="#0f8b8d" stroke-width="4"/><path data-role="pole" d="M440 170l20 20m0-20l-20 20" stroke="#b56b2e" stroke-width="5"/><text x="558" y="174" font-size="20">Re(z)</text><text x="258" y="58" font-size="20">Im(z)</text><text x="257" y="204" font-size="16">0</text><text x="347" y="204" font-size="16">1</text><text x="442" y="214" font-size="16">2</text><text x="218" y="155" fill="#0f8b8d" font-size="17">零点</text><text x="432" y="150" fill="#b56b2e" font-size="17">极点</text><text x="295" y="82" fill="#52616b" font-size="15">单位圆</text></svg>'''

def _training_html_escaped() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2015 年真题</span><span>详解见 P.____</span></div><p>七、离散因果 LTI 系统的系统函数 (H(z)) 的零极点图如图所示，其中 (h[0]=2)</p><figure>''' + pole_zero_svg() + r'''<figcaption>系统函数的零极点分布。</figcaption></figure><p>（1）求系统函数 (H(z)) 及收敛域；（2）判断是否稳定；（3）求单位脉冲响应 (h(n))；（4）求出系统的差分方程。</p></section>'''

def training_html() -> str:
    b = "\\"
    return f'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2015 年真题</span><span>详解见 P.____</span></div><p>七、离散因果 LTI 系统的系统函数 {b}(H(z){b}) 的零极点图如图所示，其中 {b}(h[0]=2{b})</p><figure>{pole_zero_svg()}<figcaption>系统函数的零极点分布。</figcaption></figure><p>（1）求系统函数 {b}(H(z){b}) 及收敛域；（2）判断是否稳定；（3）求单位脉冲响应 {b}(h(n){b})；（4）求出系统的差分方程。</p></section>'''


def _answers_html_escaped() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2015 年真题：因果系统的 ROC 与稳定性</h2><p>零点在原点、极点在 (z=2)。由 (h[0]=2) 定出增益：</p><div class="formula">[H(z)=\frac{2}{1-2z^{-1}}=\frac{2z}{z-2},qquad \operatorname{ROC}:\left|z\right|>2.\]</div><p>因果系统的 ROC 在最外极点之外，单位圆不在 ROC 内，因此系统不稳定。反变换为</p><div class="formula">[h[n]=2^{n+1}u[n].\]</div><p>由系统函数乘以分母得到</p><div class="formula">[y[n]-2y[n-1]=2x[n].\]</div></section>'''

def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2015 年真题：因果系统的 ROC 与稳定性</h2><p>零点在原点、极点在 \(z=2\)。由 \(h[0]=2\) 定出增益：</p><div class="formula">\[H(z)=\\frac{2}{1-2z^{-1}}=\\frac{2z}{z-2},\\qquad \\operatorname{ROC}:\\left|z\\right|>2.\]</div><p>因果系统的 ROC 在最外极点之外，单位圆不在 ROC 内，因此系统不稳定。反变换为</p><div class="formula">\[h[n]=2^{n+1}u[n].\]</div><p>由系统函数乘以分母得到</p><div class="formula">\[y[n]-2y[n-1]=2x[n].\]</div></section>'''


def answers_html() -> str:
    b = "\\"
    return f'''<section><h1>真题整理详解（续）</h1><h2>2015 年真题：因果系统的 ROC 与稳定性</h2><p>零点在原点、极点在 {b}(z=2{b})。由 {b}(h[0]=2{b}) 定出增益：</p><div class="formula">{b}[H(z)={b}frac{{2}}{{1-2z^{{-1}}}}={b}frac{{2z}}{{z-2}},{b}qquad {b}operatorname{{ROC}}:{b}left|z{b}right|>2.{b}]</div><p>因果系统的 ROC 在最外极点之外，单位圆不在 ROC 内，因此系统不稳定。反变换为</p><div class="formula">{b}[h[n]=2^{{n+1}}u[n].{b}]</div><p>由系统函数乘以分母得到</p><div class="formula">{b}[y[n]-2y[n-1]=2x[n].{b}]</div></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>''',encoding="utf-8")
    return output
