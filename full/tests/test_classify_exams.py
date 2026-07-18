from pathlib import Path
import sys

from reportlab.pdfgen import canvas

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from classify_exams import build_exam_page_index, classify_question, write_exam_page_index


def test_classify_dft_prompt_to_chapter_three_with_full_confidence():
    record = classify_question(
        year=2015,
        source_pages=[29],
        text="序列 x(n) 的 N 点 DFT 是 x(n) 的 z 变换在什么位置的等间隔取样？",
    )

    assert record["chapter"] == 3
    assert record["topic"] == "DFT"
    assert record["confidence"] == 1.0
    assert record["manual_review"] is False


def test_ambiguous_dsp_prompt_is_preserved_for_manual_review():
    record = classify_question(year=2025, source_pages=[56], text="DSP 题目")

    assert record["chapter"] is None
    assert record["confidence"] == 0.0
    assert record["manual_review"] is True


def test_cross_chapter_question_is_placed_once_at_its_latest_required_chapter():
    record = classify_question(
        year=2020,
        source_pages=[41],
        text="用基-2 FFT 计算 N 点 DFT，并说明计算量。",
    )

    assert record["required_chapters"] == [3, 4]
    assert record["placement_chapter"] == 4
    assert record["chapter"] == 4


def test_page_index_keeps_every_page_between_paper_start_boundaries():
    pages = [
        {"index": 5, "text": "2002 DFT"},
        {"index": 6, "text": "DFT continuation"},
        {"index": 8, "text": "2003 FFT"},
    ]

    index = build_exam_page_index(pages, {2002: 5, 2003: 8})

    assert [(item["year"], item["source_page"]) for item in index] == [
        (2002, 5),
        (2002, 6),
        (2003, 8),
    ]
    assert index[1]["scope_status"] == "pending_manual_review"


def test_page_index_excludes_answer_pages_after_the_question_section():
    pages = [
        {"index": 5, "text": "2002 DFT"},
        {"index": 60, "text": "2002 answer DFT"},
    ]

    index = build_exam_page_index(pages, {2002: 5}, end_page=59)

    assert [item["source_page"] for item in index] == [5]


def test_write_exam_page_index_reads_full_source_pages(tmp_path):
    fixture = tmp_path / "exam.pdf"
    output = tmp_path / "index.json"
    pdf = canvas.Canvas(str(fixture))
    pdf.drawString(72, 720, "2002 DFT")
    pdf.showPage()
    pdf.drawString(72, 720, "DFT continuation")
    pdf.save()

    records = write_exam_page_index(fixture, output, {2002: 1})

    assert output.exists()
    assert records[1]["text"] == "DFT continuation\n"
