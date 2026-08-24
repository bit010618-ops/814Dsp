"""Time-invariance material rendered through complete MathJax formulas."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main class="chapter">
  <header><h1>离散时间系统的时不变性质</h1></header>
  <section class="handoff-lede">
    <p>若系统响应与激励作用于系统的时刻无关，则该系统为时不变系统，也称移不变系统。判定时必须比较两条完整路径。</p>
  </section>
  <section>
    <h2>定义</h2>
    <div class="formula">\[y(n)=T[x(n)]\quad\Longrightarrow\quad T[x(n-k)]=y(n-k),\qquad \forall k\in\mathbb{Z}\]</div>
    <p>第一条路径是先让输入延迟 \(k\) 个样本，再通过系统；第二条路径是先通过系统，再将输出延迟 \(k\) 个样本。二者相等才是时不变。</p>
  </section>
  <section>
    <h2>判别步骤</h2>
    <p>（1）由原输入 \(x(n)\) 写出 \(y(n)\)；（2）把输入替换为 \(x(n-k)\) 并求输出 \(T[x(n-k)]\)；（3）把原输出替换为 \(y(n-k)\)；（4）比较两式。</p>
    <div class="formula">\[T[x(n-k)]=y(n-k)\]</div>
  </section>
  <section>
    <h3>例：验证下面的系统是否为移不变系统</h3>
    <div class="formula">\[(1)\qquad y(n)=\sum_{m=-\infty}^{n}x(m)\]</div>
    <p>对移位输入，先有 \(T[x(n-k)]=\sum_{m=-\infty}^{n}x(m-k)\)。令 \(m'=m-k\)，下限仍为负无穷，得到：</p>
    <div class="formula">\[T[x(n-k)]=\sum_{m'=-\infty}^{n-k}x(m')=y(n-k)\]</div>
    <p>故从负无穷开始的累加器是时不变系统。</p>
    <h3>例：验证下面的系统是否为移不变系统</h3>
    <div class="formula">\[(2)\qquad y(n)=\sum_{m=0}^{n}x(m)\]</div>
    <p>相同变量替换后，下限由 \(0\) 变为 \(-k\)，因此一般不能与 \(y(n-k)\) 的下限 \(0\) 一致。</p>
    <div class="formula">\[T[x(n-k)]=\sum_{m'=-k}^{n-k}x(m')\ne\sum_{m=0}^{n-k}x(m')=y(n-k)\]</div>
    <p>故这个从固定时刻 \(0\) 开始的累加器不是时不变系统。</p>
  </section>
  <section>
    <h3>例：验证下面的系统是否为移不变系统</h3>
    <div class="formula">\[y(n)=x(2n)\]</div>
    <p>系统定义为 \(y(n)=x(2n)\)。先延迟输出得到 \(y(n-k)=x(2n-2k)\)；先延迟输入再通过系统则得到 \(T[x(n-k)]=x(2n-k)\)。两式一般不相等。</p>
    <div class="formula">\[x(2n-2k)\ne x(2n-k)\]</div>
    <p>按原例取有限序列 \(x(n)=\{0,1,2,3,4,5\}\)，并令 \(k=1\)、\(n=3\)。两条路径在同一时刻的取值不同：</p>
    <div class="formula">\[y(n-1)=x\bigl(2(n-1)\bigr)=x(2\cdot3-2)=x(4)=4,\qquad T[x(n-1)]=x(2n-1)=x(2\cdot3-1)=x(5)=5\]</div>
    <p>故可由 \(4\ne5\) 直接构成反例，说明 \(y(n)=x(2n)\) 是时变系统。</p>
    <h2>线性时不变系统：滑动平均</h2>
    <div class="formula">\[T[x(n)]=\frac{1}{M_2-M_1+1}\sum_{k=M_1}^{M_2}x(n-k)\]</div>
    <p>当 \(M_1=0\)、\(M_2=3\) 时，\(y(n)=\frac{1}{4}[x(n)+x(n-1)+x(n-2)+x(n-3)]\)。加权求和保持线性，固定的相对延迟保持时不变，因此它是线性时不变系统。</p>
  </section>
</main>
"""
    template = r"""<!doctype html>
<html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>数字信号处理讲义：离散时间系统的时不变性质</title>
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
        [
            str(EDGE), "--headless=new", "--disable-gpu", "--no-first-run",
            "--no-pdf-header-footer", f"--virtual-time-budget={wait_ms}",
            f"--print-to-pdf={output.resolve()}", html.resolve().as_uri(),
        ],
        check=True,
    )
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full" / "outputs" / "chapter_01_time_invariance_mathjax_component.pdf"))
