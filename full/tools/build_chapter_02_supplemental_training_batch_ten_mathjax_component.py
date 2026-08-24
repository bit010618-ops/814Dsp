"""Tenth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}figure{break-inside:avoid;margin:12pt auto;text-align:center}.diagram{display:block;width:min(100%,470pt);height:auto;margin:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}figcaption{color:#315d7c;font-size:9.5pt;margin-top:4pt}
</style>"""


def _math_label(x: float, y: float, width: float, height: float, latex: str, size: int = 16) -> str:
    return (f'<foreignObject x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}">'
            '<div xmlns="http://www.w3.org/1999/xhtml" '
            f'style="height:100%;display:flex;align-items:center;justify-content:center;font-size:{size}px">'
            f'\\({latex}\\)</div></foreignObject>')


def flow_svg() -> str:
    """Programmatic textbook system graph for y[n] = x[n] - x[n-N]."""
    return r'''<svg class="diagram" data-source-candidate-id="2022-q八-01" viewBox="0 0 720 350" role="img" aria-label="2022 年第八题的离散 LTI 系统流图">
<defs><marker id="arrow-b10-flow" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<path fill="none" stroke="#174b73" stroke-width="2.5" marker-end="url(#arrow-b10-flow)" d="M58 116H486"/><path fill="none" stroke="#174b73" stroke-width="2.5" marker-end="url(#arrow-b10-flow)" d="M522 116H668"/>
<circle cx="174" cy="116" r="5" fill="#174b73" data-role="branch-node"/><path fill="none" stroke="#174b73" stroke-width="2.5" marker-end="url(#arrow-b10-flow)" d="M174 121V238H260"/>
<rect data-role="gain-block" x="260" y="214" width="82" height="48" rx="5" fill="#fff" stroke="#0f8b8d" stroke-width="2"/>
<path fill="none" stroke="#174b73" stroke-width="2.5" marker-end="url(#arrow-b10-flow)" d="M342 238H390"/>
<rect data-role="delay-block" x="390" y="214" width="98" height="48" rx="5" fill="#fff" stroke="#0f8b8d" stroke-width="2"/>
<path fill="none" stroke="#174b73" stroke-width="2.5" marker-end="url(#arrow-b10-flow)" d="M488 238H504V151"/>
<circle data-role="summing-node" cx="504" cy="116" r="18" fill="#fff" stroke="#174b73" stroke-width="2.5"/><text x="497" y="123" fill="#174b73" font-family="Georgia, serif" font-size="22">+</text>
''' + _math_label(38, 65, 84, 34, r'x[n]', 18) + _math_label(604, 66, 84, 34, r'y[n]', 18) + _math_label(267, 218, 68, 38, r'-1', 18) + _math_label(396, 216, 86, 38, r'z^{-N}', 18) + r'''<text x="170" y="310" text-anchor="middle" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">输入分支</text><text x="390" y="310" text-anchor="middle" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">延时反馈支路</text><text x="570" y="310" text-anchor="middle" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">求和输出</text></svg>'''


def pole_zero_svg() -> str:
    center_x, center_y, radius = 310.0, 215.0, 130.0
    zeros = []
    for k in range(8):
        theta = 2 * math.pi * k / 8
        x = center_x + radius * math.cos(theta)
        y = center_y - radius * math.sin(theta)
        zeros.append(f'<circle data-role="zero" cx="{x:.2f}" cy="{y:.2f}" r="7" fill="#fff" stroke="#0f8b8d" stroke-width="3"/>')
    return r'''<svg class="diagram" style="width:min(100%,410pt)" viewBox="0 0 620 420" role="img" aria-label="2022 年第八题的零极点图">
<defs><marker id="arrow-b10-pz" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<path fill="none" stroke="#a6b4be" stroke-width="1.8" stroke-dasharray="5 4" d="M310 85A130 130 0 1 0 310 345A130 130 0 1 0 310 85"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b10-pz)" d="M80 215H550"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b10-pz)" d="M310 370V48"/>
<path fill="none" stroke="#52616b" stroke-width="1.2" d="M180 208V222M440 208V222M303 85H317M303 345H317"/><text x="166" y="241" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">−1</text><text x="436" y="241" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">1</text><text x="322" y="98" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">j</text><text x="320" y="350" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">−j</text><text x="320" y="241" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">0</text>
''' + ''.join(zeros) + r'''<path data-role="pole-at-origin" fill="none" stroke="#b56b2e" stroke-width="3.2" d="M299 204L321 226M321 204L299 226"/><text x="331" y="202" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="14">8 重极点</text>
''' + _math_label(520, 218, 82, 34, r'\operatorname{Re}(z)', 15) + _math_label(225, 30, 170, 34, r'\operatorname{Im}(z)', 15) + r'''<text x="108" y="392" fill="#0f8b8d" font-family="Microsoft YaHei, sans-serif" font-size="14">○ 零点：单位圆上 8 个八次单位根</text></svg>'''


def magnitude_svg() -> str:
    left, right, baseline = 90.0, 650.0, 252.0
    points = []
    for index in range(321):
        omega = 2 * math.pi * index / 320
        x = left + (right - left) * index / 320
        y = baseline - 82 * (2 * abs(math.sin(4 * omega)))
        points.append(f"{x:.2f},{y:.2f}")
    ticks = [(left, '0'), (left + (right-left)/4, r'\frac{\pi}{2}'), (left + (right-left)/2, r'\pi'), (left + 3*(right-left)/4, r'\frac{3\pi}{2}'), (right, r'2\pi')]
    tick_svg = ''.join(f'<path fill="none" stroke="#52616b" stroke-width="1.2" d="M{x:.2f} {baseline-6:.2f}V{baseline+6:.2f}"/>' + _math_label(x-33, baseline+10, 66, 30, label, 14) for x, label in ticks)
    return r'''<svg class="diagram" style="width:min(100%,450pt)" viewBox="0 0 720 330" role="img" aria-label="2022 年第八题的幅频响应">
<defs><marker id="arrow-b10-mag" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs><path fill="none" stroke="#d8e0e5" stroke-width="1" d="M90 170H650"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b10-mag)" d="M72 252H676"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b10-mag)" d="M90 274V42"/><path fill="none" stroke="#52616b" stroke-width="1.2" d="M83 252H97M83 88H97"/><text x="62" y="257" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">0</text><text x="62" y="93" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">2</text><polyline data-role="magnitude-curve" fill="none" stroke="#0f8b8d" stroke-width="3" stroke-linejoin="round" points="''' + ' '.join(points) + r'''"/>
''' + tick_svg + _math_label(632, 268, 50, 30, r'\omega', 18) + _math_label(11, 42, 152, 32, r'\left|H(e^{j\omega})\right|', 16) + r'''<text x="332" y="66" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="13">峰值 2</text></svg>'''


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2022 年真题</span><span>详解见 P.____</span></div><p>八、一离散时间 LTI 系统流图如下图所示：</p><figure>''' + flow_svg() + r'''<figcaption>离散 LTI 系统流图。</figcaption></figure><p class="indent">（1）该系统的系统函数 \(H(z)\)；</p><p class="indent">（2）当 \(N=8\) 时，画出该系统的零极点图及幅频响应曲线。</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2022 年真题：延时差分系统的频率特性</h2><p>由流图可直接读出：输出由直通分量和经 \(N\) 拍延时、增益为 \(-1\) 的分量相加，故</p><div class="formula">\[y[n]=x[n]-x[n-N].\]</div><p>在零初始条件下作 \(z\) 变换：</p><div class="formula">\[Y(z)=\left(1-z^{-N}\right)X(z),\qquad H(z)=1-z^{-N}=\frac{z^N-1}{z^N}.\]</div><p>令 \(N=8\)。分子为零时给出单位圆上的 8 个零点；分母则在原点给出 8 重极点：</p><div class="formula">\[z_k=e^{j\frac{2\pi k}{8}},\quad k=0,1,\ldots,7;\qquad z=0\text{ 为 8 重极点}.\]</div><figure>''' + pole_zero_svg() + r'''<figcaption>零点均匀分布在单位圆上，原点为 8 重极点。</figcaption></figure><p>令 \(z=e^{j\omega}\)，并提出线性相位因子，可得幅度：</p><div class="formula">\[H(e^{j\omega})=1-e^{-j8\omega}=2j e^{-j4\omega}\sin(4\omega),\qquad \left|H(e^{j\omega})\right|=2\left|\sin(4\omega)\right|.\]</div><p>因此在 \(\omega=\frac{k\pi}{4}\) 处出现零点，一个 \(2\pi\) 周期内共有 8 个幅度瓣，峰值均为 2。</p><figure>''' + magnitude_svg() + r'''<figcaption>幅频响应：每个半周期形成一个峰，零点与单位圆零点的角度相对应。</figcaption></figure></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(text, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
