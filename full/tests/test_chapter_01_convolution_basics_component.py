from pathlib import Path
import re

from pypdf import PdfReader

from full.tools.build_chapter_01_convolution_basics_component import build_pdf, load_model


def test_convolution_basics_component_preserves_core_material_and_excludes_matlab(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [86, 87, 88, 89, 90, 91, 92, 93, 94, 95]
    assert [item["source_page"] for item in model["excluded_by_user_scope"]] == [96]
    output = build_pdf(output_path=tmp_path / "convolution-basics.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 4
    assert "MATLAB" not in text
    assert "线性卷积" in text


def test_convolution_basics_continues_the_graphical_method_heading_on_page_one(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "convolution-basics.pdf")
    reader = PdfReader(str(output))
    assert "图解计算法：反褶、移位、相乘、相加" in (reader.pages[0].extract_text() or "")


def test_convolution_basics_carries_complete_first_two_graphical_steps_into_page_one(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "convolution-basics.pdf")
    first_page = PdfReader(str(output)).pages[0].extract_text() or ""

    assert "1. 反褶" in first_page
    assert "2. 移位" in first_page


def test_convolution_basics_carries_the_complete_input_response_stem_pair_after_the_prompt(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "convolution-basics.pdf")
    reader = PdfReader(str(output))
    page_two = reader.pages[1]
    drawings = page_two.get("/Resources", {}).get("/XObject", {})

    assert "试求该系统的输出响应" in re.sub(r"\s+", "", page_two.extract_text() or "")
    assert len(drawings) >= 6


def test_convolution_basics_preserves_the_original_example_statement_on_page_two(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "convolution-basics.pdf")
    reader = PdfReader(str(output))
    page_text = re.sub(r"\s+", "", reader.pages[1].extract_text() or "")
    assert "已知某LSI系统的单位脉冲响应为：" in page_text
    assert "若该系统的输入为序列：" in page_text
    assert "试求该系统的输出响应。" in page_text
    builder_text = Path("full/tools/build_chapter_01_convolution_basics_component.py").read_text(encoding="utf-8")
    assert 'r"h(n)=3\\delta(n)+2\\delta(n-1)+\\delta(n-2)"' in builder_text
    assert 'r"x(n)=\\delta(n)+2\\delta(n-1)"' in builder_text


def test_convolution_basics_continues_the_impulse_response_solution_on_page_three(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "convolution-basics.pdf")
    reader = PdfReader(str(output))
    assert "详解：由脉冲响应直接求输出" in (reader.pages[2].extract_text() or "")
