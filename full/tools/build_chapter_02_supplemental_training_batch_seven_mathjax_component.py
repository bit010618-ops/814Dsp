"""Seventh verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}figure{break-inside:avoid;margin:12pt auto;text-align:center}.diagram{display:block;width:min(100%,470pt);height:auto;margin:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}figcaption{color:#315d7c;font-size:9.5pt;margin-top:4pt}
</style>"""


def _math_label(x: float, y: float, width: float, height: float, latex: str, *, size: int = 16) -> str:
    return (
        f'<foreignObject x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}">'
        '<div xmlns="http://www.w3.org/1999/xhtml" '
        f'style="height:100%;display:flex;align-items:center;justify-content:center;font-size:{size}px">'
        f'\\({latex}\\)</div></foreignObject>'
    )


def zero_pole_svg() -> str:
    """Draw the 2024 zero-pole diagram from the actual roots of H(z)."""
    return r'''<svg class="diagram" style="width:min(100%,410pt)" viewBox="0 0 720 430" role="img" aria-label="2024 年第二章真题的零极点图">
<defs><marker id="arrow-b7-z" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b7-z)" d="M84 210H656"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b7-z)" d="M320 366V48"/>
<circle cx="320" cy="210" r="112" fill="none" stroke="#8797a3" stroke-width="1.6" stroke-dasharray="6 4"/>
<path data-role="zero-at-minus-one" fill="white" stroke="#0f8b8d" stroke-width="4" d="M208 210m-10 0a10 10 0 1 0 20 0a10 10 0 1 0-20 0"/>
<path data-role="zero-at-plus-one" fill="white" stroke="#0f8b8d" stroke-width="4" d="M432 210m-10 0a10 10 0 1 0 20 0a10 10 0 1 0-20 0"/>
<path data-role="pole-at-plus-j08" fill="none" stroke="#b56b2e" stroke-width="4" d="M310 120l20 20m0-20l-20 20"/>
<path data-role="pole-at-minus-j08" fill="none" stroke="#b56b2e" stroke-width="4" d="M310 280l20 20m0-20l-20 20"/>
<circle cx="320" cy="210" r="3.6" fill="#174b73"/>
<path fill="none" stroke="#52616b" stroke-width="1.2" d="M208 202V218M432 202V218M312 120H328M312 300H328"/>
''' + _math_label(650, 191, 54, 32, r'\operatorname{Re}\{z\}', size=17) + _math_label(286, 42, 64, 32, r'\operatorname{Im}\{z\}', size=17) + _math_label(304, 220, 34, 28, '0') + _math_label(180, 221, 55, 28, '-1') + _math_label(409, 221, 55, 28, '1') + _math_label(267, 102, 54, 28, 'j0.8') + _math_label(264, 292, 58, 28, '-j0.8') + r'''<text x="358" y="105" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">单位圆</text><path fill="none" stroke="#8797a3" stroke-width="1.2" d="M355 110L386 132"/><text x="448" y="191" fill="#0f8b8d" font-family="Microsoft YaHei, sans-serif" font-size="14">零点</text><text x="347" y="154" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="14">极点</text></svg>'''


def magnitude_response_svg() -> str:
    """Plot the exact sampled magnitude response using real response data."""
    left, right, top, baseline = 92.0, 662.0, 66.0, 282.0
    points: list[str] = []
    for index in range(241):
        omega = 2 * math.pi * index / 240
        magnitude = 0.36 * abs(math.sin(omega)) / math.sqrt(1.4096 + 1.28 * math.cos(2 * omega))
        x = left + (right - left) * index / 240
        y = baseline - 184 * magnitude
        points.append(f"{x:.2f},{y:.2f}")
    curve = " ".join(points)
    ticks = (
        (left, "0"),
        (left + (right - left) / 4, r"\frac{\pi}{2}"),
        (left + (right - left) / 2, r"\pi"),
        (left + 3 * (right - left) / 4, r"\frac{3\pi}{2}"),
        (right, r"2\pi"),
    )
    tick_svg = "".join(
        f'<path fill="none" stroke="#52616b" stroke-width="1.2" d="M{x:.2f} {baseline - 7:.2f}V{baseline + 7:.2f}"/>'
        + _math_label(x - 28, baseline + 12, 56, 28, label, size=15)
        for x, label in ticks
    )
    return r'''<svg class="diagram" style="width:min(100%,470pt)" viewBox="0 0 750 380" role="img" aria-label="2024 年第二章真题的幅频响应">
<defs><marker id="arrow-b7-w" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<path fill="none" stroke="#d8e0e5" stroke-width="1" d="M92 190H662"/><path fill="none" stroke="#d8e0e5" stroke-width="1" d="M92 98H662"/>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b7-w)" d="M76 282H684"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b7-w)" d="M92 304V48"/>
<path fill="none" stroke="#52616b" stroke-width="1.2" d="M85 282H99M85 98H99"/>
<text x="62" y="287" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">0</text><text x="62" y="103" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">1</text>
<polyline data-role="magnitude-curve" fill="none" stroke="#0f8b8d" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" points="''' + curve + r'''"/>
<circle cx="234.5" cy="98" r="4" fill="#b56b2e"/><circle cx="519.5" cy="98" r="4" fill="#b56b2e"/>
''' + tick_svg + _math_label(640, 298, 70, 32, r'\omega', size=18) + _math_label(18, 48, 150, 34, r'\left|H(e^{j\omega})\right|', size=17) + r'''<text x="188" y="80" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="13">峰值 1</text><text x="473" y="80" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="13">峰值 1</text></svg>'''


def training_html() -> str:
    """Preserve the independent 2024 DSP subquestion exactly."""
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2024 年真题</span><span>详解见 P.____</span></div><p>2.已知某线性移不变系统的系统函数是</p><div class="formula">\[H(z)=0.18\frac{1-z^{-2}}{1+0.64z^{-2}}.\]</div><p>请画出系统函数 \(H(z)\) 的零极点图，并粗略画出 \(\omega\in[0,2\pi]\) 的系统幅频响应 \(\left|H(e^{j\omega})\right|\)。</p></section>'''


def answers_html() -> str:
    """Detailed z-plane and magnitude-response solution for the 2024 question."""
    return r'''<section><h1>真题整理详解（续）</h1>
<h2>2024 年真题：零极点与幅频响应</h2>
<p>先同乘 \(z^2\)，把系统函数改写成便于读出零、极点的多项式比值：</p>
<div class="formula">\[H(z)=0.18\frac{1-z^{-2}}{1+0.64z^{-2}}=0.18\frac{z^2-1}{z^2+0.64}.\]</div>
<p>因此分子给出两个零点，分母给出一对共轭极点：</p>
<div class="formula">\[z=\pm1\quad\text{（零点）},\qquad z=\pm j0.8\quad\text{（极点）}.\]</div>
<p>题目没有指定因果性或收敛域，所以零极点图只标出零、极点与单位圆，不额外假定 ROC。</p>
<figure>''' + zero_pole_svg() + r'''<figcaption>零点位于单位圆的 \(z=\pm1\)；极点位于虚轴上的 \(z=\pm j0.8\)。</figcaption></figure>
<p>在单位圆上令 \(z=e^{j\omega}\)。分子与分母分别按共轭相乘求模：</p>
<div class="formula">\[\begin{aligned}\left|1-e^{-j2\omega}\right|&=2\left|\sin\omega\right|,\\\left|1+0.64e^{-j2\omega}\right|&=\sqrt{1.4096+1.28\cos(2\omega)}.\end{aligned}\]</div>
<p>于是幅频响应的精确表达式为</p>
<div class="formula">\[\left|H(e^{j\omega})\right|=\frac{0.36\left|\sin\omega\right|}{\sqrt{1.4096+1.28\cos(2\omega)}}.\]</div>
<p>为画出草图，先标出一个周期内的零点和峰值：\(\left|H(e^{j0})\right|=\left|H(e^{j\pi})\right|=\left|H(e^{j2\pi})\right|=0\)，而 \(\left|H(e^{j\pi/2})\right|=\left|H(e^{j3\pi/2})\right|=1\)。因此曲线在 \([0,2\pi]\) 内呈两个相同的带通形峰，关于 \(\omega=\pi\) 对称。</p>
<figure>''' + magnitude_response_svg() + r'''<figcaption>根据精确幅度公式计算的 \(0\leq\omega\leq2\pi\) 幅频响应；作答时标出零点和两个峰值即可。</figcaption></figure>
</section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
