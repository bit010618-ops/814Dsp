from __future__ import annotations

import json
from pathlib import Path

from classify_exams import classify_question


def annotate_candidates(candidates: list[dict]) -> list[dict]:
    annotated = []
    for candidate in candidates:
        classification = classify_question(
            year=candidate["year"],
            source_pages=candidate["source_pages"],
            text=candidate["text"],
        )
        annotated.append(
            {
                **candidate,
                "auto_classification": {
                    "chapter": classification["chapter"],
                    "required_chapters": classification["required_chapters"],
                    "placement_chapter": classification["placement_chapter"],
                },
                "review_status": "pending_dependency_review",
            }
        )
    return annotated


def write_annotated_candidates(source_path: Path, output_path: Path) -> list[dict]:
    candidates = json.loads(source_path.read_text(encoding="utf-8"))
    annotated = annotate_candidates(candidates)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(annotated, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return annotated
