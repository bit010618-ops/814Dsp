"""Chapter-three §3.1 DFS material as one reflowable MathJax component."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}
h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}
p{margin:5pt 0 8pt}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.note{color:#52616b;margin:4pt 0 8pt}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>3.1 离散傅里叶级数及其性质</h1>
<p>周期离散序列在时域和频域都呈离散性、周期性。离散傅里叶级数（DFS）给出一个周期内的时域样值与一个周期内的频域系数之间的对应关系；它是后续 DFT、循环卷积和频域取样的直接基础。</p>

<h2>DFS 的变换对</h2>
<p>设 [[\widetilde{x}(n)]] 是以 [[N]] 为周期的离散序列。记旋转因子为：</p>
<div class="formula">\[
W_N=e^{-j\frac{2\pi}{N}},\qquad W_N^{k+N}=W_N^k.
\]</div>
<p>一个周期内的 DFS 正变换与反变换分别为：</p>
<div class="formula">\[
\widetilde{X}(k)=\sum_{n=0}^{N-1}\widetilde{x}(n)W_N^{nk},\qquad
\widetilde{x}(n)=\frac{1}{N}\sum_{k=0}^{N-1}\widetilde{X}(k)W_N^{-nk}.
\]</div>
<p>其中 [[n]] 和 [[k]] 都可取任意整数，但只需考察任意连续的 [[N]] 个样值。因 [[W_N^{N}=1]]，有：</p>
<div class="formula">\[
\widetilde{x}(n+N)=\widetilde{x}(n),\qquad
\widetilde{X}(k+N)=\widetilde{X}(k).
\]</div>
<p class="note">记忆时应同时保留反变换前的系数 [[1/N]] 与指数符号的相反性；两者不能遗漏。</p>

<h2>由 DTFT 到 DFS</h2>
<p>将一个有限长序列取 [[N]] 点后作周期延拓，便得到 [[\widetilde{x}(n)]]。其 DTFT 是周期谱；在一个周期内等间隔取 [[N]] 个频率样值，就得到 DFS 系数。因而 DFS 描述的是“时域周期、频域离散”的情形。</p>
<div class="formula">\[
\widetilde{X}(k)=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{N}}.
\]</div>
<h3>采样参数与频域离散的对应</h3>
<p>把连续时间信号每隔 [[T]] 采样一次，并以 [[N]] 个样值构成一个周期时，记录周期与频率取样间隔由同一组参数确定：</p>
<div class="formula">\[
T_0=NT,\qquad f_s=\frac{1}{T},\qquad F_0=\frac{1}{T_0},\qquad f_s=NF_0.
\]</div>
<div class="formula">\[
\Omega_s=2\pi f_s=\frac{2\pi}{T},\qquad
\Omega_0=2\pi F_0=\frac{2\pi}{T_0},\qquad
\frac{k}{N}=\frac{\omega}{2\pi}=\frac{f}{f_s}=\frac{\Omega}{\Omega_s}.
\]</div>
<p>相反地，DFS 系数经过反变换恢复一周期内的样值，并按 [[N]] 周期延拓。时间与频率的周期性形成严格对偶，后续判断循环卷积、频域抽样或零填充时都需要先确认这个周期 [[N]]。</p>

<h2>DFS 的基本性质</h2>
<p>以下等式均在相同周期 [[N]] 下成立。若 [[\widetilde{x}_1(n)\leftrightarrow\widetilde{X}_1(k)]]、[[\widetilde{x}_2(n)\leftrightarrow\widetilde{X}_2(k)]]，则：</p>
<div class="formula">\[
a\widetilde{x}_1(n)+b\widetilde{x}_2(n)
\quad\longleftrightarrow\quad
a\widetilde{X}_1(k)+b\widetilde{X}_2(k).
\]</div>
<div class="formula">\[
\widetilde{x}(n-n_0)
\quad\longleftrightarrow\quad
W_N^{kn_0}\widetilde{X}(k),\qquad
\widetilde{x}(n)W_N^{-n k_0}
\quad\longleftrightarrow\quad
\widetilde{X}(k-k_0).
\]</div>
<p>周期移位和频移均按模 [[N]] 理解。周期卷积把时域卷积与频域逐点相乘对应起来：</p>
<div class="formula">\[
\widetilde{y}(n)=\widetilde{x}_1(n)\mathbin{\circledast}_N\widetilde{x}_2(n)
\quad\longleftrightarrow\quad
\widetilde{Y}(k)=\widetilde{X}_1(k)\widetilde{X}_2(k),
\]</div>
<div class="formula">\[
\widetilde{y}(n)=\sum_{m=0}^{N-1}\widetilde{x}_1(m)\widetilde{x}_2(n-m).
\]</div>
<p>下标 [[n-m]] 必须按周期折回。若希望用循环卷积得到有限长序列的线性卷积，周期长度必须足够长，避免首尾混叠。</p>

<h2>对偶性</h2>
<p>DFS 的时域和频域都具有离散周期结构，因此其对偶性比一般 z 变换更直接：</p>
<div class="formula">\[
\widetilde{x}(n)\quad\longleftrightarrow\quad\widetilde{X}(k)
\qquad\Longrightarrow\qquad
\widetilde{X}(n)\quad\longleftrightarrow\quad N\widetilde{x}(-k).
\]</div>
<p>使用这条性质时，反折、系数 [[N]] 与变量位置必须同时出现；不能只把两个符号互换。</p>

<h2>例题：8 点周期延拓序列的 DFS</h2>
<p>已知序列 [[x(n)=R_4(n)]]，将 [[x(n)]] 以 [[N=8]] 为周期进行周期延拓形成 [[\widetilde{x}_8(n)]]，求 [[\widetilde{x}_8(n)]] 的 DFS 一个周期内的系数。</p>
<h3>解</h3>
<p>在一个周期 [[0\leq n\leq7]] 内，前四个样值为 1，其余四个样值为 0。因此正变换的求和上限可由 7 缩至 3：</p>
<div class="formula">\[
\begin{aligned}
\widetilde{X}_8(k)
&=\sum_{n=0}^{7}\widetilde{x}_8(n)W_8^{nk}\\
&=\sum_{n=0}^{3}W_8^{nk}
=1+W_8^k+W_8^{2k}+W_8^{3k}.
\end{aligned}
\]</div>
<p>代入 [[W_8=e^{-j\pi/4}]]，在 [[k=0,1,\ldots,7]] 的一个周期内得到：</p>
<div class="formula">\[
\begin{aligned}
&\widetilde{X}_8(0)=4,\qquad
\widetilde{X}_8(2)=\widetilde{X}_8(4)=\widetilde{X}_8(6)=0,\\
&\widetilde{X}_8(1)=1-j(1+\sqrt{2}),\qquad
\widetilde{X}_8(3)=1-j(\sqrt{2}-1),\\
&\widetilde{X}_8(5)=\widetilde{X}_8^*(3),\qquad
\widetilde{X}_8(7)=\widetilde{X}_8^*(1).
\end{aligned}
\]</div>
<p>由于 [[\widetilde{x}_8(n)]] 为实序列，结果满足共轭对称性。计算完成后，先检查直流系数是否等于一个周期内样值之和，再检查共轭对称性，可快速发现旋转因子符号错误。</p>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(document, encoding="utf-8")
    return output
