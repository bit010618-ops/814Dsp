import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_manual_page_review_accounts_for_every_question_section_page():
    source_pages = json.loads(
        (ROOT / "artifacts" / "exam_page_index.json").read_text(encoding="utf-8")
    )
    review = json.loads(
        (ROOT / "source" / "exam_page_review.json").read_text(encoding="utf-8")
    )

    assert {item["id"] for item in review} == {item["id"] for item in source_pages}
    assert all(item["scope_status"] in {"assigned", "out_of_scope"} for item in review)
    assert all(item["manual_reviewed"] is True for item in review)
