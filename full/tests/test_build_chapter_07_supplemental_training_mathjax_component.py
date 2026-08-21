from pathlib import Path


def test_chapter_seven_supplemental_training_keeps_all_eight_verified_questions(tmp_path: Path):
    from full.tools import build_chapter_07_supplemental_training_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-07-supplemental-training.html").read_text(
        encoding="utf-8"
    )
    answers = component.write_answers_html(tmp_path / "chapter-07-supplemental-answers.html").read_text(
        encoding="utf-8"
    )

    assert training.count('class="exam-head"') == 8
    assert "窗函数的长短和形状对滤波器性能产生什么样的影响" in training
    assert "用频率采样法设计一类线性相位 FIR 滤波器" in training
    assert "FIR 滤波器的单位采样响应" in training
    assert r"用 \(N=15\) 设计一类 FIR" in training
    assert "用矩形窗设计一个低通滤波器" in training
    assert "设计 FIR 滤波器" in training
    assert "若有一窄带干扰，主频率分量等于" in training
    assert "已知某 2 阶 FIR 数字滤波器" in training
    assert "水木观畴" not in training
    assert "详解见 P.____" in training
    assert 'data-diagram="frequency-sampling-target"' in training
    assert 'class="structure-svg frequency-sampling-diagram"' in answers
    assert "主瓣" in answers
    assert "线性相位" in answers
    assert "水木观畴" not in answers
