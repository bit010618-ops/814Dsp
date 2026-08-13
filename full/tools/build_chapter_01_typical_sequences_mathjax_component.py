"""Typical discrete sequences rendered with MathJax and data-driven SVG."""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX
from full.tools.signal_plot_svg import render_stem_svg


ROOT = Path(__file__).resolve().parents[2]


def _stem(output_dir: Path, name: str, samples: dict[int, float], title: str) -> str:
    path = output_dir / f"{name}.svg"
    xs = tuple(samples)
    render_stem_svg(
        path,
        samples=samples,
        x_label="",
        y_label="",
        title=title,
        x_limits=(min(xs) - 1.5, max(xs) + 1.8),
        y_limits=(min(-1, min(samples.values()) - .6), max(1.5, max(samples.values()) + .6)),
    )
    return path.read_text(encoding="utf-8")


def _figure(svg: str, caption: str) -> str:
    return f'<figure class="chart">{svg}<figcaption>{caption}</figcaption></figure>'


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    sine = {n: round(math.sin(.2 * math.pi * n), 4) for n in range(10)}
    complex_values = {n: round(2 * math.exp(-n / 12), 4) for n in range(13)}
    charts = {
        "impulse": _figure(_stem(output.parent, "typical-impulse", {0: 1}, r"\(\delta(n)\)"), r"单位抽样序列"),
        "step": _figure(_stem(output.parent, "typical-step", {-2: 0, -1: 0, 0: 1, 1: 1, 2: 1, 3: 1}, r"\(u(n)\)"), r"单位阶跃序列"),
        "rectangle": _figure(_stem(output.parent, "typical-rectangle", {-1: 0, 0: 1, 1: 1, 2: 1, 3: 1, 4: 0}, r"\(R_4(n)\)"), r"矩形序列"),
        "decay": _figure(_stem(output.parent, "typical-decay", {n: round(.7**n, 4) for n in range(8)}, r"\(0.7^n u(n)\)"), r"收敛的实指数序列"),
        "alternate": _figure(_stem(output.parent, "typical-alternate", {n: round((-.7)**n, 4) for n in range(8)}, r"\((-0.7)^n u(n)\)"), r"正负交替的实指数序列"),
        "sine": _figure(_stem(output.parent, "typical-sine", sine, r"\(\sin(0.2\pi n)\)"), r"十个样点构成一个周期"),
        "real": _figure(_stem(output.parent, "typical-complex-real", {n: round(complex_values[n] * math.cos(math.pi*n/6), 4) for n in complex_values}, r"\(\operatorname{Re}\{x(n)\}\)"), r"复指数序列的实部"),
        "imag": _figure(_stem(output.parent, "typical-complex-imag", {n: round(complex_values[n] * math.sin(math.pi*n/6), 4) for n in complex_values}, r"\(\operatorname{Im}\{x(n)\}\)"), r"复指数序列的虚部"),
        "magnitude": _figure(_stem(output.parent, "typical-complex-magnitude", complex_values, r"\(\left|x(n)\right|\)"), r"复指数序列的模"),
    }
    content = r"""
<main class="chapter">
  <header><h1>几种常用的典型序列</h1></header>
  <section>
    <p>本节依课程顺序介绍单位抽样、单位阶跃、矩形、实指数、正弦和复指数序列；以下保留各序列的基础定义、关系与性质。</p>
    <h2>单位抽样序列</h2>
    <div class="formula">\[
\delta(n)=
\begin{cases}
1, & n=0,\\
0, & n\ne0.
\end{cases}
\]</div>
    <div class="next-page">
    <p>\(\delta(n)\) 是脉冲幅度为 1 的离散序列，也称单位脉冲序列或时域离散冲激；它不同于连续时间的 \(\delta(t)\) 数学极限。</p>
    __IMPULSE__
    <h2>单位阶跃序列</h2>
    <div class="formula">\[
u(n)=
\begin{cases}
1, & n\geq0,\\
0, & n<0.
\end{cases}
\]</div>
    <div class="formula">\[\delta(n)=u(n)-u(n-1),\qquad u(n)=\sum_{k=-\infty}^{n}\delta(k)\]</div>
    __STEP__
    </div>
  </section>
  <section class="typical-sequence-continuation">
    <h2>矩形序列</h2>
    <div class="formula">\[
R_N(n)=
\begin{cases}
1, & 0\leq n\leq N-1,\\
0, & n\notin[0,N-1].
\end{cases}
\]</div>
    <div class="formula">\[R_N(n)=u(n)-u(n-N),\qquad R_N(n)=\sum_{m=0}^{N-1}\delta(n-m)\]</div>
    <p>矩形序列在索引 0 至 \(N-1\) 取 1，其余索引取 0；它可等价地由两个阶跃序列相减，或由 \(N\) 个移位单位抽样序列求和得到。</p>
    __RECTANGLE__
    <h2>实指数序列</h2>
    <div class="formula">\[x(n)=a^n u(n)\]</div>
    <p>当 \(\left|a\right|<1\) 时，样值随 \(n\) 增大而衰减；当 \(\left|a\right|\geq1\) 时发散。若 \(a<0\)，样值符号交替，呈摇动特征。</p>
    <div class="chart-grid">__DECAY____ALTERNATE__</div>
  </section>
  <section>
    <h2>正弦序列</h2>
    <div class="formula">\[x(n)=A\sin(n\omega+\varphi),\qquad x(n)=A\cos(n\omega+\varphi)\]</div>
    <div class="formula">\[\omega=\Omega T=2\pi\frac{f_0}{f_s}\]</div>
    <p>连续时间正弦信号经等间隔 \(T\) 采样后得到正弦序列。\(\omega\) 为数字角频率（rad），\(\Omega\) 为模拟角频率（rad/s），二者通过 \(\omega=\Omega T\) 联系。</p>
    <p>\(\omega=0.2\pi\) 表示相邻样值的相位差为 \(0.2\pi\) rad，因此一个完整周期包含 \(\frac{2\pi}{0.2\pi}=10\) 个采样点。数字角频率是相对频率，而非模拟角频率的单位。</p>
    __SINE__
  </section>
  <section>
    <h2>复指数序列</h2>
    <div class="formula">\[x(n)=e^{(\sigma+j\omega)n}=e^{\sigma n}\left[\cos(\omega n)+j\sin(\omega n)\right]\]</div>
    <div class="formula">\[e^{\pm jx}=\cos x\pm j\sin x\]</div>
    <p>复指数序列的实部与虚部分别是同一数字角频率的余弦和正弦序列；指数因子 \(e^{\sigma n}\) 决定其包络。</p>
    <div class="formula">\[\operatorname{Re}\{x(n)\}=e^{\sigma n}\cos(\omega n),\quad \operatorname{Im}\{x(n)\}=e^{\sigma n}\sin(\omega n),\quad \left|x(n)\right|=e^{\sigma n}\]</div>
    <p>例如，对 \(x(n)=2e^{(-\frac{1}{12}+j\frac{\pi}{6})n}\)，实部与虚部为衰减振荡，而模值按指数规律衰减。</p>
    <div class="chart-grid">__REAL____IMAG____MAGNITUDE__</div>
  </section>
</main>
"""
    for key, chart in charts.items():
        content = content.replace(f"__{key.upper()}__", chart)
    template = r"""<!doctype html>
<html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>数字信号处理讲义：几种常用的典型序列</title>
<script>window.MathJax={tex:{packages:{'[+]':['ams']}},chtml:{scale:1}};</script>
<script defer src="__MATHJAX__"></script>
<style>
@page { size:A4; margin:18mm 18mm 20mm; }
* { box-sizing:border-box; }
body { margin:0; color:#1f2933; font-family:"Noto Serif CJK SC","Microsoft YaHei",serif; font-size:11pt; line-height:1.75; }
.chapter { max-width:174mm; margin:0 auto; }
h1 { color:#1e4f79; font-size:22pt; font-weight:400; line-height:1.3; border-bottom:1.4pt solid #b56b2e; padding-bottom:8pt; margin:0 0 15pt; }
h2 { color:#1e4f79; font-size:15pt; font-weight:400; border-bottom:.8pt solid #c59d6e; padding-bottom:4pt; margin:20pt 0 8pt; }
p { margin:0 0 9pt; }
.formula { background:#f4f7f8; border-radius:5pt; padding:9pt 14pt; margin:10pt 0 13pt; overflow-x:auto; overflow-y:hidden; text-align:center; }
.formula mjx-container[display="true"] { margin:0 !important; }
.chart { margin:10pt auto 16pt; break-inside:avoid; }
.chart svg { display:block; width:100%; height:auto; max-width:720px; margin:0 auto; }
figcaption { text-align:center; color:#596875; font-size:9pt; margin-top:2pt; }
.chart-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9pt; }
.chart-grid figure:last-child { grid-column:1 / -1; }
@media screen and (max-width:560px) { body { font-size:10.5pt; } .chapter { width:100%; max-width:100%; } .chart { margin-left:0; margin-right:0; } .chart-grid { grid-template-columns:1fr; } .chart-grid figure:last-child { grid-column:auto; } }
</style>__CONTENT__</html>"""
    output.write_text(template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", content), encoding="utf-8")
    return output


def render_pdf(output: Path, *, wait_ms: int = 10000) -> Path:
    if not EDGE.exists():
        raise FileNotFoundError(f"Microsoft Edge is required: {EDGE}")
    html = write_html(output.with_suffix(".html"))
    subprocess.run(
        [str(EDGE), "--headless=new", "--disable-gpu", "--no-first-run",
         "--no-pdf-header-footer", f"--virtual-time-budget={wait_ms}",
         f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()],
        check=True,
    )
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_01_typical_sequences_mathjax_component.pdf"))
