"""Backfill printed answer pages from internal PDF answer anchors."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Mapping


_LINKED_REFERENCE = re.compile(
    r'(?P<prefix><a class="answer-page-ref" href="#(?P<anchor>answer-\d{3})" '
    r'data-answer-ref="(?P<reference>answer-\d{3})">)'
    r'详解见 P\.____(?P<suffix></a>)'
)

_NAVIGATION_PAGE_REFERENCE = re.compile(
    r'(?P<prefix><tr\b(?=[^>]*\bdata-exam-navigation="true")'
    r'(?=[^>]*\bdata-exam-id="(?P<exam_id>[^"]+)")[^>]*>.*?'
    r'<td class="page-ref">)详解见 P\.待回填(?P<suffix></td>.*?</tr>)',
    flags=re.DOTALL,
)


def apply_page_map(html_text: str, page_by_answer: Mapping[str, int]) -> str:
    """Replace only linked training placeholders with their printed answer pages."""

    def replace(match: re.Match[str]) -> str:
        anchor = match.group("anchor")
        if anchor != match.group("reference"):
            raise ValueError(f"mismatched answer reference: {match.group(0)}")
        try:
            page = page_by_answer[anchor]
        except KeyError as error:
            raise ValueError(f"missing printed page for {anchor}") from error
        if page < 1:
            raise ValueError(f"invalid printed page for {anchor}: {page}")
        return f'{match.group("prefix")}详解见 P.{page}{match.group("suffix")}'

    result = _LINKED_REFERENCE.sub(replace, html_text)
    if _LINKED_REFERENCE.search(result):
        raise ValueError("a linked training page reference was not backfilled")
    return result


def apply_navigation_page_map(
    html_text: str,
    answer_by_exam_id: Mapping[str, str],
    page_by_answer: Mapping[str, int],
) -> str:
    """Backfill Appendix E pages using audited question IDs, never table-row order."""

    expected_rows = html_text.count('data-exam-navigation="true"')

    def replace(match: re.Match[str]) -> str:
        exam_id = match.group("exam_id")
        try:
            answer_id = answer_by_exam_id[exam_id]
        except KeyError as error:
            raise ValueError(f"missing audited answer target for {exam_id}") from error
        try:
            page = page_by_answer[answer_id]
        except KeyError as error:
            raise ValueError(f"missing printed page for {answer_id}") from error
        if page < 1:
            raise ValueError(f"invalid printed page for {answer_id}: {page}")
        return f'{match.group("prefix")}详解见 P.{page}{match.group("suffix")}'

    result, replacements = _NAVIGATION_PAGE_REFERENCE.subn(replace, html_text)
    if replacements != expected_rows:
        raise ValueError(
            f"backfilled {replacements} appendix navigation rows, expected {expected_rows}"
        )
    return result


def extract_answer_page_map(pdf_path: Path) -> dict[str, int]:
    """Read each answer anchor's 1-based printed target page from a PDF."""
    try:
        import pymupdf
    except ImportError as error:  # pragma: no cover - environment dependency
        raise RuntimeError("PyMuPDF is required to read PDF answer anchors") from error

    document = pymupdf.open(pdf_path)
    pages: dict[str, int] = {}
    try:
        for source_page in document:
            for link in source_page.get_links():
                answer_id = str(link.get("nameddest", ""))
                target = link.get("page", -1)
                if not re.fullmatch(r"answer-\d{3}", answer_id) or not isinstance(target, int):
                    continue
                printed_page = target + 1
                existing = pages.setdefault(answer_id, printed_page)
                if existing != printed_page:
                    raise ValueError(
                        f"contradictory printed pages for {answer_id}: {existing} and {printed_page}"
                    )
    finally:
        document.close()
    if not pages:
        raise ValueError("no answer anchors were found in the PDF")
    return pages


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(
            "usage: backfill_answer_page_references.py INPUT_HTML FIRST_PASS_PDF OUTPUT_HTML"
        )
    source_html = Path(argv[1])
    first_pass_pdf = Path(argv[2])
    output_html = Path(argv[3])
    rendered = apply_page_map(
        source_html.read_text(encoding="utf-8"), extract_answer_page_map(first_pass_pdf)
    )
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(rendered, encoding="utf-8")
    print(output_html)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
