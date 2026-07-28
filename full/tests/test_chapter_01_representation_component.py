import sys
from pathlib import Path
import re

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "full" / "tools"))

from build_chapter_01_representation_component import build_pdf, load_model


def test_representation_model_covers_source_pages_and_merges_only_exact_repeat():
    model = load_model(ROOT)

    assert model["source_pages"] == list(range(9, 16))
    assert model["component_status"] == "rendered_and_visually_verified_for_integration"
    assert model["exact_repeat_merge"] == {"source_page": 15, "merged_with": 10}
    assert r"\delta(n)=\begin{cases}1,&n=0\\0,&n\ne0\end{cases}" in model["formal_formulae"]
    assert r"x(n)=\sum_{m=-\infty}^{\infty}x(m)\delta(n-m)" in model["formal_formulae"]
    assert model["sample_plot"]["values"]["5"] == -2
    assert model["coordinate_label_rule"]["horizontal_tick_offset_pt"] == 4


def test_representation_component_flows_the_next_complete_graph_section_on_to_the_delta_page(tmp_path):
    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_representation_component.pdf")

    reader = PdfReader(str(output))
    assert "用图形表示离散时间信号" in (reader.pages[0].extract_text() or "")
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    # The parent component now carries the section heading and lead-in to
    # avoid a large blank area before this component begins.
    assert "用数列与函数表示" in text
    assert "单位抽样序列" in text
    assert "移位加权和" in text


def test_representation_component_preserves_original_unit_sample_example_prompt(tmp_path):
    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_representation_component.pdf")

    reader = PdfReader(str(output))
    text = re.sub(r"\s+", "", "".join(page.extract_text() or "" for page in reader.pages))
    assert "例：用单位抽样序列" in text
    assert "表示任意序列" in text


def test_unit_sample_piecewise_definition_is_rendered_as_one_standard_cases_formula():
    builder = (ROOT / "full" / "tools" / "build_chapter_01_representation_component.py").read_text(encoding="utf-8")

    assert "height = 64" in builder
    assert "def _draw_cases_brace" in builder
    assert "curveTo" in builder
    assert 'page.roundRect(x, bottom, width, height' in builder
