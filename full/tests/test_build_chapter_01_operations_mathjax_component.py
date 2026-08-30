from pathlib import Path


def test_operations_component_uses_mathjax_and_data_driven_svg(tmp_path: Path):
    from full.tools.build_chapter_01_operations_mathjax_component import write_html

    page = write_html(tmp_path / "operations.html").read_text(encoding="utf-8")

    assert "tex-mml-chtml.js" in page
    assert r"y(n)=x_1(n)+x_2(n)" in page
    assert r"y(n)=x(-n)" in page
    assert r"\sum_{k=-\infty}^{n}x(k)" in page
    assert r"\frac{1}{2N+1}" in page
    assert "<image" not in page
    assert "drawImage" not in page
    assert page.count("<svg") >= 6
    assert 'data-index="0"' in page
    assert 'data-index="-2"' in page
    assert "复习提示" not in page
