from pathlib import Path


def test_chapter_two_priority_training_preserves_questions_and_mathjax(tmp_path: Path):
    from full.tools.build_chapter_02_training_mathjax_component import write_html

    html = write_html(tmp_path / "chapter-two-training.html").read_text(encoding="utf-8")
    for label in ("2015 年真题", "2021 年真题", "2025 年真题"):
        assert label in html
    assert html.count("详解见 P.18") == 2
    assert html.count("详解见 P.19") == 1
    assert "离散因果 LTI 系统的系统函数" in html
    assert "若使" in html and "恢复出" in html
    assert "因果稳定的" in html and "LSI" in html
    assert "\\(H(z)\\)" in html
    assert "<svg" in html
    assert "水印" not in html
    assert "page-break-after:always" not in html
    assert ".answer{break-before" not in html
