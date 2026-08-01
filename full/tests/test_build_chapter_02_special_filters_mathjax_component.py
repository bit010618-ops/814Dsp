from pathlib import Path


def test_special_filters_keep_core_theory_without_matlab(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")
    assert "mathjax@3" in html
    assert "page-break-after:always" not in html
    assert r"\frac{1}{2}(1+z^{-1})" in html
    assert r"\frac{1}{2}(1-z^{-1})" in html
    assert r"z=e^{\pm j\omega_0}" in html
    assert r"\left|H_{\mathrm{ap}}(e^{j\omega})\right|=1" in html
    assert r"H(z)=H_{\min}(z)H_{\mathrm{ap}}(z)" in html
    assert "MATLAB" not in html and "plot(" not in html
    assert "drawImage" not in html
