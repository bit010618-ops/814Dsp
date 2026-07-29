"""Engineering sampling material with MathJax and coordinate-defined figures."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def process_chain_svg() -> str:
    boxes = (
        (54, "模拟输入"), (254, "抗混叠滤波"), (454, "模数转换"), (654, "离散序列"),
    )
    rendered = "\n".join(
        f'<rect class="chain-box" x="{x}" y="48" width="146" height="58" rx="7"/>'
        f'<text class="chain-label" x="{x + 73}" y="83" text-anchor="middle">{label}</text>'
        for x, label in boxes
    )
    arrows = "\n".join(
        f'<path class="chain-arrow" d="M{x} 77 H{x + 42}" marker-end="url(#chain-arrow)"/>'
        for x in (204, 404, 604)
    )
    return """
<!-- process_chain_svg: standard left-to-right sampling process -->
<svg class="chain-svg" viewBox="0 0 854 152" role="img" aria-label="抗混叠采样处理链">
  <defs><marker id="chain-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4"
    orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs>
  __BOXES__
  __ARROWS__
</svg>
""".replace("__BOXES__", rendered).replace("__ARROWS__", arrows)


def anti_alias_spectrum_svg() -> str:
    top = "\n".join(
        f'<path class="overlap" d="M{center - 88} 96 L{center} 35 L{center + 88} 96"/>'
        for center in (190, 430, 670)
    )
    lower = "\n".join(
        f'<path class="separated" d="M{center - 46} 223 L{center} 162 L{center + 46} 223"/>'
        for center in (170, 430, 690)
    )
    return r"""
<!-- anti_alias_spectrum_svg: true coordinate spectral replicas -->
<svg class="signal-svg" viewBox="0 0 860 278" role="img" aria-label="带宽限制前后的频谱副本">
  <defs><marker id="anti-alias-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4"
    orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs>
  <path class="axis" d="M45 96 H815" marker-end="url(#anti-alias-arrow)"/>
  <path class="axis" d="M45 223 H815" marker-end="url(#anti-alias-arrow)"/>
  <g>__TOP__</g><g>__LOWER__</g>
  <text class="figure-note" x="48" y="22">带宽未限制：频谱副本相交</text>
  <text class="figure-note" x="48" y="150">先限制输入带宽：频谱副本分离</text>
  <text class="bad-note" x="430" y="28" text-anchor="middle">混叠</text>
  <text class="good-note" x="430" y="155" text-anchor="middle">可恢复</text>
  <g class="math-label">
    <foreignObject x="816" y="73" width="32" height="34"><div>\(f\)</div></foreignObject>
    <foreignObject x="816" y="200" width="32" height="34"><div>\(f\)</div></foreignObject>
  </g>
</svg>
""".replace("__TOP__", top).replace("__LOWER__", lower)


def bandpass_spectrum_svg() -> str:
    return r"""
<!-- bandpass_spectrum_svg: band edges driven by explicit frequency positions -->
<svg class="signal-svg" viewBox="0 0 860 240" role="img" aria-label="带通信号的频带位置与带宽">
  <defs><marker id="bandpass-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4"
    orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs>
  <path class="axis" d="M52 146 H814" marker-end="url(#bandpass-arrow)"/>
  <rect class="band-fill" x="505" y="74" width="168" height="72" rx="2"/>
  <path class="dimension" d="M505 174 H673 M505 168 V180 M673 168 V180"/>
  <g class="math-label">
    <foreignObject x="785" y="122" width="36" height="36"><div>\(f\)</div></foreignObject>
    <foreignObject x="481" y="184" width="78" height="36"><div>\(f_h-\Delta f_0\)</div></foreignObject>
    <foreignObject x="652" y="184" width="44" height="36"><div>\(f_h\)</div></foreignObject>
    <foreignObject x="557" y="151" width="64" height="34"><div>\(\Delta f_0\)</div></foreignObject>
    <foreignObject x="568" y="46" width="56" height="34"><div>\(f_0\)</div></foreignObject>
  </g>
</svg>
"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main class="chapter">
  <header><h1>工程采样的带宽约束</h1></header>
  <section class="engineering-intro">
    <p>实际模拟信号进入模数转换器之前，通常先经过抗混叠滤波器。它限制输入带宽，使采样后的频谱副本彼此分离，从而避免不可逆的混叠。</p>
    <figure><figcaption>采样前的抗混叠处理链</figcaption>__PROCESS_CHAIN__</figure>
    <h2>采样前的带宽约束</h2>
    <p>若滤波后的模拟输入最高频率为 \(f_h\)，则选择采样频率时应满足采样定理。工程上还要为滤波器的过渡带留出余量，截止频率不宜恰好压在临界位置。</p>
    <div class="formula">\[
      f_h\leq\frac{f_s}{2}
      \qquad\Longleftrightarrow\qquad
      \Omega_h\leq\frac{\Omega_s}{2}
    \]</div>
  </section>

  <section>
    <h2>抗混叠滤波的频域作用</h2>
    <p>采样会使模拟频谱按 \(f_s\) 为间隔重复出现。若原信号带宽过宽，相邻副本会相交；先用低通滤波器限制输入带宽后，副本之间保留空隙，才可用重构滤波器取回所需频带。</p>
    <figure><figcaption>带宽限制前后的频谱副本</figcaption>__ANTI_ALIAS_SPECTRUM__</figure>
    <p>两图的差别不在于采样操作本身，而在于采样前是否已经满足带宽条件。混叠一旦发生，重叠区域来自哪些原始频率成分便不再能够唯一判定。</p>
  </section>

  <section>
    <h2>带通信号的采样参数</h2>
    <p>带通信号的频谱只占据某一段非零频率附近的区间，而不是从零频率开始。记最高频率为 \(f_h\)、频带宽度为 \(\Delta f_0\)，则频带中心频率由右端点与带宽共同确定。</p>
    <div class="formula">\[
      f_0=f_h-\frac{\Delta f_0}{2}
    \]</div>
    <figure><figcaption>频带位置与带宽</figcaption>__BANDPASS_SPECTRUM__</figure>
    <h2>带通信号的无混叠采样</h2>
    <p>当带通信号的最高频率恰好是带宽的整数倍时，可直接选用两倍带宽作为采样频率。采样后的频谱副本不重叠，并可由适当的带通滤波器恢复原信号。</p>
    <div class="formula">\[
      f_h=r\Delta f_0,\quad r\in\mathbb{Z}
      \qquad\Longrightarrow\qquad
      f_s=2\Delta f_0
    \]</div>
  </section>

  <section>
    <h2>非整数情形</h2>
    <p>若 \(\frac{f_h}{\Delta f_0}\) 不是整数，则将频带下端向低频方向延伸，构造一个不小于原带宽的 \(\Delta f_0'\)，使最高频率成为该扩展带宽的整数倍；随后按相同方法选择采样频率。</p>
    <div class="formula">\[
      \Delta f_0'=\frac{f_h}{r}\geq\Delta f_0,\qquad
      r\in\mathbb{Z},\qquad
      f_s=2\Delta f_0'
    \]</div>
    <p>这里的扩展只用于确定可行的采样频率和滤波器通带，并不表示原信号新增了频率成分；恢复时仍使用与原频带相匹配的带通滤波器。</p>
  </section>
</main>
"""
    template = r"""<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<script>window.MathJax={tex:{packages:{'[+]':['ams']}}};</script>
<script defer src="__MATHJAX__"></script>
<style>
@page{size:A4;margin:21mm 18mm 23mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933}
.chapter{max-width:174mm;margin:auto}.chapter>header h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt}
h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:16pt 0 7pt}
.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
figure{margin:10pt 0 12pt}figcaption{text-align:center;color:#486d8b;font-size:9.5pt;margin-bottom:3pt}
.chain-svg,.signal-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.chain-box{fill:#f4f7f8;stroke:#b08d57;stroke-width:1.6}.chain-label{fill:#1e4f79;font:18px "Microsoft YaHei",sans-serif}
.chain-arrow,.axis{fill:none;stroke:#174b73;stroke-width:2.1;stroke-linecap:round}.overlap{fill:none;stroke:#b13a3a;stroke-width:3}.separated{fill:none;stroke:#0f8b8d;stroke-width:3}
.figure-note{fill:#486d8b;font:16px "Microsoft YaHei",sans-serif}.bad-note{fill:#b13a3a;font:16px "Microsoft YaHei",sans-serif}.good-note{fill:#0f8b8d;font:16px "Microsoft YaHei",sans-serif}
.band-fill{fill:#dceff0;stroke:#0f8b8d;stroke-width:2}.dimension{fill:none;stroke:#b08d57;stroke-width:1.7}
.math-label foreignObject div{height:100%;display:flex;justify-content:center;align-items:center;color:#172b3a;font-size:18px}
</style>__CONTENT__</html>"""
    document = template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", content)
    document = document.replace("__PROCESS_CHAIN__", process_chain_svg())
    document = document.replace("__ANTI_ALIAS_SPECTRUM__", anti_alias_spectrum_svg())
    document = document.replace("__BANDPASS_SPECTRUM__", bandpass_spectrum_svg())
    output.write_text(document, encoding="utf-8")
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
    print(render_pdf(ROOT / "full/outputs/chapter_01_sampling_engineering_mathjax_component.pdf"))
