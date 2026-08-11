"""Chapter-seven FIR design body, excluding source-code demonstrations."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt;orphans:3;widows:3}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt}.table th,.table td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:left;vertical-align:top}.table th{color:#315d7c;font-weight:500;background:#f4f7f8}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.table{font-size:9.5pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>第七章 FIR 数字滤波器设计</h1>
<h2>7.1 线性相位 FIR 数字滤波器的条件和特点</h2>
<p>FIR 滤波器可严格实现线性相位。若长度为 [[N]] 的实序列冲激响应满足关于 [[(N-1)/2]] 的偶对称或奇对称，则相位可写成线性项加常数，群延迟为常数。其充要对称条件为：</p>
<div class="formula">\[
h(n)=\pm h(N-1-n),\qquad 0\leq n\leq N-1.
\]</div>
<p>偶对称属于第一类线性相位，奇对称属于第二类线性相位。长度奇偶与对称类型共同决定 [[H(0)]]、[[H(\pi)]] 是否必为零，进而决定能否实现低通、高通、带通或带阻。实系数线性相位 FIR 的零点同时满足共轭成对与关于单位圆镜像对称；全部极点位于原点，系统稳定。</p>
<div class="formula">\[
H(z)=\sum_{n=0}^{N-1}h(n)z^{-n},
\qquad
z_i\text{ 为零点 }\Longrightarrow z_i^*,\ \frac{1}{z_i},\ \frac{1}{z_i^*}\text{ 也按重数出现。}
\]</div>

<h2>7.2 利用窗函数法设计 FIR 滤波器</h2>
<p>窗函数法先由理想频响 [[H_d(e^{j\omega})]] 作 IDTFT 得到通常无限长的 [[h_d(n)]]，再用有限长度窗截断为可实现序列：</p>
<div class="formula">\[
h(n)=h_d(n)w(n).
\]</div>
<p>时域相乘对应频域卷积，因此加窗会形成过渡带并产生振荡起伏。增加 [[N]] 会缩窄主瓣、减小过渡带宽，但同一窗形的主旁瓣能量比例并不因此改变；选窗则主要控制阻带衰减。矩形、三角、汉宁、海明和布莱克曼窗的典型阻带衰减依次增强，而对应过渡带通常变宽。</p>
<p>设计步骤是：由通/阻带边界取理想截止频率；写出 [[h_d(n)]]；按阻带衰减选择窗型；由过渡带宽确定 [[N]]；计算 [[h(n)]] 并复核频响。线性相位高通与带阻设计通常要求 [[N]] 为奇数，避免结构固有的端点零值与指标冲突。</p>

<h2>7.3 利用频率采样法设计 FIR 滤波器</h2>
<p>频率采样法在等间隔频点指定目标频响样值 [[H(k)]]，再用 IDFT 唯一确定有限长冲激响应：</p>
<div class="formula">\[
h(n)=\frac{1}{N}\sum_{k=0}^{N-1}H(k)W_N^{-nk},
\qquad
H(k)=H\!\left(e^{j2\pi k/N}\right).
\]</div>
<p>若要求线性相位，[[H(k)]] 的幅度和相位必须满足与偶/奇对称、长度奇偶一致的约束。低通示例中，[[N=33]] 为奇数时应选第一类线性相位；第二类奇对称会强制 [[H(0)=H(\pi)=0]]，不适合一般低通。</p>
<p>频率采样点之间由内插关系连接。理想频响变化越陡，不连续点附近的肩峰和起伏越明显；增加采样点或在过渡带安排非零的过渡采样值可显著改善阻带衰减。设计时不可只让通带、阻带采样点“对上”，还应检查采样点之间的真实频响。</p>

<h2>7.4 利用等波纹逼近法设计 FIR 滤波器</h2>
<p>等波纹最佳逼近采用加权切比雪夫准则：在给定长度与线性相位约束下，使逼近区域内加权误差的最大值最小，并让极大误差近似均匀分布。设 [[H_d(\omega)]] 为理想广义幅度、[[H_g(\omega)]] 为设计结果，则：</p>
<div class="formula">\[
E(\omega)=W(\omega)\left[H_d(\omega)-H_g(\omega)\right],
\qquad
\min\max_{\omega\in\mathcal{B}}\left|E(\omega)\right|.
\]</div>
<p>加权函数 [[W(\omega)]] 越大，对应频段的逼近精度越高。通带和阻带是逼近区域，过渡带是不要求精确逼近的无关区域；无关区宽度不能为零。Remez 多重交换迭代通过交替更新极值频点求取 [[h(n)]]，能分别控制通带与阻带波纹，常比窗函数法和基本频率采样法以更短长度达到同一指标。</p>
<table class="table"><thead><tr><th>方法</th><th>直接控制量</th><th>主要特征</th></tr></thead><tbody><tr><td>窗函数法</td><td>窗型与长度</td><td>过程直观；过渡带与旁瓣受窗函数制约。</td></tr><tr><td>频率采样法</td><td>离散频响样值</td><td>便于指定关键频点；需处理采样点间插误差。</td></tr><tr><td>等波纹逼近</td><td>误差权重与长度</td><td>在给定长度下最大加权误差最小；通、阻带可独立加权。</td></tr></tbody></table>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
