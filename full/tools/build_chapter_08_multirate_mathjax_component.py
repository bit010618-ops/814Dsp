"""Chapter-eight multirate DSP body, excluding source-code exercises."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt;orphans:3;widows:3}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt}.table th,.table td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:left;vertical-align:top}.table th{color:#315d7c;font-weight:500;background:#f4f7f8}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.table{font-size:9.5pt}}</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>第八章 多采样率数字信号处理</h1>
<p>多采样率处理研究同一系统中不同采样率信号的表示、变换和实现。它用于降低传输或运算速率、实现窄带滤波器、完成子带分解与重构，以及连接采样率不同的处理模块。核心原则是：任何改变采样率的操作都要同时检查频谱压缩、镜像、混叠和抗混叠滤波。</p>

<h2>8.1 信号的整数倍抽取</h2>
<p>[[M]] 倍抽取使采样率降低为原来的 [[1/M]]，每隔 [[M]] 个样本取一个样本：</p>
<div class="formula">\[
y(n)=x(Mn),\qquad F_s'=\frac{F_s}{M}.
\]</div>
<p>时域抽取会使频谱在数字频率轴上压缩并叠加：</p>
<div class="formula">\[
Y\!\left(e^{j\omega}\right)=\frac{1}{M}
\sum_{r=0}^{M-1}X\!\left(e^{j(\omega-2\pi r)/M}\right).
\]</div>
<p>因此若原信号带宽未限制在 [[\pi/M]] 以内，抽取后会产生不可逆混叠。正确结构是先用抗混叠低通滤波器限制带宽，再接 [[\downarrow M]] 抽取器；不能把低通滤波器放在抽取之后当作补救。</p>

<h2>8.2 信号的整数倍内插</h2>
<p>[[L]] 倍内插使采样率提高 [[L]] 倍。第一步在相邻原样本间插入 [[L-1]] 个零：</p>
<div class="formula">\[
y(n)=\sum_{k=-\infty}^{\infty}x(k)\delta(n-kL),
\qquad F_s'=LF_s.
\]</div>
<p>零插入不会自动产生新的平滑样本，而是在频域形成镜像谱：</p>
<div class="formula">\[
Y\!\left(e^{j\omega}\right)=X\!\left(e^{j\omega L}\right).
\]</div>
<p>随后必须使用插值低通滤波器去除镜像，并补偿增益。理想插值器在 [[|\omega|\leq\pi/L]] 内增益为 [[L]]，其他频段为零；这样可保留原谱并获得较高采样率序列。</p>

<h2>8.3 抽取与内插的频域关系</h2>
<p>抽取前的低通滤波器防止谱副本叠加，内插后的低通滤波器去除零插入产生的镜像。二者都是低通滤波器，但所处位置、目的和增益要求不同：前者的截止频率受抽取倍数限制，后者的截止频率受内插倍数限制并需补偿 [[L]] 倍幅度。</p>
<table class="table"><thead><tr><th>操作</th><th>时域效果</th><th>频域风险与滤波目的</th></tr></thead><tbody><tr><td>抽取 [[\downarrow M]]</td><td>按间隔取样，长度/采样率下降</td><td>频谱压缩并叠加；先低通以防混叠。</td></tr><tr><td>内插 [[\uparrow L]]</td><td>插零，采样率上升</td><td>频谱压缩后周期镜像；后低通以消除镜像并补偿增益。</td></tr></tbody></table>

<h2>8.4 有理数倍采样率变换与多相结构</h2>
<p>以先 [[L]] 倍内插、再 [[M]] 倍抽取实现 [[L/M]] 倍采样率变换，输入输出采样率满足：</p>
<div class="formula">\[
F_s'=\frac{L}{M}F_s.
\]</div>
<p>为避免不必要的运算，可把低通滤波器拆成多相分量。对抽取因子 [[M]]，多相展开写为：</p>
<div class="formula">\[
H(z)=\sum_{r=0}^{M-1}z^{-r}E_r\!\left(z^M\right).
\]</div>
<p>多相结构把原来会在抽取后丢弃的中间运算移除，并允许滤波器和采样率变换器交换位置或合并。实现时仍需逐项核对：上采样/下采样倍数、滤波器位置、各相位支路和输出采样率必须一致；任何一处颠倒都会改变频谱并造成混叠或镜像残留。</p>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
