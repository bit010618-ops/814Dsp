from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_supplemental_component import build_answers_pdf, build_training_pdf, load_model


ROOT = Path(__file__).resolve().parents[2]


def test_chapter_one_sampling_supplemental_questions_and_answers_are_reader_clean(tmp_path: Path):
    model = load_model(ROOT)
    assert [item["id"] for item in model["questions"]] == [
        "2002-qintro-p4",
        "2003-qintro-p4",
        "2003-q二-whole",
        "2003-q六-whole",
        "2002-q八-whole",
        "2014-qintro-p2",
        "2015-qintro-p1",
        "2020-qintro-p4",
    ]

    training = build_training_pdf(ROOT, output_path=tmp_path / "chapter_01_supplemental.pdf")
    answers = build_answers_pdf(ROOT, output_path=tmp_path / "chapter_01_supplemental_answers.pdf")
    training_text = "\n".join(page.extract_text() or "" for page in PdfReader(str(training)).pages)
    answer_text = "\n".join(page.extract_text() or "" for page in PdfReader(str(answers)).pages)
    training_compact = "".join(training_text.split())
    answer_compact = "".join(answer_text.split())

    assert len(PdfReader(str(training)).pages) == 8
    assert len(PdfReader(str(answers)).pages) == 5
    assert "2002年真题" in training_compact
    assert "2003年真题" in training_compact
    assert "单位样值响应" in training_compact
    assert "2015年真题" in training_compact
    assert "2014年真题" in training_compact
    assert "2020年真题" in training_compact
    assert "奈奎斯特" in training_compact
    assert "最高角频率" in answer_compact
    assert "最小采样频率" in answer_compact
    assert "离散时间信号" in answer_compact
    assert "不是时变系统" in answer_compact
    assert "部分分式" in answer_compact
    assert "组合带限信号的抽样频率" in answer_compact
    for text in (training_compact, answer_compact):
        for forbidden in ("源课件", "源文件", "原始材料", "根据原课件"):
            assert forbidden not in text
