from pathlib import Path


def test_chapter_two_first_supplemental_batch_preserves_prompts_and_mathjax(tmp_path: Path):
    from full.tools.build_chapter_02_supplemental_training_mathjax_component import write_html

    html = write_html(tmp_path / "chapter-two-supplemental-training.html").read_text(encoding="utf-8")
    for label in (
        "2002 年真题",
        "2003 年真题",
        "2004 年真题：梳状滤波器",
        "2004 年真题：频率响应",
        "2005 年真题",
        "2006 年真题",
        "2007 年真题",
    ):
        assert label in html
    assert "H(z)=\\frac{1}{(z-a)(z-b)}" in html
    assert "F(z)=\\frac{2z^2}{\\left(z-\\frac12\\right)^2(z-1)}" in html
    assert "h(n)=\\delta(n)-\\frac{\\sin(n\\pi/3)}{n\\pi}" in html
    assert "\\[" in html and "\\(" in html
    assert "水印" not in html
    assert "详解页码待全书合成后回填" not in html
    assert html.count("详解见 P.____") == 7
    assert "page-break-after:always" not in html


def test_supplemental_exam_formulas_are_typeset_by_the_browser(tmp_path: Path):
    from full.tools.build_chapter_02_supplemental_training_mathjax_component import (
        rendered_dom,
        write_html,
    )

    dom = rendered_dom(write_html(tmp_path / "chapter-two-supplemental-training.html"))
    assert "<mjx-container" in dom
    question_section = dom[dom.index("2003 年真题"):dom.index("2004 年真题：梳状滤波器")]
    assert r"\(H(z)\)" not in question_section
    assert r"\(a\)" not in question_section
    assert r"\(b\)" not in question_section
