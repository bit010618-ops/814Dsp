from pathlib import Path


def test_batch_four_preserves_three_verified_dft_questions_and_answers(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_four_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-four-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-four-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 3
    assert "2020 年真题（第三题）" in training
    assert r"Y(k)=X(3k)" in training
    assert "2020 年真题（第五题）" in training
    assert r"Y(k)=W_6^{4k}X(k)" in training
    assert "2023 年真题（DSP 第 3 小题）" in training
    assert r"x(n)=nR_6(n)" in training
    assert r"Y(k)=X(k)\cos\left(\frac{2\pi}{5}k\right)" in training
    assert r"y(0)=4+3+2=9" in answers
    assert r"y(1)=7+1=8" in answers
    assert r"y(n)=x\left((n-4)\right)_6" in answers
    assert r"(x\circledast_6x)(n)=\left\{17,24,25,20,10,4\right\}" in answers
    assert r"y(n)=\frac{1}{2}\left[x\left((n-2)\right)_{10}+x\left((n+2)\right)_{10}\right]" in answers
    assert r"\left\{1,\frac{3}{2},2,3,1,\frac{3}{2},2,\frac{5}{2},0,\frac{1}{2}\right\}" in answers
    assert "mod N" not in training + answers
