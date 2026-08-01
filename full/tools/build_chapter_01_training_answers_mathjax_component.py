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
<section class="answer-page"><h1>真题整理详解（续）</h1><h2>2006 年真题：系统结构</h2><p>逐节点列式并消去中间变量，可得到系统传递函数：</p><div class="formula">\[\frac{Y(z)}{X(z)}=\frac{0.2+0.04z^{-1}-0.03z^{-2}}{1-0.3z^{-1}-0.4z^{-2}}\]</div><p>因此描述系统的差分方程为：</p><div class="formula">\[y(n)-0.3y(n-1)-0.4y(n-2)=0.2x(n)+0.04x(n-1)-0.03x(n-2)\]</div><p>令输入为单位阶跃 \(u(n)\)，把传递函数化为 \(H(z)=0.075+\frac{0.125}{1-0.8z^{-1}}\)，对冲激响应累加：</p><div class="formula">\[s(n)=\bigl(0.7-0.5\times0.8^n\bigr)u(n)\]</div></section>
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


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full/outputs/chapter_01_training_answers_mathjax_component.pdf"))
