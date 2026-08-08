from pathlib import Path


def test_batch_eleven_preserves_all_four_related_2024_difference_equation_parts(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_eleven_mathjax_component as component

    html = component.write_html(tmp_path / "batch-eleven.html").read_text(encoding="utf-8")

    assert "2024 年真题" in html
    assert "九、如果一个因果 LSI 系统的输入输出满足如下差分方程" in html
    assert r"\[y(n)=ay(n-1)+x(n)\]" in html
    assert "（1）请问" in html
    assert "（2）考虑一个因果 LSI 系统，其输入输出关系由如下差分方程描述：" in html
    assert r"\[y(n)=ay(n-1)+x(n)-a^Nx(n-N)\]" in html
    assert "（3）请问(2)中的系统是 FIR 还是 IIR 系统？" in html
    assert r"（4）若(2)中的系统是稳定的，请问对 \(a\) 取何值是否有限制？" in html


def test_batch_eleven_derives_cancellation_fir_response_and_stability(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_eleven_mathjax_component as component

    html = component.write_html(tmp_path / "batch-eleven.html").read_text(encoding="utf-8")

    assert r"\left|a\right|<1" in html
    assert r"H(z)=\frac{1-a^Nz^{-N}}{1-az^{-1}}" in html
    assert r"\\&=a^n\left(u[n]-u[n-N]\right)" in html
    assert r"=\sum_{k=0}^{N-1}a^kz^{-k}" in html
    assert r"是一个长度为 \(N\) 的 FIR 系统" in html
    assert r"任意有限的 \(a\) 均稳定" in html


def test_batch_eleven_browser_dom_has_no_raw_math_delimiters(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_eleven_mathjax_component as component

    dom = component.rendered_dom(component.write_html(tmp_path / "batch-eleven.html"))

    assert "<mjx-container" in dom
    for delimiter in (r"\(", r"\)", r"\[", r"\]"):
        assert delimiter not in dom
