from pathlib import Path


def test_z_transform_foundations_component_uses_mathjax_and_vector_diagrams(tmp_path: Path):
    from full.tools.build_chapter_02_foundations_mathjax_component import write_html

    html = write_html(tmp_path / "foundations.html").read_text(encoding="utf-8")

    assert "mathjax@3" in html
    assert "page-break-after:always" not in html
    assert r"\sum_{n=-\infty}^{\infty}x(n)z^{-n}" in html
    assert r"\left|z\right|=e^{\sigma T}" in html
    assert r"\begin{cases}" in html
    assert "四种典型序列的 ROC 形状" in html
    assert r"\left|z\right|>\left|p_{\max}\right|" in html
    assert "给定极点时 ROC 的可能性" in html
    assert r"\(p_{\max}\)" in html
    assert r"\(X(z)\)" in html
    assert "(p_{\\max})" not in html
    assert "(X(z))" not in html
    assert "z_plane_svg" in html
    assert "<svg" in html
    assert "drawImage" not in html
    assert "<image" not in html
