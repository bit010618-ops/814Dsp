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
figure{break-inside:avoid;margin:12pt auto;text-align:center}
.chart-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9pt;align-items:start}
.chart-grid figure{width:100%;margin:6pt auto 10pt}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9pt;align-items:start}
.grid svg{width:100%;height:auto}
svg{max-width:100%;height:auto}
@media(max-width:560px){body{font-size:10.5pt}.formula{padding:7pt 8pt}.chart-grid,.grid{grid-template-columns:1fr}}
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
