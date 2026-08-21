from pathlib import Path


def test_batch_eleven_preserves_2007_target_frequency_dft_question_and_answer(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_eleven_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-eleven-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-eleven-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 1
    assert "2007 年真题（第十三题第 1 问）" in training
    assert r"8192\,\mathrm{Hz}" in training
    assert r"800\,\mathrm{Hz}" in training
    assert r"N=512" in answers
    assert r"\Delta f=\frac{8192}{512}=16\,\mathrm{Hz}" in answers
    assert r"k_0=\frac{800}{16}=50" in answers
