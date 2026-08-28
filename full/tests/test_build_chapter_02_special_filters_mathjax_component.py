from pathlib import Path


def test_special_filters_keep_core_theory_without_matlab(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")
    assert "tex-mml-chtml.js" in html
    assert "page-break-after:always" not in html
    assert r"\frac{1}{2}(1+z^{-1})" in html
    assert r"\frac{1}{2}(1-z^{-1})" in html
    assert r"H(z)=\frac{1-a}{2}\frac{z+1}{z-a}" in html
    assert r"\cos\omega_c=\frac{4a-a^2-1}{2a}" in html
    assert r"\omega_c\approx1-a" in html
    assert r"z=e^{\pm j\omega_0}" in html
    assert r"\left|H_{\mathrm{ap}}(e^{j\omega})\right|=1" in html
    assert r"H(z)=H_{\min}(z)H_{\mathrm{ap}}(z)" in html
    assert "MATLAB" not in html and "plot(" not in html
    assert "drawImage" not in html


def test_special_filters_include_first_order_bandwidth_and_design_example(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")
    assert r"\omega_c=\arccos\left(\frac{2a}{1+a^2}\right)" in html
    assert r"0.0628&lt;\omega_c&lt;0.5\pi" in html
    assert r"a=0.9" in html
    assert r"H(z)=0.05\frac{1+z^{-1}}{1-0.9z^{-1}}" in html
    assert r"y(n)=0.9y(n-1)+0.05x(n)+0.05x(n-1)" in html
    assert 'alt="一阶低通滤波器的零极点图"' in html
    assert 'alt="10 Hz 与 250 Hz 输入、输出的离散序列对比"' in html
    assert 'alt="一阶低通滤波前后的离散频谱"' in html


def test_special_filters_keep_resonator_dtmf_and_engineering_filtering_body(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")
    assert "数字谐振器" in html
    assert r"p_{1,2}=re^{\pm j\omega_0}" in html
    assert "DTMF" in html
    assert r"\omega_i=2\pi\frac{f_i}{f_s}" in html
    assert "限幅滤波" in html
    assert "中值滤波" in html
    assert "滑动平均" in html
