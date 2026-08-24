"""Periodicity material rendered only through complete MathJax formulas."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main class="chapter">
  <header><h1>离散时间序列的周期性</h1></header>
  <section>
    <p>本节先给出周期序列的定义，再说明正弦序列何时为周期序列，并建立从数字角频率求最小正周期的统一方法。</p>
    <h2>周期序列的定义</h2>
    <div class="formula">\[x(n+N)=x(n),\quad n\in\mathbb{Z},\quad N\in\mathbb{Z}_{+}\]</div>
    <p>若存在满足上式的最小正整数 \(N\)，则 \(x(n)\) 为周期序列，\(N\) 称为它的基本周期。定义必须对所有整数 \(n\) 成立。</p>
    <h2>正弦序列的周期性</h2>
    <div class="formula">\[x(n)=A\sin(n\omega+\varphi),\qquad N\omega=2k\pi\]</div>
    <p>由 \(x(n+N)=A\sin[(n+N)\omega+\varphi]\) 可知，只有当 \(N\omega\) 是 \(2\pi\) 的整数倍时，相移才不改变每一个样值。</p>
    <div class="formula">\[N=\frac{2\pi k}{\omega},\qquad k\in\mathbb{Z}_{+}\]</div>
    <h3>整数周期的情形</h3>
    <p>当 \(\frac{2\pi}{\omega}\) 本身为整数时，取 \(k=1\) 即得到基本周期。它也说明：在一个连续信号周期内以间隔 \(T\) 取到的样值数，正是离散序列的周期。</p>
    <p>例：求 \(x(n)=A\cos(0.01\pi n)\) 的周期。</p>
    <div class="formula">\[x(n)=A\cos(0.01\pi n),\qquad \frac{2\pi}{\omega}=\frac{2\pi}{0.01\pi}=200,\qquad N=200\]</div>
    <p>因为 \(\frac{2\pi}{\omega}=200\) 为整数，故该序列的基本周期为 \(200\)。</p>
    <h2>由频率求基本周期</h2>
    <h3>有理性判据</h3>
    <div class="formula">\[\frac{2\pi}{\omega}=\frac{N}{k},\qquad N,k\in\mathbb{Z}_{+},\qquad \gcd(N,k)=1\]</div>
    <p>当 \(\frac{2\pi}{\omega}\) 为整数时，基本周期就是该整数；当它是既约分数 \(\frac{N}{k}\) 时，基本周期为分子 \(N\)；若它是无理数，序列无周期。</p>
    <p>例：求 \(x(n)=A\cos\left(\frac{3\pi}{7}n\right)\) 的周期。</p>
    <div class="formula">\[x(n)=A\cos\left(\frac{3\pi}{7}n\right),\qquad \frac{2\pi}{\omega}=\frac{2\pi}{3\pi/7}=\frac{14}{3},\qquad N=14\]</div>
    <p>\(\frac{14}{3}\) 已为既约分数，故基本周期取分子 \(N=14\)。若 \(\frac{2\pi}{\omega}\) 为无理数，则不存在整数 \(k\) 使上式给出整数 \(N\)，相应序列无周期。</p>
  </section>
  <section>
    <h3>例：由数字角频率判断周期</h3>
    <p>（A）\(x(n)=A\cos\left(\frac{13\pi}{4}n\right)\)</p>
    <div class="formula">\[x(n)=A\cos\left(\frac{13\pi}{4}n\right),\qquad \frac{2\pi}{\omega}=\frac{8}{13},\qquad N=8\]</div>
    <p>\(8\) 与 \(13\) 互素，故既约分数的分子为基本周期，即 \(N=8\)。从采样观点看，\(13\) 个连续正弦周期内取到 \(8\) 个离散样值周期。</p>
    <p>（B）\(x(n)=e^{j(\frac{n}{6}-\pi)}\)</p>
    <div class="formula">\[x(n)=e^{j(\frac{n}{6}-\pi)},\qquad \omega=\frac{1}{6},\qquad \frac{2\pi}{\omega}=12\pi\notin\mathbb{Q}\]</div>
    <p>结论：\(12\pi\) 为无理数，不存在整数 \(N\) 使 \(N\omega=2k\pi\)，所以该复指数序列不是周期序列。</p>
  </section>
  <section>
    <h2>周期求解方法与调幅序列</h2>
    <h3>组合序列的处理</h3>
    <p>先找出每个含 \(n\) 的正弦、余弦或复指数分量的数字角频率，再分别求基本周期。对 \(\sin(\omega_1n)+\sin(\omega_2n)\)，总周期为 \(\operatorname{lcm}(N_1,N_2)\)。</p>
    <p>对 \(\sin(\omega_1n)\sin(\omega_2n)\)，先利用积化和差公式得到 \(\omega_a=\left|\omega_1+\omega_2\right|\) 与 \(\omega_b=\left|\omega_1-\omega_2\right|\)，再取各周期的最小公倍数。含 \(n\) 的系数或非零实指数包络会破坏周期性。</p>
    <h3>先排除不可能有周期的形式</h3>
    <p>在求角频率前，应先识别是否带有随 \(n\) 增长或衰减的包络。\(n\sin(\omega n+\varphi)\)、\(a^n u(n)\)、\(e^{(\sigma+j\omega)n}\)（\(\sigma\ne0\)）以及 \(\sin(\omega n+\varphi)u(n)\) 均不可能是周期序列。</p>
    <h3>调幅序列的频率成分</h3>
    <div class="formula">\[x(n)=A[1+m\cos(\omega_Ln)]\cos(\omega_Hn)\]</div>
    <p>该式可写成载波分量和两个边带分量，数字角频率分别为 \(\omega_H\)、\(\omega_H+\omega_L\)、\(\omega_H-\omega_L\)。因此应分别检查三个分量的周期，再取最小公倍数。</p>
    <h3>参数的周期结论</h3>
    <div class="formula">\[\omega_L=0.01\pi,\quad\omega_H=0.2\pi,\quad N_1=10,\quad N_2=N_3=200\]</div>
    <p>三项频率为 \(0.2\pi\)、\(0.21\pi\)、\(0.19\pi\)，相应基本周期为 \(10\)、\(200\)、\(200\)；故调幅序列的基本周期为 \(\operatorname{lcm}(10,200,200)=200\)。</p>
  </section>
</main>
"""
    template = r"""<!doctype html>
<html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>数字信号处理讲义：离散时间序列的周期性</title>
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
@media screen and (max-width:560px) { body { font-size:10.5pt; } .chapter { width:100%; max-width:100%; } }
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
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_01_periodicity_mathjax_component.pdf"))
