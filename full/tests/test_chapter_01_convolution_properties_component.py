from pathlib import Path
import re
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


def test_convolution_properties_component_preserves_original_support_interval_prompt(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'convolution-properties.pdf')
    text = re.sub(r'\s+', '', ''.join(page.extract_text() or '' for page in PdfReader(str(out)).pages))

    assert '例1：有两个序列' in text
    # 行内 y(n) 以数学图像绘制，文本层仅能可靠提取题干文字。
    assert '问：' in text
    assert '不为零的区间为：' in text


def test_convolution_properties_component_continues_support_interval_into_first_page(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'convolution-properties.pdf')
    reader = PdfReader(str(out))

    assert '有限支持序列的卷积区间' in (reader.pages[0].extract_text() or '')


def test_convolution_properties_component_continues_correlation_into_third_page(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'convolution-properties.pdf')
    reader = PdfReader(str(out))

    assert '实序列的相关：相似度与延时' in (reader.pages[2].extract_text() or '')


def test_convolution_properties_component_continues_delay_example_into_second_page(tmp_path: Path):
    out = build_pdf(output_path=tmp_path / 'convolution-properties.pdf')
    reader = PdfReader(str(out))

    assert '应用例：延时叠加系统' in (reader.pages[1].extract_text() or '')
