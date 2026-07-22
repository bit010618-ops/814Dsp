import json
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
