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
<h2>数字谐振器</h2>
<p>数字谐振器把输入频谱中靠近某一固有频率的成分显著增强。二阶实系数谐振器通常在单位圆内、角度为 [[\pm\omega_0]] 的位置配置一对共轭极点：</p>
<div class="formula">\[p_{1,2}=re^{\pm j\omega_0},\qquad 0&lt;r&lt;1\]</div>
<p>极点角度决定通带中心频率 [[\omega_0]]；半径 [[r]] 决定选择性。[[r]] 越接近 1，极点越接近单位圆，谐振峰越尖、带宽越窄。若同时要求在直流与最高频率处完全抑制，可在 [[z=1]]、[[z=-1]] 处配置零点，得到一类二阶带通结构：</p>
<div class="formula">\[H(z)=G\frac{1-z^{-2}}{1-2r\cos\omega_0\,z^{-1}+r^2z^{-2}}\]</div>
<p>其中 [[G]] 用中心频率处的目标幅度确定；[[r]] 则由给定带宽或指定频率处的幅度条件确定。设计后必须检查极点半径小于 1，才能保证因果稳定。</p>
<h2>DTMF 双音多频信号</h2>
<p>电话按键的 DTMF 信号由一个低频组频率与一个高频组频率叠加而成。低频组为 697、770、852、941 Hz，高频组为 1209、1336、1477、1633 Hz。每个按键对应唯一的一对频率；例如按键 8 对应 852 Hz 和 1336 Hz。</p>
<div class="formula">\[x(n)=A_1\cos(\omega_1n+\varphi_1)+A_2\cos(\omega_2n+\varphi_2),\qquad \omega_i=2\pi\frac{f_i}{f_s}\]</div>
<p>生成某个按键信号时，可分别用两个中心频率对应的数字谐振器选择所需频率，再将两路输出相加。判读题目时先由采样频率换算数字频率，再确认两个通带中心分别落在对应低频组和高频组频率上。</p>
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
<h2>工程中常用的滤波方法</h2>
<p>下列方法用于离散采样数据的预处理，重点在于理解适用的干扰类型与参数选择，而非程序实现。</p>
<h3>限幅滤波</h3>
<p>设 [[E]] 为两次采样允许的最大偏差。若新样值与上一次有效输出相差过大，则以旧输出代替新样值，因而可抑制偶发脉冲干扰：</p>
<div class="formula">\[y(n)=\begin{cases}x(n),&\left|x(n)-y(n-1)\right|\le E,\\y(n-1),&\left|x(n)-y(n-1)\right|&gt;E.\end{cases}\]</div>
<p>阈值过小会误删信号的真实突变；阈值过大则难以去除干扰。</p>
<h3>中值滤波与滑动平均</h3>
<p>中值滤波把连续 [[N]] 个采样值排序后取中间值，对孤立异常点有效；滑动平均则取一个局部窗口内的算术平均，能平滑高频波动，但对脉冲干扰的抑制较弱：</p>
<div class="formula">\[y(n)=\operatorname{med}\left\{x(n-M),\ldots,x(n),\ldots,x(n+M)\right\}\]</div>
<div class="formula">\[y(n)=\frac{1}{M_1+M_2+1}\sum_{k=-M_1}^{M_2}x(n-k)\]</div>
<p>中值平均可先删除一个最大值和一个最小值，再对其余样值取均值；限幅平均可先作限幅，再作滑动平均。加权平均中离当前时刻越近的样值通常赋予更大的权重，灵敏度提高的同时平滑能力会下降。</p>
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
