from pathlib import Path


def test_batch_two_preserves_eight_verified_dfs_dft_questions_and_answers(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_two_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-two-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-two-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 8
    assert "2013 年真题（填空题第 5 小题）" in training
    assert r"N=4" in training
    assert r"a_2=3" in training
    assert r"a_7=5" in training
    assert "2014 年真题（填空题第 7 小题）" in training
    assert r"N=6" in training
    assert r"a_{14}=2" in training
    assert r"\sum_{n=0}^{5}x(n)(-1)^n=1" in training
    assert "2015 年真题（填空题第 3 小题）" in training
    assert "2015 年真题（填空题第 4 小题）" in training
    assert "2016 年真题（DSP 第 3 小题）" in training
    assert r"Y(k)=X(2k)" in training
    assert "2016 年真题（DSP 第 4 小题）" in training
    assert r"x(n)=2+2\cos\left(\frac{2\pi n}{N}\right)" in training
    assert "2016 年真题（DSP 第 5 小题）" in training
    assert "2016 年真题（第八题）" in training
    assert r"a_{-3}=a_3=\frac{1}{6}" in answers
    assert r"a_{-2}=a_2=2" in answers
    assert r"L\geq4+5-1=8" in answers
    assert r"y(n)=x(n)+x(n+3)" in answers
    assert r"X(0)=2N" in answers
    assert r"X_1(k)=\frac{1}{2}\left[X(k)+X^*\left((N-k)\right)_N\right]" in answers
    assert "mod N" not in training + answers
