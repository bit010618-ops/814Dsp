# 第二章补充真题第二批

## Objective

将已审计归入第二章的 2004 年第五题、2005 年填空第 4 小题与第十题按原题干纳入候选讲义，并提供完整详解、规范图形和 MathJax 公式渲染。

## Constraints

- 原题干不得改写；含水印的原卷结构图需按教材规范重绘，不复制水印。
- 题目每题独立作答页；答案自然续排。
- 公式导出必须通过完整 DOM 的 MathJax 检查。

## Status

Completed — 已纳入 2004 年第五题、2005 年第 4 小题与第十题；三题题干保持原文，详解使用 MathJax 整体渲染。2004 年结构图、稳定收敛域零极点图与 2005 年带阻幅频图均为带显式绘制属性的无水印矢量图，避免总讲义抽取组件主体时丢失 SVG 类样式。候选 PDF 已重建并在 160 dpi 下逐页检查新增内容；回归测试 6 项通过。

## Verification

- `full/tests/test_build_chapter_02_supplemental_training_batch_two_mathjax_component.py`
- `full/tests/test_build_chapter_02_mathjax_handout.py`
- 候选 PDF：`full/outputs/chapter_02_mathjax_handout.pdf`（36 页，仅为内部候选，不进入 `output/`）
