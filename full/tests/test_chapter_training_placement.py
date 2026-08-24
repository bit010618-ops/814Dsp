"""Book-level structure for chapter-end exam training and book-end answers."""

from __future__ import annotations


def test_training_is_attached_to_its_own_chapter_and_answers_stay_at_book_end(
    tmp_path,
) -> None:
    """Readers should finish a chapter before meeting that chapter's exam set."""
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "handout.html").read_text(
        encoding="utf-8"
    )

    first_training = html.index("<h1>第一章真题整理</h1>")
    second_chapter = html.index('<section class="chapter-start"><h1>第二章')
    second_training = html.index("<h1>第二章真题整理</h1>")
    third_chapter = html.index('<section class="chapter-start"><h1>第三章')
    final_training = html.index("<h1>第八章真题整理</h1>")
    answers = html.index('<section class="answer-section">')

    assert first_training < second_chapter
    assert second_chapter < second_training < third_chapter
    assert final_training < answers
    assert '<section class="training-section">' not in html
    assert "附录 F：华理 814 历年 DSP 真题整理详解" not in html
    assert "<h1>附录 F：真题整理详解</h1>" in html


def test_legacy_exam_inline_math_is_normalized_before_pdf_render(tmp_path) -> None:
    """Training prose must not leave parenthesized TeX as ordinary text."""
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "handout.html").read_text(
        encoding="utf-8"
    )

    assert r"\(X(e^{j\omega})\)" in html
    assert "(omega_m=\\frac{\\pi}{6})" not in html
    assert r"\(\omega_m=\frac{\pi}{6}\)" in html
