"""Fourth verified batch of chapter-two supplemental exam questions and answers."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}.indent{padding-left:1.7em;text-indent:-1.7em}.diagram{display:block;width:min(100%,470pt);height:auto;margin:10pt auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
</style>"""


def feedback_system_svg() -> str:
    """Watermark-free vector redraw of the two-delay feedback structure."""
    return """<svg class="diagram" viewBox="0 0 780 360" role="img" aria-label="2013 年第五题的离散系统结构图">
<defs><marker id="arrow-b4-f" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker><marker id="arrow-b4-g" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#0f8b8d"/></marker></defs>
<text x="34" y="132" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">x[n]</text><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b4-f)" d="M80 128H165"/><circle cx="190" cy="128" r="25" fill="white" stroke="#174b73" stroke-width="2"/><text x="180" y="136" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="18">Σ</text><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b4-f)" d="M215 128H675"/><circle cx="500" cy="128" r="4" fill="#174b73"/><text x="685" y="132" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">y[n]</text>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b4-f)" d="M500 128V175H540"/><rect x="542" y="151" width="78" height="48" rx="5" fill="#f4f7f8" stroke="#0f8b8d" stroke-width="2"/><text x="558" y="181" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">延时</text><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b4-f)" d="M620 175H666"/><rect x="668" y="151" width="78" height="48" rx="5" fill="#f4f7f8" stroke="#0f8b8d" stroke-width="2"/><text x="684" y="181" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">延时</text>
<path fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-b4-g)" d="M620 175V240H190V153"/><text x="365" y="232" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="16">5/2</text><path fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-b4-g)" d="M746 175V312H125V148H175"/><text x="320" y="303" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="16">−1</text><text x="36" y="345" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">每个延时器均为一拍延时；主信号流自左向右。</text>
</svg>"""


def feedback_system_svg_v2() -> str:
    """Textbook feedback diagram with two separate gain blocks and summer ports."""
    return r'''<svg class="diagram" viewBox="0 0 780 370" role="img" aria-label="2013 年第五题与 2015 年第四题的离散系统结构图">
<defs>
  <marker id="arrow-b4-v2-main" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker>
  <marker id="arrow-b4-v2-feedback" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#0f8b8d"/></marker>
</defs>
<text x="36" y="125" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">x[n]</text>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b4-v2-main)" d="M80 120H173"/>
<circle cx="205" cy="120" r="32" fill="white" stroke="#174b73" stroke-width="2"/>
<text x="193" y="130" fill="#315d7c" font-family="Cambria Math, serif" font-size="24">Σ</text>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b4-v2-main)" d="M237 120H688"/>
<circle cx="495" cy="120" r="4" fill="#174b73"/>
<text x="697" y="125" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">y[n]</text>

<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b4-v2-main)" d="M495 120V165H535"/>
<rect x="535" y="141" width="82" height="48" rx="5" fill="#f4f7f8" stroke="#0f8b8d" stroke-width="2"/>
<text x="552" y="171" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">延时</text>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b4-v2-main)" d="M617 165H660"/>
<rect x="660" y="141" width="82" height="48" rx="5" fill="#f4f7f8" stroke="#0f8b8d" stroke-width="2"/>
<text x="677" y="171" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="16">延时</text>

<path fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-b4-v2-feedback)" d="M617 165V235H515"/>
<rect data-role="feedback-first-gain" x="435" y="213" width="80" height="44" rx="5" fill="#f4f7f8" stroke="#0f8b8d" stroke-width="2"/>
<foreignObject x="435" y="213" width="80" height="44"><div xmlns="http://www.w3.org/1999/xhtml" style="height:44px;display:flex;align-items:center;justify-content:center;font-size:17px">\(\frac{5}{2}\)</div></foreignObject>
<path data-role="feedback-first-output" fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-b4-v2-feedback)" d="M435 235H390"/>
<path data-role="feedback-first-return" data-port="lower-left" fill="none" stroke="#0f8b8d" stroke-width="2" d="M390 235H150V142H180"/>

<path fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-b4-v2-feedback)" d="M742 165V310H515"/>
<rect data-role="feedback-second-gain" x="435" y="288" width="80" height="44" rx="5" fill="#f4f7f8" stroke="#0f8b8d" stroke-width="2"/>
<foreignObject x="435" y="288" width="80" height="44"><div xmlns="http://www.w3.org/1999/xhtml" style="height:44px;display:flex;align-items:center;justify-content:center;font-size:17px">\(-1\)</div></foreignObject>
<path data-role="feedback-second-output" fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-b4-v2-feedback)" d="M435 310H390"/>
<path data-role="feedback-second-return" data-port="bottom" fill="none" stroke="#0f8b8d" stroke-width="2" d="M390 310H205V152"/>

<text x="36" y="356" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">每个延时器均为一拍延时；主信号流自左向右。</text>
</svg>'''


def training_html() -> str:
    return (
        r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1>
<div class="exam-head"><span>2013、2015 年真题</span><span>详解见 P.____</span></div>
<p>2013 年第五题／2015 年第四题：某离散系统如图所示：</p>'''
        + feedback_system_svg_v2()
        + r'''<p class="indent">（1）求出系统函数 \(H(z)\)，并求出收敛域；</p><p class="indent">（2）求出系统的单位脉冲响应；</p><p class="indent">（3）写出一个满足稳定、非因果的单位脉冲响应函数。</p></section>'''
    )


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2013、2015 年真题：两延时反馈系统</h2>
<p>由两个反馈支路直接列出差分方程：</p>
<div class="formula">\[y[n]=x[n]+\frac{5}{2}y[n-1]-y[n-2].\]</div>
<p>作 \(z\) 变换可得</p>
<div class="formula">\[H(z)=\frac{Y(z)}{X(z)}=\frac{1}{1-\frac{5}{2}z^{-1}+z^{-2}}=\frac{1}{(1-2z^{-1})\left(1-\frac12z^{-1}\right)}.\]</div>
<p>图示为因果实现，因此收敛域为 \(|z|>2\)。先作部分分式展开：</p>
<div class="formula">\[H(z)=\frac{4}{3}\frac{1}{1-2z^{-1}}-\frac{1}{3}\frac{1}{1-\frac12z^{-1}}.\]</div>
<p>因果单位脉冲响应为</p>
<div class="formula">\[h[n]=\frac{4}{3}2^n u[n]-\frac{1}{3}\left(\frac12\right)^n u[n].\]</div>
<p>要同时满足稳定与非因果，收敛域取两个极点之间的 \(\frac12<|z|<2\)。半径为 2 的极点项取左边序列，半径为 \(\frac12\) 的极点项取右边序列：</p>
<div class="formula">\[h_{\mathrm{s}}[n]=-\frac{4}{3}2^n u[-n-1]-\frac{1}{3}\left(\frac12\right)^n u[n].\]</div></section>'''


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
