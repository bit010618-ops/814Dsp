from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from question_units import plan_question_units


def test_independent_subquestions_are_split_to_their_own_chapters():
    units = plan_question_units(
        question_id="2020-p41-q1",
        parts=[
            {"id": "a", "required_chapters": [3], "dependency_group": None},
            {"id": "b", "required_chapters": [4], "dependency_group": None},
        ],
    )

    assert units == [
        {
            "id": "2020-p41-q1-a",
            "split_mode": "independent_subquestion",
            "source_part_ids": ["a"],
            "required_chapters": [3],
            "placement_chapter": 3,
        },
        {
            "id": "2020-p41-q1-b",
            "split_mode": "independent_subquestion",
            "source_part_ids": ["b"],
            "required_chapters": [4],
            "placement_chapter": 4,
        },
    ]


def test_linked_subquestions_stay_together_at_the_latest_required_chapter():
    units = plan_question_units(
        question_id="2023-p51-q5",
        parts=[
            {"id": "a", "required_chapters": [3], "dependency_group": "whole"},
            {"id": "b", "required_chapters": [4], "dependency_group": "whole"},
        ],
    )

    assert units == [
        {
            "id": "2023-p51-q5-whole",
            "split_mode": "linked_whole_question",
            "source_part_ids": ["a", "b"],
            "required_chapters": [3, 4],
            "placement_chapter": 4,
        }
    ]
