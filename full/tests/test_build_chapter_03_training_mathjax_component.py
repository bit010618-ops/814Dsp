from pathlib import Path


def test_priority_2003_question_preserves_statement_and_detailed_solution(tmp_path: Path):
    from full.tools import build_chapter_03_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-03-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-03-answers.html").read_text(encoding="utf-8")

    assert "2003 年真题" in question
    assert "最高频率为 200 Hz" in question
    assert "以 Nyquist 频率采样" in question
    assert "频率分辨率为 10 Hz" in question
    assert r"x(n)=x_a(nT)" in question
    assert r"f_s=2\times200=400\,\mathrm{Hz}" in answer
    assert r"N=\frac{f_s}{F_0}=40" in answer
    assert r"\omega_k=\frac{2\pi k}{N}=\frac{2\pi k}{40}=\frac{\pi k}{20}" in answer
    assert r"f_k=kF_0=10k\,\mathrm{Hz}" in answer
