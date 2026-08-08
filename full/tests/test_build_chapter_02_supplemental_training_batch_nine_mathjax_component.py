from pathlib import Path


def test_batch_nine_preserves_the_complete_2020_frequency_response_question(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_nine_mathjax_component as component

    html = component.write_html(tmp_path / "batch-nine.html").read_text(encoding="utf-8")

    assert "2020 年真题" in html
    assert "四、设 LTI 系统的频率响应为" in html
    assert r"\(H(e^{j\omega})=\frac{1-e^{-2j\omega}}{1+0.5e^{-2j\omega}}\)" in html
    assert r"\(x[n]=\cos\left(\frac{\pi n}{2}\right)\)" in html
    assert "求系统的输出信号。" in html


def test_batch_nine_derives_the_complex_gain_and_output_signal(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_nine_mathjax_component as component

    html = component.write_html(tmp_path / "batch-nine.html").read_text(encoding="utf-8")

    assert r"H\!\left(e^{j\frac{\pi}{2}}\right)&=" in html
    assert r"H\!\left(e^{-j\frac{\pi}{2}}\right)&=" in html
    assert r"=4" in html
    assert r"\\&=4\cos\left(\frac{\pi n}{2}\right)" in html
    assert "无需附加相位偏移" in html


def test_batch_nine_browser_dom_has_no_raw_math_delimiters(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_nine_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-nine.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
