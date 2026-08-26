from pathlib import Path


def test_system_frequency_and_geometry_are_reflowed_with_coordinate_plot(tmp_path: Path):
    from full.tools.build_chapter_02_system_frequency_mathjax_component import write_html

    html = write_html(tmp_path / "system-frequency.html").read_text(encoding="utf-8")
    assert "tex-mml-chtml.js" in html
    assert "page-break-after:always" not in html
    assert r"H(z)=\frac{Y(z)}{X(z)}=\mathcal{Z}\{h(n)\}" in html
    assert r"h(n)=0,\qquad n<0" in html
    assert r"\sum_{n=-\infty}^{\infty}\left|h(n)\right|<\infty" in html
    assert r"h(n)=\frac{1}{3}\left[\delta(n+1)+\delta(n)+\delta(n-1)\right]" in html
    assert r"H(z)=\frac{1}{3}\left(z+1+z^{-1}\right)" in html
    assert r"\operatorname{ROC}:\quad 0<\left|z\right|<\infty" in html
    assert r"h'(n)=\frac{1}{3}\left[\delta(n)+\delta(n-1)+\delta(n-2)\right]" in html
    assert r"H'(z)=H(z)z^{-1}=\frac{1}{3}\left(1+z^{-1}+z^{-2}\right)" in html
    assert r"\operatorname{ROC}:\quad \left|z\right|>0" in html
    assert ".diagram-plot{width:min(100%,470pt);height:auto}" in html
    assert '<img class="diagram-plot"' in html
    assert "data:image/png;base64," in html
    assert r"H(e^{j\omega})=\sum_{n=-\infty}^{\infty}h(n)e^{-j\omega n}" in html
    assert r"20\log_{10}\left|H(e^{j\omega})\right|" in html
    assert r"\tau_g(\omega)=-\frac{\mathrm{d}}{\mathrm{d}\omega}\angle H(e^{j\omega})" in html
    assert r"e^{j(N-M)\omega}" in html
    assert r"\left|H(e^{j\omega})\right|=\left|A\right|" in html
    assert "data:image/svg+xml" not in html
    assert '<figure><svg' not in html
    assert "drawImage" not in html
    assert "<image" not in html
