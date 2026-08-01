"""Third verified batch of chapter-two supplemental exam questions and answers."""
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
p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
.figure-svg{display:block;width:min(100%,470pt);height:auto;margin:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
</style>"""


def ideal_filter_grid_svg() -> str:
    """Four vector plots with actual axes and cutoff markers, no slide watermark."""
    return """<svg class="figure-svg" viewBox="0 0 760 430" role="img" aria-label="理想低通、高通、带通和带阻滤波器的幅频响应">
<defs><marker id="arrow-ideal-b3" markerWidth="8" markerHeight="8" refX="6.5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#174b73"/></marker></defs>
<text x="40" y="28" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">理想低通</text><path fill="none" stroke="#174b73" stroke-width="1.5" marker-end="url(#arrow-ideal-b3)" d="M42 170H336"/><path fill="none" stroke="#174b73" stroke-width="1.5" marker-end="url(#arrow-ideal-b3)" d="M72 186V53"/><path fill="none" stroke="#0f8b8d" stroke-width="3" d="M80 76H195V170H320"/><path fill="none" stroke="#b56b2e" stroke-width="1.2" stroke-dasharray="5 4" d="M195 76V170"/><text x="40" y="242" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">理想高通</text><path fill="none" stroke="#174b73" stroke-width="1.5" marker-end="url(#arrow-ideal-b3)" d="M42 384H336"/><path fill="none" stroke="#174b73" stroke-width="1.5" marker-end="url(#arrow-ideal-b3)" d="M72 400V267"/><path fill="none" stroke="#0f8b8d" stroke-width="3" d="M80 384H195V290H320"/><path fill="none" stroke="#b56b2e" stroke-width="1.2" stroke-dasharray="5 4" d="M195 290V384"/>
<text x="424" y="28" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">理想带通</text><path fill="none" stroke="#174b73" stroke-width="1.5" marker-end="url(#arrow-ideal-b3)" d="M424 170H718"/><path fill="none" stroke="#174b73" stroke-width="1.5" marker-end="url(#arrow-ideal-b3)" d="M454 186V53"/><path fill="none" stroke="#0f8b8d" stroke-width="3" d="M462 170H535V76H630V170H704"/><path fill="none" stroke="#b56b2e" stroke-width="1.2" stroke-dasharray="5 4" d="M535 76V170M630 76V170"/><text x="424" y="242" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">理想带阻</text><path fill="none" stroke="#174b73" stroke-width="1.5" marker-end="url(#arrow-ideal-b3)" d="M424 384H718"/><path fill="none" stroke="#174b73" stroke-width="1.5" marker-end="url(#arrow-ideal-b3)" d="M454 400V267"/><path fill="none" stroke="#0f8b8d" stroke-width="3" d="M462 290H535V384H630V290H704"/><path fill="none" stroke="#b56b2e" stroke-width="1.2" stroke-dasharray="5 4" d="M535 290V384M630 290V384"/>
<text x="305" y="186" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">频率</text><text x="687" y="186" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">频率</text><text x="305" y="400" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">频率</text><text x="687" y="400" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">频率</text><text x="83" y="50" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">幅度</text><text x="465" y="50" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">幅度</text><text x="83" y="264" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">幅度</text><text x="465" y="264" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">幅度</text>
</svg>"""


def zero_pole_svg() -> str:
    """A textbook zero-pole plane for H(z)=1-0.98 z^-6."""
    return """<svg class="figure-svg" viewBox="0 0 640 360" role="img" aria-label="六个零点和单位圆的零极点图">
<defs><marker id="arrow-zero-b3" markerWidth="8" markerHeight="8" refX="6.5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#174b73"/></marker></defs>
<path fill="none" stroke="#174b73" stroke-width="1.7" marker-end="url(#arrow-zero-b3)" d="M72 180H570"/><path fill="none" stroke="#174b73" stroke-width="1.7" marker-end="url(#arrow-zero-b3)" d="M320 325V34"/><circle cx="320" cy="180" r="115" fill="none" stroke="#8797a3" stroke-width="1.5" stroke-dasharray="5 4"/>
<circle cx="432.6" cy="180" r="7" fill="white" stroke="#0f8b8d" stroke-width="3"/><circle cx="376.3" cy="82.5" r="7" fill="white" stroke="#0f8b8d" stroke-width="3"/><circle cx="263.7" cy="82.5" r="7" fill="white" stroke="#0f8b8d" stroke-width="3"/><circle cx="207.4" cy="180" r="7" fill="white" stroke="#0f8b8d" stroke-width="3"/><circle cx="263.7" cy="277.5" r="7" fill="white" stroke="#0f8b8d" stroke-width="3"/><circle cx="376.3" cy="277.5" r="7" fill="white" stroke="#0f8b8d" stroke-width="3"/>
<text x="575" y="188" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">实部</text><text x="328" y="43" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">虚部</text><text x="442" y="169" fill="#0f8b8d" font-family="Microsoft YaHei, sans-serif" font-size="13">零点</text><text x="400" y="73" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">单位圆</text><text x="328" y="197" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">原点</text><text x="185" y="337" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">无有限极点</text>
</svg>"""


def training_html() -> str:
    return (
        r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1>
<div class="exam-head"><span>2013 年真题：理想滤波器幅频响应</span><span>详解见 P.____</span></div>
<p>三、画出理想低通、高通、带通、带阻频率滤波器的幅频响应，要求标出截止频率。</p></section>
<section class="exam-page"><div class="exam-head"><span>2013 年真题：单位脉冲响应与频率特性</span><span>详解见 P.____</span></div>
<p>六、离散系统的单位脉冲响应 \(h(n)=\delta(n)-0.98\delta(n-6)\)，求系统函数 \(H(z)\)，画出零极点图和该系统的幅频特性。</p></section>'''
    )


def answers_html() -> str:
    return (
        r'''<section><h1>真题整理详解（续）</h1><h2>2013 年真题：四类理想滤波器</h2>
<p>设截止角频率为 \(\omega_c\)，带通、带阻的两个截止角频率为 \(0<\omega_1<\omega_2<\pi\)。图中虚线即各截止频率的位置：</p>'''
        + ideal_filter_grid_svg()
        + r'''<p>四类理想滤波器的幅度响应可分别写成</p>
<div class="formula">\[\left|H_{\mathrm{LP}}(e^{j\omega})\right|=\begin{cases}1,&|\omega|<\omega_c,\\0,&\omega_c<|\omega|\le\pi,\end{cases}\qquad \left|H_{\mathrm{HP}}(e^{j\omega})\right|=\begin{cases}0,&|\omega|<\omega_c,\\1,&\omega_c<|\omega|\le\pi.\end{cases}\]</div>
<div class="formula">\[\left|H_{\mathrm{BP}}(e^{j\omega})\right|=\begin{cases}1,&\omega_1<|\omega|<\omega_2,\\0,&\text{其他频率},\end{cases}\qquad \left|H_{\mathrm{BS}}(e^{j\omega})\right|=\begin{cases}0,&\omega_1<|\omega|<\omega_2,\\1,&\text{其他频率}.\end{cases}\]</div></section>
<section><h2>2013 年真题：由单位脉冲响应求零极点与幅频特性</h2>
<p>对 \(h(n)\) 作 \(z\) 变换，得到有限长 FIR 系统函数</p>
<div class="formula">\[H(z)=1-0.98z^{-6}.\]</div>
<p>令 \(H(z)=0\)，六个零点等角分布在半径 \(0.98^{1/6}\) 的圆上；系统没有有限极点。零极点图如下：</p>'''
        + zero_pole_svg()
        + r'''<p>零点的精确位置为</p>
<div class="formula">\[z_k=0.98^{1/6}e^{j k\pi/3},\qquad k=0,1,\ldots,5.\]</div>
<p>代入单位圆 \(z=e^{j\omega}\) 可得频率响应与幅度特性：</p>
<div class="formula">\[H(e^{j\omega})=1-0.98e^{-j6\omega},\qquad \left|H(e^{j\omega})\right|=\sqrt{1+0.98^2-1.96\cos(6\omega)}.\]</div>
<p>因此当 \(6\omega\) 接近 \(2k\pi\) 时幅度出现很深的陷波；在每个 \(2\pi\) 周期内共有六个等间隔的抑制频点。</p></section>'''
    )


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    completed = subprocess.run(
        [
            str(EDGE),
            "--headless=new",
            "--disable-gpu",
            "--virtual-time-budget=10000",
            "--dump-dom",
            html.resolve().as_uri(),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout
