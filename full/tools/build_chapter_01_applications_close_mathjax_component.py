"""Sampling applications and chapter close, rendered as MathJax and SVG."""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def _wheel(cx: float, cy: float, marker_angle: float) -> str:
    spokes = "\n".join(
        f'<path class="spoke" d="M{cx} {cy} L{cx + 94 * math.cos(math.radians(index * 45)):.1f} {cy + 94 * math.sin(math.radians(index * 45)):.1f}"/>'
        for index in range(8)
    )
    marker_x = cx + 74 * math.cos(math.radians(marker_angle))
    marker_y = cy + 74 * math.sin(math.radians(marker_angle))
    return (
        f'<g>{spokes}<circle class="wheel-rim" cx="{cx}" cy="{cy}" r="113"/>'
        f'<circle class="hub" cx="{cx}" cy="{cy}" r="40"/>'
        f'<circle class="marker" cx="{marker_x:.1f}" cy="{marker_y:.1f}" r="13"/></g>'
    )


def wagon_wheel_svg() -> str:
    """Paired, geometrically generated wheels explain visual aliasing."""
    return r"""
<!-- wagon_wheel_svg: two equal-spoke wheels with different angular samples -->
<svg class="wheel-svg" viewBox="0 0 920 410" role="img" aria-label="车轮视觉混叠示意">
  __LEFT_WHEEL__
  __RIGHT_WHEEL__
  <text class="wheel-label" x="230" y="354" text-anchor="middle">帧间转过一个辐条间距：看起来近似静止</text>
  <text class="wheel-label" x="690" y="354" text-anchor="middle">帧间略少转一些：看起来反向转动</text>
  <text class="wheel-note" x="460" y="394" text-anchor="middle">离散观察只保留有限时刻的状态，连续转动可能产生相同或近似相同的帧序列。</text>
</svg>
""".replace("__LEFT_WHEEL__", _wheel(230, 172, 90)).replace("__RIGHT_WHEEL__", _wheel(690, 172, 45))


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main class="chapter">
  <header><h1>从采样定理到信息论</h1></header>
  <section class="apps-intro">
    <p>采样问题的核心在于：在满足条件时，离散样值足以恢复连续信号；不满足条件时，不同连续信号可能留下同一组样值。这个结论奠定了数字信号处理对连续世界进行离散表示的基础。</p>
    <h2>奈奎斯特的采样思想</h2>
    <p>哈利·奈奎斯特在 1927 年提出：对带宽有限的模拟信号进行采样，若要由样值准确恢复原信号，采样频率至少应为原信号最高频率的两倍。采样频率的一半称为奈奎斯特频率。</p>
    <div class="formula">\[
      f_s\geq2f_h,\qquad f_N=\frac{f_s}{2}
    \]</div>
    <h2>香农的推广</h2>
    <p>克劳德·香农建立现代信息论，并在带宽、噪声和信息传输速率的研究中发展了相关理论。采样定理通常也称为奈奎斯特—香农采样定理。</p>
  </section>
  <section>
    <h2>同一组样值未必对应唯一连续信号</h2>
    <p>设离散序列 \(x(n)=\sin(0.1\pi n)\) 来自在 \(f_s=1000\,\mathrm{Hz}\) 下对某个连续正弦信号的采样。虽然样值的变化规律已经确定，但若不额外限制连续信号的频带，仅凭这些样值仍无法唯一判断原连续信号。</p>
    <div class="formula">\[
      x(n)=\sin(0.1\pi n),\qquad T=\frac{1}{f_s}=1\,\mathrm{ms}
    \]</div>
    <h2>两个给出相同样值的连续信号</h2>
    <div class="formula">\[
      \left.\sin(100\pi t)\right|_{t=nT}=\sin(0.1\pi n)
    \]</div>
    <div class="formula">\[
      \left.\sin(2100\pi t)\right|_{t=nT}=\sin(2.1\pi n)=\sin(0.1\pi n)
    \]</div>
    <p>前者的频率为 \(50\,\mathrm{Hz}\)，后者的频率为 \(1050\,\mathrm{Hz}\)；在该采样频率下，它们的样值完全相同。这正是频谱复制造成的歧义：连续信号必须先满足带限条件，才能从样值中唯一恢复。</p>
  </section>
  <section>
    <h2>车轮现象：视觉中的混叠</h2>
    <p>摄像机以固定帧率记录转动的车轮，相邻帧之间只能看到有限次状态。当车轮在一帧间隔内转过接近一个辐条间距时，下一帧的图案会与上一帧十分相似，于是视觉上可能出现车轮静止或反向转动。</p>
    <figure><figcaption>离散观察下的不同表象</figcaption>__WHEEL__</figure>
    <p>该现象与信号采样中的混叠本质相同：连续变化被离散时刻观察后，原本不同的变化过程可能映射为难以区分的离散序列。提高观察频率或限制原信号带宽，才能消除这种歧义。</p>
  </section>
  <section>
    <h2>透过现象看本质</h2>
    <p>我们通过感官或测量认识世界时，常常只接触到局部表象。采样、量化、观察帧率等过程会改变表象与原始连续过程之间的对应关系，因此需要用明确的模型和条件判断结论是否可靠。</p>
    <h2>第一章小结</h2>
    <p>本章从离散时间信号的表示、运算与典型序列出发，讨论了系统性质、线性卷积、差分方程，以及采样、恢复和模拟—数字处理链。贯穿全章的判断原则是：先明确对象与条件，再使用相应的数学表示和系统关系。</p>
  </section>
</main>
"""
    template = r"""<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<script>window.MathJax={tex:{packages:{'[+]':['ams']}}};</script><script defer src="__MATHJAX__"></script>
<style>
@page{size:A4;margin:21mm 18mm 23mm}
body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933}.chapter{max-width:174mm;margin:auto}
.chapter>header h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt}
h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:16pt 0 7pt}
.apps-intro{break-after:page}
.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
figure{break-inside:avoid;margin:10pt 0 12pt}figcaption{text-align:center;color:#486d8b;font-size:9.5pt;margin-bottom:3pt}
.wheel-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.wheel-rim{fill:none;stroke:#b6342d;stroke-width:4}.spoke{stroke:#0f8b8d;stroke-width:2.5}.hub{fill:#f4f7f8;stroke:#b6342d;stroke-width:3}.marker{fill:#174b73}
.wheel-label{fill:#1e4f79;font:17px "Microsoft YaHei",sans-serif}.wheel-note{fill:#51697b;font:15px "Microsoft YaHei",sans-serif}
</style>__CONTENT__</html>"""
    document = template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", content)
    output.write_text(document.replace("__WHEEL__", wagon_wheel_svg()), encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run(
        [str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()],
        check=True,
    )
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full/outputs/chapter_01_applications_close_mathjax_component.pdf"))
