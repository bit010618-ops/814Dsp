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


def group_sections_into_question_candidates(sections: list[dict]) -> list[dict]:
    candidates: list[dict] = []
    active_by_year: dict[int, dict] = {}
    counts: dict[tuple[int, str], int] = {}

    for section in sections:
        year = section["year"]
        if section["section_kind"] == "question_start":
            label = section["source_label"]
            active_by_year[year] = _new_candidate(section, f"q{label}", counts)
            candidates.append(active_by_year[year])
        elif year in active_by_year:
            _append_section(active_by_year[year], section)
        else:
            active_by_year[year] = _new_candidate(section, "qintro", counts)
            candidates.append(active_by_year[year])
    return candidates


def write_question_candidates(sections_path: Path, output_path: Path) -> list[dict]:
    sections = json.loads(sections_path.read_text(encoding="utf-8"))
    candidates = group_sections_into_question_candidates(sections)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return candidates


def _new_candidate(section: dict, stem: str, counts: dict[tuple[int, str], int]) -> dict:
    key = (section["year"], stem)
    counts[key] = counts.get(key, 0) + 1
    candidate = {
        "id": f"{section['year']}-{stem}-{counts[key]:02d}",
        "year": section["year"],
        "source_section_ids": [],
        "source_pages": [],
        "source_labels": [],
        "text": "",
        "review_status": "pending_dependency_review",
    }
    _append_section(candidate, section)
    return candidate


def _append_section(candidate: dict, section: dict) -> None:
    candidate["source_section_ids"].append(section["id"])
    for page in section["source_pages"]:
        if page not in candidate["source_pages"]:
            candidate["source_pages"].append(page)
    if section["source_label"] is not None:
        candidate["source_labels"].append(section["source_label"])
    candidate["text"] = "\n\n".join(part for part in [candidate["text"], section["text"]] if part)


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
