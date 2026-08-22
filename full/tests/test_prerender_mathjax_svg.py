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
    assert r'\begin{cases}' not in rendered
    assert 'data-mathjax-static="true"' in rendered
