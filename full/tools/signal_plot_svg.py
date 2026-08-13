"""Data-driven SVG primitives for textbook-style signal figures."""
from __future__ import annotations

from html import escape
from pathlib import Path


def _map(value: float, lower: float, upper: float, start: float, end: float) -> float:
    return start + (value - lower) * (end - start) / (upper - lower)


def render_stem_svg(
    output: Path,
    *,
    samples: dict[int, float],
    x_label: str,
    y_label: str,
    title: str,
    x_limits: tuple[float, float],
    y_limits: tuple[float, float],
) -> Path:
    """Render a coordinate-driven discrete sequence as textbook-style SVG."""
    x_label = x_label.strip() or "n"
    y_label = y_label.strip() or "幅值"
    width, height = 720, 420
    left, right, top, bottom = 82, 670, 64, 348
    x_min, x_max = x_limits
    y_min, y_max = y_limits
    if not (x_min < x_max and y_min < y_max):
        raise ValueError("axis limits must have positive span")

    px = lambda value: _map(value, x_min, x_max, left, right)
    py = lambda value: _map(value, y_min, y_max, bottom, top)
    x_axis = py(0) if y_min <= 0 <= y_max else bottom
    y_axis = px(0) if x_min <= 0 <= x_max else left
    # The vertical axis is the n=0 axis.  Do not create a second, displaced
    # "zero axis" beside a sample at n=0: the stem and axis intentionally
    # share the same mathematical coordinate.
    plotted_y_axis = y_axis

    ticks = []
    for index in range(int(x_min), int(x_max) + 1):
        x = px(index)
        ticks.append(
            f'<line class="tick" x1="{x:.2f}" y1="{x_axis - 5:.2f}" x2="{x:.2f}" y2="{x_axis + 5:.2f}"/>'
            f'<text class="tick-label" x="{x:.2f}" y="{x_axis + 25:.2f}">{index}</text>'
        )

    stems = []
    for index, value in sorted(samples.items()):
        x, y = px(index), py(value)
        stems.append(
            f'<line class="stem-line" data-index="{index}" x1="{x:.2f}" y1="{x_axis:.2f}" x2="{x:.2f}" y2="{y:.2f}"/>'
            f'<circle class="sample-marker" data-index="{index}" cx="{x:.2f}" cy="{y:.2f}" r="4.6"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" style="max-width:720px;display:block" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<defs><marker id="axis-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#284B63"/></marker></defs>
<style>
.axis {{ stroke:#284B63; stroke-width:2; fill:none; }}
.tick {{ stroke:#284B63; stroke-width:1.4; }}
.tick-label {{ fill:#40515e; font-family:"Noto Serif CJK SC","Microsoft YaHei",serif; font-size:15px; text-anchor:middle; }}
.axis-label {{ fill:#1F2933; font-family:serif; font-size:20px; }}
.title {{ fill:#1E4F79; font-family:"Noto Serif CJK SC","Microsoft YaHei",serif; font-size:22px; text-anchor:middle; }}
.stem-line {{ stroke:#008F95; stroke-width:2.6; }}
.sample-marker {{ fill:#C46A00; stroke:#C46A00; }}
</style>
<text class="title" data-title-label-clearance="true" x="{width / 2:.2f}" y="34">{escape(title)}</text>
<line class="axis" data-axis="horizontal" x1="{left - 12}" y1="{x_axis:.2f}" x2="{right + 24}" y2="{x_axis:.2f}" marker-end="url(#axis-arrow)"/>
<line class="axis" data-axis="vertical" data-first-sample-clearance="false" x1="{plotted_y_axis:.2f}" y1="{bottom + 13}" x2="{plotted_y_axis:.2f}" y2="{top - 18}" marker-end="url(#axis-arrow)"/>
{''.join(ticks)}
{''.join(stems)}
<text class="axis-label" x="{right + 34}" y="{x_axis + 7:.2f}">{escape(x_label)}</text>
<text class="axis-label" x="{plotted_y_axis + 10:.2f}" y="{top + 24}">{escape(y_label)}</text>
</svg>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    return output
