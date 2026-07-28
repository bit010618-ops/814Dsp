from pathlib import Path
import re
from pypdf import PdfReader
from full.tools.build_chapter_01_difference_equation_component import build_pdf, load_model

ROOT = Path(__file__).resolve().parents[2]

def test_difference_equation_component_preserves_core_and_excludes_matlab(tmp_path: Path):
    model=load_model()
    assert model['excluded_by_user_scope'][0]['source_pages']==[132]
    out=build_pdf(output_path=tmp_path/'difference-equation.pdf')
    text='\n'.join(page.extract_text() or '' for page in PdfReader(str(out)).pages)
    assert len(PdfReader(str(out)).pages)==3
    assert 'MATLAB' not in text


def test_difference_equation_component_continues_causal_iteration_into_first_page(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'difference-equation.pdf')
    reader = PdfReader(str(out))

    assert '迭代法：因果单位脉冲响应' in (reader.pages[0].extract_text() or '')


def test_difference_equation_component_uses_remaining_first_page_space_for_noncausal_lead_in(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'difference-equation.pdf')
    reader = PdfReader(str(out))

    text = re.sub(r'\s+', '', reader.pages[0].extract_text() or '')
    assert '迭代法：非因果单位脉冲响应' in text
    assert '若改用另一边界条件' in text


def test_difference_equation_component_continues_structure_intro_into_third_page(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'difference-equation.pdf')
    reader = PdfReader(str(out))

    assert '由差分方程得到系统结构' in (reader.pages[2].extract_text() or '')


def test_difference_equation_component_continues_noncausal_intro_into_second_page(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'difference-equation.pdf')
    reader = PdfReader(str(out))

    assert '迭代法：非因果单位脉冲响应' in (reader.pages[1].extract_text() or '')


def test_difference_equation_component_uses_complete_source_structure_slide(tmp_path: Path):
    assert (ROOT / 'full/artifacts/source_pages/chapter_01/difference_equation_feedback_structure.png').exists()
    out = build_pdf(output_path=tmp_path / 'difference-equation.pdf')
    assert len(PdfReader(str(out)).pages[2].images) >= 1
