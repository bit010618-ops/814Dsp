"""Chapter-one selected real-exam training with MathJax and structured SVG."""
from __future__ import annotations

import subprocess
from pathlib import Path

from full.tools.render_mathjax_formula import EDGE, MATHJAX


ROOT = Path(__file__).resolve().parents[2]


def training_system_svg() -> str:
    """Render the verified 2006 source system with equation-backed paths."""
    return r"""<!-- training_system_svg: paths match the detailed answer state equations -->
<svg class="structure-svg" data-diagram="2006-system-structure" viewBox="0 0 1140 540" role="img" aria-label="2006 年真题离散系统结构图">
 <defs><marker id="sys-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <style>.wire{fill:none;stroke:#174b73;stroke-width:2.4;marker-end:url(#sys-arrow)}.plain{fill:none;stroke:#174b73;stroke-width:2.4}.sum{fill:#fff;stroke:#174b73;stroke-width:2.4}.block{fill:#fff;stroke:#174b73;stroke-width:2.2;rx:4}.node{fill:#174b73}.dlabel{fill:#263746;font:20px "Microsoft YaHei",sans-serif}.small{fill:#263746;font:17px "Microsoft YaHei",sans-serif}.sumlabel{fill:#174b73;font:25px serif}</style>
 <text class="dlabel" x="570" y="34" text-anchor="middle">离散系统结构图</text>
 <g class="math"><foreignObject x="46" y="238" width="62" height="38"><div>\(x[n]\)</div></foreignObject></g><path class="wire" d="M105 260H142"/><circle class="node" cx="142" cy="260" r="4"/>
 <path class="plain" d="M142 260V72H812"/><rect class="block" x="814" y="51" width="70" height="42"/><text class="small" x="849" y="78" text-anchor="middle">0.2</text><path class="wire" d="M884 72H930V398"/>
 <rect class="block" x="204" y="239" width="72" height="42"/><text class="small" x="240" y="266" text-anchor="middle">0.25</text><path class="wire" d="M142 260H204"/><path class="wire" d="M276 260H337"/>
 <circle class="sum" cx="360" cy="260" r="23"/><text class="sumlabel" x="360" y="269" text-anchor="middle">Σ</text><text class="small" x="329" y="249">+</text><text class="small" x="351" y="301">+</text>
 <rect class="block" x="458" y="239" width="76" height="42"/><g class="math"><foreignObject x="466" y="242" width="60" height="36"><div>\(z^{-1}\)</div></foreignObject></g><path class="wire" d="M383 260H458"/><path class="wire" d="M534 260H647"/>
 <circle class="sum" cx="670" cy="260" r="23"/><text class="sumlabel" x="670" y="269" text-anchor="middle">Σ</text><text class="small" x="640" y="249">+</text><text class="small" x="662" y="228">+</text>
 <rect class="block" x="531" y="112" width="58" height="42"/><text class="small" x="560" y="139" text-anchor="middle">0.5</text><path class="wire" d="M560 72V112"/><path class="wire" d="M560 154V232"/>
 <path class="wire" d="M693 260H724"/><circle class="node" cx="724" cy="260" r="4"/>
 <rect class="block" x="686" y="322" width="76" height="42"/><g class="math"><foreignObject x="694" y="325" width="60" height="36"><div>\(z^{-1}\)</div></foreignObject></g><path class="wire" d="M724 260V322"/><path class="plain" d="M724 364V432"/><circle class="node" cx="724" cy="432" r="4"/>
 <path class="wire" d="M724 432H578"/><rect class="block" x="516" y="411" width="62" height="42"/><text class="small" x="547" y="438" text-anchor="middle">0.4</text><path class="wire" d="M516 432H420V283H360"/>
 <path class="wire" d="M724 260H798V326"/><rect class="block" x="768" y="326" width="60" height="42"/><text class="small" x="798" y="353" text-anchor="middle">0.3</text><path class="wire" d="M798 368V420H937"/>
 <path class="wire" d="M724 432V462H826"/><rect class="block" x="826" y="441" width="60" height="42"/><text class="small" x="856" y="468" text-anchor="middle">0.2</text><path class="wire" d="M886 462H960V443"/>
 <circle class="sum" cx="960" cy="420" r="23"/><text class="sumlabel" x="960" y="429" text-anchor="middle">Σ</text><text class="small" x="932" y="409">+</text><text class="small" x="953" y="393">+</text><text class="small" x="953" y="455">+</text><path class="wire" d="M983 420H1082"/><g class="math"><foreignObject x="1088" y="401" width="54" height="38"><div>\(y[n]\)</div></foreignObject></g>
</svg>"""


def training_stem_svg(
    values: dict[int, float], label: str, *, source_candidate_id: str | None = None
) -> str:
    """Create an integer-indexed textbook stem plot."""
    ordered = sorted(values.items())
    candidate_attribute = (
        f' data-source-candidate-id="{source_candidate_id}"'
        if source_candidate_id
        else ""
    )
    lo, hi = ordered[0][0] - 1, ordered[-1][0] + 1
    left, step, base, scale = 95, 105, 165, 48
    x = lambda n: left + (n - lo) * step
    stems = "\n".join(f'<path class="stem" fill="none" stroke="#b45309" stroke-width="2" d="M{x(n)} {base}V{base-v*scale}"/><circle class="dot" fill="#b45309" cx="{x(n)}" cy="{base-v*scale}" r="4"/>' for n, v in ordered)
    ticks = "\n".join(
        f'<path class="tick" fill="none" stroke="#174b73" stroke-width="1.4" data-index="{n}" d="M{x(n)} {base-5}V{base+5}"/>'
        f'<text class="ticktext" data-index="{n}" x="{x(n)}" y="{base+26}" text-anchor="middle">{n}</text>'
        for n in range(lo, hi + 1)
        if n != 0
    )
    origin_label = (
        f'<text class="ticktext" data-origin-label="true" x="{x(0) + 10}" '
        f'y="{base + 26}" text-anchor="start">0</text>'
    )
    return f"""<!-- training_stem_svg: samples derived from supplied values -->
<svg class="signal-svg"{candidate_attribute} viewBox="0 0 860 270" role="img" aria-label="{label} 离散序列">
 <defs><marker id="stemarrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#174b73"/></marker></defs>
 <path class="axis" fill="none" stroke="#174b73" stroke-width="2" d="M48 {base}H814" marker-end="url(#stemarrow)"/><path class="axis" data-origin-at-zero="true" fill="none" stroke="#174b73" stroke-width="2" d="M{x(0)} 230V38" marker-end="url(#stemarrow)"/>
 {ticks}{stems}{origin_label}<g class="math"><foreignObject x="{x(0)+8}" y="24" width="70" height="34"><div>\\({label}\\)</div></foreignObject><foreignObject x="814" y="{base-19}" width="28" height="30"><div>\\(n\\)</div></foreignObject></g>
</svg>"""


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    f1 = training_stem_svg({-2: 1, -1: 1, 0: 1, 1: 1, 2: 1}, "f_1(n)", source_candidate_id="2019-q二-01")
    f2 = training_stem_svg({-1: 1, 0: 2, 1: -1, 2: 2, 3: -1}, "f_2(n)", source_candidate_id="2019-q二-01")
    content = r"""
<main>
 <section class="exam-page"><h1>第一章 分章强化训练</h1><div class="exam-head"><span>2002 年真题</span><span>详解见 P.59</span></div>
 <p>如图，\(f(t)=\mathrm{Sa}(1000\pi t)\)，\(p(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT)\)。\(f_s(t)\) 为 \(f(t)\) 与 \(p(t)\) 的乘积，经矩形滤波器 \(H(\Omega)\) 后得到 \(y(t)\)。</p>
 <div class="formula">\[f(t)\ \xrightarrow{\ \times p(t)\ }\ f_s(t)\ \xrightarrow{\ H(\Omega)\ }\ y(t)\]</div>
 <p>（1）要从 \(f_s(t)\) 中无失真地恢复 \(f(t)\)，求最大采样间隔 \(T_{\max}\)。<br>（2）若 \(T=0.0008\,\mathrm{s}\)，计算 \(f_s(t)\) 的频谱函数，并画出示意关系。<br>（3）设计矩形滤波器 \(H(\Omega)\)，使 \(y(t)\) 无失真地反映 \(f(t)\)。</p></section>
 <section class="exam-page"><h1>第一章 分章强化训练</h1><div class="exam-head"><span>2006 年真题</span><span>详解见 P.59</span></div><p>一离散系统如图所示：</p><figure>__SYSTEM__</figure><p>试求：<br>（1）系统的传递函数；<br>（2）描述系统的差分方程；<br>（3）系统的单位阶跃函数响应。</p></section>
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
