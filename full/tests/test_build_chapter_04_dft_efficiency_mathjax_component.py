from pathlib import Path


def test_chapter_four_efficiency_component_preserves_direct_dft_counts(tmp_path: Path):
    from full.tools import build_chapter_04_dft_efficiency_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-04-efficiency.html").read_text(encoding="utf-8")

    assert "4.1 直接计算 DFT 的问题及改进途径" in html
    assert r"N^2" in html
    assert r"N(N-1)" in html
    assert "171479025" in html
    assert r"f_s=11025\,\mathrm{Hz}" in html
    assert r"171.479025\,\mathrm{s}" in html
    assert r"\left(W_N^{nk}\right)^*=W_N^{-nk}" in html
    assert r"W_N^{nk}=W_N^{(N+n)k}=W_N^{n(N+k)}" in html
    assert r"W_N^{N/2}=-1" in html
    assert ",mathrm" not in html
    assert "DIT" in html and "DIF" in html
    assert "MATLAB" not in html
