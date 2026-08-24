from pathlib import Path


def test_representation_component_is_a_reflowing_mathjax_and_svg_document(tmp_path: Path):
    from full.tools.build_chapter_01_representation_mathjax_component import write_html

    output = write_html(tmp_path / "representation.html")
    page = output.read_text(encoding="utf-8")

    assert "tex-mml-chtml.js" in page
    assert r"\begin{cases}" in page
    assert r"x_1(n)=\{1,2,3,4,5\}" in page
    assert r"x_2(n)=\{1,2,3,4,5\}" in page
    assert r"x_3(n)=\{0,0,1,2,3,4,5\}" in page
    assert r"x_4(n)=A\sin(\omega n+\varphi)" in page
    assert r"x(n)=\sum_{m=-\infty}^{\infty}x(m)\delta(n-m)" in page
    assert r"x(n)=\delta(n)+2\delta(n-1)+3\delta(n-2)" in page
    assert page.count("<svg ") >= 5
    assert "data-index=\"-1\"" in page
    assert "data-index=\"2\"" in page
    assert "page-break-after" not in page
    assert "section { break-inside: avoid;" not in page
    assert '<p class="eyebrow">' not in page
    assert ".chapter { width:100%; max-width:100%;" in page
    assert ".chart { margin-left:0; margin-right:0; }" in page
    assert "<image" not in page
