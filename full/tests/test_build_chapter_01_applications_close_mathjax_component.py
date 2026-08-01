from pathlib import Path


def test_applications_close_uses_mathjax_and_data_driven_wheel_diagram(tmp_path: Path):
    from full.tools.build_chapter_01_applications_close_mathjax_component import write_html

    html = write_html(tmp_path / "applications-close.html").read_text(encoding="utf-8")

    assert "mathjax@3" in html
    assert r"\sin(100\pi t)" in html
    assert r"\sin(2100\pi t)" in html
    assert r"f_s\geq2f_h" in html
    assert "wagon_wheel_svg" in html
    assert 'class="apps-intro"' in html
    assert ".apps-intro{break-after:page}" in html
    assert "figure{break-inside:avoid;" in html
    assert "<svg" in html
    assert "drawImage" not in html
    assert "<image" not in html
