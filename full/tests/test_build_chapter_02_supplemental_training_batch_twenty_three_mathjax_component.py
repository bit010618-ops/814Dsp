from pathlib import Path


def test_2014_dtft_properties_prompt_preserves_the_original_question(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_three_mathjax_component as component

    html = component.write_html(tmp_path / "batch.html").read_text(encoding="utf-8")
    assert "2014 年真题" in html
    assert r"已知系统 \(x[n]\) 的傅里叶变换 \(X(e^{j\omega})\) 在 \(-\pi\leq\omega\leq\pi\) 的区间上幅频和相频图如图，" in html
    assert r"试确定 \(x[n]\) 是否是周期的，实信号，偶信号及有限能量的？" in html


def test_2014_dtft_properties_has_separate_textbook_amplitude_and_phase_plots(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_three_mathjax_component as component

    html = component.write_html(tmp_path / "batch.html").read_text(encoding="utf-8")
    assert 'aria-label="2014 年真题的 DTFT 幅频图"' in html
    assert 'aria-label="2014 年真题的 DTFT 相频图"' in html
    assert "幅频图" in html and "相频图" in html
    assert "marker-end=" in html
    assert r"\(-\pi/2\)" in html and r"\(\pi/2\)" in html
    assert ".plot-pair{break-inside:avoid" in html
    assert ".plot{display:block" in html


def test_2014_dtft_properties_renders_all_mathjax_and_explains_each_property(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_three_mathjax_component as component

    html_path = component.write_html(tmp_path / "batch.html")
    html = html_path.read_text(encoding="utf-8")
    assert r"X^*(e^{j\omega})=X(e^{-j\omega})" in html
    assert r"E_x=\frac{1}{2\pi}\int_{-\pi}^{\pi}\left|X(e^{j\omega})\right|^2\,\mathrm{d}\omega" in html
    dom = component.rendered_dom(html_path)
    assert "<mjx-container" in dom
    assert r"\(" not in dom and r"\[" not in dom
    for required in ("不是周期序列", "是实序列", "不是偶序列", "是有限能量序列"):
        assert required in dom
    assert "<math" in dom
