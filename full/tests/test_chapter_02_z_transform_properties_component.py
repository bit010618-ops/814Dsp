from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_02_z_transform_properties_component import build_pdf


def test_z_transform_properties_component_keeps_original_order(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "chapter-02-z-properties.pdf")
    reader = PdfReader(str(output))
    normalized = "".join("\n".join(page.extract_text() or "" for page in reader.pages).split())

    assert len(reader.pages) == 3
    for required in ("线性性质", "移位性质", "卷积和性质", "其他常用性质", "收敛域", "x(n)=u(n)-u(n-3)", "零极点相消"):
        assert required in normalized
    assert "MATLAB" not in normalized
    assert "源课件" not in normalized
