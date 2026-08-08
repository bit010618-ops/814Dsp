"""Twentieth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
</style>"""


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2005 年真题</span><span>详解见 P.____</span></div><p>一、计算</p><p>4.求 \(F(z)=\frac{z^2}{z^2-2z-3}\) 在收敛域为 \(1<\left|z\right|<3\) 时的原序列 \(f(n)\)。</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2005 年真题：指定 ROC 的反 \(z\) 变换</h2>
<p>先对分母因式分解，并按标准 \(z/(z-a)\) 形式作部分分式展开：</p>
<div class="formula">\[\begin{aligned}F(z)&=\frac{z^2}{(z-3)(z+1)}\\&=\frac{1}{2}\frac{z}{z-3}+\frac{1}{2}\frac{z}{z+1}.\end{aligned}\]</div>
<p>极点分别为 \(z=3\) 和 \(z=-1\)。给定收敛域为 \(1<\left|z\right|<3\)，因此相对于极点 \(3\) 取内侧 ROC，而相对于极点 \(-1\) 取外侧 ROC：</p>
<div class="formula">\[\begin{aligned}\frac{z}{z-3},\quad \left|z\right|<3&\quad\Longleftrightarrow\quad-3^n u[-n-1],\\\frac{z}{z+1},\quad \left|z\right|>1&\quad\Longleftrightarrow\quad(-1)^n u[n].\end{aligned}\]</div>
<p>将两个分量连同各自的系数相加，得到满足指定 ROC 的双边序列：</p>
<div class="formula">\[f[n]=\frac{1}{2}(-1)^n u[n]-\frac{1}{2}3^n u[-n-1].\]</div>
<p>其中第一项是右边序列，第二项是左边序列；二者的 ROC 交集恰为 \(1<\left|z\right|<3\)，与题设一致。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(text, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
