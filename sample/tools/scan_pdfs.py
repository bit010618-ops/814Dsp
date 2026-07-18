from __future__ import annotations

import argparse
import json
from pathlib import Path

from pypdf import PdfReader


def outline_tree(reader: PdfReader, entries: list | None = None) -> list[dict]:
    nodes = []
    for entry in (reader.outline if entries is None else entries):
        if isinstance(entry, list):
            if nodes:
                nodes[-1]["children"] = outline_tree(reader, entry)
            continue
        try:
            page = reader.get_destination_page_number(entry) + 1
        except Exception:
            page = None
        nodes.append(
            {
                "title": str(entry.get("/Title", "")),
                "page": page,
                "children": [],
            }
        )
    return nodes


def scan_pdf(path: Path, max_pages: int | None = None) -> dict:
    reader = PdfReader(str(path))
    limit = len(reader.pages) if max_pages is None else min(max_pages, len(reader.pages))
    pages = []
    for index in range(limit):
        text = reader.pages[index].extract_text() or ""
        pages.append(
            {
                "index": index + 1,
                "text_chars": len(text),
                "text": text[:1200],
            }
        )
    return {
        "path": str(path),
        "page_count": len(reader.pages),
        "outline": outline_tree(reader),
        "pages": pages,
    }


def find_incremental_runs(pages: list[dict]) -> list[dict]:
    runs = []
    run_start = None
    previous = ""

    for page in pages:
        current = " ".join(page["text"].split())
        if previous and previous in current and len(current) > len(previous):
            if run_start is None:
                run_start = previous_index
        else:
            if run_start is not None:
                runs.append(
                    {
                        "start": run_start,
                        "end": previous_index,
                        "final_page": previous_index,
                    }
                )
            run_start = None
        previous = current
        previous_index = page["index"]

    if run_start is not None:
        runs.append(
            {
                "start": run_start,
                "end": previous_index,
                "final_page": previous_index,
            }
        )
    return runs


def write_inventory(path: Path, output: Path) -> dict:
    inventory = scan_pdf(path)
    inventory["incremental_runs"] = find_incremental_runs(inventory["pages"])
    output.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return inventory


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    inventory = write_inventory(args.pdf, args.output)
    print(
        f"{inventory['page_count']} pages; "
        f"{len(inventory['incremental_runs'])} incremental candidates"
    )


if __name__ == "__main__":
    main()
