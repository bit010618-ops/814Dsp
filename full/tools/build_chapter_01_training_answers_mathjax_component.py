"""Detailed answers for the selected chapter-one exams, rendered by MathJax."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 23mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933;margin:0}main{max-width:174mm;margin:auto}.answer-page{page-break-after:always;break-after:page;min-height:244mm}.answer-page:last-child{page-break-after:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}</style>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = r"""
<main>
<section class="answer-page"><h1>真题整理详解</h1><h2>2002 年真题：采样与恢复</h2><p>\(\mathrm{Sa}(1000\pi t)\) 的最高角频率为 \(\Omega_h=1000\pi\,\mathrm{rad}\,\mathrm{s}^{-1}\)。由 \(\Omega_s\geq2\Omega_h\) 和 \(\Omega_s=\frac{2\pi}{T}\)，可得：</p><div class="formula">\[T_{\max}=\frac{\pi}{\Omega_h}=10^{-3}\,\mathrm{s}\]</div><p>当 \(T=0.0008\,\mathrm{s}\) 时，\(\Omega_s=2500\pi\,\mathrm{rad}\,\mathrm{s}^{-1}\)。冲激采样使频谱以 \(\Omega_s\) 周期复制：</p><div class="formula">\[F_s(j\Omega)=\frac{1}{T}\sum_{k=-\infty}^{\infty}F\bigl(j(\Omega-k\Omega_s)\bigr)\]</div><p>各副本的支撑区为 \(\left|\Omega-k\Omega_s\right|\leq1000\pi\)，相邻副本仍有间隔。用通带增益为 \(T\) 的理想低通滤波器即可恢复原信号：</p><div class="formula">\[H(\Omega)=\begin{cases}T,&\left|\Omega\right|\leq1000\pi,\\0,&\left|\Omega\right|>1000\pi.\end{cases}\]</div></section>
<section class="answer-page"><h1>真题整理详解（续）</h1><h2>2006 年真题：离散系统结构分析</h2><p>令 \(a[n]\) 为第一个加法器输出，\(c[n]\) 为第二个加法器输出，\(b[n]\) 为 \(c[n]\) 延时一拍后的状态。逐条支路写得：</p><div class="formula">\[\begin{aligned}a[n]&=0.25x[n]+0.4b[n],\\c[n]&=a[n-1]+0.5x[n],\\b[n]&=c[n-1],\\y[n]&=0.2x[n]+0.3c[n]+0.2b[n].\end{aligned}\]</div><p>消去中间变量，得到传递函数和差分方程：</p><div class="formula">\[H(z)=\frac{Y(z)}{X(z)}=\frac{0.35+0.175z^{-1}-0.03z^{-2}}{1-0.4z^{-2}}\]</div><div class="formula">\[y[n]-0.4y[n-2]=0.35x[n]+0.175x[n-1]-0.03x[n-2]\]</div><p>对单位阶跃 \(u[n]\) 输入，部分分式展开后得到单位阶跃响应：</p><div class="formula">\[s[n]=\left[\frac{33}{40}-\frac{19+6\sqrt{10}}{80}\left(\frac{\sqrt{10}}{5}\right)^n-\frac{19-6\sqrt{10}}{80}\left(-\frac{\sqrt{10}}{5}\right)^n\right]u[n]\]</div></section>
<section class="answer-page"><h1>真题整理详解（续）</h1><h2>2019 年真题：图形卷积</h2><p>由图读出 \(f_1(n)=1\)（\(-2\leq n\leq2\)），而 \(f_2(-1)=1,f_2(0)=2,f_2(1)=-1,f_2(2)=2,f_2(3)=-1\)。卷积支撑区是 \(-3\leq n\leq5\)。</p><p>因为 \(f_1\) 在连续五个整数点取 1，\((f_1*f_2)(n)\) 等于 \(f_2\) 的五点滑动和。逐点相加：</p><div class="formula">\[(f_1*f_2)(n)=\{1,3,2,4,3,2,0,1,-1\},\qquad -3\leq n\leq5\]</div><p>结果长度为 \(5+5-1=9\)，与支撑区长度一致，可作为检验。</p></section>
</main>"""
    document = f'<!doctype html><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]": ["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}'
    output.write_text(document, encoding="utf-8")
    return output


def rendered_dom(html: Path) -> str:
    """Return the DOM only after the same browser has finished MathJax typesetting."""
    completed = subprocess.run(
        [
            str(EDGE), "--headless=new", "--disable-gpu",
            "--virtual-time-budget=10000", "--dump-dom", html.resolve().as_uri(),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout


def assert_mathjax_ready(dom: str) -> None:
    """Reject a reader-facing export when even one formula remains literal TeX."""
    if "<mjx-container" not in dom:
        raise RuntimeError("MathJax did not produce any rendered formula containers")
    raw_delimiters = (r"\(", r"\)", r"\[", r"\]")
    remaining = [delimiter for delimiter in raw_delimiters if delimiter in dom]
    if remaining:
        raise RuntimeError(
            "MathJax left unprocessed formula delimiters in the document: "
            + ", ".join(remaining)
        )


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    assert_mathjax_ready(rendered_dom(html))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full/outputs/chapter_01_training_answers_mathjax_component.pdf"))
