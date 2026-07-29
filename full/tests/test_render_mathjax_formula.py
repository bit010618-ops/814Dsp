from full.tools.render_mathjax_formula import document


def test_cases_formula_is_sent_to_mathjax_as_one_complete_latex_unit():
    latex = r"""\delta(n)=
\begin{cases}
1, & n=0,\\
0, & n\ne 0.
\end{cases}"""
    page = document(latex)

    assert "mathjax@3" in page
    assert "\\begin{cases}" in page
    assert "\\end{cases}" in page
    assert "<main class=\"math-display\">" in page
