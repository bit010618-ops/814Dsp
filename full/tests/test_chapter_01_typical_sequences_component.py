import sys
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'full/tools'))
from build_chapter_01_typical_sequences_component import build_pdf, load_model
def test_typical_sequences_excludes_matlab_but_keeps_concepts(tmp_path):
    m=load_model(ROOT); assert [x['source_page'] for x in m['excluded_by_user_scope']]==[52,54,56]
    out=build_pdf(ROOT,tmp_path/'a.pdf'); r=PdfReader(str(out)); assert len(r.pages)==4
    text=''.join(p.extract_text() or '' for p in r.pages); assert 'MATLAB' not in text and '复指数序列' in text
