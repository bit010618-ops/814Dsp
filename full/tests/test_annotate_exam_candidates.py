from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import json

from annotate_exam_candidates import annotate_candidates, write_annotated_candidates


def test_annotate_candidates_preserves_source_and_adds_manual_reviewable_suggestion():
    annotated = annotate_candidates(
        [
            {
                "id": "2020-q一-01",
                "year": 2020,
                "source_pages": [41],
                "text": "用 FFT 计算 DFT。",
            }
        ]
    )

    assert annotated == [
        {
            "id": "2020-q一-01",
            "year": 2020,
            "source_pages": [41],
            "text": "用 FFT 计算 DFT。",
            "auto_classification": {
                "chapter": 4,
                "required_chapters": [3, 4],
                "placement_chapter": 4,
            },
            "review_status": "pending_dependency_review",
        }
    ]


def test_write_annotated_candidates_persists_candidates_for_manual_review(tmp_path):
    source = tmp_path / "candidates.json"
    output = tmp_path / "annotated.json"
    source.write_text(
        json.dumps([{"id": "2020-q一-01", "year": 2020, "source_pages": [41], "text": "DFT"}]),
        encoding="utf-8",
    )

    write_annotated_candidates(source, output)

    assert json.loads(output.read_text(encoding="utf-8"))[0]["auto_classification"]["chapter"] == 3
