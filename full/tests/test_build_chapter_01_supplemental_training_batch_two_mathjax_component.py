def test_chapter_one_batch_two_preserves_the_2007_sampling_question_and_solution():
    from full.tools import (
        build_chapter_01_supplemental_training_batch_two_mathjax_component as batch,
    )

    question = batch.training_html()
    answer = batch.answers_html()

    assert "2007 年真题" in question
    assert r"\dfrac{\sin^2\!\left(\pi\times10^3t\right)}{\left(\pi\times10^3t\right)^2}" in question
    assert r"T=0.5\times10^{-3}\,\mathrm{s}" in question
    assert r"\sum_{k=-\infty}^{\infty}\delta(t-kT)" in question
    assert 'data-diagram="2007-sampling-system"' in question
    assert r"X_p(\omega)=\frac{1}{T}\sum_{k=-\infty}^{\infty}X(\omega-k\omega_s)" in answer
    assert r"X\!\left(e^{j\Omega}\right)=2\left(1-\frac{|\Omega|}{\pi}\right)" in answer
    assert r"\int_{-\infty}^{\infty}x(t)\,\mathrm{d}t=X(0)=10^{-3}" in answer
    assert r"\sum_{n=-\infty}^{\infty}x(n)=X\!\left(e^{j0}\right)=2" in answer
    assert 'data-plot="2007-sampling-frequency-relations"' in answer


def test_chapter_one_batch_two_is_assembled_in_the_full_handout(tmp_path):
    from full.tools.build_full_handout import write_html

    html = write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    assert "2007 年真题：模拟采样与离散序列频谱" in html
    assert 'data-diagram="2007-sampling-system"' in html
