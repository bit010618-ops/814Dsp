from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PYTHON = Path(r"C:\Users\HP\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe")
SCRIPT = ROOT / "full" / "tools" / "split_main_body_chapters.py"


def test_split_main_body_writes_one_complete_html_document_per_chapter(tmp_path: Path) -> None:
    source = tmp_path / "body.html"
    output = tmp_path / "chapters"
    source.write_text(
        '<html><head><style>body{}</style></head><body><main>'
        '<section class="chapter-start"><h1>第一章</h1><p>甲</p></section>'
        '<section class="chapter-start"><h1>第二章</h1><p>乙</p></section>'
        '</main></body></html>',
        encoding="utf-8",
    )
    result = subprocess.run([str(PYTHON), str(SCRIPT), str(source), str(output)], capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    files = sorted(output.glob("chapter_*.html"))
    assert len(files) == 2
    first = files[0].read_text(encoding="utf-8")
    assert '<style>body{}</style>' in first
    assert '第一章' in first
    assert '第二章' not in first
    assert first.endswith('</main></body></html>')


def test_split_main_body_resolves_relative_figure_urls_from_the_source_document(tmp_path: Path) -> None:
    output_root = tmp_path / "outputs"
    output_root.mkdir()
    figure = tmp_path / "assets" / "figure.png"
    figure.parent.mkdir()
    figure.write_bytes(b"png")
    source = output_root / "body.html"
    output = tmp_path / "chapters"
    source.write_text(
        '<html><head></head><body><main>'
        '<section class="chapter-start"><h1>第一章</h1><img src="../assets/figure.png"></section>'
        '</main></body></html>',
        encoding="utf-8",
    )

    result = subprocess.run([str(PYTHON), str(SCRIPT), str(source), str(output)], capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    assert figure.as_uri() in (output / "chapter_01.html").read_text(encoding="utf-8")
