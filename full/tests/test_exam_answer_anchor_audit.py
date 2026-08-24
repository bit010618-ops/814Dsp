import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_chapter_one_anchor_audit_uses_manifest_ids_and_existing_answer_targets():
    audit = json.loads(
        (ROOT / "full/source/exam_answer_anchor_audit.json").read_text(encoding="utf-8")
    )
    manifest = json.loads(
        (ROOT / "full/source/exam_training_manifest.json").read_text(encoding="utf-8")
    )
    chapter_one = manifest["chapters"][0]
    manifest_ids = {
        item["id"]
        for bucket in ("priority_questions", "supplemental_questions")
        for item in chapter_one[bucket]
    }
    mapping = audit["verified_mappings"]

    assert audit["scope"] == "chapter_1"
    assert len(mapping) == 41
    assert set(mapping) == manifest_ids
    assert set(mapping.values()) == {f"answer-{index:03d}" for index in range(1, 42)}

    from full.tools import build_full_handout

    rendered = build_full_handout.write_html(ROOT / "tmp" / "anchor-audit.html").read_text(
        encoding="utf-8"
    )
    rendered_ids = set(re.findall(r'data-answer-id="(answer-\d{3})"', rendered))
    assert set(mapping.values()) <= rendered_ids
