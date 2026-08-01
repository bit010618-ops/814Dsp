"""DTFT and conjugate-symmetry material as one continuous MathJax document."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools.render_mathjax_formula import EDGE, MATHJAX


STYLE = r"""<style>
@page{size:A4;margin:20mm 18mm 22mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}
h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
h3{color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}
p{margin:5pt 0 8pt}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>离散时间信号傅里叶变换</h1>
<p>离散时间非周期序列可用离散时间傅里叶变换（DTFT）描述。DTFT 把时域序列映射为关于连续频率变量的周期函数。</p>
<h2>正变换、反变换与存在条件</h2>
<p>序列 [[x(n)]] 的 DTFT 定义为：</p>
<div class="formula">\[X(e^{j\omega})=\sum_{n=-\infty}^{\infty}x(n)e^{-j\omega n}\]</div>
<p>它是 z 变换在单位圆上的取值；当 [[z=e^{j\omega}]] 且收敛域包含单位圆时，[[X(z)]] 即给出 [[X(e^{j\omega})]]。在任意一个长度为 [[2\pi]] 的频率区间上，可由反变换恢复序列：</p>
<div class="formula">\[x(n)=\frac{1}{2\pi}\int_{-\pi}^{\pi}X(e^{j\omega})e^{j\omega n}\,\mathrm{d}\omega\]</div>
<p>绝对可和是一个常用的充分存在条件：</p>
<div class="formula">\[\sum_{n=-\infty}^{\infty}\left|x(n)\right|&lt;\infty\]</div>
<p>实际判断时，先检查 z 变换的收敛域是否包含单位圆；单位圆不在收敛域内时，不能把该 z 变换直接当作 DTFT。</p>
<h2>频域周期性</h2>
<p>因为 [[n]] 为整数，频率增加整数倍 [[2\pi]] 后复指数不变，故 DTFT 必为 [[2\pi]] 周期函数：</p>
<div class="formula">\[X(e^{j(\omega+2\pi k)})=X(e^{j\omega}),\qquad k\in\mathbb{Z}\]</div>
<p>因此分析时通常只看一个主值区间，例如 [[-\pi\leq\omega&lt;\pi]]。这正是“离散时间对应周期频域”的核心区别。</p>
<h1>DTFT 的共轭对称性质</h1>
<h2>共轭对称与分解</h2>
<p>若 [[x(n)=x^*(-n)]]，称为共轭对称；若 [[x(n)=-x^*(-n)]]，称为共轭反对称。任意序列可唯一分解为两部分：</p>
<div class="formula">\[x_e(n)=\frac{1}{2}\left[x(n)+x^*(-n)\right],\qquad x_o(n)=\frac{1}{2}\left[x(n)-x^*(-n)\right]\]</div>
<p>相应频域分量为：</p>
<div class="formula">\[X_e(e^{j\omega})=\frac{1}{2}\left[X(e^{j\omega})+X^*(e^{-j\omega})\right],\quad X_o(e^{j\omega})=\frac{1}{2}\left[X(e^{j\omega})-X^*(e^{-j\omega})\right]\]</div>
<h2>实序列的频谱对称性</h2>
<p>当 [[x(n)]] 为实序列时，频谱满足共轭对称关系；实部为偶函数、虚部为奇函数，幅度为偶函数，相位为奇函数：</p>
<div class="formula">\[X(e^{j\omega})=X^*(e^{-j\omega}),\qquad \operatorname{Re}\{X(e^{j\omega})\}=\operatorname{Re}\{X(e^{-j\omega})\}\]</div>
<div class="formula">\[\operatorname{Im}\{X(e^{j\omega})\}=-\operatorname{Im}\{X(e^{-j\omega})\},\qquad \left|X(e^{j\omega})\right|=\left|X(e^{-j\omega})\right|\]</div>
<div class="formula">\[\arg X(e^{j\omega})=-\arg X(e^{-j\omega})\]</div>
<p>在变换对中，实部与虚部也分别对应共轭对称和共轭反对称分量：</p>
<div class="formula">\[\mathcal{F}\{\operatorname{Re}[x(n)]\}=X_e(e^{j\omega}),\qquad \mathcal{F}\{j\operatorname{Im}[x(n)]\}=X_o(e^{j\omega})\]</div>
<h2>例题：由实部恢复实因果序列</h2>
<p><strong>例题</strong>：设 [[h(n)]] 为实因果序列，且 [[H_R(e^{j\omega})=1+\cos\omega]]，求 [[h(n)]] 与 [[H(e^{j\omega})]]。</p>
<h3>解</h3>
<p>由 [[H_R(e^{j\omega})]] 得其时域共轭对称分量：</p>
<div class="formula">\[h_e(n)=\delta(n)+\frac{1}{2}\delta(n-1)+\frac{1}{2}\delta(n+1)\]</div>
<p>因 [[h(n)]] 因果，[[n&lt;0]] 时 [[h(n)=0]]。为抵消 [[n=-1]] 处的值，需要 [[h_o(-1)=-\frac{1}{2}]]；又 [[h_o(n)]] 为奇函数，因此 [[h_o(0)=0]]、[[h_o(1)=\frac{1}{2}]]。故：</p>
<div class="formula">\[h(n)=h_e(n)+h_o(n)=\delta(n)+\delta(n-1)\]</div>
<p>所以 [[H(e^{j\omega})=1+e^{-j\omega}]]。其实际部为 [[1+\cos\omega]]，虚部为 [[-\sin\omega]]，与已知条件及实序列频谱对称性一致。</p>
</main>""".replace("[[", chr(92) + "(").replace("]]", chr(92) + ")")
    document = f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}</html>'
    output.write_text(document, encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_02_dtft_mathjax_component.pdf"))
