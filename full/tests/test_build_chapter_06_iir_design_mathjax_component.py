from pathlib import Path


def test_chapter_six_component_covers_the_five_source_sections(tmp_path: Path):
    from full.tools import build_chapter_06_iir_design_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-06.html").read_text(encoding="utf-8")

    titles = (
        "6.1 数字滤波器设计方法概述",
        "6.2 模拟滤波器的设计",
        "6.3 脉冲响应不变法",
        "6.4 双线性变换法",
        "6.5 IIR 数字滤波器设计方法小结",
    )
    positions = [html.index(title) for title in titles]
    assert positions == sorted(positions)
    assert r"H_a(s)=H(z)\big|_{z=e^{sT}}" in html
    assert r"s=\frac{2}{T}\frac{1-z^{-1}}{1+z^{-1}}" in html
    assert "MATLAB" not in html
    assert "真题" not in html
