import re
from pathlib import Path

from full.tools.signal_plot_svg import render_stem_svg


def test_stem_svg_uses_real_data_coordinates_and_textbook_axes(tmp_path: Path):
    output = tmp_path / "impulse.svg"

    result = render_stem_svg(
        output,
        samples={0: 1.0, 2: -0.5},
        x_label=r"n",
        y_label=r"\delta(n)",
        title="单位抽样序列",
        x_limits=(-2, 4),
        y_limits=(-1, 2),
    )

    svg = result.read_text(encoding="utf-8")
    assert result == output
    assert "<svg" in svg
    assert 'viewBox="' in svg
    assert 'height="auto"' not in svg
    assert "单位抽样序列" in svg
    assert "marker-end" in svg
    assert "stem-line" in svg
    assert "sample-marker" in svg
    assert "data-index=\"0\"" in svg
    assert "data-index=\"2\"" in svg
    assert "<image" not in svg


def test_stem_svg_keeps_the_vertical_axis_clear_of_the_zero_sample(tmp_path: Path):
    output = tmp_path / "zero-first.svg"

    render_stem_svg(
        output,
        samples={0: 1.0},
        x_label="n",
        y_label="x[n]",
        title="离散序列",
        x_limits=(-1, 3),
        y_limits=(-0.5, 1.5),
    )

    svg = output.read_text(encoding="utf-8")
    assert 'data-index="0"' in svg
    assert 'data-axis="vertical"' in svg
    assert 'data-first-sample-clearance="true"' in svg
    axis_match = re.search(r'<line class="axis" data-axis="vertical"[^>]*x1="([0-9.]+)"', svg)
    stem_match = re.search(r'<line class="stem-line" data-index="0" x1="([0-9.]+)"', svg)
    assert axis_match is not None
    assert stem_match is not None
    assert float(axis_match.group(1)) < float(stem_match.group(1))


def test_stem_svg_reserves_a_distinct_safe_zone_for_title_and_vertical_label(tmp_path: Path):
    output = tmp_path / "title-clearance.svg"

    render_stem_svg(
        output,
        samples={0: 1.0},
        x_label="n",
        y_label="x[n]",
        title="单位抽样序列",
        x_limits=(-1, 3),
        y_limits=(-0.5, 1.5),
    )

    svg = output.read_text(encoding="utf-8")
    assert 'data-title-label-clearance="true"' in svg


def test_stem_svg_scales_to_a_narrow_container_without_clipping(tmp_path: Path):
    output = tmp_path / "responsive.svg"

    render_stem_svg(
        output,
        samples={0: 1.0, 2: -0.5},
        x_label="n",
        y_label="x[n]",
        title="离散序列",
        x_limits=(-2, 4),
        y_limits=(-1, 2),
    )

    svg = output.read_text(encoding="utf-8")
    assert 'width="100%"' in svg
    assert 'max-width:720px' in svg


def test_stem_svg_supplies_standard_axis_labels_when_callers_leave_them_blank(tmp_path: Path):
    output = tmp_path / "default-labels.svg"

    render_stem_svg(
        output,
        samples={0: 1.0},
        x_label="",
        y_label="",
        title="单位抽样序列",
        x_limits=(-1, 3),
        y_limits=(-0.5, 1.5),
    )

    svg = output.read_text(encoding="utf-8")
    assert 'class="axis-label"' in svg
    assert ">n</text>" in svg
    assert ">幅值</text>" in svg
    assert not re.search(r'<text class="axis-label"[^>]*>\s*</text>', svg)
