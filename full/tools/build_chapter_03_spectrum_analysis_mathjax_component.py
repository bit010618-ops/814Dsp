"""Chapter-three §3.5 analog-signal spectrum analysis with DFT."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}</style>"""


def analog_dft_spectrum_chain_svg() -> str:
    """Render the actual analog-to-DFT spectrum-analysis chain."""
    return '''<figure data-diagram="analog-dft-spectrum-chain" style="break-inside:avoid;margin:12pt 0 13pt"><svg viewBox="0 0 980 180" role="img" aria-labelledby="analog-dft-spectrum-chain-title" style="display:block;width:100%;height:auto;border:1px solid #d6dde2;border-radius:5pt;background:#fff"><title id="analog-dft-spectrum-chain-title">模拟信号经采样、截断和 DFT 的频谱分析流程</title><defs><marker id="analog-dft-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#174b73"/></marker></defs><text x="35" y="35" fill="#174b73" font-family="Microsoft YaHei, sans-serif" font-size="18" font-weight="700">模拟信号的 DFT 频谱分析链路</text><rect x="55" y="72" width="150" height="55" rx="6" fill="#f4f7f8" stroke="#0d8794" stroke-width="1.5"/><rect x="300" y="72" width="150" height="55" rx="6" fill="#f4f7f8" stroke="#0d8794" stroke-width="1.5"/><rect x="545" y="72" width="150" height="55" rx="6" fill="#fff8e8" stroke="#b56b2e" stroke-width="1.5"/><rect x="790" y="72" width="150" height="55" rx="6" fill="#eef7f1" stroke="#16866d" stroke-width="1.5"/><text x="130" y="105" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="17">模拟信号 xₐ(t)</text><text x="375" y="105" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="17">采样序列 x(n)</text><text x="620" y="105" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="17">有限记录 x(n)w(n)</text><text x="865" y="105" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="17">DFT 样值 X(k)</text><line x1="205" y1="99" x2="300" y2="99" stroke="#174b73" stroke-width="2" marker-end="url(#analog-dft-arrow)"/><line x1="450" y1="99" x2="545" y2="99" stroke="#174b73" stroke-width="2" marker-end="url(#analog-dft-arrow)"/><line x1="695" y1="99" x2="790" y2="99" stroke="#174b73" stroke-width="2" marker-end="url(#analog-dft-arrow)"/><text x="235" y="70" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">采样</text><text x="475" y="70" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">截断／加窗</text><text x="725" y="70" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">N 点 DFT</text><text x="58" y="160" fill="#52616d" font-family="Microsoft YaHei, sans-serif" font-size="14">采样率决定混叠；记录与窗函数决定泄漏和分辨率；零填充仅加密观察频点。</text></svg><figcaption style="margin-top:4pt;color:#52616d;text-align:center;font-size:9.5pt">图 3-8　模拟信号作 DFT 频谱分析的处理链。</figcaption></figure>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>3.5 用 DFT 对模拟信号作频谱分析</h1>
<p>将模拟信号的有限时段记录采样后作 DFT，得到的是连续频谱的离散观察。分析结果同时受时域采样、记录长度、截断和频域取样影响，因此必须区分采样频率与频率分辨率。</p>
""" + analog_dft_spectrum_chain_svg() + r"""
<h2>采样参数与频率分辨率</h2>
<div class="formula">\[
T_0=NT,\qquad f_s=\frac{1}{T},\qquad F_0=\frac{1}{T_0},\qquad f_s=NF_0.
\]</div>
<p>其中 [[T]] 为采样间隔，[[f_s]] 为采样频率，[[T_0]] 为记录长度，[[F_0]] 为频率分辨率（频谱间隔），[[N]] 为采样点数。为避免时域采样造成的频域混叠，应满足：</p>
<div class="formula">\[
f_s\geq2f_h.
\]</div>
<p>提高 [[f_s]] 扩大可观察的最高频率；增大记录长度 [[T_0]] 才能减小 [[F_0]]、提高频率分辨率。两者由不同参数控制，不能混为一谈。</p>
<h2>频谱分析的三个典型问题</h2>
<p><strong>频域混叠：</strong>时域采样率不足时，原连续频谱的周期副本相互重叠。处理方法是选择足够的 [[f_s]]，并在 A/D 前使用抗混叠低通滤波器。</p>
<p><strong>频谱泄漏：</strong>有限时间记录等价于时域乘窗，频域则与窗函数频谱卷积；非整周期截断会使原本集中的谱线扩展到相邻频率。选择合适的窗函数形状、增加窗长可改善泄漏表现。</p>
<p><strong>栅栏效应：</strong>DFT 只在离散频点上取样，真实谱峰若落在两个 DFT 栅栏之间，观察到的峰值与位置都会受限。时域零填充能加密频域样点，使观察更细致，但不改变由 [[T_0]] 决定的本征分辨率。</p>
<h2>窗函数与记录长度</h2>
<p>矩形窗主瓣较窄但旁瓣较高；三角窗和升余弦类窗可降低旁瓣、缓解泄漏，但主瓣会变宽。窗的形状决定主瓣与旁瓣的权衡，窗长 [[N]] 增大则通常使过渡带变窄。选择窗函数时应根据相邻谱线间隔与强弱差异综合判断。</p>
<h2>矩形窗的频谱展宽</h2>
<p><strong>矩形窗频谱公式：</strong>长度为 [[N]] 的矩形窗在频域中的响应为：</p>
<div class="formula">\[
W_R\left(e^{j\omega}\right)
=e^{-j\frac{N-1}{2}\omega}
\frac{\sin\left(\frac{N\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}.
\]</div>
<p>这个公式用来判断有限记录对单根谱线的展宽方式。其幅度主瓣的两侧第一个零点间隔约为 [[4\pi/N]]；因此增大 [[N]] 能使主瓣变窄、过渡带变窄。仅仅增大记录长度并不会使矩形窗旁瓣的相对起伏消失，强谱线附近仍可能掩盖较弱谱线。</p>
<h2>观察实例：窗口长度与泄漏</h2>
<p><strong>单一余弦的记录长度比较：</strong>令 [[x(n)=\cos\left(\frac{\pi}{4}n\right)]]，分别记录 [[y_1(n)=x(n)R_{32}(n)]] 与 [[y_2(n)=x(n)R_{64}(n)]]。这两个记录使用同一种矩形窗；较长的 [[R_{64}(n)]] 使主瓣更窄，从而使频率位置的观察更精细。</p>
<p><strong>强弱相邻分量的记录长度比较：</strong>令</p>
<div class="formula">\[
x(n)=\cos\left(\frac{\pi}{4}n\right)+0.2\cos\left(\frac{\pi}{5}n\right).
\]</div>
<p>分别采用 [[R_{40}(n)]] 和 [[R_{320}(n)]] 截取记录。短记录时，较强分量的泄漏可能覆盖弱分量；延长为 [[R_{320}(n)]] 后主瓣变窄，弱分量更容易分辨。三角窗通常具有更低旁瓣、但更宽主瓣：若窗口长度不变，它未必更利于分开很接近的两条谱线。</p>
<h2>零填充的作用</h2>
<p><strong>零填充序列：</strong>把已有的 [[N]] 点记录补到 [[L]] 点，可写成：</p>
<div class="formula">\[
x_L(n)=
\begin{cases}
x(n),&0\leq n\leq N-1,\\
0,&N\leq n\leq L-1.
\end{cases}
\]</div>
<p>此操作用于加密 DFT 的频率观察网格：频点间隔由 [[2\pi/N]] 变为 [[2\pi/L]]。它不会延长真实记录 [[T_0]]，也不会改变本征频率分辨率 [[F_0=1/T_0]]；零填充只能帮助更细地观察已有频谱形状。</p>
<h2>工程处理流程</h2>
<ol class="steps">
<li>由最高频率 [[f_h]] 选定采样率，满足 [[f_s\geq2f_h]] 并留出模拟滤波过渡带。</li>
<li>由所需频率间隔 [[F_0]] 确定最小记录长度 [[T_0\geq1/F_0]]。</li>
<li>计算 [[N=T_0/T]]；若处理器要求 2 的整数幂，可向上选取合适 [[N]]。</li>
<li>根据泄漏要求选窗；需要更密显示时可零填充后再作 DFT。</li>
</ol>
<h2>例题：参数选取</h2>
<p>某 FFT 处理器要求采样点数为 2 的整数幂。若频率分辨率要求为 [[F_0\leq10\,\mathrm{Hz}]]，信号最高频率不超过 [[4\,\mathrm{kHz}]]，则先取 [[T_0\geq0.1\,\mathrm{s}]]，再取 [[f_s\geq8\,\mathrm{kHz}]]。相应点数 [[N=T_0f_s\geq800]]，向上取 1024 点；此时 [[T=1/8000\,\mathrm{s}]]，[[T_0=1024T=0.128\,\mathrm{s}]]，实际频率间隔为 [[F_0=7.8125\,\mathrm{Hz}]]。</p>
<h3>例题题干</h3>
<p>有一频谱分析用的 FFT 处理器，其抽样点数必须是 2 的整数幂，假设没有采用任何数据处理的措施，已给条件为：（a）对频率分辨率的要求是 [[F_0\leq10\text{ Hz}]]；（b）信号频率不超过 [[4\text{ kHz}]]。试确定以下参量：（A）最小记录长度 [[T_0]]；（B）抽样点间的最大时间间隔 [[T]]（即最小抽样频率）；（C）在一个记录中最少点数 [[N]]。</p>
<p>解：[[T_0\geq1/F_0=0.1\text{ s}]]；为满足采样定理，[[f_s\geq2\times4\text{ kHz}=8\text{ kHz}]]，所以 [[T\leq0.125\text{ ms}]]。由 [[N\geq T_0f_s=800]] 且 [[N]] 必须为 2 的整数幂，取 [[N=1024]]。此时 [[T_0=1024\times0.125\text{ ms}=0.128\text{ s}]]，实际频率分辨率为 [[F_0=1/T_0=7.8125\text{ Hz}]]，满足要求。</p>

<h2>傅里叶的故事</h2>
<p>傅里叶分析得名于法国数学家让·巴普蒂斯·约瑟夫·傅里叶（1768—1830）。在他之前，人们已经知道可用三角函数描述周期现象；欧拉研究声波传播时进一步使用正弦分解，拉格朗日也将相关思想用于天体轨道的观察与预测。</p>
<p>1807 年，傅里叶提交有关热传播的论文，主张周期信号可以由适当的正弦分量组合表示。这一观点当时引起争议，特别是对于不连续信号能否分解的问题。后来他在《热的解析理论》（1822）中系统阐述了这些思想；狄利克雷等数学家给出了相应的严格条件，通常称为狄利克雷条件。</p>
<p>这一历史提醒我们：频谱图不是只为“看见峰值”，还要结合采样、截断、加窗和变换条件解释峰值为什么出现、为什么展宽，以及所得结论的适用范围。</p>
</main>
"""
    content = content.replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    html = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(html, encoding="utf-8")
    return output
