"""Chapter-two z-transform foundations in a continuous MathJax document."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]

STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 23mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933;margin:0}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:16pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:17pt 0 7pt}.formula{background:#f4f7f8;border-radius:5pt;padding:10pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.diagram{display:block;width:100%;height:auto;margin:12pt 0;break-inside:avoid}.axis{fill:none;stroke:#174b73;stroke-width:2}.circle{fill:none;stroke:#0f8b8d;stroke-width:2}.guide{fill:none;stroke:#b56b2e;stroke-width:1.5;stroke-dasharray:6 4}.label{fill:#374c5b;font:17px "Microsoft YaHei",sans-serif}.math foreignObject div{height:100%;display:flex;align-items:center;justify-content:center;font-size:17px;color:#172b3a}</style>"""


def z_plane_svg() -> str:
    """Programmatic s-plane/z-plane mapping diagram with full coordinate axes."""
    return r"""<!-- z_plane_svg: coordinate geometry for the z-plane mapping -->
<svg class="diagram" viewBox="0 0 900 360" role="img" aria-label="s 平面与 z 平面的映射">
 <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path class="axis" d="M60 180H390" marker-end="url(#arrow)"/><path class="axis" d="M225 325V35" marker-end="url(#arrow)"/>
 <path class="guide" d="M120 65V295"/><text class="label" x="395" y="165">\(\sigma\)</text><text class="label" x="233" y="45">\(j\Omega\)</text>
 <text class="label" x="172" y="330">s 平面：\(\sigma=0\)</text>
 <path class="axis" d="M520 180H844" marker-end="url(#arrow)"/><path class="axis" d="M682 325V35" marker-end="url(#arrow)"/>
 <circle class="circle" cx="682" cy="180" r="106"/><text class="label" x="849" y="165">\(\operatorname{Re}\{z\}\)</text><text class="label" x="690" y="45">\(\operatorname{Im}\{z\}\)</text>
 <text class="label" x="580" y="330">z 平面：\(\left|z\right|=1\)</text>
 <g class="math"><foreignObject x="62" y="44" width="118" height="28"><div>\(\Omega+\frac{2\pi}{T}\)</div></foreignObject><foreignObject x="717" y="74" width="110" height="28"><div>\(e^{j\omega}\)</div></foreignObject></g>
</svg>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>2.1 z 变换的基本概念</h1>
<p>z 变换把离散时间序列表示为复变量 \(z\) 的函数，是分析离散 LSI 系统、收敛域、系统函数和频率响应的统一工具。本节建立定义、收敛域与反变换的基本规则。</p>
<h2>z 变换的由来与定义</h2>
<p>将连续时间拉普拉斯变换中的 \(s=\sigma+j\Omega\) 与采样间隔 \(T\) 联系起来，令 \(z=e^{sT}\)，连续系统的指数因子就转换为离散系统中的幂次因子。</p>
<div class="formula">\[z=e^{sT}=e^{\sigma T}e^{j\Omega T}\]</div>
<p>序列 \(x(n)\) 的双边 z 变换定义为：</p>
<div class="formula">\[X(z)=\sum_{n=-\infty}^{\infty}x(n)z^{-n}\]</div>
<p>只有该级数绝对收敛的 \(z\) 才属于收敛域（ROC）。离散 LSI 系统的单位脉冲响应为 \(h(n)\) 时，\(H(z)=\mathcal{Z}\{h(n)\}\) 称为系统函数，并满足 \(Y(z)=H(z)X(z)\)。</p>
<h2>s 平面与 z 平面的映射</h2>
<p>由定义可得 \(\left|z\right|=e^{\sigma T}\)、\(\arg z=\Omega T\)。因此 s 平面的竖直线映射为 z 平面的圆，虚轴 \(\sigma=0\) 映射为单位圆；频率相差 \(\frac{2\pi}{T}\) 的点映射到同一 z 平面位置，这正是离散时间频域周期性的几何来源。</p>
__Z_PLANE__
<p>对稳定的离散 LSI 系统，频率响应由单位圆上的取值给出：</p>
<div class="formula">\[H(e^{j\omega})=H(z)\big|_{z=e^{j\omega}},\qquad \omega=\Omega T\]</div>
<h2>收敛域与典型序列</h2>
<p>同一个代数式 \(X(z)\) 在不同 ROC 下可以对应不同的时间序列。因此求反变换或判断系统时，必须同时给出表达式与 ROC；ROC 内不能包含极点。</p>
<div class="formula">\[
\frac{1}{1-az^{-1}}
\quad\Longleftrightarrow\quad
\begin{cases}
a^n u(n), & \left|z\right|>\left|a\right|,\\
-a^n u(-n-1), & \left|z\right|<\left|a\right|.
\end{cases}
\]</div>
<p>右边序列的 ROC 位于最外极点之外；左边序列的 ROC 位于最内极点之内；双边序列的 ROC 是两个极点圆之间的环域。有限长序列的 ROC 通常覆盖全部有限 z 平面，是否包含零点或无穷远点取决于其时间支持范围。</p>
<h2>z 反变换与判定顺序</h2>
<p>由 \(X(z)\) 求 \(x(n)\) 称为 z 反变换。本质上是根据 ROC 把 \(X(z)\) 展开成合适方向的幂级数，再读取 \(z^{-n}\) 的系数。常用方法包括围线积分、部分分式展开和幂级数展开。</p>
<div class="formula">\[x(n)=\frac{1}{2\pi j}\oint_C X(z)z^{n-1}\,\mathrm{d}z\]</div>
<p>对有理型 \(X(z)\)，先找有限极点；再由右边、左边或双边性质确定 ROC；最后检查单位圆是否在 ROC 内，以判断稳定性与频率响应是否存在。若 ROC 位于最外极点之外，按 \(z^{-1}\) 的降幂展开；若 ROC 位于最内极点之内，按 \(z\) 的升幂展开。</p>
<h2>例题：同一代数式与不同收敛域</h2>
<p>设 \(X(z)=\frac{1}{1-az^{-1}}\)。当 \(\left|z\right|>\left|a\right|\) 时，按 \(z^{-1}\) 的降幂展开，得到 \(x(n)=a^n u(n)\)；当 \(\left|z\right|<\left|a\right|\) 时，按 \(z\) 的升幂展开，得到 \(x(n)=-a^n u(-n-1)\)。代数式相同而 ROC 不同，时间支持范围也不同。</p>
<div class="formula">\[x(n)=\delta(n)\quad\Longrightarrow\quad X(z)=1,\qquad \text{ROC：全 z 平面}\]</div>
</main>""".replace("__Z_PLANE__", z_plane_svg())
    output.write_text(f'<!doctype html><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}', encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full/outputs/chapter_02_foundations_mathjax_component.pdf"))
