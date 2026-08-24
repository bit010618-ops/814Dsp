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
    assert r"时间间隔 \(T\) 等间隔取样" in html
    assert r"\frac{f_s}{4}" in html
    assert r"\frac{f_s}{16}" in html


def test_opening_keeps_the_four_sampling_rate_waveform_comparison(tmp_path: Path):
    """The source's sampling-rate comparison is a required knowledge figure, not prose only."""
    from full.tools.build_chapter_01_body_only import write_html

    html = write_html(tmp_path / "chapter-one-body.html").read_text(encoding="utf-8")

    assert 'class="sampling-rate-comparison"' in html
    for role in ("continuous-waveform", "quarter-rate", "eighth-rate", "sixteenth-rate"):
        assert f'data-role="{role}"' in html
    assert "不同采样频率下钢琴乐曲的赏析" in html
    # The four short rows must fit the opening page's remaining A4 space;
    # otherwise figure avoidance creates a conspicuous blank page tail.
    assert 'viewBox="0 0 980 330"' in html
    # WeasyPrint ignores CSS fill/stroke declarations on SVG primitives; the
    # printable source must therefore carry visual attributes on the shapes.
    assert '<rect fill="#ffffff" stroke="#c4ced6"' in html
    assert '<path fill="none" stroke="#174b73"' in html


def test_opening_keeps_the_continuous_to_discrete_signal_mapping_figure(tmp_path: Path):
    """Source page 7's sampling correspondence must remain visible, not prose only."""
    from full.tools.build_chapter_01_body_only import write_html

    html = write_html(tmp_path / "chapter-one-body.html").read_text(encoding="utf-8")

    assert 'class="continuous-discrete-mapping"' in html
    assert 'data-role="continuous-signal"' in html
    assert 'data-role="discrete-samples"' in html
    assert 'data-role="sampling-arrow"' in html
    assert "连续时间信号到离散序列的对应关系" in html
