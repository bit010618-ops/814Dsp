from pathlib import Path


def test_2007_constant_dtft_prompt_is_source_faithful(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_five_mathjax_component as component

    html = component.write_html(tmp_path / "batch.html").read_text(encoding="utf-8")
    assert "2007 年真题" in html
    assert r"2.若信号\(x(n)=k\)，\(k\)为常数，求其离散时间傅里叶变换；" in html


def test_2007_constant_dtft_renders_the_periodic_impulse_train(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_five_mathjax_component as component

    html_path = component.write_html(tmp_path / "batch.html")
    html = html_path.read_text(encoding="utf-8")
    assert r"X\!\left(e^{j\omega}\right)=2\pi k\sum_{m=-\infty}^{\infty}\delta\!\left(\omega-2\pi m\right)" in html
    dom = component.rendered_dom(html_path)
    assert "<mjx-container" in dom
    assert r"\(" not in dom and r"\[" not in dom
    assert "广义函数意义下" in dom
