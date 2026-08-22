"""Split the assembled main-body HTML into complete chapter documents."""
from __future__ import annotations

import re
import sys
from pathlib import Path


CHAPTER_START = '<section class="chapter-start">'
MAIN_OPEN = '<body><main>'
MAIN_CLOSE = '</main></body></html>'
LOCAL_IMAGE_SOURCE = re.compile(r'(<img\b[^>]*?\bsrc=")([^"]+)(")', re.IGNORECASE)


def split(source: str) -> tuple[str, list[str]]:
    if MAIN_OPEN not in source or not source.endswith(MAIN_CLOSE):
        raise ValueError("expected a complete main-body HTML document")
    prefix, content = source.split(MAIN_OPEN, 1)
    body = content[: -len(MAIN_CLOSE)]
    chapters = [chunk for chunk in body.split(CHAPTER_START) if chunk.strip()]
    if not chapters:
        raise ValueError("main-body HTML contains no chapter starts")
    return f"{prefix}{MAIN_OPEN}", [f"{CHAPTER_START}{chapter}{MAIN_CLOSE}" for chapter in chapters]


def resolve_local_image_sources(document: str, source_path: Path) -> str:
    """Freeze relative image URLs before moving chapter HTML into a temp directory."""

    def replace(match: re.Match[str]) -> str:
        source = match.group(2)
        if source.startswith(("data:", "file:", "http:", "https:", "#")):
            return match.group(0)
        resolved = (source_path.parent / source).resolve()
        return f'{match.group(1)}{resolved.as_uri()}{match.group(3)}'

    return LOCAL_IMAGE_SOURCE.sub(replace, document)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: split_main_body_chapters.py INPUT.html OUTPUT_DIR")
    source_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    source = resolve_local_image_sources(source_path.read_text(encoding="utf-8"), source_path)
    prefix, chapters = split(source)
    output_dir.mkdir(parents=True, exist_ok=True)
    for number, chapter in enumerate(chapters, start=1):
        (output_dir / f"chapter_{number:02d}.html").write_text(prefix + chapter, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
