from pathlib import Path


def test_priority_2003_question_preserves_statement_and_detailed_solution(tmp_path: Path):
    from full.tools import build_chapter_03_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-03-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-03-answers.html").read_text(encoding="utf-8")

    assert "2003 年真题" in question
    assert "最高频率为 200 Hz" in question
    assert "以 Nyquist 频率采样" in question
    assert "频率分辨率为 10 Hz" in question
    assert r"x(n)=x_a(nT)" in question
    assert r"f_s=2\times200=400\,\mathrm{Hz}" in answer
    assert r"N=\frac{f_s}{F_0}=40" in answer
    assert r"\omega_k=\frac{2\pi k}{N}=\frac{2\pi k}{40}=\frac{\pi k}{20}" in answer
    assert r"f_k=kF_0=10k\,\mathrm{Hz}" in answer


def test_2002_dft_idft_convolution_question_keeps_the_unspecified_length_explicit(tmp_path: Path):
    from full.tools import build_chapter_03_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-03-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-03-answers.html").read_text(encoding="utf-8")

    assert "2002 年真题" in question
    assert r"x_1(n)=\left(\frac{1}{2}\right)^n" in question
    assert r"0\leq n\leq4" in question
    assert r"x_2(n)=1" in question
    assert r"x_3(n)=\operatorname{IDFT}\left[X_1(K)X_2(K)\right]" in question
    assert r"x_3(n)=x_1(n)\mathbin{\circledast}_N x_2(n)" in answer
    assert r"N\geq5+3-1=7" in answer
    assert r"\left\{1,\frac{3}{2},\frac{7}{4},\frac{7}{8},\frac{7}{16},\frac{3}{16},\frac{1}{16}\right\}" in answer


def test_2002_frequency_resolution_question_has_the_required_zero_padding_calculation(tmp_path: Path):
    from full.tools import build_chapter_03_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-03-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-03-answers.html").read_text(encoding="utf-8")

    assert "2002 年真题（第十题）" in question
    assert r"T=0.15\,\mathrm{s}" in question
    assert r"\Delta\Omega=\frac{2\pi}{NT}" in answer
    assert r"N>\frac{2\pi}{2\times0.15}" in answer
    assert r"N\geq21" in answer
    assert r"N=32" in answer


def test_2004_frequency_resolution_question_keeps_all_three_sine_frequencies(tmp_path: Path):
    from full.tools import build_chapter_03_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-03-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-03-answers.html").read_text(encoding="utf-8")

    assert "2004 年真题" in question
    assert r"f_s=100\,\mathrm{Hz}" in question
    assert "取样 256 点" in question
    assert r"f_1=2\,\mathrm{Hz}" in question
    assert r"f_2=2.02\,\mathrm{Hz}" in question
    assert r"f_3=2.07\,\mathrm{Hz}" in question
    assert r"F_0=\frac{f_s}{N}=\frac{100}{256}=0.390625\,\mathrm{Hz}" in answer
    assert r"\left|f_3-f_1\right|=0.07\,\mathrm{Hz}<F_0" in answer


def test_2005_five_point_dft_question_and_answer_keep_periodic_aliasing(tmp_path: Path):
    from full.tools import build_chapter_03_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "questions.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "answers.html").read_text(encoding="utf-8")

    assert "2005 年真题" in question
    assert r"2\delta(n-5)" in question
    assert r"\mathbin{\circledast}_5" in answer
    assert r"y(n)=\{6,6,9,9,6\}" in answer


def test_2005_question_uses_complete_latex_for_every_math_fragment(tmp_path: Path):
    from full.tools import build_chapter_03_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "questions.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "answers.html").read_text(encoding="utf-8")

    assert r"\(x(n)=\delta(n)+3\delta(n-1)+3\delta(n-2)+2\delta(n-5)\)" in question
    assert r"\(h(n)=\delta(n)+\delta(n-1)+\delta(n-2)+\delta(n-3)\)" in question
    assert r"\(X(K)\)" in question
    assert r"\(H(K)\)" in question
    assert r"\(Y(K)=X(K)H(K)\)" in question
    assert "(delta(n-5))" not in answer


def test_every_chapter_three_training_question_has_its_own_exam_page(tmp_path: Path):
    from full.tools import build_chapter_03_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "questions.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') == 5
