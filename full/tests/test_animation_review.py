import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_visual_review_records_a_retain_or_merge_decision_for_every_candidate():
    review_path = ROOT / "full" / "source" / "animation_merge_review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))

    decisions = {
        tuple(item["source_pages"]): item["decision"]
        for item in review["candidates"]
    }

    assert len(decisions) == 18
    assert all(decision in {"retain", "merge"} for decision in decisions.values())
    assert decisions[(142, 143)] == "retain"
    assert decisions[(918, 919)] == "retain"
