def test_chapter_one_batch_three_preserves_the_2025_pulse_sampling_question_and_solution():
    from full.tools import (
        build_chapter_01_supplemental_training_batch_three_mathjax_component as batch,
    )

    question = batch.training_html()
    answer = batch.answers_html()

    assert "2025 年真题" in question
    assert r"T_s=10^{-2}\,\mathrm{s}" in question
    assert r"\tau\ll T_s" in question
    assert "是否满足采样定理" in question
    assert 'data-plot="2025-bipolar-square-wave"' in question
    assert '<foreignObject x="438" y="183" width="32" height="28"><div xmlns="http://www.w3.org/1999/xhtml">\\(0\\)</div></foreignObject>' in question
    assert r"\omega_s=\frac{2\pi}{T_s}=200\pi\,\mathrm{rad}\,\mathrm{s}^{-1}" in answer
    assert r"S(\omega)=2\pi\frac{\tau}{T_s}" in answer
    assert r"X_s(\omega)=\frac{\tau}{T_s}" in answer
    assert r"X_{s,\delta}(\omega)=\frac{1}{T_s}" in answer
    assert 'data-plot="2025-pulse-sampling-spectrum"' in answer
    assert r"\operatorname{Sa}" not in batch._pulse_sampling_spectrum_svg()


def test_chapter_one_batch_three_is_assembled_in_the_full_handout(tmp_path):
    from full.tools.build_full_handout import write_html

    html = write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    assert "2025 年真题：周期脉冲采样与频谱对比" in html
    assert 'data-plot="2025-bipolar-square-wave"' in html
