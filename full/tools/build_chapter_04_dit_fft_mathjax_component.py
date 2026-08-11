"""Chapter-four 4.2 radix-2 decimation-in-time FFT material."""
from __future__ import annotations

from pathlib import Path

from full.tools.normalize_mathjax_inline import normalize_legacy_inline_math
from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt}.table th,.table td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:center}.table th{color:#315d7c;font-weight:500;background:#f4f7f8}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.table{font-size:9.5pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>4.2 基于时间抽取的基-2-FFT 快速算法</h1>
<p>基-2 时间抽取 FFT（DIT-FFT）要求变换长度为 (N=2^M)，其中 (M) 为正整数。若原记录长度不满足这一条件，可在序列末尾补零到合适的 (2^M) 点。所谓“时间抽取”是按时间下标的奇偶性不断拆分输入序列，而频域输出最终保持自然顺序。</p>

<h2>奇偶分解与一次蝶形</h2>
<p>令偶序号和奇序号样本分别构成两个 (N/2) 点序列：</p>
<div class="formula">\[
x_1(r)=x(2r),\qquad x_2(r)=x(2r+1),\qquad 0\leq r\leq\frac{N}{2}-1.
\]</div>
<p>设它们的 (N/2) 点 DFT 分别为 (X_1(k))、(X_2(k))。将 (N) 点 DFT 的求和按偶数项与奇数项分开，可得：</p>
<div class="formula">\[
\begin{aligned}
X(k)&=X_1(k)+W_N^kX_2(k),\\
X\left(k+\frac{N}{2}\right)&=X_1(k)-W_N^kX_2(k),
\qquad 0\leq k\leq\frac{N}{2}-1.
\end{aligned}
\]</div>
<p>这对“加、减”输出构成一个标准蝶形。每个蝶形包含一次旋转因子乘法和两次复数加法；其中 (W_N^k=e^{-j2\pi k/N}) 称为旋转因子。</p>

<h2>递归分解与运算量</h2>
<p>一次分解把一个 (N) 点 DFT 化为两个 (N/2) 点 DFT 和 (N/2) 个蝶形。继续对每个子序列按奇偶下标分解，直至得到 2 点 DFT。对于 (N=8=2^3)，共有 3 级，每一级有 (N/2=4) 个蝶形，总复数乘法数为：</p>
<div class="formula">\[
\frac{N}{2}\log_2N.
\]</div>
<p>因此 8 点基-2 DIT-FFT 需要 (4\times3=12) 次复数乘法，而直接计算需要 (8^2=64) 次复数乘法。一般地，FFT 将主导运算量从 (N^2) 降到 (N\log_2N) 数量级。</p>

<h2>例题：512 点 DFT 的计算时间</h2>
<p>设通用计算机平均每次复数乘法需要 (5\,\mu\mathrm{s})，每次复数加法需要 (0.5\,\mu\mathrm{s})。对 (N=512) 点序列：</p>
<div class="formula">\[
\begin{aligned}
T_{\mathrm{DFT}}
&=512^2\times5\times10^{-6}+512\times511\times0.5\times10^{-6}\\
&=1.441536\,\mathrm{s},\\
T_{\mathrm{FFT}}
&=\frac{512}{2}\log_2(512)\times5\times10^{-6}
+512\log_2(512)\times0.5\times10^{-6}\\
&=0.013824\,\mathrm{s}.
\end{aligned}
\]</div>
<p>这说明 FFT 的优势来自算法结构，而不是只靠机器速度提升。</p>

<h2>用 FFT 求线性卷积的规模判断</h2>
<p>当两个有限长序列的线性卷积采用频域方法时，须先补零到 (L\geq N_1+N_2-1)，再作两次 FFT、逐点相乘和一次 IFFT。课件的比较表明：长度 240 的序列与长度 10 的序列卷积时，直接法需 (2400) 次乘法，而补零到 (L=256) 的 FFT 法约需 (3328) 次乘法，直接法更合适；当两个序列都为 240 点时，直接法需 (57600) 次乘法，补零到 (L=512) 的 FFT 法约需 (7424) 次乘法，FFT 法更合适。</p>
<p>因此 FFT 并非在所有短序列情形都优于直接卷积；应先比较序列长度与补零后的变换规模。</p>

<h2>原位计算、旋转因子与码位倒序</h2>
<p>每一级蝶形都由同一批 (N) 个复数数据两两运算得到新的 (N) 个数据，因此中间结果可写回同一数组，称为原位计算（同址计算）。第 (L) 级共有 (N/2) 个蝶形，并出现 (2^{L-1}) 类旋转因子；旋转因子按 (W_N^{J2^{M-L}}) 的规律重复，(J=0,1,\ldots,2^{L-1}-1)。</p>
<h3>第 \(L\) 级原位蝶形运算</h3>
<p>令两输入数据的间距为 \(B=2^{L-1}\)。对 \(N=2^M\) 的基-2 DIT-FFT，第 \(L\) 级使用的旋转因子指数为 \(p=J\cdot2^{M-L}\)，从而：</p>
<div class="formula">\[
W_N^p=W_N^{J2^{M-L}},
\qquad J=0,1,\ldots,2^{L-1}-1.
\]</div>
<div class="formula">\[
\begin{aligned}
A_L(J)&=A_{L-1}(J)+A_{L-1}(J+B)W_N^p,\\
A_L(J+B)&=A_{L-1}(J)-A_{L-1}(J+B)W_N^p,\\
B&=2^{L-1},\qquad L=1,2,\ldots,M.
\end{aligned}
\]</div>
<p>这里 \(A_L(J)\) 表示第 \(L\) 级运算后数组第 \(J\) 个元素的值。两式必须先使用第 \(L-1\) 级的两个输入值，再同时写回对应位置，才能保持原位计算的蝶形含义。</p>
<p>对 (N=8) 的 DIT 原位实现，输入的自然序号应按二进制码位倒序重排为：</p>
<table class="table"><thead><tr><th>自然序号 (n)</th><th>二进制</th><th>码位倒序</th><th>倒序位置 (n')</th></tr></thead><tbody>
<tr><td>0</td><td>000</td><td>000</td><td>0</td></tr><tr><td>1</td><td>001</td><td>100</td><td>4</td></tr><tr><td>2</td><td>010</td><td>010</td><td>2</td></tr><tr><td>3</td><td>011</td><td>110</td><td>6</td></tr><tr><td>4</td><td>100</td><td>001</td><td>1</td></tr><tr><td>5</td><td>101</td><td>101</td><td>5</td></tr><tr><td>6</td><td>110</td><td>011</td><td>3</td></tr><tr><td>7</td><td>111</td><td>111</td><td>7</td></tr>
</tbody></table>
<p>故输入存储顺序为 (x(0),x(4),x(2),x(6),x(1),x(5),x(3),x(7))，完成各级蝶形后输出 (X(0),\ldots,X(7)) 为自然顺序。这一规则必须与“时间抽取”对应：DIT 是输入倒序、输出正序。</p>
</main>
"""
    content = normalize_legacy_inline_math(content)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
