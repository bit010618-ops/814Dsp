from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_sampling_recovery_component import build_pdf, load_model


def test_sampling_recovery_component_keeps_reconstruction_and_interpolation_core(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [161, 162, 163, 165, 166]
    assert model["merged_pages"][1]["source_pages"] == [164, 165]
    output = build_pdf(output_path=tmp_path / "sampling-recovery.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 4
    assert "重构的时域表达" in (reader.pages[0].extract_text() or "")
    assert "内插函数" in (reader.pages[1].extract_text() or "")
    assert "采样点处的严格插值" in (reader.pages[2].extract_text() or "")
    assert "源课件" not in text
    assert "源文件" not in text
