"""Supplemental chapter-one real exams and detailed answers in MathJax."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 23mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933;margin:0}main{max-width:174mm;margin:auto}
.exam-page{page-break-after:always;break-after:page;min-height:244mm}.exam-page:last-child{page-break-after:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}.exam-head{display:flex;justify-content:space-between;color:#485b69;margin-bottom:18pt}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.signal-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}.axis{fill:none;stroke:#174b73;stroke-width:2}.stem{stroke:#b45309;stroke-width:2}.dot{fill:#b45309}.tick{stroke:#174b73;stroke-width:1.3}.label{fill:#374c5b;font:16px "Microsoft YaHei",sans-serif}
</style>"""


def _document(content: str) -> str:
    return f'<!doctype html><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{STYLE}{content}'


def supplemental_spectrum_svg() -> str:
    """Discrete spectral impulses from the 2002 sampling answer."""
    positions = (145, 275, 385, 475, 585, 715)
    heights = (54, 94, 128, 128, 94, 54)
    labels = ("−5π", "−3π", "−2π", "2π", "3π", "5π")
    parts = []
    for x, h, label in zip(positions, heights, labels):
        parts.append(f'<path class="stem" d="M{x} 184V{184-h}"/><circle class="dot" cx="{x}" cy="{184-h}" r="4"/><text class="label" x="{x}" y="213" text-anchor="middle">{label}</text>')
    return """<!-- supplemental_spectrum_svg: data-defined line spectrum -->
<svg class="signal-svg" viewBox="0 0 860 260" role="img" aria-label="连续时间幅度谱">
 <defs><marker id="sarrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path class="axis" d="M45 184H814" marker-end="url(#sarrow)"/><path class="axis" d="M430 224V38" marker-end="url(#sarrow)"/>
 __STEMS__<text class="label" x="815" y="164">Ω</text><text class="label" x="440" y="46">|X(jΩ)|</text>
</svg>""".replace("__STEMS__", "".join(parts))


QUESTIONS = (
    (2002, 60, r"已知 \(x(t)=\cos(50t)\)，对其进行时域采样。要求能从采样信号中恢复原始信号，填空：奈奎斯特频率为______ \(\mathrm{Hz}\)；奈奎斯特采样周期为______ \(\mathrm{s}\)。"),
    (2003, 60, r"已知 \(x(t)=1+\cos(200t)+\sin(300t)\)，对其进行时域采样。要求能从采样信号中恢复原始信号，填空：奈奎斯特频率为______ \(\mathrm{Hz}\)；奈奎斯特采样周期为______ \(\mathrm{s}\)。"),
    (2014, 61, r"已知系统 \(y[n]=x[n]\{g[n]+g[n-1]\}\)，若 \(g[n]=1+(-1)^n\)，则系统是否为时变系统？______。"),
    (2015, 61, "对模拟信号进行采样，得到的是______信号。"),
    (2020, 61, r"已知频带宽度有限信号 \(x(t)\)、\(y(t)\) 的最高频率分别为 \(f_1\) 和 \(f_2\)，其中 \(f_1&lt;f_2\)，则对信号 \(2x(t)+5y(t)\) 进行无失真抽样的采样频率为______。"),
    (2002, 62, r"有一信号 \(x(t)=3\cos(2\pi t)+2\sin(3\pi t)+\cos(5\pi t)\)，现以 \(\Omega_s=8\pi\) 的频率对其采样得到离散信号 \(x(n)\)。画出 \(x(t)\) 和 \(x(n)\) 的幅度谱，判断是否存在混叠；若存在，说明避免方法并画出不失真时的离散频谱。"),
    (2003, 62, r"信号经过理想冲激串采样后，再经过增益为 \(T\) 的理想低通滤波器。证明：当低通滤波器截止角频率为 \(\omega_c=\frac{\omega_s}{2}\) 时，对任意 \(T\)，重建信号与原信号在采样时刻始终相等。"),
    (2003, 61, r"已知系统差分方程为 \(r(n)-6r(n-1)+8r(n-2)=e(n-1)+2e(n-2)\)，求单位样值响应。"),
)


def write_questions_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    pages = []
    for index, (year, answer_page, prompt) in enumerate(QUESTIONS):
        title = "第一章 补充真题" if index == 0 else "第一章 补充真题（续）"
        pages.append(f'<section class="exam-page"><h1>{title}</h1><div class="exam-head"><span>{year} 年真题</span><span>详解见 P.{answer_page}</span></div><p>{prompt}</p></section>')
    output.write_text(_document("<main>" + "".join(pages) + "</main>"), encoding="utf-8")
    return output


def write_answers_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    spectrum = supplemental_spectrum_svg()
    content = r"""
<main>
<section class="exam-page"><h1>真题整理详解</h1><h2>2002 年真题：单频正弦信号采样</h2><p>最高角频率为 \(\Omega_m=50\,\mathrm{rad}\,\mathrm{s}^{-1}\)。无混叠恢复要求 \(\Omega_s\geq2\Omega_m\)，换算为频率与采样周期：</p><div class="formula">\[f_{s,\min}=\frac{50}{\pi}\,\mathrm{Hz},\qquad T_{s,\max}=\frac{\pi}{50}\,\mathrm{s}\]</div><h2>2003 年真题：多频正弦信号采样</h2><p>常数项不增加频率上限，最高角频率为 \(\Omega_m=300\,\mathrm{rad}\,\mathrm{s}^{-1}\)。</p><div class="formula">\[f_{s,\min}=\frac{300}{\pi}\,\mathrm{Hz},\qquad T_{s,\max}=\frac{\pi}{300}\,\mathrm{s}\]</div><p>检查时必须先统一单位：50、200、300 均为角频率，不能直接当作 Hz。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2014 年真题：离散系统时变性判定</h2><p>代入 \(g[n]=1+(-1)^n\)，有 \(g[n-1]=1-(-1)^n\)，故 \(g[n]+g[n-1]=2\)。系统化为 \(y[n]=2x[n]\)，不显含时间索引，故不是时变系统。</p><h2>2015 年真题：采样后信号的类型</h2><p>采样把连续时间自变量限制在离散采样时刻，得到离散时间信号。采样本身不等同于量化；只有幅值也离散化后才得到数字信号。</p><h2>2020 年真题：组合带限信号的抽样频率</h2><p>线性组合不产生高于原分量的频率；最高频率为 \(f_2\)。</p><div class="formula">\[f_{s,\min}=2f_2\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2003 年真题：差分方程求单位样值响应</h2><p>在零状态下作 \(z\) 变换并令 \(w=z^{-1}\)，得到：</p><div class="formula">\[H(z)=\frac{z^{-1}+2z^{-2}}{1-6z^{-1}+8z^{-2}}=\frac{1}{4}-\frac{1}{1-2z^{-1}}+\frac{3}{4(1-4z^{-1})}\]</div><p>对因果系统取收敛域 \(\left|z\right|>4\)，反变换得到：</p><div class="formula">\[h[n]=\frac{1}{4}\delta[n]-2^n u[n]+\frac{3}{4}\,4^n u[n]\]</div></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2002 年真题：采样后的离散频谱与混叠</h2><p>原信号含有 \(2\pi\)、\(3\pi\)、\(5\pi\) 三个正频率分量。给定 \(\Omega_s=8\pi\)，奈奎斯特角频率为 \(4\pi\)，因此 \(5\pi\) 分量越过奈奎斯特频率并折叠到 \(-3\pi\)，产生混叠。</p>__SPECTRUM__<p>避免混叠需满足 \(\Omega_s>2\Omega_{\max}=10\pi\)，提高采样角频率后各分量即可分离。</p></section>
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2003 年真题：冲激采样后的低通重建</h2><p>采样信号为 \(f_p(t)=\sum_{n=-\infty}^{\infty}f(nT)\delta(t-nT)\)。理想低通重建输出为：</p><div class="formula">\[f_0(t)=\sum_{n=-\infty}^{\infty}f(nT)\,\operatorname{Sa}\left(\frac{t-nT}{T}\right)\]</div><p>令 \(t=mT\)。当 \(n\ne m\) 时，\(m-n\) 为非零整数，重建核为零；当 \(n=m\) 时重建核为一，因此：</p><div class="formula">\[f_0(mT)=f(mT)\]</div></section>
</main>""".replace("__SPECTRUM__", spectrum)
    output.write_text(_document(content), encoding="utf-8")
    return output


def _render(writer, output: Path) -> Path:
    html = writer(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


def render_questions_pdf(output: Path) -> Path:
    return _render(write_questions_html, output)


def render_answers_pdf(output: Path) -> Path:
    return _render(write_answers_html, output)


if __name__ == "__main__":
    print(render_questions_pdf(ROOT / "full/outputs/chapter_01_supplemental_mathjax_component.pdf"))
    print(render_answers_pdf(ROOT / "full/outputs/chapter_01_supplemental_answers_mathjax_component.pdf"))
