from pathlib import Path


def test_chapter_four_body_assembler_keeps_41_to_45_in_source_order(tmp_path: Path):
    from full.tools import build_chapter_04_mathjax_handout as handout

    html = handout.write_html(tmp_path / "chapter-04.html").read_text(encoding="utf-8")

    positions = [html.index(title) for title in (
        "4.1 直接计算 DFT 的问题及改进途径",
        "4.2 基于时间抽取的基-2-FFT 快速算法",
        "4.3 基于频率抽取的基-2-FFT 快速算法原理",
        "4.4 快速傅里叶反变换的实现方法",
        "4.5 进一步减少运算量的措施",
    )]
    assert positions == sorted(positions)
    assert "真题" not in html
    assert "MATLAB" not in html
