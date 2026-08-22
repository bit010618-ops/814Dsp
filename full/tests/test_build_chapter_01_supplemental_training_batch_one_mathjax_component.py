def test_chapter_one_batch_one_preserves_the_2016_sampling_question_and_solution():
    from full.tools import (
        build_chapter_01_supplemental_training_batch_one_mathjax_component as batch,
    )

    question = batch.training_html()
    answer = batch.answers_html()

    assert "2016 年真题" in question
    assert r"f(t)=\operatorname{Sa}(2t)" in question
    assert r"\delta_T(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT)" in question
    assert r"\omega_s=6\omega_m" in question
    assert "麦奎斯特频率" in question
    assert "奈奎斯特频率" in answer
    assert r"\omega_m=2\,\mathrm{rad}\,\mathrm{s}^{-1}" in answer
    assert r"F_s(\omega)=\frac{1}{T}\sum_{k=-\infty}^{\infty}F(\omega-k\omega_s)" in answer


def test_chapter_one_batch_one_is_assembled_in_the_full_handout(tmp_path):
    from full.tools.build_full_handout import write_html

    html = write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    assert "2016 年真题：冲激采样与频谱复制" in html
    assert r"f(t)=\operatorname{Sa}(2t)" in html
    assert 'data-plot="2016-impulse-sampling-time"' in html
    assert 'data-plot="2016-impulse-sampling-spectrum"' in html
