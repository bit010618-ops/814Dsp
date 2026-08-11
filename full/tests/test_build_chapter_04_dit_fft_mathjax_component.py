from pathlib import Path


def test_dit_fft_component_preserves_decimation_butterfly_cost_and_bit_reversal(tmp_path: Path):
    from full.tools import build_chapter_04_dit_fft_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-04-dit.html").read_text(encoding="utf-8")

    assert "4.2 基于时间抽取的基-2-FFT 快速算法" in html
    assert r"x_1(r)=x(2r)" in html
    assert r"X(k)&=X_1(k)+W_N^kX_2(k)" in html
    assert r"\frac{N}{2}\log_2N" in html
    assert "码位倒序" in html
    assert "0.013824" in html
    assert "MATLAB" not in html
