"""Chapter-one representation component rendered only by MathJax and true SVG."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX
from full.tools.signal_plot_svg import render_stem_svg


ROOT = Path(__file__).resolve().parents[2]


def _stem(output_dir: Path, name: str, samples: dict[int, float], title: str) -> str:
    svg_path = output_dir / f"{name}.svg"
    x_values = tuple(samples)
    render_stem_svg(
        svg_path,
        samples=samples,
        x_label="",
        y_label="",
        title=title,
        x_limits=(min(x_values) - 1.5, max(x_values) + 2),
        y_limits=(min(-1, min(samples.values()) - 1), max(2, max(samples.values()) + 1)),
    )
    return svg_path.read_text(encoding="utf-8")


def _chart(svg: str, *, x_label: str = r"\(n\)", y_label: str = r"\(x(n)\)") -> str:
    return f'<figure class="chart">{svg}<figcaption>{y_label} 随离散时间 {x_label} 的取值</figcaption></figure>'


def write_html(output: Path) -> Path:
    """Create the complete, naturally flowing representation-method component."""
    output.parent.mkdir(parents=True, exist_ok=True)
    charts = {
        "sequence": _chart(
            _stem(
                output.parent,
                "representation-sequence",
                {-1: 1, 0: 2, 1: 1, 2: 2, 3: 3, 4: 1, 5: -2, 6: 2, 7: -1, 8: 3, 9: 2},
                "离散序列的图形表示",
            )
        ),
        "impulse": _chart(
            _stem(output.parent, "representation-impulse", {0: 1}, "单位抽样序列"),
            y_label=r"\(\delta(n)\)",
        ),
        "term0": _chart(
            _stem(output.parent, "representation-term0", {0: 1}, r"\(\delta(n)\)"),
            y_label=r"\(\delta(n)\)",
        ),
        "term1": _chart(
            _stem(output.parent, "representation-term1", {1: 2}, r"\(2\delta(n-1)\)"),
            y_label=r"\(2\delta(n-1)\)",
        ),
        "sum": _chart(
            _stem(output.parent, "representation-sum", {0: 1, 1: 2, 2: 3}, r"\(x(n)\)"),
        ),
    }
    content = r"""
<main class="chapter">
  <header>
    <p class="eyebrow">第一章 离散时间信号与系统</p>
    <h1>离散时间信号的表示方法</h1>
  </header>
  <section>
    <h2>用数列与函数表示</h2>
    <p>三组数值相同的数列并不一定代表同一序列：必须用下划线明确 \(n=0\) 对应的项。用函数表示时，\(n\) 只取整数，因此条件 \(n<0\) 与 \(n\leq-1\) 对离散序列是等价的。</p>
    <div class="formula">\[
    x_1(n)=\{1,2,3,4,5\},\qquad
    x_2(n)=\{1,2,3,4,5\},\qquad
    x_3(n)=\{0,0,1,2,3\}.
    \]</div>
    <div class="formula">\[x_4(n)=A\sin(\omega n+\varphi),\quad n\in(-\infty,\infty)\]</div>
  </section>
  <section>
    <h2>用图形表示离散时间信号</h2>
    <p>图形的横坐标 \(n\) 表示离散时间坐标，仅在 \(n\) 为整数时有意义；纵坐标表示各信号点的值。下图给出同一序列的标准 stem 图表示。</p>
    __SEQUENCE__
  </section>
  <section>
    <h2>用单位抽样序列表示</h2>
    <p>单位抽样序列 \(\delta(n)\) 是脉冲幅度为 1 的离散序列。它只有在 \(n=0\) 时取 1，在其他整数时刻均取 0：</p>
    <div class="formula">\[
\delta(n)=
\begin{cases}
1, & n=0,\\
0, & n\ne 0.
\end{cases}
\]</div>
    __IMPULSE__
  </section>
  <section>
    <h2>单位抽样序列的移位加权和</h2>
    <p>任何序列都可以表示为单位抽样序列的移位加权和：\(x(m)\) 给出第 \(m\) 个样点的值，\(\delta(n-m)\) 给出该样点所在的位置。</p>
    <div class="formula">\[x(n)=\sum_{m=-\infty}^{\infty}x(m)\delta(n-m)\]</div>
    <h3>例：用单位抽样序列 \(\delta(n)\) 表示任意序列 \(x(n)=\{1,2,3\}\)</h3>
    <p>数列中第一项为 \(n=0\)，因此 \(x(0)=1\)、\(x(1)=2\)、\(x(2)=3\)。将三个样点分别平移到 0、1、2 处并按幅值加权。</p>
    <div class="chart-grid">__TERM0____TERM1____SUM__</div>
    <div class="formula">\[
x(n)=\delta(n)+2\delta(n-1)+3\delta(n-2)
=\sum_{m=0}^{2}x(m)\delta(n-m)
\]</div>
    <p>展开时，“值”写在 \(x(m)\) 前，“位置”由 \(\delta(n-m)\) 决定。逐项代入 \(n=0,1,2\)，应分别得到 1、2、3。</p>
  </section>
</main>
"""
    for key, chart in charts.items():
        content = content.replace(f"__{key.upper()}__", chart)

    template = r"""<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>数字信号处理讲义：离散时间信号的表示方法</title>
<script>
window.MathJax = {tex: {packages: {'[+]': ['ams']}}, chtml: {scale: 1}};
</script>
<script defer src="__MATHJAX__"></script>
<style>
@page { size: A4; margin: 18mm 18mm 20mm; }
* { box-sizing: border-box; }
body { margin:0; color:#1f2933; font-family:"Noto Serif CJK SC","Microsoft YaHei",serif; font-size:11pt; line-height:1.75; }
.chapter { max-width: 174mm; margin:0 auto; }
.eyebrow { color:#62717d; font-size:9pt; border-bottom:1px solid #c9d1d7; padding-bottom:4pt; margin:0 0 13pt; }
h1 { color:#1e4f79; font-size:22pt; font-weight:400; line-height:1.3; border-bottom:1.4pt solid #b56b2e; padding-bottom:8pt; margin:0 0 15pt; }
h2 { color:#1e4f79; font-size:15pt; font-weight:400; border-bottom:0.8pt solid #c59d6e; padding-bottom:4pt; margin:20pt 0 8pt; }
h3 { color:#315d7c; font-size:12.5pt; font-weight:400; margin:16pt 0 6pt; }
p { margin:0 0 9pt; }
.formula { background:#f4f7f8; border-radius:5pt; padding:9pt 14pt; margin:10pt 0 13pt; overflow-x:auto; overflow-y:hidden; text-align:center; }
.formula mjx-container[display="true"] { margin:0 !important; }
.chart { margin:10pt auto 16pt; break-inside:avoid; }
.chart svg { display:block; width:100%; height:auto; max-width:720px; margin:0 auto; }
figcaption { text-align:center; color:#596875; font-size:9pt; margin-top:2pt; }
.chart-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9pt; }
.chart-grid figure:last-child { grid-column:1 / -1; }
@media screen and (max-width: 560px) { body { font-size:10.5pt; } .chapter { width:100%; max-width:100%; } .chart { margin-left:0; margin-right:0; } .chart-grid { grid-template-columns:1fr; } .chart-grid figure:last-child { grid-column:auto; } }
</style>
__CONTENT__
</html>"""
    page = template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", content)
    output.write_text(page, encoding="utf-8")
    return output


def render_pdf(output: Path, *, wait_ms: int = 10000) -> Path:
    """Print the component through Edge after MathJax has completed layout."""
    if not EDGE.exists():
        raise FileNotFoundError(f"Microsoft Edge is required: {EDGE}")
    html_path = write_html(output.with_suffix(".html"))
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(EDGE), "--headless=new", "--disable-gpu", "--no-first-run",
            "--no-pdf-header-footer", f"--virtual-time-budget={wait_ms}",
            f"--print-to-pdf={output.resolve()}", html_path.resolve().as_uri(),
        ],
        check=True,
    )
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_01_representation_mathjax_component.pdf"))
