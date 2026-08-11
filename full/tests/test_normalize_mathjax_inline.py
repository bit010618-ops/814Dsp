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


def test_does_not_rewrap_function_tokens_inside_a_parenthesized_math_group():
    html = normalize_legacy_inline_math(
        r"<p>输入顺序为 (x(0),x(4))，输出为 (X(0),\ldots,X(7))。</p>"
    )

    assert r"\(x(0),x(4)\)" in html
    assert r"\(X(0),\ldots,X(7)\)" in html
    assert r"\(\(x(0)\)" not in html
    assert r"\(\(X(0)\)" not in html


def test_does_not_rewrap_parentheses_inside_existing_inline_math():
    html = normalize_legacy_inline_math(
        r"<p>由 \(W_N^{kN/2}=e^{-j\pi k}=(-1)^k\) 可得。</p>"
    )

    assert r"\(W_N^{kN/2}=e^{-j\pi k}=(-1)^k\)" in html
    assert r"\(W_N^{kN/2}=e^{-j\pi k}=\(-1\)^k\)" not in html
