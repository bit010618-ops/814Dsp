from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_analog_digital_chain_component import build_pdf, load_model, process_chain_layout


def test_process_chain_reserves_clearance_between_final_arrow_and_output_label():
    layout = process_chain_layout()
    assert layout["final_arrow_end"] + layout["label_clearance"] <= layout["output_label_left"]


def test_analog_digital_chain_component_keeps_the_complete_conversion_chain(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [169, 170, 171, 172, 173, 174, 175, 176]
    assert model["reused_direct_rewrite_source_pages"] == [171]
    output = build_pdf(output_path=tmp_path / "analog-digital-chain.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 3
    assert "采样、量化与编码" in (reader.pages[0].extract_text() or "")
    assert "采样间隔与实际恢复" in (reader.pages[2].extract_text() or "")
    assert "源课件" not in text
    assert "源文件" not in text
    assert "根据原课件" not in text
    assert "复习提示" not in text
    assert "让未来的你感谢曾经努力拼搏的自己" not in text


def test_analog_digital_chain_continues_after_recovery_page(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "analog-digital-chain.pdf")
    reader = PdfReader(str(output))
    assert "模拟信号的数字处理链路（续）" in (reader.pages[0].extract_text() or "")
