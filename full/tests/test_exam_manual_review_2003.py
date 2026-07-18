import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_2003_manual_review_accounts_for_every_source_candidate_and_keeps_placement_valid():
    candidates = json.loads((ROOT / "full" / "artifacts" / "exam_question_candidates.json").read_text(encoding="utf-8"))
    review = json.loads((ROOT / "full" / "source" / "exam_question_review_2003.json").read_text(encoding="utf-8"))

    assert {item["candidate_id"] for item in review["candidate_reviews"]} == {
        item["id"] for item in candidates if item["year"] == 2003
    }
    for candidate in review["candidate_reviews"]:
        for part in candidate.get("included_parts", []):
            assert part["placement_chapter"] == max(part["required_chapters"])


def test_2003_keeps_dft_spectrum_analysis_whole_and_splits_independent_judgements():
    review = json.loads((ROOT / "full" / "source" / "exam_question_review_2003.json").read_text(encoding="utf-8"))
    by_candidate = {item["candidate_id"]: item for item in review["candidate_reviews"]}

    assert by_candidate["2003-q七-01"]["decision"] == "whole_question"
    assert by_candidate["2003-q七-01"]["included_parts"][0]["placement_chapter"] == 3
    assert by_candidate["2003-q九-01"]["decision"] == "split_independent_parts"
    assert {part["placement_chapter"] for part in by_candidate["2003-q九-01"]["included_parts"]} == {2, 3}
