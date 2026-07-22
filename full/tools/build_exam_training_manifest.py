from __future__ import annotations

import json
from pathlib import Path


FIGURE_INSTRUCTION = "逐幅检查水印；有水印即去除；遮挡有效信息时修复或重绘，且不得裁掉坐标、曲线、公式、单位或标签。"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _training_question(question: dict) -> dict:
    return {
        **question,
        "answer_page_ref_status": "pending_final_pagination",
        "figure_instruction": FIGURE_INSTRUCTION,
    }


def build_exam_training_manifest(root: Path) -> dict:
    bank = _read_json(root / "full" / "source" / "exam_question_bank.json")
    selection = _read_json(root / "full" / "source" / "exam_drill_selection.json")
    selected_by_chapter = {
        item["chapter"]: item["priority_question_ids"]
        for item in selection["chapters"]
    }
    chapters = []

    for chapter in bank["chapters"]:
        chapter_number = chapter["chapter"]
        questions_by_id = {question["id"]: question for question in chapter["questions"]}
        priority_ids = selected_by_chapter[chapter_number]
        if not set(priority_ids) <= set(questions_by_id):
            raise ValueError(f"selected question is absent from chapter {chapter_number}")
        priority = [_training_question(questions_by_id[question_id]) for question_id in priority_ids]
        supplemental = [
            _training_question(question)
            for question in chapter["questions"]
            if question["id"] not in set(priority_ids)
        ]
        chapters.append(
            {
                "chapter": chapter_number,
                "priority_questions": priority,
                "supplemental_questions": supplemental,
            }
        )

    return {
        "schema_version": 1,
        "source": "exam question bank plus verified priority selection",
        "answer_section": "真题整理详解",
        "chapters": chapters,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    output = root / "full" / "source" / "exam_training_manifest.json"
    output.write_text(
        json.dumps(build_exam_training_manifest(root), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
