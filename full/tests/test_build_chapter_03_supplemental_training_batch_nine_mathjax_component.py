from pathlib import Path


def test_batch_nine_preserves_2025_dtft_sampling_and_idft_question_and_answer(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_nine_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-nine-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-nine-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 1
    assert "2025 年真题（第七题第 2 小题）" in training
    assert r"x(n)=\left(\frac{1}{2}\right)^n u(n)" in training
    assert r"\omega=\frac{\pi}{2}k" in training
    assert r"y(n)=\sum_{r=-\infty}^{\infty}x(n-4r)" in answers
    assert r"\frac{16}{15}\left(\frac{1}{2}\right)^n" in answers
    assert r"y(0)=\frac{16}{15}" in answers
    assert "mod N" not in training + answers
