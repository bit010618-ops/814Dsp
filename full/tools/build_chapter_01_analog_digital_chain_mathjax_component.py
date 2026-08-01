"""Analog-to-digital signal-processing chain with MathJax and vector diagrams."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def analog_digital_chain_svg() -> str:
    """Return a standard left-to-right DSP processing structure."""
    blocks = (
        (94, 150, "前置预滤波器"),
        (272, 126, "模数转换"),
        (426, 154, "数字信号处理"),
        (608, 126, "数模转换"),
        (762, 150, "模拟低通滤波器"),
    )
    block_markup = "\n".join(
        f'<g><rect class="block" x="{x}" y="106" width="{width}" height="62" rx="7"/>'
        f'<text class="block-label" x="{x + width / 2}" y="143" text-anchor="middle">{label}</text></g>'
        for x, width, label in blocks
    )
    arrow_markup = "\n".join(
        f'<path class="arrow" d="M{x + width + 8} 137 H{next_x - 10}" marker-end="url(#chain-arrow)"/>'
        for (x, width, _), (next_x, _, _) in zip(blocks, blocks[1:])
    )
    return r"""
<!-- analog_digital_chain_svg: standard left-to-right signal flow -->
<svg class="structure-svg" viewBox="0 0 1010 268" role="img" aria-label="模拟信号数字处理链路">
  <defs>
    <marker id="chain-arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#174b73"/>
    </marker>
  </defs>
  <path class="arrow" d="M33 137 H84" marker-end="url(#chain-arrow)"/>
  __BLOCKS__
  __ARROWS__
  <path class="arrow" d="M920 137 H978" marker-end="url(#chain-arrow)"/>
  <path class="domain-line" d="M32 214 H382 M411 214 H569 M596 214 H978"/>
  <text class="domain-label" x="207" y="242" text-anchor="middle">模拟域</text>
  <text class="domain-label" x="490" y="242" text-anchor="middle">数字域</text>
  <text class="domain-label" x="787" y="242" text-anchor="middle">模拟域</text>
  <g class="math-label">
    <foreignObject x="20" y="78" width="78" height="34"><div>\(x_a(t)\)</div></foreignObject>
    <foreignObject x="386" y="69" width="74" height="34"><div>\(x(n)\)</div></foreignObject>
    <foreignObject x="574" y="69" width="74" height="34"><div>\(y(n)\)</div></foreignObject>
    <foreignObject x="917" y="78" width="82" height="34"><div>\(y_a(t)\)</div></foreignObject>
  </g>
</svg>
""".replace("__BLOCKS__", block_markup).replace("__ARROWS__", arrow_markup)


def zero_order_hold_svg() -> str:
    """Draw true sampled values and a zero-order-held waveform."""
    values = (0.30, 0.62, 0.43, 0.78, 0.56, 0.36)
    left, step, baseline, scale = 108.0, 112.0, 190.0, 132.0
    points = [(left + index * step, baseline - value * scale) for index, value in enumerate(values)]
    staircase = [f"M{points[0][0]:.1f},{points[0][1]:.1f}"]
    for index, (x, y) in enumerate(points[:-1]):
        next_x, next_y = points[index + 1]
        staircase.append(f"H{next_x:.1f} V{next_y:.1f}")
    stems = "\n".join(
        f'<path class="stem" d="M{x:.1f} {baseline:.1f} V{y:.1f}"/><circle class="sample-dot" cx="{x:.1f}" cy="{y:.1f}" r="4"/>'
        for x, y in points
    )
    ticks = "\n".join(
        f'<path class="tick" d="M{x:.1f} {baseline - 5:.1f} V{baseline + 5:.1f}"/>'
        for x, _ in points[:5]
    )
    labels = "\n".join(
        f'<foreignObject x="{x - 21:.1f}" y="202" width="42" height="32"><div>\\({label}\\)</div></foreignObject>'
        for (x, _), label in zip(points[:5], ("0", "T", "2T", "3T", "4T"))
    )
    return r"""
<!-- zero_order_hold_svg: values drive both stems and step waveform -->
<svg class="signal-svg" viewBox="0 0 860 270" role="img" aria-label="零阶保持输出">
  <defs>
    <marker id="zoh-time-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/>
    </marker>
    <marker id="zoh-value-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/>
    </marker>
  </defs>
  <path class="axis" d="M71 190 H812" marker-end="url(#zoh-time-arrow)"/>
  <path class="axis" d="M108 223 V41" marker-end="url(#zoh-value-arrow)"/>
  __TICKS__
  __STEMS__
  <path class="hold" d="__STAIRCASE__"/>
  <g class="math-label">
    __LABELS__
    <foreignObject x="814" y="171" width="34" height="34"><div>\(t\)</div></foreignObject>
    <foreignObject x="114" y="26" width="60" height="34"><div>\(y_0(t)\)</div></foreignObject>
  </g>
</svg>
""".replace("__STEMS__", stems).replace("__TICKS__", ticks).replace("__LABELS__", labels).replace("__STAIRCASE__", " ".join(staircase))


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main class="chapter">
  <header><h1>模拟信号的数字处理方法</h1></header>

  <section>
    <h2>从模拟输入到模拟输出</h2>
    <p>数字信号处理系统把连续时间的模拟输入变为离散数字序列，经过运算后再恢复为模拟输出。完整链路中，前置预滤波、模数转换、数字处理、数模转换和模拟低通滤波依次承担不同职责。</p>
    <figure><figcaption>模拟信号的数字处理链路</figcaption>__CHAIN__</figure>
    <div class="formula">\[
      x_a(t)\longrightarrow x(n)\longrightarrow y(n)\longrightarrow y_a(t)
    \]</div>
    <p>前置预滤波器先抑制可能在采样后折叠进有效频带的高频分量。若输入最高角频率为 \(\Omega_c\)，采样角频率应满足 \(\Omega_s\geq2\Omega_c\)，这样离散表示才不会发生频谱混叠。</p>
    <div class="formula">\[
      \Omega_s\geq2\Omega_c,\qquad f_s=\frac{1}{T}
    \]</div>
  </section>

  <section>
    <h2>采样、量化与编码</h2>
    <p>模数转换先在等时间间隔取得样值，再把连续幅度映射到有限个量化等级，并把量化结果表示为数字系统可以存储、传输和运算的码字。采样决定时间位置，量化决定幅度精度，编码决定数字表示。</p>
    <div class="formula">\[
      x(n)=x_a(nT),\qquad q(n)=Q\!\left[x(n)\right]
    \]</div>
    <h2>数字域中的处理</h2>
    <p>形成离散序列后，可在数字域完成滤波、降噪、增强、变换、压缩和识别等处理。数字处理器的输出仍是离散序列 \(y(n)\)，因此还需经过数模转换与平滑滤波，才得到连续时间输出。</p>
  </section>

  <section>
    <h2>数模转换与零阶保持</h2>
    <p>数模转换器把各个离散数值依次送入保持电路。最常见的零阶保持在两个采样时刻之间维持前一个样值不变，因而得到阶梯状的连续时间波形。</p>
    <figure><figcaption>零阶保持：样值在下一个采样时刻到来前保持不变</figcaption>__HOLD__</figure>
    <div class="formula">\[
      y(n)\longrightarrow y_0(t)\longrightarrow y_a(t)
    \]</div>
    <p>阶梯波形包含目标低频成分，也包含保持过程带来的高频分量。实际系统在保持器之后配置模拟平滑低通滤波器，使输出波形更接近连续信号。</p>
    <h2>采样间隔与实际恢复</h2>
    <p>在相同的模拟低通滤波条件下，采样间隔 \(T\) 越小，每一级台阶越短，保持输出对连续信号变化的跟随越细致。采样点更密并不替代重构滤波，但能降低实际恢复的近似误差。</p>
    <div class="formula">\[
      T\downarrow\quad\Longrightarrow\quad f_s=\frac{1}{T}\uparrow
    \]</div>
  </section>

  <section>
    <h2>处理链的检查顺序</h2>
    <p>先检查输入是否带限、采样频率是否满足无混叠条件；再检查量化和编码是否得到正确的数字序列；最后检查数模转换、保持与平滑滤波是否按正确次序连接。任何一个环节失配，都会使最终模拟输出偏离预期波形。</p>
  </section>
</main>
"""
    template = r"""<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<script>window.MathJax={tex:{packages:{'[+]':['ams']}}};</script>
<script defer src="__MATHJAX__"></script>
<style>
@page{size:A4;margin:21mm 18mm 23mm}
body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933}
.chapter{max-width:174mm;margin:auto}.chapter>header h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt}
h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:16pt 0 7pt;break-after:avoid}
.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
figure{margin:10pt 0 12pt}figcaption{text-align:center;color:#486d8b;font-size:9.5pt;margin-bottom:3pt}
.structure-svg,.signal-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.block{fill:#f4f7f8;stroke:#0f8b8d;stroke-width:2}.block-label{fill:#174b73;font:17px "Microsoft YaHei",sans-serif}
.arrow{fill:none;stroke:#174b73;stroke-width:2.2;stroke-linecap:round}.domain-line{stroke:#b08d57;stroke-width:1.3}.domain-label{fill:#79582d;font:16px "Microsoft YaHei",sans-serif}
.axis{fill:none;stroke:#174b73;stroke-width:2;stroke-linecap:round}.tick{stroke:#174b73;stroke-width:1.4}.stem{stroke:#8b4d11;stroke-width:1.8}.sample-dot{fill:#b56b2e}.hold{fill:none;stroke:#0f8b8d;stroke-width:3;stroke-linejoin:round}
.math-label foreignObject div{height:100%;display:flex;justify-content:center;align-items:center;color:#172b3a;font-size:18px}
</style>__CONTENT__</html>"""
    document = template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", content)
    document = document.replace("__CHAIN__", analog_digital_chain_svg()).replace("__HOLD__", zero_order_hold_svg())
    output.write_text(document, encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run(
        [
            str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}",
            html.resolve().as_uri(),
        ],
        check=True,
    )
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full/outputs/chapter_01_analog_digital_chain_mathjax_component.pdf"))
