"""Second verified batch of chapter-two supplemental exam questions and answers."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}.indent{padding-left:1.7em;text-indent:-1.7em}.system-svg,.spectrum-svg{display:block;width:min(100%,470pt);height:auto;margin:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}.wire{fill:none;stroke:#174b73;stroke-width:2}.feedback{fill:none;stroke:#0f8b8d;stroke-width:2}.sum{fill:#fff;stroke:#174b73;stroke-width:2}.delay{fill:#f4f7f8;stroke:#0f8b8d;stroke-width:2}.svg-text{fill:#315d7c;font:15px "Microsoft YaHei",sans-serif}.svg-small{fill:#52616b;font:13px "Microsoft YaHei",sans-serif}.axis{fill:none;stroke:#174b73;stroke-width:2}.pass{fill:none;stroke:#0f8b8d;stroke-width:3}.stop{fill:#fbf2e8;stroke:#b56b2e;stroke-width:1.4;stroke-dasharray:5 4}</style>"""


def system_svg() -> str:
    """A watermark-free vector redraw of the 2004 two-delay system."""
    return """<svg class="system-svg" viewBox="0 0 760 350" role="img" aria-label="两级延时离散系统结构图">
<defs><marker id="arrow-b2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker><marker id="arrow-feedback-b2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#0f8b8d"/></marker></defs>
<text x="35" y="155" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">输入</text><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b2)" d="M75 150H157"/>
<circle fill="white" stroke="#174b73" stroke-width="2" cx="180" cy="150" r="23"/><text x="171" y="157" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">Σ</text>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b2)" d="M203 150H390"/>
<circle fill="white" stroke="#174b73" stroke-width="2" cx="420" cy="150" r="23"/><text x="411" y="157" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">Σ</text><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-b2)" d="M443 150H680"/><text x="688" y="155" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">输出</text>
<path fill="none" stroke="#174b73" stroke-width="2" d="M300 150V235H350" marker-end="url(#arrow-b2)"/><rect fill="#f4f7f8" stroke="#0f8b8d" stroke-width="2" x="352" y="211" width="95" height="48" rx="5"/><text x="372" y="241" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">延时</text>
<path fill="none" stroke="#174b73" stroke-width="2" d="M447 235H500" marker-end="url(#arrow-b2)"/><rect fill="#f4f7f8" stroke="#0f8b8d" stroke-width="2" x="502" y="211" width="95" height="48" rx="5"/><text x="522" y="241" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">延时</text>
<path fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-feedback-b2)" d="M447 235V305H130V173H157"/><path fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-feedback-b2)" d="M447 235V184H420"/><path fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-feedback-b2)" d="M597 235V322H95V170H157"/>
<text x="187" y="296" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">反馈二</text><text x="455" y="197" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">反馈一</text><text x="39" y="338" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">主信号流从左至右；两块均为一拍延时。</text>
</svg>"""


def bandstop_svg() -> str:
    """A textbook sketch whose exact cutoffs are stated by surrounding MathJax."""
    return """<svg class="spectrum-svg" viewBox="0 0 760 290" role="img" aria-label="理想带阻滤波器幅度频谱">
<defs><marker id="arrow-spectrum-b2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-spectrum-b2)" d="M65 225H710"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-spectrum-b2)" d="M385 245V40"/>
<path fill="none" stroke="#0f8b8d" stroke-width="3" d="M85 85H230V225H290"/><path fill="none" stroke="#0f8b8d" stroke-width="3" d="M480 225H540V85H690"/>
<rect fill="#fbf2e8" stroke="#b56b2e" stroke-width="1.4" stroke-dasharray="5 4" x="290" y="85" width="190" height="140"/><text x="350" y="155" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">阻带</text><text x="122" y="70" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">通带</text><text x="570" y="70" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">通带</text><text x="394" y="270" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">数字频率</text><text x="398" y="77" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">幅度</text><text x="72" y="246" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">负频率</text><text x="650" y="246" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">正频率</text>
</svg>"""


def stable_roc_svg() -> str:
    """Zero-pole plane for the stable realization of the 2004 system."""
    return """<svg class="system-svg" viewBox="0 0 760 330" role="img" aria-label="稳定收敛域零极点图">
<defs><marker id="arrow-roc-b2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<circle cx="385" cy="165" r="140" fill="#e8f3f2" opacity="0.78"/><circle cx="385" cy="165" r="46" fill="white"/><circle cx="385" cy="165" r="140" fill="none" stroke="#0f8b8d" stroke-width="2" stroke-dasharray="7 5"/><circle cx="385" cy="165" r="46" fill="none" stroke="#0f8b8d" stroke-width="2" stroke-dasharray="7 5"/><circle cx="385" cy="165" r="92" fill="none" stroke="#8797a3" stroke-width="1.5" stroke-dasharray="5 4"/>
<path fill="none" stroke="#174b73" stroke-width="1.7" marker-end="url(#arrow-roc-b2)" d="M90 165H690"/><path fill="none" stroke="#174b73" stroke-width="1.7" marker-end="url(#arrow-roc-b2)" d="M385 292V34"/>
<circle fill="white" stroke="#0f8b8d" stroke-width="3" cx="477" cy="165" r="7"/><path fill="none" stroke="#b56b2e" stroke-width="3" d="M425 159l12 12m0-12l-12 12M241 159l12 12m0-12l-12 12"/>
<text x="696" y="172" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">实部</text><text x="393" y="42" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="15">虚部</text><text x="393" y="184" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="13">原点</text><text x="486" y="151" fill="#0f8b8d" font-family="Microsoft YaHei, sans-serif" font-size="13">零点</text><text x="417" y="194" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="13">极点</text><text x="196" y="151" fill="#b56b2e" font-family="Microsoft YaHei, sans-serif" font-size="13">极点</text><text x="467" y="84" fill="#0f8b8d" font-family="Microsoft YaHei, sans-serif" font-size="14">稳定收敛域</text><text x="467" y="104" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">阴影环带</text><text x="470" y="183" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="12">单位圆</text>
</svg>"""


def training_html() -> str:
    return (
        r'''<section class="exam-page"><h1>第二章 补充真题（续）</h1>
<div class="exam-head"><span>2004 年真题</span><span>详解见 P.____</span></div>
<p>五、已知某离散系统方框图如下：求</p>
<figure>'''
        + system_svg()
        + r'''<figcaption>两个延时单元均表示 \(z^{-1}\)。第一条反馈支路的系数为 \(-1\)，第二条反馈支路的系数为 \(\frac{3}{4}\)。</figcaption></figure>
<p class="indent">（1）该系统的系统函数 \(H(z)\)；</p><p class="indent">（2）描述该系统的差分方程；</p><p class="indent">（3）分析该系统的因果、稳定性，画出零极点及收敛域；</p><p class="indent">（4）求系统稳定时的冲激响应。</p></section>
<section class="exam-page"><div class="exam-head"><span>2005 年真题</span><span>详解见 P.____</span></div>
<p>4. 求 \(F(z)=\frac{z^2}{z^2-2z-3}\) 在收敛域为 \(1<|z|<3\) 时的原序列 \(f(n)\)。</p></section>
<section class="exam-page"><div class="exam-head"><span>2005 年真题</span><span>详解见 P.____</span></div>
<p>十、对连续时间信号 \(x_a(t)\) 滤波，以除去 5kHz&lt;F&lt;10kHz 的频率成分，\(x_a(t)\) 中的最大频率是20kHz。滤波是通过采样 \(x_a(t)\)、滤波彩样信号，然后用一个理想 D/A 转换器重构模拟信号来完成的。求可用来避免混叠的最小采样频率，并对该最小采样频率求从 \(x_a(t)\) 中滤除 5kHz~10kHz 的理想带阻滤波器的 \(H(e^{j\omega})\) 的频率响应幅度频谱。</p></section>'''
    )


def answers_html() -> str:
    return (
        r'''<section><h1>真题整理详解（续）</h1><h2>2004 年真题：离散系统结构</h2>
<p>设第一个加法器的输出为 \(w[n]\)。由结构图逐节点列式，可得</p>
<div class="formula">\[w[n]=x[n]-w[n-1]+\frac{3}{4}w[n-2],\qquad y[n]=w[n]-w[n-1].\]</div>
<p>对上式作 \(z\) 变换并消去 \(W(z)\)，得到系统函数：</p>
<div class="formula">\[H(z)=\frac{Y(z)}{X(z)}=\frac{1-z^{-1}}{1+z^{-1}-\frac{3}{4}z^{-2}}=\frac{1-z^{-1}}{\left(1-\frac{1}{2}z^{-1}\right)\left(1+\frac{3}{2}z^{-1}\right)}.\]</div>
<p>因此，该系统的差分方程为</p><div class="formula">\[y[n]+y[n-1]-\frac{3}{4}y[n-2]=x[n]-x[n-1].\]</div>
<p>零点为 \(z=1\)，极点为 \(z=\frac{1}{2}\) 与 \(z=-\frac{3}{2}\)。图示实现是因果的，其收敛域为 \(|z|>\frac{3}{2}\)，故不稳定。若要求稳定，则收敛域必须夹住单位圆：</p>
<div class="formula">\[\frac{1}{2}<|z|<\frac{3}{2}.\]</div>
<figure>'''
        + stable_roc_svg()
        + r'''<figcaption>零点、极点和稳定收敛域如图所示；阴影环带对应 \(\frac{1}{2}<|z|<\frac{3}{2}\)。</figcaption></figure>
<p>在该稳定收敛域中，先作部分分式展开：</p>
<div class="formula">\[H(z)=-\frac{1}{4}\frac{1}{1-\frac{1}{2}z^{-1}}+\frac{5}{4}\frac{1}{1+\frac{3}{2}z^{-1}}.\]</div>
<p>第一个极点项取右边序列，第二个极点项取左边序列，故稳定时的冲激响应为</p>
<div class="formula">\[h[n]=-\frac{1}{4}\left(\frac{1}{2}\right)^n u[n]-\frac{5}{4}\left(-\frac{3}{2}\right)^n u[-n-1].\]</div></section>
<section><h2>2005 年真题：指定收敛域的反 \(z\) 变换</h2>
<p>先将系统函数化为 \(z^{-1}\) 的形式并展开：</p>
<div class="formula">\[F(z)=\frac{1}{(1-3z^{-1})(1+z^{-1})}=\frac{3}{4}\frac{1}{1-3z^{-1}}+\frac{1}{4}\frac{1}{1+z^{-1}}.\]</div>
<p>题设收敛域 \(1<|z|<3\) 表明极点 \(z=3\) 对应左边序列，而极点 \(z=-1\) 对应右边序列。因此</p>
<div class="formula">\[f[n]=\frac{1}{4}(-1)^n u[n]-\frac{3}{4}3^n u[-n-1].\]</div></section>
<section><h2>2005 年真题：采样、带阻滤波与重构</h2>
<p>为避免最高频率 \(20\,\mathrm{kHz}\) 的模拟信号混叠，最小采样频率为</p>
<div class="formula">\[f_s^{\min}=2\times20\,\mathrm{kHz}=40\,\mathrm{kHz}.\]</div>
<p>在 \(f_s=40\,\mathrm{kHz}\) 时，模拟频率与数字角频率满足 \(\omega=2\pi F/f_s\)，故 \(5\,\mathrm{kHz}\) 与 \(10\,\mathrm{kHz}\) 分别映射到 \(\pi/4\) 和 \(\pi/2\)。理想带阻滤波器的幅度频谱如下：</p>
<figure>'''
        + bandstop_svg()
        + r'''<figcaption>阻带及其负频率对称区间由下式精确定义。</figcaption></figure>
<div class="formula">\[\left|H(e^{j\omega})\right|=\begin{cases}1,&0\leq\left|\omega\right|<\frac{\pi}{4},\\0,&\frac{\pi}{4}\leq\left|\omega\right|\leq\frac{\pi}{2},\\1,&\frac{\pi}{2}<\left|\omega\right|\leq\pi.\end{cases}\]</div>
<p>边界点的取值不影响理想滤波器的频率选择结论；该带阻响应抑制 \(5\,\mathrm{kHz}\) 至 \(10\,\mathrm{kHz}\) 及其负频率对称分量。</p></section>'''
    )


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    completed = subprocess.run(
        [str(EDGE), "--headless=new", "--disable-gpu", "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri()],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout
