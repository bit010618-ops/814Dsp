from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_analog_digital_chain_component import build_pdf, load_model


def test_analog_digital_chain_component_keeps_the_complete_conversion_chain(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [169, 170, 171, 172, 173, 174, 175, 176]
    assert model["reused_direct_rewrite_source_pages"] == [171]
    output = build_pdf(output_path=tmp_path / "analog-digital-chain.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 4
    assert "源课件" not in text
    assert "源文件" not in text
    assert "根据原课件" not in text
