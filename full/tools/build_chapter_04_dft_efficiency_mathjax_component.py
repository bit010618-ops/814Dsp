"""Chapter-four 4.1 direct DFT cost and FFT motivation."""
from __future__ import annotations

from pathlib import Path

from full.tools.normalize_mathjax_inline import normalize_legacy_inline_math
from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.counts{border-collapse:collapse;width:100%;margin:10pt 0 12pt}.counts th,.counts td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:center}.counts th{color:#315d7c;font-weight:500;background:#f4f7f8}.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.counts{font-size:9.5pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>4.1 直接计算 DFT 的问题及改进途径</h1>
<p>DFT 将有限长序列直接映射为有限个频域样值，但直接按定义求和时，计算量随点数的平方增长。对长记录或实时处理，运算时间与内存需求会迅速成为限制，因此需要研究利用 DFT 系数结构的快速算法。</p>

<h2>直接计算的运算量</h2>
<p>对 (N) 点序列，DFT 与 IDFT 的求和结构相同，计算量同数量级。以 DFT 为例：</p>
<div class="formula">\[
X(k)=\sum_{n=0}^{N-1}x(n)W_N^{nk},\qquad k=0,1,\ldots,N-1.
\]</div>
<p>计算一个 (X(k)) 需要 (N) 次复数乘法和 (N-1) 次复数加法；计算全部 (N) 个频点则得到：</p>
<table class="counts"><thead><tr><th>对象</th><th>复数乘法</th><th>复数加法</th></tr></thead><tbody>
<tr><td>一个 (X(k))</td><td>(N)</td><td>(N-1)</td></tr>
<tr><td>(N) 点 DFT</td><td>(N^2)</td><td>(N(N-1))</td></tr>
</tbody></table>
<p>若把一次复数乘法按 4 次实数乘法和 2 次实数加法计算，一次复数加法按 2 次实数加法计算，则直接 DFT 约需 (4N^2) 次实数乘法与 (4N^2-2N) 次实数加法。这里的关键结论是：直接算法的主导复杂度为 (N^2)。</p>

<h2>规模为何会成为问题</h2>
<p>课件中的音频频谱分析例使用 \(f_s=11025\,\mathrm{Hz}\)、\(N=13095\) 点。仅复数乘法次数即为：</p>
<div class="formula">\[
N^2=13095^2=171479025.
\]</div>
<p>若每次复数乘法仅需 \(1\,\mu\mathrm{s}\)，也需要约 \(171.479025\,\mathrm{s}\)，接近 3 分钟。实际系统还要计入复数加法、数据搬运和显示，因此直接 DFT 很难满足实时频谱分析的要求。</p>

<h2>改善运算效率的基本途径</h2>
<ol class="steps">
<li>利用旋转因子 (W_N^{nk}) 的周期性、对称性和重复性，合并重复的乘法项。</li>
<li>把一个长点数 DFT 分解为若干短点数 DFT，再按规则组合；由于平方量级的长变换被拆分，主导运算量可以显著降低。</li>
</ol>
<h3>旋转因子的可复用结构</h3>
<div class="formula">\[
\left(W_N^{nk}\right)^*=W_N^{-nk}=W_N^{(N-n)k}=W_N^{n(N-k)}.
\]</div>
<div class="formula">\[
W_N^{nk}=W_N^{(N+n)k}=W_N^{n(N+k)},\qquad
W_N^{nk}=W_{mN}^{mnk}=W_{N/m}^{nk/m}.
\]</div>
<div class="formula">\[
W_N^0=W_N^N=1,\qquad W_N^{N/2}=-1,\qquad W_N^{k+N/2}=-W_N^k.
\]</div>
<p>快速傅里叶变换（FFT）正是以上思路的系统实现。Cooley 与 Tukey 在 1965 年提出的快速算法使 DFT 运算速度得到数量级提升。后续将讨论两类基 2 结构：时间抽取法 DIT（Decimation-In-Time）与频率抽取法 DIF（Decimation-In-Frequency）。</p>
</main>
"""
    content = normalize_legacy_inline_math(content)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
