"""Assemble the third and fourth chapters' main-body components only."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools import (
    build_chapter_03_dfs_mathjax_component as dfs,
    build_chapter_03_dft_mathjax_component as dft,
    build_chapter_03_frequency_sampling_mathjax_component as frequency_sampling,
    build_chapter_03_lsi_output_mathjax_component as lsi_output,
    build_chapter_03_overview_mathjax_component as overview,
    build_chapter_03_spectrum_analysis_mathjax_component as spectrum_analysis,
    build_chapter_04_dft_efficiency_mathjax_component as dft_efficiency,
    build_chapter_04_dif_ifft_optimization_mathjax_component as dif_ifft,
    build_chapter_04_dit_fft_mathjax_component as dit_fft,
)
from full.tools.build_chapter_05_to_08_body import STYLE, _main_body
from full.tools.render_mathjax_formula import MATHJAX


COMPONENTS = (
    overview,
    dfs,
    dft,
    lsi_output,
    frequency_sampling,
    spectrum_analysis,
    dft_efficiency,
    dit_fft,
    dif_ifft,
)


def _combined_body() -> str:
    with tempfile.TemporaryDirectory(prefix="dsp-chapter-03-to-04-") as directory:
        temporary = Path(directory)
        bodies = []
        for component in COMPONENTS:
            component_file = component.write_html(
                temporary / f"{component.__name__.split('.')[-1]}.html"
            )
            bodies.append(_main_body(component_file.read_text(encoding="utf-8")))
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
    print(write_html(ROOT / "full" / "outputs" / "chapter_03_to_04_body.html"))
