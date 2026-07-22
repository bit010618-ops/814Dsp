from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_time_invariance_component import build_pdf, load_model


def test_time_invariance_component_preserves_core_examples_and_excludes_experiment(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [78, 79, 80, 81, 82]
    assert [item["source_page"] for item in model["excluded_by_user_scope"]] == [83]
    output = build_pdf(output_path=tmp_path / "time-invariance.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 3
    assert "仿真实验" not in text
    assert "滑动平均" in text
    assert "从零开始的累加器" in text
