from pathlib import Path


def test_periodicity_component_uses_complete_mathjax_formulas(tmp_path: Path):
    from full.tools.build_chapter_01_periodicity_mathjax_component import write_html

    page = write_html(tmp_path / "periodicity.html").read_text(encoding="utf-8")

    assert "tex-mml-chtml.js" in page
    assert r"x(n+N)=x(n)" in page
    assert r"\frac{2\pi}{\omega}=\frac{N}{k}" in page
    assert r"A\cos\left(\frac{13\pi}{4}n\right)" in page
    assert r"A\cos(0.01\pi n)" in page
    assert r"A\cos\left(\frac{3\pi}{7}n\right)" in page
    assert r"n\sin(\omega n+\varphi)" in page
    assert r"12\pi\notin\mathbb{Q}" in page
    assert r"\operatorname{lcm}(10,200,200)=200" in page
    assert "<image" not in page
    assert "drawImage" not in page
    assert "MATLAB" not in page
