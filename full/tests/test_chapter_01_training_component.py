from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_training_component import build_answers_pdf, build_training_pdf, load_model


ROOT = Path(__file__).resolve().parents[2]


def test_chapter_one_priority_training_and_detailed_answers_are_clean_and_complete(tmp_path: Path):
    model = load_model(ROOT)
    assert [item["id"] for item in model["priority_questions"]] == [
        "2002-q七-whole",
        "2006-q七-whole",
        "2019-q二-whole",
    ]

    training = build_training_pdf(ROOT, output_path=tmp_path / "chapter_01_training.pdf")
    answers = build_answers_pdf(ROOT, output_path=tmp_path / "chapter_01_answers.pdf")
    training_text = "\n".join(page.extract_text() or "" for page in PdfReader(str(training)).pages)
    answer_text = "\n".join(page.extract_text() or "" for page in PdfReader(str(answers)).pages)
    answer_compact = "".join(answer_text.split())

    assert len(PdfReader(str(training)).pages) == 3
    assert len(PdfReader(str(answers)).pages) == 3
    assert "2002 年真题" in training_text
    assert "2006 年真题" in training_text
    assert "2019 年真题" in training_text
    assert "详解：真题整理详解" in training_text
    assert "最大抽样间隔" in answer_compact
    assert "传递函数" in answer_compact
    assert "卷积结果" in answer_compact
    for text in (training_text, answer_text):
        for forbidden in ("源课件", "源文件", "原始材料", "根据原课件"):
            assert forbidden not in text


def test_training_diagrams_use_rendered_math_for_subscripts_and_delays():
    source = (ROOT / "full" / "tools" / "build_chapter_01_training_component.py").read_text(encoding="utf-8")
    assert 'r"z^{-1}"' in source
    assert 'r"f_1(n)"' in source
    assert 'r"f_2(n)"' in source
    assert "z⁻¹" not in source
    assert "f₁(n)" not in source
    assert "f₂(n)" not in source
