import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


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


def test_supplemental_training_excludes_continuous_time_out_of_scope_questions(tmp_path: Path):
    from full.tools.build_chapter_01_supplemental_mathjax_component import write_answers_html, write_questions_html

    questions = write_questions_html(tmp_path / "supplemental.html").read_text(encoding="utf-8")
    answers = write_answers_html(tmp_path / "supplemental-answers.html").read_text(encoding="utf-8")

    for out_of_scope_prompt in (
        r"已知 \(f(t)=u(t)-u(t-2)\)，求 \(f(t)*f(t)\)的表达式及波形。",
        r"信号 \(y(t)=x(3t)\)是否线性，是否时变，为什么？",
        r"x(t)=2\delta(t-1)-3\delta(t-2)-2\delta(t-5)",
    ):
        assert out_of_scope_prompt not in questions
    assert "self_convolution_waveform_svg" not in answers
    assert r"2u(-1-t)-3u(-t)-2u(3-t)" not in answers


def test_supplemental_training_preserves_the_2005_second_order_difference_equation_prompt_and_solution(tmp_path: Path):
    from full.tools.build_chapter_01_supplemental_mathjax_component import write_answers_html, write_questions_html

    questions = write_questions_html(tmp_path / "supplemental.html").read_text(encoding="utf-8")
    answers = write_answers_html(tmp_path / "supplemental-answers.html").read_text(encoding="utf-8")

    assert r"某离散系统可由二阶常系数线性差分方程描述" in questions
    assert r"y(n)=[2^n+3(5)^n+10]u(n)" in questions
    assert r"f(n)=3u(n)+3u(n-7)" in questions
    assert r"&=\frac{14-85z^{-1}+111z^{-2}}{1-7z^{-1}+10z^{-2}}" in answers
    assert r"y[n]-7y[n-1]+10y[n-2]" in answers
    assert r"3s[n]+3s[n-7]" in answers


def test_supplemental_training_does_not_repeat_2006_priority_structure_question(tmp_path: Path):
    from full.tools.build_chapter_01_supplemental_mathjax_component import write_answers_html, write_questions_html

    questions = write_questions_html(tmp_path / "supplemental.html").read_text(encoding="utf-8")
    answers = write_answers_html(tmp_path / "supplemental-answers.html").read_text(encoding="utf-8")

    assert "2006 年真题" not in questions
    assert "2006 年真题：离散系统结构分析" not in answers


def test_supplemental_source_model_keeps_only_audited_chapter_one_question_ids():
    model = json.loads(
        (ROOT / "full" / "source" / "chapter_01_supplemental_component.json").read_text(
            encoding="utf-8"
        )
    )
    ids = {item["id"] for item in model["questions"]}

    assert "2005-q七-whole" in ids
    assert "2004-qintro-01" not in ids
    assert "2005-q二-01" not in ids
