from pathlib import Path


def test_chapter_eight_component_covers_multirate_main_body(tmp_path: Path):
    from full.tools import build_chapter_08_multirate_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-08.html").read_text(encoding="utf-8")

    titles = (
        "8.1 信号的整数倍抽取",
        "8.2 信号的整数倍内插",
        "8.3 抽取与内插的频域关系",
        "8.4 有理数倍采样率变换与多相结构",
    )
    positions = [html.index(title) for title in titles]
    assert positions == sorted(positions)
    assert r"y(n)=x(Mn)" in html
    assert r"y(n)=\sum_{k=-\infty}^{\infty}x(k)\delta(n-kL)" in html
    assert r"F_s'=\frac{L}{M}F_s" in html
    assert "MATLAB" not in html
    assert "真题" not in html
