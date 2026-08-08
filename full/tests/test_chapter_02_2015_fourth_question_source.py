"""Source-fidelity regression for the 2015 fourth question."""


def test_2015_fourth_question_keeps_its_real_year_number_and_three_parts():
    from full.tools import build_chapter_02_supplemental_training_batch_four_mathjax_component as component

    training = component.training_html()

    assert "2015 年真题" in training
    assert "四、某离散系统如图所示：" in training
    assert "（1）求出系统函数" in training
    assert "（2）求出系统的单位脉冲响应；" in training
    assert "（3）写出一个满足稳定、非因果的单位脉冲响应函数。" in training
    assert 'aria-label="2015 年第四题的离散系统结构图"' in training
