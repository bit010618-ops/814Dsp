from pathlib import Path


def test_dft_component_covers_definition_periodicity_and_circular_operations(tmp_path: Path):
    from full.tools import build_chapter_03_dft_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-dft.html").read_text(encoding="utf-8")

    assert "3.2 离散傅里叶变换的定义及性质" in html
    assert r"X(k)=\sum_{n=0}^{N-1}x(n)W_N^{nk}" in html
    assert r"x(n)=\frac{1}{N}\sum_{k=0}^{N-1}X(k)W_N^{-nk}" in html
    assert r"X(k)=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{N}}" in html
    assert "例题：序列 R_4(n) 的 DTFT、8 点 DFT 与 16 点 DFT" in html
    assert r"x\left((n-n_0)\bmod N\right)" in html
    assert r"\begin{aligned}" in html
    assert "MATLAB" not in html
