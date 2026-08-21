# 循环索引记号确认

## Objective

全书循环索引一律采用完整括号外的周期下标记号，例如 `x\left((n+m)\right)_N` 与 `x^*\left((N-n)\right)_N`；不得在读者可见的循环索引中使用 `mod N`。

## Scope

- 仅替换循环索引的 `mod N` 写法；不改变相位主值等其他数学语义中的 `\pmod{2\pi}`。
- 公式必须仍由完整 LaTeX 交给 MathJax 渲染。

## Verification

- 第三章 DFT 组件必须覆盖移位、共轭对称和循环卷积三类循环索引。
- 回归检查禁止该组件出现 `\bmod`、`\operatorname{mod}`、`\mathrm{mod}` 或 `\pmod`。

## Result

- 已核查当前正文源码：循环移位、共轭对称和循环卷积均分别使用完整括号外的 `_N` 下标；未发现读者可见的 `mod N`。
- `full/tests/test_build_chapter_03_dft_mathjax_component.py`：2 passed。
