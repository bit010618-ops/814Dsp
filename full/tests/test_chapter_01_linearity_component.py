from pathlib import Path
import re

from pypdf import PdfReader

from full.tools.build_chapter_01_linearity_component import build_pdf, load_model


def test_linearity_component_preserves_examples_and_excludes_experiment(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [70, 71, 72, 73, 74]
    assert [item["source_page"] for item in model["excluded_by_user_scope"]] == [75]
    output = build_pdf(output_path=tmp_path / "linearity.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    compact_text = re.sub(r"\s+", "", text)
    assert len(reader.pages) == 2
    assert "仿真实验" not in text
    assert "三点中值滤波器" in compact_text
    assert "叠加原理" in text


def test_linearity_component_uses_available_page_space_before_opening_the_next_example_page(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "linearity.pdf")
    reader = PdfReader(str(output))

    assert "\u4f8b\uff1a" in (reader.pages[0].extract_text() or "")
    assert "3\u70b9\u4e2d\u503c\u6ee4\u6ce2\u5668" in (reader.pages[1].extract_text() or "")


def test_linearity_component_carries_first_example_lead_into_definition_page(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "linearity.pdf")
    reader = PdfReader(str(output))
    first = re.sub(r"\s+", "", reader.pages[0].extract_text() or "")
    text = "".join(page.extract_text() or "" for page in reader.pages)

    assert "零输入产生零输出" in first
    assert "复习提示" not in text


def test_linearity_component_reflows_all_three_examples_into_two_full_pages(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "linearity.pdf")
    reader = PdfReader(str(output))
    second = re.sub(r"\s+", "", reader.pages[1].extract_text() or "")

    assert len(reader.pages) == 2
    assert "三点中值滤波器为非线性系统" in second


def test_linearity_component_preserves_original_example_statements(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "linearity.pdf")
    reader = PdfReader(str(output))
    text = re.sub(r"\s+", "", "".join(page.extract_text() or "" for page in reader.pages))
    assert "例：验证下面的系统是否为线性系统：" in text
    assert "例：验证下面的3点中值滤波器是否是线性系统：" in text
    builder_text = Path("full/tools/build_chapter_01_linearity_component.py").read_text(encoding="utf-8")
    assert 'r"y(n)=x^2(n)"' in builder_text
    assert 'r"y(n)=x(-n)"' in builder_text
    assert 'r"y(n)=\\operatorname{Mid}\\{x(k)\\},\\qquad n-1\\leq k\\leq n+1"' in builder_text
    assert 'y = section(page, "例：验证下面的3点中值滤波器是否是线性系统：", y - 4)' in builder_text
