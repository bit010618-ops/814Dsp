"""Assemble chapter two's main body without training or answer modules."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from full.tools import (
    build_chapter_02_dtft_mathjax_component as dtft,
    build_chapter_02_foundations_mathjax_component as foundations,
    build_chapter_02_inverse_properties_mathjax_component as inverse_properties,
    build_chapter_02_special_filters_mathjax_component as special_filters,
    build_chapter_02_system_frequency_mathjax_component as system_frequency,
)
from full.tools.build_chapter_05_to_08_body import STYLE, _main_body
from full.tools.render_mathjax_formula import MATHJAX


COMPONENTS = (foundations, inverse_properties, dtft, system_frequency, special_filters)


def _combined_body() -> str:
    with tempfile.TemporaryDirectory(prefix="dsp-chapter-02-body-") as directory:
        temporary = Path(directory)
        bodies = []
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
    print(write_html(ROOT / "full" / "outputs" / "chapter_02_body.html"))
