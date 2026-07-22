import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "full" / "tools"))

from build_exam_training_manifest import build_exam_training_manifest


def test_training_manifest_places_every_bank_question_once_and_preserves_priority_selection():
    manifest = build_exam_training_manifest(ROOT)
    bank = json.loads((ROOT / "full" / "source" / "exam_question_bank.json").read_text(encoding="utf-8"))
    selection = json.loads((ROOT / "full" / "source" / "exam_drill_selection.json").read_text(encoding="utf-8"))
    expected_ids = {
        question["id"]
        for chapter in bank["chapters"]
        for question in chapter["questions"]
    }
    selected_by_chapter = {
        item["chapter"]: item["priority_question_ids"]
        for item in selection["chapters"]
    }

    actual_ids = set()
    for chapter in manifest["chapters"]:
        priority = chapter["priority_questions"]
        supplemental = chapter["supplemental_questions"]
        assert [question["id"] for question in priority] == selected_by_chapter[chapter["chapter"]]
        assert not ({question["id"] for question in priority} & {question["id"] for question in supplemental})
        for question in priority + supplemental:
            assert question["answer_page_ref_status"] == "pending_final_pagination"
            assert question["figure_instruction"] == "逐幅检查水印；有水印即去除；遮挡有效信息时修复或重绘，且不得裁掉坐标、曲线、公式、单位或标签。"
            actual_ids.add(question["id"])

    assert actual_ids == expected_ids
    assert sum(
        len(chapter["priority_questions"]) + len(chapter["supplemental_questions"])
        for chapter in manifest["chapters"]
    ) == len(expected_ids)
