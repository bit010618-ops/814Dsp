from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_applications_close_component import build_pdf, load_model


def test_applications_close_component_keeps_aliasing_and_chapter_closure(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == list(range(177, 186))
    output = build_pdf(output_path=tmp_path / "applications-close.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 2
    assert "源课件" not in text
    assert "源文件" not in text


def test_applications_close_carries_first_aliasing_formula_to_previous_page(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "applications-close.pdf")
    reader = PdfReader(str(output))
    first_page = reader.pages[0].extract_text() or ""
    assert "两个给出相同样值的连续信号" in first_page
