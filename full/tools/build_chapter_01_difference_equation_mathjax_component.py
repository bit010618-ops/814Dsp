"""Difference-equation material rendered as complete MathJax formulae."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def feedback_structure_svg() -> str:
    """Return a coordinate-driven SVG for y(n)=b0*x(n)-a1*y(n-1)."""
    return r"""
<svg class="structure-svg" viewBox="0 0 860 270" role="img"
     aria-label="一阶反馈系统结构图">
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4"
            orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#174b73"/></marker>
  </defs>
  <g class="wire" marker-end="url(#arrow)">
    <path d="M45 88 H170"/><path d="M290 88 H398"/>
    <path d="M474 88 H785"/>
    <path d="M660 104 V205"/><path d="M540 205 H460"/>
    <path d="M340 205 H305 V122 H398"/>
  </g>
  <circle class="sum" cx="436" cy="88" r="38"/>
  <text class="sum-sign" x="422" y="82">+</text>
  <text class="sum-sign" x="422" y="112">−</text>
  <rect class="block" x="170" y="55" width="120" height="66" rx="8"/>
  <rect class="block" x="540" y="172" width="120" height="66" rx="8"/>
  <rect class="block" x="340" y="172" width="120" height="66" rx="8"/>
  <g class="math-label">
    <foreignObject x="55" y="47" width="90" height="40"><div>\(x(n)\)</div></foreignObject>
    <foreignObject x="195" y="69" width="70" height="38"><div>\(b_0\)</div></foreignObject>
    <foreignObject x="560" y="186" width="82" height="38"><div>\(z^{-1}\)</div></foreignObject>
    <foreignObject x="360" y="186" width="80" height="38"><div>\(-a_1\)</div></foreignObject>
    <foreignObject x="720" y="47" width="90" height="40"><div>\(y(n)\)</div></foreignObject>
  </g>
  <circle class="branch" cx="660" cy="88" r="5"/>
</svg>
"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    structure = feedback_structure_svg()
    content = rf"""
<main class="chapter">
  <header><h1>常系数线性差分方程</h1></header>
  <section>
    <p>常系数线性差分方程以过去和当前的输入、输出样值建立关系，是离散时间系统的重要表示方法：</p>
    <div class="formula">\[
      \sum_{{k=0}}^{{N}}a_k y(n-k)=\sum_{{m=0}}^{{M}}b_m x(n-m),
      \qquad a_0\ne 0
    \]</div>
    <h2>三个术语</h2>
    <p>常系数指 \(a_k\) 与 \(b_m\) 都是常数；阶数是输出项 \(y(n)\) 中最大、最小序号之差；线性指各输入、输出样值只出现一次幂且没有相乘项。这里“线性”的含义不同于系统线性。</p>
    <h2>四种求解思路</h2>
    <p>可用齐次解、特解和边界条件求待定系数；也可逐项迭代、转入 \(z\) 域，或先求单位脉冲响应 \(h(n)\) 后再与 \(x(n)\) 卷积。</p>
  </section>

  <section>
    <h2>迭代法：因果单位脉冲响应</h2>
    <p>考虑一阶差分方程 \(y(n)-a y(n-1)=x(n)\)。令 \(x(n)=\delta(n)\)，并采用零状态边界条件 \(h(n)=0\;(n<0)\)。</p>
    <div class="formula">\[
      \begin{{aligned}}
      h(0)&=1,\qquad h(1)=a,\qquad h(2)=a^2,\\
      h(n)&=a h(n-1)=a^n u(n).
      \end{{aligned}}
    \]</div>
    <p>此解因果；当 \(\left|a\right|<1\) 时，\(h(n)\) 绝对可和，系统还稳定。</p>
    <h2>迭代法：非因果单位脉冲响应</h2>
    <p>对同一方程，若采用另一边界条件 \(h(n)=0\;(n>0)\)，从反向递推关系出发：</p>
    <div class="formula">\[
      \begin{{aligned}}
      y(n-1)&=a^{{-1}}\left[y(n)-x(n)\right],\\
      h(0)&=0,\qquad h(-1)=-a^{{-1}},\qquad h(-2)=-a^{{-2}},\\
      h(n)&=-a^n u(-n-1).
      \end{{aligned}}
    \]</div>
    <p>该响应在负时间一侧存在非零值，因此系统非因果。同一差分方程在不同边界条件下可对应不同的单位脉冲响应。</p>
  </section>

  <section>
    <h2>由差分方程得到系统结构</h2>
    <p>以一阶关系为例：</p>
    <div class="formula">\[
      y(n)=b_0x(n)-a_1y(n-1)
    \]</div>
    <p>下图以标准加法器、增益块、延时器和反馈支路表示该关系；每一条支路都对应方程中的一项。</p>
    <div class="diagram">{structure}</div>
    <p>输入经 \(b_0\) 进入求和器；输出由分支点取出，经 \(z^{{-1}}\) 延迟和 \(-a_1\) 加权后反馈到负输入端。由图反向写出的差分方程与上式一致。</p>
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
.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.diagram{background:#f8fafb;border:1px solid #d8e0e5;border-radius:5pt;padding:8pt;margin:10pt 0}
.structure-svg{display:block;width:100%;height:auto}.wire{fill:none;stroke:#174b73;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}.block{fill:#f4f7f8;stroke:#0d8794;stroke-width:2}.sum{fill:#fff;stroke:#174b73;stroke-width:2.4}.branch{fill:#174b73}.sum-sign{font:24px "Times New Roman",serif;fill:#174b73}.math-label foreignObject div{height:100%;display:flex;justify-content:center;align-items:center;color:#172b3a;font-size:20px}
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
    print(render_pdf(ROOT / "full/outputs/chapter_01_difference_equation_mathjax_component.pdf"))
