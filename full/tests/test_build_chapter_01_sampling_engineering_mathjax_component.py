from pathlib import Path


def test_sampling_engineering_uses_mathjax_and_vector_signal_figures(tmp_path: Path):
    from full.tools.build_chapter_01_sampling_engineering_mathjax_component import write_html

    html = write_html(tmp_path / "sampling-engineering.html").read_text(encoding="utf-8")

    assert "mathjax@3" in html
    assert r"f_h\leq\frac{f_s}{2}" in html
    assert r"f_0=f_h-\frac{\Delta f_0}{2}" in html
    assert r"f_s=2\Delta f_0" in html
    assert "anti_alias_spectrum_svg" in html
    assert "bandpass_spectrum_svg" in html
    assert "<svg" in html
    assert "drawImage" not in html
    assert "<image" not in html
