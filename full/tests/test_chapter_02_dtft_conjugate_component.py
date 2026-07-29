from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_02_dtft_conjugate_component import build_pdf


def test_dtft_conjugate_component_preserves_property_and_example(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "chapter-02-dtft-conjugate.pdf")
    reader = PdfReader(str(output))
    text = "".join("\n".join(page.extract_text() or "" for page in reader.pages).split())

    assert len(reader.pages) == 3
    for required in ("共轭对称", "共轭反对称", "实序列", "实因果序列", "由实部恢复", "抵消"):
        assert required in text
    assert "MATLAB" not in text
    assert "源课件" not in text
