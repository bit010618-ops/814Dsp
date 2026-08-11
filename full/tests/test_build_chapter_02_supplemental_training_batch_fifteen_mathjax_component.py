from pathlib import Path


def test_batch_fifteen_preserves_and_solves_2025_question_seven_part_four(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_fifteen_mathjax_component as component

    html = component.write_html(tmp_path / "batch-fifteen.html").read_text(encoding="utf-8")

    assert "2025 年真题" in html
    assert "利用如下框图处理连续时间信号" in html
    assert r"T=1\,\mathrm{ms}" in html
    assert r"(-1)^n" in html
    assert r"\left|\omega\right|\leq0.6\pi" in html
    assert r"0.5\pi\leq\left|\omega\right|\leq\pi" in html
    assert r"500\pi\leq\left|\Omega\right|\leq1000\pi" in html


def test_batch_fifteen_mathjax_renders_every_formula_as_a_single_structure(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_fifteen_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-fifteen.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom


def test_batch_fifteen_is_included_in_the_reusable_chapter_two_collection():
    from full.tools import build_chapter_02_mathjax_handout as handout
    from full.tools import build_chapter_02_supplemental_training_batch_fifteen_mathjax_component as component

    assert component in handout.COMPONENTS
