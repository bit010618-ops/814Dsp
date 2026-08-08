from pathlib import Path


def test_batch_six_preserves_2014_feedback_system_prompt_and_uses_standard_svg(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_six_mathjax_component as component

    html = component.write_html(tmp_path / "batch-six.html").read_text(encoding="utf-8")

    assert "2014 年真题" in html
    assert "五、某离散 LTI 系统如图所示：" in html
    assert "（1）写出系统的差分方程；" in html
    assert "（5）写出系统的频率响应。" in html
    assert 'aria-label="2014 年第五题的单延时反馈离散系统结构图"' in html
    assert 'data-role="feedback-gain"' in html
    assert 'data-port="bottom"' in html
    assert 'class="diagram roc-diagram"' in html
    assert '.roc-diagram{width:min(100%,330pt)}' in html
    assert 'style="width:min(100%,330pt)"' in html
    assert r"\(+\)" in html
    assert "ІВ" not in html
    assert r"\(z^{-1}\)" in html
    assert r"\(\frac{1}{2}\)" in html


def test_batch_six_derives_h_roc_impulse_and_frequency_response(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_six_mathjax_component as component

    html = component.write_html(tmp_path / "batch-six.html").read_text(encoding="utf-8")

    assert r"y[n]=x[n]+\frac{1}{2}y[n-1]" in html
    assert r"\frac{Y(z)}{X(z)}=\frac{1}{1-\frac{1}{2}z^{-1}}" in html
    assert r"\operatorname{ROC}:\left|z\right|>\frac{1}{2}" in html
    assert r"h[n]=\left(\frac{1}{2}\right)^n u[n]" in html
    assert r"H(e^{j\omega})&=\frac{1}{1-\frac{1}{2}e^{-j\omega}}" in html
    assert html.index(r"h[n]=\left(\frac{1}{2}\right)^n u[n]") < html.index(
        'class="diagram roc-diagram"'
    )


def test_batch_six_browser_dom_has_no_raw_math_delimiters(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_six_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-six.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
