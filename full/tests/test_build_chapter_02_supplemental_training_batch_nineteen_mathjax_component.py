from pathlib import Path


def test_batch_nineteen_preserves_the_two_2020_fill_in_prompts(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_nineteen_mathjax_component as component

    html = component.write_html(tmp_path / "batch-nineteen.html").read_text(encoding="utf-8")

    assert "2020 年真题（填空题第 2、3 小题）" in html
    assert "序列实部的傅里叶变换等于傅里叶变换的" in html
    assert "一个线性时不变离散系统稳定的充要条件是系统函数的收敛域包含" in html
    assert r"\frac{1}{2}\left[X\!\left(e^{j\omega}\right)+X^*\!\left(e^{-j\omega}\right)\right]" in html
    assert r"\left|z\right|=1" in html


def test_batch_nineteen_renders_fill_in_answers_with_mathjax(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_nineteen_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-nineteen.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
    assert "右端正是 (X" not in dom
