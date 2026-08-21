"""Second verified batch of supplemental chapter-three DFS/DFT training."""
from __future__ import annotations

from pathlib import Path

from full.tools.build_chapter_08_training_mathjax_component import _document


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第三章 补充真题（第二批）</h1>
<div class="exam-head"><span>2013 年真题（填空题第 5 小题）</span><span>详解见 P.____</span></div>
<p>一、填空题。5．\(x[n]\) 为实偶的周期信号，\(N=4\)，其傅里叶级数为 \(a_k\)，已知 \(a_2=3\)，\(a_7=5\)，求 \(a_{-3}=\underline{\hspace{16mm}}\)，\(a_{-2}=\underline{\hspace{16mm}}\)，\(a_{-1}=\underline{\hspace{16mm}}\)。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2014 年真题（填空题第 7 小题）</span><span>详解见 P.____</span></div>
<p>一、填空题。7．已知 \(x(n)\) 为一实偶周期信号，\(N=6\)，其傅里叶级数为 \(a_k\)，且 \(a_{14}=2\)，\(a_5=1\)，\(\sum_{n=0}^{5}x(n)=2\)，\(\sum_{n=0}^{5}x(n)(-1)^n=1\)，求 \(a_{-3}=\underline{\hspace{14mm}}\)，\(a_{-2}=\underline{\hspace{14mm}}\)，\(a_{-1}=\underline{\hspace{14mm}}\)，\(a_0=\underline{\hspace{14mm}}\)。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2015 年真题（填空题第 3 小题）</span><span>详解见 P.____</span></div>
<p>一、填空题。3．序列 \(x(n)\) 的 \(N\) 点 DFT 是 \(x(n)\) 的 \(z\) 变换在________的 \(N\) 点等间隔取样；</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2015 年真题（填空题第 4 小题）</span><span>详解见 P.____</span></div>
<p>一、填空题。4．若 \(x_1(n)=R_4(n)\)，\(x_2(n)=R_5(n)\)，只有当循环卷积长度 \(L\)________的时候，二者的循环卷积等于线性卷积；</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2016 年真题（DSP 第 3 小题）</span><span>详解见 P.____</span></div>
<p>七、DSP 题目。3．已知 \(x(n)=\delta(n)+\delta(n-1)+\delta(n-2)+\delta(n-3)\)，\(X(k)\) 是 \(x(n)\) 的 6 点 DFT，若 \(Y(k)=X(2k)\)，求 \(Y(k)\) 的三点 DFT 反变换 \(y(n)\) 的值。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2016 年真题（DSP 第 4 小题）</span><span>详解见 P.____</span></div>
<p>七、DSP 题目。4．若 \(x(n)=2+2\cos\left(\frac{2\pi n}{N}\right)\)，设 \(X(k)\) 是 \(x(n)\) 的 \(N\) 点 DFT，求 \(X(k)\)。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2016 年真题（DSP 第 5 小题）</span><span>详解见 P.____</span></div>
<p>七、DSP 题目。5．栅栏效应是什么？简述减小方法。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2016 年真题（第八题）</span><span>详解见 P.____</span></div>
<p>八、\(N\) 点 \(x_1(n)\)、\(x_2(n)\)，用一次 \(N\) 点 DFT，其中 \(x_1(n)\)、\(x_2(n)\) 各自的 \(N\) 点 DFT 的值为 \(X_1(k)\) 和 \(X_2(k)\)，应如何设计？</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解（第三章补充）</h1>
<h2>2013 年真题（填空题第 5 小题）</h2>
<p>实偶周期序列的 DFS 系数满足周期性与偶对称性：</p>
<div class="formula">\[
a_{k+N}=a_k,\qquad a_{-k}=a_k.
\]</div>
<p>由 \(a_7=a_3=5\)，又 \(a_{-3}=a_1=a_3\)，故：</p>
<div class="formula">\[
a_{-3}=5,\qquad a_{-2}=a_2=3,\qquad a_{-1}=a_1=5.
\]</div>
<h2>2014 年真题（填空题第 7 小题）</h2>
<p>实偶序列仍有 \(a_{-k}=a_k\) 与 \(a_{k+6}=a_k\)。先由下标周期性得到：</p>
<div class="formula">\[
a_2=a_{14}=2,\qquad a_1=a_{-1}=a_5=1.
\]</div>
<p>DFS 的直流项与 \(k=3\) 项分别为：</p>
<div class="formula">\[
a_0=\frac{1}{6}\sum_{n=0}^{5}x(n)=\frac{1}{3},\qquad
a_3=\frac{1}{6}\sum_{n=0}^{5}x(n)(-1)^n=\frac{1}{6}.
\]</div>
<p>所以：</p><div class="formula">\[
a_{-3}=a_3=\frac{1}{6},\qquad a_{-2}=a_2=2,\qquad
a_{-1}=a_1=1,\qquad a_0=\frac{1}{3}.
\]</div>
<h2>2015 年真题（填空题第 3 小题）</h2>
<p>DFT 是 \(z\) 变换在单位圆上的等间隔取样：</p>
<div class="formula">\[
X(k)=X(z)\left|_{z=e^{j2\pi k/N}}\right.,\qquad k=0,1,\ldots,N-1.
\]</div>
<p>填：<strong>单位圆上</strong>。</p>
<h2>2015 年真题（填空题第 4 小题）</h2>
<p>两个有限序列线性卷积的长度为 \(4+5-1\)。为不发生循环折叠，循环卷积长度必须满足：</p>
<div class="formula">\[
L\geq4+5-1=8.
\]</div>
<h2>2016 年真题（DSP 第 3 小题）</h2>
<p>对 6 点 DFT 的频域偶抽取，作 3 点 IDFT 时对应时域按间隔 3 的周期叠加：</p>
<div class="formula">\[
y(n)=x(n)+x(n+3),\qquad n=0,1,2.
\]</div>
<p>原序列在 \(n=0,1,2,3\) 取 1，其余取 0，因此：</p>
<div class="formula">\[
y(0)=2,\qquad y(1)=1,\qquad y(2)=1.
\]</div>
<h2>2016 年真题（DSP 第 4 小题）</h2>
<p>先把余弦展开为复指数：</p>
<div class="formula">\[
x(n)=2+e^{j2\pi n/N}+e^{-j2\pi n/N}.
\]</div>
<p>据 DFT 基函数正交性，一个周期内仅三个谱线非零：</p>
<div class="formula">\[
X(0)=2N,\qquad X(1)=N,\qquad X(N-1)=N,
\]</div>
<p>其余 \(X(k)=0\)。</p>
<h2>2016 年真题（DSP 第 5 小题）</h2>
<p>栅栏效应是有限长记录的 DFT 只能在离散栅栏频点取样，真实谱峰若落在两个频点之间，其能量会被相邻频点分摊，幅值与频率估计因而产生偏差。可通过延长有效记录时间、增加 DFT 点数以减小频率间隔、尽量作相干采样，并结合合适窗函数降低泄露影响来改善。</p>
<h2>2016 年真题（第八题）</h2>
<p>构造一个复序列：</p><div class="formula">\[
x(n)=x_1(n)+jx_2(n).
\]</div>
<p>只作一次 \(N\) 点 DFT 得 \(X(k)\)。因为 \(x_1(n)\)、\(x_2(n)\) 都是实序列，利用共轭对称性可分离：</p>
<div class="formula">\[
X_1(k)=\frac{1}{2}\left[X(k)+X^*\left((N-k)\right)_N\right],
\qquad
X_2(k)=\frac{1}{2j}\left[X(k)-X^*\left((N-k)\right)_N\right].
\]</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output
