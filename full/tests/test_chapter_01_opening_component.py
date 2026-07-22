from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_opening_component import build_pdf, load_model


ROOT = Path(__file__).resolve().parents[2]


def test_opening_component_preserves_the_four_section_outline_without_source_identity(tmp_path: Path):
    model = load_model(ROOT)

    assert model["source_pages"] == [1]
    assert model["sections"] == [
        "1.1 离散时间信号——序列",
        "1.2 离散时间系统",
        "1.3 常系数线性差分方程",
        "1.4 连续时间信号的抽样",
    ]

    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_opening_component.pdf")
    reader = PdfReader(str(output))
    assert len(reader.pages) == 1
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "第一章 离散时间信号与系统" in text
    assert "1.4" in text
    assert "连续时间信号的抽样" in text
    for forbidden in ("源课件", "源文件", "原始材料", "根据原课件"):
        assert forbidden not in text
