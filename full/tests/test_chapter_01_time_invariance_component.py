from pathlib import Path
import re

from pypdf import PdfReader

from full.tools.build_chapter_01_time_invariance_component import build_pdf, load_model


def test_time_invariance_component_preserves_core_examples_and_excludes_experiment(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [78, 79, 80, 81, 82]
    assert [item["source_page"] for item in model["excluded_by_user_scope"]] == [83]
    output = build_pdf(output_path=tmp_path / "time-invariance.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 2
    assert "仿真实验" not in text
    assert "滑动平均" in text
    assert "验证下面的系统是否为移不变系统：" in text
    assert "例：验证下面的系统是否为移不变系统：" in (reader.pages[0].extract_text() or "")
    assert "例：验证下面的系统是否为移不变系统：" in (reader.pages[1].extract_text() or "")


def test_time_invariance_component_preserves_original_example_statements(tmp_path: Path):
    output = build_pdf(output_path=tmp_path / "time-invariance.pdf")
    reader = PdfReader(str(output))
    text = re.sub(r"\s+", "", "".join(page.extract_text() or "" for page in reader.pages))
    assert "例：验证下面的系统是否为移不变系统：" in text
    builder_text = Path("full/tools/build_chapter_01_time_invariance_component.py").read_text(encoding="utf-8")
    assert 'r"(1)\\quad y(n)=\\sum_{m=-\\infty}^{n}x(m)"' in builder_text
    assert 'r"(2)\\quad y(n)=\\sum_{m=0}^{n}x(m)"' in builder_text
    assert 'r"y(n)=x(2n)"' in builder_text
