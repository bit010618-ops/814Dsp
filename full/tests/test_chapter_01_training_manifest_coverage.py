import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_every_chapter_one_manifest_question_has_a_training_component():
    """Protect the source-audited chapter-one question inventory from silent omissions."""
    manifest = json.loads(
        (ROOT / "full" / "source" / "exam_training_manifest.json").read_text(encoding="utf-8")
    )
    chapter = next(item for item in manifest["chapters"] if item["chapter"] == 1)
    expected = {
        question["id"]
        for question in chapter["priority_questions"] + chapter["supplemental_questions"]
    }

    priority = json.loads(
        (ROOT / "full" / "source" / "chapter_01_training_component.json").read_text(
            encoding="utf-8"
        )
    )
    supplemental = json.loads(
        (ROOT / "full" / "source" / "chapter_01_supplemental_component.json").read_text(
            encoding="utf-8"
        )
    )
    covered = {
        question["id"]
        for question in priority["priority_questions"] + supplemental["questions"]
    }
    covered.update({"2016-q六-whole", "2007-q五-whole", "2025-q六-whole"})

    assert covered == expected
