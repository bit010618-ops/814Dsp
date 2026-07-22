from pathlib import Path
from pypdf import PdfReader
from full.tools.build_chapter_01_convolution_properties_component import build_pdf, load_model

def test_convolution_properties_component_preserves_core_and_excludes_matlab(tmp_path: Path):
    model=load_model()
    assert model['excluded_by_user_scope'][0]['source_pages']==[107,108]
    out=build_pdf(output_path=tmp_path/'convolution-properties.pdf')
    text='\n'.join(page.extract_text() or '' for page in PdfReader(str(out)).pages)
    assert len(PdfReader(str(out)).pages)==4
    assert 'MATLAB' not in text
    assert '互相关' in text
