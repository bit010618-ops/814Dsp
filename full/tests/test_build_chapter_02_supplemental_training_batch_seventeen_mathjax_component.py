from pathlib import Path


def test_batch_seventeen_preserves_the_2016_transform_relations_prompt(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_seventeen_mathjax_component as component

    html = component.write_html(tmp_path / "batch-seventeen.html").read_text(encoding="utf-8")

    assert "2016 年真题" in html
    assert "二、简答题第 1 小题：说明" in html
    assert r"\(\mathrm{FT}\)、\(\mathrm{LT}\)、\(\mathrm{ZT}\) 的关系；" in html
    assert r"X(j\Omega)=X(s)\big|_{s=j\Omega}" in html
    assert r"X\!\left(e^{j\omega}\right)=X(z)\big|_{z=e^{j\omega}}" in html


def test_batch_seventeen_uses_mathjax_for_the_transform_relations(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_seventeen_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-seventeen.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
