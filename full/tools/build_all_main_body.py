"""Build the eight-chapter handout body before any training is attached."""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools import (
    build_chapter_01_body_only as chapter_one,
    build_chapter_02_body_only as chapter_two,
    build_chapter_03_dfs_mathjax_component as chapter_three_dfs,
    build_chapter_03_dft_mathjax_component as chapter_three_dft,
    build_chapter_03_frequency_sampling_mathjax_component as chapter_three_frequency_sampling,
    build_chapter_03_lsi_output_mathjax_component as chapter_three_lsi_output,
    build_chapter_03_overview_mathjax_component as chapter_three_overview,
    build_chapter_03_spectrum_analysis_mathjax_component as chapter_three_spectrum,
    build_chapter_04_dft_efficiency_mathjax_component as chapter_four_efficiency,
    build_chapter_04_dif_ifft_optimization_mathjax_component as chapter_four_dif_ifft,
    build_chapter_04_dit_fft_mathjax_component as chapter_four_dit,
    build_chapter_05_filter_structures_mathjax_component as chapter_five,
    build_chapter_06_iir_design_mathjax_component as chapter_six,
    build_chapter_07_fir_design_mathjax_component as chapter_seven,
    build_chapter_08_multirate_mathjax_component as chapter_eight,
)
from full.tools.render_mathjax_formula import MATHJAX


STYLE = r"""
<style>
@page{size:A4;margin:24mm 18mm 20mm}
body{margin:0;color:#1f2933;font:11pt/1.75 "Microsoft YaHei",serif}
main{max-width:174mm;margin:auto}
.chapter-start+.chapter-start{break-before:page}
h1{break-after:avoid;color:#1e4f79;font-size:22pt;font-weight:400;border-bottom:1.4pt solid #b56b2e;padding-bottom:8pt;margin:0 0 16pt}
h2{break-after:avoid;color:#1e4f79;font-size:15pt;font-weight:400;border-bottom:.8pt solid #c59d6e;padding-bottom:2pt;margin:15pt 0 7pt}
h3{break-after:avoid;color:#315d7c;font-size:12.5pt;font-weight:400;margin:12pt 0 4pt}
h4{break-after:avoid;color:#315d7c;font-size:11.5pt;font-weight:400;margin:10pt 0 3pt}
p{margin:5pt 0 8pt}
.formula{break-inside:avoid;background:#f4f7f8;border-radius:5pt;padding:9pt 14pt;margin:10pt 0;text-align:center;overflow-x:auto}
.formula-wide{padding:8pt 10pt;font-size:9.5pt}
.formula mjx-container[display="true"]{max-width:100%;margin:0 auto!important}
.mapping,.table{border-collapse:collapse;width:100%;margin:10pt 0 12pt;break-inside:avoid}
.mapping th,.mapping td,.table th,.table td{border:.45pt solid #b9c6cf;padding:6pt 7pt;text-align:left;vertical-align:top}
.mapping th,.table th{color:#315d7c;font-weight:600;background:#f4f7f8}
figure{break-inside:avoid;margin:12pt auto;text-align:center}
.source-figure{max-width:100%;padding:0;background:#fff;border:1px solid #d8e0e5;border-radius:5pt;overflow:hidden}
.source-figure.compact{max-width:156mm}
.source-figure img{display:block;width:100%;height:auto}
.source-figure figcaption{padding:5pt 8pt 6pt;color:#486d8b;font-size:9.5pt;text-align:center;background:#fbfcfd}
.chart-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9pt;align-items:start}
.chart-grid figure{width:100%;margin:6pt auto 10pt}
.typical-sequence-continuation .chart{break-inside:auto;margin:6pt auto 8pt}
.typical-sequence-continuation .chart svg{max-width:500px!important}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9pt;align-items:start}
.grid svg{width:100%;height:auto}
svg{max-width:100%;height:auto}
.diagram{background:#f8fafb;border:1px solid #d8e0e5;border-radius:5pt;padding:8pt;margin:10pt 0}
.structure-svg{display:block;width:100%;height:auto}
.structure-svg .wire{fill:none;stroke:#174b73;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.structure-svg .block{fill:#f4f7f8;stroke:#0d8794;stroke-width:2}
.structure-svg .sum{fill:#fff;stroke:#174b73;stroke-width:2.4}
.structure-svg .branch{fill:#174b73}
.structure-svg .sum-sign{font:24px "Times New Roman",serif;fill:#174b73}
.structure-svg .math-label foreignObject div{height:100%;display:flex;justify-content:center;align-items:center;color:#172b3a;font-size:20px}
.multirate-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.multirate-svg .wire{fill:none;stroke:#174b73;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}.multirate-svg .block{fill:#f4f7f8;stroke:#0d8794;stroke-width:2}.multirate-svg .label{fill:#315d7c;font:17px "Microsoft YaHei",sans-serif}.multirate-svg .annotation{fill:#587083;font:14px "Microsoft YaHei",sans-serif}.multirate-svg .axis{fill:none;stroke:#315d7c;stroke-width:1.7;stroke-linecap:round}.multirate-svg .spectrum-a{fill:none;stroke:#0d8794;stroke-width:2.4;stroke-linejoin:round}.multirate-svg .spectrum-b{fill:none;stroke:#b56b2e;stroke-width:2.4;stroke-linejoin:round}.multirate-svg .panel{fill:#fff;stroke:#d8e0e5;stroke-width:1.2}.multirate-svg .math-label div{height:100%;display:flex;align-items:center;justify-content:center;color:#172b3a;font-size:17px;white-space:nowrap;overflow:visible}
.chain-svg,.spectrum-svg,.wheel-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.chain-svg .chain-box{fill:#f4f7f8;stroke:#b08d57;stroke-width:1.6}.chain-svg .chain-label{fill:#1e4f79;font:18px "Microsoft YaHei",sans-serif}.chain-svg .chain-arrow{fill:none;stroke:#174b73;stroke-width:2.1;stroke-linecap:round}
.spectrum-svg .axis,.spectrum-svg .guide{fill:none;stroke:#174b73;stroke-linecap:round}.spectrum-svg .axis{stroke-width:2.1}.spectrum-svg .guide{stroke-width:1.5}.spectrum-svg .replica{fill:none;stroke-width:3;stroke-linejoin:round}
.wheel-svg .wheel-rim{fill:none;stroke:#b6342d;stroke-width:4}.wheel-svg .spoke{fill:none;stroke:#0f8b8d;stroke-width:2.5}.wheel-svg .hub{fill:#f4f7f8;stroke:#b6342d;stroke-width:3}.wheel-svg .marker{fill:#174b73}.wheel-svg .wheel-label{fill:#1e4f79;font:17px "Microsoft YaHei",sans-serif}.wheel-svg .wheel-note{fill:#51697b;font:15px "Microsoft YaHei",sans-serif}
.signal-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.signal-svg .axis{fill:none;stroke:#174b73;stroke-width:2}
.signal-svg .guide{fill:none;stroke:#174b73;stroke-width:1.45}.signal-svg .overlap{fill:none;stroke:#b13a3a;stroke-width:3}.signal-svg .separated,.signal-svg .replica{fill:none;stroke:#0f8b8d;stroke-width:3;stroke-linejoin:round}.signal-svg .passband{fill:none;stroke:#b08d57;stroke-width:2.2}.signal-svg .band-fill{fill:#dceff0;stroke:#0f8b8d;stroke-width:2}.signal-svg .dimension{fill:none;stroke:#b08d57;stroke-width:1.7}.signal-svg .plain-label,.signal-svg .figure-note{fill:#486d8b;font:16px "Microsoft YaHei",sans-serif}.signal-svg .bad-note{fill:#b13a3a;font:16px "Microsoft YaHei",sans-serif}.signal-svg .good-note{fill:#0f8b8d;font:16px "Microsoft YaHei",sans-serif}.signal-svg .sinc-primary{fill:none;stroke:#0f8b8d;stroke-width:3}.signal-svg .sinc-secondary{fill:none;stroke:#78babc;stroke-width:2}.signal-svg .sample-dot{fill:#b56b2e}
.signal-svg .stem{stroke:#b45309;stroke-width:2}
.signal-svg .hold{fill:none;stroke:#0f8b8d;stroke-width:3;stroke-linejoin:round}
.signal-svg .dot{fill:#b45309}.signal-svg .tick{stroke:#174b73;stroke-width:1.3}
.signal-svg .label{fill:#374c5b;font:16px "Microsoft YaHei",sans-serif}
.signal-svg .conv-line{fill:none;stroke:#008f95;stroke-width:3}
.fir-flow-svg,.fir-symmetry-svg,.fir-pz-svg,.fir-sampling-svg{display:block;width:100%;height:auto;background:#fbfcfd;border:1px solid #d8e0e5;border-radius:5pt}
.fir-flow-svg .box{fill:#f4f7f8;stroke:#0d8794;stroke-width:2}.fir-flow-svg .freq-box{fill:#fff8df;stroke:#b08d57;stroke-width:2}.fir-flow-svg .wire{fill:none;stroke:#174b73;stroke-width:2.4}.fir-flow-svg .arrow{fill:none;stroke:#174b73;stroke-width:2.4;marker-end:url(#fir-flow-arrow)}.fir-flow-svg .label,.fir-symmetry-svg .label,.fir-pz-svg .label,.fir-sampling-svg .label{fill:#243746;font:16px "Microsoft YaHei",sans-serif}.fir-flow-svg .math,.fir-symmetry-svg .math,.fir-pz-svg .math,.fir-sampling-svg .math{fill:#172b3a;font:italic 19px "Times New Roman",serif}.fir-flow-svg .caption,.fir-symmetry-svg .caption,.fir-pz-svg .caption,.fir-sampling-svg .caption{fill:#486d8b;font:15px "Microsoft YaHei",sans-serif}
.math-foreign>div{width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#172b3a;font-size:16px;line-height:1;overflow:visible}.math-foreign mjx-container{margin:0!important}
.fir-symmetry-svg .axis,.fir-pz-svg .axis,.fir-sampling-svg .axis{fill:none;stroke:#174b73;stroke-width:2}.fir-symmetry-svg .guide{stroke:#8ba1b0;stroke-width:1.5;stroke-dasharray:5 4}.fir-symmetry-svg .stem{stroke:#b45309;stroke-width:2.2}.fir-symmetry-svg .dot{fill:#b45309}.fir-symmetry-svg .mirror{stroke:#0d8794;stroke-width:1.8;stroke-dasharray:5 4}.fir-pz-svg .unit{fill:none;stroke:#8ba1b0;stroke-width:1.7}.fir-pz-svg .zero{fill:#fff;stroke:#0d8794;stroke-width:3}.fir-pz-svg .pole{stroke:#b6342d;stroke-width:3}.fir-sampling-svg .ideal{fill:none;stroke:#0d8794;stroke-width:2.5;stroke-dasharray:7 4}.fir-sampling-svg .response{fill:none;stroke:#174b73;stroke-width:3}.fir-sampling-svg .stem{stroke:#b45309;stroke-width:2}.fir-sampling-svg .dot{fill:#b45309}.fir-sampling-svg .transition{fill:#fbf0e7;stroke:none}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.formula-wide{font-size:9pt}.mapping,.table{font-size:9.5pt}.chart-grid,.grid{grid-template-columns:1fr}}
</style>
"""


def _main_body(html: str) -> str:
    match = re.search(r"<main(?:\s[^>]*)?>(.*)</main>", html, flags=re.DOTALL)
    if not match:
        raise ValueError("main-body component is missing its main container")
    return match.group(1)


def _render_component_bodies(components: tuple, directory: Path) -> str:
    bodies = []
    for component in components:
        path = component.write_html(directory / f"{component.__name__.split('.')[-1]}.html")
        bodies.append(_main_body(path.read_text(encoding="utf-8")))
    return "\n".join(bodies)


def _demote_headings(body: str) -> str:
    def replace(match: re.Match[str]) -> str:
        closing, level = match.group(1), int(match.group(2))
        return f"<{closing}h{level + 1}>"

    return re.sub(r"<(/?)h([1-3])>", replace, body)


def _keep_first_heading_as_chapter_title(body: str) -> str:
    match = re.search(r"<h1>.*?</h1>", body, flags=re.DOTALL)
    if not match:
        raise ValueError("chapter body is missing its chapter title")
    return f"{match.group(0)}{_demote_headings(body[match.end():])}"


def _with_chapter_title(title: str, body: str) -> str:
    return f"<h1>{title}</h1>{_demote_headings(body)}"


def _chapters() -> list[str]:
    with tempfile.TemporaryDirectory(prefix="dsp-all-main-body-") as directory:
        temporary = Path(directory)
        chapter_one_path = chapter_one.write_html(temporary / "chapter-one.html")
        chapter_two_path = chapter_two.write_html(temporary / "chapter-two.html")
        raw = [
            _main_body(chapter_one_path.read_text(encoding="utf-8")),
            _main_body(chapter_two_path.read_text(encoding="utf-8")),
            _render_component_bodies(
                (
                    chapter_three_overview,
                    chapter_three_dfs,
                    chapter_three_dft,
                    chapter_three_lsi_output,
                    chapter_three_frequency_sampling,
                    chapter_three_spectrum,
                ),
                temporary,
            ),
            _render_component_bodies(
                (chapter_four_efficiency, chapter_four_dit, chapter_four_dif_ifft),
                temporary,
            ),
            _render_component_bodies((chapter_five,), temporary),
            _render_component_bodies((chapter_six,), temporary),
            _render_component_bodies((chapter_seven,), temporary),
            _render_component_bodies((chapter_eight,), temporary),
        ]
    raw[0] = _keep_first_heading_as_chapter_title(raw[0])
    raw[2] = _keep_first_heading_as_chapter_title(raw[2])
    raw[3] = _with_chapter_title("第四章 快速傅里叶变换", raw[3])
    return raw


def write_html(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    chapters = "\n".join(
        f'<section class="chapter-start">{body}</section>' for body in _chapters()
    )
    document = (
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<script>window.MathJax={tex:{packages:{"[+]": ["ams"]}}};</script>'
        f'<script defer src="{MATHJAX}"></script>{STYLE}<body><main>{chapters}</main></body></html>'
    )
    output.write_text(document, encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_html(ROOT / "full" / "outputs" / "dsp_main_body.html"))
