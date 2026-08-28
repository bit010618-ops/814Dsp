"""Chapter-four DIF FFT, IFFT, optimized FFT and CZT material."""
from __future__ import annotations

from pathlib import Path

from full.tools.normalize_mathjax_inline import normalize_legacy_inline_math
from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt}.table th,.table td{border-bottom:.4pt solid #d6dde2;padding:6pt 7pt;text-align:center}.table th{color:#315d7c;font-weight:500;background:#f4f7f8}.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.table{font-size:9.5pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>4.3 基于频率抽取的基-2-FFT 快速算法原理</h1>
<p>基-2 频率抽取 FFT（DIF-FFT）同样要求 (N=2^M)，但它不先按时间索引奇偶拆分输入，而是先把频域输出按偶、奇频率索引拆分。输入序列在前后两半之间作蝶形组合，再分别作 (N/2) 点 FFT。</p>
<p>将 (N) 点 DFT 的时域求和以前后半段配对，可定义：</p>
<div class="formula">\[
X(k)=\sum_{n=0}^{N/2-1}
\left[x(n)+(-1)^k x\left(n+\frac{N}{2}\right)\right]W_N^{kn},
\qquad 0\leq k\leq N-1.
\]</div>
<p>这里利用了 \(W_N^{kN/2}=e^{-j\pi k}=(-1)^k\)。因此当 \(k\) 为偶数或奇数时，括号内分别自然产生“和”或“差”，这正是 DIF 蝶形先相加／相减、再在差分支路乘旋转因子的来源。</p>
<div class="formula">\[
\begin{aligned}
x_1(n)&=x(n)+x\left(n+\frac{N}{2}\right),\\
x_2(n)&=\left[x(n)-x\left(n+\frac{N}{2}\right)\right]W_N^n,
\qquad 0\leq n\leq\frac{N}{2}-1.
\end{aligned}
\]</div>
<p>对 (x_1(n)) 与 (x_2(n)) 分别作 (N/2) 点 DFT，即得偶、奇频率序号的输出：</p>
<div class="formula">\[
\begin{aligned}
X(2r)&=\sum_{n=0}^{N/2-1}x_1(n)W_{N/2}^{nr},\\
X(2r+1)&=\sum_{n=0}^{N/2-1}x_2(n)W_{N/2}^{nr},
\qquad 0\leq r\leq\frac{N}{2}-1.
\end{aligned}
\]</div>
<p>递归进行该分解即可得到基-2 DIF-FFT。DIT 与 DIF 的总计算量相同，都可以原位计算，也都包含码位倒序；差别主要在顺序：DIF 是输入正序、输出码位倒序，DIT 则相反。两者的蝶形形式也略有不同，不能把旋转因子放在错误的支路上。</p>

<figure class="source-figure source-figure-flow">
<img src="../assets/source-figures/ch04-dif-fft-n8-flow.png" alt="基-2 DIF-FFT 算法蝶形流图，N 等于 8">
<figcaption>图 4-2 基-2 DIF-FFT 算法蝶形流图（N=8）</figcaption>
</figure>
<h1>4.4 快速傅里叶反变换的实现方法</h1>
<p>IDFT 与 DFT 的结构完全对应，只是旋转因子的指数符号相反，并多出比例因子：</p>
<div class="formula">\[
x(n)=\frac{1}{N}\sum_{k=0}^{N-1}X(k)W_N^{-nk}.
\]</div>
<p>因此可以直接把 FFT 流图中的旋转因子改为共轭旋转因子，并在最后统一乘以 (1/N)。若已有标准 FFT 子程序，也可使用共轭技巧：</p>
<div class="formula">\[
\operatorname{IDFT}\{X(k)\}=\frac{1}{N}\left[\operatorname{DFT}\{X^*(k)\}\right]^*.
\]</div>
<p>为防止中间蝶形结果溢出，也可将比例因子分散到各级中；无论采用何种缩放方式，最终总比例必须严格为 (1/N)。</p>

<h1>4.5 进一步减少运算量的措施</h1>
<h2>多类蝶形单元</h2>
<h3>四类蝶形单元的化简</h3>
<p>旋转因子中存在特殊值。若对这些值单独处理，可减少实数乘法次数：一类蝶形保留全部旋转因子乘法；二类蝶形去掉 (W_N^r=\pm1) 的乘法；三类蝶形进一步去掉 (W_N^r=\pm j) 的乘法；四类蝶形还对 (W_N^r=\frac{1}{\sqrt2}(\pm1\pm j)) 等特殊因子作专门处理。</p>
<table class="table"><thead><tr><th>(N)</th><th>一类</th><th>二类</th><th>三类</th><th>四类</th></tr></thead><tbody>
<tr><td>2</td><td>4</td><td>0</td><td>0</td><td>0</td></tr><tr><td>8</td><td>48</td><td>20</td><td>8</td><td>4</td></tr><tr><td>32</td><td>320</td><td>196</td><td>136</td><td>108</td></tr><tr><td>128</td><td>1792</td><td>1284</td><td>1032</td><td>908</td></tr><tr><td>512</td><td>9216</td><td>7172</td><td>6152</td><td>5644</td></tr><tr><td>2048</td><td>45056</td><td>36868</td><td>32776</td><td>30372</td></tr>
</tbody></table>
<p>表中数值为相应基-2 FFT 所需实数乘法次数。规模增大时，利用特殊旋转因子的收益更加明显。旋转因子的正弦、余弦值还可预先存入查找表，避免在执行中反复计算三角函数。</p>

<h2>实序列的 FFT</h2>
<p>若有两个 (N) 点实序列，可将一个序列作为复序列的实部，另一个作为虚部，经过一次 (N) 点 FFT 后，利用共轭对称性分离出各自的频谱。对于一个 (N) 点实序列，也可把偶序号样本与奇序号样本分别作为新序列的实部和虚部：</p>
<div class="formula">\[
\begin{aligned}
x_1(n)&=x(2n),\\
x_2(n)&=x(2n+1),\\
y(n)&=x_1(n)+j\,x_2(n),
\qquad 0\leq n\leq\frac{N}{2}-1.
\end{aligned}
\]</div>
<p><strong>一次半长 FFT 的分离公式：</strong>对 (y(n)) 作一次 (N/2) 点 FFT 得 (Y(k)) 后，取其偶、奇共轭分量，即可恢复偶、奇子序列的频谱：</p>
<div class="formula">\[
\begin{aligned}
X_1(k)&=Y_{\mathrm{ep}}(k),\\
X_2(k)&=-jY_{\mathrm{op}}(k),
\qquad 0\leq k\leq\frac{N}{2}-1.
\end{aligned}
\]</div>
<p><strong>实序列频谱的共轭对称关系：</strong>原序列为实序列时，后半谱可由前半谱得到：</p>
<div class="formula">\[
X(N-k)=X^*(k),
\qquad 0\leq k\leq\frac{N}{2}-1.
\]</div>
<p>将 (X_1(k)) 与 (X_2(k)) 代入 DIT 蝶形的加、减关系，即可得到 (X(k)) 的前、后半部分。这些公式说明，实序列的共轭对称性可使一个 (N) 点实序列的变换由一次 (N/2) 点复 FFT 完成。</p>

<h2>高斯的遗憾</h2>
<p>FFT 常称为 Cooley–Tukey 算法；但在此之前一个多世纪，高斯已在计算问题中提出过类似的快速思想。它在数字计算机时代才成为普遍重要的方法，说明算法价值既取决于数学结构，也取决于实际计算需求与技术条件。</p>

<h2>线性调频 z 变换</h2>
<p>标准 DFT 只在单位圆上以等角间隔取 (N) 个样本，且输入、输出长度相同。若只关心窄频带，或需要在非单位圆位置取样，直接增加 DFT 点数会造成不必要的计算。线性调频 z 变换（CZT）允许沿 z 平面的一段螺线以等角间隔取样。</p>
<div class="formula">\[
z_k=A_0W_0^{-k}e^{j\theta_0}e^{jk\varphi_0},
\qquad k=0,1,\ldots,M-1.
\]</div>
<p>其中 (A_0) 表示起始半径，\(\theta_0\) 表示起始相角，\(\varphi_0\) 为相邻样点的角度差，\(W_0\) 控制螺线伸展率（课件约定 (W_0>1) 时螺线向内收缩）。CZT 可以借助布鲁斯坦等式把目标样点的计算转化为时域卷积，再用 FFT 和 IFFT 高效完成；卷积长度选择必须避免循环混叠，只取所需的 (M) 个有效输出样点。</p>
<figure class="source-figure compact">
<img src="../assets/source-figures/ch04-czt-zplane-sampling.png" alt="CZT 在 z 平面上从起始向量开始沿螺线等角取样">
<figcaption>图 4-3　CZT 在 z 平面上的螺线取样路径</figcaption>
</figure>
<h3>布鲁斯坦等式与卷积化</h3>
<p>为写出计算关系，可将取样点简写为 \(z_k=AW^{-k}\)。则 z 变换样值满足：</p>
<div class="formula">\[
X(z_k)=\sum_{n=0}^{N-1}x(n)z_k^{-n}
=\sum_{n=0}^{N-1}x(n)A^{-n}W^{nk}.
\]</div>
<div class="formula">\[
nk=\frac{1}{2}\left[n^2+k^2-(k-n)^2\right],
\]</div>
<div class="formula">\[
X(z_k)=W^{k^2/2}
\sum_{n=0}^{N-1}
\left[x(n)A^{-n}W^{n^2/2}\right]W^{-(k-n)^2/2}.
\]</div>
<p><strong>卷积化的两个序列：</strong>下面的定义把输入加权为 (g(n))，并将二次相位项写为 (h(n))；它们用于把 CZT 求和改写成标准线性卷积。</p>
<div class="formula">\[
\begin{aligned}
g(n)&=x(n)A^{-n}W^{n^2/2},\
h(n)&=W^{-n^2/2},\\
X(z_k)&=W^{k^2/2}\,[g*h](k).
\end{aligned}
\]</div>
<p><strong>避免循环混叠的补零定义：</strong>使用 FFT 计算这段线性卷积时，取 \(L\geq N+M-1\)，并将两序列扩展为同一长度：</p>
<div class="formula">\[
L\geq N+M-1.
\]</div>
<div class="formula">\[
g_L(n)=
\begin{cases}
x(n)A^{-n}W^{n^2/2}, & 0\leq n\leq N-1,\\
0, & N\leq n\leq L-1,
\end{cases}
\qquad
h_L(n)=
\begin{cases}
W^{-n^2/2}, & 0\leq n\leq M-1,\\
0, & M\leq n\leq L-N,\\
W^{-(L-n)^2/2}, & L-N+1\leq n\leq L-1.
\end{cases}
\]</div>
<p>求和项因此成为两个序列的线性卷积形式。以这两个长度为 \(L\) 的序列作圆周卷积时，前 \(M\) 个输出恰为无混叠的线性卷积结果；实现上依次进行 FFT、逐点相乘和 IFFT，再只保留 \(k=0,1,\ldots,M-1\) 的有效样点。</p>
<figure class="source-figure source-figure-flow">
<img src="../assets/source-figures/ch04-czt-fft-convolution-flow.png" alt="CZT 以加权序列、两次 FFT、逐点相乘和 IFFT 完成卷积化计算的流程">
<figcaption>图 4-4　CZT 的 FFT 卷积化计算流程</figcaption>
</figure>
<p>这样，CZT 在窄带高分辨率观察或非单位圆 z 变换取样时，能比“盲目扩大整段 DFT”更有针对性。</p>
</main>
"""
    content = normalize_legacy_inline_math(content)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
