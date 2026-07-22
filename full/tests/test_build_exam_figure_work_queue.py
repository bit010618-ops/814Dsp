import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "full" / "tools"))

from build_exam_figure_work_queue import build_exam_figure_work_queue


def test_figure_work_queue_covers_every_watermarked_exam_figure_without_duplicate_source_work():
    queue = build_exam_figure_work_queue(ROOT)
    bank = json.loads((ROOT / "full" / "source" / "exam_question_bank.json").read_text(encoding="utf-8"))
    expected_questions = {
        question["id"]
        for chapter in bank["chapters"]
        for question in chapter["questions"]
        if question["source_figure_handling"]
    }
    queued_questions = {
        question_id
        for item in queue["items"]
        for question_id in item["question_ids"]
    }

    assert queued_questions == expected_questions
    assert len({item["source_candidate_id"] for item in queue["items"]}) == len(queue["items"])
    for item in queue["items"]:
        assert item["watermark_present"] is True
        assert item["handout_action"] in {"repair", "redraw"}
        assert item["verification"] == "渲染后逐幅核验：水印消失，且坐标、曲线、公式、单位、标签零丢失。"
