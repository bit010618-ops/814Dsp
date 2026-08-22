from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PYTHON = Path(r"C:\Users\HP\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe")
SCRIPT = ROOT / "full" / "tools" / "split_chapter_sections.py"


def test_split_chapter_sections_keeps_title_and_one_h2_section_per_document(tmp_path: Path) -> None:
    source = tmp_path / "chapter.html"
    output = tmp_path / "sections"
    source.write_text(
        '<html><head></head><body><main><section class="chapter-start"><h1>第七章</h1>'
        '<h2>7.1</h2><p>甲</p><h2>7.2</h2><p>乙</p></section></main></body></html>',
        encoding="utf-8",
    )
    result = subprocess.run([str(PYTHON), str(SCRIPT), str(source), str(output)], capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    files = sorted(output.glob("section_*.html"))
    assert len(files) == 2
    assert '第七章' in files[0].read_text(encoding="utf-8")
    assert '7.1' in files[0].read_text(encoding="utf-8")
    assert '7.2' not in files[0].read_text(encoding="utf-8")
    assert '7.2' in files[1].read_text(encoding="utf-8")
    assert files[1].read_text(encoding="utf-8").endswith('</section></main></body></html>')
