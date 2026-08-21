from pathlib import Path


def test_batch_five_preserves_2023_overlap_save_question_and_answer(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_five_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-five-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-five-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 1
    assert "2023 年真题（DSP 第 4 小题）" in training
    assert "对 80 点长序列" in training
    assert "重叠保留法计算线性卷积" in training
    assert "每段长度为 5" in training
    assert r"N=5" in answers
    assert r"M=N-(L_h-1)=5-2=3" in answers
    assert r"L_x+L_h-1=80+3-1=82" in answers
    assert r"B=\left\lceil\frac{L_x+L_h-1}{M}\right\rceil" in answers
    assert r"\left\{0,0,x(0),x(1),x(2)\right\}" in answers
    assert r"\left\{x(77),x(78),x(79),0,0\right\}" in answers
    assert "mod N" not in training + answers
