import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "full" / "tools"))

from build_chapter_01_origin_component import build_pdf, load_model


def test_origin_model_covers_each_source_page_once_and_locks_math_notation():
    model = load_model(ROOT)

    assert model["source_pages"] == list(range(2, 9))
    assert model["component_status"] == "rendered_and_visually_verified_for_integration"
    assert r"T=\frac{1}{f_s}" in model["formal_formulae"]
    assert r"f_s\geq 2f_h" in model["formal_formulae"]
    assert model["waveform_comparison"]["labels"] == [
        r"f_s=44100\,\mathrm{Hz}", r"\frac{f_s}{4}", r"\frac{f_s}{8}", r"\frac{f_s}{16}"
    ]
    assert model["coordinate_label_rule"]["horizontal_tick_offset_pt"] == 4
    assert model["waveform_comparison"]["left_label_clearance_pt"] == 24
    assert "学校标识" in model["remove_as_cosmetic"]


def test_origin_component_uses_natural_flow_in_two_editable_a4_pages(tmp_path):
    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_origin_component.pdf")

    reader = PdfReader(str(output))
    assert len(reader.pages) == 2
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "离散时间信号的由来" in text
    assert "不同采样频率下钢琴乐曲的赏析" in text
    assert "离散时间信号的表达" in text
    assert "采样频率" in text


def test_origin_expression_page_carries_the_next_section_heading_before_its_safe_break(tmp_path):
    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_origin_component.pdf")
    page_text = PdfReader(str(output)).pages[1].extract_text() or ""

    assert "离散时间信号的表示方法" in page_text


def test_origin_expression_page_carries_the_next_complete_sequence_representation_lead_in(tmp_path):
    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_origin_component.pdf")
    page_text = PdfReader(str(output)).pages[1].extract_text() or ""
    compact_text = re.sub(r"\s+", "", page_text)

    assert "用数列与函数表示" in page_text
    assert "下划线标出" in compact_text


def test_origin_expression_primary_heading_keeps_clear_of_the_header_rule(tmp_path):
    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_origin_component.pdf")
    positions: list[float] = []

    def collect(text, _cm, tm, _font, _size):
        if "离散时间信号的表达" in text:
            positions.append(float(tm[5]))

    PdfReader(str(output)).pages[1].extract_text(visitor_text=collect)
    assert positions
    assert max(positions) <= 735
