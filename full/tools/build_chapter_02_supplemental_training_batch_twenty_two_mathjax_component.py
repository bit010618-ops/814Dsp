"""2013 bilateral z-transform question."""
from __future__ import annotations
import subprocess
from pathlib import Path
from full.tools.render_mathjax_formula import EDGE, MATHJAX
STYLE=r"""<style>@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;color:#52616b;margin:0 0 10pt}</style>"""
def training_html(): return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2013 年真题</span><span>详解见 P.____</span></div><p>二、计算题</p><p>5.已知 \(x[n]=\left(\frac{1}{3}\right)^n u[n]+\left(\frac{1}{2}\right)^n u[-n-1]\)，求 \(x[n]\) 的 \(z\) 变换 \(X(z)\)。</p></section>'''
def answers_html(): return r'''<section><h1>真题整理详解（续）</h1><h2>2013 年真题：双边序列的 \(z\) 变换</h2><p>右边序列与左边序列必须分别确定 ROC：</p><div class="formula">\[\begin{aligned}\left(\frac{1}{3}\right)^nu[n]&\Longleftrightarrow\frac{1}{1-\frac{1}{3}z^{-1}},\quad\left|z\right|>\frac{1}{3},\\\left(\frac{1}{2}\right)^nu[-n-1]&\Longleftrightarrow-\frac{1}{1-\frac{1}{2}z^{-1}},\quad\left|z\right|<\frac{1}{2}.\end{aligned}\]</div><p>故</p><div class="formula">\[X(z)=\frac{1}{1-\frac{1}{3}z^{-1}}-\frac{1}{1-\frac{1}{2}z^{-1}},\qquad\frac{1}{3}<\left|z\right|<\frac{1}{2}.\]</div><p>最终 ROC 是两个分量 ROC 的交集；缺少 ROC 时，双边序列的 \(z\) 变换不完整。</p></section>'''
def write_html(output:Path)->Path:
 output.parent.mkdir(parents=True,exist_ok=True);output.write_text(f'''<!doctype html><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main>''',encoding="utf-8");return output
def rendered_dom(html:Path)->str:
 return subprocess.run([str(EDGE),"--headless=new","--disable-gpu","--virtual-time-budget=10000","--dump-dom",html.resolve().as_uri()],check=True,capture_output=True,text=True,encoding="utf-8").stdout
