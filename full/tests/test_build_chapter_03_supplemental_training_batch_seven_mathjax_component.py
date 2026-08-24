from pathlib import Path


def test_batch_seven_preserves_2007_circular_convolution_range_question_and_answer(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_seven_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-seven-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-seven-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 1
    assert "2007 年真题（填空题第 4 小题）" in training
    assert r"x(n)=R_{100}(n)" in training
    assert r"h(n)=R_{10}(n)" in training
    assert r"\mathbin{\circledast}_{80}" in training
    assert r"29\le n\le79" in answers
    assert r"y_{80}[n]=y_{\mathrm{lin}}[n]+y_{\mathrm{lin}}[n+80]" in answers
    assert 'class="formula-name">循环卷积的周期折回关系（用于判断折回叠加）' in answers
    assert 'class="formula-name">未折回区间判据（用于确定与线性卷积一致的样点）' in answers
    assert "mod N" not in training + answers
