from pathlib import Path

from full.tools.build_chapter_01_difference_equation_mathjax_component import write_html


ROOT = Path(__file__).resolve().parents[2]


def test_difference_equation_component_uses_mathjax_and_a_real_svg_structure_diagram(
    tmp_path: Path,
):
    source = (
        ROOT / "full/tools/build_chapter_01_difference_equation_mathjax_component.py"
    ).read_text(encoding="utf-8")

    html = write_html(tmp_path / "difference-equation.html").read_text(encoding="utf-8")
    assert "mathjax@3" in html
    assert r"\sum_{k=0}^{N}a_k y(n-k)" in html
    assert r"h(n)&=a h(n-1)=a^n u(n)" in html
    assert r"h(n)&=-a^n u(-n-1)" in html
    assert r"y(n)=b_0x(n)-a_1y(n-1)" in html
    assert "feedback_structure_svg" in source
    assert "<svg" in source
    assert "drawImage" not in source
    assert "ImageReader" not in source
