"""Second-chapter priority exam training and detailed solutions, in MathJax HTML."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]

STYLE = r"""<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.exam-page{break-before:page;min-height:230mm}.exam-head{display:flex;justify-content:space-between;align-items:baseline;color:#52616b;margin:0 0 10pt}.answer h1{font-size:19pt}figure{break-inside:avoid;margin:12pt auto;text-align:center}figure > svg:not(.mathjax-svg){width:min(100%,500pt);height:auto}figcaption{color:#315d7c;font-size:9.5pt;margin-top:4pt}.indent{padding-left:1.7em;text-indent:-1.7em}
</style>"""


def _zero_pole_svg() -> str:
    return r'''<svg data-source-candidate-id="2015-q七-01" viewBox="0 0 540 290" role="img" aria-label="零极点图：原点零点、实轴 2 处极点与单位圆">
<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7z" fill="#234d70"/></marker></defs>
<line x1="68" y1="145" x2="470" y2="145" stroke="#234d70" stroke-width="1.4" marker-end="url(#arrow)"/><line x1="196" y1="236" x2="196" y2="46" stroke="#234d70" stroke-width="1.4" marker-end="url(#arrow)"/>
<circle cx="196" cy="145" r="75" fill="none" stroke="#7d8d98" stroke-width="1.15" stroke-dasharray="4 3"/><circle cx="196" cy="145" r="6" fill="white" stroke="#0e7490" stroke-width="2"/><path d="M326 136l18 18m0-18l-18 18" stroke="#b56b2e" stroke-width="2.5"/>
<path d="M137 67L151 80" fill="none" stroke="#7d8d98" stroke-width="1"/>
<text x="476" y="151" font-size="16" fill="#1f2933">Re(z)</text><text x="196" y="34" text-anchor="middle" font-size="16" fill="#1f2933">Im(z)</text><text x="205" y="166" font-size="14" fill="#52616b">0</text><text x="264" y="166" font-size="14" fill="#52616b">1</text><text x="333" y="166" font-size="14" fill="#52616b">2</text><text x="103" y="62" font-size="13" fill="#52616b">单位圆</text><text x="354" y="129" font-size="13" fill="#b56b2e">极点</text><text x="142" y="131" font-size="13" fill="#0e7490">零点</text>
</svg>'''


def _math_label(x: float, y: float, width: float, height: float, latex: str, *, size: int = 16) -> str:
    """Put one complete MathJax expression into an SVG label region."""
    return (
        f'<foreignObject x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}">'
        '<div xmlns="http://www.w3.org/1999/xhtml" '
        f'style="height:100%;display:flex;align-items:center;justify-content:center;font-size:{size}px">'
        f'\\({latex}\\)</div></foreignObject>'
    )


def _am_svg() -> str:
    """Rebuild the three source diagrams without watermark or text-formula hacks."""
    spectrum = (
        '<path data-role="input-periodic-spectrum" fill="none" stroke="#0f8b8d" '
        'stroke-width="3" stroke-linejoin="round" d="M92 356L132 276L172 356 '
        'M260 356L340 276L420 356 '
        'M508 356L548 276L588 356"/>'
    )
    return r'''<svg class="diagram" data-source-candidate-id="2021-q六-01" viewBox="0 0 680 700" role="img" aria-label="2021 年 AM 调制题的调制框图、输入周期谱与相干解调框图">
<defs><marker id="arrow-am-source" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<text x="52" y="42" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="18">(a) 正弦调制</text>
<path data-role="am-modulator" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-source)" d="M95 96H282"/><circle cx="310" cy="96" r="28" fill="#fff" stroke="#174b73" stroke-width="2"/><path d="M294 80l32 32m0-32l-32 32" fill="none" stroke="#b56b2e" stroke-width="2.4"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-source)" d="M338 96H548"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-source)" d="M310 176V126"/>
''' + _math_label(72, 55, 80, 34, r'x(n)', size=18) + _math_label(528, 55, 84, 34, r'y(n)', size=18) + _math_label(208, 174, 205, 36, r'\cos(\omega_cn)', size=17) + r'''
<text x="52" y="246" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="18">(b) 输入信号的周期频谱</text>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-source)" d="M70 356H625"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-source)" d="M340 382V265"/>
''' + spectrum + _math_label(343, 262, 116, 34, r'X(e^{j\omega})', size=17) + _math_label(315, 278, 42, 31, '1', size=15) + _math_label(92, 361, 80, 33, r'-2\pi', size=15) + _math_label(346, 361, 40, 33, r'0', size=15) + _math_label(508, 361, 80, 33, r'2\pi', size=15) + _math_label(210, 361, 100, 33, r'-\omega_0', size=15) + _math_label(370, 361, 100, 33, r'\omega_0', size=15) + _math_label(606, 337, 45, 34, r'\omega', size=18) + r'''
<text x="52" y="470" fill="#315d7c" font-family="Microsoft YaHei, sans-serif" font-size="18">(c) 相干解调与低通恢复</text>
<path data-role="coherent-demodulator" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-source)" d="M95 528H232"/><circle cx="260" cy="528" r="28" fill="#fff" stroke="#174b73" stroke-width="2"/><path d="M244 512l32 32m0-32l-32 32" fill="none" stroke="#b56b2e" stroke-width="2.4"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-source)" d="M288 528H358"/><rect x="365" y="489" width="148" height="78" rx="5" fill="#fff" stroke="#174b73" stroke-width="2"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-source)" d="M513 528H594"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-source)" d="M260 620V558"/>
''' + _math_label(75, 488, 85, 34, r'y(n)', size=18) + _math_label(536, 488, 95, 34, r'\hat{x}(n)', size=18) + _math_label(377, 508, 126, 38, r'H(e^{j\omega})', size=18) + _math_label(135, 619, 250, 40, r'\cos(\omega_cn+\theta_c)', size=17) + r'''</svg>'''


def _am_output_spectrum_svg() -> str:
    """Draw the modulated DTFT from the two exact frequency-shift copies."""
    return r'''<svg class="diagram" data-source-candidate-id="2021-q六-01" style="width:min(100%,470pt)" viewBox="0 0 720 390" role="img" aria-label="2021 年 AM 调制后 Y(e^{jω}) 的频谱图">
<defs><marker id="arrow-am-output" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#174b73"/></marker></defs>
<path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-output)" d="M72 286H662"/><path fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#arrow-am-output)" d="M367 314V58"/>
<path data-role="am-output-spectrum" fill="none" stroke="#0f8b8d" stroke-width="3" stroke-linejoin="round" d="M132 286L196 128L260 286 M474 286L538 128L602 286"/>
<path data-role="shifted-copy-minus" fill="none" stroke="#b56b2e" stroke-width="1.4" stroke-dasharray="5 4" d="M196 286V128"/><path data-role="shifted-copy-plus" fill="none" stroke="#b56b2e" stroke-width="1.4" stroke-dasharray="5 4" d="M538 286V128"/>
''' + _math_label(374, 49, 120, 36, r'Y(e^{j\omega})', size=18) + _math_label(343, 107, 42, 32, r'\frac12', size=15) + _math_label(508, 107, 42, 32, r'\frac12', size=15) + _math_label(124, 296, 100, 32, r'-\omega_c-\omega_0', size=14) + _math_label(232, 296, 100, 32, r'-\omega_c+\omega_0', size=14) + _math_label(302, 296, 110, 32, r'0', size=15) + _math_label(450, 296, 100, 32, r'\omega_c-\omega_0', size=14) + _math_label(560, 296, 100, 32, r'\omega_c+\omega_0', size=14) + _math_label(647, 263, 48, 34, r'\omega', size=18) + r'''<text x="73" y="353" fill="#52616b" font-family="Microsoft YaHei, sans-serif" font-size="14">两个幅度缩小为原谱一半的搬移副本</text></svg>'''


def training_html() -> str:
    return rf'''<section class="exam-page"><h1>第二章 分章强化训练</h1>
<div class="exam-head"><span>2015 年真题</span><span>详解见 P.18</span></div>
<p>七、离散因果 LTI 系统的系统函数 \(H(z)\) 的零极点图如图所示，其中 \(h[0]=2\)。</p>
<p class="indent">（1）求系统函数 \(H(z)\) 及收敛域；</p><p class="indent">（2）判断是否稳定；</p><p class="indent">（3）求单位脉冲响应 \(h(n)\)；</p><p class="indent">（4）求出系统的差分方程。</p><figure>{_zero_pole_svg()}<figcaption>零极点图</figcaption></figure></section>
<section class="exam-page"><div class="exam-head"><span>2021 年真题</span><span>详解见 P.18</span></div>
<p>六、（AM 调制）已知离散时间信号 \(x(n)\)，其傅里叶变换 \(X(e^{{j\omega}})\) 如图（a）所示，该信号被一个正弦序列调制，如图（b）所示：</p>
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
<p>因此 \(Y(e^{j\omega})\) 是原谱的两份、各缩小为一半的副本，分别移到 \(+\omega_c\) 与 \(-\omega_c\) 附近，并以 \(2\pi\) 为周期重复。</p><figure>''' + _am_output_spectrum_svg() + r'''<figcaption>调制后的两个谱副本：中心频率为 \(\pm\omega_c\)，每份幅度为原谱的 \(1/2\)。</figcaption></figure><p>解调相乘后有</p><div class="formula">\[y(n)\cos(\omega_cn+\theta_c)=\frac{\cos\theta_c}{2}x(n)+\frac12x(n)\cos(2\omega_cn+\theta_c).\]</div>
<p>低通滤波器只保留第一项，故 \(\hat x(n)=\frac{G\cos\theta_c}{2}x(n)\)。只要 \(\cos\theta_c\ne0\)，应取</p><div class="formula">\[G=\frac{2}{\cos\theta_c}.\]</div>
<p>设原谱的主值支撑为 \(|\omega|\leq\omega_0\)。为使调制后的两个谱副本不重叠，必须有 \(\omega_0<\omega_c<\pi-\omega_0\)。解调后的高频副本中心位于 \(\pm2\omega_c\)（按 \(2\pi\) 周期折返），故低通滤波器还必须在保留基带的同时排除两侧副本：</p><div class="formula">\[\omega_0<\omega_{cp}<\min\!\left\{2\omega_c-\omega_0,\;2\pi-2\omega_c-\omega_0\right\}.\]</div></section>
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


def rendered_dom(html: Path) -> str:
    """Return this component after MathJax has typeset every formula."""
    profile = html.parent / "edge-profile"
    completed = subprocess.run(
        [
            str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={profile}",
            "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri(),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout


def assert_mathjax_ready(dom: str) -> None:
    if "<mjx-container" not in dom:
        raise RuntimeError("MathJax did not render the 2021 AM formulae")
    remaining = [token for token in (r"\(", r"\)", r"\[", r"\]") if token in dom]
    if remaining:
        raise RuntimeError("MathJax left raw formula delimiters: " + ", ".join(remaining))


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    assert_mathjax_ready(rendered_dom(html))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_02_training_mathjax_component.pdf"))
