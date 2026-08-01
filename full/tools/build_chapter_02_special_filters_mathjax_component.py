"""Core special-filter design theory, rendered only by MathJax."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:20mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r'''
<main>
<h1>特殊滤波器的设计</h1>
<p>本节只保留数字信号处理与考研复习所需的设计思想、数学结构和判读原则。所有设计都从同一规则出发：要抑制某个频率，就在单位圆对应位置布置零点；要增强某个频率，就在同方向、单位圆内靠近该位置布置极点。</p>
<h2>简单一阶低通与高通</h2>
<p>在 [[\omega=\pi]] 处放零点可抑制最高离散频率，得到最简单的低通平滑器：</p>
<div class="formula">\[H(z)=\frac{z+1}{2z}=\frac{1}{2}(1+z^{-1}),\qquad y(n)=\frac{1}{2}[x(n)+x(n-1)]\]</div>
<p>在 [[\omega=0]] 处放零点可抑制直流和缓慢变化部分，得到最简单的高通器：</p>
<div class="formula">\[H(z)=\frac{z-1}{2z}=\frac{1}{2}(1-z^{-1}),\qquad y(n)=\frac{1}{2}[x(n)-x(n-1)]\]</div>
<p>另一类低通设计是在 [[z=a]]、[[0&lt;a&lt;1]] 处放一个靠近 [[z=1]] 的极点；极点越接近单位圆，低频增强越明显，但必须严格留在单位圆内以保证稳定：</p>
<div class="formula">\[H(z)=\frac{1-a}{z-a},\qquad 0&lt;a&lt;1\]</div>
<h2>数字陷波器</h2>
<p>陷波器用于消除特定窄带干扰。若要抑制数字频率 [[\omega_0]]，必须在单位圆上成对放置共轭零点，才能保证实系数：</p>
<div class="formula">\[z=e^{\pm j\omega_0},\qquad \omega_0=2\pi\frac{f_0}{f_s}\]</div>
<p>一个二阶陷波器可写为：</p>
<div class="formula">\[H(z)=K\frac{(z-e^{j\omega_0})(z-e^{-j\omega_0})}{z^2}\]</div>
<p>频率、采样率与 DFT 索引的换算必须统一使用：</p>
<div class="formula">\[\frac{k}{N}=\frac{\omega}{2\pi}=\frac{f}{f_s}=\frac{\Omega}{\Omega_s}\]</div>
<h2>全通滤波器</h2>
<p>全通滤波器的幅度在整个频带内恒为一；它不改变幅度，只校正相位或群延迟：</p>
<div class="formula">\[\left|H_{\mathrm{ap}}(e^{j\omega})\right|=1,\qquad 0\leq\omega&lt;2\pi\]</div>
<p>若 [[D(z)]] 的极点都在单位圆内，则实系数稳定全通滤波器可表示为：</p>
<div class="formula">\[H_{\mathrm{ap}}(z)=A\frac{z^{-N}D(z^{-1})}{D(z)}=A\prod_{i=1}^{N}\frac{z^{-1}-p_i^*}{1-p_i z^{-1}}\]</div>
<p>其零极点具有共轭倒易关系：每个极点 [[p_i]] 对应零点 [[1/p_i^*]]。稳定实系数全通滤波器在 [[0,\pi]] 内相位单调减小，群延迟为正。</p>
<h2>最小相位滤波器</h2>
<p>若一个因果稳定系统及其逆系统都要求因果稳定，则原系统的全部零点和极点都必须位于单位圆内。这类系统称为最小相位系统。</p>
<p>任何适当的因果稳定系统可分解为最小相位部分和全通部分：</p>
<div class="formula">\[H(z)=H_{\min}(z)H_{\mathrm{ap}}(z)\]</div>
<p>相位与群延迟满足可加关系：</p>
<div class="formula">\[\arg H(e^{j\omega})=\arg H_{\min}(e^{j\omega})+\arg H_{\mathrm{ap}}(e^{j\omega})\]</div>
<div class="formula">\[\operatorname{grd}\{H(e^{j\omega})\}=\operatorname{grd}\{H_{\min}(e^{j\omega})\}+\operatorname{grd}\{H_{\mathrm{ap}}(e^{j\omega})\}\]</div>
<p>全通部分只额外引入相位滞后和正群延迟，因此最小相位部分具有最小相位滞后、最小群延迟和最小能量延迟。分解时，将单位圆内的零极点归入 [[H_{\min}(z)]]，单位圆外的零点通过共轭倒易配对组成 [[H_{\mathrm{ap}}(z)]]。</p>
<h2>本节检查顺序</h2>
<p>先把目标频率换成数字频率，再按“零点抑制、极点增强”的规则确定位置；随后检查共轭对称以保证实系数、检查全部极点位于单位圆内以保证稳定；最后根据是否保幅判断是否属于全通，并根据零极点位置判断是否最小相位。</p>
</main>'''.replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    document = f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'
    output.write_text(document, encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_02_special_filters_mathjax_component.pdf"))
