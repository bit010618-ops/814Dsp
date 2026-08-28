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


def test_lsi_output_component_preserves_circular_length_and_self_convolution_examples(
    tmp_path: Path,
):
    from full.tools import build_chapter_03_lsi_output_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-lsi.html").read_text(encoding="utf-8")

    assert "例题：不同长度的圆周卷积" in html
    assert r"x_1(n)=R_5(n)" in html
    assert r"\{7,8,9,6\}" in html
    assert r"\{6,6,6,6,6\}" in html
    assert r"\{4,3,6,6,6,5\}" in html
    assert r"\{1,3,6,6,6,5,3\}" in html
    assert "例题：4 点 DFT 的自卷积" in html
    assert r"x(n)=\delta(n)+2\delta(n-2)+\delta(n-3)" in html
    assert r"X(0)&=4" in html
    assert r"y(n)=x(n)\circledast_4x(n)=\{5,4,5,2\}" in html
    assert r"Y(k)=X(k)X(k)" in html
