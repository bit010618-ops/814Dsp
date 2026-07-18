from pathlib import Path
import sys

from reportlab.pdfgen import canvas

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from scan_pdfs import find_incremental_runs, scan_pdf, write_inventory


def test_scan_pdf_reports_page_count_and_extracts_text(tmp_path):
    fixture = tmp_path / "fixture.pdf"
    pdf = canvas.Canvas(str(fixture))
    pdf.drawString(72, 720, "Digital Signal Processing")
    pdf.showPage()
    pdf.drawString(72, 720, "Example solution")
    pdf.save()

    report = scan_pdf(fixture, max_pages=2)

    assert report["page_count"] == 2
    assert report["pages"][0]["text_chars"] > 0
    assert "Digital Signal Processing" in report["pages"][0]["text"]


def test_find_incremental_runs_groups_pages_that_accumulate_text():
    pages = [
        {"index": 10, "text": "definition"},
        {"index": 11, "text": "definition formula"},
        {"index": 12, "text": "definition formula example"},
        {"index": 13, "text": "new topic"},
    ]

    assert find_incremental_runs(pages) == [
        {"start": 10, "end": 12, "final_page": 12}
    ]


def test_write_inventory_records_incremental_runs(tmp_path):
    fixture = tmp_path / "fixture.pdf"
    pdf = canvas.Canvas(str(fixture))
    pdf.drawString(72, 720, "definition")
    pdf.showPage()
    pdf.drawString(72, 720, "definition formula")
    pdf.save()
    output = tmp_path / "inventory.json"

    write_inventory(fixture, output)

    assert output.exists()
    assert '"incremental_runs"' in output.read_text(encoding="utf-8")
