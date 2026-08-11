from pathlib import Path


def test_chapter_three_to_four_body_assembly_excludes_training(tmp_path: Path):
    from full.tools.build_chapter_03_to_04_body import write_html

    html = write_html(tmp_path / "chapter-03-to-04-body.html").read_text(encoding="utf-8")

    assert "第三章 离散傅里叶变换" in html
    assert "4.1 直接计算 DFT 的问题及改进途径" in html
    assert "4.5 进一步减少运算量的措施" in html
    assert html.count("<main>") == 1
    assert "真题" not in html
    assert "MATLAB" not in html
    assert "page-break-after:always" not in html
