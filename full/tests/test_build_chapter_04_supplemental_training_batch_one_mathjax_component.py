from pathlib import Path
import json


def test_chapter_four_supplemental_batch_matches_every_missing_manifest_question_id():
    from full.tools import build_chapter_04_supplemental_training_batch_one_mathjax_component as component

    manifest = json.loads(Path("full/source/exam_training_manifest.json").read_text(encoding="utf-8"))
    chapter_four = next(item for item in manifest["chapters"] if item["chapter"] == 4)
    manifest_ids = {
        item["id"]
        for item in chapter_four["priority_questions"] + chapter_four["supplemental_questions"]
    }
    expected = {
        "2024-dsp-p5", "2007-q十一-whole", "2007-q十三-p2", "2015-qintro-p5", "2015-qintro-p6",
        "2017-q六-p4", "2020-qintro-p1", "2020-qintro-p5", "2023-dsp-p5",
    }

    assert set(component.QUESTION_IDS) == expected
    assert set(component.QUESTION_IDS) <= manifest_ids


def test_chapter_four_supplemental_batch_keeps_all_nine_source_checked_questions_and_answers(tmp_path: Path):
    from full.tools import build_chapter_04_supplemental_training_batch_one_mathjax_component as component

    question = component.write_training_html(tmp_path / "chapter-04-supplemental-training.html").read_text(encoding="utf-8")
    answer = component.write_answers_html(tmp_path / "chapter-04-supplemental-answers.html").read_text(encoding="utf-8")

    assert question.count('class="exam-page"') == 9
    assert "十一、请简略推导采用按时间抽取的 2-FFT 算法将 8 点 DFT 计算分解为两个 4 点 DFT 计算的过程，并画出分解后的算法流图。" in question
    assert "（2）如果只能进行一次 256 点数值的 FFT 运算，用什么办法能实现信号 \\(x(n)\\) 的谱分析？" in question
    assert "5.直接计算 \\(N=16\\) 的 DFT，需要进行________次复数乘法，________次复数加法。使用 2FFT 算法，需要________次复数乘法；" in question
    assert "4.实现一个 10000 点的序列与一个 100 点长的 FIR 单位脉冲响应的线性卷积，要求利用重叠相加法并通过 256 点 FFT 和 IFFT 来实现，问至少需要多少次 FFT 和 IFFT？" in question
    assert "1.计算 256 点的按时间抽取基-2FFT，在每一级有________个蝶形运算。" in question
    assert "5.直接计算 \\(N\\) 点 DFT 需要进行________次复数乘法运算。" in question
    assert "5.已知序列 \\(x(n)=(n+1)R_4(n)\\)，利用基 2-DIT-FFT 算法，画出 \\(x(n)\\) 的 8 点离散 FT 的蝶形运算流图，输入序列的值需标在图中。" in question
    assert "5.一个 8000 点的序列与线性时不变滤波器线性卷积，滤波器的单位脉冲响应长度为 50 点，为了利用快速傅里叶变换算法的计算效率，该滤波器用 128 点的 FFT 和 IFFT 实现，如果采用重叠保留法，为了完成滤波运算，需要至少进行多少次 FFT 运算和 IFFT 运算？请写出推算过程。" in question
    assert r"N_{\mathrm{FFT}}=1+K=65" in answer
    assert r"N_{\mathrm{IFFT}}=K=64" in answer
    assert r"N_{\mathrm{FFT}}=1+102=103" in answer
    assert r"N_{\mathrm{IFFT}}=102" in answer
    assert r"\frac{N}{2}=128" in answer
    assert r"N^2" in answer
    assert 'data-diagram="dit-two-four-point-decomposition"' in answer
    assert 'data-diagram="dit-eight-point-values-flow"' in answer
