"""Assemble chapter one as a MathJax-only main body, without training pages."""
from __future__ import annotations

import math
import re
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools import (
    build_chapter_01_analog_digital_chain_mathjax_component as analog_digital_chain,
    build_chapter_01_applications_close_mathjax_component as applications_close,
    build_chapter_01_causal_stable_mathjax_component as causal_stable,
    build_chapter_01_convolution_basics_mathjax_component as convolution_basics,
    build_chapter_01_convolution_properties_mathjax_component as convolution_properties,
    build_chapter_01_difference_equation_mathjax_component as difference_equation,
    build_chapter_01_linearity_mathjax_component as linearity,
    build_chapter_01_operations_mathjax_component as operations,
    build_chapter_01_periodicity_mathjax_component as periodicity,
    build_chapter_01_representation_mathjax_component as representation,
    build_chapter_01_sampling_engineering_mathjax_component as sampling_engineering,
    build_chapter_01_sampling_recovery_mathjax_component as sampling_recovery,
    build_chapter_01_sampling_theorem_mathjax_component as sampling_theorem,
    build_chapter_01_time_invariance_mathjax_component as time_invariance,
    build_chapter_01_typical_sequences_mathjax_component as typical_sequences,
)
from full.tools.render_mathjax_formula import MATHJAX


COMPONENTS = (
    representation,
    operations,
    typical_sequences,
    periodicity,
    linearity,
    time_invariance,
    convolution_basics,
    convolution_properties,
    causal_stable,
    difference_equation,
    sampling_theorem,
    sampling_engineering,
    sampling_recovery,
    analog_digital_chain,
    applications_close,
)

STYLE = r"""
<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
h1{break-after:avoid;color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:18pt 0 16pt}
h1:first-child{margin-top:0}
h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}
p{margin:5pt 0 8pt}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
figure{break-inside:avoid;margin:12pt auto;text-align:center}
svg{max-width:100%;height:auto}
.sampling-rate-comparison{max-width:174mm;padding:8pt 0 2pt}
.sampling-rate-comparison svg{display:block;width:100%;height:auto}
.sampling-rate-comparison .plot-frame{fill:#fff;stroke:#c4ced6;stroke-width:1}
.sampling-rate-comparison .axis{fill:none;stroke:#174b73;stroke-width:1.2}
.sampling-rate-comparison .continuous{fill:none;stroke:#0d8794;stroke-width:1.8}
.sampling-rate-comparison .stem{stroke:#0d8794;stroke-width:1.1}
.sampling-rate-comparison .sample{fill:#b56b2e;stroke:#b56b2e}
.sampling-rate-comparison .math-label foreignObject div{height:100%;display:flex;align-items:center;justify-content:center;font-size:17px;color:#172b3a}
.continuous-discrete-mapping{max-width:174mm;padding:4pt 0 2pt}
.continuous-discrete-mapping svg{display:block;width:100%;height:auto}
.continuous-discrete-mapping .math-label foreignObject div{height:100%;display:flex;align-items:center;justify-content:center;font-size:17px;color:#172b3a}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}}
</style>
"""

def _sampling_rate_comparison_svg() -> str:
    """Return source page 5's comparison as data-driven vector curves and stems."""
    left, right = 166, 956
    tops = (18, 94, 170, 246)
    labels = (r"f_s=44100\,\mathrm{Hz}", r"\frac{f_s}{4}", r"\frac{f_s}{8}", r"\frac{f_s}{16}")

    def amplitude(point: float) -> float:
        return (
            0.48 * math.sin(2 * math.pi * 7 * point)
            + 0.23 * math.sin(2 * math.pi * 19 * point)
            + 0.10 * math.sin(2 * math.pi * 31 * point)
        )

    def x_at(point: float) -> float:
        return left + point * (right - left)

    rows: list[str] = []
    for index, (top, label) in enumerate(zip(tops, labels)):
        base = top + 31
        rows.append(f'<rect fill="#ffffff" stroke="#c4ced6" stroke-width="1" x="{left}" y="{top}" width="{right-left}" height="60"/>')
        rows.append(f'<path fill="none" stroke="#174b73" stroke-width="1.2" d="M{left} {base}H{right}"/>')
        for tick in range(5):
            x = left + tick * (right - left) / 4
            rows.append(f'<path fill="none" stroke="#174b73" stroke-width="1.2" d="M{x:.1f} {base-3}V{base+3}"/>')
        rows.append(
            f'<foreignObject class="math-label" x="22" y="{top+9}" width="126" height="38">'
            f'<div xmlns="http://www.w3.org/1999/xhtml">\\({label}\\)</div></foreignObject>'
        )
        if index == 0:
            points = " ".join(
                f"{x_at(i / 220):.1f},{base - 23 * amplitude(i / 220):.1f}" for i in range(221)
            )
            rows.append(f'<polyline fill="none" stroke="#0d8794" stroke-width="1.8" data-role="continuous-waveform" points="{points}"/>')
        else:
            count = (56, 28, 14)[index - 1]
            role = ("quarter-rate", "eighth-rate", "sixteenth-rate")[index - 1]
            for sample in range(count + 1):
                point = sample / count
                x = x_at(point)
                value = base - 23 * amplitude(point)
                rows.append(
                    f'<line stroke="#0d8794" stroke-width="1.1" data-role="{role}" x1="{x:.1f}" y1="{base}" '
                    f'x2="{x:.1f}" y2="{value:.1f}"/><circle fill="#b56b2e" stroke="#b56b2e" cx="{x:.1f}" '
                    f'cy="{value:.1f}" r="2.0"/>'
                )
    return (
        '<figure class="sampling-rate-comparison"><svg viewBox="0 0 980 330" role="img" '
        'aria-label="不同采样频率下钢琴乐曲的波形和离散采样对比">'
        + "".join(rows)
        + '</svg><figcaption>不同采样频率下钢琴乐曲的赏析：上图为高采样率波形，'
        '下三图依次展示采样率降低后的离散样值。</figcaption></figure>'
    )


def _continuous_discrete_mapping_svg() -> str:
    """Return source page 7's continuous-time-to-sequence correspondence as a clean vector figure."""
    left, right = 110, 505
    continuous_base, discrete_base = 103, 235

    def x_at(point: float) -> float:
        return 142 + point * (right - 142)

    def amplitude(point: float) -> float:
        return 0.60 * math.sin(math.pi * point * 0.94) + 0.16 * math.sin(math.pi * point * 2.7)

    def y_at(point: float, base: float) -> float:
        return base - 48 * amplitude(point)

    continuous_points = " ".join(
        f"{x_at(index / 180):.1f},{y_at(index / 180, continuous_base):.1f}" for index in range(181)
    )
    parts = [
        '<figure class="continuous-discrete-mapping"><svg viewBox="0 0 980 302" role="img" '
        'aria-label="连续时间信号到离散序列的对应关系">',
        '<defs><marker id="mapping-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        '<path fill="#174b73" d="M0,0 L8,4 L0,8 z"/></marker></defs>',
        f'<path fill="none" stroke="#174b73" stroke-width="1.35" d="M{left} {continuous_base}H{right}" marker-end="url(#mapping-arrow)"/>',
        f'<path fill="none" stroke="#174b73" stroke-width="1.35" d="M{left+22} {continuous_base+14}V36" marker-end="url(#mapping-arrow)"/>',
        f'<polyline fill="none" stroke="#0d8794" stroke-width="2" data-role="continuous-signal" points="{continuous_points}"/>',
        f'<path fill="none" stroke="#174b73" stroke-width="1.35" d="M{left} {discrete_base}H{right}" marker-end="url(#mapping-arrow)"/>',
        f'<path fill="none" stroke="#174b73" stroke-width="1.35" d="M{left+22} {discrete_base+14}V166" marker-end="url(#mapping-arrow)"/>',
    ]
    for index in range(10):
        point = index / 9
        x = x_at(point)
        continuous_y = y_at(point, continuous_base)
        discrete_y = y_at(point, discrete_base)
        parts.append(f'<line stroke="#b33b2e" stroke-width="1.4" x1="{x:.1f}" y1="{continuous_base}" x2="{x:.1f}" y2="{continuous_y:.1f}"/>')
        parts.append(f'<circle fill="#b56b2e" stroke="#b56b2e" cx="{x:.1f}" cy="{continuous_y:.1f}" r="2.7"/>')
        parts.append(f'<line stroke="#b33b2e" stroke-width="1.5" data-role="discrete-samples" x1="{x:.1f}" y1="{discrete_base}" x2="{x:.1f}" y2="{discrete_y:.1f}"/>')
        parts.append(f'<circle fill="#b56b2e" stroke="#b56b2e" cx="{x:.1f}" cy="{discrete_y:.1f}" r="2.8"/>')
        parts.append(f'<path fill="none" stroke="#174b73" stroke-width="1" d="M{x:.1f} {continuous_base-3}V{continuous_base+3}"/>')
        parts.append(f'<path fill="none" stroke="#174b73" stroke-width="1" d="M{x:.1f} {discrete_base-3}V{discrete_base+3}"/>')
        parts.append(f'<text fill="#4c6274" font-size="12" text-anchor="middle" x="{x:.1f}" y="{continuous_base+18}">{index}T</text>')
        parts.append(f'<text fill="#4c6274" font-size="12" text-anchor="middle" x="{x:.1f}" y="{discrete_base+18}">{index}</text>')
    parts.extend(
        [
            '<foreignObject class="math-label" x="110" y="4" width="330" height="34"><div xmlns="http://www.w3.org/1999/xhtml">\\(x_a(t)\\vert_{t=nT}=x_a(nT)\\)</div></foreignObject>',
            '<foreignObject class="math-label" x="112" y="137" width="150" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\\(x(n)\\)</div></foreignObject>',
            '<foreignObject class="math-label" x="470" y="94" width="58" height="32"><div xmlns="http://www.w3.org/1999/xhtml">\\(t\\)</div></foreignObject>',
            '<foreignObject class="math-label" x="470" y="226" width="58" height="32"><div xmlns="http://www.w3.org/1999/xhtml">\\(n\\)</div></foreignObject>',
            '<path fill="none" stroke="#174b73" stroke-width="1.6" data-role="sampling-arrow" d="M584 143H668" marker-end="url(#mapping-arrow)"/>',
            '<path fill="none" stroke="#174b73" stroke-width="1.6" data-role="sampling-arrow" d="M756 143H840" marker-end="url(#mapping-arrow)"/>',
            '<rect fill="#f4f7f8" stroke="#78a9c2" stroke-width="1.2" x="532" y="112" width="100" height="62" rx="5"/>',
            '<rect fill="#f4f7f8" stroke="#78a9c2" stroke-width="1.2" x="704" y="112" width="100" height="62" rx="5"/>',
            '<rect fill="#f4f7f8" stroke="#78a9c2" stroke-width="1.2" x="876" y="112" width="72" height="62" rx="5"/>',
            '<foreignObject class="math-label" x="536" y="127" width="92" height="32"><div xmlns="http://www.w3.org/1999/xhtml">\\(x_a(t)\\)</div></foreignObject>',
            '<foreignObject class="math-label" x="708" y="127" width="92" height="32"><div xmlns="http://www.w3.org/1999/xhtml">\\(x_a(nT)\\)</div></foreignObject>',
            '<foreignObject class="math-label" x="880" y="127" width="64" height="32"><div xmlns="http://www.w3.org/1999/xhtml">\\(x(n)\\)</div></foreignObject>',
            '<foreignObject class="math-label" x="636" y="82" width="126" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\\(t=nT\\)</div></foreignObject>',
            '<text fill="#315d7c" font-size="16" text-anchor="middle" x="740" y="210">以采样间隔 T 记录样值</text>',
            '</svg><figcaption>连续时间信号到离散序列的对应关系：在等间隔时刻读取样值，再以整数序列索引存储。</figcaption></figure>',
        ]
    )
    return "".join(parts)


OPENING = r"""
<h1>第一章 离散时间信号与系统</h1>
<h2>离散时间信号的由来</h2>
<p>连续时间信号以时间间隔 \(T\) 等间隔取样后得到离散时间序列。采用离散表示，才能将样值存入计算机并进行数字处理；采样频率的选择则由原信号的最高频率成分决定。</p>
<div class="formula">\[x(n)=x_a(nT),\qquad f_s=\frac{1}{T}\]</div>
__CONTINUOUS_DISCRETE_MAPPING__
<p>对最高频率为 \(f_h\) 的带限信号，为避免频谱混叠，采样频率必须满足奈奎斯特条件：</p>
<div class="formula">\[f_s\geq2f_h\]</div>
<h2>采样频率与信号细节</h2>
<p>钢琴音频的谐音成分通常可延伸到数千赫兹。以 \(f_s=44100\,\mathrm{Hz}\) 记录时，高频细节能够较完整地保留；将采样率依次降为 \(f_s/4\)、\(f_s/8\)、\(f_s/16\) 时，可保留的最高频率同步降低，音质会出现失真。</p>
__SAMPLING_RATE_COMPARISON__
<div class="formula">\[44100\,\mathrm{Hz},\qquad \frac{f_s}{4},\qquad \frac{f_s}{8},\qquad \frac{f_s}{16}\]</div>
<p>这一实例说明：采样频率较低时，高频细节会丢失；后续关于抽样、频谱与恢复的讨论，均以该频率约束为基础。</p>
"""


def _main_body(html: str) -> str:
    match = re.search(r"<main(?:\s[^>]*)?>(.*)</main>", html, flags=re.DOTALL)
    if not match:
        raise ValueError("chapter-one body component is missing its main container")
    return match.group(1)


def _combined_body() -> str:
    with tempfile.TemporaryDirectory(prefix="dsp-chapter-01-body-") as directory:
        temporary = Path(directory)
        opening = OPENING.replace("__CONTINUOUS_DISCRETE_MAPPING__", _continuous_discrete_mapping_svg())
        bodies = [opening.replace("__SAMPLING_RATE_COMPARISON__", _sampling_rate_comparison_svg())]
        for component in COMPONENTS:
            path = component.write_html(temporary / f"{component.__name__.split('.')[-1]}.html")
            bodies.append(_main_body(path.read_text(encoding="utf-8")))
    return "\n".join(bodies)


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = (
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<script>window.MathJax={tex:{packages:{"[+]": ["ams"]}}};</script>'
        f'<script defer src="{MATHJAX}"></script>{STYLE}<body><main>'
        f"{_combined_body()}</main></body></html>"
    )
    output.write_text(document, encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_html(ROOT / "full" / "outputs" / "chapter_01_body.html"))
