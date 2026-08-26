"""Convolution properties rendered through complete MathJax formulas."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX

ROOT = Path(__file__).resolve().parents[2]


def delay_superposition_svg() -> str:
    """Return the source-equivalent two-path delay-and-sum system diagram."""
    return r'''<figure class="system-figure" aria-label="延时叠加系统结构图">
<svg id="delay-superposition-diagram" role="img" aria-labelledby="delay-superposition-title" viewBox="0 0 860 310" xmlns="http://www.w3.org/2000/svg">
  <title id="delay-superposition-title">延时叠加系统：输入分成直通支路与延时衰减支路后，在求和器汇合为输出</title>
  <defs><marker id="delay-arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="#1f557d"/></marker></defs>
  <rect x="18" y="18" width="824" height="250" rx="10" fill="#f7fafb" stroke="#c8d7e0" stroke-width="2"/>
  <text x="430" y="48" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="17" fill="#314b60">延时叠加系统的两支路实现</text>
  <line x1="72" y1="156" x2="160" y2="156" stroke="#1f557d" stroke-width="3" marker-end="url(#delay-arrow)"/>
  <text x="74" y="140" font-family="Times New Roman, serif" font-style="italic" font-size="23" fill="#1f2933">x(n)</text>
  <circle cx="160" cy="156" r="5.5" fill="#1f557d"/>
  <path d="M160 156 V98 H238" fill="none" stroke="#1f557d" stroke-width="3" marker-end="url(#delay-arrow)"/>
  <path d="M160 156 V226 H238" fill="none" stroke="#1f557d" stroke-width="3" marker-end="url(#delay-arrow)"/>
  <rect x="238" y="68" width="175" height="60" rx="7" fill="#f7fbfd" stroke="#0495a2" stroke-width="2"/>
  <text x="325.5" y="92" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="16" fill="#1f2933">直通支路</text>
  <text x="325.5" y="113" text-anchor="middle" font-family="Times New Roman, serif" font-size="20" fill="#1f2933">H₁(z)</text>
  <rect x="238" y="196" width="175" height="60" rx="7" fill="#f7fbfd" stroke="#0495a2" stroke-width="2"/>
  <text x="325.5" y="220" text-anchor="middle" font-family="Microsoft YaHei, sans-serif" font-size="16" fill="#1f2933">延时衰减支路</text>
  <text x="325.5" y="241" text-anchor="middle" font-family="Times New Roman, serif" font-size="20" fill="#1f2933">H₂(z)</text>
  <line x1="413" y1="98" x2="605" y2="98" stroke="#1f557d" stroke-width="3"/>
  <line x1="605" y1="98" x2="635" y2="137" stroke="#1f557d" stroke-width="3" marker-end="url(#delay-arrow)"/>
  <line x1="413" y1="226" x2="605" y2="226" stroke="#1f557d" stroke-width="3"/>
  <line x1="605" y1="226" x2="635" y2="175" stroke="#1f557d" stroke-width="3" marker-end="url(#delay-arrow)"/>
  <text x="477" y="86" font-family="Times New Roman, serif" font-style="italic" font-size="18" fill="#1f2933">w₁(n)=x(n)</text>
  <text x="454" y="251" font-family="Times New Roman, serif" font-style="italic" font-size="18" fill="#1f2933">w₂(n)=αx(n−R)</text>
  <circle cx="664" cy="156" r="31" fill="#fff" stroke="#1f557d" stroke-width="3"/>
  <text x="664" y="165" text-anchor="middle" font-family="Times New Roman, serif" font-size="31" fill="#1f2933">Σ</text>
  <line x1="695" y1="156" x2="794" y2="156" stroke="#1f557d" stroke-width="3" marker-end="url(#delay-arrow)"/>
  <text x="755" y="140" font-family="Times New Roman, serif" font-style="italic" font-size="23" fill="#1f2933">y(n)</text>
</svg><figcaption>图 1-11　延时叠加系统的标准结构图：两条支路在求和器处汇合。</figcaption></figure>'''


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main class="chapter"><header><h1>线性卷积的运算规则</h1></header>
<section class="properties-intro"><p>卷积满足交换律、结合律和分配律，分别对应 LSI 系统级联顺序可交换、多个级联系统可合并及并联系统可合并。</p>
<h2>交换律、结合律与分配律</h2>
<div class="formula">\[x(n)*h(n)=h(n)*x(n)\]</div>
 </section>
<section>
<div class="formula">\[\bigl[x(n)*h_1(n)\bigr]*h_2(n)=x(n)*\bigl[h_1(n)*h_2(n)\bigr]\]</div>
<div class="formula">\[x(n)*[h_1(n)+h_2(n)]=x(n)*h_1(n)+x(n)*h_2(n)\]</div>
<h2>有限支持序列的卷积区间</h2><p>例 1：有两个序列 \(x(n)\) 和 \(h(n)\)。\(x(n)\) 不为零的区间为 \(N_1\leq n\leq N_2\)，\(h(n)\) 不为零的区间为 \(N_3\leq n\leq N_4\)。设 \(y(n)=x(n)*h(n)\)，问 \(y(n)\) 不为零的区间为：______。</p>
<div class="formula">\[x(m)\ne0:\ N_1\leq m\leq N_2,\qquad h(n-m)\ne0:\ n-N_4\leq m\leq n-N_3\]</div>
<p>第一次重叠发生在 \(n=N_1+N_3\)，最后一次重叠发生在 \(n=N_2+N_4\)，因此：</p>
<div class="formula">\[N_1+N_3\leq n\leq N_2+N_4\]</div>
<div class="formula">\[L_y=L_x+L_h-1\]</div></section>
<section><h2>应用例：延时叠加系统</h2><p>某 LSI 系统的单位脉冲响应为 \(h(n)=\delta(n)+\alpha\delta(n-R)\)，其中 \(0<\alpha<1\)，\(R\) 为正整数。</p>
<div class="formula">\[\begin{aligned}y(n)&=x(n)*[\delta(n)+\alpha\delta(n-R)]\\&=x(n)+\alpha x(n-R).\end{aligned}\]</div>
<p>第一项是原信号，第二项是延迟 \(R\) 个采样点、幅度缩小为 \(\alpha\) 倍的副本。\(R\) 决定延迟，\(\alpha\) 决定回声强度。</p>{delay_superposition_svg()}
<h2>实序列的相关：相似度与延时</h2><p>相关函数衡量两个序列在不同相对位移下的相似程度。计算中同样包含反褶、移位、相乘和相加，但其意义是“对齐后有多像”。</p>
<div class="formula">\[r_{xy}(n)=x(n)*y(-n),\qquad r_{yx}(n)=y(n)*x(-n)\]</div>
<div class="formula">\[r_{xx}(n)=x(n)*x(-n)\]</div>
<p>若 \(y(n)=x(n-2)+w(n)\)，其中 \(w(n)\) 为零均值噪声，则 \(r_{yx}(n)\) 在 \(n=2\) 附近出现显著峰值；这表明 \(y(n)\) 与延迟两点的 \(x(n)\) 最相似。</p></section></main>"""
    template = r"""<!doctype html><html lang="zh-CN"><meta charset="utf-8"><script>window.MathJax={tex:{packages:{'[+]':['ams']}}};</script><script defer src="__MATHJAX__"></script><style>@page{size:A4;margin:18mm 18mm 20mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933}.chapter{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.system-figure{margin:14pt 0;text-align:center}.system-figure svg{display:block;width:100%;height:auto}.system-figure figcaption{margin-top:5pt;color:#52697a;font-size:9.5pt;text-align:center}</style>__CONTENT__</html>"""
    rendered_content = content.replace("{delay_superposition_svg()}", delay_superposition_svg())
    output.write_text(template.replace("__MATHJAX__", MATHJAX).replace("__CONTENT__", rendered_content), encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_01_convolution_properties_mathjax_component.pdf"))
