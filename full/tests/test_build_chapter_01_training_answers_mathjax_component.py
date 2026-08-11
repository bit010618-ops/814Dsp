from pathlib import Path

import pytest


def test_selected_training_answers_use_one_mathjax_document(tmp_path: Path):
    from full.tools.build_chapter_01_training_answers_mathjax_component import write_html

    html = write_html(tmp_path / "answers.html").read_text(encoding="utf-8")
    assert "mathjax@3" in html
    assert "page-break-after:always" in html
    assert r"\frac{Y(z)}{X(z)}" in html
    assert r"\frac{0.35+0.175z^{-1}-0.03z^{-2}}{1-0.4z^{-2}}" in html
    assert r"y[n]-0.4y[n-2]" in html
    assert r"\frac{\sqrt{10}}{5}" in html
    assert r"(f_1*f_2)(n)" in html
    # All 2019 explanatory formulas must retain their inline MathJax
    # delimiters; a previous escaping error leaked literal source notation.
    for formula in (
        r"\(f_1(n)=1\)",
        r"\(-2\leq n\leq2\)",
        r"\(f_2(-1)=1,f_2(0)=2,f_2(1)=-1,f_2(2)=2,f_2(3)=-1\)",
        r"\((f_1*f_2)(n)\)",
        r"\(5+5-1=9\)",
    ):
        assert formula in html
    assert "drawImage" not in html
    assert "<image" not in html


def test_2019_answer_has_no_unprocessed_tex_after_browser_typesetting(tmp_path: Path):
    """A formula is not accepted until MathJax has replaced its source tokens."""
    from full.tools.build_chapter_01_training_answers_mathjax_component import (
        rendered_dom,
        write_html,
    )

    dom = rendered_dom(write_html(tmp_path / "answers.html"))
    assert '<mjx-container' in dom
    section = dom[dom.index('2019 年真题：图形卷积'):]
    assert r"\(f_1(n)=1\)" not in section
    assert r"\(-2\leq n\leq2\)" not in section
    assert r"\((f_1*f_2)(n)\)" not in section


def test_answer_document_rejects_any_raw_mathjax_delimiter_after_typesetting(
    tmp_path: Path,
):
    """One sampled formula is insufficient: every answer fragment must render."""
    from full.tools.build_chapter_01_training_answers_mathjax_component import (
        assert_mathjax_ready,
        rendered_dom,
        write_html,
    )

    dom = rendered_dom(write_html(tmp_path / "answers.html"))
    assert_mathjax_ready(dom)


def test_answer_document_rejects_literal_formula_that_browser_left_unprocessed():
    from full.tools.build_chapter_01_training_answers_mathjax_component import (
        assert_mathjax_ready,
    )

    with pytest.raises(RuntimeError, match="unprocessed formula delimiters"):
        assert_mathjax_ready("<mjx-container></mjx-container><p>\\(f_1(n)\\)</p>")
