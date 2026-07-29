from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_02_z_transform_foundations_component import build_pdf


def test_z_transform_foundations_component_keeps_core_concepts(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "chapter-02-z-foundations.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 5
    for required in (
        "z 变换的定义",
        "收敛域",
        "s 平面与 z 平面的映射",
        "典型序列的收敛域",
        "LSI 系统的系统函数",
        "极点与收敛域",
        "判定顺序",
        "有限长序列",
        "z 反变换",
    ):
        assert required in text
    assert "源课件" not in text
    assert "MATLAB" not in text
