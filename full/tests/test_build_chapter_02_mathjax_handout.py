from pathlib import Path


def test_chapter_two_mathjax_handout_uses_one_continuous_document(tmp_path: Path):
    from full.tools import build_chapter_02_mathjax_handout as handout

    html = handout.write_html(tmp_path / "chapter-two.html").read_text(encoding="utf-8")
    assert "tex-mml-chtml.js" in html
    assert "page-break-after:always" not in html
    assert "z 变换的基本概念" in html
    assert "离散时间信号傅里叶变换" in html
    assert "系统函数及其与系统性质的关系" in html
    assert "特殊滤波器的设计" in html
    assert "2015 年真题" in html
    assert "2021 年真题" in html
    assert "2025 年真题" in html
    assert "2002 年真题" in html
    assert "2006 年真题" in html
    assert "已知某离散系统方框图如下：求" in html
    assert r"F(z)=\frac{z^2}{z^2-2z-3}" in html
    assert "以除去 5kHz&lt;F&lt;10kHz 的频率成分" in html
    assert "2013 年真题：理想滤波器幅频响应" in html
    assert "2016 年真题" in html
    assert "二、简答题第 1 小题：说明" in html
    assert r"X(j\Omega)=X(s)\big|_{s=j\Omega}" in html
    assert "2017 年真题" in html
    assert "二、简答题第 1 小题：在信号与系统里面，拉氏变换和" in html
    assert r"z=e^{sT}" in html
    assert "2020 年真题（填空题第 2、3 小题）" in html
    assert "序列实部的傅里叶变换等于傅里叶变换的" in html
    assert r"\left|z\right|=1" in html
    assert "2005 年真题" in html
    assert "<p>一、计算</p>" in html
    assert "4.求" in html
    assert r"F(z)=\frac{z^2}{z^2-2z-3}" in html
    assert r"f[n]=\frac{1}{2}(-1)^n u[n]-\frac{1}{2}3^n u[-n-1]" in html
    assert r"h(n)=\delta(n)-0.98\delta(n-6)" in html
    assert "2013 年第五题／2015 年第四题：某离散系统如图所示：" in html
    assert html.count("七、离散因果 LTI 系统的系统函数") == 2
    assert "八、离散因果 LTI 系统的系统函数" not in html
    assert "第二组·第 5 小题：已知" in html
    assert r"\operatorname{ROC}:\frac13<\left|z\right|<\frac12" in html
    assert "2014 年真题" in html
    assert r"试确定 \(x[n]\) 是否是周期的，实信号，偶信号及有限能量的？" in html
    assert 'aria-label="2014 年真题的 DTFT 幅频图"' in html
    assert 'aria-label="2014 年真题的 DTFT 相频图"' in html
    assert ".plot-pair{break-inside:avoid;display:block" in html
    assert ".plot{display:block;break-inside:avoid" in html
    assert "2003 年真题" in html
    assert "八、已知时域离散线性非移变系统的系统函数" in html
    assert r"H(z)=\frac{1}{(z-a)(z-b)}" in html
    assert "2007 年真题" in html
    assert r"2.若信号\(x(n)=k\)，\(k\)为常数，求其离散时间傅里叶变换；" in html
    assert r"X\!\left(e^{j\omega}\right)=2\pi k\sum_{m=-\infty}^{\infty}\delta\!\left(\omega-2\pi m\right)" in html
    assert "五、某离散 LTI 系统如图所示：" in html
    assert r"H(e^{j\omega})&=\frac{1}{1-\frac{1}{2}e^{-j\omega}}" in html
    assert "2024 年真题" in html
    assert "2.已知某线性移不变系统的系统函数是" in html
    assert r"H(z)=0.18\frac{1-z^{-2}}{1+0.64z^{-2}}" in html
    assert 'aria-label="2024 年第二章真题的零极点图"' in html
    assert 'aria-label="2024 年第二章真题的幅频响应"' in html
    assert "2023 年真题" in html
    assert "八、设某 LSTI 系统的差分方程" in html
    assert r"\left|H(e^{j\omega})\right|=2\left|\sin\omega\right|" in html
    assert 'aria-label="2023 年第八题的相频响应"' in html
    assert "2020 年真题" in html
    assert "四、设 LTI 系统的频率响应为" in html
    assert r"H\!\left(e^{j\frac{\pi}{2}}\right)&=" in html
    assert r"\\&=4\cos\left(\frac{\pi n}{2}\right)" in html
    assert "2022 年真题" in html
    assert "八、一离散时间 LTI 系统流图如下图所示：" in html
    assert r"H(z)=1-z^{-N}=\frac{z^N-1}{z^N}" in html
    assert r"\left|H(e^{j\omega})\right|=2\left|\sin(4\omega)\right|" in html
    assert 'aria-label="2022 年第八题的零极点图"' in html
    assert "九、如果一个因果 LSI 系统的输入输出满足如下差分方程" in html
    assert r"H(z)=\frac{1-a^Nz^{-N}}{1-az^{-1}}" in html
    assert r"h[n]&=a^nu[n]-a^N a^{n-N}u[n-N]" in html
    assert r"\sum_{k=0}^{N-1}a^kz^{-k}" in html
    assert "四、一连续脉冲时间函数表达式为" in html
    assert r"x[n]=u[n]-u[n-7]" in html
    assert r"\left|X(e^{j\omega})\right|=\left|\frac{\sin\left(\frac{7\omega}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}\right|" in html
    assert 'aria-label="2025 年第四题的 DTFT 幅度谱"' in html
    assert r"八、已知某因果稳定的 \(LSI\) 系统" in html
    assert r"h_2[n]=(-1)^nh_1[n]" in html
    assert "七、离散因果 LTI 系统的系统函数" in html
    assert r"H(z)=\frac{2}{1-2z^{-1}}=\frac{2z}{z-2}" in html
    assert 'aria-label="2015 年第七题的零极点图"' in html
    assert "2017 年真题" in html
    assert r"H(z)=\frac{z^{-1}}{1-z^{-1}-z^{-2}}" in html
    assert r"\operatorname{ROC}:\frac{\sqrt5-1}{2}<\left|z\right|<\frac{1+\sqrt5}{2}" in html
    assert 'aria-label="2017 年第十题的零极点图"' in html
    assert 'class="header"' not in html
    assert 'counter(page)' not in html
    assert 'class="running-header"' not in html
    assert "page_style.draw_header(layer, chapter)" in Path(handout.__file__).read_text(encoding="utf-8")
    builder_source = Path(handout.__file__).read_text(encoding="utf-8")
    assert "writer.add_blank_page" in builder_source
    # Browser page content and PDF furniture must be isolated in separate
    # Form XObjects; a broken browser graphics stack must never hide a header.
    assert "_page_as_form_xobject" in builder_source
    assert 'b"q\\n/Source Do\\nQ\\nq\\n/Header Do\\nQ\\n"' in builder_source
    assert 'NameObject("/Group")' in builder_source
    assert '.exam-page{break-before:page;min-height:230mm}' in html
    assert html.count('<main>') == 1


def test_chapter_two_pdf_export_requires_complete_mathjax_document(tmp_path: Path):
    from full.tools.build_chapter_02_mathjax_handout import (
        assert_mathjax_ready,
        rendered_dom,
        write_html,
    )

    dom = rendered_dom(write_html(tmp_path / "chapter-two.html"))
    assert_mathjax_ready(dom)
