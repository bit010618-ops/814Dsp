import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_every_chapter_has_a_valid_representative_exam_selection():
    bank = json.loads((ROOT / "full" / "source" / "exam_question_bank.json").read_text(encoding="utf-8"))
    selection = json.loads((ROOT / "full" / "source" / "exam_drill_selection.json").read_text(encoding="utf-8"))
    by_chapter = {item["chapter"]: {question["id"] for question in item["questions"]} for item in bank["chapters"]}
    assert {item["chapter"] for item in selection["chapters"]} == set(range(1, 9))
    for item in selection["chapters"]:
        assert 1 <= len(item["priority_question_ids"]) <= 3
        assert set(item["priority_question_ids"]) <= by_chapter[item["chapter"]]
