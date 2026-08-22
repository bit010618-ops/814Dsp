from pathlib import Path
from urllib.parse import unquote, urlparse

from full.tools.render_mathjax_formula import MATHJAX, document


def test_cases_formula_is_sent_to_mathjax_as_one_complete_latex_unit():
    latex = r"""\delta(n)=
\begin{cases}
1, & n=0,\\
0, & n\ne 0.
\end{cases}"""
    page = document(latex)

    script_url = urlparse(MATHJAX)
    assert script_url.scheme == "file"
    assert Path(unquote(script_url.path.lstrip("/"))).is_file()
    assert MATHJAX in page
    assert "cdn.jsdelivr.net" not in page
    assert "\\begin{cases}" in page
    assert "\\end{cases}" in page
    assert "<main class=\"math-display\">" in page


def test_fragment_page_is_a_single_centered_mathjax_formula_container():
    page = document(r"x=\frac{a}{b}", page_size="250pt 70pt", margin="0", centered=True)

    assert "@page { size: 250pt 70pt; margin: 0; }" in page
    assert "justify-content: center" in page
    assert "--no-pdf-header-footer" not in page
