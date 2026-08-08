from pathlib import Path


def test_batch_ten_preserves_the_2022_flow_graph_question_and_two_parts(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_ten_mathjax_component as component

    html = component.write_html(tmp_path / "batch-ten.html").read_text(encoding="utf-8")

    assert "2022 年真题" in html
    assert "八、一离散时间 LTI 系统流图如下图所示：" in html
    assert "（1）该系统的系统函数" in html
    assert "（2）当" in html
    assert r"\(N=8\)" in html
    assert "画出该系统的零极点图及幅频响应曲线。" in html
    assert 'aria-label="2022 年第八题的离散 LTI 系统流图"' in html
    assert 'data-role="summing-node"' in html
    assert 'data-role="delay-block"' in html
    assert 'data-role="gain-block"' in html


def test_batch_ten_derives_system_function_poles_zeros_and_magnitude(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_ten_mathjax_component as component

    html = component.write_html(tmp_path / "batch-ten.html").read_text(encoding="utf-8")

    assert r"H(z)=1-z^{-N}=\frac{z^N-1}{z^N}" in html
    assert r"z_k=e^{j\frac{2\pi k}{8}}" in html
    assert r"\left|H(e^{j\omega})\right|=2\left|\sin(4\omega)\right|" in html
    assert 'aria-label="2022 年第八题的零极点图"' in html
    assert 'aria-label="2022 年第八题的幅频响应"' in html
    assert 'data-role="zero"' in html
    assert 'data-role="pole-at-origin"' in html
    assert 'data-role="magnitude-curve"' in html
    assert r"\operatorname{Re}(z)" in html
    assert r"\operatorname{Im}(z)" in html


def test_batch_ten_browser_dom_has_no_raw_math_delimiters(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_ten_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-ten.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
