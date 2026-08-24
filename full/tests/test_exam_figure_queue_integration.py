"""Regression coverage for the reviewed source-figure queue."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "full" / "source" / "exam_figure_work_queue.json"


def test_every_reviewed_exam_figure_has_a_printed_handout_figure(tmp_path: Path) -> None:
    """A reviewed figure may not remain an unconnected audit-only record."""
    from full.tools import build_full_handout

    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    handout = build_full_handout.write_html(tmp_path / "handout.html").read_text(
        encoding="utf-8"
    )

    for item in queue["items"]:
        candidate = item["source_candidate_id"]
        assert f'data-source-candidate-id="{candidate}"' in handout
