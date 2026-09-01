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


def test_overview_includes_general_fs_pair_and_calculated_partial_sum_comparison(
    tmp_path: Path,
):
    """The opening FS source pages require the transform pair and finite-harmonic evidence."""
    from full.tools import build_chapter_03_overview_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-overview.html").read_text(
        encoding="utf-8"
    )

    assert r"\widetilde{x}(t)=\sum_{k=-\infty}^{\infty}X(jk\Omega_0)e^{jk\Omega_0t}" in html
    assert r"X(jk\Omega_0)=\frac{1}{T_0}\int_{-T_0/2}^{T_0/2}" in html
    assert 'data-plot="fourier-series-partial-sums"' in html
    assert "有限谐波数逼近的实际效果" in html


def test_overview_keeps_the_fs_to_ft_limit_bridge(tmp_path: Path):
    from full.tools import build_chapter_03_overview_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-overview.html").read_text(
        encoding="utf-8"
    )

    assert r"X(j\Omega)=T_0X(jk\Omega_0)" in html
    assert r"\sum_{k=-\infty}^{\infty}\frac{\Omega_0}{2\pi}" in html
    assert r"x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(j\Omega)e^{j\Omega t}\,\mathrm{d}\Omega" in html


def test_overview_explains_that_fs_coefficient_value_needs_frequency_context(
    tmp_path: Path,
):
    from full.tools import build_chapter_03_overview_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-overview.html").read_text(
        encoding="utf-8"
    )

    assert r"同一序号 \(k\) 的系数数值可相同" in html
    assert r"物理频率仍由 \(k\Omega_0\) 给出" in html


def test_overview_redraws_the_five_stage_fourier_family_map(tmp_path: Path):
    """The unique source-page-527 relationship graphic must remain editable."""
    from full.tools import build_chapter_03_overview_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-overview.html").read_text(
        encoding="utf-8"
    )

    assert 'id="fourier-family-map"' in html
    assert "连续、离散、截断与周期延拓的频谱对应关系" in html
    for transform in ("FT", "DTFT", "DFS", "DFT"):
        assert transform in html
    for expression in (
        r"x_a(t)",
        r"X_a(j\Omega)",
        r"x(n)w(n)",
        r"\widetilde{x}_N(n)",
        r"X_N(k)",
    ):
        assert expression in html
    assert "MOOC" not in html
    assert "watermark" not in html
