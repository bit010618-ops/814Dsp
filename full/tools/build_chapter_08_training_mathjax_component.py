"""Chapter-eight multirate-system training and consolidated answer components."""
from __future__ import annotations

from pathlib import Path

from full.tools.render_mathjax_formula import MATHJAX


QUESTION_IDS = (
    "2013-q九-whole",
    "2015-q八-whole",
    "2016-qintro-brief2",
    "2020-qintro-brief3",
)


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:20pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.exam-page{break-before:page;break-inside:avoid;page-break-inside:avoid;min-height:230mm}.exam-page:first-child{break-before:auto}.exam-head{display:flex;justify-content:space-between;gap:18pt;color:#52616b;margin:0 0 10pt}.writing-space{min-height:118mm}.answer-step{break-inside:avoid;margin:8pt 0}.answer-step strong{color:#315d7c}.formula{break-inside:avoid;padding:7pt 4pt;margin:8pt 0;text-align:center;overflow-x:auto}.diagram{display:block;width:100%;max-width:166mm;height:auto;margin:10pt auto;break-inside:avoid}@media(max-width:560px){body{font-size:10.5pt}.writing-space{min-height:100mm}}
</style>"""


def _document(content: str) -> str:
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<body>{content}</body></html>'''


def _math(x: int, y: int, width: int, text: str, height: int = 34) -> str:
    return (
        f'<foreignObject x="{x}" y="{y}" width="{width}" height="{height}">'
        f'<div xmlns="http://www.w3.org/1999/xhtml" style="font:16px serif;text-align:center">\\({text}\\)</div>'
        '</foreignObject>'
    )


def _multirate_chain() -> str:
    """Redraw the source chain and input spectrum without its watermark/template."""
    return f'''<svg class="diagram" data-source-candidate-id="2015-q八-01" data-diagram="multirate-zero-insertion-chain" viewBox="0 0 960 520" role="img" aria-label="零值插入、低通滤波和周期采样的多采样率系统及输入频谱">
<defs><marker id="mr-arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0L9,4.5L0,9Z" fill="#174b73"/></marker></defs>
<text x="480" y="30" text-anchor="middle" fill="#263746" style="font:17px Microsoft YaHei,sans-serif">零值插入、低通滤波与周期采样链</text>
<path d="M75 105H190" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#mr-arrow)"/>
<rect x="190" y="71" width="164" height="68" rx="7" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M354 105H460" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#mr-arrow)"/>
<rect x="460" y="71" width="164" height="68" rx="7" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M624 105H730" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#mr-arrow)"/>
<rect x="730" y="71" width="120" height="68" rx="7" fill="#fff" stroke="#0d8794" stroke-width="2"/>
<path d="M850 105H910" fill="none" stroke="#174b73" stroke-width="2.4" marker-end="url(#mr-arrow)"/>
<text x="272" y="113" text-anchor="middle" fill="#263746" style="font:17px Microsoft YaHei,sans-serif">零值插入</text><text x="790" y="113" text-anchor="middle" fill="#263746" style="font:17px Microsoft YaHei,sans-serif">采样</text>
{_math(33,66,92,'x[n]')}{_math(366,66,76,'g[n]')}{_math(490,84,104,'H(e^{j\\omega})')}{_math(638,66,76,'\\omega[n]')}{_math(864,66,76,'y[n]')}
<text x="480" y="205" text-anchor="middle" fill="#315d7c" style="font:17px Microsoft YaHei,sans-serif">给定输入频谱</text>
<line x1="165" y1="408" x2="780" y2="408" stroke="#174b73" stroke-width="2" marker-end="url(#mr-arrow)"/><line x1="472" y1="450" x2="472" y2="250" stroke="#174b73" stroke-width="2" marker-end="url(#mr-arrow)"/>
<path d="M318 408L472 286L626 408" fill="none" stroke="#0d8794" stroke-width="3" stroke-linejoin="round"/>
<line x1="318" y1="408" x2="318" y2="420" stroke="#174b73" stroke-width="1.5"/><line x1="626" y1="408" x2="626" y2="420" stroke="#174b73" stroke-width="1.5"/><line x1="165" y1="408" x2="165" y2="420" stroke="#174b73" stroke-width="1.5"/><line x1="780" y1="408" x2="780" y2="420" stroke="#174b73" stroke-width="1.5"/>
{_math(300,420,48,'-\\frac{\\pi}{2}')}{_math(608,420,48,'\\frac{\\pi}{2}')}{_math(145,420,42,'-\\pi')}{_math(760,420,42,'\\pi')}{_math(478,413,38,'0')}{_math(435,252,70,'X(e^{j\\omega})')}{_math(795,389,35,'\\omega')}{_math(447,267,42,'1')}
<text x="472" y="486" text-anchor="middle" fill="#52616b" style="font:14px Microsoft YaHei,sans-serif">三角谱的支撑区间为 −π/2 至 π/2</text>
</svg>'''


def _sampled_spectrum() -> str:
    centers = (190, 470, 750)
    triangles = "".join(
        f'<path d="M{center - 56} 305L{center} 238L{center + 56} 305" fill="none" stroke="#0d8794" stroke-width="3" stroke-linejoin="round"/>'
        for center in centers
    )
    return f'''<svg class="diagram" data-diagram="multirate-sampled-spectrum" viewBox="0 0 940 380" role="img" aria-label="周期采样后频谱复制示意图">
<defs><marker id="mr-spectrum-arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0L9,4.5L0,9Z" fill="#174b73"/></marker></defs>
<text x="470" y="28" text-anchor="middle" fill="#263746" style="font:17px Microsoft YaHei,sans-serif">周期采样后的频谱复制</text>
<line x1="72" y1="305" x2="862" y2="305" stroke="#174b73" stroke-width="2" marker-end="url(#mr-spectrum-arrow)"/><line x1="470" y1="338" x2="470" y2="88" stroke="#174b73" stroke-width="2" marker-end="url(#mr-spectrum-arrow)"/>
{triangles}
<line x1="414" y1="305" x2="414" y2="317" stroke="#174b73" stroke-width="1.5"/><line x1="526" y1="305" x2="526" y2="317" stroke="#174b73" stroke-width="1.5"/>
{_math(390,316,54,'-\\frac{\\pi}{6}')}{_math(502,316,54,'\\frac{\\pi}{6}')}{_math(440,316,58,'0')}{_math(126,316,128,'-\\frac{2\\pi}{3}')}{_math(686,316,128,'\\frac{2\\pi}{3}')}{_math(842,284,38,'\\omega')}{_math(482,93,80,'Y(e^{j\\omega})')}
<text x="470" y="365" text-anchor="middle" fill="#52616b" style="font:14px Microsoft YaHei,sans-serif">每个副本的幅度为滤波后中心谱的 1/3</text>
</svg>'''


def write_training_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="exam-page"><h1>第八章 分章强化训练</h1>
<div class="exam-head"><span>2013 年真题</span><span>详解见 P.____</span></div>
<p>九、已知某 (x[n]) 的频谱函数 (X(e^{j\omega})) 如图所示，零点插入系统在每个 (x[n]) 值之间插入一个零值，数字理想低通滤波器 (H(e^{j\omega})) 的截止频率 (omega_m=\frac{\pi}{6})，相位为零相位，对 (omega[n]) 进行周期 (N=3) 的采样后得到 (y[n])，请画出 (y[n]) 的频谱 (Y(e^{j\omega}))，其中</p>
<div class="formula">\[
\omega[n]=
\begin{cases}
g[n],&n=0,\pm3,\pm6,\pm9,\ldots,\\
0,&n=\text{其余}.
\end{cases}
\]</div>
""" + _multirate_chain() + r"""<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2015 年真题</span><span>详解见 P.____</span></div>
<p>八、已知某 (x[n]) 的频谱函数 (X(e^{j\omega})) 如图所示，零点插入系统在每个 (x[n]) 值之间插入一个零值，数字理想低通滤波器 (H(e^{j\omega})) 的截止频率 (omega_m=\frac{\pi}{6})，相位为零相位，对 (omega[n]) 进行周期 (N=3) 的采样后得到 (y[n])，请画出 (y[n]) 的频谱 (Y(e^{j\omega}))，其中</p>
<div class="formula">\[
\omega[n]=
\begin{cases}
g[n],&n=0,\pm3,\pm6,\pm9,\ldots,\\
0,&n=\text{其余}.
\end{cases}
\]</div>
""" + _multirate_chain() + r"""<div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2016 年真题</span><span>详解见 P.____</span></div>
<p>2.说明时分复用工作原理并举例。</p><div class="writing-space"></div></section>
<section class="exam-page"><div class="exam-head"><span>2020 年真题</span><span>详解见 P.____</span></div>
<p>3.什么是多路复用。</p><div class="writing-space"></div></section>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main><h1>真题整理详解</h1>
<h2>2013 年真题</h2>
<p>九、已知某 (x[n]) 的频谱函数 (X(e^{j\omega})) 如图所示，零点插入系统在每个 (x[n]) 值之间插入一个零值，数字理想低通滤波器 (H(e^{j\omega})) 的截止频率 (omega_m=\frac{\pi}{6})，相位为零相位，对 (omega[n]) 进行周期 (N=3) 的采样后得到 (y[n])，请画出 (y[n]) 的频谱 (Y(e^{j\omega}))。</p>
<div class="answer-step"><strong>第 1 步：零值插入。</strong>每两个相邻样值之间插入一个零值，插值倍率为 (L=2)。因此频谱沿频率轴压缩为原来的 (1/2)：</div>
<div class="formula">\[
G(e^{j\omega})=X(e^{j2\omega}).
\]</div>
<p>原三角谱的非零范围由 ([ -\pi/2,\pi/2 ]) 收缩为 ([ -\pi/4,\pi/4 ])，并以 (2\pi) 为周期重复。</p>
<div class="answer-step"><strong>第 2 步：理想低通。</strong>零相位低通只保留 (|\omega|\le\pi/6) 的中心部分，故令滤波后的序列为 (v[n])，则</div>
<div class="formula">\[
V(e^{j\omega})=G(e^{j\omega})H(e^{j\omega}),\qquad
V(e^{j\omega})\ne0\ \text{仅当}\ \left|\omega\right|\le\frac{\pi}{6}.
\]</div>
<div class="answer-step"><strong>第 3 步：周期采样造成频域复制。</strong>(omega[n]) 每隔 (3) 个样本保留一个 (g[n]) 的样值，其余位置置零。这个周期掩码的 DFS 系数均为 (1/3)，所以：</div>
<div class="formula">\[
Y(e^{j\omega})=\frac{1}{3}\sum_{r=0}^{2}V\!\left(e^{j\left(\omega-\frac{2\pi r}{3}\right)}\right).
\]</div>
<p>因此，输出在 (0)、(pm2\pi/3) 处各有一个宽度为 (pi/3) 的三角谱副本；每个副本的峰值为原图中心峰值的 (1/3)。</p>
""" + _sampled_spectrum() + r"""
<h2>2015 年真题</h2>
<p>八、已知某 (x[n]) 的频谱函数 (X(e^{j\omega})) 如图所示，零点插入系统在每个 (x[n]) 值之间插入一个零值，数字理想低通滤波器 (H(e^{j\omega})) 的截止频率 (omega_m=\frac{\pi}{6})，相位为零相位，对 (omega[n]) 进行周期 (N=3) 的采样后得到 (y[n])，请画出 (y[n]) 的频谱 (Y(e^{j\omega}))。</p>
<p><strong>解：</strong>本题的处理链与上一题完全相同。零值插入使频谱写为 (G(e^{j\omega})=X(e^{j2\omega}))；截止频率为 (pi/6) 的零相位低通只保留中心三角谱 ([ -\pi/6,\pi/6 ])；周期 (N=3) 的采样使该中心谱以间隔 (2\pi/3) 复制，并整体乘以 (1/3)：</p>
<div class="formula">\[
Y(e^{j\omega})=\frac{1}{3}\sum_{r=0}^{2}V\!\left(e^{j\left(\omega-\frac{2\pi r}{3}\right)}\right).
\]</div>
<p>故答案图与上图一致：在 (-2\pi/3)、(0)、(2\pi/3) 处画出三个等宽三角谱，并标明每个峰值为 (1/3)。</p>
<h2>2016 年真题</h2>
<p>2.说明时分复用工作原理并举例。</p>
<div class="answer-step"><strong>原理。</strong>时分复用把同一条物理传输通道按时间划分为互不重叠的时隙。各路信号先在各自的采样时刻取样或缓存，再按既定顺序轮流占用通道发送；接收端以同步时钟和帧结构识别时隙，并将属于不同用户的样值分离、重建。各路在时域交错，而不是在同一时刻相加传输。</div>
<div class="answer-step"><strong>例子。</strong>PCM 电话系统可把多路语音分别抽样、编码，并在一帧内分配给不同用户固定时隙；接收端按相同帧同步依次取回各路码字。数字通信中的 TDM 总线也采用相同思想。</div>
<h2>2020 年真题</h2>
<p>3.什么是多路复用。</p>
<div class="answer-step"><strong>定义。</strong>多路复用是让多路彼此独立的信息源共享同一传输介质或系统资源的技术。发送端先按某个可区分维度把各路信号组合，接收端再依据同一规则分离，从而提高通道利用率。</div>
<div class="answer-step"><strong>常见方式。</strong>按时间区分是时分复用；按不同频带区分是频分复用；还可按码型、波长或空间资源区分。无论采用哪一种，关键都是各路占用的资源在设计上可分离，避免互相干扰。</div>
</main>
"""
    output.write_text(_document(content), encoding="utf-8")
    return output


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    print(write_training_html(root / "full" / "outputs" / "chapter_08_training_mathjax_component.html"))
    print(write_answers_html(root / "full" / "outputs" / "chapter_08_answers_mathjax_component.html"))
