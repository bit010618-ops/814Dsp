from pathlib import Path


def test_batch_thirteen_preserves_and_solves_complete_2025_frequency_response_question(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_thirteen_mathjax_component as component

    html = component.write_html(tmp_path / "batch-thirteen.html").read_text(encoding="utf-8")

    assert "八、已知某因果稳定的 LSI 系统" in html
    assert r"y(n)=\frac{1}{4}\left[x(n)-x(n-1)+x(n+2)-x(n-3)\right]" in html
    assert r"H_2(e^{j\omega})=H_1(-e^{j\omega})" in html
    assert r"h_2[n]=(-1)^nh_1[n]" in html
    assert r"H_1(e^{j\omega})=j e^{-j\frac{\omega}{2}}\cos\omega\sin\left(\frac{3\omega}{2}\right)" in html


def test_batch_thirteen_browser_dom_has_no_raw_math_or_formula_scrollbar(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_thirteen_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-thirteen.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
    assert "overflow-x: auto" not in dom
