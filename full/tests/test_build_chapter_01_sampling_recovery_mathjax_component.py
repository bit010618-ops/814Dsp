from pathlib import Path


def test_sampling_recovery_uses_mathjax_and_data_driven_figures(tmp_path: Path):
    from full.tools.build_chapter_01_sampling_recovery_mathjax_component import write_html

    html = write_html(tmp_path / "sampling-recovery.html").read_text(encoding="utf-8")

    assert "mathjax@3" in html
    assert r"H_r(j\Omega)=" in html
    assert r"T, & \left|\Omega\right|\leq\frac{\Omega_s}{2}" in html
    assert r"h_r(t)=\frac{T\sin" in html
    assert r"y_a(t)=x_s(t)\ast h_r(t)" in html
    assert r"g(0)=1" in html
    assert "recovery_spectrum_svg" in html
    assert "interpolation_sinc_svg" in html
    assert "<svg" in html
    assert "drawImage" not in html
    assert "<image" not in html
