from pathlib import Path


def test_2017_eight_point_dit_fft_training_keeps_the_original_question_and_has_a_book_end_answer(tmp_path: Path):
    from full.tools import build_chapter_04_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-04-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-04-answers.html").read_text(encoding="utf-8")

    assert "2017 年真题" in question
    assert "5.画出 8 点按时间抽样的基-2FFT 算法的流程运动图。" in question
    assert "详解见 P.____" in question
    assert question.count('class="exam-page"') == 1
    assert 'data-diagram="dit-radix-2-eight-point-flow"' in answer
    assert "第 1 级" in answer
    assert "第 2 级" in answer
    assert "第 3 级" in answer
    assert r"\(N=8=2^3\)" in answer
    assert r"\(X_1(k)\)" in answer
    assert r"\(x(0),x(4),x(2),x(6),x(1),x(5),x(3),x(7)\)" in answer
    assert r"X(k)&=X_1(k)+W_8^kX_2(k)" in answer
    assert r"X\left(k+4\right)&=X_1(k)-W_8^kX_2(k)" in answer
