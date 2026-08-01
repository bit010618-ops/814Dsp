from pathlib import Path


def test_supplemental_questions_and_answers_use_mathjax(tmp_path: Path):
    from full.tools.build_chapter_01_supplemental_mathjax_component import write_answers_html, write_questions_html

    questions = write_questions_html(tmp_path / "supplemental.html").read_text(encoding="utf-8")
    answers = write_answers_html(tmp_path / "supplemental-answers.html").read_text(encoding="utf-8")

    for html in (questions, answers):
        assert "mathjax@3" in html
        assert "page-break-after:always" in html
        assert "drawImage" not in html
        assert "<image" not in html
    assert r"r(n)-6r(n-1)+8r(n-2)" in questions
    assert r"f_1&lt;f_2" in questions
    assert r"f_0(mT)=f(mT)" in answers
    assert "supplemental_spectrum_svg" in answers
