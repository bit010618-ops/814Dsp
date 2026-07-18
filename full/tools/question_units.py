from __future__ import annotations


def plan_question_units(*, question_id: str, parts: list[dict]) -> list[dict]:
    groups: list[tuple[str | None, list[dict]]] = []
    for part in parts:
        group_name = part["dependency_group"]
        if group_name is None:
            groups.append((None, [part]))
            continue
        existing = next((group for group in groups if group[0] == group_name), None)
        if existing is None:
            groups.append((group_name, [part]))
        else:
            existing[1].append(part)

    units = []
    for group_name, group_parts in groups:
        required_chapters = sorted(
            {chapter for part in group_parts for chapter in part["required_chapters"]}
        )
        source_part_ids = [part["id"] for part in group_parts]
        if group_name is None:
            unit_id = f"{question_id}-{source_part_ids[0]}"
            split_mode = "independent_subquestion"
        else:
            unit_id = f"{question_id}-{group_name}"
            split_mode = "linked_whole_question"
        units.append(
            {
                "id": unit_id,
                "split_mode": split_mode,
                "source_part_ids": source_part_ids,
                "required_chapters": required_chapters,
                "placement_chapter": max(required_chapters),
            }
        )
    return units
