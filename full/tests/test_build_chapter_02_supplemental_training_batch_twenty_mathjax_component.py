from pathlib import Path


def test_batch_twenty_preserves_the_2005_inverse_z_prompt(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_mathjax_component as component

    html = component.write_html(tmp_path / "batch-twenty.html").read_text(encoding="utf-8")

    assert "2005 年真题" in html
    assert "<p>一、计算</p>" in html
    assert "4.求" in html
    assert r"F(z)=\frac{z^2}{z^2-2z-3}" in html
    assert r"1<\left|z\right|<3" in html
    assert r"f[n]=\frac{1}{2}(-1)^n u[n]-\frac{1}{2}3^n u[-n-1]" in html


def test_batch_twenty_renders_inverse_z_formulas_with_mathjax(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-twenty.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
