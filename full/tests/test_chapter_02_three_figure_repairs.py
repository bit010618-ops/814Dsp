"""Regression checks for the three chapter-two diagrams reported by the reader."""


def test_s_to_z_mapping_svg_is_self_styled_and_shows_periodic_identification():
    from full.tools.build_chapter_02_foundations_mathjax_component import z_plane_svg

    svg = z_plane_svg()

    # The assembled handout only retains component bodies, so this SVG may not
    # depend on the component-local stylesheet for axes, guide lines or circles.
    assert 'class="axis"' not in svg
    assert '<circle cx="704" cy="205" r="110" fill="none"' in svg
    assert 'z=e^{sT}' in svg
    assert '\\Omega+\\frac{2\\pi}{T}' in svg
    assert 'e^{j\\omega}' in svg


def test_zero_pole_svg_reserves_independent_label_positions():
    from full.tools.build_chapter_02_training_mathjax_component import _zero_pole_svg

    svg = _zero_pole_svg()

    assert '单位圆' in svg
    assert 'Im(z)' in svg
    assert 'Re(z)' in svg
    # The unit-circle note lives away from the vertical-axis arrow and the
    # origin, rather than sharing their immediate area.
    assert 'x="103" y="62"' in svg
    assert 'x="196" y="34"' in svg
    assert 'x="205" y="166"' in svg


def test_am_svg_has_safe_canvas_for_spectrum_and_coherent_demodulation():
    from full.tools.build_chapter_02_training_mathjax_component import _am_svg

    svg = _am_svg()

    assert 'viewBox="0 0 540 420"' in svg
    assert '(c) 相干解调与低通恢复' in svg
    assert 'y="318"' in svg
    assert 'y="356"' in svg
