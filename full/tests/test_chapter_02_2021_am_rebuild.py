"""Regression checks for the 2021 AM-modulation question rebuild."""


def test_2021_am_question_uses_three_clean_source_figures_and_a_real_output_spectrum():
    from full.tools import build_chapter_02_training_mathjax_component as component

    source_figure = component._am_svg()
    output_spectrum = component._am_output_spectrum_svg()

    assert 'data-role="am-modulator"' in source_figure
    assert 'data-role="input-periodic-spectrum"' in source_figure
    assert 'data-role="coherent-demodulator"' in source_figure
    assert "foreignObject" in source_figure
    assert r"\cos(\omega_cn)" in source_figure
    assert r"X(e^{j\omega})" in source_figure
    assert r"\hat{x}(n)" in source_figure
    assert 'M260 356L340 276L420 356' in source_figure
    assert 'M260 356L300 276L340 356' not in source_figure
    assert 'data-role="am-output-spectrum"' in output_spectrum
    assert 'data-role="shifted-copy-minus"' in output_spectrum
    assert 'data-role="shifted-copy-plus"' in output_spectrum
    assert r"\frac12" in output_spectrum
    assert r"\omega_c-\omega_0" in output_spectrum


def test_2021_am_question_keeps_all_formulae_in_mathjax_after_typesetting(tmp_path):
    from full.tools import build_chapter_02_training_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-two-training.html")
    dom = component.rendered_dom(html)

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
