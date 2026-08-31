"""Regression coverage for textbook-style vertical-axis direction."""


def test_continuous_discrete_mapping_vertical_axes_point_upward():
    from full.tools.build_chapter_01_body_only import _continuous_discrete_mapping_svg

    svg = _continuous_discrete_mapping_svg()

    assert 'd="M132 117V36" marker-end="url(#mapping-arrow)"' in svg
    assert 'd="M132 249V166" marker-end="url(#mapping-arrow)"' in svg
