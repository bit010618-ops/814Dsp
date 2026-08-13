from pathlib import Path


def test_chapter_five_component_covers_filter_structure_body_without_training(tmp_path: Path):
    from full.tools import build_chapter_05_filter_structures_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-05.html").read_text(encoding="utf-8")

    expected = (
        "5.1 数字滤波器概述",
        "5.2 IIR 数字滤波器结构",
        "直接 I 型与直接 II 型",
        "级联型、并联型与转置型 IIR 结构",
        "5.3 FIR 数字滤波器结构",
        "抽头延迟线直接型",
        "快速卷积型结构",
        "线性相位型结构",
    )
    positions = [html.index(title) for title in expected]
    assert positions == sorted(positions)
    assert r"H(z)=\frac{\sum_{m=0}^{M}b_m z^{-m}}{1+\sum_{n=1}^{N}a_n z^{-n}}" in html
    assert r"w(n)&=x(n)-\sum_{r=1}^{N}a_r w(n-r)" in html
    assert r"y(n)&=\sum_{m=0}^{M}b_m w(n-m)" in html
    assert r"H(z)=\left(1-z^{-N}\right)\frac{1}{N}" in html
    assert r"H_k(z)=\frac{H(k)}{1-W_N^{-k}z^{-1}}" in html
    assert r"H_r(z)=\left(1-r^N z^{-N}\right)\frac{1}{N}" in html
    assert r"z_k=re^{j2\pi k/N}" in html
    assert r"L=M+N-1" in html
    assert r"N=2L+1" in html
    assert r"x(n-m)\pm x(n-2L+m)" in html
    assert r"N=2L" in html
    assert r"x(n-m)\pm x(n-2L+1+m)" in html
    assert 'src="../assets/source-figures/ch05-fir-direct-form.png"' not in html
    for diagram in (
        "iir-direct-form-i",
        "iir-cascade-form",
        "fir-direct-form",
        "dtmf-parallel-form",
        "fir-cascade-form",
        "frequency-sampling-form",
        "fast-convolution-form",
    ):
        assert f'data-diagram="{diagram}"' in html
    assert "M420 98H555V145H562" in html
    assert "M420 232H555V185H562" in html
    assert 'x="0" y="130" width="120"' in html
    assert "h(N-2)" in html and "h(N-1)" in html
    for asset in (
        "ch05-cascade-form.png",
        "ch05-direct-form-i.png",
        "ch05-parallel-form.png",
        "ch05-fir-cascade-form.png",
        "ch05-frequency-sampling-form.png",
        "ch05-fast-convolution-form.png",
    ):
        assert asset not in html
    assert 'class="source-figure"' not in html
    assert "MATLAB" not in html
    assert "真题" not in html
