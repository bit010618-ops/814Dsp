from __future__ import annotations

import json
import re
from pathlib import Path


QUESTION_HEADING = re.compile(r"(?m)^\s*([一二三四五六七八九十]+)\s*[、.．]")


def build_question_section_index(page_records: list[dict], review_records: list[dict]) -> list[dict]:
    review_by_id = {item["id"]: item for item in review_records}
    sections: list[dict] = []
    for page in page_records:
        review = review_by_id.get(page["id"])
        if review is None or review["scope_status"] != "assigned":
            continue
        sections.extend(split_question_sections(page))
    return sections


def write_question_section_index(
    page_index_path: Path, review_index_path: Path, output_path: Path
) -> list[dict]:
    pages = json.loads(page_index_path.read_text(encoding="utf-8"))
    review = json.loads(review_index_path.read_text(encoding="utf-8"))
    sections = build_question_section_index(pages, review)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(sections, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return sections


def split_question_sections(record: dict) -> list[dict]:
    text = record["text"].strip()
    matches = list(QUESTION_HEADING.finditer(text))
    boundaries = [match.start() for match in matches] + [len(text)]
    sections: list[dict] = []

    if matches and text[: matches[0].start()].strip():
        sections.append(
            _section(
                record=record,
                identifier="continuation-01",
                label=None,
                kind="continuation",
                text=text[: matches[0].start()].strip(),
            )
        )

    for index, match in enumerate(matches):
        label = match.group(1)
        sections.append(
            _section(
                record=record,
                identifier=f"q{label}",
                label=label,
                kind="question_start",
                text=text[boundaries[index] : boundaries[index + 1]].strip(),
            )
        )

    if not matches and text:
        sections.append(
            _section(
                record=record,
                identifier="continuation-01",
                label=None,
                kind="continuation",
                text=text,
            )
        )
    return sections


def _section(*, record: dict, identifier: str, label: str | None, kind: str, text: str) -> dict:
    return {
        "id": f"{record['id']}-{identifier}",
        "year": record["year"],
        "source_pages": [record["source_page"]],
        "source_label": label,
        "section_kind": kind,
        "text": text,
        "review_status": "pending_dependency_review",
    }
