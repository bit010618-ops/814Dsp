from pathlib import Path


def test_chapter_two_mathjax_handout_uses_one_continuous_document(tmp_path: Path):
    from full.tools.build_chapter_02_mathjax_handout import write_html

    html = write_html(tmp_path / "chapter-two.html").read_text(encoding="utf-8")
    assert "mathjax@3" in html
    assert "page-break-after:always" not in html
    assert "z 变换的基本概念" in html
    assert "离散时间信号傅里叶变换" in html
    assert "系统函数及其与系统性质的关系" in html
    assert "特殊滤波器的设计" in html
    assert "2015 年真题" in html
    assert "2021 年真题" in html
    assert "2025 年真题" in html
    assert "2002 年真题" in html
    assert "2006 年真题" in html
    assert "已知某离散系统方框图如下：求" in html
    assert r"F(z)=\frac{z^2}{z^2-2z-3}" in html
    assert "以除去 5kHz&lt;F&lt;10kHz 的频率成分" in html
    assert 'class="header"' not in html
    assert 'counter(page)' not in html
    assert '.exam-page{break-before:page;min-height:230mm}' in html
    assert html.count('<main>') == 1


def test_chapter_two_pdf_export_requires_complete_mathjax_document(tmp_path: Path):
    from full.tools.build_chapter_02_mathjax_handout import (
        assert_mathjax_ready,
        rendered_dom,
        write_html,
    )

    dom = rendered_dom(write_html(tmp_path / "chapter-two.html"))
    assert_mathjax_ready(dom)
