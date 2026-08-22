from pathlib import Path
import re


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


def test_full_handout_places_all_styles_in_an_explicit_head_before_the_printed_body(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    assert "<head>" in html
    assert html.index(".appendix{break-before:page}") < html.index("</head>")
    assert html.index("</head>") < html.index("<body>")


def test_full_handout_does_not_duplicate_a_chapter_formula_summary_name_as_a_formula_lead(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    assert not re.search(r'<p class="formula-name">[^<]*</p>\s*<p class="formula-lead">', html)


def test_full_handout_never_uses_an_anonymous_formula_result_label(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    assert "本段推导的结果表达式" not in html
    assert not re.search(r'class="formula-(?:lead|name)">[^<]*(?:计算关系|核心关系)', html)


def test_full_handout_uses_only_pending_page_references(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    assert "详解见 P.____" in html
    assert "详解见 P.59" not in html
    assert "详解见 P.18" not in html


def test_full_handout_places_exam_navigation_before_appendix_f_answers(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    training = html.index('<section class="training-section">')
    navigation = html.index('<section class="appendix appendix-e">')
    answers = html.index('<section class="answer-section">')

    assert training < navigation < answers
    assert "附录 E：华理 814 真题考点导航" in html
    assert '<div class="appendix-f">' in html
    assert "附录 F：华理 814 历年 DSP 真题整理详解" in html
    assert html.count('data-exam-navigation="true"') == 156
    navigation_ids = re.findall(r'data-exam-id="([^"]+)"', html)
    assert len(navigation_ids) == 156
    assert len(set(navigation_ids)) == 156
    assert "第八章" in html


def test_full_handout_gives_every_detailed_answer_heading_a_stable_anchor(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")
    answer_html = html[html.index('<section class="answer-section">'):]
    answer_ids = re.findall(r'data-answer-id="(answer-\d{3})"', answer_html)

    assert len(answer_ids) == 150
    assert answer_ids[0] == "answer-001"
    assert len(set(answer_ids)) == len(answer_ids)
    assert "详解见 P.待回填" in html


def test_full_handout_includes_the_confirmed_appendix_set(tmp_path: Path):
    from full.tools import build_full_handout

    html = build_full_handout.write_html(tmp_path / "full-handout.html").read_text(encoding="utf-8")

    titles = (
        "附录 A：常用公式与变换对速查",
        "附录 B：考研标准答题模板",
        "附录 C：分章综合训练与详细解答",
        "附录 D：考前高频公式与检查表",
        "附录 E：华理 814 真题考点导航",
        "附录 F：华理 814 历年 DSP 真题整理详解",
        "附录 I：全书自测与考场检查",
    )
    positions = [html.index(title) for title in titles]

    assert positions == sorted(positions)
    assert html.count('class="appendix-formula-group"') == 8
    assert html.count('class="appendix-c-question"') == 8
    assert "\x0c" not in html
    assert r"\(\frac{2}{3}f_s\)" in html
    assert '.formula-lead{break-after:avoid' in html
    assert 'class="formula-lead">连续信号的离散采样关系（用于把连续时间信号转为离散序列）：' in html
    assert "系统性质判断模板" in html
    assert "DFT 计算与循环卷积模板" in html
    assert "最后两分钟检查表" in html


def test_full_handout_includes_existing_chapter_one_and_two_supplemental_training_and_answers(
    tmp_path: Path,
):
    from full.tools.build_full_handout import write_html

    html = write_html(tmp_path / "dsp-full-handout.html").read_text(encoding="utf-8")

    # 已有的章末训练不能只停留在独立组件中：它们必须进入最终全书装配。
    assert "2002 年真题：单频正弦信号采样" in html
    assert "2007 年真题：常数序列的 DTFT" in html
    # 第四章补齐 9 道源卷核对题后，所有新增训练和书末详解都必须进入全书装配。
    assert html.count('class="exam-head"') == 153
    assert "2016 年真题：冲激采样与频谱复制" in html
    assert "第三章 补充真题（第一批）" in html
    assert "第三章 补充真题（第二批）" in html
    assert "第三章 补充真题（第三批）" in html
    assert "第三章 补充真题（第四批）" in html
    assert "第三章 补充真题（第五批）" in html
    assert "第三章 补充真题（第六批）" in html
    assert "第三章 补充真题（第七批）" in html
    assert "第三章 补充真题（第八批）" in html
    assert "第三章 补充真题（第九批）" in html
    assert "第三章 补充真题（第十批）" in html
    assert "第三章 补充真题（第十一批）" in html
    assert "第三章 补充真题（第十二批）" in html
    assert "第三章 补充真题（第十三批）" in html
    assert "DFT 为 1024 点的重叠保留法" in html
    assert "第四章 补充真题" in html
    assert "一个 8000 点的序列与线性时不变滤波器线性卷积" in html
    assert 'data-diagram="dit-eight-point-values-flow"' in html
    assert ".fft-flow svg{display:block;width:100%;height:auto" in html
    assert "第七章 分章强化训练" in html
    assert "利用窗函数法设计数字带阻滤波器" in html
    assert "第七章 补充真题" in html
    assert "窗函数的长短和形状对滤波器性能产生什么样的影响" in html
    assert 'data-diagram="frequency-sampling-fir"' in html
    assert "第八章 分章强化训练" in html
    assert "说明时分复用工作原理并举例。" in html
    # 书末详解同样要装配，不能只装题面。
    assert "真题整理详解（续）" in html
