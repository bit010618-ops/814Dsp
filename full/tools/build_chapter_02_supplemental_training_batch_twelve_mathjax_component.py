"""Twelfth verified batch of chapter-two supplemental examination questions."""
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


def _magnitude_svg_raw() -> str:
    left, right, baseline = 86.0, 654.0, 240.0
    points = []
    for index in range(481):
        omega = -math.pi + 2 * math.pi * index / 480
        denominator = math.sin(omega / 2)
        magnitude = 7.0 if abs(denominator) < 1e-10 else abs(math.sin(7 * omega / 2) / denominator)
        x = left + (right - left) * index / 480
        y = baseline - 18.5 * magnitude
        points.append(f"{x:.2f},{y:.2f}")
    ticks = [(left, r'-\pi'), ((left+right)/2, '0'), (right, r'\pi')]
    tick_svg = ''.join(f'<path fill="none" stroke="#52616b" stroke-width="1.2" d="M{x:.2f} {baseline-6:.2f}V{baseline+6:.2f}"/>' + _math_label(x-27, baseline+9, 54, 28, label, 14) for x, label in ticks)
    zero_omegas = (-6*math.pi/7, -4*math.pi/7, -2*math.pi/7, 2*math.pi/7, 4*math.pi/7, 6*math.pi/7)
    zero_ticks = ''.join(f'<path fill="none" stroke="#b56b2e" stroke-width="1.1" d="M{left+(right-left)*(w+math.pi)/(2*math.pi):.2f} {baseline-4:.2f}V{baseline+4:.2f}"/>' for w in zero_omegas)
    return r'''<svg class="diagram" style="width:min(100%,450pt)" viewBox="0 0 740 330" role="img" aria-label="2025 年第四题的 DTFT 幅度谱"><defs><marker id="arrow-b12" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs><path fill="none" stroke="#d8e0e5" stroke-width="1" d="M86 110H654"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b12)" d="M68 240H680"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b12)" d="M370 270V36"/><path fill="none" stroke="#52616b" stroke-width="1.2" d="M363 240H377M363 110H377"/><text x="344" y="245" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">0</text><text x="345" y="115" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">7</text><polyline data-role="magnitude-curve" fill="none" stroke="#0f8b8d" stroke-width="3" stroke-linejoin="round" points="''' + ' '.join(points) + r'''"/>''' + tick_svg + zero_ticks + _math_label(640, 255, 55, 28, r'\omega', 18) + _math_label(16, 38, 180, 32, r'\left|X(e^{j\omega})\right|', 16) + r'''<text x="389" y="91" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="13">主瓣峰值 7</text></svg>'''


def magnitude_svg() -> str:
    """Return the final textbook SVG with a single, non-overlapping origin label."""
    return _magnitude_svg_raw().replace(
        '<text x="344" y="245" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">0</text>',
        '',
    )


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2025 年真题</span><span>详解见 P.____</span></div><p>四、一连续脉冲时间函数表达式为 \(x(t)=u(t)-u(t-7)\)，单位为 s，若以时间间隔 \(T=1\,\mathrm{s}\) 进行等间隔理想采样得 \(x(n)\)，求 \(x(n)\) 的 DTFT，并画出幅度谱波形。</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2025 年真题：有限长矩形序列的 DTFT</h2><p>采样间隔为 \(T=1\,\mathrm{s}\)，因此连续脉冲在整数时刻的样值组成长度为 7 的矩形序列：</p><div class="formula">\[x[n]=u[n]-u[n-7]=\begin{cases}1, & 0\le n\le6,\\0, & \text{其他整数 }n.\end{cases}\]</div><p>对有限长序列直接按 DTFT 定义求和：</p><div class="formula">\[\begin{aligned}X(e^{j\omega})&=\sum_{n=0}^{6}e^{-j\omega n}\\&=e^{-j3\omega}\frac{\sin\left(\frac{7\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}.\end{aligned}\]</div><p>指数项只决定线性相位，不影响幅度。因此</p><div class="formula">\[\left|X(e^{j\omega})\right|=\left|\frac{\sin\left(\frac{7\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}\right|.\]</div><p>在 \(\omega=0\) 处按极限取值为 7；零点位于 \(\omega=\pm\frac{2\pi}{7},\pm\frac{4\pi}{7},\pm\frac{6\pi}{7}\)，并以 \(2\pi\) 为周期重复。</p><figure>''' + magnitude_svg() + r'''<figcaption>一个主值区间内的 DTFT 幅度谱：中心主瓣峰值为 7，两侧出现对称旁瓣。</figcaption></figure></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(text, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
