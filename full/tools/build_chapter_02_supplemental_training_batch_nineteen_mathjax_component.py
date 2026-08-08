"""Nineteenth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
</style>"""


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2020 年真题（填空题第 2、3 小题）</span><span>详解见 P.____</span></div><p>2．序列实部的傅里叶变换等于傅里叶变换的______分量；</p><p>3．一个线性时不变离散系统稳定的充要条件是系统函数的收敛域包含______；</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2020 年真题：DTFT 的共轭对称分量与稳定 ROC</h2>
<p><strong>第 2 小题。</strong>任意复序列可写为实部与虚部之和。实部满足</p>
<div class="formula">\[\operatorname{Re}\{x[n]\}=\frac{1}{2}\left(x[n]+x^*[n]\right).\]</div>
<p>利用共轭序列的 DTFT 对应关系，其傅里叶变换为</p>
<div class="formula">\[\mathcal{F}_{\mathrm{DT}}\!\left\{\operatorname{Re}\{x[n]\}\right\}=\frac{1}{2}\left[X\!\left(e^{j\omega}\right)+X^*\!\left(e^{-j\omega}\right)\right].\]</div>
<p>右端正是 \(X(e^{j\omega})\) 的<strong>共轭对称分量</strong>，故填：<strong>共轭对称</strong>。</p>
<p><strong>第 3 小题。</strong>离散 LTI 系统稳定等价于单位冲激响应绝对可和：</p>
<div class="formula">\[\sum_{n=-\infty}^{\infty}\left|h[n]\right|&lt;\infty.\]</div>
<p>对有理系统函数，这又等价于其收敛域包含单位圆，因而频率响应能够在单位圆上取值：</p>
<div class="formula">\[\left|z\right|=1.\]</div>
<p>故填：<strong>单位圆</strong>。注意这里要求的是整个单位圆包含在 ROC 内，而不是仅有某一个单位圆上的点。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(text, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
