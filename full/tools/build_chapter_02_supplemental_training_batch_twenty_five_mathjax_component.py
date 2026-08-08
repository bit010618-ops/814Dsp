"""2007 constant-sequence DTFT question."""
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
p{margin:5pt 0 8pt}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.exam-page{break-before:page;min-height:230mm}
.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
</style>"""


def training_html() -> str:
    return r'''<section class="exam-page">
<h1>第二章 补充真题（续）</h1>
<div class="exam-head"><span>2007 年真题</span><span>详解见 P.____</span></div>
<p>一、计算</p>
<p>2.若信号\(x(n)=k\)，\(k\)为常数，求其离散时间傅里叶变换；</p>
</section>'''


def answers_html() -> str:
    return r'''<section>
<h1>真题整理详解（续）</h1>
<h2>2007 年真题：常数序列的 DTFT</h2>
<p>常数序列不绝对可和，其离散时间傅里叶变换须在广义函数意义下理解。将常数 \(k\) 提出求和号：</p>
<div class="formula">\[\begin{aligned}
X\!\left(e^{j\omega}\right)
&=\sum_{n=-\infty}^{\infty} k e^{-j\omega n}\\
&=k\sum_{n=-\infty}^{\infty}e^{-j\omega n}.
\end{aligned}\]</div>
<p>利用频域冲激列恒等式</p>
<div class="formula">\[\sum_{n=-\infty}^{\infty}e^{-j\omega n}=2\pi\sum_{m=-\infty}^{\infty}\delta\!\left(\omega-2\pi m\right),\]</div>
<p>得到</p>
<div class="formula">\[\boxed{X\!\left(e^{j\omega}\right)=2\pi k\sum_{m=-\infty}^{\infty}\delta\!\left(\omega-2\pi m\right).}\]</div>
<p>因此，\(x[n]=k\) 的频谱是在 \(\omega=2\pi m\) 处的 \(2\pi\) 周期冲激列；在主值区间 \([-\pi,\pi]\) 内只保留位于 \(\omega=0\) 的冲激 \(2\pi k\delta(\omega)\)。</p>
</section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script>
<script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>''',
        encoding="utf-8",
    )
    return output


def rendered_dom(html: Path) -> str:
    return subprocess.run(
        [str(EDGE), "--headless=new", "--disable-gpu", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
