from pathlib import Path


def test_2007_bilinear_stability_proof_is_kept_as_a_sixth_chapter_question(tmp_path: Path):
    from full.tools import build_chapter_06_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-06-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-06-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') == 1
    assert "2007 年真题" in question
    assert "八、证明：时间连续的稳定系统经双线性变换后得到的离散系统仍然是稳定系统；反之亦真。" in question
    assert r"s=\frac{2}{T}\frac{z-1}{z+1}" in question
    assert "详解见 P.____" in question
    assert r"&=\frac{2}{T}\frac{\left|z\right|^2-1}{\left|z+1\right|^2}" in answer
    assert "左半平面" in answer
    assert "单位圆内" in answer
