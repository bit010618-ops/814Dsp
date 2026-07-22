from pathlib import Path
import subprocess
import sys

from pypdf import PdfReader

from full.tools.build_chapter_01_handout import _body_bounds, build_pdf, load_component_paths


ROOT = Path(__file__).resolve().parents[2]


def test_chapter_one_handout_reflows_all_component_inputs_without_source_identity(tmp_path: Path):
    component_paths = load_component_paths(ROOT)
    assert len(component_paths) == 17
    assert component_paths[0].name == "chapter_01_opening_component.pdf"
    assert component_paths[-1].name == "chapter_01_applications_close_component.pdf"

    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_handout.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    assert len(reader.pages) < 62
    assert "第一章 离散时间信号与系统" in text
    assert "连续时间信号的抽样" in text
    assert "透过现象看本质" in text
    for forbidden in ("源课件", "源文件", "原始材料", "根据原课件"):
        assert forbidden not in text
    assert all(round(float(page.mediabox.width)) == 595 for page in reader.pages)
    assert all(round(float(page.mediabox.height)) == 842 for page in reader.pages)


def test_chapter_one_handout_builder_runs_as_a_script():
    result = subprocess.run(
        [sys.executable, "full/tools/build_chapter_01_handout.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "chapter_01_handout.pdf" in result.stdout


def test_reflow_crop_keeps_a_safe_upper_margin_for_section_titles():
    source_page = PdfReader(str(ROOT / "full/outputs/chapter_01_origin_component.pdf")).pages[0]
    _bottom, top = _body_bounds(source_page)

    assert top >= 795
