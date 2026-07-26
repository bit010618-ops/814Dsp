from pathlib import Path

from pypdf import PdfReader

from full.tools.build_chapter_01_sampling_engineering_component import build_pdf, load_model


def test_sampling_engineering_component_keeps_core_and_excludes_audio_example(tmp_path: Path):
    model = load_model()
    assert model["source_pages"] == [151, 152, 153, 156, 157, 158]
    assert model["excluded_by_user_scope"][0]["source_pages"] == [154, 155]
    output = build_pdf(output_path=tmp_path / "sampling-engineering.pdf")
    reader = PdfReader(str(output))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) == 4
    assert "抗混叠滤波的频域作用" in (reader.pages[0].extract_text() or "")
    assert "频谱副本的分离" in (reader.pages[0].extract_text() or "")
    assert "带通信号的采样参数" in (reader.pages[1].extract_text() or "")
    assert "带通信号的无混叠采样" in (reader.pages[2].extract_text() or "")
    assert "音频" not in text
    assert "源课件" not in text
    assert "源文件" not in text
