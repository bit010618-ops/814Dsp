from pathlib import Path


def test_typical_sequences_component_uses_mathjax_and_real_svg(tmp_path: Path):
    from full.tools.build_chapter_01_typical_sequences_mathjax_component import write_html

    page = write_html(tmp_path / "typical.html").read_text(encoding="utf-8")

    assert "tex-mml-chtml.js" in page
    assert r"\begin{cases}" in page
    assert r"R_N(n)=u(n)-u(n-N)" in page
    assert r"x(n)=a^n u(n)" in page
    assert r"\omega=\Omega T" in page
    assert r"e^{(\sigma+j\omega)n}" in page
    assert "<image" not in page
    assert "drawImage" not in page
    assert page.count("<svg") >= 7
    assert 'data-index="-2"' in page
    assert 'class="next-page"' in page
    assert "break-before:page" not in page
    assert "MATLAB" not in page
