import json
from pathlib import Path
import sys

from PIL import Image
from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_sample import build_sample
from build_sample import DISPLAY_FORMULA_SIZE, _rich_atoms, math_asset, validate_formula_source


def test_generated_sample_is_a4_and_has_page_numbers(tmp_path):
    content = {
        "chapter": "第三章 离散傅里叶变换",
        "pages": [
            {"kind": "overview", "title": "测试页面", "body": ["正文"]}
            for _ in range(5)
        ],
    }
    content_path = tmp_path / "content.json"
    content_path.write_text(json.dumps(content, ensure_ascii=False), encoding="utf-8")
    output = tmp_path / "sample.pdf"

    build_sample(content_path, output)

    reader = PdfReader(str(output))
    assert len(reader.pages) == 5
    assert round(float(reader.pages[0].mediabox.width)) == 595
    assert round(float(reader.pages[0].mediabox.height)) == 842
    assert "数字信号处理讲义" in (reader.pages[0].extract_text() or "")
    assert "1" in (reader.pages[0].extract_text() or "")


def test_generated_sample_accepts_a_figure_page(tmp_path):
    figure = tmp_path / "figure.png"
    Image.new("RGB", (640, 360), "white").save(figure)
    content = {
        "chapter": "第三章 离散傅里叶变换",
        "pages": [
            {
                "kind": "figure",
                "title": "频域对应图",
                "figure_path": str(figure),
                "caption": "图 3-1 频域对应关系",
            }
        ],
    }
    content_path = tmp_path / "content.json"
    content_path.write_text(json.dumps(content, ensure_ascii=False), encoding="utf-8")
    output = tmp_path / "figure-sample.pdf"

    build_sample(content_path, output)

    page = PdfReader(str(output)).pages[0]
    assert "/XObject" in page["/Resources"]


def test_formula_asset_supports_true_subscripts_and_stacked_fractions(tmp_path):
    asset = math_asset(r"f_s = \frac{1}{T}", tmp_path)

    with Image.open(asset) as image:
        assert image.width > 20
        assert image.height > 10
    assert validate_formula_source(r"f_s = \frac{1}{T}") is None
    assert "solidus" in validate_formula_source("f_s = 1 / T")


def test_inline_math_token_keeps_nested_braces():
    atoms = _rich_atoms("结果为 {{\\tilde{X}_8(k)=1+W_8^{3k}}}。")

    assert atoms == [
        ("text", "结"),
        ("text", "果"),
        ("text", "为"),
        ("text", " "),
        ("math", r"\tilde{X}_8(k)=1+W_8^{3k}"),
        ("text", "。"),
    ]


def test_display_formula_uses_the_global_baseline_size():
    assert DISPLAY_FORMULA_SIZE == 11
