from pathlib import Path


def test_batch_eight_preserves_2025_dft_and_conjugate_components_question_and_answer(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_eight_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-eight-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-eight-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 1
    assert "2025 年真题（第七题第 1 小题）" in training
    assert r"x(n)=4\delta(n)+\delta(n-1)+\delta(n-2)+\delta(n-3)" in training
    assert r"X_{\mathrm{ep}}(k)" in training
    assert r"X(0)=7" in answers
    assert r"X(1)=X(2)=X(3)=3" in answers
    assert r"X^*\left((-k)\right)_4" in answers
    assert r"X_{\mathrm{op}}(k)=0" in answers
    assert "mod N" not in training + answers
