"""Sixth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}.indent{padding-left:1.7em;text-indent:-1.7em}figure{break-inside:avoid;margin:12pt auto;text-align:center}.diagram{display:block;width:min(100%,470pt);height:auto;margin:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}.roc-diagram{width:min(100%,330pt)}figcaption{color:#315d7c;font-size:9.5pt;margin-top:4pt}
</style>"""


def feedback_system_svg() -> str:
    """Programmatic textbook redraw of the 2014 single-delay feedback system."""
    return r'''<svg class="diagram" viewBox="0 0 780 330" role="img" aria-label="2014 年第五题的单延时反馈离散系统结构图">
<defs><marker id="arrow-b6-main" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker><marker id="arrow-b6-feedback" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#0f8b8d"/></marker></defs>
<text x="40" y="108" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">x[n]</text><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b6-main)" d="M84 104H185"/><circle cx="218" cy="104" r="32" fill="white" stroke="#174b73" stroke-width="2"/><foreignObject x="198" y="84" width="40" height="40"><div xmlns="http://www.w3.org/1999/xhtml" style="height:40px;display:flex;align-items:center;justify-content:center;font-size:24px">\(+\)</div></foreignObject><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b6-main)" d="M250 104H688"/><circle cx="500" cy="104" r="4" fill="#174b73"/><text x="698" y="109" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">y[n]</text>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b6-main)" d="M500 104V151H545"/><rect x="545" y="126" width="85" height="50" rx="5" fill="#f4f7f8" stroke="#0f8b8d" stroke-width="2"/><foreignObject x="545" y="126" width="85" height="50"><div xmlns="http://www.w3.org/1999/xhtml" style="height:50px;display:flex;align-items:center;justify-content:center;font-size:17px">\(z^{-1}\)</div></foreignObject>
<path fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-b6-feedback)" d="M630 151V232H470"/><rect data-role="feedback-gain" x="390" y="207" width="80" height="50" rx="5" fill="#f4f7f8" stroke="#0f8b8d" stroke-width="2"/><foreignObject x="390" y="207" width="80" height="50"><div xmlns="http://www.w3.org/1999/xhtml" style="height:50px;display:flex;align-items:center;justify-content:center;font-size:17px">\(\frac{1}{2}\)</div></foreignObject><path data-port="bottom" fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-b6-feedback)" d="M390 232H218V136"/>
<text x="40" y="305" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">每个延时单元为一拍延时；主信号流自左向右。</text></svg>'''


def zero_pole_roc_svg() -> str:
    """Vector z-plane with axes, unit circle, zero/pole symbols and causal ROC."""
    return r'''<svg class="diagram roc-diagram" style="width:min(100%,330pt)" viewBox="0 0 640 340" role="img" aria-label="2014 年第五题的零极点图及因果收敛域">
<defs><marker id="arrow-b6-z" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<rect x="66" y="35" width="500" height="270" rx="4" fill="#e8f3f2" opacity="0.82"/><circle cx="300" cy="170" r="50" fill="#fbfcfd"/><path fill="none" stroke="#174b73" stroke-width="1.8" marker-end="url(#arrow-b6-z)" d="M82 170H556"/><path fill="none" stroke="#174b73" stroke-width="1.8" marker-end="url(#arrow-b6-z)" d="M300 294V46"/><circle cx="300" cy="170" r="100" fill="none" stroke="#8797a3" stroke-width="1.5" stroke-dasharray="6 4"/><circle cx="300" cy="170" r="8" fill="white" stroke="#0f8b8d" stroke-width="3"/><path fill="none" stroke="#b56b2e" stroke-width="3" d="M344 164l12 12m0-12l-12 12"/>
<path fill="none" stroke="#52616b" stroke-width="1" d="M400 163V177M350 163V177"/><text x="294" y="194" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">0</text><text x="344" y="194" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">1/2</text><text x="394" y="194" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">1</text><text x="562" y="178" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">Re[z]</text><text x="308" y="53" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">Im[z]</text><text x="310" y="157" fill="#0f8b8d" font-family="Microsoft YaHei, sans-serif" font-size="13">零点</text><text x="362" y="158" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="13">极点</text><text x="420" y="82" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="13">单位圆</text><text x="410" y="278" fill="#0f8b8d" font-family="Microsoft YaHei, sans-serif" font-size="13">ROC：极点外侧</text></svg>'''


def training_html() -> str:
    """Preserve the five original 2014 subquestions verbatim."""
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2014 年真题</span><span>详解见 P.____</span></div><p>五、某离散 LTI 系统如图所示：</p><figure>''' + feedback_system_svg() + r'''<figcaption>离散 LTI 反馈系统。</figcaption></figure><p class="indent">（1）写出系统的差分方程；</p><p class="indent">（2）求系统函数 \(H(z)\)；</p><p class="indent">（3）画出 \(H(z)\) 的零极点分布图及收敛域；</p><p class="indent">（4）写出系统的单位脉冲响应；</p><p class="indent">（5）写出系统的频率响应。</p></section>'''


def _answers_html_legacy() -> str:
    """Derive every requested quantity from the feedback diagram."""
    return r'''<section><h1>真题整理详解（续）</h1><h2>2014 年真题：单延时反馈离散 LTI 系统</h2><p>反馈支路把输出延迟一拍并乘以 \(\frac{1}{2}\) 后送回求和器。因此先直接写出时域关系：</p><div class="formula">\[y[n]=x[n]+\frac{1}{2}y[n-1].\]</div><p>在零初始条件下作 \(z\) 变换并整理：</p><div class="formula">\[\begin{aligned}Y(z)&=X(z)+\frac{1}{2}z^{-1}Y(z),\\H(z)&=\frac{Y(z)}{X(z)}=\frac{1}{1-\frac{1}{2}z^{-1}}=\frac{z}{z-\frac{1}{2}}.\end{aligned}\]</div><p>图中给出的实现是因果实现，所以收敛域位于最外极点之外：</p><div class="formula">\[\operatorname{ROC}:\left|z\right|>\frac{1}{2}.\]</div><p>由 \(H(z)=z/(z-\frac12)\) 可见，零点位于 \(z=0\)，极点位于 \(z=\frac12\)。单位圆包含在收敛域中，因此该系统稳定。</p><figure>''' + zero_pole_roc_svg() + r'''<figcaption>零点、极点、单位圆与因果收敛域。</figcaption></figure><p>对因果 ROC 使用右边序列的标准反变换对，得到单位脉冲响应：</p><div class="formula">\[h[n]=\left(\frac{1}{2}\right)^n u[n].\]</div><p>令 \(z=e^{j\omega}\)，频率响应及其幅度、相位可写为：</p><div class="formula">\[\begin{aligned}H(e^{j\omega})&=\frac{1}{1-\frac{1}{2}e^{-j\omega}},\\\left|H(e^{j\omega})\right|&=\frac{1}{\sqrt{\frac{5}{4}-\cos\omega}},\\\angle H(e^{j\omega})&=-\arctan\!\left(\frac{\frac{1}{2}\sin\omega}{1-\frac{1}{2}\cos\omega}\right).\end{aligned}\]</div><p>直流增益为 \(2\)；当 \(\omega=\pi\) 时，幅度降为 \(\frac{2}{3}\)。这与极点位于正实轴、靠近单位圆的低频增强特性一致。</p></section>'''


def answers_html() -> str:
    """Detailed solution in a natural flow that fills the preceding A4 page."""
    return r'''<section><h1>真题整理详解（续）</h1>
<h2>2014 年真题：单延时反馈离散 LTI 系统</h2>
<p>反馈支路把输出延迟一拍并乘以 \(\frac{1}{2}\) 后送回求和器。因此先直接写出时域关系：</p>
<div class="formula">\[y[n]=x[n]+\frac{1}{2}y[n-1].\]</div>
<p>在零初始条件下作 \(z\) 变换并整理：</p>
<div class="formula">\[\begin{aligned}Y(z)&=X(z)+\frac{1}{2}z^{-1}Y(z),\\H(z)&=\frac{Y(z)}{X(z)}=\frac{1}{1-\frac{1}{2}z^{-1}}=\frac{z}{z-\frac{1}{2}}.\end{aligned}\]</div>
<p>图中给出的实现是因果实现，所以收敛域位于最外极点之外：</p>
<div class="formula">\[\operatorname{ROC}:\left|z\right|>\frac{1}{2}.\]</div>
<p>由 \(H(z)=z/(z-\frac12)\) 可见，零点位于 \(z=0\)，极点位于 \(z=\frac12\)。单位圆包含在收敛域中，因此该系统稳定。</p>
<p>对因果 ROC 使用右边序列的标准反变换对，得到单位脉冲响应：</p>
<div class="formula">\[h[n]=\left(\frac{1}{2}\right)^n u[n].\]</div>
<figure>''' + zero_pole_roc_svg() + r'''<figcaption>零点、极点、单位圆与因果收敛域。</figcaption></figure>
<p>令 \(z=e^{j\omega}\)，频率响应及其幅度、相位可写为：</p>
<div class="formula">\[\begin{aligned}H(e^{j\omega})&=\frac{1}{1-\frac{1}{2}e^{-j\omega}},\\\left|H(e^{j\omega})\right|&=\frac{1}{\sqrt{\frac{5}{4}-\cos\omega}},\\\angle H(e^{j\omega})&=-\arctan\!\left(\frac{\frac{1}{2}\sin\omega}{1-\frac{1}{2}\cos\omega}\right).\end{aligned}\]</div>
<p>直流增益为 \(2\)；当 \(\omega=\pi\) 时，幅度降为 \(\frac{2}{3}\)。这与极点位于正实轴、靠近单位圆的低频增强特性一致。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
