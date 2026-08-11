from pathlib import Path


def test_spectrum_analysis_component_covers_sampling_leakage_and_picket_fence(tmp_path: Path):
    from full.tools import build_chapter_03_spectrum_analysis_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-spectrum.html").read_text(encoding="utf-8")

    assert "3.5 用 DFT 对模拟信号作频谱分析" in html
    assert r"f_s\geq2f_h" in html
    assert r"T_0=NT" in html
    assert r"F_0=\frac{1}{T_0}" in html
    assert "频谱泄漏" in html
    assert "栅栏效应" in html
    assert "零填充" in html
    assert "MATLAB" not in html


def test_spectrum_analysis_component_keeps_the_fourier_history_reading(tmp_path: Path):
    from full.tools import build_chapter_03_spectrum_analysis_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-spectrum.html").read_text(encoding="utf-8")

    assert "傅里叶的故事" in html
    assert "热的解析理论" in html
    assert "狄利克雷条件" in html
