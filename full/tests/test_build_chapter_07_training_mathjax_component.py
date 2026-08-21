from pathlib import Path


def test_chapter_seven_priority_training_keeps_three_original_questions_and_answers(tmp_path: Path):
    from full.tools import build_chapter_07_training_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-07-training.html").read_text(
        encoding="utf-8"
    )
    answers = component.write_answers_html(tmp_path / "chapter-07-answers.html").read_text(
        encoding="utf-8"
    )

    assert training.count('class="exam-head"') == 3
    assert "利用窗函数法设计数字带阻滤波器" in training
    assert "一个线性相位因果 FIR 数字滤波器" in training
    assert "用窗函数设计一个因果稳定的 FIR 线性相位高通数字滤波器" in training
    assert "水木观畴" not in training
    assert "详解见 P.____" in training
    assert "海明窗" in answers
    assert "最小群延迟" in answers
    assert "阻带衰减" in answers
