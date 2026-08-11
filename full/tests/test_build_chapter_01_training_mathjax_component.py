from pathlib import Path


def test_training_component_uses_mathjax_and_standard_svg_diagrams(tmp_path: Path):
    from full.tools.build_chapter_01_training_mathjax_component import write_html

    html = write_html(tmp_path / "training.html").read_text(encoding="utf-8")

    assert "mathjax@3" in html
    assert "page-break-after:always" in html
    assert r"T_{\max}" in html
    assert "training_system_svg" in html
    assert 'data-diagram="2006-system-structure"' in html
    assert '0.25' in html
    assert '0.4' in html
    assert '0.3' in html
    assert '0.2' in html
    assert r"\(x[n]\)" in html
    assert r"\(y[n]\)" in html
    assert r"\(z^{-1}\)" in html
    assert "z⁻¹" not in html
    assert "training_stem_svg" in html
    assert "<svg" in html
    assert "drawImage" not in html
    assert "<image" not in html
