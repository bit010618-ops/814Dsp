import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_audited_chapter_anchor_mapping_uses_manifest_ids_and_existing_answer_targets():
    audit = json.loads(
        (ROOT / "full/source/exam_answer_anchor_audit.json").read_text(encoding="utf-8")
    )
    manifest = json.loads(
        (ROOT / "full/source/exam_training_manifest.json").read_text(encoding="utf-8")
    )
    audited_chapters = audit["audited_chapters"]
    manifest_ids = {
        item["id"]
        for chapter in manifest["chapters"]
        if chapter["chapter"] in audited_chapters
        for bucket in ("priority_questions", "supplemental_questions")
        for item in chapter[bucket]
    }
    mapping = audit["verified_mappings"]

    assert audit["scope"] == "partial_chapter_identity_mapping"
    assert audited_chapters == [1, 4]
    assert len(mapping) == 53
    assert set(mapping) == manifest_ids
    assert set(mapping.values()) == {
        *(f"answer-{index:03d}" for index in range(1, 42)),
        *(f"answer-{index:03d}" for index in range(115, 124)),
    }

    from full.tools import build_full_handout

    rendered = build_full_handout.write_html(ROOT / "tmp" / "anchor-audit.html").read_text(
        encoding="utf-8"
    )
    rendered_ids = set(re.findall(r'data-answer-id="(answer-\d{3})"', rendered))
    assert set(mapping.values()) <= rendered_ids
