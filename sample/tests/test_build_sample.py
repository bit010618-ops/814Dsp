import json
import io
from pathlib import Path
import sys

from PIL import Image
from pypdf import PdfReader
from reportlab.pdfgen import canvas

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import build_sample as build_sample_module
from build_sample import build_sample
from build_sample import DISPLAY_FORMULA_SIZE, _rich_atoms, draw_continuation_title, draw_figure, math_asset, register_fonts, validate_formula_source


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


def test_inline_math_uses_a_print_legible_global_height():
    assert getattr(build_sample_module, "INLINE_MATH_DRAWN_HEIGHT", None) == 17.5
    assert getattr(build_sample_module, "INLINE_MATH_BASELINE_OFFSET", None) == -5.5


def test_generated_sample_accepts_a_plain_past_exam_page(tmp_path):
    content = {
        "chapter": "第三章 离散傅里叶变换",
        "pages": [
            {
                "kind": "past_exam",
                "title": "2004 年真题",
                "title_right": "答案见 P.8",
                "plain_question": "设 {{x(t)}} 的最高频率不超过 {{3\\,\\mathrm{Hz}}}。",
            }
        ],
    }
    content_path = tmp_path / "content.json"
    content_path.write_text(json.dumps(content, ensure_ascii=False), encoding="utf-8")
    output = tmp_path / "past-exam.pdf"

    build_sample(content_path, output)

    page_text = PdfReader(str(output)).pages[0].extract_text() or ""
    assert "2004 年真题" in page_text
    assert "答案见 P.8" in page_text
    assert "最高频率" in page_text.replace("\n", "")


def test_figure_supports_a_compact_height_cap():
    figure = Path(__file__).resolve().parents[1] / "source-assets" / "source-spectrum-0528.png"
    register_fonts()
    page = canvas.Canvas(io.BytesIO())

    next_y = draw_figure(
        page,
        str(figure),
        "图 3-1 测试图",
        700,
        max_height=50,
    )
    assert next_y == 616


def test_continuation_title_supports_the_primary_heading_size():
    register_fonts()
    page = canvas.Canvas(io.BytesIO())

    next_y = draw_continuation_title(page, "频谱分析的参数关系", 700, size=18)

    assert next_y == 662


def test_representative_content_flows_the_figure_and_uses_plain_practice_pages():
    content_path = Path(__file__).resolve().parents[1] / "artifacts" / "sample_content.json"
    content = json.loads(content_path.read_text(encoding="utf-8"))
    pages = content["pages"]

    assert len(pages) == 5
    assert pages[0]["kind"] == "overview"
    assert pages[0]["figure_path"]
    assert pages[0]["figure_max_height"] <= 300
    assert pages[0]["continuations"][0]["title"] == "频谱分析的参数关系"
    assert pages[0]["continuations"][0]["title_size"] == 18
    assert pages[1]["title"] == "频谱分析的参数关系（续）"
    assert all(item["kind"] != "figure" for item in pages)
    assert pages[1]["continuations"][0]["title"] == "例题：8 点周期延拓序列的 DFS"
    assert pages[1]["continuations"][2]["note"]
    classroom = next(item for item in pages if item["kind"] == "exercise")
    assert classroom["plain_question"]
    assert "exercise" not in classroom
    past_exam = next(item for item in pages if item["kind"] == "past_exam")
    assert past_exam["title_right"] == "答案见 P.5"


def test_generated_sample_renders_a_continuation_section_on_the_same_page(tmp_path):
    content = {
        "chapter": "第三章 离散傅里叶变换",
        "pages": [
            {
                "kind": "summary",
                "title": "参数关系",
                "body": ["参数正文。"],
                "continuations": [
                    {
                        "title": "例题：同页连续排版",
                        "lead": "例题导语。",
                        "formula": "X_0 = 1",
                        "body": ["例题正文。"],
                        "note": "例题复习提示。",
                    }
                ],
            }
        ],
    }
    content_path = tmp_path / "content.json"
    content_path.write_text(json.dumps(content, ensure_ascii=False), encoding="utf-8")
    output = tmp_path / "continuation.pdf"

    build_sample(content_path, output)

    page_text = PdfReader(str(output)).pages[0].extract_text() or ""
    assert "参数关系" in page_text
    assert "例题：同页连续排版" in page_text
    assert "复习提示" in page_text
