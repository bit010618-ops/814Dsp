from pathlib import Path


def test_dtft_and_conjugate_content_is_one_reflowed_mathjax_document(tmp_path: Path):
    from full.tools.build_chapter_02_dtft_mathjax_component import write_html

    html = write_html(tmp_path / "dtft.html").read_text(encoding="utf-8")
    assert "tex-mml-chtml.js" in html
    assert "page-break-after:always" not in html
    assert r"X(e^{j\omega})=\sum_{n=-\infty}^{\infty}x(n)e^{-j\omega n}" in html
    assert r"x(n)=\frac{1}{2\pi}\int_{-\pi}^{\pi}X(e^{j\omega})e^{j\omega n}\,\mathrm{d}\omega" in html
    assert r"X(e^{j(\omega+2\pi k)})=X(e^{j\omega})" in html
    assert r"\mathcal{F}\{\operatorname{Re}[x(n)]\}=X_e(e^{j\omega})" in html
    assert r"\mathcal{F}\{x_e(n)\}=\operatorname{Re}\{X(e^{j\omega})\}" in html
    assert r"\mathcal{F}\{x_o(n)\}=j\operatorname{Im}\{X(e^{j\omega})\}" in html
    assert r"x_e(n)&=x_{er}(n)+jx_{ei}(n)" in html
    assert r"x_{er}(n)&=x_{er}(-n)" in html
    assert r"x_{ei}(n)&=-x_{ei}(-n)" in html
    assert r"=X_r(e^{j\omega})." in html
    assert r"&=\frac{1}{2}\left[X(e^{j\omega})+X^*(e^{j\omega})\right]" in html
    assert r"\(x(n)\)" in html
    assert r"\(z=e^{j\omega}\)" in html
    assert r"\(h_o(-1)=-\frac{1}{2}\)" in html
    assert "[[" not in html and "]]" not in html
    assert r"h(n)=h_e(n)+h_o(n)=\delta(n)+\delta(n-1)" in html
    assert "drawImage" not in html
    assert "<image" not in html
