import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_2015_manual_review_accounts_for_every_source_candidate():
    candidates = json.loads(
        (ROOT / "full" / "artifacts" / "exam_question_candidates.json").read_text(
            encoding="utf-8"
        )
    )
    review = json.loads(
        (ROOT / "full" / "source" / "exam_question_review_2015.json").read_text(
            encoding="utf-8"
        )
    )
    assert {item["candidate_id"] for item in review["candidate_reviews"]} == {
        item["id"] for item in candidates if item["year"] == 2015
    }
    for candidate in review["candidate_reviews"]:
        for part in candidate.get("included_parts", []):
            assert part["placement_chapter"] == max(part["required_chapters"])


def test_2015_figure_questions_record_watermark_safe_treatment():
    review = json.loads(
        (ROOT / "full" / "source" / "exam_question_review_2015.json").read_text(
            encoding="utf-8"
        )
    )
    by_id = {item["candidate_id"]: item for item in review["candidate_reviews"]}
    for candidate_id in ("2015-q四-01", "2015-q七-01", "2015-q八-01"):
        handling = by_id[candidate_id]["source_figure_handling"]
        assert handling["watermark_present"] is True
        assert handling["handout_action"] in {"redraw", "repair_or_redraw"}
