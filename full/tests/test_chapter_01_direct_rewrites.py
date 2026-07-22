import json
from pathlib import Path
import sys

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "full" / "tools"))

from build_chapter_01_direct_rewrites import build_pdf, load_model


def test_direct_rewrite_model_preserves_all_low_coverage_source_pages_and_key_content():
    model = load_model(ROOT)

    assert [item["source_page"] for item in model["blocks"]] == [20, 129, 130, 171]
    assert {item["component_status"] for item in model["blocks"]} == {"rendered_and_visually_verified_for_integration"}
    assert model["blocks"][0]["diagram"]["series"] == [[0, 1], [1, 2], [2, 3]]
    assert r"h(n)=a^n u(n)" in model["blocks"][1]["result_formula"]
    assert r"h(n)=-a^n u(-n-1)" in model["blocks"][2]["result_formula"]
    assert model["blocks"][3]["signal_chain"]["blocks"] == [
        "前置预滤波器", "A/D 转换器", "数字信号处理器", "D/A 转换器", "模拟低通滤波器"
    ]


def test_direct_rewrite_pdf_is_editable_output_with_expected_pages(tmp_path):
    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_direct_rewrites.pdf")

    reader = PdfReader(str(output))
    assert len(reader.pages) == 3
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    compact_text = "".join(text.split())
    assert "序列的移位" in text
    assert "impseq" not in text
    assert "因果系统" in text
    assert "非因果系统" in text
    assert "数字信号处理器" in compact_text
