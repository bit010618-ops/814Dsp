"""Regression checks for the one-origin coordinate-axis contract."""


def test_2019_sampling_uses_the_vertical_axis_as_the_only_zero_index_position():
    from full.tools.build_chapter_01_supplemental_mathjax_component import sampling_2019_svg

    output = sampling_2019_svg("time")

    assert 'd="M435.0 406V230"' in output
    assert 'd="M425.0 406V230"' not in output
    assert output.count('>\\(0\\)</div>') == 1
    assert '<polyline fill="none" stroke="#008f95" stroke-width="3"' in output
    assert output.count('fill="none" stroke="#174b73" stroke-width="2"') == 4
    assert 'fill="none" stroke="#b45309" stroke-width="2"' in output


def test_2019_sampling_spectrum_keeps_coordinate_axes_visible_without_outer_css():
    from full.tools.build_chapter_01_supplemental_mathjax_component import sampling_2019_svg

    output = sampling_2019_svg("spectrum")

    assert output.count('fill="none" stroke="#174b73" stroke-width="2"') == 2
    assert 'data-origin-at-zero="true"' in output


def test_chapter_one_convolution_stems_inline_their_axis_and_sample_paint():
    from full.tools.build_chapter_01_supplemental_mathjax_component import (
        convolution_2016_svg,
        convolution_2021_svg,
    )

    for output in (
        convolution_2016_svg("inputs"),
        convolution_2016_svg("output"),
        convolution_2021_svg("inputs"),
        convolution_2021_svg("output"),
    ):
        assert 'fill="none" stroke="#174b73" stroke-width="2"' in output
        assert 'fill="none" stroke="#b45309" stroke-width="2"' in output


def test_2019_training_stems_keep_axes_and_samples_in_static_pdf_exports():
    from full.tools.build_chapter_01_training_mathjax_component import training_stem_svg

    output = training_stem_svg({-1: 1, 0: 2, 1: -1}, "f_2(n)")

    assert output.count('fill="none" stroke="#174b73" stroke-width="2"') == 2
    assert 'fill="none" stroke="#b45309" stroke-width="2"' in output
    assert 'data-origin-label="true"' in output
