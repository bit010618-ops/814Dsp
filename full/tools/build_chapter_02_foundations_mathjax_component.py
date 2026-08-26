"""Chapter-two z-transform foundations in a continuous MathJax document."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]

STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 23mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933;margin:0}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:16pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:17pt 0 7pt}.formula{background:#f4f7f8;border-radius:5pt;padding:10pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.diagram{display:block;width:100%;height:auto;margin:12pt 0;break-inside:avoid}.axis{fill:none;stroke:#174b73;stroke-width:2}.circle{fill:none;stroke:#0f8b8d;stroke-width:2}.guide{fill:none;stroke:#b56b2e;stroke-width:1.5;stroke-dasharray:6 4}.label{fill:#374c5b;font:17px "Microsoft YaHei",sans-serif}.math foreignObject div{height:100%;display:flex;align-items:center;justify-content:center;font-size:17px;color:#172b3a}</style>"""


def z_plane_svg() -> str:
    """Textbook mapping from the s-plane imaginary axis to the unit circle.

    Every visual attribute is inline.  The chapter assembler keeps component
    bodies but not their local stylesheets, so CSS-class-dependent SVGs would
    silently fall back to SVG's black-fill defaults in the final handout.
    """
    return r"""<!-- z_plane_svg: explicit coordinate geometry for the s-to-z mapping -->
<svg class="diagram" viewBox="0 0 920 390" role="img" aria-label="s 平面虚轴映射到 z 平面单位圆，频率相差二π除以T的点重合">
 <defs>
  <marker id="s-z-arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0L9 4.5L0 9Z" fill="#174b73"/></marker>
 </defs>
 <rect x="18" y="18" width="390" height="344" rx="7" fill="#fbfcfd" stroke="#d8e0e5"/>
 <rect x="512" y="18" width="390" height="344" rx="7" fill="#fbfcfd" stroke="#d8e0e5"/>
 <text x="72" y="52" fill="#315d7c" font-size="18" font-family="Microsoft YaHei, sans-serif">s 平面</text>
 <path d="M72 205H356" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#s-z-arrow)"/>
 <path d="M214 326V72" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#s-z-arrow)"/>
 <path d="M214 88V312" fill="none" stroke="#b56b2e" stroke-width="2" stroke-dasharray="7 5"/>
 <circle cx="214" cy="142" r="5" fill="#b56b2e"/><circle cx="214" cy="234" r="5" fill="#b56b2e"/>
 <path d="M214 142H128M214 234H128" fill="none" stroke="#b56b2e" stroke-width="1.2" stroke-dasharray="4 3"/>
 <foreignObject x="359" y="184" width="46" height="32"><div xmlns="http://www.w3.org/1999/xhtml" style="font:17px serif;text-align:center">\(\sigma\)</div></foreignObject>
 <foreignObject x="224" y="54" width="52" height="31"><div xmlns="http://www.w3.org/1999/xhtml" style="font:17px serif">\(j\Omega\)</div></foreignObject>
 <foreignObject x="53" y="124" width="164" height="33"><div xmlns="http://www.w3.org/1999/xhtml" style="font:16px serif;text-align:right">\(\Omega+\frac{2\pi}{T}\)</div></foreignObject>
 <foreignObject x="118" y="218" width="88" height="31"><div xmlns="http://www.w3.org/1999/xhtml" style="font:16px serif;text-align:right">\(\Omega\)</div></foreignObject>
 <foreignObject x="143" y="330" width="143" height="32"><div xmlns="http://www.w3.org/1999/xhtml" style="font:15px serif;text-align:center">\(\sigma=0\)</div></foreignObject>
 <path d="M430 174C462 174 474 174 500 174" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#s-z-arrow)"/>
 <foreignObject x="412" y="130" width="112" height="35"><div xmlns="http://www.w3.org/1999/xhtml" style="font:18px serif;text-align:center">\(z=e^{sT}\)</div></foreignObject>
 <text x="560" y="52" fill="#315d7c" font-size="18" font-family="Microsoft YaHei, sans-serif">z 平面</text>
 <path d="M552 205H856" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#s-z-arrow)"/>
 <path d="M704 326V72" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#s-z-arrow)"/>
 <circle cx="704" cy="205" r="110" fill="none" stroke="#0f8b8d" stroke-width="2.4"/>
 <path d="M704 205L780 125" fill="none" stroke="#b56b2e" stroke-width="1.6" stroke-dasharray="6 4"/>
 <circle cx="780" cy="125" r="5.5" fill="#b56b2e"/>
 <foreignObject x="862" y="184" width="44" height="32"><div xmlns="http://www.w3.org/1999/xhtml" style="font:17px serif">\(\operatorname{Re}\{z\}\)</div></foreignObject>
 <foreignObject x="714" y="54" width="64" height="31"><div xmlns="http://www.w3.org/1999/xhtml" style="font:17px serif">\(\operatorname{Im}\{z\}\)</div></foreignObject>
 <foreignObject x="786" y="99" width="88" height="33"><div xmlns="http://www.w3.org/1999/xhtml" style="font:17px serif">\(e^{j\omega}\)</div></foreignObject>
 <foreignObject x="601" y="330" width="207" height="32"><div xmlns="http://www.w3.org/1999/xhtml" style="font:15px serif;text-align:center">\(\left|z\right|=1\)</div></foreignObject>
</svg>"""


def roc_support_svg() -> str:
    """Show the four source ROC shapes with real, equal-scale z-plane axes."""
    return r"""<!-- roc_support_svg: four textbook z-plane ROC panels -->
<svg id="roc-support-diagram" class="diagram" viewBox="0 0 920 500" role="img" aria-label="有限长、右边、左边与双边序列的收敛域示意图">
 <defs>
  <marker id="roc-axis-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker>
 </defs>
 <rect x="14" y="16" width="438" height="220" rx="8" fill="#fbfcfd" stroke="#d8e0e5"/>
 <rect x="468" y="16" width="438" height="220" rx="8" fill="#fbfcfd" stroke="#d8e0e5"/>
 <rect x="14" y="264" width="438" height="220" rx="8" fill="#fbfcfd" stroke="#d8e0e5"/>
 <rect x="468" y="264" width="438" height="220" rx="8" fill="#fbfcfd" stroke="#d8e0e5"/>
 <g font-family="Microsoft YaHei, sans-serif" fill="#315d7c" font-size="17">
  <text x="36" y="46">有限长序列</text><text x="490" y="46">右边序列</text>
  <text x="36" y="294">左边序列</text><text x="490" y="294">双边序列</text>
 </g>
 <!-- finite-duration: full finite z plane -->
 <rect x="54" y="62" width="300" height="126" rx="4" fill="#d9f3ef" opacity=".55"/>
 <path d="M74 126H340M208 202V60" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#roc-axis-arrow)"/>
 <circle cx="208" cy="126" r="5" fill="#b56b2e"/><text x="220" y="120" fill="#52616b" font-size="15">原点</text>
 <foreignObject x="66" y="194" width="290" height="30"><div xmlns="http://www.w3.org/1999/xhtml" style="font:15px serif;text-align:center">\(0&lt;\left|z\right|&lt;\infty\)</div></foreignObject>
 <!-- right-sided: the shaded exterior is the ROC, the pole circle is excluded -->
 <path d="M528 64H794V188H528Z M662 68a58 58 0 1 0 0 116a58 58 0 1 0 0 -116Z" fill="#d9f3ef" fill-rule="evenodd" opacity=".65"/>
 <path d="M528 126H794M662 202V60" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#roc-axis-arrow)"/>
 <circle cx="662" cy="126" r="58" fill="none" stroke="#b56b2e" stroke-width="2" stroke-dasharray="6 4"/>
 <circle cx="720" cy="126" r="5" fill="#b56b2e"/><text x="729" y="118" fill="#52616b" font-size="15">极点</text>
 <foreignObject x="520" y="194" width="290" height="30"><div xmlns="http://www.w3.org/1999/xhtml" style="font:15px serif;text-align:center">\(\left|z\right|&gt;\left|p_{\max}\right|\)</div></foreignObject>
 <!-- left-sided: inner ROC -->
 <path d="M74 374H340M208 450V308" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#roc-axis-arrow)"/>
 <circle cx="208" cy="374" r="58" fill="#d9f3ef" opacity=".72" stroke="#0f8b8d" stroke-width="2" stroke-dasharray="6 4"/>
 <circle cx="266" cy="374" r="5" fill="#b56b2e"/><text x="276" y="366" fill="#52616b" font-size="15">极点</text>
 <foreignObject x="66" y="442" width="290" height="30"><div xmlns="http://www.w3.org/1999/xhtml" style="font:15px serif;text-align:center">\(\left|z\right|&lt;\left|p_{\min}\right|\)</div></foreignObject>
 <!-- two-sided: annular ROC -->
 <path d="M528 374H794M662 450V308" fill="none" stroke="#174b73" stroke-width="2" marker-end="url(#roc-axis-arrow)"/>
 <circle cx="662" cy="374" r="76" fill="#d9f3ef" opacity=".72" stroke="#0f8b8d" stroke-width="2" stroke-dasharray="6 4"/>
 <circle cx="662" cy="374" r="38" fill="#fbfcfd" stroke="#0f8b8d" stroke-width="2" stroke-dasharray="6 4"/>
 <circle cx="700" cy="374" r="5" fill="#b56b2e"/><circle cx="738" cy="374" r="5" fill="#b56b2e"/>
 <foreignObject x="520" y="442" width="290" height="30"><div xmlns="http://www.w3.org/1999/xhtml" style="font:15px serif;text-align:center">\(\left|p_i\right|&lt;\left|z\right|&lt;\left|p_{i+1}\right|\)</div></foreignObject>
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
<p>由采样冲激列的拉普拉斯变换可以直接得到 z 变换的来源：把 \(\widehat h(t)=\sum_n h(nT)\delta(t-nT)\) 代入拉普拉斯积分，便得到 \(z=e^{sT}\) 下的离散幂级数。</p>
<div class="formula">\[
\begin{aligned}
\widehat{H}(s)&=\sum_{n=-\infty}^{\infty}h(n)e^{-snT}\\
&=\sum_{n=-\infty}^{\infty}h(n)\left(e^{sT}\right)^{-n}
=\sum_{n=-\infty}^{\infty}h(n)z^{-n}=H(z).
\end{aligned}
\]</div>
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
<h2>四种典型序列的 ROC 形状</h2>
<p>把时间支持范围与 ROC 对照，可以避免只看代数式而误判序列类型。有限长序列的 ROC 不含有限极点；右边序列的 ROC 向无穷远延伸；左边序列的 ROC 向原点延伸；双边序列的 ROC 被两个极点圆夹在中间。</p>
__ROC_SUPPORT__
<div class="formula">\[
\begin{aligned}
\text{有限长序列：}\;&0<\left|z\right|<\infty,\\
\text{右边序列：}\;&\left|z\right|>\left|p_{\max}\right|,\\
\text{左边序列：}\;&\left|z\right|<\left|p_{\min}\right|,\\
\text{双边序列：}\;&\left|p_i\right|<\left|z\right|<\left|p_{i+1}\right|.
\end{aligned}
\]</div>
<p>若有限长序列只含非负时间样本，ROC 包含无穷远点而可能不含原点；若只含非正时间样本，ROC 包含原点而可能不含无穷远点。这里的 \(p_{\max}\) 与 \(p_{\min}\) 分别表示模最大的有限极点和模最小的有限极点。</p>
<h2>给定极点时 ROC 的可能性</h2>
<p>对于有理型 \(X(z)\)，ROC 只能是由极点圆划分出的区域，不能穿过极点。若全部极点的模依次为 \(\left|p_1\right|<\left|p_2\right|<\cdots<\left|p_M\right|\)，可能的 ROC 依次对应左边、双边或右边序列：</p>
<div class="formula">\[
\left|z\right|<\left|p_1\right|,\quad
\left|p_1\right|<\left|z\right|<\left|p_2\right|,\quad\ldots,\quad
\left|z\right|>\left|p_M\right|.
\]</div>
<p>因此，给出 \(X(z)\) 时还必须给出 ROC；给出因果性时，ROC 取最外极点之外；给出稳定性时，ROC 必须包含单位圆。这个顺序与后续由系统函数判断因果、稳定和频率响应的步骤保持一致。</p>
<h2>例题：同一代数式与不同收敛域</h2>
<p>设 \(X(z)=\frac{1}{1-az^{-1}}\)。当 \(\left|z\right|>\left|a\right|\) 时，按 \(z^{-1}\) 的降幂展开，得到 \(x(n)=a^n u(n)\)；当 \(\left|z\right|<\left|a\right|\) 时，按 \(z\) 的升幂展开，得到 \(x(n)=-a^n u(-n-1)\)。代数式相同而 ROC 不同，时间支持范围也不同。</p>
<div class="formula">\[x(n)=\delta(n)\quad\Longrightarrow\quad X(z)=1,\qquad \text{ROC：全 z 平面}\]</div>
</main>""".replace("__Z_PLANE__", z_plane_svg()).replace("__ROC_SUPPORT__", roc_support_svg())
    output.write_text(f'<!doctype html><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}', encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full/outputs/chapter_02_foundations_mathjax_component.pdf"))
