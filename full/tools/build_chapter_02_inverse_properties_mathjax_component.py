"""Continuous MathJax treatment of z inverse transforms and z properties."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]
STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 23mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933;margin:0}main{max-width:174mm;margin:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:16pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:17pt 0 7pt}.formula{background:#f4f7f8;border-radius:5pt;padding:10pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.property-table{width:100%;border-collapse:collapse;margin:10pt 0 15pt;font-size:9.5pt;line-height:1.55}.property-table tr{break-inside:avoid;page-break-inside:avoid}.property-table th,.property-table td{border:.6pt solid #8ca4b5;padding:6pt 5pt;vertical-align:middle}.property-table thead{background:#e8f0f4;color:#174c6f}.property-table th[scope=row]{color:#1e4f79;text-align:left;background:#f7fafb;white-space:nowrap}</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<h1>z 反变换</h1>
<p>由 \(X(z)\) 求 \(x(n)\) 称为 z 反变换。围线积分给出理论定义；对有理函数，部分分式展开和幂级数展开更便于计算。无论采用哪种方法，\(X(z)\) 和 ROC 都必须同时使用。</p>
<div class="formula">\[x(n)=\frac{1}{2\pi j}\oint_C X(z)z^{n-1}\,\mathrm{d}z\]</div>
<h2>部分分式展开法</h2>
<p>先将 \(X(z)\) 因式分解为简单分式，再依据每一项的 ROC 选择右边或左边序列。若极点互异，可通过代入极点或系数比较确定系数；重极点保留相应高阶分式，多项式部分对应有限长冲激组合。</p>
<p>下式是有理函数作部分分式展开的通式：第一项对应互异极点，第二项保留重极点的各阶分式，最后一项对应有限长冲激组合。</p>
<div class="formula">\[X(z)=\sum_k\frac{A_k}{1-p_kz^{-1}}+\sum_{\ell}\sum_{r=1}^{q_\ell}\frac{C_{\ell,r}}{\left(1-p_\ell z^{-1}\right)^r}+\sum_{m=0}^{M}B_mz^{-m}\]</div>
<p>对单极点 \(p_k\)，相应简单分式的系数由留数直接给出：</p>
<div class="formula">\[A_k=\left.\left(1-p_kz^{-1}\right)X(z)\right|_{z=p_k}\]</div>
<p>若 \(p_\ell\) 是 \(q_\ell\) 重极点，则各高阶分式系数可由导数计算：</p>
<p class="formula-lead">重极点系数的导数公式（用于求有理 z 函数高阶极点项的部分分式系数）：</p>
<div class="formula">\[C_{\ell,r}=\frac{1}{(q_\ell-r)!}\left.\frac{\mathrm{d}^{q_\ell-r}}{\mathrm{d}z^{q_\ell-r}}\left[(z-p_\ell)^{q_\ell}X(z)\right]\right|_{z=p_\ell},\qquad r=1,\ldots,q_\ell\]</div>
<h2>有理函数的标准反变换对</h2>
<p>下表给出部分分式法中最常用的右边／左边序列对应关系；它用于由每一项的 ROC 选定正确时域序列。</p>
<table class="property-table"><thead><tr><th>z 域分式</th><th>时域序列</th><th>收敛域</th></tr></thead><tbody>
<tr><td>\(\displaystyle\frac{1}{1-az^{-1}}\)</td><td>\(a^n u(n)\)</td><td>\(\left|z\right|>\left|a\right|\)</td></tr>
<tr><td>\(\displaystyle\frac{1}{1-az^{-1}}\)</td><td>\(-a^n u(-n-1)\)</td><td>\(\left|z\right|<\left|a\right|\)</td></tr>
</tbody></table>
<table class="property-table"><thead><tr><th>z 域分式</th><th>时域序列</th><th>收敛域</th></tr></thead><tbody>
<tr><td>\(\displaystyle\frac{z^{-1}}{1-az^{-1}}\)</td><td>\(a^{n-1}u(n-1)\)</td><td>\(\left|z\right|>\left|a\right|\)</td></tr>
<tr><td>\(\displaystyle\frac{z^{-1}}{1-az^{-1}}\)</td><td>\(-a^{n-1}u(-n)\)</td><td>\(\left|z\right|<\left|a\right|\)</td></tr>
</tbody></table>
<p>例：设 \(X(z)=\frac{z^2}{(z-2)(z-0.5)}\)，ROC 为 \(\left|z\right|>2\)。分解后：</p>
<div class="formula">\[X(z)=\frac{4}{3}\frac{z}{z-2}-\frac{1}{3}\frac{z}{z-0.5}\]</div>
<p>ROC 位于最大极点之外，故两项均取右边序列：</p>
<div class="formula">\[x(n)=\frac{4}{3}2^n u(n)-\frac{1}{3}(0.5)^n u(n),\qquad \left|z\right|>2\]</div>
<h2>幂级数展开法</h2>
<p>若 ROC 在最外极点之外，按 \(z^{-1}\) 的降幂展开；若 ROC 在最内极点之内，按 \(z\) 的升幂展开。它直接给出 \(z^{-n}\) 的系数，适用于需要若干时域样值的情形。</p>
<div class="formula">\[\frac{3z^{-1}}{(1-3z^{-1})^2}=3z^{-1}+18z^{-2}+81z^{-3}+\cdots\quad\Longrightarrow\quad x(n)=n3^n u(n-1)\]</div>
<h1>z 变换的性质</h1>
<p>使用 z 域性质时，ROC 不是附属信息：线性组合、移位和卷积后的 ROC 以原收敛域为基础判定；零极点相消时，最终 ROC 可能扩大。</p>
<h2>性质、时域序列、z 域表达式与收敛域的对照表</h2>
<p>这张表用于在解题时同时核对运算式与收敛域，避免只变换代数式而忽略时域支持范围。</p>
<table class="property-table"><thead><tr><th>性质</th><th>时域序列</th><th>z 域表达式</th><th>收敛域</th></tr></thead><tbody>
<tr><th scope="row">线性</th><td>\(ax(n)+by(n)\)</td><td>\(aX(z)+bY(z)\)</td><td>\(\operatorname{ROC}\supseteq R_x\cap R_y\)</td></tr>
<tr><th scope="row">移位</th><td>\(x(n-m)\)</td><td>\(z^{-m}X(z)\)</td><td>\(R_x\)，可增删 \(z=0\) 或 \(z=\infty\)</td></tr>
<tr><th scope="row">乘以指数</th><td>\(a^n x(n)\)</td><td>\(X(a^{-1}z)\)</td><td>\(\left|a\right|R_x\)</td></tr>
<tr><th scope="row">z 域微分</th><td>\(nx(n)\)</td><td>\(\displaystyle-z\frac{\mathrm{d}X(z)}{\mathrm{d}z}\)</td><td>\(R_x\)</td></tr>
<tr><th scope="row">时间反转</th><td>\(x(-n)\)</td><td>\(X(z^{-1})\)</td><td>\(R_x^{-1}\)</td></tr>
<tr><th scope="row">共轭序列</th><td>\(x^*(n)\)</td><td>\(X^*(z^*)\)</td><td>\(R_x\)</td></tr>
<tr><th scope="row">时域卷积</th><td>\(x(n)*h(n)\)</td><td>\(X(z)H(z)\)</td><td>\(\operatorname{ROC}\supseteq R_x\cap R_h\)</td></tr>
</tbody></table>
<h2>线性与移位</h2>
<p>线性公式用于把加权和拆成已知变换；在没有零极点相消时，其 ROC 正好是原 ROC 的交集。若两项均为环形 ROC，可把该交集的上下边界直接写出：</p>
<div class="formula">\[\begin{aligned}\mathcal{Z}\{ax(n)+by(n)\}&=aX(z)+bY(z),\\\operatorname{ROC}\{ax(n)+by(n)\}&\supseteq R_x\cap R_y,\\R_x\cap R_y&=\left\{z:\max\!\left(R_x^-,R_y^-\right)<\left|z\right|<\min\!\left(R_x^+,R_y^+\right)\right\}.\end{aligned}\]</div>
<p>移位公式用于把时域延迟换成 z 域的幂因子；有限移位不改变原有非零极点，因此 ROC 保持为 \(R_x\)，但可能增删原点或无穷远点。</p>
<div class="formula">\[\mathcal{Z}\{x(n-m)\}=z^{-m}X(z),\qquad \operatorname{ROC}\{x(n-m)\}=R_x\]</div>
<p>冲激的移位变换是移位公式的基本检验：有限长冲激序列在除原点外的整个 z 平面收敛。</p>
<div class="formula">\[\mathcal{Z}\{\delta(n)\}=1,\qquad \mathcal{Z}\{\delta(n-1)\}=z^{-1},\qquad \mathcal{Z}\{\delta(n+1)\}=z\]</div>
<p>右边余弦序列的 z 变换公式用于将单边正弦信号写成两个一阶复指数项，再合并为实系数二阶式：</p>
<div class="formula">\[\begin{aligned}x(n)&=\cos(\omega_0n)u(n),\\X(z)&=\frac{1-\cos(\omega_0)z^{-1}}{1-2\cos(\omega_0)z^{-1}+z^{-2}},\qquad \left|z\right|>1\end{aligned}\]</div>
<p>例如 \(x(n)=u(n)-u(n-3)=\delta(n)+\delta(n-1)+\delta(n-2)\)，故：</p>
<div class="formula">\[X(z)=1+z^{-1}+z^{-2},\qquad \text{ROC：}\left|z\right|>0\]</div>
<p>应先写出相加或相减后的最终时间序列，再判定 ROC，不能机械地仅对原单边序列 ROC 求交。</p>
<h2>卷积和性质</h2>
<div class="formula">\[y(n)=x(n)*h(n)\qquad\Longleftrightarrow\qquad Y(z)=X(z)H(z)\]</div>
<p>例：若 \(X(z)=\frac{1}{1-az^{-1}}\)，\(H(z)=\frac{1-az^{-1}}{1-bz^{-1}}\)，相乘后 z=a 的零极点相消：</p>
<div class="formula">\[Y(z)=\frac{1}{1-bz^{-1}}\qquad\Longrightarrow\qquad y(n)=b^n u(n)\]</div>
<p>当 \(\left|b\right|<\left|a\right|\) 时，相消后的 ROC 可从 \(\left|z\right|>\left|a\right|\) 扩大为 \(\left|z\right|>\left|b\right|\)。</p>
<h2>其他常用性质</h2>
<p>时间反转与指数加权公式分别用于反折序列和改变指数衰减率：</p>
<div class="formula">\[\mathcal{Z}\{x(-n)\}=X(z^{-1}),\qquad \mathcal{Z}\{a^nx(n)\}=X(a^{-1}z)\]</div>
<p>z 域微分公式用于把时域的 \(n\) 因子转成 z 域导数：</p>
<div class="formula">\[\mathcal{Z}\{nx(n)\}=-z\frac{\mathrm{d}X(z)}{\mathrm{d}z}\]</div>
<p>共轭公式用于由一条序列的变换直接得到其复共轭序列的变换：</p>
<div class="formula">\[\mathcal{Z}\{x^*(n)\}=X^*(z^*)\]</div>
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
