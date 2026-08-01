"""Continuous MathJax treatment of z inverse transforms and z properties."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]
STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 23mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933;margin:0}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:16pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:17pt 0 7pt}.formula{background:#f4f7f8;border-radius:5pt;padding:10pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>z 反变换</h1>
<p>由 \(X(z)\) 求 \(x(n)\) 称为 z 反变换。围线积分给出理论定义；对有理函数，部分分式展开和幂级数展开更便于计算。无论采用哪种方法，\(X(z)\) 和 ROC 都必须同时使用。</p>
<div class="formula">\[x(n)=\frac{1}{2\pi j}\oint_C X(z)z^{n-1}\,\mathrm{d}z\]</div>
<h2>部分分式展开法</h2>
<p>先将 \(X(z)\) 因式分解为简单分式，再依据每一项的 ROC 选择右边或左边序列。若极点互异，可通过代入极点或系数比较确定系数；重极点保留相应高阶分式，多项式部分对应有限长冲激组合。</p>
<div class="formula">\[X(z)=\sum_k\frac{A_k}{1-p_kz^{-1}}+\sum_{m=0}^{M}B_mz^{-m}\]</div>
<p>例：设 \(X(z)=\frac{z^2}{(z-2)(z-0.5)}\)，ROC 为 \(\left|z\right|>2\)。分解后：</p>
<div class="formula">\[X(z)=\frac{4}{3}\frac{z}{z-2}-\frac{1}{3}\frac{z}{z-0.5}\]</div>
<p>ROC 位于最大极点之外，故两项均取右边序列：</p>
<div class="formula">\[x(n)=\frac{4}{3}2^n u(n)-\frac{1}{3}(0.5)^n u(n),\qquad \left|z\right|>2\]</div>
<h2>幂级数展开法</h2>
<p>若 ROC 在最外极点之外，按 \(z^{-1}\) 的降幂展开；若 ROC 在最内极点之内，按 \(z\) 的升幂展开。它直接给出 \(z^{-n}\) 的系数，适用于需要若干时域样值的情形。</p>
<div class="formula">\[\frac{3z^{-1}}{(1-3z^{-1})^2}=3z^{-1}+18z^{-2}+81z^{-3}+\cdots\quad\Longrightarrow\quad x(n)=n3^n u(n-1)\]</div>
<h1>z 变换的性质</h1>
<p>使用 z 域性质时，ROC 不是附属信息：线性组合、移位和卷积后的 ROC 以原收敛域为基础判定；零极点相消时，最终 ROC 可能扩大。</p>
<h2>线性与移位</h2>
<div class="formula">\[\mathcal{Z}\{ax(n)+by(n)\}=aX(z)+bY(z),\qquad \mathcal{Z}\{x(n-m)\}=z^{-m}X(z)\]</div>
<p>例如 \(x(n)=u(n)-u(n-3)=\delta(n)+\delta(n-1)+\delta(n-2)\)，故：</p>
<div class="formula">\[X(z)=1+z^{-1}+z^{-2},\qquad \text{ROC：}\left|z\right|>0\]</div>
<p>应先写出相加或相减后的最终时间序列，再判定 ROC，不能机械地仅对原单边序列 ROC 求交。</p>
<h2>卷积和性质</h2>
<div class="formula">\[y(n)=x(n)*h(n)\qquad\Longleftrightarrow\qquad Y(z)=X(z)H(z)\]</div>
<p>例：若 \(X(z)=\frac{1}{1-az^{-1}}\)，\(H(z)=\frac{1-az^{-1}}{1-bz^{-1}}\)，相乘后 z=a 的零极点相消：</p>
<div class="formula">\[Y(z)=\frac{1}{1-bz^{-1}}\qquad\Longrightarrow\qquad y(n)=b^n u(n)\]</div>
<p>当 \(\left|b\right|<\left|a\right|\) 时，相消后的 ROC 可从 \(\left|z\right|>\left|a\right|\) 扩大为 \(\left|z\right|>\left|b\right|\)。</p>
<h2>其他常用性质</h2>
<div class="formula">\[\mathcal{Z}\{x(-n)\}=X(z^{-1}),\qquad \mathcal{Z}\{a^nx(n)\}=X(a^{-1}z),\qquad \mathcal{Z}\{nx(n)\}=-z\frac{\mathrm{d}X(z)}{\mathrm{d}z}\]</div>
<p>固定的判定顺序是：先列 \(X(z)\) 与 ROC；再做性质运算；最后依据化简后的表达式和时域支持范围重新确定最终 ROC。</p>
</main>"""
    output.write_text(f'<!doctype html><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}', encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full/outputs/chapter_02_inverse_properties_mathjax_component.pdf"))
