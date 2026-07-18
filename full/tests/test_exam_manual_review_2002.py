import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_2002_manual_review_accounts_for_every_source_candidate_and_keeps_placement_valid():
    candidates = json.loads(
        (ROOT / "full" / "artifacts" / "exam_question_candidates.json").read_text(encoding="utf-8")
    )
    review = json.loads(
        (ROOT / "full" / "source" / "exam_question_review_2002.json").read_text(encoding="utf-8")
    )
    candidate_ids = {item["id"] for item in candidates if item["year"] == 2002}

    assert review["year"] == 2002
    assert {item["candidate_id"] for item in review["candidate_reviews"]} == candidate_ids
    for candidate in review["candidate_reviews"]:
        for part in candidate.get("included_parts", []):
            assert part["placement_chapter"] == max(part["required_chapters"])


def test_2002_independent_fill_blanks_are_split_but_linked_sampling_question_is_whole():
    review = json.loads(
        (ROOT / "full" / "source" / "exam_question_review_2002.json").read_text(encoding="utf-8")
    )
    by_candidate = {item["candidate_id"]: item for item in review["candidate_reviews"]}

    assert by_candidate["2002-qintro-01"]["decision"] == "split_independent_parts"
    assert {
        item["placement_chapter"] for item in by_candidate["2002-qintro-01"]["included_parts"]
    } == {1, 2}
    assert by_candidate["2002-q七-01"]["decision"] == "whole_question"
