from pathlib import Path
from pypdf import PdfReader
from full.tools.build_chapter_02_frequency_response_component import build_pdf


def test_frequency_response_component_keeps_core_concepts(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "chapter-02-frequency-response.pdf")
    reader = PdfReader(str(output))
    text = "".join("\n".join(page.extract_text() or "" for page in reader.pages).split())
    assert len(reader.pages) == 3
    for item in ("频率响应", "幅频响应", "相频响应", "群延迟", "实正弦输入", "低通"):
        assert item in text
    assert "MATLAB" not in text and "源课件" not in text
