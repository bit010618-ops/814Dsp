import json
from pathlib import Path


def test_sample_spec_has_printable_a4_fixed_type_scale_and_headers():
    spec_path = Path(__file__).resolve().parents[1] / "artifacts" / "sample_spec.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    assert spec["page_size"] == "A4"
    assert spec["orientation"] == "portrait"
    assert spec["header_left"] == "数字信号处理讲义"
    assert spec["type_scale"] == {
        "chapter": 19,
        "section": 14,
        "body": 10.5,
        "formula": 11,
        "caption": 9,
    }
    assert spec["margins_mm"]["inner"] > spec["margins_mm"]["outer"]

