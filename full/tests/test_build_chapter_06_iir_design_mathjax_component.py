from pathlib import Path


def test_chapter_six_component_covers_the_five_source_sections(tmp_path: Path):
    from full.tools import build_chapter_06_iir_design_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-06.html").read_text(encoding="utf-8")

    titles = (
        "6.1 数字滤波器设计方法概述",
        "6.2 模拟滤波器的设计",
        "6.3 脉冲响应不变法",
        "6.4 双线性变换法",
        "6.5 IIR 数字滤波器设计方法小结",
    )
    positions = [html.index(title) for title in titles]
    assert positions == sorted(positions)
    assert r"H_a(s)H_a(-s)&=\frac{1}{1+\left(\frac{s}{j\Omega_c}\right)^{2N}}" in html
    assert r"s_k&=\Omega_c e^{j\pi\left(\frac12+\frac{2k+1}{2N}\right)}" in html
    assert r"H_a(s)&=\frac{\Omega_c^N}{\prod_{k=0}^{N-1}(s-s_k)}" in html
    assert r"p&=\frac{s}{\Omega_c},\qquad p_k=\frac{s_k}{\Omega_c}" in html
    assert r"H(p)&=\frac{1}{\prod_{k=0}^{N-1}(p-p_k)}" in html
    assert "巴特沃斯低通原型的频率归一化（用于将不同截止频率统一到单位截止频率下设计）" in html
    assert r"H_a(s)=H(z)\big|_{z=e^{sT}}" in html
    assert r"s=C\frac{1-z^{-1}}{1+z^{-1}}" in html
    assert r"C=\frac{\Omega_0}{\tan(\omega_0/2)}" in html
    assert r"s=\frac{2}{T}\frac{1-z^{-1}}{1+z^{-1}}" in html
    assert "IIR 数字滤波器的设计路线" in html
    assert 'class="iir-route-svg"' in html
    assert "脉冲响应不变法的时域采样路线" in html
    assert "双线性变换的平面映射" in html
    assert 'class="iir-plane-map-svg"' in html
    # SVG paint must be self-contained: WeasyPrint does not consistently
    # inherit outer-page SVG CSS, which otherwise turns the diagram blocks
    # and stable regions into opaque black fills in the exported PDF.
    assert 'class="box" x="28" y="72" width="128" height="64" rx="8" fill="#f4f7f8"' in html
    assert 'class="method" x="526" y="50" width="160" height="108" rx="8" fill="#fff6de"' in html
    assert 'class="stable" x="72" y="55" width="148" height="200" fill="#dceef4"' in html
    assert 'class="unit" cx="700" cy="155" r="100" fill="none" stroke="#7f929f"' in html
    assert 'class="axis" d="M55 155H368" fill="none" stroke="#174b73"' in html
    assert "MATLAB" not in html
    assert "真题" not in html
