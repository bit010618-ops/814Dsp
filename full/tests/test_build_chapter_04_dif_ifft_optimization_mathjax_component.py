from pathlib import Path


def test_dif_ifft_and_optimization_component_preserves_all_remaining_chapter_topics(tmp_path: Path):
    from full.tools import build_chapter_04_dif_ifft_optimization_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-04-dif-ifft.html").read_text(encoding="utf-8")

    assert "4.3 基于频率抽取的基-2-FFT 快速算法原理" in html
    assert r"x(n)+(-1)^k x\left(n+\frac{N}{2}\right)" in html
    assert r"X(2r)" in html and r"X(2r+1)" in html
    assert "输入正序、输出码位倒序" in html
    assert "4.4 快速傅里叶反变换的实现方法" in html
    assert r"\frac{1}{N}" in html
    assert "4.5 进一步减少运算量的措施" in html
    assert "四类蝶形单元" in html
    assert "线性调频 z 变换" in html
    assert r"x(n)A^{-n}W^{nk}" in html
    assert r"nk=\frac{1}{2}\left[n^2+k^2-(k-n)^2\right]" in html
    assert "高斯的遗憾" in html
    assert 'src="../assets/source-figures/ch04-dif-fft-n8-flow.png"' in html
    assert '<figure class="source-figure source-figure-flow">' in html
    assert "DIF-FFT 算法蝶形流图（N=8）" in html
    assert "MATLAB" not in html


def test_dif_ifft_component_renders_inline_formulae_as_mathjax(tmp_path: Path):
    from full.tools import build_chapter_04_dif_ifft_optimization_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-04-dif-ifft.html").read_text(encoding="utf-8")

    assert r"\(W_N^r=\pm1\)" in html
    assert r"\(N=2^M\)" in html
    assert r"(W_N^r=\pm1)" not in html
