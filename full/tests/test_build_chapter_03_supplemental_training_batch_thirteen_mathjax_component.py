from pathlib import Path


def test_batch_thirteen_preserves_2021_whole_dft_question_and_derivations(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_thirteen_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-thirteen-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-thirteen-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 1
    assert "2021 年真题（第七题）" in training
    assert r"x(n)=(n+1)R_6(n)" in training
    assert r"h(n)=\{1,1,1,1\}" in training
    assert r"x(n)=a^nR_8(n)" in training
    assert "什么是频谱泄露，怎么抑制？" in training
    assert r"21,&k=0" in answers
    assert r"-\frac{6}{1-W_6^k}" in answers
    assert r"L=10" in answers
    assert r"\{1,3,6,10,14,18,15,11,6\}" in answers
    assert r"\widetilde{x}(n)=\sum_{r=-\infty}^{\infty}x(n-6r)" in answers
    assert r"\{1+a^6,\ a+a^7,\ a^2,\ a^3,\ a^4,\ a^5\}" in answers
    assert "窗函数" in answers
    assert "mod N" not in training + answers
