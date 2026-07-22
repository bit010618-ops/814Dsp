from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_periodicity_component import build_pdf, load_model


def test_periodicity_component_preserves_non_code_source_content(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [59, 60, 61, 62, 63, 64, 65]
    assert [item["source_page"] for item in model["excluded_by_user_scope"]] == [66]
    output = build_pdf(output_path=tmp_path / "periodicity.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 3
    assert "MATLAB" not in text
    assert "源课件" not in text
    assert "源文件" not in text
    assert "周期序列的定义" in text
    assert "调幅序列" in text
