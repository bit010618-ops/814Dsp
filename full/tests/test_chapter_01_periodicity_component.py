from pathlib import Path
import re

from pypdf import PdfReader

from full.tools.build_chapter_01_periodicity_component import build_pdf, load_model


def test_periodicity_component_preserves_non_code_source_content(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [59, 60, 61, 62, 63, 64, 65]
    assert [item["source_page"] for item in model["excluded_by_user_scope"]] == [66]
    output = build_pdf(output_path=tmp_path / "periodicity.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 3
    assert "MATLAB" not in text
    assert "源课件" not in text
    assert "源文件" not in text
    assert "周期序列的定义" in text
    assert "调幅序列" in text


def test_periodicity_component_preserves_original_a_b_example_prompt(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "periodicity.pdf")
    text = re.sub(r"\s+", "", "".join(page.extract_text() or "" for page in PdfReader(str(output)).pages))

    assert "例：（1）判断序列" in text
    assert "是否有周期，如果有请计算其周期。" in text
    assert "（A）" in text
    assert "（B）" in text
    implementation = (Path(__file__).resolve().parents[2] / "full/tools/build_chapter_01_periodicity_component.py").read_text(encoding="utf-8")
    assert r"e^{j(\frac{n}{6}-\pi)}" in implementation


def test_periodicity_component_carries_next_complete_criterion_block(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "periodicity.pdf")
    reader = PdfReader(str(output))
    first_page = re.sub(r"\s+", "", reader.pages[0].extract_text() or "")
    all_text = "".join(page.extract_text() or "" for page in reader.pages)

    assert "由频率求基本周期" in first_page
    assert "有理性判据" in first_page
    assert "复习提示" not in all_text
