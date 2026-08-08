from pathlib import Path


def test_third_supplemental_batch_preserves_the_verified_2013_prompts_and_math():
    from full.tools.build_chapter_02_supplemental_training_batch_three_mathjax_component import (
        answers_html,
        training_html,
    )

    training = training_html()
    answers = answers_html()

    assert training.count('class="exam-page"') == 2
    assert "五、离散系统的单位脉冲响应" in training
    assert "2013 年真题：理想滤波器幅频响应" in training
    assert "画出理想低通、高通、带通、带阻频率滤波器的幅频响应，要求标出截止频率。" in training
    assert "2015 年真题" in training
    assert r"h(n)=\delta(n)-0.98\delta(n-6)" in training
    assert "画出零极点图和该系统的幅频特性。" in training
    assert r"\left|H_{\mathrm{LP}}(e^{j\omega})\right|" in answers
    assert r"\left|H_{\mathrm{BS}}(e^{j\omega})\right|" in answers
    assert r"H(z)=1-0.98z^{-6}" in answers
    assert r"0.98^{1/6}" in answers
    assert r"\sqrt{1+0.98^2-1.96\cos(6\omega)}" in answers


def test_third_batch_uses_explicit_vector_drawing_and_mathjax_dom(tmp_path: Path):
    from full.tools.build_chapter_02_supplemental_training_batch_three_mathjax_component import (
        ideal_filter_grid_svg,
        rendered_dom,
        write_html,
        zero_pole_svg,
    )

    filters = ideal_filter_grid_svg()
    zeros = zero_pole_svg()
    assert 'fill="none" stroke="#174b73"' in filters
    assert 'fill="none" stroke="#0f8b8d"' in filters
    assert 'fill="white" stroke="#0f8b8d"' in zeros
    assert 'stroke-dasharray="5 4"' in zeros

    dom = rendered_dom(write_html(tmp_path / "chapter-two-supplemental-batch-three.html"))
    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
