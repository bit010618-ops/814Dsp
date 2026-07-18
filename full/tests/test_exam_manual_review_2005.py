import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_2005_manual_review_accounts_for_every_source_candidate():
    candidates = json.loads((ROOT / "full" / "artifacts" / "exam_question_candidates.json").read_text(encoding="utf-8"))
    review = json.loads((ROOT / "full" / "source" / "exam_question_review_2005.json").read_text(encoding="utf-8"))
    assert {item["candidate_id"] for item in review["candidate_reviews"]} == {
        item["id"] for item in candidates if item["year"] == 2005
    }
    for candidate in review["candidate_reviews"]:
        for part in candidate.get("included_parts", []):
            assert part["placement_chapter"] == max(part["required_chapters"])


def test_2005_keeps_linked_discretization_whole_but_splits_independent_iir_design_parts():
    review = json.loads((ROOT / "full" / "source" / "exam_question_review_2005.json").read_text(encoding="utf-8"))
    by_candidate = {item["candidate_id"]: item for item in review["candidate_reviews"]}
    assert by_candidate["2005-q八-01"]["decision"] == "whole_question"
    assert by_candidate["2005-q八-01"]["included_parts"][0]["placement_chapter"] == 6
    assert by_candidate["2005-q十二-01"]["decision"] == "split_independent_parts"
    assert len(by_candidate["2005-q十二-01"]["included_parts"]) == 2
