from pathlib import Path


def test_selected_training_answers_use_one_mathjax_document(tmp_path: Path):
    from full.tools.build_chapter_01_training_answers_mathjax_component import write_html

    html = write_html(tmp_path / "answers.html").read_text(encoding="utf-8")
    assert "mathjax@3" in html
    assert "page-break-after:always" in html
    assert r"\frac{Y(z)}{X(z)}" in html
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
