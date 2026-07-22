from pathlib import Path
from pypdf import PdfReader
from full.tools.build_chapter_01_causal_stable_component import build_pdf, load_model

def test_causal_stable_component_preserves_definitions_and_examples(tmp_path: Path):
    model=load_model()
    assert model['source_pages']==[116,117,118,119,120,121,122]
    out=build_pdf(output_path=tmp_path/'causal-stable.pdf')
    reader=PdfReader(str(out))
    text='\n'.join(page.extract_text() or '' for page in reader.pages)
    assert len(reader.pages)==4
    assert len(model['retained_core'])==4
    assert 'MATLAB' not in text
