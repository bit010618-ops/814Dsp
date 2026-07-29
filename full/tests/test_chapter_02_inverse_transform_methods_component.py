from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_02_inverse_transform_methods_component import build_pdf


def test_inverse_transform_methods_component_preserves_source_examples(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "chapter-02-inverse-methods.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    normalized = "".join(text.split())

    assert len(reader.pages) == 3
    for required in (
        "部分分式展开法",
        "幂级数展开法",
        "例",
        "收敛域",
        "系数比较",
        "长除法",
        "方法比较",
    ):
        assert required in normalized
    assert "MATLAB" not in normalized
    assert "源课件" not in normalized
