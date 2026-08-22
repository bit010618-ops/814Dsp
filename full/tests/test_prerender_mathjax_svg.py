from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NODE = Path(r"C:\Users\HP\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
SCRIPT = ROOT / "full" / "tools" / "prerender_mathjax_svg.js"


def test_prerender_replaces_a_complete_cases_formula_with_mathjax_svg(tmp_path: Path) -> None:
    source = tmp_path / "source.html"
    target = tmp_path / "target.html"
    source.write_text(
        '<html><style>svg{max-width:100%;height:auto}</style><body><div class="formula">\\[\\delta(n)=\\begin{cases}1, & n=0,\\\\ 0, & n\\ne0.\\end{cases}\\]</div></body></html>',
        encoding="utf-8",
    )
    result = subprocess.run(
        [str(NODE), str(SCRIPT), str(source), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    rendered = target.read_text(encoding="utf-8")
    assert '<svg' in rendered
    assert 'class="mathjax-svg"' in rendered
    assert 'svg:not(.mathjax-svg){max-width:100%;height:auto}' in rendered
    assert 'mjx-container{font-size:17.5pt}' in rendered
    assert 'mjx-container[display="true"]{font-size:18pt}' in rendered
    assert 'mjx-container[display="true"] svg.mathjax-svg{max-width:100%;height:auto}' in rendered
    assert r'\begin{cases}' not in rendered
    assert 'data-mathjax-static="true"' in rendered


def test_prerender_converts_static_math_inside_svg_foreign_object_to_a_placed_mathjax_svg(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.html"
    target = tmp_path / "target.html"
    source.write_text(
        '<html><body><svg viewBox="0 0 100 40"><foreignObject x="10" y="5" width="70" height="30"><div xmlns="http://www.w3.org/1999/xhtml">\\(H(e^{j\\omega})\\)</div></foreignObject></svg></body></html>',
        encoding="utf-8",
    )

    result = subprocess.run(
        [str(NODE), str(SCRIPT), str(source), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    rendered = target.read_text(encoding="utf-8")
    assert '<foreignObject' not in rendered
    assert '<svg x="10" y="5" width="70" height="30"' in rendered
    assert 'class="mathjax-svg"' in rendered
    assert 'href="data:image/svg+xml;base64,' not in rendered
    assert 'H(e^{j\\omega})' not in rendered


def test_prerender_copies_matching_svg_rules_into_the_svg_for_static_pdf_engines(tmp_path: Path) -> None:
    source = tmp_path / "source.html"
    target = tmp_path / "target.html"
    source.write_text(
        '<html><head><style>.signal-svg{display:block}.signal-svg .axis{fill:none;stroke:#174b73;stroke-width:2}</style></head><body><svg class="signal-svg" viewBox="0 0 100 40"><path class="axis" d="M0 20H95"/></svg></body></html>',
        encoding="utf-8",
    )

    result = subprocess.run(
        [str(NODE), str(SCRIPT), str(source), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    rendered = target.read_text(encoding="utf-8")
    assert '<svg class="signal-svg" viewBox="0 0 100 40"><style data-static-svg-style="signal-svg">' in rendered
    assert '.signal-svg .axis{fill:none;stroke:#174b73;stroke-width:2}' in rendered


def test_prerender_keeps_static_style_out_of_printed_body_when_document_has_no_head(tmp_path: Path) -> None:
    source = tmp_path / "source.html"
    target = tmp_path / "target.html"
    source.write_text(
        '<!doctype html><html><meta charset="utf-8"><body><p>正文</p></body></html>',
        encoding="utf-8",
    )

    result = subprocess.run(
        [str(NODE), str(SCRIPT), str(source), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    rendered = target.read_text(encoding="utf-8")
    assert rendered.index('data-mathjax-static-style="true"') < rendered.index("<body>")
    assert not rendered.startswith('<style data-mathjax-static-style="true">')


def test_prerender_decodes_html_comparison_entities_inside_latex(tmp_path: Path) -> None:
    source = tmp_path / "source.html"
    target = tmp_path / "target.html"
    source.write_text(
        '<html><body><p>此时 \\(4\\pi&amp;gt;2\\pi\\)，频谱不发生混叠。</p></body></html>',
        encoding="utf-8",
    )

    result = subprocess.run(
        [str(NODE), str(SCRIPT), str(source), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    rendered = target.read_text(encoding="utf-8")
    assert "Misplaced &" not in rendered
    assert '&amp;gt;' not in rendered
    assert 'data-mathjax-static="true"' in rendered
