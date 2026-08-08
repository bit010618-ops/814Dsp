from pathlib import Path


def test_batch_five_preserves_2013_bilateral_z_transform_prompt(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_five_mathjax_component as component

    html = component.write_html(tmp_path / "batch-five.html").read_text(encoding="utf-8")

    assert "2013 年真题" in html
    assert "第二组·第 5 小题：已知" in html
    assert "2013 年真题·第二组第 5 小题" in html
    assert r"x[n]=\left(\frac13\right)^n u[n]+\left(\frac12\right)^n u[-n-1]" in html
    assert r"求 \(x[n]\) 的 \(z\) 变换 \(X(z)\)" in html


def test_batch_five_derives_each_roc_before_combining_them(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_five_mathjax_component as component

    html = component.write_html(tmp_path / "batch-five.html").read_text(encoding="utf-8")

    assert r"\left|z\right|>\frac13" in html
    assert r"\left|z\right|<\frac12" in html
    assert r"\frac13<\left|z\right|<\frac12" in html
    assert r"\frac{1}{1-\frac13z^{-1}}-\frac{1}{1-\frac12z^{-1}}" in html


def test_batch_five_browser_dom_has_no_raw_math_delimiters(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_five_mathjax_component as component

    html = component.write_html(tmp_path / "batch-five.html")
    dom = component.rendered_dom(html)

    assert "<mjx-container" in dom
    assert r"\(" not in dom
    assert r"\[" not in dom
