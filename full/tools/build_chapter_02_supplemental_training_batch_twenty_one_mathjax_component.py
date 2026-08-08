"""Twenty-first verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations
import subprocess
from pathlib import Path
from full.tools.render_mathjax_formula import EDGE, MATHJAX

STYLE = r"""<style>@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}</style>"""

def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2015 年真题</span><span>详解见 P.____</span></div><p>一、填空题</p><p>2.已知 \(\mathrm{FT}[x(n)]=X(e^{j\omega})\)，由 \(x(n)\) 求出 \(\operatorname{Re}\{X(e^{j\omega})\}\) 对应的序列为________；</p></section>'''

def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2015 年真题：频谱实部对应的序列</h2><p>频谱实部可由频谱与其共轭相加得到：</p><div class="formula">\[\operatorname{Re}\!\left\{X(e^{j\omega})\right\}=\frac{1}{2}\left[X(e^{j\omega})+X^*(e^{j\omega})\right].\]</div><p>由 DTFT 的共轭—反折性质</p><div class="formula">\[X^*(e^{j\omega})\quad\Longleftrightarrow\quad x^*[-n],\]</div><p>因此 \(\operatorname{Re}\{X(e^{j\omega})\}\) 对应的序列为</p><div class="formula">\[x_{\mathrm{cs}}[n]=\frac{1}{2}\left(x[n]+x^*[-n]\right).\]</div><p>故填：<strong>\(\frac{1}{2}\left(x[n]+x^*[-n]\right)\)</strong>，即 \(x[n]\) 的共轭对称分量。</p></section>'''

def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>''',encoding="utf-8")
    return output

def rendered_dom(html: Path) -> str:
    profile=html.parent/"edge-profile"
    return subprocess.run([str(EDGE),"--headless=new","--disable-gpu",f"--user-data-dir={profile}","--virtual-time-budget=10000","--dump-dom",html.resolve().as_uri()],check=True,capture_output=True,text=True,encoding="utf-8",errors="replace").stdout
