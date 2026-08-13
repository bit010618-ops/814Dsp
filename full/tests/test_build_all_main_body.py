from pathlib import Path


def test_full_main_body_assembly_contains_eight_chapters_without_training(tmp_path: Path):
    from full.tools.build_all_main_body import write_html

    html = write_html(tmp_path / "dsp-main-body.html").read_text(encoding="utf-8")

    for heading in (
        "第一章 离散时间信号与系统",
        "z 变换的基本概念",
        "第三章 离散傅里叶变换",
        "4.1 直接计算 DFT 的问题及改进途径",
        "第五章 数字滤波器结构",
        "第六章 IIR 数字滤波器设计",
        "第七章 FIR 数字滤波器设计",
        "第八章 多采样率数字信号处理",
    ):
        assert heading in html
    assert html.count("<main>") == 1
    assert html.count('class="chapter-start"') == 8
    assert html.count("<h1>") == 8
    assert "<h1>第四章 快速傅里叶变换</h1>" in html
    assert "<h2>4.1 直接计算 DFT 的问题及改进途径</h2>" in html
    assert "真题" not in html
    assert "MATLAB" not in html
    assert "page-break-after:always" not in html
    assert ".chart-grid{display:grid" in html
    assert "grid-template-columns:repeat(2,minmax(0,1fr))" in html
    assert ".grid{display:grid" in html
    assert ".mapping th,.mapping td,.table th,.table td{border:.45pt solid" in html
    assert ".source-figure.compact{max-width:156mm}" in html
    assert ".formula mjx-container[display=\"true\"]" in html
    assert ".structure-svg .wire{fill:none;stroke:#174b73" in html
    assert ".structure-svg .block{fill:#f4f7f8;stroke:#0d8794" in html
    assert ".spectrum-svg .replica{fill:none;stroke-width:3" in html
    assert ".chain-svg .chain-box{fill:#f4f7f8;stroke:#b08d57" in html
    assert ".wheel-svg .wheel-rim{fill:none;stroke:#b6342d" in html
    assert ".multirate-svg .spectrum-a{fill:none;stroke:#0d8794" in html
    assert ".multirate-svg .spectrum-b{fill:none;stroke:#b56b2e" in html
    assert ".signal-svg .hold{fill:none;stroke:#0f8b8d;stroke-width:3" in html
    assert "typical-sequence-continuation" in html
    assert ".typical-sequence-continuation .chart{break-inside:auto" in html
    assert ".typical-sequence-continuation .chart svg{max-width:500px!important}" in html
