from pathlib import Path
def test_2015_spectrum_real_part_prompt_and_answer(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_one_mathjax_component as c
    html=c.write_html(tmp_path/"batch.html").read_text(encoding="utf-8")
    assert "2015 年真题" in html
    assert r"由 \(x(n)\) 求出" in html
    assert r"x_{\mathrm{cs}}[n]=\frac{1}{2}\left(x[n]+x^*[-n]\right)" in html
def test_2015_spectrum_real_part_is_mathjax_rendered(tmp_path: Path):
    from full.tools import build_chapter_02_supplemental_training_batch_twenty_one_mathjax_component as c
    dom=c.rendered_dom(c.write_html(tmp_path/"batch.html"))
    assert "<mjx-container" in dom
    assert r"\(" not in dom
