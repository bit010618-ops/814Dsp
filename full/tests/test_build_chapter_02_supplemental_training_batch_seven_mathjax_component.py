from pathlib import Path


def test_batch_seven_preserves_2024_z_plane_and_magnitude_prompt(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_seven_mathjax_component as component

    html = component.write_html(tmp_path / "batch-seven.html").read_text(encoding="utf-8")

    assert "2024 年真题" in html
    assert "2.已知某线性移不变系统的系统函数是" in html
    assert r"H(z)=0.18\frac{1-z^{-2}}{1+0.64z^{-2}}" in html
    assert r"\omega\in[0,2\pi]" in html
    assert r"\left|H(e^{j\omega})\right|" in html
    assert 'aria-label="2024 年第二章真题的零极点图"' in html
    assert 'aria-label="2024 年第二章真题的幅频响应"' in html
    assert 'data-role="zero-at-plus-one"' in html
    assert 'data-role="zero-at-minus-one"' in html
    assert 'data-role="pole-at-plus-j08"' in html
    assert 'data-role="pole-at-minus-j08"' in html


def test_batch_seven_derives_exact_magnitude_and_key_response_values(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_seven_mathjax_component as component

    html = component.write_html(tmp_path / "batch-seven.html").read_text(encoding="utf-8")

    assert r"0.18\frac{z^2-1}{z^2+0.64}" in html
    assert r"z=\pm1" in html
    assert r"z=\pm j0.8" in html
    assert r"\left|H(e^{j\omega})\right|=" in html
    assert r"\frac{0.36\left|\sin\omega\right|}{\sqrt{1.4096+1.28\cos(2\omega)}}" in html
    assert r"\left|H(e^{j0})\right|=\left|H(e^{j\pi})\right|=\left|H(e^{j2\pi})\right|=0" in html
    assert r"\left|H(e^{j\pi/2})\right|=\left|H(e^{j3\pi/2})\right|=1" in html


def test_batch_seven_browser_dom_has_no_raw_math_delimiters(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_seven_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-seven.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
