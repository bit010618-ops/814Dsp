from pathlib import Path
import re
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


def test_causal_stable_component_preserves_original_lsi_example_prompts(tmp_path: Path):
    out=build_pdf(output_path=tmp_path/'causal-stable.pdf')
    reader=PdfReader(str(out))
    text=re.sub(r'\s+','', ''.join(page.extract_text() or '' for page in reader.pages))
    assert '例：已知LSI系统的单位脉冲响应' in text
    assert '判断系统的因果性。' in text
    assert '判断系统的稳定性。' in text
    builder_text=Path('full/tools/build_chapter_01_causal_stable_component.py').read_text(encoding='utf-8')
    assert "if t == 'LSI系统的稳定性条件':" in builder_text


def test_causal_stable_component_preserves_original_example_numbering_and_conditions(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'causal-stable.pdf')
    text = re.sub(r'\s+', '', ''.join(page.extract_text() or '' for page in PdfReader(str(out)).pages))

    assert '（1）' in text
    assert '（5）' in text
    assert '项输入的求和' in text
    assert '不满足绝对可和' in text
    # 行内不等式以数学图像绘制，检查生成脚本中的标准公式源。
    builder_text = Path('full/tools/build_chapter_01_causal_stable_component.py').read_text(encoding='utf-8')
    assert r'n\\geq2' in builder_text
    assert r'n\\leq-1' in builder_text
    assert r'n-n_0+1' in builder_text


def test_causal_stable_component_continues_lsi_causality_into_first_page(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'causal-stable.pdf')
    reader = PdfReader(str(out))

    assert 'LSI 系统的因果性条件' in (reader.pages[0].extract_text() or '')


def test_causal_stable_component_carries_complete_lsi_impulse_examples_into_first_page(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'causal-stable.pdf')
    first_page = PdfReader(str(out)).pages[0].extract_text() or ''

    assert '四个单位脉冲响应例' in first_page


def test_causal_stable_component_continues_stability_into_second_page(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'causal-stable.pdf')
    reader = PdfReader(str(out))

    assert '一般系统的稳定性' in (reader.pages[1].extract_text() or '')


def test_causal_stable_component_carries_next_complete_topic_block_into_last_page(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'causal-stable.pdf')
    last_page = re.sub(r'\s+', '', PdfReader(str(out)).pages[-1].extract_text() or '')

    assert '常系数线性差分方程' in last_page
    assert '重要表示方法' in last_page
    assert r'\sum_{k=0}^{N}a_k y(n-k)' in Path('full/tools/build_chapter_01_causal_stable_component.py').read_text(encoding='utf-8')
