"""Chapter-one selected real-exam training with MathJax and structured SVG."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def training_system_svg() -> str:
    """A standard signal-flow rendering of the supplied 2006 system."""
    return r"""
<!-- training_system_svg: standard DSP signal-flow diagram -->
<svg class="structure-svg" viewBox="0 0 920 350" role="img" aria-label="2006 年真题离散系统结构图">
 <defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path class="wire" d="M44 170H113" marker-end="url(#a)"/><circle class="sum" cx="135" cy="170" r="18"/><text class="sumtext" x="135" y="176" text-anchor="middle">Σ</text>
 <path class="wire" d="M153 170H230" marker-end="url(#a)"/><rect class="delay" x="238" y="143" width="60" height="54" rx="5"/><path class="wire" d="M298 170H375" marker-end="url(#a)"/>
 <circle class="sum" cx="397" cy="170" r="18"/><text class="sumtext" x="397" y="176" text-anchor="middle">Σ</text><path class="wire" d="M415 170H492" marker-end="url(#a)"/>
 <rect class="delay" x="500" y="143" width="60" height="54" rx="5"/><path class="wire" d="M560 170H637" marker-end="url(#a)"/><circle class="sum" cx="659" cy="170" r="18"/>
 <text class="sumtext" x="659" y="176" text-anchor="middle">Σ</text><path class="wire" d="M677 170H862" marker-end="url(#a)"/>
 <path class="feedback" d="M90 170V76H659V151"/><path class="feedback" d="M530 197V283H135V189"/><path class="feedback" d="M530 218V244H397V189"/>
 <g class="math"><foreignObject x="22" y="126" width="62" height="34"><div>\(x(n)\)</div></foreignObject><foreignObject x="842" y="126" width="62" height="34"><div>\(y(n)\)</div></foreignObject>
 <foreignObject x="246" y="153" width="45" height="34"><div>\(z^{-1}\)</div></foreignObject><foreignObject x="508" y="153" width="45" height="34"><div>\(z^{-1}\)</div></foreignObject>
 <foreignObject x="202" y="176" width="50" height="32"><div>\(0.25\)</div></foreignObject><foreignObject x="588" y="176" width="45" height="32"><div>\(0.2\)</div></foreignObject>
 <foreignObject x="344" y="44" width="44" height="32"><div>\(0.5\)</div></foreignObject><foreignObject x="299" y="278" width="44" height="32"><div>\(0.4\)</div></foreignObject><foreignObject x="445" y="229" width="44" height="32"><div>\(0.3\)</div></foreignObject></g>
</svg>"""


def training_stem_svg(values: dict[int, float], label: str) -> str:
    """Create an integer-indexed textbook stem plot."""
    ordered = sorted(values.items())
    lo, hi = ordered[0][0] - 1, ordered[-1][0] + 1
    left, step, base, scale = 95, 105, 165, 48
    x = lambda n: left + (n - lo) * step
    stems = "\n".join(f'<path class="stem" d="M{x(n)} {base}V{base-v*scale}"/><circle class="dot" cx="{x(n)}" cy="{base-v*scale}" r="4"/>' for n, v in ordered)
    ticks = "\n".join(f'<path class="tick" d="M{x(n)} {base-5}V{base+5}"/><text class="ticktext" x="{x(n)}" y="{base+26}" text-anchor="middle">{n}</text>' for n in range(lo, hi + 1))
    return f"""<!-- training_stem_svg: samples derived from supplied values -->
<svg class="signal-svg" viewBox="0 0 860 270" role="img" aria-label="{label} 离散序列">
 <defs><marker id="stemarrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path class="axis" d="M48 {base}H814" marker-end="url(#stemarrow)"/><path class="axis" d="M{x(0)} 230V38" marker-end="url(#stemarrow)"/>
 {ticks}{stems}<g class="math"><foreignObject x="{x(0)+8}" y="24" width="70" height="34"><div>\\({label}\\)</div></foreignObject><foreignObject x="814" y="{base-19}" width="28" height="30"><div>\\(n\\)</div></foreignObject></g>
</svg>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    f1 = training_stem_svg({-2: 1, -1: 1, 0: 1, 1: 1, 2: 1}, "f_1(n)")
    f2 = training_stem_svg({-1: 1, 0: 2, 1: -1, 2: 2, 3: -1}, "f_2(n)")
    content = r"""
<main>
 <section class="exam-page"><h1>第一章 分章强化训练</h1><div class="exam-head"><span>2002 年真题</span><span>详解见 P.59</span></div>
 <p>如图，\(f(t)=\mathrm{Sa}(1000\pi t)\)，\(p(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT)\)。\(f_s(t)\) 为 \(f(t)\) 与 \(p(t)\) 的乘积，经矩形滤波器 \(H(\Omega)\) 后得到 \(y(t)\)。</p>
 <div class="formula">\[f(t)\ \xrightarrow{\ \times p(t)\ }\ f_s(t)\ \xrightarrow{\ H(\Omega)\ }\ y(t)\]</div>
 <p>（1）要从 \(f_s(t)\) 中无失真地恢复 \(f(t)\)，求最大采样间隔 \(T_{\max}\)。<br>（2）若 \(T=0.0008\,\mathrm{s}\)，计算 \(f_s(t)\) 的频谱函数，并画出示意关系。<br>（3）设计矩形滤波器 \(H(\Omega)\)，使 \(y(t)\) 无失真地反映 \(f(t)\)。</p></section>
 <section class="exam-page"><h1>第一章 分章强化训练</h1><div class="exam-head"><span>2006 年真题</span><span>详解见 P.59</span></div><p>一离散系统结构如图所示。</p><figure>__SYSTEM__</figure><p>求：<br>（1）系统的传递函数；<br>（2）描述系统的差分方程；<br>（3）系统的单位阶跃响应。</p></section>
 <section class="exam-page"><h1>第一章 分章强化训练</h1><div class="exam-head"><span>2019 年真题</span><span>详解见 P.60</span></div><p>已知 \(f_1(n)\) 和 \(f_2(n)\) 波形如下，求 \(f_1(n)\) 与 \(f_2(n)\) 的卷积。</p><figure>__F1__</figure><figure>__F2__</figure></section>
</main>"""
    style = r"""<style>@page{size:A4;margin:21mm 18mm 23mm}body{font:11pt/1.75 "Microsoft YaHei",serif;color:#1f2933;margin:0}main{max-width:174mm;margin:auto}.exam-page{page-break-after:always;break-after:page;min-height:244mm}.exam-page:last-child{page-break-after:auto}h1{color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}.exam-head{display:flex;justify-content:space-between;color:#485b69;margin-bottom:18pt}.formula{background:#f4f7f8;border-radius:5pt;padding:11pt 14pt;margin:12pt 0;text-align:center;overflow-x:auto}figure{break-inside:avoid;margin:15pt 0}.structure-svg,.signal-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}.wire,.axis{fill:none;stroke:#174b73;stroke-width:2}.feedback{fill:none;stroke:#0f8b8d;stroke-width:2}.sum{fill:#fff;stroke:#174b73;stroke-width:2}.sumtext{fill:#174b73;font:19px serif}.delay{fill:#f4f7f8;stroke:#0f8b8d;stroke-width:2}.math foreignObject div{height:100%;display:flex;align-items:center;justify-content:center;color:#172b3a;font-size:17px}.stem{stroke:#b45309;stroke-width:2}.dot{fill:#b45309}.tick{stroke:#174b73;stroke-width:1.4}.ticktext{fill:#52616b;font:15px serif}</style>"""
    document = f'<!doctype html><meta charset="utf-8"><script>window.MathJax={{tex:{{packages:{{"[+]":["ams"]}}}}}};</script><script defer src="{MATHJAX}"></script>{style}{content}'
    output.write_text(document.replace("__SYSTEM__", training_system_svg()).replace("__F1__", f1).replace("__F2__", f2), encoding="utf-8")
    return output


def render_pdf(output: Path) -> Path:
    html = write_html(output.with_suffix(".html"))
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={output.resolve()}", html.resolve().as_uri()], check=True)
    return output


if __name__ == "__main__":
    print(render_pdf(ROOT / "full/outputs/chapter_01_training_mathjax_component.pdf"))
