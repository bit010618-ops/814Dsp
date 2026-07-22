from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_convolution_basics_component import build_pdf, load_model


def test_convolution_basics_component_preserves_core_material_and_excludes_matlab(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [86, 87, 88, 89, 90, 91, 92, 93, 94, 95]
    assert [item["source_page"] for item in model["excluded_by_user_scope"]] == [96]
    output = build_pdf(output_path=tmp_path / "convolution-basics.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 4
    assert "MATLAB" not in text
    assert "线性卷积" in text
