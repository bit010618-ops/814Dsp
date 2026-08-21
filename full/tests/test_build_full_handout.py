from pathlib import Path


def test_full_handout_orders_body_training_then_answers(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    training = html.index('<section class="training-section">')
    answers = html.index('<section class="answer-section">')

    assert html.count('class="chapter-start"') == 8
    assert html.rindex('class="chapter-start"') < training < answers


def test_full_handout_uses_only_pending_page_references(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    assert "详解见 P.____" in html
    assert "详解见 P.59" not in html
    assert "详解见 P.18" not in html
