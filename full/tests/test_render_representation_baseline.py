from pathlib import Path
import subprocess
import sys

from full.tools.render_representation_baseline import write_html


def test_baseline_page_uses_one_mathjax_cases_formula_and_data_driven_stem_svg(tmp_path: Path):
    output = write_html(tmp_path / "representation.html")
    page = output.read_text(encoding="utf-8")

    assert "mathjax@3" in page
    assert r"\begin{cases}" in page
    assert r"\end{cases}" in page
    assert "data-index=\"0\"" in page
    assert "data-index=\"5\"" in page
    assert "marker-end" in page
    assert "<image" not in page
    assert "单位抽样序列" in page
    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in page


def test_baseline_renderer_compiles_without_syntax_warnings():
    module = Path(__file__).parents[1] / "tools" / "render_representation_baseline.py"
    result = subprocess.run(
        [sys.executable, "-W", "error::SyntaxWarning", "-m", "py_compile", str(module)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
