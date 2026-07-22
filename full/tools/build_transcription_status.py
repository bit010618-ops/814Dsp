from __future__ import annotations

import json
from pathlib import Path


LOW_COVERAGE_THRESHOLD = 0.30


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_transcription_status(root: Path) -> dict:
    chapters = _read_json(root / "full" / "source" / "chapters.json")["chapters"]
    coverage = _read_json(root / "full" / "artifacts" / "reference24_current_coverage.json")["pages"]
    coverage_by_page = {item["source_page"]: item for item in coverage}
    output_chapters = []

    for chapter in chapters:
        page_records = []
        for source_page in range(chapter["start_page"], chapter["end_page"] + 1):
            row = coverage_by_page[source_page]
            requires_direct_rewrite = (
                row["coverage"] < LOW_COVERAGE_THRESHOLD
                or row["status"] != "text-audited"
            )
            page_records.append(
                {
                    "source_page": source_page,
                    "reference24_coverage": row["coverage"],
                    "source_text_status": row["status"],
                    "transcription_status": (
                        "source_direct_rewrite_required"
                        if requires_direct_rewrite
                        else "baseline_reconcile_required"
                    ),
                    "figure_status": "pending_visual_source_review",
                }
            )
        output_chapters.append(
            {
                "chapter": chapter["number"],
                "title": chapter["title"],
                "source_range": [chapter["start_page"], chapter["end_page"]],
                "pages": page_records,
            }
        )

    return {
        "schema_version": 1,
        "source": "current MOOC source pages and reference24 page-level coverage audit",
        "low_coverage_threshold": LOW_COVERAGE_THRESHOLD,
        "chapters": output_chapters,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    output = root / "full" / "source" / "transcription_status.json"
    output.write_text(
        json.dumps(build_transcription_status(root), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
