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
    assert audited_chapters == [1, 2, 3, 4, 5, 6, 7, 8]
    assert audit["unresolved_question_ids"] == []
    assert len(mapping) == 156
    assert set(mapping) == manifest_ids
    # These choices intentionally target the answer paired with the rendered
    # training page, not a later duplicate legacy answer fragment.
    assert mapping["2025-q八-whole"] == "answer-044"
    assert mapping["2015-q七-whole"] == "answer-042"
    assert mapping["2003-q八-whole"] == "answer-077"
    assert mapping["2003-q九-p2"] == "answer-046"
    assert mapping["2006-q十-whole"] == "answer-066"
    assert mapping["2003-q七-whole"] == "answer-079"
    assert mapping["2007-q九-p4"] == "answer-108"
    assert mapping["2024-dsp-p1"] == "answer-113"

    from full.tools import build_full_handout

    rendered = build_full_handout.write_html(ROOT / "tmp" / "anchor-audit.html").read_text(
        encoding="utf-8"
    )
    rendered_ids = set(re.findall(r'data-answer-id="(answer-\d{3})"', rendered))
    assert set(mapping.values()) <= rendered_ids
