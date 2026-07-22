import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "full" / "tools"))

from build_chapter_01_operations_component import build_pdf, load_model


def test_operations_model_accounts_for_every_source_page_without_duplicate_shift_component():
    model = load_model(ROOT)

    assert model["source_pages"] == [16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    assert model["component_status"] == "rendered_and_visually_verified_for_integration"
    assert model["covered_elsewhere"]["source_page"] == 20
    assert model["covered_elsewhere"]["component_file"] == "full/source/chapter_01_direct_rewrites.json"
    assert r"P_x=\lim_{N\to\infty}\frac{1}{2N+1}\sum_{n=-N}^{N}|x(n)|^2" in model["sections"][4]["formulae"]


def test_operations_component_is_editable_five_page_pdf(tmp_path):
    output = build_pdf(ROOT, output_path=tmp_path / "chapter_01_operations_component.pdf")

    reader = PdfReader(str(output))
    assert len(reader.pages) == 5
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "离散时间信号的基本运算" in text
    assert "移位的应用：回声" in text
    assert "累加和与差分" in text
