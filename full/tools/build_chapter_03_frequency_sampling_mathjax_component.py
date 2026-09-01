"""Chapter-three §3.4 frequency-domain sampling theorem."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}</style>"""


def frequency_sampling_duality_svg() -> str:
    """Draw the frequency-sampling/periodic-extension correspondence."""
    return '''<figure data-diagram="frequency-sampling-duality" style="break-inside:avoid;margin:12pt 0 13pt">
<svg viewBox="0 0 980 260" role="img" aria-labelledby="frequency-sampling-duality-title" style="display:block;width:100%;height:auto;border:1px solid #d6dde2;border-radius:5pt;background:#fff">
<title id="frequency-sampling-duality-title">频域采样与时域周期延拓的对应关系</title>
<defs><marker id="frequency-sampling-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#174b73"/></marker></defs>
<text x="46" y="37" fill="#174b73" font-family="Microsoft YaHei, sans-serif" font-size="18" font-weight="700">频域等间隔采样与时域周期延拓</text>
<rect x="82" y="76" width="185" height="62" rx="6" fill="#f4f7f8" stroke="#0d8794" stroke-width="1.5"/><rect x="704" y="76" width="190" height="62" rx="6" fill="#fff8e8" stroke="#b56b2e" stroke-width="1.5"/><rect x="704" y="175" width="190" height="62" rx="6" fill="#eef7f1" stroke="#16866d" stroke-width="1.5"/>
<foreignObject x="94" y="88" width="160" height="35"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:16px;text-align:center">\\(x(n)\\)</div></foreignObject><foreignObject x="712" y="88" width="174" height="35"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:15px;text-align:center">\\(X(k)\\)</div></foreignObject><foreignObject x="712" y="186" width="174" height="35"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:14px;text-align:center">\\(\\widetilde{x}(n)=\\sum_r x(n-rN)\\)</div></foreignObject>
<line x1="267" y1="107" x2="704" y2="107" stroke="#174b73" stroke-width="2" marker-end="url(#frequency-sampling-arrow)"/><line x1="799" y1="138" x2="799" y2="175" stroke="#174b73" stroke-width="2" marker-end="url(#frequency-sampling-arrow)"/>
<text x="367" y="93" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="15">DTFT 后在单位圆取 N 个等间隔样点</text><text x="818" y="161" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">N 点 IDFT</text><text x="82" y="170" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="15">N≥M：副本不重叠，可恢复有限长序列。</text><text x="82" y="205" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="15">N&lt;M：相隔 N 的样本相加，产生时域混叠。</text>
</svg><figcaption style="margin-top:4pt;color:#52616d;text-align:center;font-size:9.5pt">图 3-7　频域采样与时域周期延拓的对应关系。</figcaption></figure>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>3.4 频域采样定理</h1>
<p>频域采样研究的问题是：对非周期序列的 DTFT 在单位圆上取 [[N]] 个等间隔样点后，能恢复什么样的时域序列？它与时域采样形成严格对偶：时域离散会使频域周期延拓，频域离散则使时域周期延拓。</p>
""" + frequency_sampling_duality_svg() + r"""

<h2>频域等间隔采样</h2>
<p>设 [[x(n)]] 为绝对可和的非周期序列，故其 DTFT 连续，z 变换的收敛域包含单位圆。频域抽样值定义如下；它说明 DFT 样值就是 [[z]] 变换在单位圆根上的取值。后文为简洁起见仍将 [[\widetilde{X}(k)]] 记作 [[X(k)]]：</p>
<div class="formula">\[
\widetilde{X}(k)=\left.X(z)\right|_{z=W_N^{-k}}
=\sum_{n=-\infty}^{\infty}x(n)W_N^{nk}
=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{N}},
\qquad k=0,1,\ldots,N-1.
\]</div>
<p>等价的频率坐标写法为：</p>
<div class="formula">\[
X(k)=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{N}},
\qquad k=0,1,\ldots,N-1.
\]</div>
<p>根单位正交关系用于化简 IDFT 中的双重求和，并决定哪些时域样本会折叠到同一个位置：</p>
<div class="formula">\[
\frac{1}{N}\sum_{k=0}^{N-1}W_N^{(m-n)k}
=
\begin{cases}
1, & m=n+rN,\\
0, & \text{其他 }m,
\end{cases}
\qquad r\in\mathbb{Z}.
\]</div>
<p>对这些频域样值作 [[N]] 点 IDFT，得到：</p>
<div class="formula">\[
\begin{aligned}
\widetilde{x}(n)
&=\frac{1}{N}\sum_{k=0}^{N-1}X(k)W_N^{-nk}\\
&=\sum_{r=-\infty}^{\infty}x(n-rN).
\end{aligned}
\]</div>
<p>因此，IDFT 的结果 [[\widetilde{x}(n)]] 不是一般意义上的原非周期序列，而是原序列以 [[N]] 为周期的相加延拓。若同一主值位置叠加了多个原始样本，就发生时域混叠。</p>

<h2>频域采样定理</h2>
<p>若 [[x(n)]] 是长度为 [[M]] 的有限长序列，且主值区间为 [[0\leq n\leq M-1]]，则只要频域采样点数满足：</p>
<div class="formula">\[
N\geq M,
\]</div>
<p>周期延拓的各个副本便不会在一个周期内重叠，此时可由 [[X(k)]] 无失真地恢复 [[x(n)]]。反之 [[N&lt;M]] 时，时域副本相加，无法从 IDFT 结果中分离原样本。</p>
<div class="formula">\[
\widetilde{x}(n)=x(n),\quad 0\leq n\leq M-1,\qquad N\geq M.
\]</div>

<h2>由频域样值恢复 z 变换与 DTFT</h2>
<p>恢复的第一步是 IDFT 得到有限长序列的 [[M]] 个样值；随后按 z 变换定义形成多项式：</p>
<div class="formula">\[
X(z)=\sum_{n=0}^{M-1}x(n)z^{-n}.
\]</div>
<p>由单位圆上等间隔的 [[N]] 个频率样值还可直接写出插值恢复式：</p>
<div class="formula">\[
X(z)=\frac{1-z^{-N}}{N}
\sum_{k=0}^{N-1}\frac{X(k)}{1-W_N^{-k}z^{-1}}
=\sum_{k=0}^{N-1}X(k)\Phi_k(z),
\qquad
\Phi_k(z)=\frac{1}{N}\frac{1-z^{-N}}{1-W_N^{-k}z^{-1}}.
\]</div>
<p>每个插值函数在单位圆的 [[N]] 个等间隔频率位置具有选择性；因此，当 [[N\geq M]] 时，频率样值可唯一确定有限长序列的 [[z]] 变换。</p>
<p>令 [[z=e^{j\omega}]]，便得到整个连续频率轴上的 DTFT：</p>
<div class="formula">\[
X\left(e^{j\omega}\right)=\sum_{n=0}^{M-1}x(n)e^{-j\omega n}.
\]</div>
<p>这说明频域采样点并非只用于画离散谱线；在无混叠条件满足时，它们足以恢复原有限长序列，进而恢复连续的 DTFT 曲线。</p>

<h2>判定步骤</h2>
<ol class="steps">
<li>确定原序列的有效长度 [[M]] 与起止位置。</li>
<li>确认频域等间隔采样点数 [[N]]。</li>
<li>比较 [[N]] 与 [[M]]：[[N\geq M]] 时可无混叠恢复；[[N&lt;M]] 时写出按 [[N]] 周期折回的相加关系。</li>
<li>需要连续频谱时，先 IDFT 恢复时域样值，再由 z 变换或 DTFT 定义计算。</li>
</ol>

<h2>例题：频域抽样的时域结果</h2>
<p>若一个有限长序列的有效长度为 [[M=6]]，在单位圆上取 [[N=4]] 个等间隔频率样值并作 4 点 IDFT，则恢复序列为 [[\widetilde{x}(n)=\sum_r x(n-4r)]]。其中原序列相隔 4 的样本将叠加，因此不能无失真恢复。若改取 [[N=6]] 或更多频率样点，便满足 [[N\geq M]]，可以恢复原序列。</p>
</main>
"""
    content = content.replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    html = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(html, encoding="utf-8")
    return output
