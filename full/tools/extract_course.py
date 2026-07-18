from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfReader


def normalize(text: str) -> str:
    return " ".join(text.split())


def find_incremental_candidates(pages: list[dict]) -> list[dict]:
    candidates = []
    run: list[int] = []
    previous_text = ""
    previous_page = None
    for page in pages:
        current_text = normalize(page["text"])
        if previous_text and previous_text in current_text and len(current_text) > len(previous_text):
            if not run:
                run = [previous_page]
            run.append(page["source_page"])
        else:
            if len(run) > 1:
                candidates.append(
                    {
                        "source_pages": run,
                        "proposed_final_page": run[-1],
                        "status": "pending_visual_review",
                    }
                )
            run = []
        previous_text = current_text
        previous_page = page["source_page"]
    if len(run) > 1:
        candidates.append(
            {
                "source_pages": run,
                "proposed_final_page": run[-1],
                "status": "pending_visual_review",
            }
        )
    return candidates


def write_chapter_manifest(pdf_path: Path, chapter: dict, output_path: Path) -> dict:
    reader = PdfReader(str(pdf_path))
    pages = [
        {
            "source_page": source_page,
            "text": reader.pages[source_page - 1].extract_text() or "",
            "merge_decision": "retain_pending_review",
        }
        for source_page in range(chapter["start_page"], chapter["end_page"] + 1)
    ]
    manifest = {
        "chapter": chapter,
        "source_page_count": len(pages),
        "pages": pages,
        "incremental_candidates": find_incremental_candidates(pages),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return manifest
