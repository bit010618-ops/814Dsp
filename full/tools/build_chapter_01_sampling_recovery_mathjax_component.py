"""Sampling reconstruction material with MathJax and computed vector figures."""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def recovery_spectrum_svg() -> str:
    """Draw sampled spectral replicas and the reconstruction passband."""
    centers = (170.0, 430.0, 690.0)
    triangles = "\n".join(
        f'<path class="replica" d="M{center - 96:.1f} 184 L{center:.1f} 54 L{center + 96:.1f} 184"/>'
        for center in centers
    )
    return r"""
<!-- recovery_spectrum_svg: data-defined spectral replicas and passband -->
<svg class="signal-svg" viewBox="0 0 860 270" role="img" aria-label="重构低通滤波器的通带">
  <defs>
    <marker id="recovery-omega-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4"
      orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker>
  </defs>
  <path class="axis" d="M48 184 H814" marker-end="url(#recovery-omega-arrow)"/>
  <path class="guide" d="M334 184 V201 M526 184 V201"/>
  <g>__TRIANGLES__</g>
  <path class="passband" d="M334 42 V160 H526 V42"/>
  <text class="plain-label" x="430" y="31" text-anchor="middle">理想低通重构通带</text>
  <g class="math-label">
    <foreignObject x="293" y="202" width="82" height="38"><div>\(-\frac{\Omega_s}{2}\)</div></foreignObject>
    <foreignObject x="410" y="202" width="42" height="38"><div>\(0\)</div></foreignObject>
    <foreignObject x="488" y="202" width="76" height="38"><div>\(\frac{\Omega_s}{2}\)</div></foreignObject>
    <foreignObject x="814" y="160" width="42" height="38"><div>\(\Omega\)</div></foreignObject>
  </g>
</svg>
""".replace("__TRIANGLES__", triangles)


def _sinc(value: float) -> float:
    if abs(value) < 1e-9:
        return 1.0
    return math.sin(math.pi * value) / (math.pi * value)


def _sinc_path(shift: float, *, width: float = 760, baseline: float = 144, scale_y: float = 64) -> str:
    points: list[str] = []
    for index in range(401):
        value = -3.5 + index * 7 / 400
        x = 50 + (value + 3.5) * width / 7
        y = baseline - _sinc(value - shift) * scale_y
        points.append(f"{x:.2f},{y:.2f}")
    return "M" + " L".join(points)


def interpolation_sinc_svg() -> str:
    """Draw actual shifted sinc interpolation functions from their formula."""
    center = _sinc_path(0.0)
    left = _sinc_path(-1.0)
    right = _sinc_path(1.0)
    return r"""
<!-- interpolation_sinc_svg: curves sampled from sin(pi t/T)/(pi t/T) -->
<svg class="signal-svg" viewBox="0 0 860 280" role="img" aria-label="移位 sinc 插值函数">
  <defs>
    <marker id="sinc-t-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4"
      orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker>
    <marker id="sinc-g-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4"
      orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker>
  </defs>
  <path class="axis" d="M43 144 H814" marker-end="url(#sinc-t-arrow)"/>
  <path class="axis" d="M430 220 V28" marker-end="url(#sinc-g-arrow)"/>
  <path class="guide" d="M321 140 V148 M430 140 V148 M539 140 V148"/>
  <path class="sinc-secondary" d="__LEFT__"/>
  <path class="sinc-secondary" d="__RIGHT__"/>
  <path class="sinc-primary" d="__CENTER__"/>
  <circle class="sample-dot" cx="430" cy="80" r="4.3"/>
  <g class="math-label">
    <foreignObject x="298" y="151" width="48" height="35"><div>\(-T\)</div></foreignObject>
    <foreignObject x="415" y="151" width="30" height="35"><div>\(0\)</div></foreignObject>
    <foreignObject x="525" y="151" width="38" height="35"><div>\(T\)</div></foreignObject>
    <foreignObject x="812" y="122" width="30" height="36"><div>\(t\)</div></foreignObject>
    <foreignObject x="440" y="22" width="44" height="36"><div>\(g(t)\)</div></foreignObject>
  </g>
</svg>
""".replace("__LEFT__", left).replace("__RIGHT__", right).replace("__CENTER__", center)


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    spectrum = recovery_spectrum_svg()
    sinc = interpolation_sinc_svg()
    content = r"""
<main class="chapter">
  <header><h1>时域采样信号的恢复</h1></header>

  <section class="recovery-intro">
    <h2>恢复的前提</h2>
    <p>当模拟信号满足采样定理、采样后的频谱副本彼此不重叠时，原模拟信号可由采样值唯一恢复。频域中，恢复的核心是保留中央频谱副本并抑制其他重复副本。</p>
    <h2>理想低通重构</h2>
    <p>理想重构滤波器选出中央频谱副本。其截止角频率取为 \(\frac{\Omega_s}{2}\)；实际滤波器不能做到理想的垂直截止，但可在允许误差范围内逼近该通带。</p>
  </section>

  <section>
    <figure><figcaption>理想低通重构的通带选择</figcaption>__RECOVERY_SPECTRUM__</figure>
    <div class="formula">\[
      H_r(j\Omega)=
      \begin{cases}
        T, & \left|\Omega\right|\leq\frac{\Omega_s}{2},\\
        0, & \left|\Omega\right|>\frac{\Omega_s}{2}.
      \end{cases}
    \]</div>
    <p>频域中将采样频谱乘以重构滤波器，对应到时域就是将采样信号与滤波器的冲激响应卷积。理想低通滤波器的冲激响应给出了恢复所需的基本波形：</p>
    <div class="formula">\[
      h_r(t)=\frac{T\sin\!\left(\frac{\Omega_s}{2}t\right)}{\pi t}
    \]</div>
  </section>

  <section>
    <h2>卷积形式的恢复</h2>
    <p>若恢复结果 \(y_a(t)\) 与原模拟信号 \(x_a(t)\) 相同，便完成恢复。将采样冲激串代入卷积式，可把恢复过程写成各个样值的加权叠加：</p>
    <div class="formula">\[
      y_a(t)=x_s(t)\ast h_r(t)
      =\sum_{m=-\infty}^{\infty}x_a(mT)\,g(t-mT)
    \]</div>
    <h2>插值函数</h2>
    <p>把理想低通重构的冲激响应乘以 \(T\)，可得到标准插值函数。它以某一个采样点为中心，在其他整数倍采样时刻取零，因此不会改变相邻样值。</p>
    <div class="formula">\[
      g(t)=T h_r(t)=\frac{\sin\!\left(\frac{\pi t}{T}\right)}{\frac{\pi t}{T}}
    \]</div>
    <figure><figcaption>以一个采样点为中心的移位插值波形</figcaption>__INTERPOLATION_SINC__</figure>
  </section>

  <section>
    <h2>采样点处的严格插值</h2>
    <p>插值函数在自身中心采样点的值为一，在其他整数倍采样点的值为零。因此，在任意采样时刻，求和式中只有与该时刻对应的一项保留，其余项全部消失：</p>
    <div class="formula">\[
      g(0)=1,\qquad g(kT)=0\quad\left(k\in\mathbb{Z},\ k\ne 0\right)
    \]</div>
    <div class="formula">\[
      y_a(mT)=x_a(mT)
    \]</div>
    <p>恢复后的连续信号准确穿过每一个采样值；采样点之间的波形由全部加权插值函数的延伸和叠加决定。</p>
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
h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:16pt 0 7pt}
.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
figure{margin:10pt 0 12pt}figcaption{text-align:center;color:#486d8b;font-size:9.5pt;margin-bottom:3pt}
.signal-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.axis{fill:none;stroke:#174b73;stroke-width:2.1;stroke-linecap:round}.guide{stroke:#174b73;stroke-width:1.45}
.replica{fill:none;stroke:#0f8b8d;stroke-width:3;stroke-linejoin:round}.passband{fill:none;stroke:#b08d57;stroke-width:2.2}
.plain-label{fill:#79582d;font:16px "Microsoft YaHei",sans-serif}.sinc-primary{fill:none;stroke:#0f8b8d;stroke-width:3}
.sinc-secondary{fill:none;stroke:#78babc;stroke-width:2}.sample-dot{fill:#b56b2e}
.math-label foreignObject div{height:100%;display:flex;justify-content:center;align-items:center;color:#172b3a;font-size:18px}
</style>__CONTENT__</html>"""
    document = template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", content)
    document = document.replace("__RECOVERY_SPECTRUM__", spectrum).replace("__INTERPOLATION_SINC__", sinc)
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
    print(render_pdf(ROOT / "full/outputs/chapter_01_sampling_recovery_mathjax_component.pdf"))
