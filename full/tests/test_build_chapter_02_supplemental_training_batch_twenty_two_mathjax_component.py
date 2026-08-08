from pathlib import Path


def test_2013_bilateral_z_transform_prompt_and_roc(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_two_mathjax_component as component

    html = component.write_html(tmp_path / "batch.html").read_text(encoding="utf-8")
    assert "2013 年真题" in html
    assert r"x[n]=\left(\frac{1}{3}\right)^n u[n]+\left(\frac{1}{2}\right)^n u[-n-1]" in html
    assert r"\frac{1}{3}<\left|z\right|<\frac{1}{2}" in html


def test_2013_bilateral_z_transform_renders_with_mathjax(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_two_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch.html"))
    assert "<mjx-container" in dom
    assert r"\(" not in dom
