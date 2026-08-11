import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_chapter_two_source_pages_are_allocated_once_without_claiming_body_completion(tmp_path: Path):
    from full.tools.build_chapter_02_content_model import build_content_model

    output = tmp_path / "chapter_02_content_model.json"
    model = build_content_model(ROOT, output)
    written = json.loads(output.read_text(encoding="utf-8"))

    assert model == written
    assert model["chapter"]["start_page"] == 186
    assert model["chapter"]["end_page"] == 387
    assert model["generation_contract"]["source_page_allocation_complete"] is True
    assert model["generation_contract"]["content_reconciliation_complete"] is False
    assert model["generation_contract"]["training_and_answers_frozen_until_all_chapter_bodies_are_complete"] is True
    assert [page for unit in model["units"] for page in unit["source_pages"]] == list(range(186, 388))
    assert all("training" not in str(unit).lower() and "answer" not in str(unit).lower() for unit in model["units"])
