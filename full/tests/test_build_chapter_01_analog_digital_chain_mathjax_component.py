from pathlib import Path


def test_analog_digital_chain_uses_mathjax_and_structured_vector_diagrams(tmp_path: Path):
    from full.tools.build_chapter_01_analog_digital_chain_mathjax_component import write_html

    html = write_html(tmp_path / "analog-digital-chain.html").read_text(encoding="utf-8")

    assert "mathjax@3" in html
    assert r"x(n)=x_a(nT)" in html
    assert r"q(n)=Q\!\left[x(n)\right]" in html
    assert r"f_s=\frac{1}{T}" in html
    assert "analog_digital_chain_svg" in html
    assert "zero_order_hold_svg" in html
    assert "<svg" in html
    assert "drawImage" not in html
    assert "<image" not in html
