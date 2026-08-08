"""Eleventh verified batch of chapter-two supplemental examination questions."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}.indent{padding-left:1.7em;text-indent:-1.7em}
</style>"""


def training_html() -> str:
    return r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1><div class="exam-head"><span>2024 年真题</span><span>详解见 P.____</span></div><p>九、如果一个因果 LSI 系统的输入输出满足如下差分方程</p><div class="formula">\[y(n)=ay(n-1)+x(n)\]</div><p>系统的单位冲激响应为 \(h(n)=a^nu(n)\)。</p><p class="indent">（1）请问 \(a\) 取何值时，系统是稳定的？</p><p class="indent">（2）考虑一个因果 LSI 系统，其输入输出关系由如下差分方程描述：</p><div class="formula">\[y(n)=ay(n-1)+x(n)-a^Nx(n-N)\]</div><p class="indent">式中的 \(N\) 为正整数，请求出系统的单位冲激响应。</p><p class="indent">（3）请问(2)中的系统是 FIR 还是 IIR 系统？</p><p class="indent">（4）若(2)中的系统是稳定的，请问对 \(a\) 取何值是否有限制？</p></section>'''


def answers_html() -> str:
    return r'''<section><h1>真题整理详解（续）</h1><h2>2024 年真题：延时消零项与 FIR 判定</h2><h3>（1）一阶因果系统的稳定性</h3><p>已知 \(h[n]=a^nu[n]\)。BIBO 稳定要求单位脉冲响应绝对可和：</p><div class="formula">\[\sum_{n=-\infty}^{\infty}\left|h[n]\right|=\sum_{n=0}^{\infty}\left|a\right|^n<\infty\quad\Longleftrightarrow\quad\left|a\right|<1.\]</div><h3>（2）含延时消零项的单位脉冲响应</h3><p>在零初始条件下作 \(z\) 变换，先保留分子中的消零因子：</p><div class="formula">\[Y(z)=\left(az^{-1}Y(z)+X(z)-a^Nz^{-N}X(z)\right),\qquad H(z)=\frac{1-a^Nz^{-N}}{1-az^{-1}}.\]</div><p>将前半部分看作一阶因果系统，再用移位性质处理第二项：</p><div class="formula">\[\begin{aligned}h[n]&=a^nu[n]-a^N a^{n-N}u[n-N]\\&=a^n\left(u[n]-u[n-N]\right).\end{aligned}\]</div><p>因此 \(h[n]\) 仅在 \(0\le n\le N-1\) 时非零；它恰好截断了原来无限长的一阶指数响应。</p><h3>（3）FIR/IIR 判定</h3><p>利用有限几何级数还可把传递函数写成</p><div class="formula">\[H(z)=\frac{1-a^Nz^{-N}}{1-az^{-1}}=\sum_{k=0}^{N-1}a^kz^{-k}.\]</div><p>该和式只有 \(N\) 个抽头，故(2)中的系统是一个长度为 \(N\) 的 FIR 系统，而不是 IIR 系统。</p><h3>（4）稳定性对 \(a\) 的限制</h3><p>虽然中间表示式含有 \(1-az^{-1}\) 的分母，但它已被分子中的 \(1-a^Nz^{-N}\) 完全消去为有限长冲激响应。有限长序列一定绝对可和，因此对(2)中的系统，任意有限的 \(a\) 均稳定。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(text, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    profile = html.parent / "edge-profile"
    completed = subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return completed.stdout
