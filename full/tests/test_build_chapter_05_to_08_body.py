from pathlib import Path


def test_chapter_five_to_eight_body_assembly_keeps_only_main_handout_content(
    tmp_path: Path,
):
    from full.tools.build_chapter_05_to_08_body import write_html

    html = write_html(tmp_path / "chapter-05-to-08-body.html").read_text(encoding="utf-8")

    for heading in (
        "第五章 数字滤波器结构",
        "第六章 IIR 数字滤波器设计",
        "第七章 FIR 数字滤波器设计",
        "第八章 多采样率数字信号处理",
    ):
        assert heading in html
    assert html.count("<main>") == 1
    assert "真题" not in html
    assert "MATLAB" not in html
    assert "page-break-after:always" not in html
