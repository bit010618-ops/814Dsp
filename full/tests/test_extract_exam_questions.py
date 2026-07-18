from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import json

from extract_exam_questions import (
    build_question_section_index,
    split_question_sections,
    write_question_section_index,
)


def test_split_question_sections_keeps_page_continuation_and_each_numbered_question():
    sections = split_question_sections(
        {
            "id": "2002-p6",
            "year": 2002,
            "source_page": 6,
            "text": "上页第四题的结尾。\n五、系统题。\n（1）求 H(z)。\n六、采样题。",
        }
    )

    assert sections == [
        {
            "id": "2002-p6-continuation-01",
            "year": 2002,
            "source_pages": [6],
            "source_label": None,
            "section_kind": "continuation",
            "text": "上页第四题的结尾。",
            "review_status": "pending_dependency_review",
        },
        {
            "id": "2002-p6-q五",
            "year": 2002,
            "source_pages": [6],
            "source_label": "五",
            "section_kind": "question_start",
            "text": "五、系统题。\n（1）求 H(z)。",
            "review_status": "pending_dependency_review",
        },
        {
            "id": "2002-p6-q六",
            "year": 2002,
            "source_pages": [6],
            "source_label": "六",
            "section_kind": "question_start",
            "text": "六、采样题。",
            "review_status": "pending_dependency_review",
        },
    ]


def test_build_question_section_index_excludes_confirmed_out_of_scope_pages():
    pages = [
        {"id": "2002-p5", "year": 2002, "source_page": 5, "text": "一、离散题。"},
        {"id": "2002-p6", "year": 2002, "source_page": 6, "text": "二、连续题。"},
    ]
    review = [
        {"id": "2002-p5", "scope_status": "assigned"},
        {"id": "2002-p6", "scope_status": "out_of_scope"},
    ]

    sections = build_question_section_index(pages, review)

    assert [section["id"] for section in sections] == ["2002-p5-q一"]


def test_write_question_section_index_persists_reviewable_source_sections(tmp_path):
    page_index = tmp_path / "pages.json"
    review_index = tmp_path / "review.json"
    output = tmp_path / "sections.json"
    page_index.write_text(
        json.dumps([{"id": "2002-p5", "year": 2002, "source_page": 5, "text": "一、离散题。"}]),
        encoding="utf-8",
    )
    review_index.write_text(
        json.dumps([{"id": "2002-p5", "scope_status": "assigned"}]),
        encoding="utf-8",
    )

    sections = write_question_section_index(page_index, review_index, output)

    assert sections[0]["id"] == "2002-p5-q一"
    assert json.loads(output.read_text(encoding="utf-8"))[0]["review_status"] == "pending_dependency_review"
