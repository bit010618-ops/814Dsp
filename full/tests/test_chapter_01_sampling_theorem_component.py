from pathlib import Path
from pypdf import PdfReader
from full.tools.build_chapter_01_sampling_theorem_component import build_pdf, load_model
def test_sampling_theorem_component_keeps_animation_audit_and_core(tmp_path: Path):
 model=load_model()
 assert model['merged_pages'][1]['source_pages']==[139,140,141,142,143,144]
 out=build_pdf(output_path=tmp_path/'sampling-theorem.pdf')
 assert len(PdfReader(str(out)).pages)==4
