from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_linearity_component import build_pdf, load_model


def test_linearity_component_preserves_examples_and_excludes_experiment(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [70, 71, 72, 73, 74]
    assert [item["source_page"] for item in model["excluded_by_user_scope"]] == [75]
    output = build_pdf(output_path=tmp_path / "linearity.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 3
    assert "仿真实验" not in text
    assert "三点中值滤波器" in text
    assert "叠加原理" in text
