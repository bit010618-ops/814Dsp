"""Source-checked supplemental FFT questions for chapter four."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


QUESTION_IDS = (
    "2024-dsp-p5", "2007-q十一-whole", "2007-q十三-p2", "2015-qintro-p5", "2015-qintro-p6",
    "2017-q六-p4", "2020-qintro-p1", "2020-qintro-p5", "2023-dsp-p5",
)


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:20pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.exam-page{break-before:page;min-height:230mm}.exam-page:first-child{break-before:auto}.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:0 0 10pt}.formula{break-inside:avoid;padding:7pt 4pt;margin:8pt 0;text-align:center;overflow-x:auto}.writing-space{min-height:172mm}.answer-step{break-inside:avoid;margin:8pt 0}.answer-step strong{color:#315d7c}.fft-flow{break-inside:avoid;margin:12pt 0}.fft-flow img,.fft-flow svg{display:block;width:100%;height:auto;border:.5pt solid #d6dde2;background:#fff}.fft-flow figcaption{color:#52616b;text-align:center;margin-top:5pt;font-size:9.5pt}@media(max-width:560px){body{font-size:10.5pt}.writing-space{min-height:145mm}}
</style>"""


def _document(content: str) -> str:
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'''


def _valued_dit_flow() -> str:
    rows = [
        ("x[0]=1", "x[4]=0", "x[2]=3", "x[6]=0", "x[1]=2", "x[5]=0", "x[3]=4", "x[7]=0"),
    ][0]
    y = [58 + 36 * index for index in range(8)]
    paths = []
    for stage, span in ((178, 1), (340, 2), (502, 4)):
        step = span * 2
        for start in range(0, 8, step):
            for offset in range(span):
                top = start + offset
                bottom = top + span
                paths.append(f'<path d="M {stage - 88} {y[top]} L {stage} {y[top]} M {stage - 88} {y[bottom]} L {stage} {y[bottom]} M {stage} {y[top]} L {stage + 72} {y[top]} M {stage} {y[bottom]} L {stage + 72} {y[bottom]}"/>')
                paths.append(f'<path d="M {stage - 88} {y[top]} L {stage + 72} {y[bottom]} M {stage - 88} {y[bottom]} L {stage + 72} {y[top]}" class="cross"/>')
    labels = ''.join(f'<text x="8" y="{y[index] + 5}" class="sample">{value}</text>' for index, value in enumerate(rows))
    output_labels = ''.join(f'<text x="595" y="{y[index] + 5}" class="sample">X[{index}]</text>' for index in range(8))
    return f'''<svg viewBox="0 0 680 350" role="img" aria-label="8 点基 2 DIT FFT 蝶形流图，输入码位倒序且已标注样值">
<style>.line{{stroke:#1e4f79;stroke-width:1.25;fill:none}}.cross{{stroke:#b56b2e;stroke-width:1.05;fill:none}}.sample{{font:13px 'Times New Roman',serif;fill:#1f2933}}.stage{{font:14px 'Microsoft YaHei',sans-serif;fill:#315d7c}}.note{{font:12px 'Microsoft YaHei',sans-serif;fill:#52616b}}</style>
<text x="36" y="22" class="stage">码位倒序输入</text><text x="132" y="22" class="stage">第 1 级</text><text x="294" y="22" class="stage">第 2 级</text><text x="456" y="22" class="stage">第 3 级</text><text x="585" y="22" class="stage">自然顺序输出</text>
<g class="line">{''.join(paths)}</g>{labels}{output_labels}
<text x="185" y="338" class="note">每一级为 4 个标准蝶形单元；第 3 级的下支路依次乘以 W₈ᵏ（k=0,1,2,3）。</text>
</svg>'''


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第四章 补充真题</h1>
<div class="exam-head"><span>2007 年真题</span><span>详解见 P.____</span></div>
<p>十一、请简略推导采用按时间抽取的 2-FFT 算法将 8 点 DFT 计算分解为两个 4 点 DFT 计算的过程，并画出分解后的算法流图。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2007 年真题</span><span>详解见 P.____</span></div>
<p>（2）如果只能进行一次 256 点数值的 FFT 运算，用什么办法能实现信号 \(x(n)\) 的谱分析？</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2015 年真题</span><span>详解见 P.____</span></div>
<p>5.直接计算 \(N=16\) 的 DFT，需要进行________次复数乘法，________次复数加法。使用 2FFT 算法，需要________次复数乘法；</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2015 年真题</span><span>详解见 P.____</span></div>
<p>6.FFT 是利用________来减小计算量的；</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2017 年真题</span><span>详解见 P.____</span></div>
<p>4.实现一个 10000 点的序列与一个 100 点长的 FIR 单位脉冲响应的线性卷积，要求利用重叠相加法并通过 256 点 FFT 和 IFFT 来实现，问至少需要多少次 FFT 和 IFFT？</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2020 年真题</span><span>详解见 P.____</span></div>
<p>1.计算 256 点的按时间抽取基-2FFT，在每一级有________个蝶形运算。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2020 年真题</span><span>详解见 P.____</span></div>
<p>5.直接计算 \(N\) 点 DFT 需要进行________次复数乘法运算。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2023 年真题</span><span>详解见 P.____</span></div>
<p>5.已知序列 \(x(n)=(n+1)R_4(n)\)，利用基 2-DIT-FFT 算法，画出 \(x(n)\) 的 8 点离散 FT 的蝶形运算流图，输入序列的值需标在图中。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2024 年真题</span><span>详解见 P.____</span></div>
<p>5.一个 8000 点的序列与线性时不变滤波器线性卷积，滤波器的单位脉冲响应长度为 50 点，为了利用快速傅里叶变换算法的计算效率，该滤波器用 128 点的 FFT 和 IFFT 实现，如果采用重叠保留法，为了完成滤波运算，需要至少进行多少次 FFT 运算和 IFFT 运算？请写出推算过程。</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    flow = _valued_dit_flow()
    content = r"""
<main><h1>真题整理详解</h1>
<h2>2007 年真题</h2>
<h3>第十一题：8 点 DFT 的按时间抽取分解</h3>
<p><strong>第 1 步：偶、奇序列分解。</strong>令 \(N=8\)，把输入按偶、奇时间下标拆为两条 4 点序列。利用 \(W_8^{2k}=W_4^k\)，有：</p>
<div class="formula">\[X[k]=\sum_{n=0}^3x[2n]W_4^{kn}+W_8^k\sum_{n=0}^3x[2n+1]W_4^{kn},\qquad 0\leq k\leq3.\]</div>
<p>两项各是一个 4 点 DFT。记为 \(E[k]\)、\(O[k]\)，则蝶形合成为：</p>
<div class="formula">\[\begin{aligned}X[k]&=E[k]+W_8^kO[k],\\X[k+4]&=E[k]-W_8^kO[k],\qquad 0\leq k\leq3.\end{aligned}\]</div>
<p><strong>第 2 步：画流图。</strong>继续把每个 4 点 DFT 递归拆成两个 2 点 DFT，共得到 3 级。按时间抽取结构的输入为码位倒序，输出为自然顺序；每一级含 \(N/2=4\) 个蝶形。</p>
<figure class="fft-flow" data-diagram="dit-two-four-point-decomposition"><img src="../assets/source-figures/ch04-dit-fft-n8-flow.png" alt="8 点按时间抽取基 2 FFT 流图"><figcaption>8 点 DFT 按时间抽取的 2-FFT 分解流图</figcaption></figure>
<h3>第十三题第（2）问：一次 256 点 FFT 的谱分析</h3>
<p>将 500 点实序列拆为两段各 250 点的实序列，分别补零到 256 点。构造 \(c[n]=x_1[n]+jx_2[n]\)，只作一次 256 点复 FFT，得到 \(C[k]\)。由两段均为实序列的共轭对称性可还原两个谱：</p>
<div class="formula">\[\begin{aligned}X_1[k]&=\frac{1}{2}\left(C[k]+C^*[(-k)_{256}]\right),\\X_2[k]&=\frac{1}{2j}\left(C[k]-C^*[(-k)_{256}]\right).\end{aligned}\]</div>
<p>这样一次复数 256 点 FFT 等效获得两段 256 点实序列的频谱，可分别对两段作谱分析并比较。频率分辨率为 \(f_s/256=32\,\text{Hz}\)，其中 800 Hz 对应第 \(k=25\) 个频点。</p>
<h2>2015 年真题</h2>
<p><strong>第 5 小题。</strong>直接计算 \(N\) 点 DFT：每个输出频点要进行 \(N\) 次复乘并累加 \(N\) 项，因此总复乘数为 \(N^2\)，复加数为 \(N(N-1)\)。代入 \(N=16\)：</p>
<div class="formula">\[N^2=256,\qquad N(N-1)=240.\]</div>
<p>基-2 FFT 的复乘次数为 \(\frac{N}{2}\log_2N\)，故 16 点时为 \(\frac{16}{2}\times4=32\)。填空依次为 256、240、32。</p>
<p><strong>第 6 小题。</strong>FFT 是利用 DFT 的对称性和周期性，把长度 \(N\) 的 DFT 逐级分解为若干短 DFT，再复用中间运算结果来减小计算量的。</p>
<h2>2017 年真题</h2>
<p><strong>第六题第（4）问。</strong>重叠相加法中，FFT 长度为 \(L=256\)，滤波器长度 \(N_2=100\)，每个输入分段的最大新样本数为：</p>
<div class="formula">\[M=L-N_2+1=256-100+1=157.\]</div>
<p>10000 点输入需分为 \(K=\left\lceil10000/157\right\rceil=64\) 段。滤波器频谱预先计算一次；各输入段各需一次 FFT 和一次 IFFT：</p>
<div class="formula">\[N_{\mathrm{FFT}}=1+K=65,\qquad N_{\mathrm{IFFT}}=K=64.\]</div>
<h2>2020 年真题</h2>
<p><strong>第 1 小题。</strong>256 点基-2 FFT 每一级的蝶形数始终为 \(N/2\)，故为 \(\frac{N}{2}=128\)。</p>
<p><strong>第 5 小题。</strong>直接计算 \(N\) 点 DFT 有 \(N\) 个输出，每个输出含 \(N\) 次复数乘法，故复数乘法次数为 \(N^2\)。</p>
<h2>2023 年真题</h2>
<p><strong>第 5 小题。</strong>先补零到 8 点。\(x(n)=(n+1)R_4(n)\) 的自然顺序输入为 \(\{1,2,3,4,0,0,0,0\}\)。DIT-FFT 的流图输入端按码位倒序排列为 \(\{x[0],x[4],x[2],x[6],x[1],x[5],x[3],x[7]\}\)，也就是 \(\{1,0,3,0,2,0,4,0\}\)。</p>
<figure class="fft-flow" data-diagram="dit-eight-point-values-flow">__VALUES_FLOW__<figcaption>标出输入样值的 8 点基-2 DIT-FFT 蝶形运算流图</figcaption></figure>
<p>图中共有 \(\log_2 8=3\) 级，每一级有 4 个蝶形；由左到右完成递归组合，最右端得到 \(X[0],X[1],\ldots,X[7]\)。</p>
<h2>2024 年真题</h2>
<p><strong>DSP 第 5 小题。</strong>重叠保留法中，FFT 长度 \(L=128\)，滤波器长度 \(N_2=50\)。每段保留的有效输出个数为：</p>
<div class="formula">\[M=L-N_2+1=128-50+1=79.\]</div>
<p>8000 个输入样本需分段数为 \(K=\left\lceil8000/79\right\rceil=102\)。滤波器的 128 点 FFT 只需计算一次，102 个输入段各需一次 FFT 和一次 IFFT，因此：</p>
<div class="formula">\[N_{\mathrm{FFT}}=1+102=103,\qquad N_{\mathrm{IFFT}}=102.\]</div>
<p>前置 \(N_2-1=49\) 个零仅用于提供第一段所需的历史样本，不增加有效输出数；每段丢弃前 49 个循环卷积样本，保留后 79 个样本并依次拼接。</p>
</main>""".replace("__VALUES_FLOW__", flow)
    output.write_text(_document(content), encoding="utf-8")
    return output
