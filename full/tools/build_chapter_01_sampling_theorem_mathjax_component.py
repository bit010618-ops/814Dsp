"""Sampling-theorem material with MathJax and coordinate-driven spectrum SVG."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def spectrum_svg(*, overlap: bool) -> str:
    """Generate three equally spaced triangular spectral replicas."""
    centers = (185.0, 430.0, 675.0)
    half_width = 138.0 if overlap else 92.0
    color = "#b13a3a" if overlap else "#0f8b8d"
    triangles = "\n".join(
        f'<path class="replica" d="M{center-half_width:.1f} 188 L{center:.1f} 56 L{center+half_width:.1f} 188"/>'
        for center in centers
    )
    return fr"""
<!-- spectrum_svg: data-defined spectral replicas -->
<svg class="spectrum-svg" viewBox="0 0 860 260" role="img"
     aria-label="采样后频谱的周期副本">
  <defs><marker id="omega-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4"
    orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker></defs>
  <path class="axis" d="M45 188 H815" marker-end="url(#omega-arrow)"/>
  <path class="guide" d="M185 188 V204 M430 188 V204 M675 188 V204"/>
  <g style="stroke:{color}">{triangles}</g>
  <g class="math-label">
    <foreignObject x="145" y="204" width="80" height="36"><div>\(-\Omega_s\)</div></foreignObject>
    <foreignObject x="410" y="204" width="42" height="36"><div>\(0\)</div></foreignObject>
    <foreignObject x="650" y="204" width="70" height="36"><div>\(\Omega_s\)</div></foreignObject>
    <foreignObject x="815" y="164" width="42" height="36"><div>\(\Omega\)</div></foreignObject>
  </g>
</svg>
"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    clean = spectrum_svg(overlap=False)
    overlap = spectrum_svg(overlap=True)
    content = rf"""
<main class="chapter">
  <header><h1>理想时域采样</h1></header>
  <section>
    <p>采样器可看作每隔 \(T\) 秒闭合一次的电子开关。它利用周期冲激函数序列从连续信号 \(x_a(t)\) 中抽取样值，使时间变量离散。</p>
    <div class="formula">\[
      \delta_T(t)=\sum_{{n=-\infty}}^{{\infty}}\delta(t-nT),
      \qquad x_s(t)=x_a(t)\delta_T(t)
    \]</div>
    <div class="formula">\[
      x(n)=x_a(nT),\qquad f_s=\frac{{1}}{{T}},\qquad \Omega_s=\frac{{2\pi}}{{T}}
    \]</div>
    <h2>采样后的频域周期延拓</h2>
    <p>时域相乘对应频域卷积。冲激序列在频域仍为间隔 \(\Omega_s\) 的冲激序列，因此原信号频谱会以 \(\Omega_s\) 为周期被复制：</p>
    <div class="formula">\[
      X_s(j\Omega)=\frac{{1}}{{T}}\sum_{{k=-\infty}}^{{\infty}}
      X_a\left[j(\Omega-k\Omega_s)\right]
    \]</div>
    <figure><figcaption>采样后的频域周期延拓</figcaption>{clean}</figure>
    <p>每个三角谱表示原频谱的一个平移副本。时域离散必然对应频域周期；这也是混叠与重构判断的起点。</p>
  </section>

  <section>
    <h2>不混叠与混叠</h2>
    <p>设 \(x_a(t)\) 为带限信号，其最高角频率为 \(\Omega_h\)。谱副本是否重叠完全由 \(\Omega_h\) 与 \(\frac{{\Omega_s}}{{2}}\) 的关系决定。</p>
    <h3>情况一：不混叠</h3>
    <div class="formula">\[\Omega_h\leq\frac{{\Omega_s}}{{2}}\]</div>
    <figure><figcaption>相邻谱副本互不重叠</figcaption>{clean}</figure>
    <p>理论上用截止角频率为 \(\frac{{\Omega_s}}{{2}}\) 的理想低通滤波器即可恢复原信号。</p>
    <h3>情况二：混叠</h3>
    <div class="formula">\[\Omega_h>\frac{{\Omega_s}}{{2}}\]</div>
    <figure><figcaption>相邻谱副本发生重叠</figcaption>{overlap}</figure>
    <p>副本相互交叠，原频谱不再能唯一分离；这种不可逆失真称为混叠。</p>
  </section>

  <section>
    <h2>Nyquist–Shannon 时域采样定理</h2>
    <p>若 \(x_a(t)\) 是带限信号，且在 \(\left|\Omega\right|\geq\Omega_h\) 时 \(X_a(j\Omega)=0\)，则样本 \(x(n)=x_a(nT)\) 能唯一确定原信号，当且仅当：</p>
    <div class="formula">\[
      \Omega_s\geq2\Omega_h\qquad\Longleftrightarrow\qquad f_s\geq2f_h
    \]</div>
    <h2>折叠频率与三种频率</h2>
    <p>\(\frac{{\Omega_s}}{{2}}\) 称为折叠频率：超过它的频率成分会折回并造成混叠。连续时间角频率单位为弧度每秒，普通频率单位为赫兹，离散时间数字角频率单位为弧度。</p>
    <div class="formula">\[
      \omega=\Omega T=2\pi\frac{{f}}{{f_s}}
    \]</div>
    <h2>抗混叠滤波</h2>
    <p>实际模拟信号进入模数转换器之前，通常先经过抗混叠滤波器。它的任务是限制输入带宽，使采样后的频谱副本彼此分离，从而避免不可逆的混叠。</p>
  </section>
</main>
"""
    template = r"""<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<script>window.MathJax={tex:{packages:{'[+]':['ams']}}};</script>
<script defer src="__MATHJAX__"></script>
<style>
@page{size:A4;margin:18mm 18mm 20mm}
body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933}
.chapter{max-width:174mm;margin:auto}.chapter>header h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt}
h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin-top:16pt}
h3{color:#315d7d;font-size:12pt;font-weight:400;margin:12pt 0 0}
.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
figure{margin:10pt 0 12pt}figcaption{text-align:center;color:#486d8b;font-size:9.5pt;margin-bottom:3pt}
.spectrum-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.axis{fill:none;stroke:#174b73;stroke-width:2.1;stroke-linecap:round}.guide{stroke:#174b73;stroke-width:1.5}.replica{fill:none;stroke-width:3;stroke-linejoin:round}
.math-label foreignObject div{height:100%;display:flex;justify-content:center;align-items:center;color:#172b3a;font-size:18px}
</style>__CONTENT__</html>"""
    output.write_text(
        template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", content),
        encoding="utf-8",
    )
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
    print(render_pdf(ROOT / "full/outputs/chapter_01_sampling_theorem_mathjax_component.pdf"))
