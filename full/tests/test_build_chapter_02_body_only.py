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
    assert "<h1>第二章 z 变换与 LSI 系统频域分析</h1>" in html
    assert html.count("<h1>") == 1
    assert "<h2>2.1 z 变换的基本概念</h2>" in html
    assert "真题" not in html
    assert "MATLAB" not in html
    assert "page-break-after:always" not in html
    assert ".property-table th,.property-table td{border:" in html
    assert "border-collapse:collapse" in html
    assert ".figure img{display:block;width:100%;max-width:148mm;" in html
    assert "main table th,main table td{border:.55pt solid #8299aa;" in html
    # The inverse-transform definition belongs to the dedicated inverse
    # component; assembling the body must not repeat its contour formula.
    assert html.count(r"\oint_C X(z)z^{n-1}\,\mathrm{d}z") == 1
