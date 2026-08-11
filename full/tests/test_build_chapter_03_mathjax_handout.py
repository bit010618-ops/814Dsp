from pathlib import Path


def test_chapter_three_assembler_keeps_source_order_and_training_separate(tmp_path: Path):
    from full.tools import build_chapter_03_mathjax_handout as handout

    html = handout.write_html(tmp_path / "chapter-03.html").read_text(encoding="utf-8")

    positions = [html.index(title) for title in (
        "3.1 离散傅里叶级数及其性质",
        "3.2 离散傅里叶变换的定义及性质",
        "3.3 用 DFT 求解 LSI 系统输出",
        "3.4 频域采样定理",
        "3.5 用 DFT 对模拟信号作频谱分析",
        "第三章 分章强化训练",
    )]
    assert positions == sorted(positions)
    assert "真题整理详解" not in html
    assert "MATLAB" not in html


def test_chapter_three_answer_assembler_reuses_the_answer_component(tmp_path: Path):
    from full.tools import build_chapter_03_mathjax_handout as handout

    html = handout.write_answers_html(tmp_path / "chapter-03-answers.html").read_text(encoding="utf-8")

    assert "真题整理详解" in html
    assert "2003 年真题" in html
    assert "2002 年真题（第十题）" in html
    assert "2004 年真题" in html
