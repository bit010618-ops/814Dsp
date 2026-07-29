from pathlib import Path


def test_time_invariance_component_uses_complete_mathjax_without_formula_images(tmp_path: Path):
    from full.tools.build_chapter_01_time_invariance_mathjax_component import write_html

    page = write_html(tmp_path / "time_invariance.html").read_text(encoding="utf-8")

    assert "mathjax@3" in page
    assert r"T[x(n-k)]=y(n-k)" in page
    assert r"\sum_{m=-\infty}^{n}x(m)" in page
    assert r"\sum_{m=0}^{n}x(m)" in page
    assert r"x(2n-2k)\ne x(2n-k)" in page
    assert r"\frac{1}{M_2-M_1+1}" in page
    assert 'class="handoff-lede"' in page
    assert "break-after:page" in page
    assert "<image" not in page
    assert "drawImage" not in page
