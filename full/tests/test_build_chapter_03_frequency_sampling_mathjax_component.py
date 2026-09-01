from pathlib import Path


def test_frequency_sampling_component_covers_periodic_summation_and_recovery(tmp_path: Path):
    from full.tools import build_chapter_03_frequency_sampling_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-frequency-sampling.html").read_text(encoding="utf-8")

    assert "3.4 频域采样定理" in html
    assert r"X(k)=X\left(e^{j\omega}\right)\bigg|_{\omega=\frac{2\pi k}{N}}" in html
    assert r"\widetilde{X}(k)=\left.X(z)\right|_{z=W_N^{-k}}" in html
    assert r"\frac{1}{N}\sum_{k=0}^{N-1}W_N^{(m-n)k}" in html
    assert r"\begin{cases}" in html
    assert r"1, & m=n+rN,\\" in html
    assert r"\widetilde{x}(n)" in html
    assert r"\sum_{r=-\infty}^{\infty}x(n-rN)" in html
    assert r"N\geq M" in html
    assert r"X(z)=\sum_{n=0}^{M-1}x(n)z^{-n}" in html
    assert r"X(z)=\frac{1-z^{-N}}{N}" in html
    assert r"\Phi_k(z)=\frac{1}{N}\frac{1-z^{-N}}{1-W_N^{-k}z^{-1}}" in html
    assert "时域混叠" in html
    assert "MATLAB" not in html
    assert "[[" not in html


def test_frequency_sampling_component_draws_the_sampling_duality_map(tmp_path: Path):
    from full.tools import build_chapter_03_frequency_sampling_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-frequency-sampling.html").read_text(encoding="utf-8")

    assert 'data-diagram="frequency-sampling-duality"' in html
    assert "频域采样与时域周期延拓的对应关系" in html
