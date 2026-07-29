"""The only permitted mathematical rendering entry point for the handout.

Complete LaTeX is sent as one unit to MathJax in an HTML page and printed by
Edge.  Callers must never compose braces, symbols or formula fragments in
ReportLab, SVG, Canvas or images.
"""
from __future__ import annotations

import html
import subprocess
from pathlib import Path

EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
MATHJAX = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"


def document(
    latex: str,
    *,
    title: str = "数学公式",
    page_size: str = "A4",
    margin: str = "18mm",
    centered: bool = False,
) -> str:
    """Create a single-formula MathJax page from complete display LaTeX."""
    return f"""<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<script>
window.MathJax = {{
  tex: {{packages: {{'[+]': ['ams']}}}},
  chtml: {{scale: 1}}
}};
</script>
<script defer src="{MATHJAX}"></script>
<style>
@page {{ size: {page_size}; margin: {margin}; }}
body {{ margin: 0; color: #1F2933; }}
.math-display {{
  overflow-x: auto; overflow-y: hidden; max-width: 100%;
  {"display: flex; align-items: center; justify-content: center; height: 100%;" if centered else ""}
}}
</style>
<main class="math-display">
\\[
{latex}
\\]
</main>
</html>"""


def write_html(
    latex: str,
    html_path: Path,
    *,
    title: str = "数学公式",
    page_size: str = "A4",
    margin: str = "18mm",
    centered: bool = False,
) -> Path:
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(
        document(latex, title=title, page_size=page_size, margin=margin, centered=centered),
        encoding="utf-8",
    )
    return html_path


def render_pdf(
    latex: str,
    output_path: Path,
    *,
    title: str = "数学公式",
    wait_ms: int = 8000,
    page_size: str = "A4",
    margin: str = "18mm",
    centered: bool = False,
) -> Path:
    """Render one complete MathJax formula to PDF through the browser engine."""
    if not EDGE.exists():
        raise FileNotFoundError(f"Microsoft Edge is required: {EDGE}")
    output_path = output_path.resolve()
    html_path = output_path.with_suffix(".html")
    write_html(latex, html_path, title=title, page_size=page_size, margin=margin, centered=centered)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(EDGE), "--headless=new", "--disable-gpu", "--no-first-run", "--no-pdf-header-footer",
            f"--virtual-time-budget={wait_ms}", f"--print-to-pdf={output_path}",
            html_path.as_uri(),
        ],
        check=True,
    )
    return output_path


def render_fragment_pdf(
    latex: str,
    output_path: Path,
    *,
    width_pt: int,
    height_pt: int,
    title: str = "数学公式",
) -> Path:
    """Render a tight vector PDF fragment for placement in a PDF page."""
    return render_pdf(
        latex,
        output_path,
        title=title,
        page_size=f"{width_pt}pt {height_pt}pt",
        margin="0",
        centered=True,
    )
