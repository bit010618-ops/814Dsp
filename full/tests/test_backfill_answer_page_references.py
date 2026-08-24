from full.tools.backfill_answer_page_references import apply_navigation_page_map, apply_page_map


def test_apply_page_map_replaces_only_linked_training_placeholders():
    html = (
        '<a class="answer-page-ref" href="#answer-001" data-answer-ref="answer-001">详解见 P.____</a>'
        '<span class="page-ref">详解见 P.待回填</span>'
    )

    result = apply_page_map(html, {"answer-001": 415})

    assert "详解见 P.415" in result
    assert "详解见 P.____" not in result
    assert "详解见 P.待回填" in result


def test_apply_navigation_page_map_uses_audited_question_identity_not_row_order():
    html = (
        '<tr data-exam-navigation="true" data-exam-id="second"><td class="page-ref">详解见 P.待回填</td></tr>'
        '<tr data-exam-navigation="true" data-exam-id="first"><td class="page-ref">详解见 P.待回填</td></tr>'
    )

    result = apply_navigation_page_map(
        html,
        {"first": "answer-001", "second": "answer-002"},
        {"answer-001": 415, "answer-002": 417},
    )

    assert result.index("详解见 P.417") < result.index("详解见 P.415")
    assert "P.待回填" not in result
