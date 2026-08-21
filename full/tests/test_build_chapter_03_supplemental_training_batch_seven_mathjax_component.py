from pathlib import Path


def test_batch_seven_preserves_2003_dft_spectrum_analysis_question_and_answer(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_seven_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-seven-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-seven-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 1
    assert "2003 年真题" in training
    assert "用 DFT 对模拟信号进行谱分析" in training
    assert r"200\,\mathrm{Hz}" in training
    assert r"f_s=400\,\mathrm{Hz}" in answers
    assert r"N=40" in answers
    assert r"\omega_k=\frac{2\pi k}{40}=\frac{k\pi}{20}" in answers
    assert r"(k-40)\times10\,\mathrm{Hz}" in answers
    assert "mod N" not in training + answers
