from pathlib import Path


def test_dft_component_covers_definition_periodicity_and_circular_operations(tmp_path: Path):
    from full.tools import build_chapter_03_dft_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-dft.html").read_text(encoding="utf-8")

    assert "3.2 离散傅里叶变换的定义及性质" in html
    assert r"X(k)=\sum_{n=0}^{N-1}x(n)W_N^{nk}" in html
    assert r"x(n)=\frac{1}{N}\sum_{k=0}^{N-1}X(k)W_N^{-nk}" in html
    assert r"X(k)=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{N}}" in html
    assert r"例题：序列 \(R_4(n)\) 的 DTFT、8 点 DFT 与 16 点 DFT" in html
    assert r"x\left((n-n_0)\bmod N\right)" in html
    assert r"\begin{aligned}" in html
    assert "MATLAB" not in html


def test_dft_component_preserves_the_eight_point_circular_shift_example(tmp_path: Path):
    from full.tools import build_chapter_03_dft_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-dft.html").read_text(encoding="utf-8")

    assert r"\(x(n)=\{1,2,3,4\}\)" in html
    assert r"x\left((n+2)\bmod8\right)" in html
    assert r"\{3,4,0,0,0,0,1,2\}" in html
    assert r"x\left((-3-2)\bmod8\right)=x\left((-5)\bmod8\right)=x(3)=4" in html
    assert r"Y(k)=W_4^{3k}X(k)" in html
    assert r"\left\{\frac{3}{4},\frac{2}{4},\frac{1}{4},1\right\}" in html
