from full.tools.backfill_answer_page_references import apply_page_map


def test_apply_page_map_replaces_only_linked_training_placeholders():
    html = (
        '<a class="answer-page-ref" href="#answer-001" data-answer-ref="answer-001">详解见 P.____</a>'
        '<span class="page-ref">详解见 P.待回填</span>'
    )

    result = apply_page_map(html, {"answer-001": 415})

    assert "详解见 P.415" in result
    assert "详解见 P.____" not in result
    assert "详解见 P.待回填" in result
