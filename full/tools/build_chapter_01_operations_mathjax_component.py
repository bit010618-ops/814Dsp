"""Chapter-one operations rendered as complete MathJax formulas and SVG plots."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX
from full.tools.signal_plot_svg import render_stem_svg


ROOT = Path(__file__).resolve().parents[2]


def _stem(output_dir: Path, name: str, samples: dict[int, float], title: str) -> str:
    path = output_dir / f"{name}.svg"
    x_values = tuple(samples)
    render_stem_svg(
        path,
        samples=samples,
        x_label="",
        y_label="",
        title=title,
        x_limits=(min(x_values) - 1.5, max(x_values) + 1.8),
        y_limits=(min(-1, min(samples.values()) - 1), max(2, max(samples.values()) + 1)),
    )
    return path.read_text(encoding="utf-8")


def _figure(svg: str, caption: str) -> str:
    return f'<figure class="chart">{svg}<figcaption>{caption}</figcaption></figure>'


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    charts = {
        "x1": _figure(_stem(output.parent, "operations-x1", {0: 2, 1: 1, 2: 2, 3: 1, 4: 1}, r"\(x_1(n)\)"), "输入序列 1"),
        "x2": _figure(_stem(output.parent, "operations-x2", {0: 1, 1: 1, 2: 1, 3: 1, 4: 1}, r"\(x_2(n)\)"), "输入序列 2"),
        "sum": _figure(_stem(output.parent, "operations-sum", {0: 3, 1: 2, 2: 3, 3: 2, 4: 2}, r"\(x_1(n)+x_2(n)\)"), "逐项相加的结果"),
        "product": _figure(_stem(output.parent, "operations-product", {0: 2, 1: 1, 2: 2, 3: 1, 4: 1}, r"\(x_1(n)x_2(n)\)"), "逐项相乘的结果"),
        "original": _figure(_stem(output.parent, "operations-original", {0: 1, 1: 2, 2: 3}, r"\(x(n)\)"), r"原序列：索引为 \(0,1,2\)"),
        "reversed": _figure(_stem(output.parent, "operations-reversed", {-2: 3, -1: 2, 0: 1}, r"\(x(-n)\)"), r"反褶后：索引为 \(0,-1,-2\)"),
    }
    content = r"""
<main class="chapter">
  <header><h1>离散时间信号的基本运算</h1></header>
  <section>
    <p>本节的基本运算包括：序列的和（积）、移位、反褶、累加和、差分、时间尺度（比例）变换、能量和平均功率。它们均以离散时间索引 \(n\) 为自变量，并按相同索引处的样值定义。</p>
    <h2>序列的和与积</h2>
    <p>两序列在同一索引 \(n\) 处的样值可逐项相加或逐项相乘，分别构成新序列：</p>
    <div class="formula">\[y(n)=x_1(n)+x_2(n),\qquad y(n)=x_1(n)x_2(n)\]</div>
    <div class="chart-grid">__X1____X2____SUM____PRODUCT__</div>
    <p>逐项运算的前提是两个序列使用同一索引 \(n\)。先对齐索引，再做加法或乘法；不能把图上的相邻样点错当为同一时刻。</p>
  </section>
  <section>
    <h2>移位的应用：回声</h2>
    <p>回声由原始声音的延时、衰减副本叠加而成。延时 \(R\) 个采样点意味着使用 \(x(n-R)\)；当 \(0<\alpha<1\) 时，系数 \(\alpha\) 表示回声的衰减。</p>
    <h3>单次回声</h3>
    <div class="formula">\[y(n)=x(n)+\alpha x(n-R),\qquad 0<\alpha<1\]</div>
    <p>当前输出由当前原始样值和 \(R\) 个采样点之前的样值共同决定；\(R\) 越大，听感上的回声间隔越长。</p>
    <h3>多次回声</h3>
    <div class="formula">\[y(n)=x(n)+\alpha x(n-R)+\alpha^2x(n-2R)+\cdots+\alpha^{N-1}x(n-(N-1)R)\]</div>
    <p>第 \(k\) 次回声相对原声延时 \(kR\)，幅度乘以 \(\alpha^k\)；因此在 \(0<\alpha<1\) 时，后续回声会逐次减弱。课件参数示例为回声 1：\(\alpha=0.3,\ R=6000\)；回声 2：\(\alpha=0.3,\ R=10000\)。</p>
  </section>
  <section>
    <h2>序列的反褶</h2>
    <p>序列 \(x(n)\) 的反褶序列定义为 \(y(n)=x(-n)\)。它相当于把横轴索引的正负号互换，因此以 \(n=0\) 为对称轴；\(x(0)\) 在反褶后保持不变。</p>
    <div class="formula">\[y(n)=x(-n)\]</div>
    <div class="chart-grid">__ORIGINAL____REVERSED__</div>
    <p>周期序列应在每一个周期内分别围绕该周期的局部 \(n=0\) 反褶；不能只把整条周期序列按全局坐标镜像。反褶后的移位分别为：</p>
    <div class="formula">\[x(-n+1),\qquad x(-n-1)\]</div>
  </section>
  <section>
    <h2>累加和与差分</h2>
    <p>累加和把从负无穷到当前索引的全部样值累积起来。将相邻两个累加和相减，恰好留下当前样值，因此累加和可写成递推形式。</p>
    <div class="formula">\[
\begin{aligned}
y(n)&=\sum_{k=-\infty}^{n}x(k),\\
y(n)-y(n-1)&=x(n),\\
y(n)&=y(n-1)+x(n).
\end{aligned}
\]</div>
    <p>差分反映序列样值随索引的变化。前向差分比较当前样值和下一样值；后向差分比较当前样值和前一样值。</p>
    <div class="formula">\[\nabla x(n)=x(n+1)-x(n),\qquad \Delta x(n)=x(n)-x(n-1)\]</div>
    <h3>例：矩形序列的后向差分</h3>
    <p>令 \(x(n)=R_{10}(n)\)，即 \(n=0,1,\ldots,9\) 时取 1，其他时刻取 0。\(x(n)\) 与 \(x(n-1)\) 在内部区间相同，只有进入和离开矩形序列时发生变化：</p>
    <div class="formula">\[\Delta R_{10}(n)=R_{10}(n)-R_{10}(n-1)=\{1,0,0,0,0,0,0,0,0,0,-1\}\]</div>
  </section>
  <section>
    <h2>时间尺度、能量与平均功率</h2>
    <h3>时间尺度（比例）变换</h3>
    <p>当 \(m>1\) 为正整数时，\(x(mn)\) 为抽取（下采样）序列，只保留原序列每隔 \(m\) 个索引的样值；\(x\left(\frac{n}{m}\right)\) 为插值（上采样）序列。</p>
    <div class="formula">\[x(n)=\{0,1,2,3,4,5,6\}\Longrightarrow x(2n)=\{0,2,4,6\}\]</div>
    <h3>序列的能量</h3>
    <div class="formula">\[E_x=\sum_{n=-\infty}^{\infty}\left|x(n)\right|^2=\sum_{n=-\infty}^{\infty}x(n)x^*(n)\]</div>
    <p>若 \(E_x=A<\infty\)，则 \(x(n)\) 称为能量有限信号。有限长序列以及绝对可和的无限长序列都是能量信号；\(x^*(n)\) 表示 \(x(n)\) 的复共轭。</p>
    <h3>序列的平均功率</h3>
    <div class="formula">\[P_x=\lim_{N\to\infty}\frac{1}{2N+1}\sum_{n=-N}^{N}\left|x(n)\right|^2\]</div>
    <p>若 \(P_x=C<\infty\)，则 \(x(n)\) 称为功率有限信号。周期信号和随机信号通常在无限时间内存在，因此通常不是能量信号而是功率信号。若 \(x(n)\) 的周期为 \(N\)，只需取一个周期内的样值计算平均功率：</p>
    <div class="formula">\[P_x=\frac{1}{N}\sum_{n=0}^{N-1}\left|x(n)\right|^2\]</div>
  </section>
</main>
"""
    for key, value in charts.items():
        content = content.replace(f"__{key.upper()}__", value)
    template = r"""<!doctype html>
<html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>数字信号处理讲义：离散时间信号的基本运算</title>
<script>window.MathJax={tex:{packages:{'[+]':['ams']}},chtml:{scale:1}};</script>
<script defer src="__MATHJAX__"></script>
<style>
@page { size:A4; margin:18mm 18mm 20mm; }
* { box-sizing:border-box; }
body { margin:0; color:#1f2933; font-family:"Noto Serif CJK SC","Microsoft YaHei",serif; font-size:11pt; line-height:1.75; }
.chapter { max-width:174mm; margin:0 auto; }
h1 { color:#1e4f79; font-size:22pt; font-weight:400; line-height:1.3; border-bottom:1.4pt solid #b56b2e; padding-bottom:8pt; margin:0 0 15pt; }
h2 { color:#1e4f79; font-size:15pt; font-weight:400; border-bottom:.8pt solid #c59d6e; padding-bottom:4pt; margin:20pt 0 8pt; }
h3 { color:#315d7c; font-size:12.5pt; font-weight:400; margin:16pt 0 6pt; }
p { margin:0 0 9pt; }
.formula { background:#f4f7f8; border-radius:5pt; padding:9pt 14pt; margin:10pt 0 13pt; overflow-x:auto; overflow-y:hidden; text-align:center; }
.formula mjx-container[display="true"] { margin:0 !important; }
.chart { margin:10pt auto 16pt; break-inside:avoid; }
.chart svg { display:block; width:100%; height:auto; max-width:720px; margin:0 auto; }
figcaption { text-align:center; color:#596875; font-size:9pt; margin-top:2pt; }
.chart-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9pt; }
@media screen and (max-width:560px) { body { font-size:10.5pt; } .chapter { width:100%; max-width:100%; } .chart { margin-left:0; margin-right:0; } .chart-grid { grid-template-columns:1fr; } }
</style>__CONTENT__</html>"""
    output.write_text(
        template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", content),
        encoding="utf-8",
    )
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
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_01_operations_mathjax_component.pdf"))
