from pathlib import Path


def test_2007_bilinear_stability_proof_is_kept_as_a_sixth_chapter_question(tmp_path: Path):
    from full.tools import build_chapter_06_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-06-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-06-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') >= 1
    assert "2007 年真题" in question
    assert "八、证明：时间连续的稳定系统经双线性变换后得到的离散系统仍然是稳定系统；反之亦真。" in question
    assert r"s=\frac{2}{T}\frac{z-1}{z+1}" in question
    assert "详解见 P.____" in question
    assert r"&=\frac{2}{T}\frac{\left|z\right|^2-1}{\left|z+1\right|^2}" in answer
    assert "左半平面" in answer
    assert "单位圆内" in answer


def test_2021_bilinear_butterworth_design_question_keeps_original_specification(tmp_path: Path):
    from full.tools import build_chapter_06_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-06-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-06-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') >= 2
    assert "2021 年真题" in question
    assert "八、采用双线性变换法设计一个贝特沃斯低通滤波器" in question
    assert r"f_p\,\mathrm{Hz}" in question
    assert r"f_s\,\mathrm{Hz}" in question
    assert r"\alpha_p\,\mathrm{dB}" in question
    assert r"\alpha_s\,\mathrm{dB}" in question
    assert r"\Omega_p&=\frac{2}{T}\tan\left(\frac{\omega_p}{2}\right)" in answer
    assert r"=\frac{2}{T}\tan\left(\pi f_pT\right)" in answer
    assert r"N=\left\lceil" in answer
    assert r"H(z)=H_a\left(\frac{2}{T}\frac{z-1}{z+1}\right)" in answer


def test_2023_iir_conversion_question_stays_whole_with_both_required_structures(tmp_path: Path):
    from full.tools import build_chapter_06_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-06-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-06-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') >= 3
    assert "2023 年真题" in question
    assert r"H(s)=\frac{2}{s^2+4s+3}" in question
    assert "脉冲响应不变法和双线性变换法各自的特点" in question
    assert 'data-diagram="impulse-invariance-parallel-iir"' in answer
    assert 'data-diagram="bilinear-direct-form-ii-iir"' in answer
    assert r"H_{\mathrm{ii}}(z)&=\frac{1}{1-e^{-1}z^{-1}}-\frac{1}{1-e^{-3}z^{-1}}" in answer
    assert r"H_{\mathrm{bl}}(z)" in answer
    assert r"{15-2z^{-1}-z^{-2}}" in answer
    assert "频谱混叠" in answer
    assert "频率扭曲" in answer


def test_2005_analog_system_question_is_whole_and_has_frequency_response_plot(tmp_path: Path):
    from full.tools import build_chapter_06_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-06-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-06-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') >= 4
    assert "2005 年真题" in question
    assert r"H(s)=\frac{5s+6}{s^3+5s^2+6s}" in question
    assert r"（5）设 \(T_s=0.2\)，写出该系统的离散传递函数 \(H(z)\)。" in question
    assert r"h(t)=\left(1+2e^{-2t}-3e^{-3t}\right)u(t)" in answer
    assert 'data-diagram="analog-lowpass-magnitude-response"' in answer
    assert r"H'(s)=\frac{1}{T}\sum_{k=-\infty}^{\infty}H\left(s-jk\Omega_s\right)" in answer
    assert r"H(z)" in answer
    assert r"&=\frac{1}{1-z^{-1}}" in answer


def test_2005_iir_reverse_design_question_keeps_both_independent_methods(tmp_path: Path):
    from full.tools import build_chapter_06_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-06-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-06-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') >= 5
    assert "2005 年真题（第十二题）" in question
    assert r"H(z)=\frac{2}{1-0.5z^{-1}}-\frac{1}{1-0.25z^{-1}}" in question
    assert r"脉冲响应不变法设计，\(T_s=2\)" in question
    assert r"双线性变换法设计，\(T_s=2\)" in question
    assert r"H_{\mathrm{ii}}(s)=\frac{1}{s+\frac{\ln2}{2}}-\frac{\frac12}{s+\ln2}" in answer
    assert r"&=\frac{8(s+1)^2}{(3s+1)(5s+3)}" in answer


def test_2006_minimum_phase_mapping_question_keeps_shared_system_condition(tmp_path: Path):
    from full.tools import build_chapter_06_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-06-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-06-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') >= 6
    assert "2006 年真题（第十一题）" in question
    assert r"H(s)=\sum_{k=1}^{P}\frac{A_k}{s-s_k}" in question
    assert "脉冲响应不变法能否保证最小相位模拟滤波器映射为最小相位数字滤波器？为什么？" in question
    assert r"z=\frac{1+sT/2}{1-sT/2}" in answer
    assert "不能仅由脉冲响应不变法保证" in answer
    assert "z=-1" in answer


def test_2015_ideal_filter_question_has_four_redrawn_magnitude_responses(tmp_path: Path):
    from full.tools import build_chapter_06_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-06-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-06-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') >= 7
    assert "2015 年真题" in question
    assert "画出理想低通、高通、带通、带阻频率滤波器的幅频响应，要求标出截止频率。" in question
    assert 'data-diagram="four-ideal-filter-responses"' in answer
    assert "理想低通" in answer and "理想高通" in answer
    assert "理想带通" in answer and "理想带阻" in answer


def test_2017_bilinear_lowpass_question_keeps_original_wording_and_symbolic_order(tmp_path: Path):
    from full.tools import build_chapter_06_training_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-06-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-06-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') == 8
    assert "2017 年真题" in question
    assert "只要求写出表达式，不用计算" in question
    assert r"\Omega_p\)、\(\Omega_s" in question
    assert "\\Omega=\\frac{2}{T}\\tan" in answer
    assert "N=\\left\\lceil" in answer
    assert r"10^{15/10}-1" in answer
