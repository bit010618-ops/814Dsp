import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_2013_manual_review_accounts_for_every_source_candidate():
    candidates = json.loads((ROOT / "full" / "artifacts" / "exam_question_candidates.json").read_text(encoding="utf-8"))
    review = json.loads((ROOT / "full" / "source" / "exam_question_review_2013.json").read_text(encoding="utf-8"))
    assert {item["candidate_id"] for item in review["candidate_reviews"]} == {item["id"] for item in candidates if item["year"] == 2013}
    for candidate in review["candidate_reviews"]:
        for part in candidate.get("included_parts", []):
            assert part["placement_chapter"] == max(part["required_chapters"])


def test_2013_splits_ocr_merged_independent_items_and_places_multirate_whole_in_chapter_8():
    review = json.loads((ROOT / "full" / "source" / "exam_question_review_2013.json").read_text(encoding="utf-8"))
    by_candidate = {item["candidate_id"]: item for item in review["candidate_reviews"]}
    assert by_candidate["2013-qintro-01"]["decision"] == "split_independent_parts"
    assert {part["placement_chapter"] for part in by_candidate["2013-qintro-01"]["included_parts"]} == {1, 2, 3}
    assert by_candidate["2013-q九-01"]["included_parts"][0]["placement_chapter"] == 8
