from pathlib import Path


def test_lsi_output_component_covers_zero_padding_and_overlap_methods(tmp_path: Path):
    from full.tools import build_chapter_03_lsi_output_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-lsi.html").read_text(encoding="utf-8")

    assert "3.3 用 DFT 求解 LSI 系统输出" in html
    assert r"Y(k)=X(k)H(k)" in html
    assert r"N\geq N_1+N_2-1" in html
    assert "重叠相加法" in html
    assert "重叠保留法" in html
    assert r"L_0=M+N_2-1" in html
    assert "MATLAB" not in html
