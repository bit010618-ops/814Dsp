from pathlib import Path


def test_batch_twelve_preserves_2024_four_point_dft_question_and_even_part_answer(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_twelve_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-twelve-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-twelve-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 1
    assert "2024 年真题（第七题第 1 问）" in training
    assert r"x(n)=(-1)^n+1" in training
    assert r"0\leq n\leq3" in training
    assert r"X_{\mathrm{ep}}(k)" in training
    assert r"=2+2(-1)^k" in answers
    assert r"X(0)=4" in answers
    assert r"X(1)=0" in answers
    assert r"X(2)=4" in answers
    assert r"X(3)=0" in answers
    assert r"X^*\left((-k)\right)_4" in answers
    assert "mod N" not in training + answers
