from pathlib import Path


def test_second_supplemental_batch_preserves_prompts_and_uses_mathjax(tmp_path: Path):
    from full.tools.build_chapter_02_supplemental_training_batch_two_mathjax_component import (
        answers_html,
        training_html,
        write_html,
    )

    training = training_html()
    answers = answers_html()
    html = write_html(tmp_path / "chapter-two-supplemental-batch-two.html").read_text(
        encoding="utf-8"
    )

    assert training.count('class="exam-page"') == 3
    assert "2004 年真题" in training
    assert "已知某离散系统方框图如下：求" in training
    assert "（1）该系统的系统函数" in training
    assert "（4）求系统稳定时的冲激响应。" in training
    assert "2005 年真题" in training
    assert r"F(z)=\frac{z^2}{z^2-2z-3}" in training
    assert r"1<|z|<3" in training
    assert "以除去 5kHz&lt;F&lt;10kHz 的频率成分" in training
    assert "最大频率是20kHz" in training
    assert r"\begin{cases}" in answers
    assert r"\frac{Y(z)}{X(z)}" in answers
    assert "水印" not in html
    assert "源课件" not in html
    assert "page-break-after:always" not in html


def test_second_supplemental_batch_has_no_raw_tex_after_browser_typesetting(tmp_path: Path):
    from full.tools.build_chapter_02_supplemental_training_batch_two_mathjax_component import (
        rendered_dom,
        write_html,
    )

    dom = rendered_dom(write_html(tmp_path / "chapter-two-supplemental-batch-two.html"))
    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom


def test_batch_two_svg_elements_define_their_own_vector_paint_attributes():
    """PDF export must not depend on page-level CSS cascading into SVG."""
    from full.tools.build_chapter_02_supplemental_training_batch_two_mathjax_component import (
        bandstop_svg,
        system_svg,
    )

    system = system_svg()
    spectrum = bandstop_svg()

    assert '<circle fill="white" stroke="#174b73"' in system
    assert '<rect fill="#f4f7f8" stroke="#0f8b8d"' in system
    assert 'fill="none" stroke="#174b73" stroke-width="2"' in system
    assert 'fill="none" stroke="#0f8b8d" stroke-width="2"' in system
    assert 'fill="none" stroke="#174b73" stroke-width="2"' in spectrum
    assert '<rect fill="#fbf2e8" stroke="#b56b2e"' in spectrum


def test_2004_detailed_answer_includes_a_vector_zero_pole_and_stable_roc_figure():
    from full.tools.build_chapter_02_supplemental_training_batch_two_mathjax_component import (
        answers_html,
        stable_roc_svg,
    )

    svg = stable_roc_svg()
    assert "稳定收敛域零极点图" in svg
    assert 'fill="white" stroke="#0f8b8d"' in svg
    assert 'fill="#e8f3f2"' in svg
    assert 'stroke="#b56b2e"' in svg
    assert "零点、极点和稳定收敛域如图所示" in answers_html()
