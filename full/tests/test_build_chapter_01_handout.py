from pathlib import Path
import subprocess
import sys

from pypdf import PdfReader

from full.tools.build_chapter_01_handout import (
    BODY_BOTTOM,
    BODY_TOP,
    CROP_TOP,
    _component_page_bounds,
    _body_bounds,
    build_pdf,
    load_component_paths,
)


ROOT = Path(__file__).resolve().parents[2]


def test_chapter_one_handout_reflows_all_component_inputs_without_source_identity(tmp_path: Path):
    component_paths = load_component_paths(ROOT)
    assert len(component_paths) == 21
    assert component_paths[0].name == "chapter_01_opening_component.pdf"
    assert component_paths[2].name == "chapter_01_representation_mathjax_component.pdf"
    assert component_paths[3].name == "chapter_01_operations_mathjax_component.pdf"
    assert component_paths[4].name == "chapter_01_typical_sequences_mathjax_component.pdf"
    assert component_paths[5].name == "chapter_01_periodicity_mathjax_component.pdf"
    assert component_paths[6].name == "chapter_01_linearity_mathjax_component.pdf"
    assert component_paths[7].name == "chapter_01_time_invariance_mathjax_component.pdf"
    assert component_paths[-5].name == "chapter_01_applications_close_component.pdf"
    assert component_paths[-4].name == "chapter_01_training_component.pdf"
    assert component_paths[-3].name == "chapter_01_supplemental_component.pdf"
    assert component_paths[-2].name == "chapter_01_answers_component.pdf"
    assert component_paths[-1].name == "chapter_01_supplemental_answers_component.pdf"

    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_handout.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    # Normal teaching content must flow across former component-page boundaries.
    # Training pages and the final detailed-answer appendix deliberately retain
    # their own printable page boundaries, so page count is not a hard target.
    assert len(reader.pages) < 400
    assert "第一章 离散时间信号与系统" in text
    assert "连续时间信号的抽样" in text
    assert "透过现象看本质" in text
    for forbidden in ("源课件", "源文件", "原始材料", "根据原课件"):
        assert forbidden not in text
    assert "复习提示" not in text
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


def test_reflow_leaves_clearance_below_the_rebuilt_page_header():
    # A reflowed component is aligned to BODY_TOP before the unified header is
    # overlaid.  Keeping this point below 770 pt avoids large section titles
    # touching the header rule around 794 pt.
    assert BODY_TOP <= 770


def test_reflow_crop_keeps_the_last_formula_image_and_its_background_box():
    source_page = PdfReader(str(ROOT / "full/outputs/chapter_01_time_invariance_component.pdf")).pages[0]
    bottom, _top = _body_bounds(source_page)

    # The final displayed formula occupies the box from y=368 to y=416.
    # Text extraction alone sees only the nearby heading and used to crop this box.
    assert bottom <= 368


def test_mathjax_svg_representation_pages_use_vector_geometry_bounds():
    component = ROOT / "full/outputs/chapter_01_representation_mathjax_component.pdf"
    reader = PdfReader(str(component))

    bottom, top = _component_page_bounds(component, reader.pages[2], page_index=2)
    # The third HTML page has real SVG paths and MathJax glyph paths, but no
    # raster XObjects. It must crop at the real vector-content boundary so
    # the following section can naturally continue in the remaining page area.
    assert BODY_BOTTOM < bottom < 350
    assert 760 < top <= CROP_TOP


def test_final_handout_preserves_one_printable_page_per_exam_question(tmp_path: Path):
    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_handout.pdf")
    question_pages = [
        page.extract_text() or ""
        for page in PdfReader(str(output)).pages
        if "详解见 P." in (page.extract_text() or "")
    ]

    assert len(question_pages) == 11
    for text in question_pages:
        years = [year for year in ("2002 年真题", "2003 年真题", "2006 年真题", "2014 年真题", "2015 年真题", "2019 年真题", "2020 年真题") if year in text]
        assert len(years) == 1
