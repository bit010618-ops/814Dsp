"""Seventeenth verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}
</style>"""


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2016 年真题</span><span>详解见 P.____</span></div><p>二、简答题第 1 小题：说明 \(\mathrm{FT}\)、\(\mathrm{LT}\)、\(\mathrm{ZT}\) 的关系；</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2016 年真题：\(\mathrm{FT}\)、\(\mathrm{LT}\) 与 \(\mathrm{ZT}\) 的关系</h2>
<p>三种变换分别描述连续时间信号、连续时间系统与离散时间序列；它们的联系必须同时说明变换变量和收敛域条件。</p>
<p>对连续时间信号 \(x(t)\)，拉普拉斯变换为</p>
<div class="formula">\[X(s)=\mathcal{L}\{x(t)\}=\int_{-\infty}^{\infty}x(t)e^{-st}\,\mathrm{d}t.\]</div>
<p>当 \(s\) 平面的收敛域包含虚轴时，在 \(s=j\Omega\) 上取值便得到傅里叶变换：</p>
<div class="formula">\[X(j\Omega)=X(s)\big|_{s=j\Omega}=\mathcal{F}\{x(t)\}.\]</div>
<p>对离散时间序列 \(x[n]\)，\(z\) 变换为</p>
<div class="formula">\[X(z)=\mathcal{Z}\{x[n]\}=\sum_{n=-\infty}^{\infty}x[n]z^{-n}.\]</div>
<p>当 \(z\) 平面的收敛域包含单位圆时，在 \(z=e^{j\omega}\) 上取值便得到离散时间傅里叶变换：</p>
<div class="formula">\[X\!\left(e^{j\omega}\right)=X(z)\big|_{z=e^{j\omega}}=\mathcal{F}_{\mathrm{DT}}\{x[n]\}.\]</div>
<p>在采样系统的 \(s\) 平面与 \(z\) 平面映射中，常用 \(z=e^{sT}\)。因此虚轴 \(s=j\Omega\) 映到单位圆 \(z=e^{j\Omega T}\)；这说明连续域的频率轴与离散域的单位圆频率轴相对应。若收敛域不包含相应的取值曲线，则上述傅里叶变换不存在，不能只作形式代入。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(text, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
