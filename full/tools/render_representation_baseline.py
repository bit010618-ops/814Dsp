"""First chapter baseline page using the unified MathJax and SVG paths."""
from __future__ import annotations

from pathlib import Path

from full.tools.signal_plot_svg import render_stem_svg


MATHJAX = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"


def write_html(output: Path) -> Path:
    """Write a print-ready baseline page for the unit-sample representation."""
    output.parent.mkdir(parents=True, exist_ok=True)
    svg_path = output.with_name("representation-stem.svg")
    render_stem_svg(
        svg_path,
        samples={0: 1, 1: 2, 2: 3, 5: -2},
        x_label="",
        y_label="",
        title="离散序列的图形表示",
        x_limits=(-1, 11),
        y_limits=(-3, 4),
    )
    svg = svg_path.read_text(encoding="utf-8")
    page = f"""<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>数字信号处理讲义：表示方法</title>
<script>
window.MathJax = {{tex: {{packages: {{'[+]': ['ams']}}}}, chtml: {{scale: 1}}}};
</script>
<script defer src="{MATHJAX}"></script>
<style>
@page {{ size:A4; margin:18mm; }}
* {{ box-sizing:border-box; }}
body {{ color:#1f2933; font-family:"Noto Serif CJK SC","Microsoft YaHei",serif; margin:0; padding:16px; overflow-x:hidden; }}
h1 {{ color:#1e4f79; font-weight:400; border-bottom:1px solid #bd862f; padding-bottom:8px; }}
.formula {{ background:#f4f7f8; border-radius:5px; padding:15px 20px; overflow-x:auto; }}
.chart {{ position:relative; margin-top:14px; }}
.chart svg {{ width:100%; max-width:720px; }}
.chart .x-label {{ position:absolute; right:2%; bottom:18%; }}
.chart .y-label {{ position:absolute; left:33%; top:12%; }}
</style>
<main>
<h1>用单位抽样序列表示</h1>
<p>单位抽样序列 \\(\\delta(n)\\) 是脉冲幅度为 1 的离散序列。它只在 \\(n=0\\) 时取 1，在其他整数时刻均取 0：</p>
<section class="formula">\\[
\\delta(n)=
\\begin{{cases}}
1, & n=0,\\\\
0, & n\\ne 0.
\\end{{cases}}
\\]</section>
<h2>用图形表示离散时间信号</h2>
<p>横坐标 \\(n\\) 表示离散时间坐标，仅在整数位置有意义；纵坐标表示各信号点的取值。离散序列采用 stem 图表示。</p>
<section class="chart">{svg}<span class="x-label">\\(n\\)</span><span class="y-label">\\(x(n)\\)</span></section>
</main></html>"""
    output.write_text(page, encoding="utf-8")
    return output
