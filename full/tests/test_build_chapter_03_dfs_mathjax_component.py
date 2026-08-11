from pathlib import Path


def test_dfs_component_preserves_section_one_basics_and_example(tmp_path: Path):
    from full.tools import build_chapter_03_dfs_mathjax_component as component

    html = component.write_html(tmp_path / "chapter-03-dfs.html").read_text(encoding="utf-8")

    assert "3.1 离散傅里叶级数及其性质" in html
    assert r"\widetilde{X}(k)=\sum_{n=0}^{N-1}\widetilde{x}(n)W_N^{nk}" in html
    assert r"\widetilde{x}(n)=\frac{1}{N}\sum_{k=0}^{N-1}\widetilde{X}(k)W_N^{-nk}" in html
    assert r"W_N=e^{-j\frac{2\pi}{N}}" in html
    assert r"T_0=NT" in html
    assert r"f_s=NF_0" in html
    assert r"\frac{k}{N}=\frac{\omega}{2\pi}=\frac{f}{f_s}=\frac{\Omega}{\Omega_s}" in html
    assert "例题：8 点周期延拓序列的 DFS" in html
    assert r"\widetilde{x}_8(n)" in html
    assert r"\begin{aligned}" in html
    assert "MATLAB" not in html
