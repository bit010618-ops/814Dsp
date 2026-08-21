from pathlib import Path


def test_full_handout_orders_body_training_then_answers(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    training = html.index('<section class="training-section">')
    answers = html.index('<section class="answer-section">')

    assert html.count('class="chapter-start"') == 8
    assert html.rindex('class="chapter-start"') < training < answers
    assert "第四章 分章强化训练" in html
    assert "2017 年真题" in html
    assert 'data-diagram="dit-radix-2-eight-point-flow"' in html
    assert ".fft-flow img{display:block;width:100%;height:auto" in html
    assert "第五章 分章强化训练" in html
    assert "IIR 滤波器的级联型和并联型结构特点" in html
    assert "第六章 分章强化训练" in html
    assert "时间连续的稳定系统经双线性变换后得到的离散系统仍然是稳定系统" in html
    assert ".exam-page{break-before:page;break-inside:avoid;page-break-inside:avoid;min-height:230mm}" in html


def test_full_handout_uses_only_pending_page_references(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    assert "详解见 P.____" in html
    assert "详解见 P.59" not in html
    assert "详解见 P.18" not in html
