from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_02_dtft_basics_component import build_pdf


def test_dtft_basics_component_keeps_source_order_and_definitions(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "chapter-02-dtft-basics.pdf")
    reader = PdfReader(str(output))
    normalized = "".join("\n".join(page.extract_text() or "" for page in reader.pages).split())

    assert len(reader.pages) == 3
    for required in ("离散时间信号傅里叶变换", "正变换", "反变换", "收敛条件", "周期", "z变换", "单位圆"):
        assert required in normalized
    assert "MATLAB" not in normalized
    assert "源课件" not in normalized
