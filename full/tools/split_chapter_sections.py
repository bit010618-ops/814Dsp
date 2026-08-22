"""Split one complete chapter HTML document into complete H2-section documents."""
from __future__ import annotations

import re
import sys
from pathlib import Path


MAIN_OPEN = "<body><main>"
MAIN_CLOSE = "</main></body></html>"
CHAPTER_OPEN = '<section class="chapter-start">'
H2_START = re.compile(r"(?=<h2(?:\s|>))")


def split_sections(source: str) -> tuple[str, list[str]]:
    """Return a document prefix and one complete chapter document per H2 section."""
    if MAIN_OPEN not in source or not source.endswith(MAIN_CLOSE):
        raise ValueError("expected a complete chapter HTML document")
    prefix, body = source.split(MAIN_OPEN, 1)
    chapter = body[: -len(MAIN_CLOSE)]
    if not chapter.startswith(CHAPTER_OPEN):
        raise ValueError("expected a chapter-start section")

    heading_end = chapter.find("</h1>")
    if heading_end < 0:
        raise ValueError("chapter has no H1 title")
    heading = chapter[: heading_end + len("</h1>")]
    remainder = chapter[heading_end + len("</h1>") :]
    if not remainder.rstrip().endswith("</section>"):
        raise ValueError("chapter-start section is not closed")
    # Remove only the outer chapter-start closing tag. Internal sections remain.
    remainder = remainder.rstrip()[: -len("</section>")]
    positions = [match.start() for match in H2_START.finditer(remainder)]
    if not positions:
        raise ValueError("chapter contains no H2 sections")

    pieces = [remainder[start:end] for start, end in zip(positions, positions[1:] + [len(remainder)])]
    document_prefix = f"{prefix}{MAIN_OPEN}"
    documents = [f"{heading}{piece}</section>{MAIN_CLOSE}" for piece in pieces]
    return document_prefix, documents


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: split_chapter_sections.py INPUT.html OUTPUT_DIR")
    source_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    prefix, sections = split_sections(source_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    for number, section in enumerate(sections, start=1):
        (output_dir / f"section_{number:02d}.html").write_text(prefix + section, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
