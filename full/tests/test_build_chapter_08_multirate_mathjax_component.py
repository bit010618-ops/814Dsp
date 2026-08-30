from pathlib import Path


def test_chapter_eight_component_covers_multirate_main_body(tmp_path: Path):
    from full.tools import build_chapter_08_multirate_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-08.html").read_text(encoding="utf-8")

    titles = (
        "8.1 信号的整数倍抽取",
        "8.2 信号的整数倍内插",
        "8.3 抽取与内插的频域关系",
        "8.4 有理数倍采样率变换与多相结构",
    )
    positions = [html.index(title) for title in titles]
    assert positions == sorted(positions)
    assert r"y(n)=x(Mn)" in html
    assert r"X_d\!\left(e^{j\omega}\right)=\frac{1}{M}" in html
    assert r"\frac{1}{2}X\!\left(e^{j\omega/2}\right)" in html
    assert r"w(n)&=\sum_{k=-\infty}^{\infty}h_d(k)x(n-k)" in html
    assert r"x_d(n)&=w(Mn)" in html
    assert r"h(n)&=\frac{\sin\!\left[\frac{\pi}{8}(n-20)\right]}" in html
    assert r"y(n)&=\sum_{k=-\infty}^{\infty}x(k)\delta(n-kL)" in html
    assert r"x_p(n)&=\begin{cases}" in html
    assert r"H_i\!\left(e^{j\omega}\right)&=\begin{cases}" in html
    assert "8 kHz" in html
    assert "16 kHz" in html
    assert r"h_i(n)&=2\frac{\sin(0.5\pi n)}{\pi n}" in html
    assert r"H_i\!\left(e^{j\omega}\right)&=" in html
    assert r"x_i(n)=\sum_{k=-\infty}^{\infty}x(k)" in html
    assert r"F_s'=\frac{L}{M}F_s" in html
    assert r"\omega_c=\min\!\left(\frac{\pi}{L},\frac{\pi}{M}\right)" in html
    assert r"\frac{147}{160}=\frac{7}{8}\cdot\frac{7}{5}\cdot\frac{3}{4}" in html
    assert r"y(n)&=\left\{\ldots,x_1(0),x_2(0),x_3(0)" in html
    assert "频分复用" in html
    assert "CD 音频兼容的采样率转换" in html
    assert "44.1 kHz" in html
    assert "16 bit" in html
    assert "24 bit" in html
    assert "非整数倍采样率转换" in html
    assert r"y(n)&=y_1(n)+y_2(n)+y_3(n)" in html
    assert r"X_i\!\left(e^{j3\omega}\right)" in html
    assert r"G_1(z),\ G_2(z),\ G_3(z)" in html
    assert r"44100=294\cdot50\cdot3" in html
    # Chapter-eight diagrams are lecture-native SVGs: no slide frame, watermark,
    # coloured teaching callouts, or raster crop may leak into the handout.
    for figure_id in (
        "decimation-spectrum-transform",
        "decimator-cascade",
        "interpolator-cascade",
        "rational-rate-converter",
    ):
        assert f'id="{figure_id}"' in html
    assert "../assets/source-figures/ch08-" not in html
    # The lower-right “amplitude halved” spectrum remains inside its own panel.
    assert 'M560 411L590 359L620 411' in html
    # Every spectrum panel has a complete textbook coordinate system: a
    # horizontal frequency axis and a separate upward amplitude axis.
    for vertical_axis in (
        'M96 195V112',
        'M560 195V112',
        'M560 411V328',
        'M96 411V328',
    ):
        assert vertical_axis in html
    assert html.count('>幅度</text>') == 4
    assert "MATLAB" not in html
    assert "真题" not in html
