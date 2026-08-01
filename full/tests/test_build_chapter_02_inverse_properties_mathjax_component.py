from pathlib import Path


def test_inverse_and_properties_component_is_one_mathjax_flow(tmp_path: Path):
    from full.tools.build_chapter_02_inverse_properties_mathjax_component import write_html

    html = write_html(tmp_path / "inverse-properties.html").read_text(encoding="utf-8")

    assert "mathjax@3" in html
    assert "page-break-after:always" not in html
    assert r"\oint_C X(z)z^{n-1}\,\mathrm{d}z" in html
    assert r"\mathcal{Z}\{x(n-m)\}=z^{-m}X(z)" in html
    assert r"Y(z)=X(z)H(z)" in html
    assert r"\mathcal{Z}\{nx(n)\}=-z\frac{\mathrm{d}X(z)}{\mathrm{d}z}" in html
    assert "drawImage" not in html
    assert "<image" not in html
