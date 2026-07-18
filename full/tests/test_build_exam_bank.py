import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "full" / "tools"))

from build_exam_bank import build_exam_bank


def test_exam_bank_covers_every_manually_reviewed_candidate_once():
    bank = build_exam_bank(ROOT)
    candidates = json.loads((ROOT / "full" / "artifacts" / "exam_question_candidates.json").read_text(encoding="utf-8"))
    reviewed = {
        item["source_candidate_id"]
        for chapter in bank["chapters"]
        for item in chapter["questions"]
    } | set(bank["out_of_scope_candidate_ids"])
    assert reviewed == {item["id"] for item in candidates}


def test_exam_bank_uses_latest_required_chapter_and_preserves_source_metadata():
    bank = build_exam_bank(ROOT)
    for chapter in bank["chapters"]:
        for question in chapter["questions"]:
            assert question["placement_chapter"] == chapter["chapter"]
            assert question["placement_chapter"] == max(question["required_chapters"])
            assert question["year"]
            assert question["source_pages"]
            assert question["source_figure_handling"] is None or question["source_figure_handling"]["watermark_present"] is True
