from pathlib import Path


def test_batch_ten_preserves_2025_real_symmetry_dft_question_and_answer(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_ten_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-ten-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-ten-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 1
    assert "2025 年真题（第七题第 3 小题）" in training
    assert r"x(n)=x(N-1-n)" in training
    assert r"x(n)=-x(N-1-n)" in training
    assert r"X\left(\frac{N}{2}\right)=0" in answers
    assert r"X(0)=0" in answers
    assert r"(-1)^{N-1-n}=-(-1)^n" in answers
    assert "mod N" not in training + answers
