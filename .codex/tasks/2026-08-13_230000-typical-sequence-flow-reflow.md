# 典型序列正文续排

## Objective

消除第一章典型序列中不必要的提前分页，使上页尚有可用空间时优先承接后续标题、公式与说明；技术图须完整、清晰，不以裁切或压缩至不可读为代价。

## Completed

- 将“矩形序列与实指数序列”段标记为可自然续排的正文段。
- 对续排图设定适中且可打印的最大宽度，避免后续图形过大而制造不必要的分页空白。
- 在整书样式中允许该段的图形作为可续排内容，并写入回归断言。

## Verification

- `python -m pytest -q full/tests/test_build_all_main_body.py`: `1 passed`。
- `tmp/dsp-main-body-visual-audit-v12.pdf`：MathJax `unrendered=[]`、`pageErrors=[]`。
- A4 视觉检查第 8--9 页：上页承接矩形序列的标题、公式、说明；下一页的矩形图、实指数图、正弦定义均完整清晰，无裁切、重叠或原始公式文本。

## Next

## 2026-08-13 Feedback-loop port correction

- User reported the feedback arrow in the first-order difference-equation structure diagram ended in empty space instead of the delay block.
- Root cause: the vertical feedback path used an arrow marker before reaching the `z^{-1}` module. Replaced it with a true right-side port connection: output branch -> vertical path -> horizontal path -> delay block -> gain block -> negative summing input.
- Verification: targeted regression test passed; the rebuilt full-book A4 PDF `tmp/dsp-main-body-arrow-port-v13.pdf` rendered MathJax with `unrendered=[]`, `pageErrors=[]`, and visual inspection of page 21 confirmed that all feedback arrows end on real ports.

继续整书正文的页级密度审计；仅当页尾不是章节末尾或训练书写页时，才把后续的非重复内容向上续排。
