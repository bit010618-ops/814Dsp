from pathlib import Path
from pypdf import PdfReader
from full.tools.build_chapter_01_sampling_theorem_component import build_pdf, load_model
def test_sampling_theorem_component_keeps_animation_audit_and_core(tmp_path: Path):
 model=load_model()
 assert model['merged_pages'][1]['source_pages']==[139,140,141,142,143,144]
 out=build_pdf(output_path=tmp_path/'sampling-theorem.pdf')
 reader = PdfReader(str(out))
 assert len(reader.pages)==3
 assert "理想时域采样" in (reader.pages[0].extract_text() or "")
 assert "采样后的频域周期延拓" in (reader.pages[0].extract_text() or "")
 assert "频域示意" in (reader.pages[0].extract_text() or "")


def test_sampling_theorem_component_uses_previous_page_for_the_complete_sampling_parameter_formula(tmp_path: Path):
 builder_text = Path('full/tools/build_chapter_01_sampling_theorem_component.py').read_text(encoding='utf-8')
 assert "start(p,1); y=sec(p,'理想时域采样（续）',746)" in builder_text
 reflow_body = builder_text.split('def p1_reflow', 1)[1].split('def build_pdf', 1)[0]
 assert "x(n)=x_a(nT)" not in reflow_body
