import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_2023_manual_review_accounts_for_every_source_candidate():
    candidates = json.loads((ROOT / "full" / "artifacts" / "exam_question_candidates.json").read_text(encoding="utf-8"))
    review = json.loads((ROOT / "full" / "source" / "exam_question_review_2023.json").read_text(encoding="utf-8"))
    assert {item["candidate_id"] for item in review["candidate_reviews"]} == {item["id"] for item in candidates if item["year"] == 2023}
    for item in review["candidate_reviews"]:
        for part in item.get("included_parts", []):
            assert part["placement_chapter"] == max(part["required_chapters"])
