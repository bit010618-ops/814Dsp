"""Ninth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
</style>"""


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2020 年真题</span><span>详解见 P.____</span></div><p>四、设 LTI 系统的频率响应为 \(H(e^{j\omega})=\frac{1-e^{-2j\omega}}{1+0.5e^{-2j\omega}}\)，输入信号为 \(x[n]=\cos\left(\frac{\pi n}{2}\right)\)，求系统的输出信号。</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2020 年真题：频率响应作用于余弦输入</h2>
<p>先将余弦写成正、负两支复指数之和：</p><div class="formula">\[x[n]=\frac{1}{2}e^{j\frac{\pi}{2}n}+\frac{1}{2}e^{-j\frac{\pi}{2}n}.\]</div>
<p>对 LTI 系统，频率为 \(\omega_0\) 的复指数 \(e^{j\omega_0 n}\) 是特征函数，输出只需乘以对应的频率响应。因此分别计算 \(\omega=\pm\frac{\pi}{2}\) 处的增益：</p>
<div class="formula">\[\begin{aligned}H\!\left(e^{j\frac{\pi}{2}}\right)&=\frac{1-e^{-j\pi}}{1+0.5e^{-j\pi}}=\frac{1-(-1)}{1+0.5(-1)}=4,\\H\!\left(e^{-j\frac{\pi}{2}}\right)&=\frac{1-e^{j\pi}}{1+0.5e^{j\pi}}=\frac{1-(-1)}{1+0.5(-1)}=4.\end{aligned}\]</div>
<p>两个共轭频率处的响应均为实数 \(4\)，所以不会引入附加相位，两个分量仍按原来的相位相加：</p>
<div class="formula">\[\begin{aligned}y[n]&=\frac{1}{2}\cdot4e^{j\frac{\pi}{2}n}+\frac{1}{2}\cdot4e^{-j\frac{\pi}{2}n}\\&=4\cos\left(\frac{\pi n}{2}\right).\end{aligned}\]</div>
<p>故系统在该输入频率处的幅度增益为 \(4\)，无需附加相位偏移。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(text, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
