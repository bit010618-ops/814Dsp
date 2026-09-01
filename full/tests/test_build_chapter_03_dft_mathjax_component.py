from pathlib import Path


def test_dft_component_covers_definition_periodicity_and_circular_operations(tmp_path: Path):
    from full.tools import build_chapter_03_dft_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-dft.html").read_text(encoding="utf-8")

    assert "3.2 离散傅里叶变换的定义及性质" in html
    assert r"X(k)=\sum_{n=0}^{N-1}x(n)W_N^{nk}" in html
    assert r"x(n)=\frac{1}{N}\sum_{k=0}^{N-1}X(k)W_N^{-nk}" in html
    assert r"X(k)=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{N}}" in html
    assert r"例题：序列 \(R_4(n)\) 的 DTFT、8 点 DFT 与 16 点 DFT" in html
    assert r"x\left((n-n_0)\right)_N" in html
    assert r"x_{\mathrm{ep}}(n)&=\frac{1}{2}" in html
    assert r"x_{\mathrm{op}}(n)&=\frac{1}{2}" in html
    assert r"X(k)=X^*\left((N-k)\right)_N" in html
    assert r"\begin{aligned}" in html
    assert "MATLAB" not in html


def test_dft_component_preserves_the_eight_point_circular_shift_example(tmp_path: Path):
    from full.tools import build_chapter_03_dft_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-dft.html").read_text(encoding="utf-8")

    assert r"\(x(n)=\{1,2,3,4\}\)" in html
    assert r"x\left((n+2)\right)_8" in html
    assert r"\{3,4,0,0,0,0,1,2\}" in html
    assert r"x\left((-3-2)\right)_8=x\left((-5)\right)_8=x(3)=4" in html
    assert r"\bmod" not in html
    assert r"\operatorname{mod}" not in html
    assert r"\mathrm{mod}" not in html
    assert r"\pmod" not in html
    assert "按模" not in html
    assert r"按 \(N\) 周期理解" in html
    assert r"Y(k)=W_4^{3k}X(k)" in html
    assert r"\left\{\frac{3}{4},\frac{2}{4},\frac{1}{4},1\right\}" in html


def test_dft_component_preserves_the_six_point_circular_convolution_example(tmp_path: Path):
    from full.tools import build_chapter_03_dft_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-dft.html").read_text(encoding="utf-8")

    assert r"例题：6 点圆周卷积" in html
    assert r"x_1(n)=R_5(n)" in html
    assert r"x_2(n)=n+1" in html
    assert r"\{4,3,6,6,6,5\}" in html


def test_dft_component_keeps_circular_shift_visual_and_basic_sequence_pairs(tmp_path: Path):
    from full.tools import build_chapter_03_dft_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-dft.html").read_text(encoding="utf-8")

    assert 'data-plot="circular-shift-cycle"' in html
    assert "周期延拓、移位与主值区间截取" in html
    assert r"\delta(n-m)R_N(n)" in html
    assert r"R_N(n)\quad\longleftrightarrow\quad N\delta(k)R_N(k)" in html
    assert r"e^{j\frac{2\pi}{N}mn}R_N(n)" in html


def test_dft_component_keeps_spectral_line_example_and_real_imaginary_pair(tmp_path: Path):
    from full.tools import build_chapter_03_dft_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-dft.html").read_text(encoding="utf-8")

    assert r"x(n)&=\cos\left(\frac{3\pi}{5}n\right)\sin\left(\frac{4\pi}{5}n\right)" in html
    assert r"\frac{5}{2j}\left[\delta(k-1)-\delta(k-3)+\delta(k-7)-\delta(k-9)\right]" in html
    assert r"\operatorname{DFT}\left\{\operatorname{Re}\{x(n)\}\right\}" in html
    assert r"\operatorname{DFT}\left\{\operatorname{Im}\{x(n)\}\right\}" in html
