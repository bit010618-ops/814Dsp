"""Convolution basics rendered with complete MathJax formulas and SVG stem plots."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX
from full.tools.signal_plot_svg import render_stem_svg


ROOT = Path(__file__).resolve().parents[2]


def _plot(directory: Path, name: str, samples: dict[int, float], title: str) -> str:
    path = directory / f"convolution-{name}.svg"
    render_stem_svg(
        path, samples=samples, x_label="n", y_label="", title=title,
        x_limits=(min(samples) - 1.2, max(samples) + 1.4),
        y_limits=(-1, max(samples.values()) + 1.5),
    )
    return path.read_text(encoding="utf-8")


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    charts = {
        "X": _plot(output.parent, "x", {0: 1, 1: 2}, "输入序列 x(n)"),
        "H": _plot(output.parent, "h", {0: 3, 1: 2, 2: 1}, "单位脉冲响应 h(n)"),
        "Y": _plot(output.parent, "y", {0: 3, 1: 8, 2: 5, 3: 2}, "输出序列 y(n)"),
    }
    content = r"""
<main class="chapter">
<header><h1>LSI 系统的时域求解：线性卷积</h1></header>
<section><p>同时满足线性和时不变性的离散时间系统称为 LSI 系统。其单位脉冲响应为 \(h(n)=T[\delta(n)]\)；已知输入 \(x(n)\) 与 \(h(n)\)，即可由卷积和得到输出。</p>
<h2>卷积和定义</h2><div class="formula">\[y(n)=x(n)*h(n)=\sum_{m=-\infty}^{\infty}x(m)h(n-m)\]</div>
<p>固定 \(n\) 后，求和变量 \(m\) 遍历所有整数：先将 \(h(m)\) 反褶并移位成 \(h(n-m)\)，再与 \(x(m)\) 在相同索引处相乘并累加。</p>
<h2>由单位脉冲分解导出卷积和</h2><div class="formula">\[x(n)=\sum_{m=-\infty}^{\infty}x(m)\delta(n-m)\]</div>
<div class="formula">\[T[x(n)]=\sum_{m=-\infty}^{\infty}x(m)h(n-m)\]</div>
<h2>图解计算步骤</h2><p>按“反褶、移位、相乘、相加”依次进行。有限长序列卷积的长度为 \(L_x+L_h-1\)，可据此核对首尾项。</p>
<div class="formula">\[x(n)*\delta(n-n_0)=x(n-n_0)\]</div></section>
<section><h2>例题</h2><p>已知某 LSI 系统的单位脉冲响应 \(h(n)\) 为：</p><div class="formula">\[h(n)=3\delta(n)+2\delta(n-1)+\delta(n-2)\]</div>
<p>若该系统的输入为序列 \(x(n)\)：</p><div class="formula">\[x(n)=\delta(n)+2\delta(n-1)\]</div><p>试求该系统的输出响应 \(y(n)\)。</p>
<div class="grid">__X____H__</div></section>
<section><h2>例题详解</h2><p>\(n=0\) 时 \(y(0)=1\cdot3=3\)；\(n=1\) 时 \(y(1)=1\cdot2+2\cdot3=8\)；\(n=2\) 时 \(y(2)=1\cdot1+2\cdot2=5\)；\(n=3\) 时 \(y(3)=2\cdot1=2\)。</p>
<div class="formula">\[y(n)=3\delta(n)+8\delta(n-1)+5\delta(n-2)+2\delta(n-3)\]</div><figure>__Y__<figcaption>输出长度为 \(2+3-1=4\)，与计算结果一致。</figcaption></figure>
<p>也可由脉冲分解直接计算：\(y(n)=h(n)+2h(n-1)\)，代入同一 \(h(n)\) 后得到相同结果。</p></section>
</main>""".replace("__X__", charts["X"]).replace("__H__", charts["H"]).replace("__Y__", charts["Y"])
    template = r"""<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={tex:{packages:{'[+]':['ams']}}};</script><script defer src="__MATHJAX__"></script><style>@page{size:A4;margin:18mm 18mm 20mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933}.chapter{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.grid{display:grid;grid-template-columns:1fr 1fr;gap:12pt}figure{margin:12pt 0;text-align:center}figcaption{color:#315d7c}@media(max-width:560px){.grid{grid-template-columns:1fr}}</style>__CONTENT__</html>"""
    output.write_text(template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", content), encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_01_convolution_basics_mathjax_component.pdf"))
