"""Eighth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}.indent{padding-left:1.7em;text-indent:-1.7em}figure{break-inside:avoid;margin:12pt auto;text-align:center}.diagram{display:block;width:min(100%,470pt);height:auto;margin:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}figcaption{color:#315d7c;font-size:9.5pt;margin-top:4pt}
</style>"""


def _math_label(x: float, y: float, width: float, height: float, latex: str, size: int = 16) -> str:
    return (f'<foreignObject x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}">'
            '<div xmlns="http://www.w3.org/1999/xhtml" '
            f'style="height:100%;display:flex;align-items:center;justify-content:center;font-size:{size}px">'
            f'\\({latex}\\)</div></foreignObject>')


def _axis_ticks(left: float, right: float, baseline: float) -> str:
    labels = ((left, '0'), ((left + right) / 2, r'\pi'), (right, r'2\pi'))
    return ''.join(
        f'<path fill="none" stroke="#52616b" stroke-width="1.2" d="M{x:g} {baseline - 7:g}V{baseline + 7:g}"/>'
        + _math_label(x - 26, baseline + 10, 52, 28, label, 15)
        for x, label in labels
    )


def magnitude_svg() -> str:
    """Data-driven plot of 2|sin(omega)| over one 2pi period."""
    left, right, baseline = 90.0, 650.0, 252.0
    points = []
    for index in range(241):
        omega = 2 * math.pi * index / 240
        x = left + (right - left) * index / 240
        y = baseline - 86 * (2 * abs(math.sin(omega)))
        points.append(f"{x:.2f},{y:.2f}")
    return r'''<svg class="diagram" style="width:min(100%,450pt)" viewBox="0 0 720 330" role="img" aria-label="2023 年第八题的幅频响应">
<defs><marker id="arrow-b8-mag" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<path fill="none" stroke="#d8e0e5" stroke-width="1" d="M90 166H650"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b8-mag)" d="M72 252H676"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b8-mag)" d="M90 274V42"/>
<path fill="none" stroke="#52616b" stroke-width="1.2" d="M83 252H97M83 80H97"/><text x="62" y="257" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">0</text><text x="62" y="85" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">2</text>
<polyline data-role="magnitude-curve" fill="none" stroke="#0f8b8d" stroke-width="3" stroke-linejoin="round" points="''' + ' '.join(points) + r'''"/><circle cx="230" cy="80" r="4" fill="#b56b2e"/><circle cx="510" cy="80" r="4" fill="#b56b2e"/>
''' + _axis_ticks(left, right, baseline) + _math_label(632, 268, 50, 30, r'\omega', 18) + _math_label(11, 42, 152, 32, r'\left|H(e^{j\omega})\right|', 16) + r'''<text x="198" y="68" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="13">2</text><text x="478" y="68" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="13">2</text></svg>'''


def phase_svg() -> str:
    """Two continuous principal-phase segments, separated at magnitude zeros."""
    left, right, baseline = 90.0, 650.0, 176.0
    return r'''<svg class="diagram" style="width:min(100%,450pt)" viewBox="0 0 720 330" role="img" aria-label="2023 年第八题的相频响应">
<defs><marker id="arrow-b8-phase" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<path fill="none" stroke="#d8e0e5" stroke-width="1" d="M90 118H650M90 234H650"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b8-phase)" d="M72 176H676"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b8-phase)" d="M90 274V42"/>
<path data-role="phase-segment-left" fill="none" stroke="#0f8b8d" stroke-width="3" d="M92 85L368 267"/><path data-role="phase-segment-right" fill="none" stroke="#0f8b8d" stroke-width="3" d="M372 85L648 267"/><path fill="none" stroke="#b56b2e" stroke-width="1.4" stroke-dasharray="5 4" d="M370 85V267"/>
''' + _axis_ticks(left, right, baseline) + _math_label(632, 192, 50, 30, r'\omega', 18) + _math_label(6, 42, 166, 32, r'\angle H(e^{j\omega})', 16) + _math_label(44, 72, 46, 28, r'\frac{\pi}{2}', 14) + _math_label(37, 222, 58, 28, r'-\frac{\pi}{2}', 14) + r'''<text x="380" y="72" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="13">幅度为零，相位无定义</text></svg>'''


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2023 年真题</span><span>详解见 P.____</span></div><p>八、设某 LSTI 系统的差分方程 \(y(n)=x(n)-x(n-2)\)，试求</p><p class="indent">（1）该系统函数 \(H(z)\) 和单位脉冲响应 \(h(n)\)。</p><p class="indent">（2）判断系统是否因果性和稳定性。</p><p class="indent">（3）画出系统幅频响应和相频响应，该系统是否具有线性相位？</p><p class="indent">（4）若系统输入 \(x(n)=1+2(-1)^n+\cos(0.5\pi n)\)，求系统输出 \(y(n)\)。</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2023 年真题：二阶差分 FIR 系统</h2>
<p>对差分方程作零初始条件下的 \(z\) 变换：</p><div class="formula">\[Y(z)=X(z)-z^{-2}X(z),\qquad H(z)=1-z^{-2}.\]</div>
<p>直接按 \(z\) 变换对反变换，得到有限长单位脉冲响应：</p><div class="formula">\[h[n]=\delta[n]-\delta[n-2].\]</div>
<p>\(h[n]\) 只在 \(n=0\) 和 \(n=2\) 取非零值，故系统因果；同时 \(\sum_n\left|h[n]\right|=2<\infty\)，故系统稳定。它是三抽头反对称 FIR 滤波器。</p>
<p>令 \(z=e^{j\omega}\)，并提出线性相位因子：</p><div class="formula">\[H(e^{j\omega})=1-e^{-j2\omega}=2j e^{-j\omega}\sin\omega,\qquad \left|H(e^{j\omega})\right|=2\left|\sin\omega\right|.\]</div>
<p>幅度在 \(\omega=0,\pi,2\pi\) 处为零，在 \(\omega=\frac{\pi}{2},\frac{3\pi}{2}\) 处取峰值 \(2\)。</p><figure>''' + magnitude_svg() + r'''<figcaption>幅频响应：离散频率轴上有两个完全相同的峰。</figcaption></figure>
<p>在幅度非零处，取 \([0,2\pi]\) 内的主值相位：</p><div class="formula">\[\angle H(e^{j\omega})=\begin{cases}\frac{\pi}{2}-\omega, & 0<\omega<\pi,\\\frac{3\pi}{2}-\omega, & \pi<\omega<2\pi.\end{cases}\]</div>
<p>两段直线的斜率都为 \(-1\)，在幅度为零处发生 \(\pi\) 跳变；因此该系统具有线性相位，对应群时延为 1 个样本。</p><figure>''' + phase_svg() + r'''<figcaption>相频响应：在幅度零点处不定义，故以分段曲线绘制。</figcaption></figure>
<p>最后将输入的三个频率分量分别代入差分关系。直流分量和 \((-1)^n\) 分量的两拍差均为零；而 \(\cos(0.5\pi(n-2))=-\cos(0.5\pi n)\)，所以</p><div class="formula">\[y[n]=2\cos\!\left(0.5\pi n\right).\]</div></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(text, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
