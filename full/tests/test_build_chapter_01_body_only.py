from pathlib import Path


def test_chapter_one_body_only_uses_mathjax_body_components_without_training(tmp_path: Path):
    from full.tools.build_chapter_01_body_only import write_html

    html = write_html(tmp_path / "chapter-one-body.html").read_text(encoding="utf-8")

    for heading in (
        "第一章 离散时间信号与系统",
        "离散时间信号的由来",
        "离散时间信号的表示方法",
        "离散时间系统的线性性质",
        "常系数线性差分方程",
        "理想时域采样",
    ):
        assert heading in html
    assert html.count("<main>") == 1
    assert "真题" not in html
    assert "MATLAB" not in html
    assert "drawImage" not in html
    assert "钢琴音频" in html
    assert r"\frac{f_s}{4}" in html
    assert r"\frac{f_s}{16}" in html
