from full.tools.normalize_mathjax_inline import normalize_legacy_inline_math


def test_normalizes_inline_formulae_without_touching_display_formulae():
    source = (
        "<p>令 x(n) 满足 (W_N^r=\\pm1)，并取 (N=2^M)。</p>"
        '<div class="formula">\\[\\log_2(512)\\]</div>'
    )

    html = normalize_legacy_inline_math(source)

    assert r"\(x(n)\)" in html
    assert r"\(W_N^r=\pm1\)" in html
    assert r"\(N=2^M\)" in html
    assert r"\[\log_2(512)\]" in html
