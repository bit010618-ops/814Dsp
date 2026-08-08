from pathlib import Path


def test_2003_z_stability_prompt_preserves_the_original_question(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_four_mathjax_component as component

    html = component.write_html(tmp_path / "batch.html").read_text(encoding="utf-8")
    assert "2003 年真题" in html
    assert "八、已知时域离散线性非移变系统的系统函数" in html
    assert r"H(z)=\frac{1}{(z-a)(z-b)}" in html
    assert r"\(a,b\)为常数" in html
    assert r"（1）要求系统稳定，确定\(a\)和\(b\)的取值域" in html
    assert r"（2）要求系统因果、稳定，确定\(a\)和\(b\)的取值域" in html


def test_2003_z_stability_renders_math_and_explains_two_distinct_conditions(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_four_mathjax_component as component

    html_path = component.write_html(tmp_path / "batch.html")
    html = html_path.read_text(encoding="utf-8")
    assert r"\left|a\right|<1" in html
    assert r"\left|b\right|<1" in html
    dom = component.rendered_dom(html_path)
    assert "<mjx-container" in dom
    assert r"\(" not in dom and r"\[" not in dom
    for required in ("（1）仅要求稳定", "（2）同时要求因果和稳定", "它既符合因果性，也包含单位圆，故系统稳定"):
        assert required in dom
