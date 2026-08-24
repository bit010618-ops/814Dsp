from pathlib import Path


def test_linearity_component_uses_complete_mathjax_without_formula_images(tmp_path: Path):
    from full.tools.build_chapter_01_linearity_mathjax_component import write_html

    page = write_html(tmp_path / "linearity.html").read_text(encoding="utf-8")

    assert "tex-mml-chtml.js" in page
    assert r"T[a x_1(n)+b x_2(n)]" in page
    assert r"\sum_{i=1}^{N}" in page
    assert r"(a x_1+b x_2)^2" in page
    assert r"\operatorname{Mid}" in page
    assert r"T[x_1+x_2]\ne T[x_1]+T[x_2]" in page
    assert "<image" not in page
    assert "drawImage" not in page
