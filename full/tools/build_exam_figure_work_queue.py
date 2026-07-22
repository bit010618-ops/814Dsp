from __future__ import annotations

import json
from pathlib import Path


VERIFICATION = "渲染后逐幅核验：水印消失，且坐标、曲线、公式、单位、标签零丢失。"


def build_exam_figure_work_queue(root: Path) -> dict:
    bank = json.loads(
        (root / "full" / "source" / "exam_question_bank.json").read_text(encoding="utf-8")
    )
    by_candidate: dict[str, dict] = {}
    for chapter in bank["chapters"]:
        for question in chapter["questions"]:
            figure = question["source_figure_handling"]
            if not figure:
                continue
            candidate_id = question["source_candidate_id"]
            item = by_candidate.setdefault(
                candidate_id,
                {
                    "source_candidate_id": candidate_id,
                    "source_pages": question["source_pages"],
                    "question_ids": [],
                    "placement_chapters": [],
                    "watermark_present": figure["watermark_present"],
                    "handout_action": figure["handout_action"],
                    "preserve": figure["preserve"],
                    "verification": VERIFICATION,
                    "status": "pending_redraw_or_repair",
                },
            )
            item["question_ids"].append(question["id"])
            item["placement_chapters"].append(chapter["chapter"])

    return {
        "schema_version": 1,
        "source": "exam question bank manual figure review",
        "items": list(by_candidate.values()),
    }


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    output = root / "full" / "source" / "exam_figure_work_queue.json"
    output.write_text(
        json.dumps(build_exam_figure_work_queue(root), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
