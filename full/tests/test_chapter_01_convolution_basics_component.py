from pathlib import Path

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


def test_convolution_basics_continues_the_example_heading_on_page_two(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "convolution-basics.pdf")
    reader = PdfReader(str(output))
    assert "例题：两个有限长序列的线性卷积" in (reader.pages[1].extract_text() or "")


def test_convolution_basics_continues_the_impulse_response_solution_on_page_three(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "convolution-basics.pdf")
    reader = PdfReader(str(output))
    assert "详解：由脉冲响应直接求输出" in (reader.pages[2].extract_text() or "")
