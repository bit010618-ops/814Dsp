from pathlib import Path


def test_2020_iir_structure_question_is_kept_with_a_book_end_answer(tmp_path: Path):
    from full.tools import build_chapter_05_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-05-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-05-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') == 1
    assert "2020 年真题" in question
    assert "2.IIR 滤波器的级联型和并联型结构特点；" in question
    assert "详解见 P.____" in question
    assert "因式分解" in answer
    assert "部分分式展开" in answer
    assert r"H(z)=\prod_{r=1}^{R}H_r(z)" in answer
    assert r"H(z)=\sum_{r=1}^{R}H_r(z)" in answer
