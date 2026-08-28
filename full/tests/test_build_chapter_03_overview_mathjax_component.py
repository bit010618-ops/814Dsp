from pathlib import Path


def test_overview_component_uses_mathjax_for_frequency_bridge_formulae(tmp_path: Path):
    from full.tools import build_chapter_03_overview_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-overview.html").read_text(
        encoding="utf-8"
    )

    assert "四类傅里叶描述的坐标关系" in html
    assert r"\(\Omega_0=2\pi/T_0\)" in html
    assert r"\(X(e^{j\omega})\)" in html
    assert r"\(T_0\) 无限增大" in html
    assert r"\(T\) 变为序列" in html
    assert r"\(\Omega\) 与数字角频率 \(\omega\)" in html
    assert "(Omega_0=2pi/T_0)" not in html


def test_overview_keeps_rectangular_pulse_fs_and_real_even_harmonics(tmp_path: Path):
    from full.tools import build_chapter_03_overview_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-overview.html").read_text(
        encoding="utf-8"
    )
    assert r"\operatorname{Sa}\left(\frac{k\Omega_0\tau}{2}\right)" in html
    assert r"\frac{\tau}{T_0}" in html
    assert r"\widetilde{x}(t)=X(j0)+\sum_{k=1}^{\infty}2X(jk\Omega_0)\cos(k\Omega_0t)" in html


def test_overview_explains_that_fs_coefficient_value_needs_frequency_context(
    tmp_path: Path,
):
    from full.tools import build_chapter_03_overview_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-overview.html").read_text(
        encoding="utf-8"
    )

    assert r"同一序号 \(k\) 的系数数值可相同" in html
    assert r"物理频率仍由 \(k\Omega_0\) 给出" in html
