import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _chapter_two_ids(value):
    if isinstance(value, dict):
        current = {value["id"]} if value.get("placement_chapter") == 2 and "id" in value else set()
        for child in value.values():
            current.update(_chapter_two_ids(child))
        return current
    if isinstance(value, list):
        current = set()
        for child in value:
            current.update(_chapter_two_ids(child))
        return current
    return set()


def test_chapter_two_exam_catalog_covers_every_reviewed_question_with_a_reusable_component():
    expected = _chapter_two_ids(json.loads((ROOT / "full/source/exam_training_manifest.json").read_text(encoding="utf-8")))
    catalog_path = ROOT / "full/source/chapter_02_exam_component_catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))

    assert set(catalog["question_components"]) == expected
    for component in catalog["question_components"].values():
        assert (ROOT / component).is_file()
