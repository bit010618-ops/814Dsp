from pathlib import Path


def test_batch_one_preserves_six_verified_dft_questions_and_detailed_answers(tmp_path: Path):
    from full.tools import build_chapter_03_supplemental_training_batch_one_mathjax_component as component

    training = component.write_training_html(tmp_path / "chapter-03-batch-one-training.html").read_text(encoding="utf-8")
    answers = component.write_answers_html(tmp_path / "chapter-03-batch-one-answers.html").read_text(encoding="utf-8")

    assert training.count('class="exam-page"') == 6
    assert "2003 年真题（判断题第 1 小题）" in training
    assert r"y(n)=x\left((n+5)\right)_8R_8(n)" in training
    assert "2003 年真题（判断题第 3 小题）" in training
    assert r"h_N(n)=\operatorname{IDFT}[H(k)]" in training
    assert "2006 年真题（第九题）" in training
    assert r"x(n)=\delta(n)+2\delta(n-5)" in training
    assert r"Y(k)=e^{j2k\pi/10}X(k)" in training
    assert "2006 年真题（第十二题）" in training
    assert "DFT 为 1024 点的重叠保留法" in training
    assert "2007 年真题（填空题第 2 小题）" in training
    assert "2007 年真题（简答题第 2 小题）" in training
    assert "频谱泄露产生的主要原因是什么？可以用什么方法加以改善？" in training
    assert r"X(k)=1+2e^{-j2\pi k\cdot5/10}=1+2e^{-j\pi k}=1+2(-1)^k" in answers
    assert r"y(n)=x\left((n+2)\right)_{10}" in answers
    assert r"\left\{3,3,1,1,1,3,3,2,2,2\right\}" in answers
    assert r"L_b=1024-64+1=961" in answers
    assert r"\left\lceil\frac{80000}{961}\right\rceil=84" in answers
    assert r"N\geq100" in answers
    assert "加长有效记录时间" in answers
    assert "mod N" not in training + answers
