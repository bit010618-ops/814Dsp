from pathlib import Path


def test_batch_twelve_preserves_the_complete_2025_sampling_dtft_question(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twelve_mathjax_component as component

    html = component.write_html(tmp_path / "batch-twelve.html").read_text(encoding="utf-8")

    assert "2025 年真题" in html
    assert "四、一连续脉冲时间函数表达式为" in html
    assert r"\(x(t)=u(t)-u(t-7)\)" in html
    assert r"\(T=1\,\mathrm{s}\)" in html
    assert r"求 \(x(n)\) 的 DTFT，并画出幅度谱波形。" in html


def test_batch_twelve_derives_seven_point_sequence_dtft_and_data_driven_spectrum(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twelve_mathjax_component as component

    html = component.write_html(tmp_path / "batch-twelve.html").read_text(encoding="utf-8")

    assert r"x[n]=u[n]-u[n-7]" in html
    assert r"X(e^{j\omega})&=\sum_{n=0}^{6}e^{-j\omega n}" in html
    assert r"\\&=e^{-j3\omega}\frac{\sin\left(\frac{7\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}" in html
    assert r"\left|X(e^{j\omega})\right|=\left|\frac{\sin\left(\frac{7\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}\right|" in html
    assert 'aria-label="2025 年第四题的 DTFT 幅度谱"' in html
    assert 'data-role="magnitude-curve"' in html
    assert '<text x="344" y="245"' not in component.magnitude_svg()


def test_batch_twelve_browser_dom_has_no_raw_math_delimiters(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twelve_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-twelve.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
