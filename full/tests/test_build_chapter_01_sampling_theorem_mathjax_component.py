from pathlib import Path


def test_sampling_theorem_uses_mathjax_and_data_driven_spectrum_svg(tmp_path: Path):
    from full.tools.build_chapter_01_sampling_theorem_mathjax_component import write_html

    html = write_html(tmp_path / "sampling.html").read_text(encoding="utf-8")

    assert "tex-mml-chtml.js" in html
    assert r"\delta_T(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT)" in html
    assert r"\Delta_T(j\Omega)=\Omega_s\sum_{k=-\infty}^{\infty}\delta(\Omega-k\Omega_s)" in html
    assert r"X_s(j\Omega)=\frac{1}{T}\sum_{k=-\infty}^{\infty}" in html
    assert r"\frac{\Omega}{\Omega_s}=\frac{f}{f_s}=\frac{\omega}{2\pi}" in html
    assert r"\Omega_s\geq2\Omega_h" in html
    assert r"f_s\geq2f_h" in html
    assert "spectrum_svg" in html
    assert 'id="time-domain-sampling-diagram"' in html
    assert 'aria-label="理想时域采样示意图"' in html
    assert "<svg" in html
    assert "drawImage" not in html
    assert "<image" not in html
