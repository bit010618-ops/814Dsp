from pathlib import Path


def test_batch_three_preserves_five_verified_dft_questions_and_answers(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_three_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-three-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-three-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 5
    assert "2017 年真题（第六题第 1 小题）" in training
    assert r"Y(k)=W_{10}^{2k}X(k)" in training
    assert r"M(k)=X(k)Y(k)" in training
    assert "2017 年真题（第六题第 2 小题）" in training
    assert r"x(n)=\left\{1,2,3\right\}" in training
    assert r"h(n)=\left\{1,0,1,-1,0\right\}" in training
    assert "2017 年真题（第六题第 3 小题）" in training
    assert r"F_0\leq10\,\mathrm{Hz}" in training
    assert r"T=0.1\,\mathrm{ms}" in training
    assert "2019 年真题（第三题）" in training
    assert "简述栅栏效应的原因及解决方法。" in training
    assert "2020 年真题（简答题第 1 小题）" in training
    assert "什么是栅栏效应？" in training
    assert r"y(n)=x\left((n-2)\right)_{10}" in answers
    assert r"m(n)=5\delta(n-2)+4\delta(n-7)" in answers
    assert r"\left\{-2,2,4,1,1\right\}" in answers
    assert r"N=1024" in answers
    assert r"F_0=\frac{1}{NT}=9.765625\,\mathrm{Hz}" in answers
    assert "mod N" not in training + answers
