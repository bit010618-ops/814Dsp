"""Eighteenth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
</style>"""


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2017 年真题</span><span>详解见 P.____</span></div><p>二、简答题第 1 小题：在信号与系统里面，拉氏变换和 \(z\) 变换的对应关系是怎样的？</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2017 年真题：拉氏变换与 \(z\) 变换的映射</h2>
<p>对采样周期为 \(T\) 的连续时间系统，常用指数映射把 \(s\) 平面映到 \(z\) 平面：</p>
<div class="formula">\[z=e^{sT}=e^{(\sigma+j\Omega)T}=e^{\sigma T}e^{j\Omega T},\qquad s=\sigma+j\Omega.\]</div>
<p>由 \(\left|z\right|=e^{\sigma T}\) 可直接得到半平面与单位圆内外的对应：</p>
<div class="formula">\[\begin{aligned}\operatorname{Re}\{s\}<0&\quad\Longleftrightarrow\quad\left|z\right|<1,\\\operatorname{Re}\{s\}=0&\quad\Longleftrightarrow\quad\left|z\right|=1,\\\operatorname{Re}\{s\}>0&\quad\Longleftrightarrow\quad\left|z\right|>1.\end{aligned}\]</div>
<p>因此连续时间系统的极点 \(s_k\) 映为离散系统的极点</p>
<div class="formula">\[z_k=e^{s_kT}.\]</div>
<p>虚轴 \(s=j\Omega\) 映到单位圆 \(z=e^{j\Omega T}\)。在稳定性判断中，连续时间因果稳定系统的极点位于左半平面；经该映射后对应极点位于单位圆内。反之，单位圆外的极点对应右半平面的指数增长分量。实际由连续系统离散化时，还需同时说明所采用的离散化方法和收敛域，不能把这一映射误作任意两个变换表达式之间的无条件代换。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(text, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
