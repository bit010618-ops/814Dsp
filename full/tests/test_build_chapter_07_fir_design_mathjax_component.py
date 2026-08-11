from pathlib import Path


def test_chapter_seven_component_covers_four_source_sections(tmp_path: Path):
    from full.tools import build_chapter_07_fir_design_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-07.html").read_text(encoding="utf-8")

    titles = (
        "7.1 线性相位 FIR 数字滤波器的条件和特点",
        "7.2 利用窗函数法设计 FIR 滤波器",
        "7.3 利用频率采样法设计 FIR 滤波器",
        "7.4 利用等波纹逼近法设计 FIR 滤波器",
    )
    positions = [html.index(title) for title in titles]
    assert positions == sorted(positions)
    assert r"h(n)&=\delta(n-\tau)" in html
    assert r"H\!\left(e^{j\omega}\right)&=e^{-j\tau\omega}" in html
    assert r"\tau_g(\omega)&=-\frac{\mathrm{d}\theta(\omega)}{\mathrm{d}\omega}=\tau" in html
    assert r"H\!\left(e^{j\omega}\right)&=\pm\left|H\!\left(e^{j\omega}\right)\right|e^{j\theta(\omega)}" in html
    assert r"\theta(\omega)&=-\tau\omega" in html
    assert r"\theta(\omega)&=\beta_0-\tau\omega" in html
    assert r"\beta_0&=\pm\frac{\pi}{2}" in html
    assert r"H(\omega)\cos(\omega\tau)&=\sum_{n=0}^{N-1}h(n)\cos(\omega n)" in html
    assert r"H(\omega)\sin(\omega\tau)&=\sum_{n=0}^{N-1}h(n)\sin(\omega n)" in html
    assert r"\sum_{n=0}^{N-1}h(n)\sin\!\left[(n-\tau)\omega\right]=0" in html
    assert r"\tau=\frac{N-1}{2}" in html
    assert r"h(n)=h(N-1-n)" in html
    assert r"\sum_{n=0}^{N-1}h(n)\sin\!\left[\beta_0+(n-\tau)\omega\right]=0" in html
    assert r"h(n)=-h(N-1-n)" in html
    assert r"H(z)=\pm z^{-(N-1)}H\!\left(z^{-1}\right)" in html
    assert r"H\!\left(e^{j\omega}\right)&=e^{-j\frac{N-1}{2}\omega}H_0(\omega)" in html
    assert r"H_0(\omega)&=\sum_{n=0}^{N-1}h(n)\cos\!\left[\left(\frac{N-1}{2}-n\right)\omega\right]" in html
    assert r"H_0(\omega)&=j\sum_{n=0}^{N-1}h(n)\sin\!\left[\left(\frac{N-1}{2}-n\right)\omega\right]" in html
    assert r"H_{\mathrm{I}}(\omega)&=h(M)+2\sum_{m=1}^{M}h(M-m)\cos(m\omega)" in html
    assert r"H_{\mathrm{II}}(\omega)&=2\sum_{m=1}^{M}h(M-m)\cos\!\left[\left(m-\frac{1}{2}\right)\omega\right]" in html
    assert r"H_{\mathrm{III}}(\omega)&=2\sum_{m=1}^{M}h(M-m)\sin(m\omega)" in html
    assert r"H_{\mathrm{IV}}(\omega)&=2\sum_{m=1}^{M}h(M-m)\sin\!\left[\left(m-\frac{1}{2}\right)\omega\right]" in html
    assert r"z=-1,\quad z=0.5,\quad z=0.5e^{j\pi/4}" in html
    assert r"N-1=7,\qquad \tau=\frac{N-1}{2}=3.5" in html
    assert "R_N(n)=\n\\begin{cases}" in html
    assert r"\frac{1-e^{-j\omega N}}{1-e^{-j\omega}}" in html
    assert r"e^{-j\omega\frac{N-1}{2}}\frac{\sin(N\omega/2)}{\sin(\omega/2)}" in html
    assert r"\omega_c-\frac{2\pi}{N}\lesssim\omega\lesssim\omega_c+\frac{2\pi}{N}" in html
    assert "w_{\\mathrm{tri}}(n)&=\n\\begin{cases}" in html
    assert r"w_{\mathrm{Han}}(n)&=\frac{1}{2}\left[1-\cos\!\left(\frac{2\pi n}{N-1}\right)\right]R_N(n)" in html
    assert r"w_{\mathrm{Ham}}(n)&=\left[0.54-0.46\cos\!\left(\frac{2\pi n}{N-1}\right)\right]R_N(n)" in html
    assert r"w_{\mathrm{Blk}}(n)&=\left[0.42-0.5\cos\!\left(\frac{2\pi n}{N-1}\right)+0.08\cos\!\left(\frac{4\pi n}{N-1}\right)\right]R_N(n)" in html
    assert r"\omega_p&=2\pi\frac{f_p}{f_s}=0.2\pi" in html
    assert r"\Delta\omega&=\left|\omega_{st}-\omega_p\right|=0.2\pi" in html
    assert r"N=\frac{6.6\pi}{\Delta\omega}=\frac{6.6\pi}{0.2\pi}=33" in html
    assert r"\tau=\frac{N-1}{2}=16" in html
    assert r"\sin\!\left[0.3\pi(n-16)\right]" in html
    assert r"R_{33}(n)" in html
    assert r"\sin\!\left[\pi(n-\tau)\right]-\sin\!\left[\omega_c(n-\tau)\right]" in html
    assert r"\sin\!\left[\omega_2(n-\tau)\right]-\sin\!\left[\omega_1(n-\tau)\right]" in html
    assert r"\sin\!\left[\pi(n-\tau)\right]+\sin\!\left[\omega_1(n-\tau)\right]-\sin\!\left[\omega_2(n-\tau)\right]" in html
    assert r"h(n)=\pm h(N-1-n)" in html
    assert r"h(n)=h_d(n)w(n)" in html
    assert r"h(n)=\frac{1}{N}\sum_{k=0}^{N-1}H(k)W_N^{-nk}" in html
    assert "MATLAB" not in html
    assert "真题" not in html
