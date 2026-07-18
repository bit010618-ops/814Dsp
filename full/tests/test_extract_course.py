from pathlib import Path
import sys

from reportlab.pdfgen import canvas

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from extract_course import find_incremental_candidates, write_chapter_manifest


def test_incremental_candidate_is_marked_pending_visual_review_not_deleted():
    candidates = find_incremental_candidates(
        [
            {"source_page": 4, "text": "定义"},
            {"source_page": 5, "text": "定义 公式 结论"},
        ]
    )

    assert candidates == [
        {
            "source_pages": [4, 5],
            "proposed_final_page": 5,
            "status": "pending_visual_review",
        }
    ]


def test_write_chapter_manifest_keeps_every_source_page(tmp_path):
    fixture = tmp_path / "course.pdf"
    output = tmp_path / "chapter.json"
    pdf = canvas.Canvas(str(fixture))
    pdf.drawString(72, 720, "definition")
    pdf.showPage()
    pdf.drawString(72, 720, "definition formula")
    pdf.save()

    manifest = write_chapter_manifest(
        fixture,
        {"number": 1, "title": "test", "start_page": 1, "end_page": 2},
        output,
    )

    assert [page["source_page"] for page in manifest["pages"]] == [1, 2]
    assert manifest["incremental_candidates"][0]["status"] == "pending_visual_review"
    assert output.exists()
