from pathlib import Path


def test_chapter_two_body_only_assembly_excludes_training_and_answers(tmp_path: Path):
    from full.tools.build_chapter_02_body_only import write_html

    html = write_html(tmp_path / "chapter-two-body.html").read_text(encoding="utf-8")

    for heading in (
        "z 变换的基本概念",
        "离散时间信号傅里叶变换",
        "系统函数及其与系统性质的关系",
        "特殊滤波器的设计",
    ):
        assert heading in html
    assert html.count("<main>") == 1
    assert "真题" not in html
    assert "MATLAB" not in html
    assert "page-break-after:always" not in html
