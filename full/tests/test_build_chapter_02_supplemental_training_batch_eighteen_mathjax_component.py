from pathlib import Path


def test_batch_eighteen_preserves_the_2017_laplace_z_mapping_prompt(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_eighteen_mathjax_component as component

    html = component.write_html(tmp_path / "batch-eighteen.html").read_text(encoding="utf-8")

    assert "2017 年真题" in html
    assert "二、简答题第 1 小题：在信号与系统里面，拉氏变换和" in html
    assert r"\(z\) 变换的对应关系是怎样的？" in html
    assert r"z=e^{sT}" in html
    assert r"\operatorname{Re}\{s\}<0&\quad\Longleftrightarrow\quad\left|z\right|<1" in html


def test_batch_eighteen_renders_all_mapping_formulas_with_mathjax(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_eighteen_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-eighteen.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
