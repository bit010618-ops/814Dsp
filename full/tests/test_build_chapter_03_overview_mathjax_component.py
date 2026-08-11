from pathlib import Path


def test_overview_component_uses_mathjax_for_frequency_bridge_formulae(tmp_path: Path):
    from full.tools import build_chapter_03_overview_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-overview.html").read_text(
        encoding="utf-8"
    )

    assert "四类傅里叶描述的坐标关系" in html
    assert r"\(\Omega_0=2\pi/T_0\)" in html
    assert r"\(X(e^{j\omega})\)" in html
    assert "(Omega_0=2pi/T_0)" not in html
