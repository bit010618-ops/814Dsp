from pathlib import Path


def test_system_frequency_and_geometry_are_reflowed_with_real_svg(tmp_path: Path):
    from full.tools.build_chapter_02_system_frequency_mathjax_component import write_html

    html = write_html(tmp_path / "system-frequency.html").read_text(encoding="utf-8")
    assert "mathjax@3" in html
    assert "page-break-after:always" not in html
    assert r"H(z)=\frac{Y(z)}{X(z)}=\mathcal{Z}\{h(n)\}" in html
    assert r"h(n)=0,\qquad n<0" in html
    assert r"\sum_{n=-\infty}^{\infty}\left|h(n)\right|<\infty" in html
    assert r"H(e^{j\omega})=\sum_{n=-\infty}^{\infty}h(n)e^{-j\omega n}" in html
    assert r"\left|H(e^{j\omega})\right|=\left|A\right|" in html
    assert '<svg' in html
    assert 'marker-end="url(#arrow)"' in html
    assert "drawImage" not in html
    assert "<image" not in html
