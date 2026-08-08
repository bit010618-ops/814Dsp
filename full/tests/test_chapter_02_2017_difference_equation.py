"""Regression checks for the 2017 tenth question."""


def test_2017_tenth_question_preserves_all_parts_and_stable_two_sided_response(tmp_path):
    from full.tools import build_chapter_02_supplemental_training_batch_sixteen_mathjax_component as component

    html = component.write_html(tmp_path / "batch-sixteen.html").read_text(encoding="utf-8")

    assert "2017 年真题" in html
    assert r"y(n)=y(n-1)+y(n-2)+x(n-1)" in html
    assert r"H(z)=\frac{z^{-1}}{1-z^{-1}-z^{-2}}" in html
    assert r"z=\frac{1+\sqrt5}{2}" in html
    assert r"z=\frac{1-\sqrt5}{2}" in html
    assert r"\operatorname{ROC}:\frac{\sqrt5-1}{2}<\left|z\right|<\frac{1+\sqrt5}{2}" in html
    assert 'aria-label="2017 年第十题的零极点图"' in html
