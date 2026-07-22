from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_applications_close_component import build_pdf, load_model


def test_applications_close_component_keeps_aliasing_and_chapter_closure(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == list(range(177, 186))
    output = build_pdf(output_path=tmp_path / "applications-close.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 4
    assert "源课件" not in text
    assert "源文件" not in text
