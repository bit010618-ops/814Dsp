"""Chapter-three §3.5 analog-signal spectrum analysis with DFT."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.steps{padding-left:1.5em;margin:5pt 0 8pt}.steps li{margin:3pt 0}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>3.5 用 DFT 对模拟信号作频谱分析</h1>
<p>将模拟信号的有限时段记录采样后作 DFT，得到的是连续频谱的离散观察。分析结果同时受时域采样、记录长度、截断和频域取样影响，因此必须区分采样频率与频率分辨率。</p>
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
<h2>工程处理流程</h2>
<ol class="steps">
<li>由最高频率 [[f_h]] 选定采样率，满足 [[f_s\geq2f_h]] 并留出模拟滤波过渡带。</li>
<li>由所需频率间隔 [[F_0]] 确定最小记录长度 [[T_0\geq1/F_0]]。</li>
<li>计算 [[N=T_0/T]]；若处理器要求 2 的整数幂，可向上选取合适 [[N]]。</li>
<li>根据泄漏要求选窗；需要更密显示时可零填充后再作 DFT。</li>
</ol>
<h2>例题：参数选取</h2>
<p>某 FFT 处理器要求采样点数为 2 的整数幂。若频率分辨率要求为 [[F_0\leq10\,\mathrm{Hz}]]，信号最高频率不超过 [[4\,\mathrm{kHz}]]，则先取 [[T_0\geq0.1\,\mathrm{s}]]，再取 [[f_s\geq8\,\mathrm{kHz}]]。相应点数 [[N=T_0f_s\geq800]]，向上取 1024 点；此时 [[T=1/8000\,\mathrm{s}]]，[[T_0=1024T=0.128\,\mathrm{s}]]，实际频率间隔为 [[F_0=7.8125\,\mathrm{Hz}]]。</p>
<h3>例题题干（原技术条件）</h3>
<p>有一频谱分析用的 FFT 处理器，其抽样点数必须是 2 的整数幂，假设没有采用任何数据处理的措施，已给条件为：（a）对频率分辨率的要求是 [[F_0\leq10\text{ Hz}]]；（b）信号频率不超过 [[4\text{ kHz}]]。试确定以下参量：（A）最小记录长度 [[T_0]]；（B）抽样点间的最大时间间隔 [[T]]（即最小抽样频率）；（C）在一个记录中最少点数 [[N]]。</p>
<p>解：[[T_0\geq1/F_0=0.1\text{ s}]]；为满足采样定理，[[f_s\geq2\times4\text{ kHz}=8\text{ kHz}]]，所以 [[T\leq0.125\text{ ms}]]。由 [[N\geq T_0f_s=800]] 且 [[N]] 必须为 2 的整数幂，取 [[N=1024]]。此时 [[T_0=1024\times0.125\text{ ms}=0.128\text{ s}]]，实际频率分辨率为 [[F_0=1/T_0=7.8125\text{ Hz}]]，满足要求。</p>

<h2>傅里叶的故事</h2>
<p>傅里叶分析得名于法国数学家让·巴普蒂斯·约瑟夫·傅里叶（1768—1830）。在他之前，人们已经知道可用三角函数描述周期现象；欧拉研究声波传播时进一步使用正弦分解，拉格朗日也将相关思想用于天体轨道的观察与预测。</p>
<p>1807 年，傅里叶提交有关热传播的论文，主张周期信号可以由适当的正弦分量组合表示。这一观点当时引起争议，特别是对于不连续信号能否分解的问题。后来他在《热的解析理论》（1822）中系统阐述了这些思想；狄利克雷等数学家给出了相应的严格条件，通常称为狄利克雷条件。</p>
<p>这一历史提醒我们：频谱图不是只为“看见峰值”，还要结合采样、截断、加窗和变换条件解释峰值为什么出现、为什么展宽，以及所得结论的适用范围。</p>
</main>
""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    html = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''
    output.write_text(html, encoding="utf-8")
    return output
