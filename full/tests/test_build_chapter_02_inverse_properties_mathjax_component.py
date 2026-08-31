from pathlib import Path


def test_inverse_and_properties_component_is_one_mathjax_flow(tmp_path: Path):
    from full.tools.build_chapter_02_inverse_properties_mathjax_component import write_html

    html = write_html(tmp_path / "inverse-properties.html").read_text(encoding="utf-8")

    assert "tex-mml-chtml.js" in html
    assert "page-break-after:always" not in html
    assert r"\oint_C X(z)z^{n-1}\,\mathrm{d}z" in html
    assert r"\mathcal{Z}\{x(n-m)\}=z^{-m}X(z)" in html
    assert r"Y(z)=X(z)H(z)" in html
    assert r"\mathcal{Z}\{nx(n)\}=-z\frac{\mathrm{d}X(z)}{\mathrm{d}z}" in html
    assert r"A_k=\left.\left(1-p_kz^{-1}\right)X(z)\right|_{z=p_k}" in html
    assert r"C_{\ell,r}=\frac{1}{(q_\ell-r)!}" in html
    assert r"\left.\frac{\mathrm{d}^{q_\ell-r}}{\mathrm{d}z^{q_\ell-r}}" in html
    assert "重极点系数的导数公式" in html
    assert r"x(n)&=\cos(\omega_0n)u(n)" in html
    assert r"\mathcal{Z}\{x^*(n)\}=X^*(z^*)" in html
    assert "性质、时域序列、z 域表达式与收敛域的对照表" in html
    assert r"\mathcal{Z}\{\delta(n-1)\}=z^{-1}" in html
    assert r"\mathcal{Z}\{a^nx(n)\}=X(a^{-1}z)" in html
    assert r"\operatorname{ROC}\{ax(n)+by(n)\}&\supseteq R_x\cap R_y" in html
    assert r"\max\!\left(R_x^-,R_y^-\right)<\left|z\right|<\min\!\left(R_x^+,R_y^+\right)" in html
    assert r"\operatorname{ROC}\{x(n-m)\}=R_x" in html
    assert "drawImage" not in html
    assert "<image" not in html
