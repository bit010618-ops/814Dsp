from pathlib import Path


def test_batch_fourteen_preserves_2015_pole_zero_question_and_solution(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_fourteen_mathjax_component as component

    html = component.write_html(tmp_path / "batch-fourteen.html").read_text(encoding="utf-8")

    assert "七、离散因果 LTI 系统的系统函数" in html
    assert r"h[0]=2" in html
    assert r"H(z)=\frac{2}{1-2z^{-1}}=\frac{2z}{z-2}" in html
    assert r"\operatorname{ROC}:\left|z\right|>2" in html
    assert r"h[n]=2^{n+1}u[n]" in html
    assert r"y[n]-2y[n-1]=2x[n]" in html
    assert 'aria-label="2015 年第七题的零极点图"' in html
    assert 'data-role="zero"' in html and 'data-role="pole"' in html
