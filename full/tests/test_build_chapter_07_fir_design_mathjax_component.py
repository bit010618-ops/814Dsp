from pathlib import Path


def test_chapter_seven_component_covers_four_source_sections(tmp_path: Path):
    from full.tools import build_chapter_07_fir_design_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-07.html").read_text(encoding="utf-8")

    titles = (
        "7.1 线性相位 FIR 数字滤波器的条件和特点",
        "7.2 利用窗函数法设计 FIR 滤波器",
        "7.3 利用频率采样法设计 FIR 滤波器",
        "7.4 利用等波纹逼近法设计 FIR 滤波器",
    )
    positions = [html.index(title) for title in titles]
    assert positions == sorted(positions)
    assert r"h(n)=\pm h(N-1-n)" in html
    assert r"h(n)=h_d(n)w(n)" in html
    assert r"h(n)=\frac{1}{N}\sum_{k=0}^{N-1}H(k)W_N^{-nk}" in html
    assert "MATLAB" not in html
    assert "真题" not in html
