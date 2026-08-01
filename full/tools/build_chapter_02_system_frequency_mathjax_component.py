"""System function, frequency response and geometric reading in one MathJax flow."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:20mm 18mm 22mm}body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}main{max-width:174mm;margin:auto}
h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}h3{color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}p{margin:5pt 0 8pt}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}figure{margin:12pt auto;text-align:center}svg{width:min(100%,470pt);height:auto}figcaption{color:#315d7c;font-size:9.5pt;margin-top:4pt}@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>"""


def z_plane_svg() -> str:
    """A coordinate-driven geometric z-plane, with labels kept clear of data."""
    return r'''<figure><svg viewBox="0 0 540 286" role="img" aria-label="单位圆、零点、极点与频率点 B 的 z 平面示意图">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#234b6e"/></marker></defs>
<rect x="4" y="4" width="532" height="278" rx="6" fill="#fbfcfd" stroke="#d8e0e5"/>
<line x1="65" y1="144" x2="480" y2="144" stroke="#234b6e" stroke-width="1.5" marker-end="url(#arrow)"/>
<line x1="270" y1="242" x2="270" y2="39" stroke="#234b6e" stroke-width="1.5" marker-end="url(#arrow)"/>
<circle cx="270" cy="144" r="94" fill="none" stroke="#8aa5b5" stroke-width="1.4" stroke-dasharray="4 4"/>
<line x1="270" y1="144" x2="336" y2="78" stroke="#008e96" stroke-width="1.2" stroke-dasharray="4 3"/>
<line x1="336" y1="78" x2="350" y2="144" stroke="#b83a31" stroke-width="1.4"/>
<circle cx="270" cy="144" r="3" fill="#234b6e"/>
<circle cx="336" cy="78" r="4.5" fill="#008e96"/><text x="346" y="76" fill="#006d73" font-size="15" font-family="Microsoft YaHei">频率点 B</text>
<circle cx="394" cy="144" r="8" fill="none" stroke="#008e96" stroke-width="2.2"/><text x="406" y="164" fill="#006d73" font-size="15" font-family="Microsoft YaHei">零点 C</text>
<line x1="346" y1="140" x2="354" y2="148" stroke="#b83a31" stroke-width="2.3"/><line x1="354" y1="140" x2="346" y2="148" stroke="#b83a31" stroke-width="2.3"/><text x="358" y="130" fill="#9d302a" font-size="15" font-family="Microsoft YaHei">极点 D</text>
<text x="486" y="163" fill="#234b6e" font-size="15" font-family="Microsoft YaHei">实轴</text><text x="278" y="34" fill="#234b6e" font-size="15" font-family="Microsoft YaHei">虚轴</text><text x="278" y="162" fill="#234b6e" font-size="13" font-family="Microsoft YaHei">0</text><text x="300" y="57" fill="#54758a" font-size="14" font-family="Microsoft YaHei">单位圆</text>
<text x="346" y="112" fill="#b83a31" font-size="14" font-family="Microsoft YaHei">距离 |B−D|</text><text x="196" y="267" fill="#54758a" font-size="13" font-family="Microsoft YaHei">单位圆上的位置随频率转动</text>
</svg><figcaption>单位圆上的频率点与零、极点的距离决定幅度的峰谷</figcaption></figure>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r'''
<main>
<h1>系统函数及其与系统性质的关系</h1>
<p>对零状态 LSI 系统，输出是输入与单位脉冲响应的卷积；在 z 域中卷积化为乘法。因此系统函数定义为：</p>
<div class="formula">\[H(z)=\frac{Y(z)}{X(z)}=\mathcal{Z}\{h(n)\}\]</div>
<p>系统函数的收敛域与 [[h(n)]] 的收敛域相同。因果系统的收敛域在最外极点之外；稳定系统要求单位圆落在收敛域中。因而，因果有理系统稳定的充要条件是全部极点严格位于单位圆内。</p>
<h2>例题：由差分方程求系统函数</h2>
<p><strong>例题</strong>：已知因果 LSI 系统满足 [[y(n)+0.2y(n-1)-0.24y(n-2)=x(n)+x(n-1)]]，求系统函数、收敛域、稳定性和单位脉冲响应。</p>
<h3>解</h3>
<p>零状态 z 变换给出：</p>
<div class="formula">\[H(z)=\frac{1+z^{-1}}{1+0.2z^{-1}-0.24z^{-2}}=\frac{1+z^{-1}}{(1-0.4z^{-1})(1+0.6z^{-1})}\]</div>
<p>因系统因果，收敛域为 [[|z|&gt;0.6]]；单位圆在该区域内，因此系统稳定。部分分式展开后：</p>
<div class="formula">\[h(n)=\left(\frac{7}{5}\,0.4^n-\frac{2}{5}(-0.6)^n\right)u(n)\]</div>
<h1>系统频率响应的意义</h1>
<p>频率响应是单位脉冲响应的 DTFT，也是系统函数在单位圆上的取值：</p>
<div class="formula">\[H(e^{j\omega})=\sum_{n=-\infty}^{\infty}h(n)e^{-j\omega n}=H(z)\big|_{z=e^{j\omega}}\]</div>
<p>它由幅频响应与相频响应共同构成：</p>
<div class="formula">\[H(e^{j\omega})=\left|H(e^{j\omega})\right|e^{j\angle H(e^{j\omega})}\]</div>
<p>若输入为复指数 [[x(n)=e^{j\omega_0n}]]，输出仍为同频率复指数：</p>
<div class="formula">\[y(n)=H(e^{j\omega_0})e^{j\omega_0n}\]</div>
<p>对实正弦输入 [[x(n)=A\cos(\omega_0n+\varphi)]]，频率不变；输出幅度乘以 [[|H(e^{j\omega_0})|]]，相位增加 [[\angle H(e^{j\omega_0})]]。纯延时 [[n_d]] 个样本只改变相位：</p>
<div class="formula">\[H(e^{j\omega})=e^{-j\omega n_d},\qquad \left|H(e^{j\omega})\right|=1,\quad \angle H(e^{j\omega})=-\omega n_d\]</div>
<h2>三点平均系统</h2>
<p>对 [[y(n)=\frac{x(n)+x(n-1)+x(n-2)}{3}]]，频率响应为：</p>
<div class="formula">\[H(e^{j\omega})=\frac{1+e^{-j\omega}+e^{-j2\omega}}{3}\]</div>
<p>在 [[\omega=\frac{2\pi}{3}]] 处，三个相量之和为零，故该频率被完全抑制；低频附近幅度较大，说明它具有平滑、抑制高频干扰的低通特性。</p>
<h1>几何法画频率响应</h1>
<p>设系统函数的零点为 [[c_r]]、极点为 [[d_r]]，增益为 [[A]]。令单位圆上的频率点 [[B=e^{j\omega}]] 随 [[\omega]] 转动，则零极点分解给出：</p>
<div class="formula">\[H(z)=A\frac{\prod_r(z-c_r)}{\prod_r(z-d_r)}\]</div>
<div class="formula">\[\left|H(e^{j\omega})\right|=\left|A\right|\frac{\prod_r\left|B-C_r\right|}{\prod_r\left|B-D_r\right|},\qquad B=e^{j\omega}\]</div>
<p>因此，频率点靠近极点时分母变小，幅度形成峰；靠近零点时分子变小，幅度形成谷。单位圆上的零点对应完全抑制的频率；单位圆上的极点会导致不稳定，故稳定系统的极点不能在单位圆上。</p>
__Z_PLANE__
<h2>一阶系统与梳状零点</h2>
<p>对 [[y(n)=by(n-1)+x(n)]]（[[0&lt;b&lt;1]]），有：</p>
<div class="formula">\[H(z)=\frac{1}{1-bz^{-1}},\qquad \left|H(e^{j\omega})\right|=\frac{1}{\left|e^{j\omega}-b\right|}\]</div>
<p>极点位于正实轴且在单位圆内；当 [[\omega=0]] 时频率点最接近极点，幅度最大；当 [[\omega=\pi]] 时距离最大，幅度最小，故为低通特性。</p>
<p>对 [[H(z)=1-z^{-N}]]，单位圆上有 [[N]] 个等角度零点，频响为：</p>
<div class="formula">\[\left|H(e^{j\omega})\right|=\left|1-e^{-jN\omega}\right|=2\left|\sin\frac{N\omega}{2}\right|\]</div>
<p>零点出现在 [[\omega=2\pi k/N]]，因而形成等间隔衰减槽。读图时先让频率点沿单位圆转动：靠极点找峰、靠零点找谷，再检查极点是否全在单位圆内。</p>
</main>'''.replace("[[", chr(92) + "(").replace("]]", chr(92) + ")").replace("__Z_PLANE__", z_plane_svg())
    document = f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'
    output.write_text(document, encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_02_system_frequency_mathjax_component.pdf"))
