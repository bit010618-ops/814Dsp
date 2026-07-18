import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_2006_manual_review_accounts_for_every_source_candidate():
    candidates = json.loads((ROOT / "full" / "artifacts" / "exam_question_candidates.json").read_text(encoding="utf-8"))
    review = json.loads((ROOT / "full" / "source" / "exam_question_review_2006.json").read_text(encoding="utf-8"))
    assert {item["candidate_id"] for item in review["candidate_reviews"]} == {
        item["id"] for item in candidates if item["year"] == 2006
    }
    for candidate in review["candidate_reviews"]:
        for part in candidate.get("included_parts", []):
            assert part["placement_chapter"] == max(part["required_chapters"])


def test_2006_splits_iir_mapping_methods_and_keeps_overlap_save_as_a_dft_question():
    review = json.loads((ROOT / "full" / "source" / "exam_question_review_2006.json").read_text(encoding="utf-8"))
    by_candidate = {item["candidate_id"]: item for item in review["candidate_reviews"]}
    assert by_candidate["2006-q十一-01"]["decision"] == "split_independent_parts"
    assert {part["placement_chapter"] for part in by_candidate["2006-q十一-01"]["included_parts"]} == {6}
    assert by_candidate["2006-q十二-01"]["included_parts"][0]["placement_chapter"] == 3
