from pathlib import Path


def test_convolution_properties_use_complete_mathjax_without_formula_images(tmp_path: Path):
    from full.tools.build_chapter_01_convolution_properties_mathjax_component import write_html

    page = write_html(tmp_path / "properties.html").read_text(encoding="utf-8")
    assert "mathjax@3" in page
    assert r"x(n)*h(n)=h(n)*x(n)" in page
    assert r"\bigl[x(n)*h_1(n)\bigr]*h_2(n)=x(n)*\bigl[h_1(n)*h_2(n)\bigr]" in page
    assert r"\[[" not in page
    assert r"N_1+N_3\leq n\leq N_2+N_4" in page
    assert r"\\&=x(n)+\alpha x(n-R)" in page
    assert r"r_{xy}(n)=x(n)*y(-n)" in page
    assert "break-after:page" not in page
    assert "<image" not in page
    assert "drawImage" not in page
