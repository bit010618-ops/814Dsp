from pathlib import Path


def test_causal_stable_uses_complete_mathjax_without_formula_images(tmp_path: Path):
    from full.tools.build_chapter_01_causal_stable_mathjax_component import write_html
    page = write_html(tmp_path / "causal.html").read_text(encoding="utf-8")
    assert "mathjax@3" in page
    assert r"h(n)=0\quad(n<0)" in page
    assert r"|x(n)|\leq M<\infty" in page
    assert r"\sum_{n=-\infty}^{\infty}|h(n)|=q<\infty" in page
    assert "break-after:page" not in page
    assert "<image" not in page
    assert "drawImage" not in page
