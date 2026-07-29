"""Causality and stability material rendered with MathJax."""
from __future__ import annotations
import subprocess
from pathlib import Path
from full.tools.render_mathjax_formula import EDGE, MATHJAX
ROOT=Path(__file__).resolve().parents[2]
def write_html(output: Path)->Path:
 output.parent.mkdir(parents=True,exist_ok=True)
 c=r"""<main class="chapter"><header><h1>因果性与稳定性</h1></header>
<section class="causal-intro"><h2>一般系统的因果性</h2><p>若 \(y(n_0)\) 只依赖于 \(n\leq n_0\) 的输入 \(x(n)\)，系统因果；若依赖未来输入则非因果。</p><div class="formula">\[y(n_0)\Longleftarrow x(n),\qquad n\leq n_0\]</div><p>例：\(y(n)=nx(n)\) 因果；\(y(n)=x(n+2)\)、\(y(n)=x(n^2)\) 和 \(y(n)=x(-n)\) 非因果；\(y(n)=\sin(n+2)x(n)\) 因果。</p></section>
<section><h2>LSI 系统的因果条件</h2><div class="formula">\[h(n)=0\quad(n<0)\]</div><p>\(h(n)=\delta(n-2)+\delta(n+2)\) 非因果；\(0.5^n u(n-2)\) 因果；\(2^n u(-n-1)\) 与 \(0.5^n\) 非因果。</p></section>
<section><h2>一般系统的稳定性</h2><div class="formula">\[|x(n)|\leq M<\infty\Longrightarrow |y(n)|\leq P<\infty\]</div><p>\(y(n)=nx(n)\) 不稳定；\(y(n)=x(n^2)\) 稳定；\(\frac13\sum_{k=n-1}^{n+1}x(k)\) 稳定；\(\sum_{k=n_0}^{n}x(k)\) 不稳定。因果性和稳定性彼此独立。</p>
<h2>LSI 系统的稳定性条件</h2><div class="formula">\[\sum_{n=-\infty}^{\infty}|h(n)|=q<\infty\]</div><div class="formula">\[|y(n)|\leq\sum_{m=-\infty}^{\infty}|h(m)|\,|x(n-m)|\leq Mq\]</div><p>上述四个单位脉冲响应中，前 3 个绝对可和而稳定；\(h(n)=0.5^n\) 在双边索引上不绝对可和，故不稳定。</p></section></main>"""
 t=r"""<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={tex:{packages:{'[+]':['ams']}}};</script><script defer src="__MATHJAX__"></script><style>@page{size:A4;margin:18mm 18mm 20mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933}.chapter{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.causal-intro{break-after:page}</style>__CONTENT__</html>"""
 output.write_text(t.replace("__MATHJAX__",MATHJAX).replace("__CONTENT__",c),encoding="utf-8"); return output
def render_pdf(output:Path)->Path:
 html=write_html(output.with_suffix(".html")); subprocess.run([str(EDGE),"--headless=new","--disable-gpu","--no-pdf-header-footer","--virtual-time-budget=10000",f"--print-to-pdf={output.resolve()}",html.resolve().as_uri()],check=True); return output
if __name__=="__main__": print(render_pdf(ROOT/"full"/"outputs"/"chapter_01_causal_stable_mathjax_component.pdf"))
