import sys
from pathlib import Path

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


def test_representation_component_is_editable_three_page_pdf(tmp_path):
    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_representation_component.pdf")

    reader = PdfReader(str(output))
    assert len(reader.pages) == 3
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "离散时间信号的表示方法" in text
    assert "单位抽样序列" in text
    assert "移位加权和" in text
