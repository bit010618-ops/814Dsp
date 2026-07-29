from pathlib import Path
from pypdf import PdfReader
from full.tools.build_chapter_02_system_function_component import build_pdf


def test_system_function_component_preserves_causality_stability_and_example(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "chapter-02-system-function.pdf")
    reader = PdfReader(str(output))
    text = "".join("\n".join(page.extract_text() or "" for page in reader.pages).split())
    assert len(reader.pages) == 3
    for item in ("系统函数", "因果", "稳定", "单位圆", "差分方程", "收敛域"):
        assert item in text
    assert "MATLAB" not in text and "源课件" not in text
