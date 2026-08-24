from pathlib import Path


def test_batch_thirteen_preserves_and_solves_the_missing_2006_dtft_inverse_question(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_thirteen_mathjax_component as component

    html = component.write_html(tmp_path / "batch-thirteen.html").read_text(encoding="utf-8")

    assert "十、求如下图所示的" in html
    assert r"X(e^{j\omega})=" in html
    assert r"2, & \left|\omega\right|\le\frac{\pi}{4}" in html
    assert r"1, & \frac{\pi}{4}<\left|\omega\right|\le\frac{3\pi}{4}" in html
    assert r"x[n]=\begin{cases}" in html
    assert r"\frac{\sin\left(\frac{3\pi n}{4}\right)+\sin\left(\frac{\pi n}{4}\right)}{\pi n}" in html
    assert 'class="formula-name">离散时间傅里叶反变换积分（用于由给定频谱恢复离散序列）' in html
    assert 'class="formula-name">分段频谱的反变换结果（用于给出完整离散序列）' in html


def test_batch_thirteen_browser_dom_has_no_raw_math_or_formula_scrollbar(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_thirteen_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-thirteen.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
    assert "overflow-x: auto" not in dom
