"""Supplemental chapter-one real exams and detailed answers in MathJax."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


STYLE = r"""<style>
@page{size:A4;margin:21mm 18mm 23mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933;margin:0}main{max-width:174mm;margin:auto}
.exam-page{page-break-after:always;break-after:page;min-height:244mm}.exam-page:last-child{page-break-after:auto}.bridge-page{page-break-after:auto;break-after:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}h2{color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}.exam-head{display:flex;justify-content:space-between;color:#485b69;margin-bottom:18pt}.formula{background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}.signal-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}.axis{fill:none;stroke:#174b73;stroke-width:2}.stem{stroke:#b45309;stroke-width:2}.dot{fill:#b45309}.tick{stroke:#174b73;stroke-width:1.3}.label{fill:#374c5b;font:16px "Microsoft YaHei",sans-serif}.conv-line{fill:none;stroke:#008f95;stroke-width:3}
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


def self_convolution_waveform_svg() -> str:
    """Render the 2004 rectangle self-convolution from its exact breakpoints."""
    width, height = 860, 310
    left, right, top, bottom = 82, 792, 58, 238
    x_min, x_max, y_min, y_max = -0.5, 4.6, -0.25, 2.45
    x_map = lambda value: left + (value - x_min) * (right - left) / (x_max - x_min)
    y_map = lambda value: bottom - (value - y_min) * (bottom - top) / (y_max - y_min)
    points = ((0, 0), (2, 2), (4, 0))
    polyline = " ".join(f"{x_map(x):.2f},{y_map(y):.2f}" for x, y in points)
    ticks = "".join(
        f'<line class="tick" x1="{x_map(x):.2f}" y1="{y_map(0)-5:.2f}" x2="{x_map(x):.2f}" y2="{y_map(0)+5:.2f}"/>'
        f'<text class="label" x="{x_map(x):.2f}" y="{y_map(0)+27:.2f}" text-anchor="middle">{x}</text>'
        for x in (0, 2, 4)
    )
    return rf'''<!-- self_convolution_waveform_svg: y(t) is calculated from the overlap length -->
<svg class="signal-svg" data-plot="self-convolution" viewBox="0 0 {width} {height}" role="img" aria-label="矩形脉冲自卷积的三角波形">
 <defs><marker id="conv-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <text class="label" x="{width / 2:.2f}" y="30" text-anchor="middle">矩形脉冲的自卷积波形</text>
 <line class="axis" x1="{left-12}" y1="{y_map(0):.2f}" x2="{right+22}" y2="{y_map(0):.2f}" marker-end="url(#conv-arrow)"/>
 <line class="axis" x1="{x_map(0):.2f}" y1="{bottom+8}" x2="{x_map(0):.2f}" y2="{top-12}" marker-end="url(#conv-arrow)"/>
 {ticks}
 <line class="tick" x1="{x_map(0)-5:.2f}" y1="{y_map(2):.2f}" x2="{x_map(0)+5:.2f}" y2="{y_map(2):.2f}"/>
 <text class="label" x="{x_map(0)-13:.2f}" y="{y_map(2)+5:.2f}" text-anchor="end">2</text>
 <polyline class="conv-line" points="{polyline}"/>
 <circle class="dot" cx="{x_map(2):.2f}" cy="{y_map(2):.2f}" r="4"/>
 <foreignObject x="{right+25}" y="{y_map(0)-18:.2f}" width="34" height="30"><div>\(t\)</div></foreignObject>
 <foreignObject x="{x_map(0)+10:.2f}" y="{top-34:.2f}" width="84" height="30"><div>\((f*f)(t)\)</div></foreignObject>
</svg>'''


def system_structure_svg() -> str:
    """Render the 2006 source system with explicit, equation-backed signal paths."""
    return '''<!-- system_structure_svg: signal paths match the state equations in the detailed answer -->
<svg class="signal-svg" data-diagram="2006-system-structure" viewBox="0 0 1140 540" role="img" aria-label="2006 年离散系统结构图">
 <defs><marker id="sys-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <style>.wire{fill:none;stroke:#174b73;stroke-width:2.4;marker-end:url(#sys-arrow)}.plain{fill:none;stroke:#174b73;stroke-width:2.4}.sum{fill:#fff;stroke:#174b73;stroke-width:2.4}.block{fill:#fff;stroke:#174b73;stroke-width:2.2;rx:4}.node{fill:#174b73}.dlabel{fill:#263746;font:20px "Microsoft YaHei",sans-serif}.small{fill:#263746;font:17px "Microsoft YaHei",sans-serif}.sumlabel{fill:#174b73;font:25px serif}</style>
 <text class="dlabel" x="570" y="34" text-anchor="middle">离散系统结构图</text>
 <text class="dlabel" x="48" y="266">x[n]</text><path class="wire" d="M105 260H142"/><circle class="node" cx="142" cy="260" r="4"/>
 <path class="plain" d="M142 260V72H812"/><rect class="block" x="814" y="51" width="70" height="42"/><text class="small" x="849" y="78" text-anchor="middle">0.2</text><path class="wire" d="M884 72H930V398"/>
 <rect class="block" x="204" y="239" width="72" height="42"/><text class="small" x="240" y="266" text-anchor="middle">0.25</text><path class="wire" d="M142 260H204"/><path class="wire" d="M276 260H337"/>
 <circle class="sum" cx="360" cy="260" r="23"/><text class="sumlabel" x="360" y="269" text-anchor="middle">Σ</text><text class="small" x="329" y="249">+</text><text class="small" x="351" y="301">+</text>
 <rect class="block" x="458" y="239" width="76" height="42"/><text class="dlabel" x="496" y="266" text-anchor="middle">z⁻¹</text><path class="wire" d="M383 260H458"/><path class="wire" d="M534 260H647"/>
 <circle class="sum" cx="670" cy="260" r="23"/><text class="sumlabel" x="670" y="269" text-anchor="middle">Σ</text><text class="small" x="640" y="249">+</text><text class="small" x="662" y="228">+</text>
 <rect class="block" x="531" y="112" width="58" height="42"/><text class="small" x="560" y="139" text-anchor="middle">0.5</text><path class="wire" d="M560 72V112"/><path class="wire" d="M560 154V232"/>
 <path class="wire" d="M693 260H724"/><circle class="node" cx="724" cy="260" r="4"/>
 <rect class="block" x="686" y="322" width="76" height="42"/><text class="dlabel" x="724" y="349" text-anchor="middle">z⁻¹</text><path class="wire" d="M724 260V322"/><path class="plain" d="M724 364V432"/><circle class="node" cx="724" cy="432" r="4"/>
 <path class="wire" d="M724 432H578"/><rect class="block" x="516" y="411" width="62" height="42"/><text class="small" x="547" y="438" text-anchor="middle">0.4</text><path class="wire" d="M516 432H420V283H360"/>
 <path class="wire" d="M724 260H798V326"/><rect class="block" x="768" y="326" width="60" height="42"/><text class="small" x="798" y="353" text-anchor="middle">0.3</text><path class="wire" d="M798 368V420H937"/>
 <path class="wire" d="M724 432V462H826"/><rect class="block" x="826" y="441" width="60" height="42"/><text class="small" x="856" y="468" text-anchor="middle">0.2</text><path class="wire" d="M886 462H960V443"/>
 <circle class="sum" cx="960" cy="420" r="23"/><text class="sumlabel" x="960" y="429" text-anchor="middle">Σ</text><text class="small" x="932" y="409">+</text><text class="small" x="953" y="393">+</text><text class="small" x="953" y="455">+</text><path class="wire" d="M983 420H1082"/><text class="dlabel" x="1090" y="427">y[n]</text>
 <text class="small" x="454" y="488">反馈支路</text><text class="small" x="734" y="492">一拍延时状态</text><text class="small" x="874" y="118">输入直通支路</text>
</svg>'''


QUESTIONS = (
    (2002, 60, r"已知 \(x(t)=\cos(50t)\)，对其进行时域采样。要求能从采样信号中恢复原始信号，填空：奈奎斯特频率为______ \(\mathrm{Hz}\)；奈奎斯特采样周期为______ \(\mathrm{s}\)。"),
    (2003, 60, r"已知 \(x(t)=1+\cos(200t)+\sin(300t)\)，对其进行时域采样。要求能从采样信号中恢复原始信号，填空：奈奎斯特频率为______ \(\mathrm{Hz}\)；奈奎斯特采样周期为______ \(\mathrm{s}\)。"),
    (2005, "____", r"某离散系统可由二阶常系数线性差分方程描述，且已知该系统单位阶跃响应序列为\(y(n)=[2^n+3(5)^n+10]u(n)\)。<br>（1）求此二阶差分方程；<br>（2）若激励为\(f(n)=3u(n)+3u(n-7)\)，求响应\(y(n)\)。"),
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
        figure = ""
        pages.append(f'<section class="exam-page"><h1>{title}</h1><div class="exam-head"><span>{year} 年真题</span><span>详解见 P.{answer_page}</span></div><p>{prompt}</p>{figure}</section>')
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
<section class="exam-page"><h1>真题整理详解（续）</h1><h2>2005 年真题：由阶跃响应反求二阶差分方程</h2><p>为避免与本问的输出记号混淆，记给定的单位阶跃响应为 \(s[n]\)。单位阶跃的 \(z\) 变换为 \(U(z)=1/(1-z^{-1})\)，因此系统函数为：</p><div class="formula">\[
\begin{aligned}
S(z)&=\frac{1}{1-2z^{-1}}+\frac{3}{1-5z^{-1}}+\frac{10}{1-z^{-1}},\\
H(z)&=\left(1-z^{-1}\right)S(z)\\
&=\frac{14-85z^{-1}+111z^{-2}}{1-7z^{-1}+10z^{-2}}.
\end{aligned}
\]</div><p>两边同乘分母并作反变换，得到所求二阶常系数线性差分方程：</p><div class="formula">\[
y[n]-7y[n-1]+10y[n-2]
=14f[n]-85f[n-1]+111f[n-2].
\]</div><p>第二问中 \(f[n]=3u[n]+3u[n-7]\)。利用线性与时不变性，输出等于两项阶跃响应的加权和：</p><div class="formula">\[
\begin{aligned}
y[n]&=3s[n]+3s[n-7]\\
&=3\left[2^n+3\left(5\right)^n+10\right]u[n]\\
&\quad+3\left[2^{n-7}+3\left(5\right)^{n-7}+10\right]u[n-7].
\end{aligned}
\]</div></section>
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
