from __future__ import annotations

import json
from pathlib import Path


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_exam_bank(root: Path) -> dict:
    candidates = _read_json(root / "full" / "artifacts" / "exam_question_candidates.json")
    candidate_by_id = {item["id"]: item for item in candidates}
    review_paths = sorted((root / "full" / "source").glob("exam_question_review_*.json"))
    chapters = {number: [] for number in range(1, 9)}
    out_of_scope_candidate_ids = []
    reviewed_ids = set()

    for path in review_paths:
        review = _read_json(path)
        if review["review_status"] != "manual_dependency_review_complete":
            raise ValueError(f"unfinished review: {path.name}")
        for decision in review["candidate_reviews"]:
            candidate_id = decision["candidate_id"]
            candidate = candidate_by_id[candidate_id]
            if candidate_id in reviewed_ids:
                raise ValueError(f"duplicate manual review: {candidate_id}")
            reviewed_ids.add(candidate_id)
            if decision["decision"] == "out_of_scope":
                out_of_scope_candidate_ids.append(candidate_id)
                continue
            figure_handling = decision.get("source_figure_handling")
            for part in decision["included_parts"]:
                chapter = part["placement_chapter"]
                chapters[chapter].append(
                    {
                        "id": part["id"],
                        "year": review["year"],
                        "source_candidate_id": candidate_id,
                        "source_pages": candidate["source_pages"],
                        "source_section_ids": candidate["source_section_ids"],
                        "source_locator": part["source_locator"],
                        "required_chapters": part["required_chapters"],
                        "placement_chapter": chapter,
                        "split_mode": decision["decision"],
                        "source_figure_handling": figure_handling,
                    }
                )

    missing = set(candidate_by_id) - reviewed_ids
    if missing:
        raise ValueError(f"unreviewed source candidates: {sorted(missing)}")
    return {
        "schema_version": 1,
        "source": "manual exam question reviews",
        "chapters": [
            {"chapter": number, "questions": chapters[number]}
            for number in range(1, 9)
        ],
        "out_of_scope_candidate_ids": sorted(out_of_scope_candidate_ids),
    }


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    output = root / "full" / "source" / "exam_question_bank.json"
    output.write_text(
        json.dumps(build_exam_bank(root), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
