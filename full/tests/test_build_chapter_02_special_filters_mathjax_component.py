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


def test_special_filters_restore_dtmf_keypad_table_and_notch_zero_pole_response(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")

    assert 'data-table="dtmf-keypad"' in html
    assert "941 Hz" in html and "1633 Hz" in html
    assert 'data-plot="notch-zero-pole-response"' in html
    assert 'alt="50 Hz 陷波器的零极点与幅频响应"' in html


def test_special_filters_render_resonator_geometry_and_bandpass_response_from_real_data(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")

    assert 'data-plot="resonator-pole-zero-response"' in html
    assert 'data-plot="bandpass-resonator-response"' in html
    assert 'alt="谐振器极点半径与频率选择性"' in html
    assert 'alt="二阶带通谐振器的幅频响应"' in html
    assert "极点半径越接近单位圆，谐振峰越尖" in html


def test_special_filters_keep_source_design_conditions_and_notch_example(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")
    assert r"H(z)=\frac{A}{(1-re^{j\omega_0}z^{-1})(1-re^{-j\omega_0}z^{-1})}" in html
    assert r"\omega_0=\frac{\pi}{2}" in html
    assert r"\omega=\frac{4\pi}{9}" in html
    assert r"r^2=0.7" in html and r"G=0.15" in html
    assert r"\omega_1=2\pi\frac{852}{8000}=0.213\pi" in html
    assert r"\omega_2=2\pi\frac{1336}{8000}=0.334\pi" in html
    assert r"\omega_0=2\pi\frac{50}{1000}=0.1\pi" in html
    assert r"H(z)=\frac{1}{3.9}\frac{(z-e^{j\omega_0})(z-e^{-j\omega_0})}{z^2}" in html
    assert "有限字长会使陷波中心偏移" in html
    assert "Matlab" not in html and "MATLAB" not in html


def test_special_filters_keep_inverse_system_and_minimum_phase_factorization(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")
    assert r"H_i(z)=\frac{1}{H(z)}" in html
    assert r"H(z)H_i(z)=1" in html
    assert r"H(z)=\frac{1-3z^{-1}}{1-\frac{3}{4}z^{-1}}" in html
    assert r"H_{\min}(z)=3\frac{z-\frac{1}{3}}{z-\frac{3}{4}}" in html
    assert r"H_{\mathrm{ap}}(z)=\frac{z-3}{3z-1}" in html


def test_special_filters_keep_allpass_section_phase_and_group_delay_relationships(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")

    assert r"\theta_i(\omega)=-\omega-2\arctan" in html
    assert r"\operatorname{grd}_i(\omega)" in html
    assert r"\frac{1-r^2}{1+r^2-2r\cos(\omega-\theta)}" in html
    assert 'data-plot="allpass-phase-group-delay"' in html
    assert 'alt="一阶全通节的幅度、相位与群延迟"' in html


def test_special_filters_restore_minimum_phase_compensation_topology(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")

    assert 'data-diagram="minimum-phase-compensation"' in html
    assert r"H_d(z)=H_{d\min}(z)H_{\mathrm{ap}}(z)" in html
    assert r"H_c(z)=\frac{1}{H_{d\min}(z)}" in html
    assert r"G(z)=H_d(z)H_c(z)=H_{\mathrm{ap}}(z)" in html


def test_special_filters_compare_engineering_filter_algorithms_with_real_data(tmp_path: Path):
    from full.tools.build_chapter_02_special_filters_mathjax_component import write_html

    html = write_html(tmp_path / "special-filters.html").read_text(encoding="utf-8")

    assert 'data-plot="engineering-filter-comparison"' in html
    assert 'alt="限幅、中值与滑动平均滤波的实际效果对比"' in html
    assert "阈值限幅、中值和滑动平均三种方法" in html
