"""Second-chapter priority exam training and detailed solutions, in MathJax HTML."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]

STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}.answer h1{font-size:19pt}figure{break-inside:avoid;margin:12pt auto;text-align:center}svg{width:min(100%,500pt);height:auto}figcaption{color:#315d7c;font-size:9.5pt;margin-top:4pt}.indent{padding-left:1.7em;text-indent:-1.7em}
</style>"""


def _zero_pole_svg() -> str:
    return r'''<svg viewBox="0 0 540 290" role="img" aria-label="零极点图：原点零点、实轴 2 处极点与单位圆">
<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7z" fill="#234d70"/></marker></defs>
<line x1="68" y1="145" x2="470" y2="145" stroke="#234d70" stroke-width="1.4" marker-end="url(#arrow)"/><line x1="196" y1="236" x2="196" y2="46" stroke="#234d70" stroke-width="1.4" marker-end="url(#arrow)"/>
<circle cx="196" cy="145" r="75" fill="none" stroke="#7d8d98" stroke-width="1.15" stroke-dasharray="4 3"/><circle cx="196" cy="145" r="6" fill="white" stroke="#0e7490" stroke-width="2"/><path d="M326 136l18 18m0-18l-18 18" stroke="#b56b2e" stroke-width="2.5"/>
<path d="M137 67L151 80" fill="none" stroke="#7d8d98" stroke-width="1"/>
<text x="476" y="151" font-size="16" fill="#1f2933">Re(z)</text><text x="196" y="34" text-anchor="middle" font-size="16" fill="#1f2933">Im(z)</text><text x="205" y="166" font-size="14" fill="#52616b">0</text><text x="264" y="166" font-size="14" fill="#52616b">1</text><text x="333" y="166" font-size="14" fill="#52616b">2</text><text x="103" y="62" font-size="13" fill="#52616b">单位圆</text><text x="354" y="129" font-size="13" fill="#b56b2e">极点</text><text x="142" y="131" font-size="13" fill="#0e7490">零点</text>
</svg>'''


def _am_svg() -> str:
    return r'''<svg viewBox="0 0 540 420" role="img" aria-label="离散时间正弦调制、频谱搬移和相干解调框图">
<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7z" fill="#234d70"/></marker></defs>
<text x="30" y="34" font-size="15" fill="#315d7c">(a) 正弦调制</text><line x1="54" y1="72" x2="176" y2="72" stroke="#234d70" stroke-width="1.4" marker-end="url(#arrow)"/><circle cx="201" cy="72" r="19" fill="white" stroke="#234d70" stroke-width="1.4"/><path d="M190 61l22 22m0-22l-22 22" stroke="#b56b2e" stroke-width="1.5"/><line x1="220" y1="72" x2="362" y2="72" stroke="#234d70" stroke-width="1.4" marker-end="url(#arrow)"/><line x1="201" y1="115" x2="201" y2="91" stroke="#234d70" stroke-width="1.2" marker-end="url(#arrow)"/><text x="53" y="63" font-size="15">x(n)</text><text x="335" y="63" font-size="15">y(n)</text><text x="143" y="132" font-size="14">cos(ω<tspan baseline-shift="sub" font-size="10">c</tspan>n)</text>
<text x="30" y="169" font-size="15" fill="#315d7c">(b) 频谱搬移</text><line x1="50" y1="267" x2="500" y2="267" stroke="#234d70" stroke-width="1.3" marker-end="url(#arrow)"/><line x1="275" y1="278" x2="275" y2="186" stroke="#234d70" stroke-width="1.3" marker-end="url(#arrow)"/><path d="M210 267 L243 205 L275 267 M275 267 L307 205 L340 267" fill="none" stroke="#0e8d93" stroke-width="2"/><path d="M50 267 L83 205 L115 267 M435 267 L467 205 L500 267" fill="none" stroke="#0e8d93" stroke-width="2"/><text x="276" y="195" font-size="14">Y(e<tspan baseline-shift="super" font-size="10">jω</tspan>)</text><text x="267" y="290" font-size="12">0</text><text x="205" y="290" font-size="12">−ω<tspan baseline-shift="sub" font-size="9">c</tspan></text><text x="328" y="290" font-size="12">ω<tspan baseline-shift="sub" font-size="9">c</tspan></text><text x="506" y="272" font-size="14">ω</text>
<text x="30" y="318" font-size="15" fill="#315d7c">(c) 相干解调与低通恢复</text><line x1="54" y1="356" x2="160" y2="356" stroke="#234d70" stroke-width="1.4" marker-end="url(#arrow)"/><circle cx="183" cy="356" r="19" fill="white" stroke="#234d70" stroke-width="1.4"/><path d="M172 345l22 22m0-22l-22 22" stroke="#b56b2e" stroke-width="1.5"/><line x1="202" y1="356" x2="264" y2="356" stroke="#234d70" stroke-width="1.4" marker-end="url(#arrow)"/><rect x="269" y="333" width="109" height="45" rx="3" fill="white" stroke="#234d70" stroke-width="1.4"/><line x1="378" y1="356" x2="470" y2="356" stroke="#234d70" stroke-width="1.4" marker-end="url(#arrow)"/><text x="52" y="347" font-size="14">y(n)</text><text x="289" y="362" font-size="15">H(e<tspan baseline-shift="super" font-size="10">jω</tspan>)</text><text x="439" y="347" font-size="14">x̂(n)</text><text x="118" y="398" font-size="12">cos(ω<tspan baseline-shift="sub" font-size="9">c</tspan>n+θ<tspan baseline-shift="sub" font-size="9">c</tspan>)</text>
</svg>'''


def training_html() -> str:
    return rf'''<section class="exam-page"><h1>第二章 分章强化训练</h1>
<div class="exam-head"><span>2015 年真题</span><span>详解见 P.18</span></div>
<p>七、离散因果 LTI 系统的系统函数 \(H(z)\) 的零极点图如图所示，其中 \(h[0]=2\)。</p>
<p class="indent">（1）求系统函数 \(H(z)\) 及收敛域；</p><p class="indent">（2）判断是否稳定；</p><p class="indent">（3）求单位脉冲响应 \(h(n)\)；</p><p class="indent">（4）求出系统的差分方程。</p><figure>{_zero_pole_svg()}<figcaption>零极点图</figcaption></figure></section>
<section class="exam-page"><div class="exam-head"><span>2021 年真题</span><span>详解见 P.18</span></div>
<p>六、（AM 调制）已知离散时间信号 \(x(n)\)，其傅里叶变换 \(X(e^{{j\omega}})\) 如图（b）所示，该信号被一个正弦序列调制，如图（a）所示：</p>
<figure>{_am_svg()}</figure><p class="indent">1．写出 \(y(n)\) 的傅里叶变换 \(Y(e^{{j\omega}})\)，并画出其频谱图；</p>
<p class="indent">2．图（c）是一个解调系统，其中 \(H(e^{{j\omega}})=\begin{{cases}}G,&|\omega|<\omega_{{cp}},\\0,&\text{{其他}}.\end{{cases}}\) 若使 \(\hat x(n)=x(n)\)，\(G\) 应取何值？</p>
<p class="indent">3．为保证从 \(y(n)\) 中恢复出 \(x(n)\)，\(\omega_c\) 和 \(\omega_{{cp}}\) 应满足什么关系？</p></section>
<section class="exam-page"><div class="exam-head"><span>2025 年真题</span><span>详解见 P.19</span></div>
<p>八、已知某因果稳定的 \(LSI\) 系统 \(S_1\) 的差分方程如下</p><div class="formula">\[y(n)=\frac{{1}}{{4}}[x(n)-x(n-1)+x(n+2)-x(n-3)]\]</div>
<p>假设系统函数为 \(H_1(z)\)，求系统的频谱响应为 \(H_1(e^{{j\omega}})\)，单位脉冲响应为 \(h_1(n)\)。</p>
<p class="indent">（1）设系统 \(S_1\) 的频率响应表达式为 \(H_1(e^{{j\omega}})=|H_1(e^{{j\omega}})|e^{{j\theta_1(\omega)}}\)，其中 \(|H_1(e^{{j\omega}})|\) 为振幅响应，\(\theta_1(\omega)\) 为相位响应，请写出 \(|H_1(e^{{j\omega}})|\) 和 \(\theta_1(\omega)\) 的表达式。</p>
<p class="indent">（2）假设有一个系统 \(S_2\)，该系统的频率响应为 \(H_2(e^{{j\omega}})\)，且有 \(H_2(e^{{j\omega}})=H_1(-e^{{j\omega}})\)，设系统 \(S_2\) 的频率响应同样可以表示为 \(H_2(e^{{j\omega}})=|H_2(e^{{j\omega}})|e^{{j\theta_2(\omega)}}\)，试写出单位脉冲响应 \(h_2(n)\)，以及 \(|H_2(e^{{j\omega}})|\) 和 \(\theta_2(\omega)\) 的表达式。</p>
<p class="indent">（3）试分析系统 \(S_1\) 和系统 \(S_2\) 的滤波特性。</p></section>'''


def answers_html() -> str:
    return r'''<section class="answer"><h1>真题整理详解</h1><h2>2015 年真题：零极点、收敛域与差分方程</h2>
<p>图中零点在原点，极点位于实轴 \(z=2\)。因此系统函数只能写成</p><div class="formula">\[H(z)=K\frac{z}{z-2}=\frac{K}{1-2z^{-1}}.\]</div>
<p>因系统因果，收敛域为极点外侧 \(|z|>2\)。又因 \(h[0]=2\)，将 \(H(z)\) 在 \(z^{-1}\) 的幂级数中展开，常数项就是 \(K\)，故 \(K=2\)。</p><div class="formula">\[H(z)=\frac{2}{1-2z^{-1}},\qquad \operatorname{ROC}:|z|>2.\]</div>
<p>于是</p><div class="formula">\[h(n)=2\cdot2^n u(n)=2^{n+1}u(n).\]</div><p>收敛域不包含单位圆，故系统不稳定。由 \((1-2z^{-1})Y(z)=2X(z)\) 直接得到差分方程：</p><div class="formula">\[y(n)-2y(n-1)=2x(n).\]</div></section>
<section class="answer"><h2>2021 年真题：调制、解调与恢复条件</h2><p>调制信号为 \(y(n)=x(n)\cos(\omega_cn)\)。利用余弦的指数展开与 DTFT 的频移性质，得到</p><div class="formula">\[Y(e^{j\omega})=\frac{1}{2}X\!\left(e^{j(\omega-\omega_c)}\right)+\frac{1}{2}X\!\left(e^{j(\omega+\omega_c)}\right).\]</div>
<p>因此 \(Y(e^{j\omega})\) 是原谱的两份、各缩小为一半的副本，分别移到 \(+\omega_c\) 与 \(-\omega_c\) 附近，并以 \(2\pi\) 为周期重复。</p><p>解调相乘后有</p><div class="formula">\[y(n)\cos(\omega_cn+\theta_c)=\frac{\cos\theta_c}{2}x(n)+\frac12x(n)\cos(2\omega_cn+\theta_c).\]</div>
<p>低通滤波器只保留第一项，故 \(\hat x(n)=\frac{G\cos\theta_c}{2}x(n)\)。只要 \(\cos\theta_c\ne0\)，应取</p><div class="formula">\[G=\frac{2}{\cos\theta_c}.\]</div>
<p>设原谱的主值支撑为 \(|\omega|\leq\omega_0\)。为使调制后的两个谱副本不重叠且解调时低通滤波器能隔离基带，需满足</p><div class="formula">\[\omega_0<\omega_c<\pi-\omega_0,\qquad \omega_0<\omega_{cp}<2\omega_c-\omega_0.\]</div></section>
<section class="answer"><h2>2025 年真题：频响、幅相特性与频移</h2><p>令输入为单位脉冲，即得</p><div class="formula">\[h_1(n)=\frac14[\delta(n)-\delta(n-1)+\delta(n+2)-\delta(n-3)].\]</div>
<p>代入 DTFT 定义：</p><div class="formula">\[\begin{aligned}H_1(e^{j\omega})&=\frac14\left(1-e^{-j\omega}+e^{j2\omega}-e^{-j3\omega}\right)\\&=j e^{-j\omega/2}\sin\!\left(\frac{3\omega}{2}\right)\cos\omega.\end{aligned}\]</div>
<p>因此</p><div class="formula">\[|H_1(e^{j\omega})|=\left|\sin\!\left(\frac{3\omega}{2}\right)\cos\omega\right|.\]</div>
<p>相位可由上式的 \(j e^{-j\omega/2}\) 与实因子符号共同确定；在实因子为正、负的区间分别取 \(\frac\pi2-\frac\omega2\) 与 \(-\frac\pi2-\frac\omega2\)（再按主值区间折返）。</p>
<p>由 \(H_2(e^{j\omega})=H_1(-e^{j\omega})=H_1(e^{j(\omega+\pi)})\)，可知时域为乘以 \((-1)^n\)：</p><div class="formula">\[h_2(n)=(-1)^nh_1(n)=\frac14[\delta(n)+\delta(n-1)+\delta(n+2)+\delta(n-3)].\]</div>
<p>相应的幅度响应为</p><div class="formula">\[|H_2(e^{j\omega})|=\left|\cos\!\left(\frac{3\omega}{2}\right)\cos\omega\right|,\qquad \theta_2(\omega)=\theta_1(\omega+\pi).\]</div>
<p>系统 \(S_2\) 是 \(S_1\) 的 \(\pi\) 频移版本：\(S_1\) 的阻带零点位于 \(\omega=0,\ \pm\frac{2\pi}{3},\ \pm\frac\pi2\)；\(S_2\) 的对应零点整体平移 \(\pi\)。两者均表现为由多个零点形成的梳状抑制特性。</p></section>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}<main>{training_html()}{answers_html()}</main></html>'''
    output.write_text(document, encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_02_training_mathjax_component.pdf"))
