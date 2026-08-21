from pathlib import Path


def test_chapter_eight_training_keeps_all_audited_questions_and_answers(tmp_path: Path):
    from full.tools import build_chapter_08_training_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-08-training.html").read_text(
        encoding="utf-8"
    )
    answers = component.write_answers_html(tmp_path / "chapter-08-answers.html").read_text(
        encoding="utf-8"
    )

    assert training.count('class="exam-head"') == 4
    assert "2013 年真题" in training
    assert "2015 年真题" in training
    assert "说明时分复用工作原理并举例。" in training
    assert "什么是多路复用。" in training
    assert "data-diagram=\"multirate-zero-insertion-chain\"" in training
    assert "水木观畴" not in training
    assert "详解见 P.____" in training
    assert "完整LaTeX源码" not in training
    assert "时分复用" in answers
    assert "频域复制" in answers
