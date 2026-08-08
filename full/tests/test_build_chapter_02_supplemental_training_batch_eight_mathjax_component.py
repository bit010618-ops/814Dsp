from pathlib import Path


def test_batch_eight_preserves_all_2023_lsti_subquestions(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_eight_mathjax_component as component

    html = component.write_html(tmp_path / "batch-eight.html").read_text(encoding="utf-8")

    assert "2023 年真题" in html
    assert r"y(n)=x(n)-x(n-2)" in html
    assert "（1）该系统函数" in html
    assert r"\(H(z)\)" in html
    assert r"\(h(n)\)" in html
    assert "（2）判断系统是否因果性和稳定性。" in html
    assert "（3）画出系统幅频响应和相频响应，该系统是否具有线性相位？" in html
    assert "（4）若系统输入" in html
    assert r"\(x(n)=1+2(-1)^n+\cos(0.5\pi n)\)" in html


def test_batch_eight_derives_fir_response_and_spectral_output(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_eight_mathjax_component as component

    html = component.write_html(tmp_path / "batch-eight.html").read_text(encoding="utf-8")

    assert r"H(z)=1-z^{-2}" in html
    assert r"h[n]=\delta[n]-\delta[n-2]" in html
    assert r"\left|H(e^{j\omega})\right|=2\left|\sin\omega\right|" in html
    assert r"\frac{\pi}{2}-\omega" in html
    assert r"\frac{3\pi}{2}-\omega" in html
    assert r"y[n]=2\cos\!\left(0.5\pi n\right)" in html
    assert 'aria-label="2023 年第八题的幅频响应"' in html
    assert 'aria-label="2023 年第八题的相频响应"' in html
    assert 'data-role="magnitude-curve"' in html
    assert 'data-role="phase-segment-left"' in html
    assert 'data-role="phase-segment-right"' in html


def test_batch_eight_browser_dom_has_no_raw_math_delimiters(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_eight_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-eight.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
