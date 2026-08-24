from pathlib import Path


def test_convolution_basics_uses_mathjax_and_data_driven_stem_plots(tmp_path: Path):
    from full.tools.build_chapter_01_convolution_basics_mathjax_component import write_html

    page = write_html(tmp_path / "convolution.html").read_text(encoding="utf-8")

    assert "tex-mml-chtml.js" in page
    assert r"\sum_{m=-\infty}^{\infty}x(m)h(n-m)" in page
    assert r"x(n)*\delta(n-n_0)=x(n-n_0)" in page
    assert r"y(n)=h(n)+2h(n-1)" in page
    source = Path("full/tools/build_chapter_01_convolution_basics_mathjax_component.py").read_text(encoding="utf-8")
    assert "render_stem_svg" in source
    assert "<image" not in page
    assert "drawImage" not in page
