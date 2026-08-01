from pathlib import Path
import re


def test_batch_four_preserves_2013_source_prompts_and_mathjax(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_four_mathjax_component as batch

    html = batch.write_html(tmp_path / "batch-four.html").read_text(encoding="utf-8")
    assert "五、某离散系统如图所示：" in html
    assert r"（1）求出系统函数 \(H(z)\)，并求出收敛域；" in html
    assert "（3）写出一个满足稳定、非因果的单位脉冲响应函数。" in html
    assert r"八、离散因果 LTI 系统的系统函数 \(H(z)\) 的零极点图如图所示，其中 \(h[0]=2\)" in html
    assert "（4）求出系统的差分方程。" in html
    assert r"\frac{1}{1-\frac{5}{2}z^{-1}+z^{-2}}" in html
    assert r"H(z)=\frac{2}{1-2z^{-1}}" in html
    assert 'aria-label="2013 年第五题的离散系统结构图"' in html
    assert 'aria-label="2013 年第八题的零极点图"' in html
    assert 'stroke="#174b73"' in html
    assert 'fill="#0f8b8d"' in html
    assert 'd="M617 165V235H515"' in html
    # Each feedback branch must use its own gain block and its own input port
    # on the summing node; neither may merge into x[n] before the node.
    assert 'd="M435 235H390"' in html
    assert 'd="M390 235H150V142H180"' in html
    assert 'd="M742 165V310H515"' in html
    assert 'd="M435 310H390"' in html
    assert 'd="M390 310H205V152"' in html


def test_batch_four_feedback_branches_use_separate_gain_blocks_and_summer_ports(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_four_mathjax_component as batch

    html = batch.write_html(tmp_path / "batch-four.html").read_text(encoding="utf-8")
    assert 'data-role="feedback-first-gain"' in html
    assert 'data-role="feedback-second-gain"' in html
    assert 'data-role="feedback-first-output" fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-b4-v2-feedback)"' in html
    assert 'data-role="feedback-second-output" fill="none" stroke="#0f8b8d" stroke-width="2" marker-end="url(#arrow-b4-v2-feedback)"' in html
    assert 'data-role="feedback-first-return"' in html
    assert 'data-role="feedback-second-return"' in html
    assert 'data-port="lower-left"' in html
    assert 'data-port="bottom"' in html
    first_return = re.search(r'<path(?=[^>]*data-role="feedback-first-return")[^>]*>', html).group(0)
    second_return = re.search(r'<path(?=[^>]*data-role="feedback-second-return")[^>]*>', html).group(0)
    assert 'marker-end' not in first_return
    assert 'marker-end' not in second_return


def test_batch_four_browser_dom_has_no_raw_math_delimiters(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_four_mathjax_component as batch
    from full.tools.build_chapter_02_mathjax_handout import assert_mathjax_ready

    dom = batch.rendered_dom(batch.write_html(tmp_path / "batch-four.html"))
    assert_mathjax_ready(dom)
