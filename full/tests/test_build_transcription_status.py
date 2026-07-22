import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "full" / "tools"))

from build_transcription_status import build_transcription_status


def test_transcription_status_covers_every_source_page_once_and_forces_low_coverage_pages_to_be_rewritten():
    manifest = build_transcription_status(ROOT)
    chapters = json.loads((ROOT / "full" / "source" / "chapters.json").read_text(encoding="utf-8"))["chapters"]
    coverage = json.loads((ROOT / "full" / "artifacts" / "reference24_current_coverage.json").read_text(encoding="utf-8"))["pages"]

    records = [record for chapter in manifest["chapters"] for record in chapter["pages"]]
    assert [record["source_page"] for record in records] == list(range(1, 1057))
    assert [chapter["chapter"] for chapter in manifest["chapters"]] == [chapter["number"] for chapter in chapters]

    for record, coverage_row in zip(records, coverage):
        assert record["source_page"] == coverage_row["source_page"]
        assert record["reference24_coverage"] == coverage_row["coverage"]
        if coverage_row["coverage"] < 0.30 or coverage_row["status"] != "text-audited":
            assert record["transcription_status"] == "source_direct_rewrite_required"
        else:
            assert record["transcription_status"] == "baseline_reconcile_required"
