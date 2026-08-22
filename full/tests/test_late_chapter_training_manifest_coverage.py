import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _expected_ids(chapter_number: int) -> set[str]:
    manifest = json.loads(
        (ROOT / "full" / "source" / "exam_training_manifest.json").read_text(encoding="utf-8")
    )
    chapter = next(item for item in manifest["chapters"] if item["chapter"] == chapter_number)
    return {
        question["id"]
        for question in chapter["priority_questions"] + chapter["supplemental_questions"]
    }


def test_chapters_five_seven_and_eight_have_exact_manifest_question_coverage():
    from full.tools import build_chapter_05_training_mathjax_component as chapter_five
    from full.tools import build_chapter_07_supplemental_training_mathjax_component as chapter_seven_supplemental
    from full.tools import build_chapter_07_training_mathjax_component as chapter_seven
    from full.tools import build_chapter_08_training_mathjax_component as chapter_eight

    assert set(chapter_five.QUESTION_IDS) == _expected_ids(5)
    assert set(chapter_seven.QUESTION_IDS) | set(
        chapter_seven_supplemental.QUESTION_IDS
    ) == _expected_ids(7)
    assert set(chapter_eight.QUESTION_IDS) == _expected_ids(8)
